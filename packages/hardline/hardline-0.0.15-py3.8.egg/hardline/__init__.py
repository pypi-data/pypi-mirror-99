
import urllib
import sys

import configparser
from ipaddress import ip_network, ip_address
import select
import threading
import re
import weakref
import os
import socket
import time
import ssl
import collections
import binascii
import traceback
import random
import sqlite3
import json
import random
import uuid
import hmac
import base64
from nacl.hash import blake2b
import nacl
import hashlib
import stat
import struct
from . import util
from .cachingproxy import CachingProxy

services = weakref.WeakValueDictionary()

socket.setdefaulttimeout(5)



def createWifiChecker():
    """Detects if we are on something like WiFi, and if we have sufficient battery power to keep going.

    But if we aren't on android at all, assume that we are always connected to a LAN, even htough there are 4g laptops.
    don't use for anything critical because of that.

    """
    def alwaysTrue():
        return True

    try:
        import kivy.utils
    except ImportError:
        return alwaysTrue

    if kivy.utils.platform != 'android':
        return alwaysTrue

    from plyer import wifi
    from plyer import battery

    def check_connectivity():
        if battery.status['isCharging'] or battery.status['percentage'] > 30:
            return wifi.is_connected()
        else:
            return False

    return check_connectivity()


isOnLan = createWifiChecker()


P2P_PORT = 7009

dhtlock = threading.RLock()

# Both of these are hosted in the cloud.  The second one is Yggdrasil mesh version, in case you should find yourself without internet but having mesh
DHT_PROXIES = [
    "http://185.198.26.230:4223/",
    "http://[200:6a4e:d4a9:d773:388:b367:481:5382]:4223/"
    # "http://dhtproxy.jami.net/"
]


# Mutable containers we can pass to services
WANPortContainer = [0]
ExternalAddrs = ['']

try:
    from android.storage import app_storage_path
    settings_path = app_storage_path()
except:
    settings_path = os.path.expanduser('~/.hardlinep2p/')


try:
    from jnius import autoclass, cast
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Environment = autoclass('android.os.Environment')
    context = cast('android.content.Context', PythonActivity.mActivity)

    r = context.getExternalFilesDir(
        Environment.getDataDirectory().getAbsolutePath()
    ).getAbsolutePath()

    user_services_dir = os.path.join(r, "services")
    proxy_cache_root = os.path.join(r, "proxycache")

except:
    user_services_dir = os.path.expanduser('~/.hardlinep2p/services/')
    proxy_cache_root = os.path.expanduser('~/.hardlinep2p/proxycache/')

# clientidkeyfile = os.path.join(os.path.expanduser(settings_path), "clientid.txt")

# #This client ID is only ever sent in hashed form to remote sites.  It cannot be used to track you unless they know the raw unhashed key
# if not os.path.exists(clientidkeyfile):
#     with os.path.open(clientidkeyfile, "w") as f:
#         f.write(str(uuid.uuid4()))

# with os.path.open(clientidkeyfile) as f:
#     clientUUID = f.read()


try:
    os.makedirs(os.path.expanduser(settings_path))
except Exception:
    pass

DB_PATH = os.path.join(os.path.expanduser(settings_path), "peers.db")

print("Peers DB: "+DB_PATH)
discoveryDB = sqlite3.connect(DB_PATH)
c = discoveryDB.cursor()

# Create table which we will use to store our peers.
c.execute('''CREATE TABLE IF NOT EXISTS peers
             (serviceID text, info text)''')


dbLock = threading.RLock()


# LThread local storage to store DB connections, we can only  use each from one thread.
dbLocal = threading.local()


try:
    import netifaces
except:
    netifaces = None
    print("Did not find netifaces, mesh-awareness disabled")


def getWanHostsString():
    # String describing how a node might access us from the public internet, as a prioritized comma separated list.

    meshAddress = ''
    l = []
    if netifaces:
        x = netifaces.interfaces()
        for i in x:

            y = netifaces.ifaddresses(i)

            if netifaces.AF_INET6 in y:
                y2 = y[netifaces.AF_INET6]
                for j in y2:
                    l.append(j['addr'].split("%")[0])

        for i in l:
            # Specifically look for the addresses the Yggdrasil mesh uses
            if ip_address(i) in ip_network("200::/7"):
                meshAddress = '['+i+"]:"+str(WANPortContainer[0])

    s = []
    if ExternalAddrs[0]:
        s.append(ExternalAddrs[0]+":"+str(WANPortContainer[0]))
    if meshAddress:
        s.append(meshAddress)

    return ",".join(s)


