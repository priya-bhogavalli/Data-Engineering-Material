# Access Control - Key Concepts

## Overview
Access control is a security mechanism that regulates who can access resources and what actions they can perform, ensuring data confidentiality, integrity, and availability.

## Access Control Models

### Discretionary Access Control (DAC)
- **Owner control**: Resource owners set permissions
- **User discretion**: Flexible permission assignment
- **Access Control Lists**: Permission matrices
- **Identity-based**: User/group permissions
- **Inheritance**: Permission propagation

### Mandatory Access Control (MAC)
- **System-enforced**: Centralized policy control
- **Security labels**: Classification levels
- **Clearance levels**: User security ratings
- **Bell-LaPadula**: Confidentiality model
- **Biba**: Integrity model

### Role-Based Access Control (RBAC)
- **Role assignment**: Users assigned to roles
- **Permission assignment**: Roles have permissions
- **Role hierarchy**: Inheritance relationships
- **Separation of duties**: Conflicting role prevention
- **Least privilege**: Minimum necessary access

### Attribute-Based Access Control (ABAC)
- **Policy-driven**: Rule-based decisions
- **Attributes**: User, resource, environment
- **Dynamic evaluation**: Context-aware decisions
- **Fine-grained**: Detailed permission control
- **Scalability**: Complex environment support

## Authentication

### Authentication Factors
- **Something you know**: Passwords, PINs
- **Something you have**: Tokens, smart cards
- **Something you are**: Biometrics
- **Somewhere you are**: Location-based
- **Something you do**: Behavioral patterns

### Multi-Factor Authentication (MFA)
- **Two-factor**: Two different factors
- **Multi-factor**: Multiple factors required
- **Risk-based**: Adaptive authentication
- **Push notifications**: Mobile app approval
- **Hardware tokens**: Physical devices

### Single Sign-On (SSO)
- **Centralized authentication**: One login
- **Federation**: Cross-domain authentication
- **SAML**: Security Assertion Markup Language
- **OAuth**: Authorization framework
- **OpenID Connect**: Identity layer

## Authorization

### Permission Models
- **Read/Write/Execute**: File system permissions
- **CRUD**: Create, Read, Update, Delete
- **Custom permissions**: Application-specific
- **Negative permissions**: Explicit denials
- **Permission inheritance**: Hierarchical propagation

### Access Decision Process
- **Authentication**: Verify identity
- **Authorization**: Check permissions
- **Policy evaluation**: Apply access rules
- **Decision**: Allow or deny
- **Audit**: Log access attempts

## Identity Management

### Identity Lifecycle
- **Provisioning**: Account creation
- **Maintenance**: Profile updates
- **De-provisioning**: Account removal
- **Certification**: Access reviews
- **Governance**: Policy compliance

### Directory Services
- **LDAP**: Lightweight Directory Access Protocol
- **Active Directory**: Microsoft directory service
- **Identity providers**: Centralized identity
- **User repositories**: Identity storage
- **Synchronization**: Multi-system consistency

## Access Control Implementation

### Operating System Level
- **File permissions**: Unix/Linux permissions
- **User accounts**: System user management
- **Group membership**: Collective permissions
- **Sudo/UAC**: Privilege escalation
- **ACLs**: Extended permission lists

### Application Level
- **User authentication**: Application login
- **Session management**: User sessions
- **API security**: Service authentication
- **Database access**: Data permissions
- **Business logic**: Application rules

### Network Level
- **Firewall rules**: Network access control
- **VPN access**: Remote connectivity
- **Network segmentation**: Isolation boundaries
- **Port security**: Service access control
- **Intrusion prevention**: Threat blocking

## Privileged Access Management

### Privileged Accounts
- **Administrative accounts**: System administrators
- **Service accounts**: Application services
- **Emergency accounts**: Break-glass access
- **Shared accounts**: Multiple user access
- **Default accounts**: System defaults

### PAM Solutions
- **Password vaulting**: Secure storage
- **Session recording**: Activity monitoring
- **Just-in-time access**: Temporary elevation
- **Approval workflows**: Access requests
- **Rotation policies**: Regular password changes

## Zero Trust Architecture

### Core Principles
- **Never trust, always verify**: Continuous validation
- **Least privilege**: Minimal access rights
- **Assume breach**: Security-first mindset
- **Verify explicitly**: Multi-factor verification
- **Continuous monitoring**: Ongoing assessment

### Implementation
- **Identity verification**: Strong authentication
- **Device compliance**: Endpoint security
- **Network segmentation**: Micro-segmentation
- **Data protection**: Encryption and classification
- **Analytics**: Behavioral monitoring

## Compliance & Governance

### Regulatory Requirements
- **SOX**: Sarbanes-Oxley Act
- **GDPR**: General Data Protection Regulation
- **HIPAA**: Health Insurance Portability
- **PCI DSS**: Payment Card Industry
- **SOC 2**: Service Organization Control

### Access Governance
- **Access reviews**: Periodic certification
- **Segregation of duties**: Conflict prevention
- **Audit trails**: Access logging
- **Risk assessment**: Access risk evaluation
- **Policy enforcement**: Compliance monitoring