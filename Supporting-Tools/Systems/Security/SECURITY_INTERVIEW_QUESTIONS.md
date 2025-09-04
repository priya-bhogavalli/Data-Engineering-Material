# Security Interview Questions for Data Engineering

## Data Security Fundamentals

### Q1: What are the key security principles for data engineering?
**Answer:**
**CIA Triad:**
- **Confidentiality**: Protect sensitive data from unauthorized access
- **Integrity**: Ensure data accuracy and prevent unauthorized modification
- **Availability**: Maintain system uptime and data accessibility

**Additional Principles:**
- **Authentication**: Verify user identity
- **Authorization**: Control access to resources
- **Auditing**: Track and log all data access
- **Non-repudiation**: Prevent denial of actions
- **Data minimization**: Collect only necessary data
- **Privacy by design**: Build privacy into systems from the start

### Q2: How do you implement data encryption in transit and at rest?
**Answer:**
```python
# Encryption at rest
from cryptography.fernet import Fernet
import base64

# Generate encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt data
sensitive_data = "customer_ssn:123-45-6789"
encrypted_data = cipher_suite.encrypt(sensitive_data.encode())

# Decrypt data
decrypted_data = cipher_suite.decrypt(encrypted_data).decode()

# Database encryption (SQL Server)
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name NVARCHAR(100),
    ssn VARBINARY(256) -- Encrypted column
);

-- Insert encrypted data
INSERT INTO customers (id, name, ssn) 
VALUES (1, 'John Doe', EncryptByKey(Key_GUID('SSN_Key'), '123-45-6789'));
```

```bash
# Encryption in transit
# HTTPS/TLS for web APIs
curl -X POST https://api.example.com/data \
  -H "Content-Type: application/json" \
  -d '{"data": "sensitive_info"}'

# SSH for file transfers
scp -i private_key.pem data.csv user@server:/secure/path/

# Database connections with SSL
mysql --ssl-ca=ca-cert.pem --ssl-cert=client-cert.pem --ssl-key=client-key.pem
```

## Access Control & Authentication

### Q3: How do you implement role-based access control (RBAC)?
**Answer:**
```sql
-- Database RBAC implementation
-- Create roles
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;
CREATE ROLE data_admin;

-- Grant permissions to roles
GRANT SELECT ON sales_data TO data_analyst;
GRANT SELECT, INSERT, UPDATE ON sales_data TO data_engineer;
GRANT ALL PRIVILEGES ON sales_data TO data_admin;

-- Assign roles to users
GRANT data_analyst TO user_john;
GRANT data_engineer TO user_jane;
GRANT data_admin TO user_admin;

-- Row-level security
CREATE POLICY sales_policy ON sales_data
FOR SELECT TO data_analyst
USING (region = current_user_region());
```

```python
# Application-level RBAC
class RoleBasedAccessControl:
    def __init__(self):
        self.roles = {
            'analyst': ['read_data', 'create_reports'],
            'engineer': ['read_data', 'write_data', 'create_pipelines'],
            'admin': ['read_data', 'write_data', 'manage_users', 'delete_data']
        }
    
    def check_permission(self, user_role, action):
        return action in self.roles.get(user_role, [])
    
    def authorize(self, user_role, action):
        if not self.check_permission(user_role, action):
            raise PermissionError(f"User with role '{user_role}' cannot perform '{action}'")

# Usage
rbac = RoleBasedAccessControl()
rbac.authorize('analyst', 'read_data')  # OK
rbac.authorize('analyst', 'delete_data')  # Raises PermissionError
```

### Q4: How do you implement secure API authentication?
**Answer:**
```python
# JWT Token Authentication
import jwt
import datetime
from functools import wraps

class JWTAuth:
    def __init__(self, secret_key):
        self.secret_key = secret_key
    
    def generate_token(self, user_id, role):
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

# API Key Authentication
import hashlib
import secrets

class APIKeyAuth:
    def __init__(self):
        self.api_keys = {}  # In production, store in secure database
    
    def generate_api_key(self, user_id):
        api_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        self.api_keys[key_hash] = user_id
        return api_key
    
    def validate_api_key(self, api_key):
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        return self.api_keys.get(key_hash)

# OAuth 2.0 implementation
from authlib.integrations.flask_oauth2 import ResourceProtector
from authlib.oauth2.rfc6750 import BearerTokenValidator

class OAuth2Validator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        # Validate token with authorization server
        return validate_oauth_token(token_string)

require_oauth = ResourceProtector()
require_oauth.register_token_validator(OAuth2Validator())

@app.route('/api/data')
@require_oauth('read:data')
def get_data():
    return jsonify({"data": "sensitive information"})
```