def getDB():
    try:
        return dbLocal.db
    except:
        dbLocal.db = sqlite3.connect(DB_PATH)
        return dbLocal.db


def parseHostsList(p):
    "Parse a comma separated list of hosts which may include bot ipv4 and ipv6, into a list of host port tuples "
    p = p.replace("[", '').replace("]", "")
    d = p.split(",")
    l = []
    for i in d:
        i = i.strip()
        # This could be IPv6 or IPv4, and if it's 4, we will need to take the last : separated part
        # as the port, and reassemble the rest.
        i = i.split(":")
        p = int(i[-1])
        h = ":".join(i[:-1])
        l.append((h, p))
    return l


class DiscoveryPeer(util.LPDPeer):
    def __init__(self):
        util.LPDPeer.__init__(self, "HARDLINE-SERVICE",
                              "HARDLINE-SEARCH", server=False)

    def onDiscovery(self, hash, host, port, title):
        # Local discovery has priority zero
        cleanDiscoveries()

        # Assign the discovery data to the cache object
        getDiscoveryCacheFor(hash).LPDcacheRecord = (
            (host, port), time.time(), 0, title)


discoveryPeer = DiscoveryPeer()


class DiscoveryCache():
    "Manage discovery for one remote peer, including requesting updated data as needed."

    def __init__(self, hash):
        self.infohash = hash

        # We treat local discovery differently and cache in RAM, because it can change ofen
        # As we roam off the wifi, and it is not secure.
        self.LPDcacheRecord = (None, 0, 10, '')

        # Don't cache DHT all all, if gives the same info we will get and cache over SSL
        # But DO rate limit it.
        self.lastTriedDHT = 0

    def doDHTLookup(self):
        """Perform a DHT lookup using the public OpenDHT proxy service.  We don't cache the result of this, we just rate limit.
           and let the connection thread cache the same data that it will get via the server.

           This is pretty separate from the normal caching.
        """
        # Lock is needed mostly to avoid confusion in ratelimit logic when debugging

        with dhtlock:
            import requests
            if self.lastTriedDHT > (time.time()-60):
                # Rate limit queries to the public DHT proxy to one per minute
                return []

            self.lastTriedDHT = time.time()

            # Rolling code changes the DHT key every 24 hours, ensuring that we don't heavily load down any particular
            # DHT node for more than a day, if there is somehow an incredibly popular site.
            # It also gives less information to people who don't know the unhashed ID, who may want to
            # spy on when your service is up, or some crap like that.
            timePeriod = struct.pack("<Q", int(time.time()/(3600*24)))
            rollingCode = blake2b(bytes.fromhex(self.infohash)+timePeriod,
                                  encoder=nacl.encoding.RawEncoder())[:20]
            # Use SHA1 here as it is openDHT custom
            k = hashlib.sha1(rollingCode.hex().encode()).digest()[:20].hex()

            r = None
            lines = []
            # Prioritized DHT proxies list
            for i in DHT_PROXIES:
                print("Trying DHT Proxy request to: "+i+k)
                try:
                    r = requests.get(i+k, timeout=20, stream=True)
                    for j in r.iter_lines():
                        if j:
                            lines.append(j)
                            break
                    break
                except:
                    print(traceback.format_exc())
                    print("DHT Proxy request to: "+i+" failed for"+k)

            if lines:
                # This only tries one item, which is a little too easy to DoS, but that's also part of the inherent problem with DHTs.
                # By randomizing, we allow for some very basic load balancing, although nodes will stay pinned to their chosen node until failure.
                d = base64.b64decode(json.loads(
                    random.choice(lines).strip())['data']).decode()

                # Return a list of candidates to try
                return parseHostsList(d)

            return []

    def doLookup(self):
        try:
            discoveryPeer.search(self.infohash)
        except:
            print(traceback.format_exc())

    def get(self, invalidate=False):

        if invalidate:
            self.LPDcacheRecord = (None, 0, 10, '')

        # Try a local serach
        for i in range(0, 4):

            # Look in the cache first
            x = self.LPDcacheRecord
            if x[1] > (time.time() - 60):
                return [x[0]]

            self.doLookup()
            # Wait a bit for replies, waiting a little longer every time
            time.sleep(i*0.1 + 0.05)

        # Local search failed, we haven't seen a packet from them, so we are probably not on their network.
        # lets try a stored WAN address search, maybe we have a record we can use?
        with dbLock:
            discoveryDB = getDB()
            c = discoveryDB.cursor()
            c = discoveryDB.cursor()
            d = c.execute("select info from peers where serviceID=?",
                          (self.infohash,)).fetchone()
            if d:
                p = json.loads(d[0])['WANHosts']
                # Return a list of candidates to try
                return parseHostsList(p)
        return []


