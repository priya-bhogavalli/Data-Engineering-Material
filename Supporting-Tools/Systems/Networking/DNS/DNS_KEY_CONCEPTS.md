# DNS - Key Concepts

## Overview
DNS (Domain Name System) is a hierarchical distributed naming system that translates human-readable domain names into IP addresses and provides other domain-related information.

## DNS Hierarchy

### Domain Structure
- **Root Domain**: . (dot)
- **Top-Level Domains**: .com, .org, .net, .gov
- **Second-Level Domains**: example.com
- **Subdomains**: www.example.com, mail.example.com
- **FQDN**: Fully Qualified Domain Name

### DNS Servers
- **Root Servers**: 13 root server clusters worldwide
- **TLD Servers**: Top-level domain servers
- **Authoritative Servers**: Domain-specific servers
- **Recursive Resolvers**: ISP/public DNS servers
- **Caching Servers**: Local DNS caches

## DNS Records

### Common Record Types
- **A**: IPv4 address mapping
- **AAAA**: IPv6 address mapping
- **CNAME**: Canonical name alias
- **MX**: Mail exchange servers
- **NS**: Name server records
- **PTR**: Reverse DNS lookup
- **TXT**: Text information
- **SOA**: Start of Authority

### Record Components
- **Name**: Domain name
- **Type**: Record type
- **Class**: Usually IN (Internet)
- **TTL**: Time to Live (cache duration)
- **Data**: Record-specific information

## DNS Resolution Process

### Query Types
- **Recursive**: Full resolution by server
- **Iterative**: Step-by-step resolution
- **Forward Lookup**: Name to IP
- **Reverse Lookup**: IP to name
- **Authoritative**: From authoritative server
- **Non-authoritative**: From cache

### Resolution Steps
1. **Local Cache**: Check resolver cache
2. **Root Query**: Query root servers
3. **TLD Query**: Query TLD servers
4. **Authoritative Query**: Query domain servers
5. **Response**: Return IP address
6. **Caching**: Store result with TTL

## DNS Security

### Security Threats
- **DNS Spoofing**: False DNS responses
- **Cache Poisoning**: Corrupt cached data
- **DDoS Attacks**: Overwhelm DNS servers
- **DNS Tunneling**: Data exfiltration
- **Typosquatting**: Similar domain names

### Security Measures
- **DNSSEC**: DNS Security Extensions
- **DNS over HTTPS**: Encrypted queries
- **DNS over TLS**: Secure transport
- **Rate Limiting**: Query throttling
- **Monitoring**: Anomaly detection

## DNS Configuration

### Zone Files
- **SOA Record**: Zone authority information
- **NS Records**: Name server delegation
- **Resource Records**: Domain mappings
- **Zone Transfer**: Replica synchronization
- **Dynamic Updates**: Automatic record updates

### DNS Tools
- **nslookup**: Basic DNS queries
- **dig**: Detailed DNS information
- **host**: Simple DNS lookups
- **ping**: Test connectivity
- **traceroute**: Path tracing

## Performance Optimization
- **Caching**: Reduce query latency
- **Load Balancing**: Distribute queries
- **Anycast**: Route to nearest server
- **CDN Integration**: Content delivery
- **Monitoring**: Performance tracking