## Data Privacy & Compliance

### Q5: How do you implement GDPR compliance in data systems?
**Answer:**
```python
# Data anonymization and pseudonymization
import hashlib
import uuid

class GDPRCompliance:
    def __init__(self):
        self.salt = "random_salt_value"
    
    def pseudonymize_email(self, email):
        """Pseudonymize email while maintaining referential integrity"""
        return hashlib.sha256((email + self.salt).encode()).hexdigest()
    
    def anonymize_ip(self, ip_address):
        """Anonymize IP address by masking last octet"""
        parts = ip_address.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0"
        return ip_address
    
    def generate_consent_record(self, user_id, purposes):
        """Track user consent for data processing"""
        return {
            'user_id': user_id,
            'consent_id': str(uuid.uuid4()),
            'purposes': purposes,
            'timestamp': datetime.datetime.utcnow(),
            'ip_address': self.anonymize_ip(request.remote_addr)
        }
    
    def right_to_be_forgotten(self, user_id):
        """Implement data deletion for GDPR compliance"""
        # Delete from all systems
        delete_user_data(user_id)
        log_deletion_request(user_id)

# Data retention policies
class DataRetentionPolicy:
    def __init__(self):
        self.retention_periods = {
            'user_activity': 365,  # days
            'transaction_data': 2555,  # 7 years
            'marketing_data': 1095,  # 3 years
        }
    
    def cleanup_expired_data(self):
        for data_type, retention_days in self.retention_periods.items():
            cutoff_date = datetime.datetime.now() - datetime.timedelta(days=retention_days)
            delete_data_before_date(data_type, cutoff_date)
```

### Q6: How do you implement data masking and tokenization?
**Answer:**
```python
# Data masking techniques
class DataMasking:
    @staticmethod
    def mask_credit_card(card_number):
        """Mask credit card number"""
        if len(card_number) >= 4:
            return '*' * (len(card_number) - 4) + card_number[-4:]
        return '*' * len(card_number)
    
    @staticmethod
    def mask_ssn(ssn):
        """Mask Social Security Number"""
        return f"XXX-XX-{ssn[-4:]}" if len(ssn) >= 4 else "XXX-XX-XXXX"
    
    @staticmethod
    def mask_email(email):
        """Mask email address"""
        local, domain = email.split('@')
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1] if len(local) > 2 else '*' * len(local)
        return f"{masked_local}@{domain}"

# Format-preserving encryption (FPE)
from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
import os

class TokenizationService:
    def __init__(self, key):
        self.key = key
        self.token_vault = {}  # In production, use secure database
    
    def tokenize(self, sensitive_data):
        """Replace sensitive data with non-sensitive token"""
        token = self.generate_token()
        self.token_vault[token] = self.encrypt(sensitive_data)
        return token
    
    def detokenize(self, token):
        """Retrieve original data using token"""
        encrypted_data = self.token_vault.get(token)
        if encrypted_data:
            return self.decrypt(encrypted_data)
        return None
    
    def generate_token(self):
        return secrets.token_urlsafe(16)
    
    def encrypt(self, data):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_data = self.pad_data(data.encode())
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted
    
    def decrypt(self, encrypted_data):
        iv = encrypted_data[:16]
        encrypted = encrypted_data[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted) + decryptor.finalize()
        return self.unpad_data(decrypted).decode()
```

## Security Monitoring & Auditing