discoveries = collections.OrderedDict()
discoveriesLock = threading.RLock()


def cleanDiscoveries():
    if len(discoveries) > 128:
        with discoveriesLock:
            if len(discoveries) > 128:
                for i in range(16):
                    discoveries.popitem(True)


def getDiscoveryCacheFor(key):
    "this function is not perfectlu threadsafe and may very rarely fail, that's fine for now, it's still way more reliable than the network itself."
    if not key in discoveries:
        with discoveriesLock:
            discoveries[key] = DiscoveryCache(key)

    return discoveries[key]


def getAllDiscoveries():
    "Part of public API.  Return a list of discoveries."
    l = []
    with discoveriesLock:
        for i in discoveries:
            x = discoveries[i]

            if x.LPDcacheRecord[1] > (time.time()-10*60):
                l.append({
                    'title':  x.LPDcacheRecord[3],
                    'hash':  i,
                    'from_ip': x.LPDcacheRecord[0][0]
                })
    return l

# Not threadsafe, but we rely on the application anyway, to handle the unreliable network


def discover(key, refresh=False):
    cleanDiscoveries()
    return getDiscoveryCacheFor(key).get(refresh)


def dhtDiscover(key, refresh=False):
    cleanDiscoveries()
    return getDiscoveryCacheFor(key).doDHTLookup()


def writeWanInfoToDatabase(infohash, hosts):
    # The device can tell us how to later find it even when we leave the WAN
    # TODO: People can give us fake values, which we will then save. Solution: digitally sign.
    if hosts:
        print("Got WAN connection info from server")
        with dbLock:
            # Todo don't just reopen a new connection like this
            discoveryDB = getDB()
            cur = discoveryDB.cursor()
            d = cur.execute(
                "select info from peers where serviceid=?", (infohash,)).fetchone()
            if d:
                # No change has been made
                try:
                    d = json.loads(d[0])['WANHosts']
                    if d == hosts:
                        return
                except:
                    print(traceback.format_exc())
                print("Writing updated info to DB")
                cur.execute("update peers set info=? where serviceid=?",
                            (json.dumps({"WANHosts": hosts}), infohash))
            else:
                print("Writing ne host info to DB")
                cur.execute("insert into peers values (?,?)",
                            (infohash, json.dumps({"WANHosts": hosts})))
            discoveryDB.commit()


class InstanceTracker():
    pass


connections = weakref.WeakValueDictionary()


