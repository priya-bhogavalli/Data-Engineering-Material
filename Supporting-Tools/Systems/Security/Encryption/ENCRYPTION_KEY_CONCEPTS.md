# Encryption - Key Concepts

## Overview
Encryption is the process of converting plaintext data into ciphertext using cryptographic algorithms to protect data confidentiality and integrity.

## Encryption Types

### Symmetric Encryption
- **Single key**: Same key for encryption/decryption
- **Fast performance**: Efficient for large data
- **Key distribution**: Secure key sharing challenge
- **Algorithms**: AES, DES, 3DES, ChaCha20
- **Block vs Stream**: Fixed blocks vs continuous

### Asymmetric Encryption
- **Key pairs**: Public and private keys
- **Public key**: Freely shared for encryption
- **Private key**: Secret key for decryption
- **Digital signatures**: Authentication and non-repudiation
- **Algorithms**: RSA, ECC, DSA

### Hybrid Encryption
- **Best of both**: Combines symmetric and asymmetric
- **Key exchange**: Asymmetric for key distribution
- **Data encryption**: Symmetric for bulk data
- **Performance**: Efficient and secure
- **Common usage**: TLS, PGP, S/MIME

## Encryption Algorithms

### AES (Advanced Encryption Standard)
- **Block cipher**: 128-bit blocks
- **Key sizes**: 128, 192, 256 bits
- **Modes**: ECB, CBC, GCM, CTR
- **Government approved**: FIPS 140-2
- **Wide adoption**: Industry standard

### RSA
- **Public key**: Widely used asymmetric
- **Key sizes**: 2048, 3072, 4096 bits
- **Mathematical basis**: Prime factorization
- **Digital signatures**: Authentication
- **Key exchange**: Secure key distribution

## Data Encryption

### Data at Rest
- **File encryption**: Individual file protection
- **Database encryption**: TDE, column-level
- **Disk encryption**: Full disk encryption
- **Cloud storage**: Provider encryption
- **Key management**: Secure key storage

### Data in Transit
- **TLS/SSL**: Web communication
- **VPN**: Network tunneling
- **Email encryption**: S/MIME, PGP
- **API security**: HTTPS, OAuth
- **Message queues**: Encrypted messaging

### Data in Use
- **Application-level**: Runtime encryption
- **Homomorphic encryption**: Compute on encrypted data
- **Secure enclaves**: Hardware protection
- **Memory encryption**: RAM protection
- **Processing encryption**: Confidential computing

## Key Management

### Key Lifecycle
- **Generation**: Secure random keys
- **Distribution**: Secure key sharing
- **Storage**: Protected key repositories
- **Rotation**: Regular key updates
- **Destruction**: Secure key deletion

### Key Management Systems
- **Hardware Security Modules**: Dedicated hardware
- **Key vaults**: Cloud-based storage
- **Certificate authorities**: PKI management
- **Key escrow**: Recovery mechanisms
- **Access controls**: Key usage policies

## Hashing & Digital Signatures

### Hash Functions
- **One-way**: Irreversible transformation
- **Fixed output**: Consistent hash size
- **Collision resistance**: Unique hashes
- **Algorithms**: SHA-256, SHA-3, BLAKE2
- **Use cases**: Integrity verification, passwords

### Digital Signatures
- **Authentication**: Verify sender identity
- **Non-repudiation**: Prevent denial
- **Integrity**: Detect tampering
- **Process**: Hash + private key encryption
- **Verification**: Public key decryption

## Compliance & Standards
- **FIPS 140-2**: Cryptographic module standards
- **Common Criteria**: Security evaluation
- **GDPR**: Data protection requirements
- **HIPAA**: Healthcare data encryption
- **PCI DSS**: Payment card data protection