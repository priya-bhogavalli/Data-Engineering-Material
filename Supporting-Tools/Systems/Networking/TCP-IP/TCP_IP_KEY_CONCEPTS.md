# TCP/IP - Key Concepts

## Overview
TCP/IP (Transmission Control Protocol/Internet Protocol) is the fundamental communication protocol suite that enables data transmission across networks and the internet.

## OSI vs TCP/IP Model

### TCP/IP Layers
- **Application Layer**: HTTP, FTP, SMTP, DNS
- **Transport Layer**: TCP, UDP
- **Internet Layer**: IP, ICMP, ARP
- **Network Access Layer**: Ethernet, Wi-Fi

### Layer Functions
- **Application**: User interface and services
- **Transport**: End-to-end communication
- **Internet**: Routing and addressing
- **Network Access**: Physical transmission

## Internet Protocol (IP)

### IPv4 Addressing
- **32-bit addresses**: 4 octets (192.168.1.1)
- **Address classes**: A, B, C, D, E
- **Private ranges**: 10.x.x.x, 172.16-31.x.x, 192.168.x.x
- **Subnet masks**: Network/host separation
- **CIDR notation**: /24, /16, /8

### IPv6 Addressing
- **128-bit addresses**: 8 groups of 4 hex digits
- **Address types**: Unicast, multicast, anycast
- **Link-local**: fe80::/10 prefix
- **Global unicast**: 2000::/3 prefix
- **Dual stack**: IPv4 and IPv6 coexistence

### IP Packet Structure
- **Header**: Version, length, TTL, protocol
- **Source/Destination**: IP addresses
- **Fragmentation**: Packet splitting
- **Checksum**: Error detection
- **Options**: Additional header fields

## Transmission Control Protocol (TCP)

### TCP Characteristics
- **Connection-oriented**: Establish connection first
- **Reliable**: Guaranteed delivery
- **Ordered**: Sequential data delivery
- **Flow control**: Manage data rate
- **Error detection**: Checksum validation

### TCP Connection
- **Three-way handshake**: SYN, SYN-ACK, ACK
- **Connection establishment**: Client-server setup
- **Data transfer**: Bidirectional communication
- **Connection termination**: FIN, ACK sequence
- **Connection states**: LISTEN, ESTABLISHED, CLOSED

### TCP Features
- **Sequence numbers**: Packet ordering
- **Acknowledgments**: Delivery confirmation
- **Window size**: Flow control mechanism
- **Retransmission**: Lost packet recovery
- **Congestion control**: Network congestion management

## User Datagram Protocol (UDP)

### UDP Characteristics
- **Connectionless**: No connection setup
- **Unreliable**: No delivery guarantee
- **Fast**: Low overhead
- **Stateless**: No connection state
- **Broadcast/Multicast**: One-to-many communication

### UDP Use Cases
- **DNS queries**: Fast lookups
- **DHCP**: Address assignment
- **Streaming media**: Real-time data
- **Gaming**: Low-latency communication
- **SNMP**: Network management

## Routing

### Routing Concepts
- **Default gateway**: Local network exit
- **Routing table**: Path information
- **Static routing**: Manual configuration
- **Dynamic routing**: Automatic updates
- **Metric**: Path cost calculation

### Routing Protocols
- **RIP**: Routing Information Protocol
- **OSPF**: Open Shortest Path First
- **BGP**: Border Gateway Protocol
- **EIGRP**: Enhanced Interior Gateway Routing
- **IS-IS**: Intermediate System to Intermediate System

## Network Address Translation (NAT)

### NAT Types
- **Static NAT**: One-to-one mapping
- **Dynamic NAT**: Pool-based mapping
- **PAT**: Port Address Translation
- **SNAT**: Source NAT
- **DNAT**: Destination NAT

### NAT Benefits
- **IP conservation**: Reuse private addresses
- **Security**: Hide internal structure
- **Flexibility**: Network design freedom
- **Cost reduction**: Fewer public IPs needed

## Common Protocols

### Application Protocols
- **HTTP/HTTPS**: Web communication
- **FTP/SFTP**: File transfer
- **SMTP/POP3/IMAP**: Email
- **SSH**: Secure shell access
- **Telnet**: Remote terminal access

### Network Services
- **DHCP**: Dynamic IP assignment
- **DNS**: Name resolution
- **NTP**: Time synchronization
- **SNMP**: Network management
- **ICMP**: Error reporting and diagnostics

## Troubleshooting Tools
- **ping**: Connectivity testing
- **traceroute**: Path tracing
- **netstat**: Network connections
- **nslookup/dig**: DNS queries
- **wireshark**: Packet analysis