class Service():
    def __init__(self, cert, destination, port, info={'title': ''}, friendlyName=None, cacheSettings={}):
        global P2P_PORT

        self.certfile = cert
        self.dest = destination+":"+str(port)

        self.closed = False

        # This is a name we use in GUI service listings for display
        self.friendlyName = friendlyName
        # #Used for tracking who we have directly connected to on the lan.
        # #For GDPR reasons, we do not store data besides the anonymous ID and the fact that they connected at some point.
        # self.lanClientsFile = self.certfile+".lanclients"
        # self.lanClientsLock = threading.Lock()

        # if os.path.exists(self.lanClientsFile):
        #     with open(self.lanClientsFile) as f:
        #         self.lanClients= {i.strip():None for i in f.read.replace("\r","").split("\n") if i.strip}
        # self.la

        # #Forbids connection by anyone who has not connected via our LAN directly before.  Weak security,
        # #But better than nothing.
        # self.noStrangers = nostrangers

        if os.path.exists(cert+'.hash'):
            with open(cert+'.hash', "r") as f:
                s = f.read()

                # Allow an extremely weak password authentication for a marginal amount of extra security.
                s = s.split("-")

                if len(s) > 1:
                    pwd = s[0]
                else:
                    pwd = ''

                self.keyhash = bytes.fromhex(s[-1])
                self.password = pwd
        else:
            self.cert_gen(cert)

        # Should there be a proxy dir set up, we run an in-process caching proxy
        # Just for that.  It's mostly an extra convenience and not something
        # Deeply integrated.
        self.cachingProxy = None
        proxyDir = cacheSettings.get("directory")
        if proxyDir:
            proxyDir = os.path.join(proxy_cache_root, proxyDir)

            # No spurious port 80 that isn't needed and breaks stuff
            if port and not int(port) == 80:
                dest = destination+":"+str(port)
            else:
                dest = destination
            yes = ('yes','true','on','Yes','True','On','TRUE')
            self.cachingProxy = CachingProxy(dest, proxyDir, maxAge=cacheSettings.get("maxAge"), 
            maxSize=cacheSettings.get("maxSize"),
            downloadRateLimit=cacheSettings.get("downloadRateLimit"), 
            allowListing=cacheSettings.get("allowListing") in yes,
            dynamicContent=cacheSettings.get("dynamicContent") in yes)

            for i in range(0, 10):
                if self.cachingProxy.port:
                    break
                time.sleep(1)
            else:
                raise RuntimeError("Proxy did not start")

            self.dest = "localhost:"+str(self.cachingProxy.port)

        services[self.keyhash.hex()] = self

        self.lpd = util.LPDPeer("HARDLINE-SERVICE", "HARDLINE-SEARCH")
        self.lpd.register(self.password+"-"+self.keyhash.hex(),
                          WANPortContainer, info)

    def close(self):
        global P2P_PORT
        try:
            services.pop(self.keyhash.hex())
        except KeyError:
            pass

        if self.cachingProxy:
            try:
                self.cachingProxy.server.shutdown()
                self.cachingProxy = None
            except KeyError:
                pass

        self.closed = True

        self.lpd.unregister(self.password+"-" +
                            self.keyhash.hex())

    def dhtPublish(self, node):
        # Publish this service to the DHT for WAN discovery.

        timePeriod = struct.pack("<Q", int(time.time()/(3600*24)))
        rollingCode = blake2b(self.keyhash+timePeriod,
                              encoder=nacl.encoding.RawEncoder())[:20]

        # We never actually know if this will be available on the platform or not
        if node:
            try:
                import opendht as dht

                with dhtlock:
                    node.put(dht.InfoHash.get(rollingCode.hex()),
                             dht.Value(getWanHostsString().encode()))
            except Exception:
                print("Could not use local DHT node")
                print(traceback.format_exc())
            return

        # Using a DHT proxy we can host a site without actually using the DHT directly.
        # This is for future direct-from-android hosting.
        for i in DHT_PROXIES:
            import requests
            try:
                data = {"data": base64.b64encode(
                    getWanHostsString()).decode(), "id": "id 1", "seq": 0, "type": 3}
                url = i+hashlib.sha1(rollingCode.hex().encode()
                                     ).digest()[:20].hex()
                r = requests.post(url, data=data)
                r.raise_for_status()
                break
            except Exception:
                print(traceback.format_exc())

    def handleConnection(self, sock):
        "Handle incoming encrypted connection from another hardline instance.  The root server code has alreadt recieved the SNI and has dispatched it to us"
        # Swap out the contetx,  now that we know the service they want, we need to serve the right certificate
        p2p_server_context = ssl.create_default_context(
            ssl.Purpose.CLIENT_AUTH)
        p2p_server_context.options |= ssl.OP_NO_TLSv1
        p2p_server_context.options |= ssl.OP_NO_TLSv1_1

        if not os.path.exists(self.certfile):
            raise RuntimeError("No cert")
        if not os.path.exists(self.certfile+".private"):
            raise RuntimeError("No key")
        p2p_server_context.load_cert_chain(
            certfile=self.certfile, keyfile=self.certfile+".private")
        sock.context = p2p_server_context

    def handleConnectionReady(self, sock):
        def f():
            conn = socket.socket(socket.AF_INET)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15)
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

            # Use weakrefs to track how many of these are running
            instanceTracker = InstanceTracker()

            connections[time.time()] = instanceTracker

            # TODO maybe make this configurable
            if len(connections) > 320:
                raise RuntimeError(
                    "Too many incoming P2P connections all at once")

            h, p = self.dest.split(":")[-2:]
            conn.connect((h, int(p)))

            # Wait for ready
            for i in range(50):
                r, w, x = select.select([], [sock], [], 0.1)
                if w:
                    break

            sendOOB = {

            }

            # Using a list as an easy mutable global.
            # Should there be an external addr we can tell them about, we stuff it in our header so they can memorize it.
            # Note that this is secured via the same SSH tunnel, only the real server can send this.
            if ExternalAddrs[0]:
                sendOOB['WANHosts'] = getWanHostsString()

            # Send our oob data header
            sock.send(json.dumps(sendOOB, separators=(',', ':')).encode()+b"\n")

            oob = b''

            # The first part of the data is reserved for an OOB header
            while(1):
                if self.closed:
                    raise RuntimeError("Closed at server side")
                r, w, x = select.select([sock, ], [], [], 1)
                if r:
                    oob += sock.recv(4096)
                    if b"\n" in oob:
                        break

            oob, overflow = oob.split(b"\n")

            if self.password:
                oob = json.loads(oob)
                if not hmac.compare_digest(self.password, oob['password']):
                    raise RuntimeError(
                        "This Service requires a password component to the name, which must match")

            # Send any data that was after the newline
            conn.send(overflow)

            while(1):
                if self.closed:
                    raise RuntimeError("Closed at server side")
                r, w, x = select.select([sock, conn], [], [], 1)

                # Whichever one has data, shove it down the other one
                for i in r:
                    try:
                        if i == sock:
                            d = i.recv(4096)
                            if d:
                                conn.send(d)
                            else:
                                raise ValueError(
                                    "Zero length read, probably closed")
                        else:
                            d = i.recv(4096)
                            if d:
                                sock.send(d)
                            else:
                                raise ValueError(
                                    "Zero length read, probably closed")
                    except:
                        print(traceback.format_exc())

                        print("socket closing")
                        try:
                            sock.close()
                        except:
                            pass
                        try:
                            conn.close()
                        except:
                            pass
                        return

        t = threading.Thread(target=f, daemon=True)
        t.start()

    # def addKnownLANClient(self,l):
    #     with lanClientsLock:
    #         self.lanClients[l].append(l)
    #         #Put line endings befio
    #         with open(self.lanClientsFile,"a+") as f:
    #             f.write("\r\n"+l)

    def cert_gen(self, fn):
        # None of these parameters matter.  We will be using the hash directly, comparing
        # exact certificate identity
        from OpenSSL import crypto, SSL

        emailAddress = "emailAddress"
        commonName = "commonName"
        countryName = "NT"
        localityName = "localityName"
        stateOrProvinceName = "stateOrProvinceName"
        organizationName = "organizationName"
        organizationUnitName = "organizationUnitName"
        serialNumber = 0
        validityStartInSeconds = 0
        validityEndInSeconds = 100*365*24*60*60
        KEY_FILE = fn+".private"
        CERT_FILE = fn
        # can look at generated file using openssl:
        # openssl x509 -inform pem -in selfsigned.crt -noout -text
        # create a key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 4096)
        # create a self-signed cert
        cert = crypto.X509()
        cert.get_subject().C = countryName
        cert.get_subject().ST = stateOrProvinceName
        cert.get_subject().L = localityName
        cert.get_subject().O = organizationName
        cert.get_subject().OU = organizationUnitName
        cert.get_subject().CN = commonName
        cert.get_subject().emailAddress = emailAddress
        cert.set_serial_number(serialNumber)
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(validityEndInSeconds)
        cert.set_issuer(cert.get_subject())
        cert.set_pubkey(k)
        cert.sign(k, 'sha512')

        # This is NOT meant to be anyone's primary means of security!  It is only for a very basic
        # layer that keeps casual remote attackers out.   The password can also be reused to put a bit of freetext in the domain.
        # That is how insecure it is!!

        # Nonetheless it will probably stop most people IRL.

        # Also, this is not really base32, it's random freetext.  User could use any length he wants.
        self.password = base64.b32encode(
            os.urandom(8)).decode().replace("=", '').lower()

        with open(CERT_FILE, "wt") as f:
            f.write(crypto.dump_certificate(
                crypto.FILETYPE_PEM, cert).decode("utf-8"))
        os.chmod(CERT_FILE, stat.S_IRWXU)

        with open(KEY_FILE, "wt") as f:
            f.write(crypto.dump_privatekey(
                crypto.FILETYPE_PEM, k).decode("utf-8"))

        os.chmod(KEY_FILE, stat.S_IRWXU)

        with open(CERT_FILE+'.hash', "wt") as f:
            f.write(self.password + '-' + blake2b(crypto.dump_certificate(
                crypto.FILETYPE_ASN1, cert), encoder=nacl.encoding.RawEncoder())[:20].hex())
            self.keyhash = blake2b(crypto.dump_certificate(
                crypto.FILETYPE_ASN1, cert), encoder=nacl.encoding.RawEncoder())[:20]

        os.chmod(CERT_FILE+'.hash', stat.S_IRWXU)