### Q7: How do you implement security monitoring and alerting?
**Answer:**
```python
# Security event monitoring
import logging
from datetime import datetime, timedelta
from collections import defaultdict

class SecurityMonitor:
    def __init__(self):
        self.failed_attempts = defaultdict(list)
        self.suspicious_activities = []
        self.alert_thresholds = {
            'failed_login_attempts': 5,
            'data_access_rate': 1000,  # requests per minute
            'unusual_hours': (22, 6),  # 10 PM to 6 AM
        }
    
    def log_failed_login(self, user_id, ip_address):
        """Track failed login attempts"""
        timestamp = datetime.now()
        self.failed_attempts[user_id].append({
            'timestamp': timestamp,
            'ip_address': ip_address
        })
        
        # Check for brute force attack
        recent_attempts = [
            attempt for attempt in self.failed_attempts[user_id]
            if timestamp - attempt['timestamp'] < timedelta(minutes=15)
        ]
        
        if len(recent_attempts) >= self.alert_thresholds['failed_login_attempts']:
            self.trigger_alert('BRUTE_FORCE_ATTACK', {
                'user_id': user_id,
                'ip_address': ip_address,
                'attempts': len(recent_attempts)
            })
    
    def monitor_data_access(self, user_id, table_name, query_type):
        """Monitor data access patterns"""
        access_event = {
            'user_id': user_id,
            'table_name': table_name,
            'query_type': query_type,
            'timestamp': datetime.now(),
            'ip_address': self.get_client_ip()
        }
        
        # Check for unusual access patterns
        if self.is_unusual_access(access_event):
            self.trigger_alert('UNUSUAL_DATA_ACCESS', access_event)
        
        # Log all access events
        logging.info(f"Data access: {access_event}")
    
    def trigger_alert(self, alert_type, details):
        """Send security alert"""
        alert = {
            'type': alert_type,
            'timestamp': datetime.now(),
            'details': details,
            'severity': self.get_alert_severity(alert_type)
        }
        
        # Send to SIEM system
        self.send_to_siem(alert)
        
        # Send email notification for high severity
        if alert['severity'] == 'HIGH':
            self.send_email_alert(alert)

# Database activity monitoring
class DatabaseAuditLogger:
    def __init__(self, db_connection):
        self.db = db_connection
    
    def log_query(self, user_id, query, affected_rows=0):
        """Log all database queries"""
        audit_record = {
            'user_id': user_id,
            'query': query,
            'timestamp': datetime.now(),
            'affected_rows': affected_rows,
            'session_id': self.get_session_id()
        }
        
        # Insert into audit table
        self.db.execute("""
            INSERT INTO audit_log (user_id, query_text, timestamp, affected_rows, session_id)
            VALUES (?, ?, ?, ?, ?)
        """, audit_record.values())
    
    def detect_suspicious_queries(self, query):
        """Detect potentially malicious queries"""
        suspicious_patterns = [
            r'DROP\s+TABLE',
            r'DELETE\s+FROM.*WHERE\s+1=1',
            r'UNION\s+SELECT',
            r'--\s*$',  # SQL comments
            r"'\s*OR\s*'1'\s*=\s*'1'"  # SQL injection
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return True
        return False
```

### Q8: How do you implement secure data pipeline monitoring?
**Answer:**
```python
# Pipeline security monitoring
class PipelineSecurityMonitor:
    def __init__(self):
        self.data_lineage = {}
        self.access_logs = []
        self.data_quality_alerts = []
    
    def track_data_lineage(self, source, destination, transformation):
        """Track data movement and transformations"""
        lineage_record = {
            'source': source,
            'destination': destination,
            'transformation': transformation,
            'timestamp': datetime.now(),
            'user': self.get_current_user(),
            'checksum': self.calculate_checksum(source)
        }
        
        self.data_lineage[destination] = lineage_record
    
    def validate_data_integrity(self, dataset_id):
        """Validate data hasn't been tampered with"""
        lineage = self.data_lineage.get(dataset_id)
        if lineage:
            current_checksum = self.calculate_checksum(lineage['source'])
            if current_checksum != lineage['checksum']:
                self.trigger_integrity_alert(dataset_id, lineage)
    
    def monitor_pipeline_execution(self, pipeline_id, stage, status):
        """Monitor pipeline execution for anomalies"""
        execution_record = {
            'pipeline_id': pipeline_id,
            'stage': stage,
            'status': status,
            'timestamp': datetime.now(),
            'duration': self.get_stage_duration(pipeline_id, stage)
        }
        
        # Check for unusual execution times
        if self.is_unusual_duration(pipeline_id, stage, execution_record['duration']):
            self.trigger_performance_alert(execution_record)
    
    def scan_for_sensitive_data(self, dataset):
        """Scan datasets for sensitive information"""
        sensitive_patterns = {
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        }
        
        findings = {}
        for data_type, pattern in sensitive_patterns.items():
            matches = re.findall(pattern, str(dataset))
            if matches:
                findings[data_type] = len(matches)
        
        if findings:
            self.trigger_data_exposure_alert(findings)
        
        return findings
```

## Incident Response

