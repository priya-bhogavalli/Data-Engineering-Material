# HTTP/HTTPS - Key Concepts

## Overview
HTTP (HyperText Transfer Protocol) is the foundation of web communication, while HTTPS adds SSL/TLS encryption for secure data transmission between clients and servers.

## HTTP Fundamentals

### Request-Response Model
- **Client**: Web browser, API client
- **Server**: Web server, API server
- **Stateless**: Each request independent
- **Text-based**: Human-readable protocol
- **Port 80**: Default HTTP port

### HTTP Methods
- **GET**: Retrieve data
- **POST**: Submit data
- **PUT**: Update/create resource
- **DELETE**: Remove resource
- **PATCH**: Partial update
- **HEAD**: Get headers only
- **OPTIONS**: Check allowed methods

### Status Codes
- **1xx**: Informational responses
- **2xx**: Success (200 OK, 201 Created)
- **3xx**: Redirection (301 Moved, 302 Found)
- **4xx**: Client errors (400 Bad Request, 404 Not Found)
- **5xx**: Server errors (500 Internal Error, 503 Unavailable)

## HTTP Headers

### Request Headers
- **Host**: Target server
- **User-Agent**: Client information
- **Accept**: Acceptable content types
- **Authorization**: Authentication credentials
- **Content-Type**: Request body format
- **Cookie**: Session cookies

### Response Headers
- **Content-Type**: Response format
- **Content-Length**: Response size
- **Set-Cookie**: Set client cookies
- **Cache-Control**: Caching directives
- **Location**: Redirect target
- **Server**: Server information

### Security Headers
- **Strict-Transport-Security**: Force HTTPS
- **Content-Security-Policy**: XSS protection
- **X-Frame-Options**: Clickjacking protection
- **X-Content-Type-Options**: MIME sniffing protection
- **Referrer-Policy**: Referrer information control

## HTTPS Security

### SSL/TLS Encryption
- **Symmetric Encryption**: Shared secret key
- **Asymmetric Encryption**: Public/private keys
- **Digital Certificates**: Identity verification
- **Certificate Authorities**: Trusted issuers
- **Port 443**: Default HTTPS port

### TLS Handshake
1. **Client Hello**: Supported protocols/ciphers
2. **Server Hello**: Selected protocol/cipher
3. **Certificate**: Server identity verification
4. **Key Exchange**: Establish shared secret
5. **Finished**: Handshake completion

### Certificate Management
- **Certificate Types**: DV, OV, EV certificates
- **Wildcard Certificates**: *.domain.com
- **SAN Certificates**: Multiple domains
- **Certificate Chain**: Root, intermediate, leaf
- **Certificate Renewal**: Expiration management

## HTTP Versions

### HTTP/1.1
- **Persistent Connections**: Keep-alive
- **Chunked Transfer**: Streaming responses
- **Host Header**: Virtual hosting
- **Caching**: Improved cache control
- **Compression**: gzip encoding

### HTTP/2
- **Binary Protocol**: Efficient parsing
- **Multiplexing**: Multiple streams
- **Server Push**: Proactive resource delivery
- **Header Compression**: HPACK algorithm
- **Stream Prioritization**: Resource ordering

### HTTP/3
- **QUIC Protocol**: UDP-based transport
- **Reduced Latency**: Faster connections
- **Connection Migration**: IP address changes
- **Built-in Security**: Integrated encryption
- **Improved Performance**: Better congestion control

## Caching

### Cache Types
- **Browser Cache**: Client-side caching
- **Proxy Cache**: Intermediate caching
- **CDN Cache**: Content delivery networks
- **Server Cache**: Application-level caching
- **Database Cache**: Query result caching

### Cache Control
- **Cache-Control**: Caching directives
- **ETag**: Entity tags for validation
- **Last-Modified**: Modification timestamps
- **Expires**: Absolute expiration time
- **Vary**: Response variation factors

## Authentication & Authorization

### Authentication Methods
- **Basic Auth**: Username/password in headers
- **Bearer Token**: JWT or API tokens
- **OAuth 2.0**: Delegated authorization
- **API Keys**: Simple authentication
- **Mutual TLS**: Certificate-based auth

### Session Management
- **Cookies**: Client-side storage
- **Sessions**: Server-side storage
- **JWT**: JSON Web Tokens
- **CSRF Protection**: Cross-site request forgery
- **Same-Site Cookies**: Cookie security

## Performance Optimization
- **Compression**: gzip, brotli encoding
- **Minification**: Reduce file sizes
- **CDN**: Content delivery networks
- **HTTP/2**: Protocol improvements
- **Connection Pooling**: Reuse connections