def server_thread(sock):
    "Spawns a thread for the server that is meant to be accessed via localhost, and create the backend P2P"
    # In a thread, we are going to
    def f():
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

        rb = b''
        t = time.time()
        # Sniff for an HTTP host so we know who to connect to.
        # Normally we would use the SSL SNI, but the localhost conection doesn't have that.
        while time.time()-t < 5:
            r, w, x = select.select([sock], [], [], 1)
            if r:
                rb += sock.recv(4096)

                # Found it!
                x = re.search(b"^Host: *(.*?)$", rb, re.MULTILINE)
                if x:
                    destination = x.groups(1)[0].replace(b"\r", b'')
                    break
                if len(rb) > 10000:
                    raise RuntimeError("HTTP sniffing fail")

        x = destination.split(b".")

        # This is the service we want, identified by hex key hash.  SERVICE.localhost
        service = x[-2]

        fullservice = service

        # Look for a password component, as in password-service.localhost
        service = service.split(b"-")

        if len(service) > 1:
            password = service[0].decode().lower()
        else:
            password = ''

        service = service[-1].decode()

        # This is the location at which we actually find it.
        # We need to pack an entire hostname which could actually be an IP address, into a single subdomain level component
        # Use fullservice for discovery, the LPD code takes care of not actually sending the password part
        hosts = discover(fullservice.decode())

        conn = None

        def connect(to):
            # We do our own verification
            sk = ssl.create_default_context()

            sk.options |= ssl.OP_NO_TLSv1
            sk.options |= ssl.OP_NO_TLSv1_1

            sk.check_hostname = False
            sk.verify_mode = ssl.CERT_NONE
            sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # clientID = blake2b(clientUUID.encode()+service ,encoder=nacl.encoding.RawEncoder())[:20]

            # Use TCP keepalives here.  Note that this isn't really secure because it's at the TCP layer,
            # Someone could DoS it, but DoS is hard to stop no matter what.
            sock2.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock2.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5)
            sock2.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15)
            sock2.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

            conn = sk.wrap_socket(sock2, server_hostname=service)
            conn.connect(to)
            return conn
        try:
            # Try our discovered hosts
            for host in hosts:
                try:
                    connectingTo = host
                    print("trying", host)
                    conn = connect(host)
                    break
                except:
                    print(traceback.format_exc())
            else:
                # Retry discovery, this time refresh so we don't get old cached lan values
                for host in discover(fullservice.decode(), refresh=True):
                    try:
                        connectingTo = host
                        print("trying", host)
                        conn = connect(host)
                        break
                    except:
                        print(traceback.format_exc())
                else:
                    # Last resort we try using the DHT
                    for host in dhtDiscover(service):
                        try:
                            print("trying", host)
                            connectingTo = host
                            conn = connect(host)
                            break
                        except:
                            print(traceback.format_exc())
                    else:
                        raise RuntimeError(
                            "All saved host options and dht options failed:"+str(hosts))
        except:
            if conn:
                conn.close()
            raise
       # else:
            # We have failed, now we have to use DHT lookup

        c = conn.getpeercert(True)

        hashkey = blake2b(c, encoder=nacl.encoding.RawEncoder())[:20].hex()
        if not hashkey == service:
            raise ValueError("Server certificate does not match key in URL")

        # Wait for connection
        for i in range(50):
            r, w, x = select.select([], [conn], [], 0.1)
            if w:
                break

        sendOOB = {}
        if password:
            sendOOB['password'] = password
        # Send our oob data header to the other end of things.
        conn.send(json.dumps(sendOOB, separators=(',', ':')).encode()+b"\n")

        oob = b''

        # The first part of the data is reserved for an OOB header
        for i in range(0, 100):
            r, w, x = select.select([conn, ], [], [], 1)
            if r:
                oob += conn.recv(4096)
                if b"\n" in oob:
                    break
            time.sleep(0.01)

        oob, overflow = oob.split(b"\n")

        # Send any data that was after the newline, back up to the localhost client
        sock.send(overflow)

        oob = json.loads(oob)

        # The remote server is telling us how we can contact it in the future via WAN, should local discovery
        # fail.  We record this, indexed by the key hash.  Note that we do this inside the SSL channel
        # because we don't want anyone to make us write fake crap to our database
        if 'WANHosts' in oob:
            writeWanInfoToDatabase(fullservice.decode(), oob['WANHosts'])

        while(1):
            r, w, x = select.select(
                [sock, conn], [sock, conn] if rb else [], [], 1)
            # Send the traffic we had to buffer in order to sniff for the destination
            if rb:
                if w:
                    conn.send(rb)
                    rb = b''

            # Whichever one has data, shove it down the other one
            for i in r:
                try:
                    if i == sock:
                        d = i.recv(4096)
                        if d:
                            conn.send(d)
                        else:
                            raise ValueError(
                                "Zero length read, probably closed")
                    else:
                        d = i.recv(4096)
                        if d:
                            sock.send(d)
                        else:
                            raise ValueError(
                                "Zero length read, probably closed")
                except:
                    print(traceback.format_exc())

                    try:
                        sock.close()
                    except:
                        pass
                    try:
                        conn.close()
                    except:
                        pass

                    return

    t = threading.Thread(target=f, daemon=True)
    t.start()


