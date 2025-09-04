# Networking Interview Questions & Answers

## Table of Contents
1. [OSI Model & TCP/IP](#osi-model--tcpip)
2. [HTTP/HTTPS & Web Protocols](#httphttps--web-protocols)
3. [DNS & Domain Resolution](#dns--domain-resolution)
4. [Load Balancing & CDN](#load-balancing--cdn)
5. [Network Security](#network-security)
6. [Performance & Troubleshooting](#performance--troubleshooting)

---

## OSI Model & TCP/IP

### 1. Explain the OSI model and how it relates to network communication.

**Answer:**
The OSI (Open Systems Interconnection) model is a 7-layer framework that standardizes network communication functions.

**OSI Layers:**

| Layer | Name | Function | Examples |
|-------|------|----------|----------|
| 7 | Application | User interface, network services | HTTP, FTP, SMTP, DNS |
| 6 | Presentation | Data encryption, compression, translation | SSL/TLS, JPEG, ASCII |
| 5 | Session | Session management, connections | NetBIOS, RPC, SQL sessions |
| 4 | Transport | End-to-end delivery, error recovery | TCP, UDP |
| 3 | Network | Routing, logical addressing | IP, ICMP, OSPF, BGP |
| 2 | Data Link | Frame formatting, error detection | Ethernet, Wi-Fi, PPP |
| 1 | Physical | Electrical signals, physical medium | Cables, hubs, repeaters |

**TCP/IP Model (4 layers):**
```
Application Layer    (OSI 5-7) → HTTP, FTP, SMTP
Transport Layer      (OSI 4)   → TCP, UDP  
Internet Layer       (OSI 3)   → IP, ICMP
Network Access Layer (OSI 1-2) → Ethernet, Wi-Fi
```

**Data Flow Example:**
```python
# Application Layer - HTTP Request
GET /api/users HTTP/1.1
Host: example.com

# Transport Layer - TCP Segment
Source Port: 54321, Dest Port: 80
Sequence: 1000, Acknowledgment: 2000

# Network Layer - IP Packet  
Source IP: 192.168.1.100, Dest IP: 203.0.113.10
TTL: 64, Protocol: TCP

# Data Link Layer - Ethernet Frame
Source MAC: AA:BB:CC:DD:EE:FF
Dest MAC: 11:22:33:44:55:66
```

### 2. What are the differences between TCP and UDP?

**Answer:**

| Feature | TCP | UDP |
|---------|-----|-----|
| **Connection** | Connection-oriented | Connectionless |
| **Reliability** | Reliable, guaranteed delivery | Unreliable, best effort |
| **Ordering** | Ordered delivery | No ordering guarantee |
| **Error Checking** | Extensive error checking | Basic checksum |
| **Flow Control** | Yes | No |
| **Congestion Control** | Yes | No |
| **Header Size** | 20 bytes minimum | 8 bytes |
| **Speed** | Slower due to overhead | Faster, minimal overhead |

**TCP Use Cases:**
- Web browsing (HTTP/HTTPS)
- Email (SMTP, POP3, IMAP)
- File transfer (FTP, SFTP)
- Database connections

**UDP Use Cases:**
- DNS queries
- Video streaming
- Online gaming
- DHCP
- SNMP

**TCP Three-Way Handshake:**
```
Client                    Server
  |                         |
  |-------- SYN ----------->|  (Sequence: 100)
  |                         |
  |<----- SYN-ACK ----------|  (Sequence: 200, Ack: 101)
  |                         |
  |-------- ACK ----------->|  (Sequence: 101, Ack: 201)
  |                         |
  |   Connection Established |
```

**Python Example:**
```python
import socket

# TCP Socket
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect(('example.com', 80))
tcp_socket.send(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
response = tcp_socket.recv(1024)
tcp_socket.close()

# UDP Socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.sendto(b'Hello', ('example.com', 53))
data, addr = udp_socket.recvfrom(1024)
udp_socket.close()
```

### 3. How does IP addressing and subnetting work?

**Answer:**

**IPv4 Address Structure:**
- 32-bit address (4 octets)
- Format: 192.168.1.1
- Classes: A, B, C, D, E

**CIDR Notation:**
```
192.168.1.0/24
- Network: 192.168.1.0
- Subnet Mask: 255.255.255.0 (/24)
- Host Range: 192.168.1.1 - 192.168.1.254
- Broadcast: 192.168.1.255
- Total Hosts: 254 (2^8 - 2)
```

**Subnetting Example:**
```python
import ipaddress

# Create network
network = ipaddress.IPv4Network('192.168.1.0/24')

print(f"Network: {network.network_address}")
print(f"Broadcast: {network.broadcast_address}")
print(f"Netmask: {network.netmask}")
print(f"Host count: {network.num_addresses - 2}")

# Subnet into smaller networks
subnets = list(network.subnets(new_prefix=26))
for i, subnet in enumerate(subnets):
    print(f"Subnet {i+1}: {subnet}")
    # Output: 192.168.1.0/26, 192.168.1.64/26, etc.
```

**Private IP Ranges:**
- Class A: 10.0.0.0/8 (10.0.0.0 - 10.255.255.255)
- Class B: 172.16.0.0/12 (172.16.0.0 - 172.31.255.255)  
- Class C: 192.168.0.0/16 (192.168.0.0 - 192.168.255.255)

**IPv6 Addressing:**
```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
- 128-bit address (8 groups of 4 hex digits)
- Shortened: 2001:db8:85a3::8a2e:370:7334
- Link-local: fe80::/10
- Unique local: fc00::/7
```

---

## HTTP/HTTPS & Web Protocols

### 4. Explain the HTTP request/response cycle and common status codes.

**Answer:**

**HTTP Request Structure:**
```http
GET /api/users/123 HTTP/1.1
Host: api.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
Content-Length: 45

{"name": "John Doe", "email": "john@example.com"}
```

**HTTP Response Structure:**
```http
HTTP/1.1 200 OK
Date: Mon, 15 Jan 2024 10:30:00 GMT
Server: nginx/1.18.0
Content-Type: application/json
Content-Length: 156
Cache-Control: max-age=3600
Set-Cookie: sessionid=abc123; HttpOnly; Secure

{"id": 123, "name": "John Doe", "email": "john@example.com", "created_at": "2024-01-15T10:30:00Z"}
```

**Common Status Codes:**

**1xx Informational:**
- 100 Continue
- 101 Switching Protocols

**2xx Success:**
- 200 OK - Request successful
- 201 Created - Resource created
- 202 Accepted - Request accepted for processing
- 204 No Content - Success but no content to return

**3xx Redirection:**
- 301 Moved Permanently - Resource permanently moved
- 302 Found - Temporary redirect
- 304 Not Modified - Use cached version
- 307 Temporary Redirect - Temporary redirect (preserve method)

**4xx Client Error:**
- 400 Bad Request - Invalid request syntax
- 401 Unauthorized - Authentication required
- 403 Forbidden - Access denied
- 404 Not Found - Resource not found
- 409 Conflict - Request conflicts with current state
- 429 Too Many Requests - Rate limit exceeded

**5xx Server Error:**
- 500 Internal Server Error - Generic server error
- 502 Bad Gateway - Invalid response from upstream
- 503 Service Unavailable - Server temporarily unavailable
- 504 Gateway Timeout - Upstream server timeout

**Python HTTP Client Example:**
```python
import requests

# GET request
response = requests.get('https://api.example.com/users/123')
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Body: {response.json()}")

# POST request with authentication
headers = {
    'Authorization': 'Bearer token123',
    'Content-Type': 'application/json'
}
data = {'name': 'John Doe', 'email': 'john@example.com'}
response = requests.post('https://api.example.com/users', 
                        json=data, headers=headers)
```

### 5. What is HTTPS and how does SSL/TLS work?

**Answer:**

**HTTPS = HTTP + SSL/TLS**
- Encrypts data in transit
- Authenticates server identity
- Ensures data integrity

**SSL/TLS Handshake Process:**
```
Client                           Server
  |                                |
  |-------- ClientHello --------->|
  |                                |
  |<------- ServerHello ----------|
  |<------- Certificate ----------|
  |<--- ServerKeyExchange --------|
  |<----- ServerHelloDone --------|
  |                                |
  |--- ClientKeyExchange -------->|
  |--- ChangeCipherSpec --------->|
  |------- Finished ------------->|
  |                                |
  |<-- ChangeCipherSpec ----------|
  |<------- Finished -------------|
  |                                |
  |    Encrypted Communication    |
```

**Certificate Validation:**
```python
import ssl
import socket

def verify_certificate(hostname, port=443):
    context = ssl.create_default_context()
    
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            
            print(f"Subject: {cert['subject']}")
            print(f"Issuer: {cert['issuer']}")
            print(f"Version: {cert['version']}")
            print(f"Serial Number: {cert['serialNumber']}")
            print(f"Not Before: {cert['notBefore']}")
            print(f"Not After: {cert['notAfter']}")
            
            return cert

# Verify certificate
cert = verify_certificate('example.com')
```

**TLS Versions:**
- TLS 1.0 (deprecated)
- TLS 1.1 (deprecated)
- TLS 1.2 (widely used)
- TLS 1.3 (latest, faster handshake)

**Cipher Suites:**
```
TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
- Key Exchange: ECDHE (Elliptic Curve Diffie-Hellman Ephemeral)
- Authentication: RSA
- Encryption: AES-256-GCM
- Hash: SHA-384
```

### 6. What are the differences between HTTP/1.1, HTTP/2, and HTTP/3?

**Answer:**

**HTTP/1.1 (1997):**
- Text-based protocol
- One request per connection (or connection reuse)
- Head-of-line blocking
- No compression of headers
- No server push

**HTTP/2 (2015):**
- Binary protocol
- Multiplexing (multiple requests per connection)
- Header compression (HPACK)
- Server push capability
- Stream prioritization

**HTTP/3 (2020):**
- Uses QUIC instead of TCP
- Built-in encryption
- Reduced connection establishment time
- Better handling of packet loss
- Connection migration support

**Performance Comparison:**
```python
import asyncio
import aiohttp
import time

async def http1_requests():
    # HTTP/1.1 - Sequential requests
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            async with session.get(f'https://httpbin.org/delay/1') as response:
                await response.text()
    
    return time.time() - start_time

async def http2_requests():
    # HTTP/2 - Concurrent requests over single connection
    start_time = time.time()
    
    connector = aiohttp.TCPConnector(limit=1)  # Single connection
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(10):
            task = session.get(f'https://httpbin.org/delay/1')
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        for response in responses:
            await response.text()
            response.close()
    
    return time.time() - start_time

# HTTP/1.1: ~10 seconds (sequential)
# HTTP/2: ~1 second (parallel)
```

**HTTP/2 Features:**
```python
# Server Push example (conceptual)
# Server can push resources before client requests them

# Client requests index.html
GET /index.html HTTP/2

# Server responds with index.html AND pushes related resources
HTTP/2 200 OK
# Push Promise for /style.css
# Push Promise for /script.js
# Push Promise for /image.png
```

---

## DNS & Domain Resolution

### 7. How does DNS resolution work?

**Answer:**

**DNS Resolution Process:**
```
1. User types "www.example.com" in browser
2. Browser checks local DNS cache
3. OS checks system DNS cache
4. Query sent to configured DNS resolver (ISP/8.8.8.8)
5. Resolver checks its cache
6. Resolver queries root nameserver (.)
7. Root returns TLD nameserver for .com
8. Resolver queries .com nameserver
9. .com returns authoritative nameserver for example.com
10. Resolver queries example.com nameserver
11. Authoritative server returns IP address
12. Response cached and returned to browser
```

**DNS Record Types:**

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | example.com → 192.0.2.1 |
| AAAA | IPv6 address | example.com → 2001:db8::1 |
| CNAME | Canonical name (alias) | www.example.com → example.com |
| MX | Mail exchange | example.com → mail.example.com |
| NS | Name server | example.com → ns1.example.com |
| TXT | Text records | example.com → "v=spf1 include:_spf.google.com ~all" |
| PTR | Reverse DNS | 1.2.0.192.in-addr.arpa → example.com |
| SRV | Service records | _http._tcp.example.com → server.example.com:80 |

**Python DNS Queries:**
```python
import dns.resolver
import socket

def dns_lookup(domain, record_type='A'):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        results = []
        for answer in answers:
            results.append(str(answer))
        return results
    except dns.resolver.NXDOMAIN:
        return f"Domain {domain} not found"
    except Exception as e:
        return f"Error: {e}"

# A record lookup
print(dns_lookup('example.com', 'A'))
# Output: ['93.184.216.34']

# MX record lookup  
print(dns_lookup('example.com', 'MX'))
# Output: ['0 .']

# Reverse DNS lookup
def reverse_dns(ip_address):
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        return hostname
    except socket.herror:
        return f"No reverse DNS for {ip_address}"

print(reverse_dns('8.8.8.8'))
# Output: dns.google.
```

**DNS Caching:**
```python
import time
import dns.resolver

class DNSCache:
    def __init__(self):
        self.cache = {}
    
    def resolve(self, domain, record_type='A'):
        cache_key = f"{domain}:{record_type}"
        
        # Check cache
        if cache_key in self.cache:
            result, timestamp, ttl = self.cache[cache_key]
            if time.time() - timestamp < ttl:
                return result
            else:
                del self.cache[cache_key]
        
        # Perform DNS lookup
        try:
            answers = dns.resolver.resolve(domain, record_type)
            result = [str(answer) for answer in answers]
            ttl = answers.rrset.ttl
            
            # Cache result
            self.cache[cache_key] = (result, time.time(), ttl)
            return result
        except Exception as e:
            return f"Error: {e}"

dns_cache = DNSCache()
print(dns_cache.resolve('example.com'))
```

### 8. What is DNS load balancing and how does it work?

**Answer:**

**DNS Load Balancing Methods:**

**1. Round Robin DNS:**
```python
# Multiple A records for same domain
example.com.    300    IN    A    192.0.2.1
example.com.    300    IN    A    192.0.2.2  
example.com.    300    IN    A    192.0.2.3

# DNS server rotates responses
# Request 1: returns 192.0.2.1
# Request 2: returns 192.0.2.2
# Request 3: returns 192.0.2.3
# Request 4: returns 192.0.2.1 (cycle repeats)
```

**2. Weighted Round Robin:**
```python
# Different weights for servers
server1.example.com    A    192.0.2.1    # Weight: 3
server2.example.com    A    192.0.2.2    # Weight: 2
server3.example.com    A    192.0.2.3    # Weight: 1

# Traffic distribution: 50%, 33%, 17%
```

**3. Geographic DNS (GeoDNS):**
```python
# Route based on client location
# US clients
us.example.com      A    192.0.2.1
# EU clients  
eu.example.com      A    203.0.113.1
# Asia clients
asia.example.com    A    198.51.100.1

# DNS resolver returns closest server
```

**4. Health Check Based:**
```python
import requests
import dns.resolver

class HealthCheckDNS:
    def __init__(self):
        self.servers = {
            '192.0.2.1': {'healthy': True, 'weight': 3},
            '192.0.2.2': {'healthy': True, 'weight': 2},
            '192.0.2.3': {'healthy': False, 'weight': 1}
        }
    
    def health_check(self, ip):
        try:
            response = requests.get(f'http://{ip}/health', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def update_health_status(self):
        for ip in self.servers:
            self.servers[ip]['healthy'] = self.health_check(ip)
    
    def get_healthy_servers(self):
        return [ip for ip, info in self.servers.items() if info['healthy']]
    
    def resolve_with_health_check(self, domain):
        self.update_health_status()
        healthy_servers = self.get_healthy_servers()
        
        if not healthy_servers:
            return "No healthy servers available"
        
        # Return healthy servers based on weight
        weighted_servers = []
        for ip in healthy_servers:
            weight = self.servers[ip]['weight']
            weighted_servers.extend([ip] * weight)
        
        return weighted_servers
```

**DNS Failover:**
```python
# Primary and backup servers
primary.example.com     A    192.0.2.1    # TTL: 60
backup.example.com      A    192.0.2.2    # TTL: 300

# Monitoring script
def dns_failover():
    if not health_check('192.0.2.1'):
        # Update DNS to point to backup
        update_dns_record('example.com', 'A', '192.0.2.2', ttl=60)
    else:
        # Restore primary
        update_dns_record('example.com', 'A', '192.0.2.1', ttl=300)
```

---

## Load Balancing & CDN

### 9. What are the different types of load balancers and their use cases?

**Answer:**

**Load Balancer Types:**

**1. Layer 4 (Transport Layer) Load Balancer:**
```python
# Routes based on IP and port
# Fast, low latency
# Cannot inspect application data

class L4LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current = 0
    
    def route_connection(self, client_ip, client_port, dest_port):
        # Simple round-robin routing
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        
        # Forward TCP connection to selected server
        return f"Route {client_ip}:{client_port} -> {server}:{dest_port}"

l4_lb = L4LoadBalancer(['192.168.1.10', '192.168.1.11', '192.168.1.12'])
```

**2. Layer 7 (Application Layer) Load Balancer:**
```python
# Routes based on HTTP content
# Can inspect headers, URLs, cookies
# More intelligent routing but higher latency

class L7LoadBalancer:
    def __init__(self):
        self.api_servers = ['api1.example.com', 'api2.example.com']
        self.web_servers = ['web1.example.com', 'web2.example.com']
        self.static_servers = ['cdn1.example.com', 'cdn2.example.com']
    
    def route_request(self, request):
        path = request.get('path', '')
        
        if path.startswith('/api/'):
            return self.select_server(self.api_servers)
        elif path.startswith('/static/'):
            return self.select_server(self.static_servers)
        else:
            return self.select_server(self.web_servers)
    
    def select_server(self, servers):
        # Could use various algorithms: round-robin, least connections, etc.
        return servers[0]  # Simplified

# Example request routing
request = {'path': '/api/users', 'method': 'GET'}
l7_lb = L7LoadBalancer()
server = l7_lb.route_request(request)
```

**Load Balancing Algorithms:**

**1. Round Robin:**
```python
class RoundRobinLB:
    def __init__(self, servers):
        self.servers = servers
        self.current = 0
    
    def get_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server
```

**2. Least Connections:**
```python
class LeastConnectionsLB:
    def __init__(self, servers):
        self.servers = {server: 0 for server in servers}
    
    def get_server(self):
        return min(self.servers, key=self.servers.get)
    
    def add_connection(self, server):
        self.servers[server] += 1
    
    def remove_connection(self, server):
        self.servers[server] -= 1
```

**3. Weighted Round Robin:**
```python
class WeightedRoundRobinLB:
    def __init__(self, server_weights):
        self.servers = []
        for server, weight in server_weights.items():
            self.servers.extend([server] * weight)
        self.current = 0
    
    def get_server(self):
        server = self.servers[self.current]
        self.current = (self.current + 1) % len(self.servers)
        return server

# Usage
lb = WeightedRoundRobinLB({
    'server1': 3,  # 50% of traffic
    'server2': 2,  # 33% of traffic  
    'server3': 1   # 17% of traffic
})
```

**4. IP Hash:**
```python
import hashlib

class IPHashLB:
    def __init__(self, servers):
        self.servers = servers
    
    def get_server(self, client_ip):
        hash_value = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
        return self.servers[hash_value % len(self.servers)]
```

### 10. How do Content Delivery Networks (CDNs) work?

**Answer:**

**CDN Architecture:**
```
User Request → Edge Server → Origin Server (if cache miss)
             ↓
        Cached Content
             ↓
        Response to User
```

**CDN Components:**

**1. Edge Servers (Points of Presence):**
```python
class EdgeServer:
    def __init__(self, location, capacity):
        self.location = location
        self.capacity = capacity
        self.cache = {}
        self.cache_size = 0
    
    def get_content(self, url):
        if url in self.cache:
            # Cache hit
            self.cache[url]['hits'] += 1
            return self.cache[url]['content']
        else:
            # Cache miss - fetch from origin
            content = self.fetch_from_origin(url)
            self.cache_content(url, content)
            return content
    
    def cache_content(self, url, content):
        if self.cache_size < self.capacity:
            self.cache[url] = {
                'content': content,
                'timestamp': time.time(),
                'hits': 1,
                'size': len(content)
            }
            self.cache_size += len(content)
        else:
            # Evict least recently used content
            self.evict_lru()
            self.cache_content(url, content)
```

**2. Cache Strategies:**
```python
class CDNCache:
    def __init__(self):
        self.cache = {}
    
    def set_cache_headers(self, response, cache_type):
        if cache_type == 'static':
            # Static assets - long cache time
            response.headers['Cache-Control'] = 'public, max-age=31536000'  # 1 year
            response.headers['Expires'] = (datetime.now() + timedelta(days=365)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        elif cache_type == 'dynamic':
            # Dynamic content - short cache time
            response.headers['Cache-Control'] = 'public, max-age=300'  # 5 minutes
        
        elif cache_type == 'private':
            # User-specific content - no public cache
            response.headers['Cache-Control'] = 'private, max-age=0'
        
        elif cache_type == 'no-cache':
            # Always revalidate
            response.headers['Cache-Control'] = 'no-cache, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
        
        return response
```

**3. Geographic Distribution:**
```python
import geopy.distance

class CDNRouter:
    def __init__(self):
        self.edge_servers = {
            'us-east': {'lat': 40.7128, 'lon': -74.0060, 'server': 'edge-us-east.cdn.com'},
            'us-west': {'lat': 37.7749, 'lon': -122.4194, 'server': 'edge-us-west.cdn.com'},
            'eu-west': {'lat': 51.5074, 'lon': -0.1278, 'server': 'edge-eu-west.cdn.com'},
            'asia-pacific': {'lat': 35.6762, 'lon': 139.6503, 'server': 'edge-ap.cdn.com'}
        }
    
    def find_nearest_edge(self, user_lat, user_lon):
        min_distance = float('inf')
        nearest_edge = None
        
        user_location = (user_lat, user_lon)
        
        for edge_id, edge_info in self.edge_servers.items():
            edge_location = (edge_info['lat'], edge_info['lon'])
            distance = geopy.distance.distance(user_location, edge_location).kilometers
            
            if distance < min_distance:
                min_distance = distance
                nearest_edge = edge_info['server']
        
        return nearest_edge, min_distance

# Usage
router = CDNRouter()
nearest_server, distance = router.find_nearest_edge(40.7589, -73.9851)  # NYC coordinates
print(f"Nearest server: {nearest_server}, Distance: {distance:.2f} km")
```

**4. Cache Invalidation:**
```python
class CDNInvalidation:
    def __init__(self):
        self.edge_servers = ['edge1.cdn.com', 'edge2.cdn.com', 'edge3.cdn.com']
    
    def invalidate_content(self, urls, invalidation_type='immediate'):
        if invalidation_type == 'immediate':
            # Purge content immediately from all edges
            for server in self.edge_servers:
                self.purge_from_edge(server, urls)
        
        elif invalidation_type == 'lazy':
            # Mark content as stale, refresh on next request
            for server in self.edge_servers:
                self.mark_stale(server, urls)
        
        elif invalidation_type == 'scheduled':
            # Schedule invalidation for specific time
            self.schedule_invalidation(urls, scheduled_time)
    
    def purge_from_edge(self, server, urls):
        # Send purge request to edge server
        for url in urls:
            requests.post(f'http://{server}/purge', json={'url': url})
    
    def mark_stale(self, server, urls):
        # Mark content as stale without immediate purge
        for url in urls:
            requests.post(f'http://{server}/stale', json={'url': url})
```

**CDN Performance Benefits:**
```python
# Performance comparison
def measure_cdn_performance():
    # Without CDN - direct to origin
    origin_response_time = requests.get('https://origin.example.com/large-image.jpg').elapsed.total_seconds()
    
    # With CDN - from edge server
    cdn_response_time = requests.get('https://cdn.example.com/large-image.jpg').elapsed.total_seconds()
    
    improvement = ((origin_response_time - cdn_response_time) / origin_response_time) * 100
    
    return {
        'origin_time': origin_response_time,
        'cdn_time': cdn_response_time,
        'improvement_percentage': improvement
    }

# Typical results:
# Origin: 2.5 seconds
# CDN: 0.3 seconds  
# Improvement: 88%
```

---

## Network Security

### 11. What are common network security threats and how do you mitigate them?

**Answer:**

**Common Network Threats:**

**1. DDoS (Distributed Denial of Service):**
```python
import time
from collections import defaultdict, deque

class DDoSProtection:
    def __init__(self, rate_limit=100, time_window=60):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.request_counts = defaultdict(deque)
        self.blocked_ips = set()
    
    def is_request_allowed(self, client_ip):
        current_time = time.time()
        
        # Clean old requests outside time window
        while (self.request_counts[client_ip] and 
               current_time - self.request_counts[client_ip][0] > self.time_window):
            self.request_counts[client_ip].popleft()
        
        # Check if IP is blocked
        if client_ip in self.blocked_ips:
            return False
        
        # Check rate limit
        if len(self.request_counts[client_ip]) >= self.rate_limit:
            self.blocked_ips.add(client_ip)
            return False
        
        # Allow request and record it
        self.request_counts[client_ip].append(current_time)
        return True

# Usage
ddos_protection = DDoSProtection(rate_limit=100, time_window=60)
if ddos_protection.is_request_allowed('192.168.1.100'):
    # Process request
    pass
else:
    # Block request
    pass
```

**2. Man-in-the-Middle (MITM) Attacks:**
```python
import ssl
import socket
import certifi

def secure_connection(hostname, port=443):
    # Create secure SSL context
    context = ssl.create_default_context(cafile=certifi.where())
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    
    # Additional security settings
    context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS')
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    
    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # Verify certificate
                cert = ssock.getpeercert()
                print(f"Connected to {hostname} with certificate: {cert['subject']}")
                return ssock
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
        return None
    except Exception as e:
        print(f"Connection Error: {e}")
        return None
```

**3. SQL Injection via Network:**
```python
import re
import html

class NetworkInputValidator:
    def __init__(self):
        self.sql_injection_patterns = [
            r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER)\b)",
            r"(\b(UNION|OR|AND)\b.*\b(SELECT|INSERT|UPDATE|DELETE)\b)",
            r"(--|#|/\*|\*/)",
            r"(\b(EXEC|EXECUTE|SP_|XP_)\b)",
            r"(\b(SCRIPT|JAVASCRIPT|VBSCRIPT)\b)"
        ]
    
    def validate_input(self, user_input):
        # HTML encode
        sanitized = html.escape(user_input)
        
        # Check for SQL injection patterns
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, sanitized, re.IGNORECASE):
                return False, "Potential SQL injection detected"
        
        # Length validation
        if len(sanitized) > 1000:
            return False, "Input too long"
        
        return True, sanitized
    
    def sanitize_for_database(self, user_input):
        # Use parameterized queries instead
        return user_input.replace("'", "''")  # Basic escaping (use proper ORM)

validator = NetworkInputValidator()
is_valid, result = validator.validate_input("'; DROP TABLE users; --")
```

**4. Network Scanning and Intrusion Detection:**
```python
import socket
import threading
from datetime import datetime, timedelta

class IntrusionDetectionSystem:
    def __init__(self):
        self.scan_attempts = {}
        self.blocked_ips = set()
        self.suspicious_patterns = {
            'port_scan': {'threshold': 10, 'time_window': 60},
            'brute_force': {'threshold': 5, 'time_window': 300}
        }
    
    def detect_port_scan(self, source_ip, dest_port):
        current_time = datetime.now()
        
        if source_ip not in self.scan_attempts:
            self.scan_attempts[source_ip] = {'ports': set(), 'timestamps': []}
        
        # Add port and timestamp
        self.scan_attempts[source_ip]['ports'].add(dest_port)
        self.scan_attempts[source_ip]['timestamps'].append(current_time)
        
        # Clean old timestamps
        cutoff_time = current_time - timedelta(seconds=60)
        self.scan_attempts[source_ip]['timestamps'] = [
            ts for ts in self.scan_attempts[source_ip]['timestamps'] 
            if ts > cutoff_time
        ]
        
        # Check for port scan
        unique_ports = len(self.scan_attempts[source_ip]['ports'])
        recent_attempts = len(self.scan_attempts[source_ip]['timestamps'])
        
        if unique_ports > 10 and recent_attempts > 20:
            self.blocked_ips.add(source_ip)
            self.alert_admin(f"Port scan detected from {source_ip}")
            return True
        
        return False
    
    def alert_admin(self, message):
        print(f"SECURITY ALERT: {message}")
        # Send email, log to SIEM, etc.

ids = IntrusionDetectionSystem()
```

**5. Firewall Rules:**
```python
class NetworkFirewall:
    def __init__(self):
        self.rules = []
        self.default_policy = 'DENY'
    
    def add_rule(self, action, protocol, src_ip, src_port, dest_ip, dest_port):
        rule = {
            'action': action,  # ALLOW or DENY
            'protocol': protocol,  # TCP, UDP, ICMP
            'src_ip': src_ip,
            'src_port': src_port,
            'dest_ip': dest_ip,
            'dest_port': dest_port
        }
        self.rules.append(rule)
    
    def check_packet(self, packet):
        for rule in self.rules:
            if self.match_rule(rule, packet):
                return rule['action']
        
        return self.default_policy
    
    def match_rule(self, rule, packet):
        # Simplified matching logic
        if rule['protocol'] != 'ANY' and rule['protocol'] != packet['protocol']:
            return False
        
        if not self.match_ip(rule['src_ip'], packet['src_ip']):
            return False
        
        if not self.match_port(rule['src_port'], packet['src_port']):
            return False
        
        if not self.match_ip(rule['dest_ip'], packet['dest_ip']):
            return False
        
        if not self.match_port(rule['dest_port'], packet['dest_port']):
            return False
        
        return True
    
    def match_ip(self, rule_ip, packet_ip):
        if rule_ip == 'ANY':
            return True
        return rule_ip == packet_ip
    
    def match_port(self, rule_port, packet_port):
        if rule_port == 'ANY':
            return True
        return rule_port == packet_port

# Configure firewall
firewall = NetworkFirewall()
firewall.add_rule('ALLOW', 'TCP', 'ANY', 'ANY', '192.168.1.100', 80)
firewall.add_rule('ALLOW', 'TCP', 'ANY', 'ANY', '192.168.1.100', 443)
firewall.add_rule('DENY', 'TCP', 'ANY', 'ANY', '192.168.1.100', 22)

# Test packet
packet = {
    'protocol': 'TCP',
    'src_ip': '203.0.113.1',
    'src_port': 54321,
    'dest_ip': '192.168.1.100',
    'dest_port': 80
}

action = firewall.check_packet(packet)  # Returns 'ALLOW'
```

---

## Performance & Troubleshooting

### 12. How do you troubleshoot network performance issues?

**Answer:**

**Network Performance Monitoring:**

**1. Latency Measurement:**
```python
import subprocess
import re
import statistics

def ping_test(host, count=10):
    try:
        # Execute ping command
        result = subprocess.run(['ping', '-c', str(count), host], 
                              capture_output=True, text=True)
        
        # Parse ping output
        times = re.findall(r'time=(\d+\.?\d*)', result.stdout)
        times = [float(t) for t in times]
        
        if times:
            return {
                'host': host,
                'packet_loss': (count - len(times)) / count * 100,
                'min_time': min(times),
                'max_time': max(times),
                'avg_time': statistics.mean(times),
                'std_dev': statistics.stdev(times) if len(times) > 1 else 0
            }
    except Exception as e:
        return {'error': str(e)}

# Test network latency
result = ping_test('8.8.8.8', 20)
print(f"Average latency: {result['avg_time']:.2f}ms")
print(f"Packet loss: {result['packet_loss']:.1f}%")
```

**2. Bandwidth Testing:**
```python
import time
import requests
import threading

class BandwidthTester:
    def __init__(self):
        self.download_speeds = []
        self.upload_speeds = []
    
    def test_download_speed(self, url, duration=10):
        start_time = time.time()
        total_bytes = 0
        
        while time.time() - start_time < duration:
            try:
                response = requests.get(url, stream=True)
                for chunk in response.iter_content(chunk_size=8192):
                    total_bytes += len(chunk)
                    if time.time() - start_time >= duration:
                        break
            except Exception as e:
                print(f"Download test error: {e}")
                break
        
        elapsed_time = time.time() - start_time
        speed_mbps = (total_bytes * 8) / (elapsed_time * 1000000)  # Convert to Mbps
        
        return {
            'bytes_downloaded': total_bytes,
            'duration': elapsed_time,
            'speed_mbps': speed_mbps
        }
    
    def test_upload_speed(self, url, data_size_mb=10):
        # Generate test data
        test_data = b'0' * (data_size_mb * 1024 * 1024)
        
        start_time = time.time()
        try:
            response = requests.post(url, data=test_data)
            elapsed_time = time.time() - start_time
            speed_mbps = (data_size_mb * 8) / elapsed_time
            
            return {
                'bytes_uploaded': len(test_data),
                'duration': elapsed_time,
                'speed_mbps': speed_mbps
            }
        except Exception as e:
            return {'error': str(e)}
    
    def run_comprehensive_test(self):
        # Test multiple servers
        test_servers = [
            'http://speedtest.example1.com/download',
            'http://speedtest.example2.com/download',
            'http://speedtest.example3.com/download'
        ]
        
        results = []
        for server in test_servers:
            result = self.test_download_speed(server)
            results.append(result)
        
        avg_speed = statistics.mean([r['speed_mbps'] for r in results if 'speed_mbps' in r])
        return {
            'individual_results': results,
            'average_speed_mbps': avg_speed
        }

tester = BandwidthTester()
```

**3. Network Path Analysis:**
```python
import subprocess
import re

def traceroute(host):
    try:
        # Execute traceroute command
        result = subprocess.run(['traceroute', host], 
                              capture_output=True, text=True, timeout=60)
        
        hops = []
        lines = result.stdout.split('\n')
        
        for line in lines:
            # Parse traceroute output
            match = re.match(r'\s*(\d+)\s+(.+)', line)
            if match:
                hop_num = int(match.group(1))
                hop_info = match.group(2)
                
                # Extract IP addresses and response times
                ip_matches = re.findall(r'(\d+\.\d+\.\d+\.\d+)', hop_info)
                time_matches = re.findall(r'(\d+\.?\d*)\s*ms', hop_info)
                
                hops.append({
                    'hop': hop_num,
                    'ips': ip_matches,
                    'times': [float(t) for t in time_matches],
                    'raw': hop_info.strip()
                })
        
        return hops
    except Exception as e:
        return {'error': str(e)}

def analyze_network_path(host):
    hops = traceroute(host)
    
    analysis = {
        'total_hops': len(hops),
        'high_latency_hops': [],
        'timeout_hops': [],
        'total_latency': 0
    }
    
    for hop in hops:
        if hop.get('times'):
            avg_time = statistics.mean(hop['times'])
            analysis['total_latency'] += avg_time
            
            if avg_time > 100:  # High latency threshold
                analysis['high_latency_hops'].append({
                    'hop': hop['hop'],
                    'latency': avg_time,
                    'ips': hop['ips']
                })
        else:
            analysis['timeout_hops'].append(hop['hop'])
    
    return analysis

# Analyze path to destination
path_analysis = analyze_network_path('example.com')
```

**4. Network Interface Monitoring:**
```python
import psutil
import time

class NetworkMonitor:
    def __init__(self):
        self.previous_stats = None
    
    def get_network_stats(self):
        stats = psutil.net_io_counters(pernic=True)
        return stats
    
    def calculate_throughput(self, interface='eth0', interval=1):
        # Get initial stats
        stats1 = psutil.net_io_counters(pernic=True)
        time.sleep(interval)
        stats2 = psutil.net_io_counters(pernic=True)
        
        if interface in stats1 and interface in stats2:
            bytes_sent = stats2[interface].bytes_sent - stats1[interface].bytes_sent
            bytes_recv = stats2[interface].bytes_recv - stats1[interface].bytes_recv
            
            # Convert to Mbps
            upload_mbps = (bytes_sent * 8) / (interval * 1000000)
            download_mbps = (bytes_recv * 8) / (interval * 1000000)
            
            return {
                'interface': interface,
                'upload_mbps': upload_mbps,
                'download_mbps': download_mbps,
                'total_mbps': upload_mbps + download_mbps
            }
        
        return None
    
    def monitor_continuously(self, interface='eth0', duration=60):
        measurements = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            throughput = self.calculate_throughput(interface, 1)
            if throughput:
                throughput['timestamp'] = time.time()
                measurements.append(throughput)
            time.sleep(1)
        
        # Calculate statistics
        if measurements:
            upload_speeds = [m['upload_mbps'] for m in measurements]
            download_speeds = [m['download_mbps'] for m in measurements]
            
            return {
                'measurements': measurements,
                'avg_upload_mbps': statistics.mean(upload_speeds),
                'avg_download_mbps': statistics.mean(download_speeds),
                'max_upload_mbps': max(upload_speeds),
                'max_download_mbps': max(download_speeds),
                'min_upload_mbps': min(upload_speeds),
                'min_download_mbps': min(download_speeds)
            }
        
        return None

monitor = NetworkMonitor()
stats = monitor.monitor_continuously('eth0', 30)
```

**5. DNS Performance Testing:**
```python
import dns.resolver
import time

def test_dns_performance(domains, dns_servers):
    results = {}
    
    for dns_server in dns_servers:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]
        resolver.timeout = 5
        resolver.lifetime = 10
        
        server_results = []
        
        for domain in domains:
            start_time = time.time()
            try:
                answers = resolver.resolve(domain, 'A')
                response_time = (time.time() - start_time) * 1000  # Convert to ms
                
                server_results.append({
                    'domain': domain,
                    'response_time_ms': response_time,
                    'success': True,
                    'ip_addresses': [str(answer) for answer in answers]
                })
            except Exception as e:
                server_results.append({
                    'domain': domain,
                    'response_time_ms': None,
                    'success': False,
                    'error': str(e)
                })
        
        # Calculate average response time for this DNS server
        successful_queries = [r for r in server_results if r['success']]
        if successful_queries:
            avg_response_time = statistics.mean([r['response_time_ms'] for r in successful_queries])
            success_rate = len(successful_queries) / len(server_results) * 100
        else:
            avg_response_time = None
            success_rate = 0
        
        results[dns_server] = {
            'individual_results': server_results,
            'average_response_time_ms': avg_response_time,
            'success_rate_percent': success_rate
        }
    
    return results

# Test DNS performance
test_domains = ['google.com', 'facebook.com', 'amazon.com', 'microsoft.com']
dns_servers = ['8.8.8.8', '1.1.1.1', '208.67.222.222']  # Google, Cloudflare, OpenDNS

dns_results = test_dns_performance(test_domains, dns_servers)
```

---

## Summary

Network fundamentals are crucial for data engineers working with distributed systems. Key areas include:

1. **Protocol Understanding**: OSI model, TCP/UDP, HTTP/HTTPS
2. **DNS & Routing**: Domain resolution, load balancing, CDN
3. **Security**: Threat mitigation, encryption, firewalls
4. **Performance**: Monitoring, troubleshooting, optimization
5. **Scalability**: Load balancing, caching, geographic distribution

Success requires understanding both theoretical concepts and practical implementation, with focus on performance, security, and reliability in distributed data systems.