### Q9: How do you implement security incident response procedures?
**Answer:**
```python
# Incident response framework
class SecurityIncidentResponse:
    def __init__(self):
        self.incident_status = {
            'OPEN': 'open',
            'INVESTIGATING': 'investigating',
            'CONTAINED': 'contained',
            'RESOLVED': 'resolved'
        }
        self.severity_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    
    def create_incident(self, incident_type, description, severity='MEDIUM'):
        """Create new security incident"""
        incident = {
            'id': self.generate_incident_id(),
            'type': incident_type,
            'description': description,
            'severity': severity,
            'status': self.incident_status['OPEN'],
            'created_at': datetime.now(),
            'assigned_to': self.get_on_call_analyst(),
            'timeline': []
        }
        
        # Immediate response based on severity
        if severity == 'CRITICAL':
            self.initiate_emergency_response(incident)
        
        return incident
    
    def contain_incident(self, incident_id):
        """Contain security incident"""
        containment_actions = [
            self.isolate_affected_systems,
            self.revoke_compromised_credentials,
            self.block_malicious_ips,
            self.preserve_evidence
        ]
        
        for action in containment_actions:
            try:
                action(incident_id)
                self.log_incident_action(incident_id, action.__name__, 'SUCCESS')
            except Exception as e:
                self.log_incident_action(incident_id, action.__name__, f'FAILED: {str(e)}')
    
    def collect_forensic_evidence(self, incident_id):
        """Collect evidence for forensic analysis"""
        evidence = {
            'system_logs': self.collect_system_logs(),
            'database_logs': self.collect_database_logs(),
            'network_traffic': self.collect_network_logs(),
            'file_hashes': self.calculate_file_hashes(),
            'memory_dumps': self.create_memory_dumps()
        }
        
        # Store evidence securely
        self.store_evidence(incident_id, evidence)
        return evidence
    
    def generate_incident_report(self, incident_id):
        """Generate comprehensive incident report"""
        incident = self.get_incident(incident_id)
        
        report = {
            'executive_summary': self.create_executive_summary(incident),
            'timeline': incident['timeline'],
            'impact_assessment': self.assess_impact(incident),
            'root_cause_analysis': self.perform_root_cause_analysis(incident),
            'lessons_learned': self.extract_lessons_learned(incident),
            'recommendations': self.generate_recommendations(incident)
        }
        
        return report
```

### Q10: How do you implement backup and disaster recovery security?
**Answer:**
```python
# Secure backup and disaster recovery
class SecureBackupManager:
    def __init__(self):
        self.encryption_key = self.load_encryption_key()
        self.backup_locations = ['primary', 'secondary', 'offsite']
    
    def create_secure_backup(self, data_source, backup_type='full'):
        """Create encrypted backup with integrity checks"""
        backup_id = self.generate_backup_id()
        
        # Create backup
        backup_data = self.extract_data(data_source, backup_type)
        
        # Encrypt backup
        encrypted_backup = self.encrypt_backup(backup_data)
        
        # Calculate integrity hash
        integrity_hash = self.calculate_hash(encrypted_backup)
        
        # Store backup metadata
        metadata = {
            'backup_id': backup_id,
            'source': data_source,
            'type': backup_type,
            'timestamp': datetime.now(),
            'size': len(encrypted_backup),
            'integrity_hash': integrity_hash,
            'encryption_algorithm': 'AES-256-GCM'
        }
        
        # Store in multiple locations
        for location in self.backup_locations:
            self.store_backup(location, backup_id, encrypted_backup, metadata)
        
        return backup_id
    
    def verify_backup_integrity(self, backup_id):
        """Verify backup integrity across all locations"""
        results = {}
        
        for location in self.backup_locations:
            try:
                backup_data, metadata = self.retrieve_backup(location, backup_id)
                current_hash = self.calculate_hash(backup_data)
                
                results[location] = {
                    'status': 'VALID' if current_hash == metadata['integrity_hash'] else 'CORRUPTED',
                    'hash_match': current_hash == metadata['integrity_hash'],
                    'size_match': len(backup_data) == metadata['size']
                }
            except Exception as e:
                results[location] = {'status': 'ERROR', 'error': str(e)}
        
        return results
    
    def disaster_recovery_procedure(self, recovery_point):
        """Execute disaster recovery with security validation"""
        recovery_steps = [
            self.validate_recovery_environment,
            self.restore_from_backup,
            self.verify_data_integrity,
            self.update_security_configurations,
            self.test_system_functionality,
            self.notify_stakeholders
        ]
        
        recovery_log = []
        
        for step in recovery_steps:
            try:
                result = step(recovery_point)
                recovery_log.append({
                    'step': step.__name__,
                    'status': 'SUCCESS',
                    'timestamp': datetime.now(),
                    'result': result
                })
            except Exception as e:
                recovery_log.append({
                    'step': step.__name__,
                    'status': 'FAILED',
                    'timestamp': datetime.now(),
                    'error': str(e)
                })
                # Stop recovery on critical failure
                if self.is_critical_step(step):
                    break
        
        return recovery_log
```

## Key Takeaways

**Essential Security Concepts for Data Engineering:**
- **Data encryption** at rest and in transit
- **Access control** with RBAC and authentication
- **Privacy compliance** (GDPR, CCPA, HIPAA)
- **Security monitoring** and incident response
- **Data masking** and tokenization
- **Audit logging** and forensic capabilities
- **Secure backup** and disaster recovery
- **Vulnerability management** and security testing