def handleClient(sock):
    server_thread(sock)


def handleP2PClient(sock):
    def f():
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 5)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

        p2p_server_context = ssl.create_default_context(
            ssl.Purpose.CLIENT_AUTH)
        p2p_server_context.options |= ssl.OP_NO_TLSv1
        p2p_server_context.options |= ssl.OP_NO_TLSv1_1

        # Use this list to get the name
        l = []
        p2p_server_context.sni_callback = makeHelloHandler(l)
        conn = p2p_server_context.wrap_socket(sock, server_side=True)

        # handleP2PClientHello put the name in the list
        services[l[0]].handleConnectionReady(conn)

    threading.Thread(target=f, daemon=True).start()


def makeHelloHandler(l):
    def handleP2PClientHello(sock, name, ctd):
        if name in services:
            services[name].handleConnection(sock)
            l.append(name)
    return handleP2PClientHello


dhtContainer = [0]


lastUsedIPAPI = 0


# This loop just refreshes the WAN addresses every 8 minutes.
# We need this so we can send them for clients to store, to later connect to us.

# It also refreshes any OpenDHT keys that clients might have
def taskloop():
    global lastUsedIPAPI

    from . import upnpwrapper
    while 1:
        success = False
        try:
            a = upnpwrapper.getWANAddresses()
            if a:
                ExternalAddrs[0] = a[0]
                success = True
        except:
            print(traceback.format_exc())

        # If we can't get a UPNP listing we have to rely on a manual port mapping.
        if not success:
            # Don't hammer IP API for no reason if we don't actually have services to serve.
            if services and isOnLan():
                if time.time() > lastUsedIPAPI-40*60:
                    lastUsedIPAPI = time.time()
                    try:
                        import requests
                        r = requests.get("https://api.ipify.org/", timeout=5)
                        r.raise_for_status()
                        ExternalAddrs[0] = r.text
                        success = True
                    except:
                        print(traceback.format_exc())

                if not success:
                    ExternalAddrs[0] = ''

        try:
            for i in services:
                if isOnLan():
                    services[i].dhtPublish(dhtContainer[0])
        except:
            print(traceback.format_exc())

        time.sleep(8*60)


portMapping = None

running = True
exited = True


def stop():
    # Will not instant;y stop active connections
    global running, exited
    while not exited:
        running = False
        time.sleep(0.1)


cached_localport = 7008


def start(localport=None):
    global P2P_PORT, WANPort, portMapping, running, exited, cached_localport

    running = True

    ports = []

    localport = localport or cached_localport
    cached_localport = localport

    try:
        # This is the server context we use for localhost coms
        bindsocket = socket.socket()
        if localport:
            # Try for 30 seconds of waiting to see if the port becomes available.
            for i in range(30):
                try:
                    bindsocket.bind(('localhost', localport))
                    bindsocket.listen()
                    ports.append(bindsocket)
                    break
                except OSError:
                    if i < 9:
                        time.sleep(1)
                    else:
                        raise
    except Exception:
        bindsocket = None
        print("Failed to start localhost gateway.  Perhaps another Hardline instance is running.  Continuing as server only")

    # This is the server context we use for the remote coms, accepting incoming ssl connections from other instances and proxying them into
    # local services

    p2p_bindsocket = socket.socket()

    for i in range(30):
        try:
            p2p_bindsocket.bind(('0.0.0.0', P2P_PORT))
            p2p_bindsocket.listen()
            WANPortContainer[0] = P2P_PORT
            break
        except OSError:
            if i < 28:
                time.sleep(1)
                P2P_PORT += 1

            else:
                raise

    if services:
        from . import upnpwrapper

        # Start the d.   Node that we would really like to avoid actually having to use this,
        # So although we publish to it, we try local discovery and the local cache first.
        try:
            import opendht as dht
        except:
            dht = None
            print("Unable to import openDHT.  If you would like to use this feature, install dhtnode if you are on debian.")

        if dht:
            node = dht.DhtRunner()
            node.run()

            # Join the network through any running node,
            # here using a known bootstrap node.
            node.bootstrap("bootstrap.jami.net", "4222")
            dhtContainer[0] = node

        # Only daemons exposing a service need a WAN mapping
        t = threading.Thread(target=taskloop, daemon=True)
        t.start()
        # We don't actually know what an unbusy port really is. Try a bunch till we find one.
        # Note that there is a slight bit of unreliableness here.  The router could get rebooted, and lose
        # our mapping, and someone else could have taken it when we retry.  But that is rather unlikely.
        # Default to the p2p port
        WANPortContainer[0] = P2P_PORT

        for i in range(0, 5):
            try:
                portMapping = upnpwrapper.addMapping(
                    P2P_PORT, "TCP", WANPort=WANPortContainer[0])
                break
            except:
                WANPortContainer[0] += 1
                print(traceback.format_exc())
                print("Failed to register port mapping, retrying")
        else:
            # Default to the p2p port
            print("Failed to register port mapping, you will need to manually configure.")
            WANPortContainer[0] = P2P_PORT

    toScan = [p2p_bindsocket]

    if bindsocket:
        toScan.append(bindsocket)

    exited = False
    while(running):
        r, w, x = select.select(toScan, [], [], 1)
        try:

            # Whichever one has data, shove it down the other one
            for i in r:
                if i == bindsocket:
                    handleClient(i.accept()[0])
                else:
                    if services:
                        handleP2PClient(i.accept()[0])
                    else:
                        i.accept()[0].close()
        except:
            pass

    try:
        bindsocket.close()
        p2p_bindsocket.close()
    finally:
        exited = True


def closeServices(only=None):
    "Only lets us only close one,  by it's friendly name"
    for i in list(services.values()):
        try:
            if only:
                if not i.friendlyName == only:
                    continue
            i.close()
        except:
            print(traceback.format_exc())


userServices = {}

# "User Services" are configurable services stored in files, asw opposed to those defined in code


def loadUserServices(serviceDir, only=None):
    "Load services from a configuration directory.  Only to  only reload one."
    try:
        os.makedirs(serviceDir)
    except:
        pass

    if os.path.exists(serviceDir):
        for i in os.listdir(serviceDir):
            if not i.endswith(".ini"):
                continue
            if only:
                if not i == only+".ini":
                    continue
            try:
                config = configparser.ConfigParser()
                config.read(os.path.join(serviceDir, i))

                if "Info" in config.sections():
                    title = config['Info'].get("title", 'untitled')
                else:
                    title = 'untitled'

                if "Cache" in config.sections():
                    cache = config['Cache']
                else:
                    cache = {}

                service = config['Service']

                # Close any existing service by that same friendly local name
                closeServices(i[:-4])

                defaultCertFile = os.path.join(serviceDir, i+".cert")
                # Take friendly name from filename
                s = Service(service['certfile'] or defaultCertFile, service['service'], int(
                    service.get('port', '80')), {'title': title}, friendlyName=i[:-4], cacheSettings=cache)
                print("Serving a service from "+service['service'])

                userServices[i] = s
            except:
                print(traceback.format_exc())


def makeUserService(dir, name, title="A service", service="localhost", port='80',  certfile=None, cacheInfo={}):
    c = configparser.ConfigParser()
    c.add_section("Service")
    c.add_section("Info")
    c.add_section("Cache")

    file = os.path.join(dir, name+'.ini')

    sinfo = c['Service']
    sinfo['port'] = str(port)
    sinfo['service'] = service
    # Default gets used
    sinfo['certfile'] = ""

    info = c['Info']
    info['title'] = title

    for i in cacheInfo:
        c['Cache'][i] = cacheInfo[i]

    with open(file, "w") as f:
        c.write(f)
    loadUserServices(dir, name)


def delUserService(dir, name):

    file = os.path.join(dir, name+'.ini')

    if os.path.exists(dir):
        for n in os.listdir(dir):
            i = os.path.join(dir, n)
            if file and i.startswith(file):
                os.remove(i)
    closeServices(dir, name)


def listServices(serviceDir):
    try:
        os.makedirs(serviceDir)
    except:
        pass

    services = {}
    if os.path.exists(serviceDir):
        for i in os.listdir(serviceDir):
            if not i.endswith(".ini"):
                continue
            try:
                config = configparser.ConfigParser()
                config.read(os.path.join(serviceDir, i))
                services[i[:-4]] = config
            except:
                print(traceback.format_exc())

    return services
