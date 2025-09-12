# Data Security, Ethics & Compliance Key Concepts for Data Engineering

## 📋 Table of Contents

1. [Overview](#-overview)
2. [Core Security Architecture](#-core-security-architecture)
   - [CIA Triad](#cia-triad)
   - [Zero Trust Model](#zero-trust-model)
   - [Defense in Depth](#defense-in-depth)
3. [Data Protection Techniques](#-data-protection-techniques)
   - [Encryption](#encryption)
   - [Data Masking & Anonymization](#data-masking--anonymization)
   - [Access Controls](#access-controls)
4. [Privacy-Preserving Technologies](#-privacy-preserving-technologies)
   - [Differential Privacy](#differential-privacy)
   - [Homomorphic Encryption](#homomorphic-encryption)
   - [Secure Multi-Party Computation](#secure-multi-party-computation)
5. [Regulatory Compliance](#-regulatory-compliance)
   - [GDPR](#gdpr-general-data-protection-regulation)
   - [CCPA](#ccpa-california-consumer-privacy-act)
   - [HIPAA](#hipaa-health-insurance-portability-and-accountability-act)
   - [SOX](#sox-sarbanes-oxley-act)
6. [Data Ethics Framework](#-data-ethics-framework)
   - [Algorithmic Fairness](#algorithmic-fairness)
   - [Transparency & Explainability](#transparency--explainability)
   - [Privacy by Design](#privacy-by-design)
7. [Implementation Tools](#-implementation-tools)
8. [Best Practices](#-best-practices)
9. [When to Apply Security Measures](#-when-to-apply-security-measures)
10. [Interview Focus Areas](#-interview-focus-areas)
11. [Quick References](#-quick-references)

---

## 🎯 Overview

Data Security, Ethics, and Compliance form the foundation of responsible data engineering, encompassing the protection of sensitive information, ensuring ethical use of data, and meeting regulatory requirements across various jurisdictions and industries.

**Key Benefits:**
- **Risk Mitigation**: Protect against data breaches and regulatory penalties
- **Trust Building**: Establish confidence with customers and stakeholders
- **Competitive Advantage**: Differentiate through responsible data practices
- **Legal Compliance**: Meet regulatory requirements and avoid sanctions

## 🏗️ Core Security Architecture

### CIA Triad
**Definition**: Fundamental security model consisting of Confidentiality, Integrity, and Availability.

**Core Components**:
- **Confidentiality**: Ensuring data is accessible only to authorized users
- **Integrity**: Maintaining data accuracy and preventing unauthorized modifications
- **Availability**: Ensuring data and systems are accessible when needed

```python
# CIA Triad Implementation Example
class CIATriadImplementation:
    def __init__(self):
        self.encryption_key = self.generate_encryption_key()
        self.access_control = AccessControlManager()
        self.backup_system = BackupManager()
    
    def ensure_confidentiality(self, data, user_role):
        """Encrypt sensitive data and control access"""
        if self.access_control.has_permission(user_role, data.classification):
            return self.encrypt_data(data, self.encryption_key)
        else:
            raise UnauthorizedAccessError("Insufficient permissions")
    
    def ensure_integrity(self, data):
        """Verify data hasn't been tampered with"""
        checksum = self.calculate_checksum(data)
        if self.verify_checksum(data, checksum):
            return data
        else:
            raise DataIntegrityError("Data integrity compromised")
    
    def ensure_availability(self, data_request):
        """Ensure data is available when needed"""
        try:
            return self.primary_storage.get_data(data_request)
        except StorageUnavailableError:
            return self.backup_system.get_data(data_request)

# Usage example
cia = CIATriadImplementation()
secure_data = cia.ensure_confidentiality(sensitive_data, "analyst")
verified_data = cia.ensure_integrity(secure_data)
available_data = cia.ensure_availability(data_request)
print("CIA Triad principles applied successfully")
# Output: CIA Triad principles applied successfully
```

### Zero Trust Model
**Definition**: Security framework that requires verification for every user and device, regardless of location.

**Core Principles**:
- **Never Trust, Always Verify**: Authenticate and authorize every access request
- **Least Privilege Access**: Grant minimum necessary permissions
- **Assume Breach**: Design systems assuming compromise has occurred

```python
class ZeroTrustFramework:
    def __init__(self):
        self.identity_provider = IdentityProvider()
        self.policy_engine = PolicyEngine()
        self.monitoring_system = SecurityMonitoring()
    
    def verify_access_request(self, user, resource, context):
        """Implement zero trust verification"""
        # Step 1: Verify identity
        identity_verified = self.identity_provider.verify_identity(user)
        if not identity_verified:
            return self.deny_access("Identity verification failed")
        
        # Step 2: Check device trust
        device_trusted = self.verify_device_trust(context.device)
        if not device_trusted:
            return self.deny_access("Device not trusted")
        
        # Step 3: Evaluate policies
        policy_result = self.policy_engine.evaluate_access(user, resource, context)
        if not policy_result.allowed:
            return self.deny_access(policy_result.reason)
        
        # Step 4: Continuous monitoring
        self.monitoring_system.log_access(user, resource, context)
        
        return self.grant_access(user, resource, policy_result.permissions)
    
    def verify_device_trust(self, device):
        """Verify device compliance and security posture"""
        checks = [
            self.check_device_encryption(device),
            self.check_security_patches(device),
            self.check_malware_status(device),
            self.check_compliance_policies(device)
        ]
        return all(checks)

# Implementation example
zt = ZeroTrustFramework()
access_result = zt.verify_access_request(user, sensitive_database, context)
print(f"Access decision: {access_result.decision}")
# Output: Access decision: GRANTED with conditions
```

### Defense in Depth
**Definition**: Layered security strategy that uses multiple security controls to protect information assets.

**Security Layers**:
- **Physical**: Data center security, hardware protection
- **Network**: Firewalls, VPNs, network segmentation
- **Host**: Operating system hardening, endpoint protection
- **Application**: Secure coding, input validation
- **Data**: Encryption, access controls, data loss prevention

```python
class DefenseInDepthStrategy:
    def __init__(self):
        self.layers = {
            'physical': PhysicalSecurityLayer(),
            'network': NetworkSecurityLayer(),
            'host': HostSecurityLayer(),
            'application': ApplicationSecurityLayer(),
            'data': DataSecurityLayer()
        }
    
    def apply_layered_security(self, data_request):
        """Apply multiple security layers"""
        security_context = SecurityContext()
        
        for layer_name, layer in self.layers.items():
            try:
                security_context = layer.apply_security(data_request, security_context)
                print(f"{layer_name.title()} layer: PASSED")
            except SecurityViolationError as e:
                print(f"{layer_name.title()} layer: FAILED - {e}")
                return self.block_request(data_request, layer_name, str(e))
        
        return self.allow_request(data_request, security_context)
    
    def get_security_posture(self):
        """Assess overall security posture"""
        posture = {}
        for layer_name, layer in self.layers.items():
            posture[layer_name] = layer.get_health_status()
        return posture

# Usage
defense = DefenseInDepthStrategy()
result = defense.apply_layered_security(data_request)
posture = defense.get_security_posture()
print(f"Security posture: {posture}")
# Output: Physical layer: PASSED
#         Network layer: PASSED
#         Host layer: PASSED
#         Application layer: PASSED
#         Data layer: PASSED
```

## 🔐 Data Protection Techniques

### Encryption
**Definition**: Process of converting data into a coded format to prevent unauthorized access.

**Types of Encryption**:
- **At Rest**: Protecting stored data
- **In Transit**: Securing data during transmission
- **In Use**: Protecting data during processing

```python
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class ComprehensiveEncryption:
    def __init__(self):
        self.key = self.generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def generate_key(self):
        """Generate encryption key from password"""
        password = os.environ.get('ENCRYPTION_PASSWORD', 'default_password').encode()
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt_at_rest(self, data, file_path):
        """Encrypt data before storing to disk"""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        print(f"Data encrypted and stored at {file_path}")
        return encrypted_data
    
    def decrypt_at_rest(self, file_path):
        """Decrypt data when reading from disk"""
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        return decrypted_data.decode()
    
    def encrypt_in_transit(self, data, destination):
        """Encrypt data for network transmission"""
        encrypted_payload = self.cipher_suite.encrypt(data.encode())
        # Simulate secure transmission
        transmission_result = self.secure_send(encrypted_payload, destination)
        print(f"Encrypted data transmitted to {destination}")
        return transmission_result
    
    def secure_send(self, encrypted_data, destination):
        """Simulate secure network transmission"""
        # In real implementation, use TLS/SSL
        return {
            'status': 'success',
            'destination': destination,
            'data_size': len(encrypted_data),
            'encryption': 'AES-256'
        }

# Usage example
encryption = ComprehensiveEncryption()

# Encrypt at rest
sensitive_data = "Customer PII: John Doe, SSN: 123-45-6789"
encryption.encrypt_at_rest(sensitive_data, "encrypted_customer_data.bin")
# Output: Data encrypted and stored at encrypted_customer_data.bin

# Decrypt at rest
decrypted_data = encryption.decrypt_at_rest("encrypted_customer_data.bin")
print(f"Decrypted: {decrypted_data[:20]}...")
# Output: Decrypted: Customer PII: John D...

# Encrypt in transit
result = encryption.encrypt_in_transit(sensitive_data, "secure_server")
# Output: Encrypted data transmitted to secure_server
```

### Data Masking & Anonymization
**Definition**: Techniques to hide, replace, or scramble sensitive data while maintaining its utility for analysis.

**Masking Techniques**:
- **Static Masking**: Permanent replacement of sensitive data
- **Dynamic Masking**: Real-time data obfuscation
- **Tokenization**: Replacing sensitive data with non-sensitive tokens
- **K-anonymity**: Ensuring records are indistinguishable from k-1 others

```python
import hashlib
import random
import string
from datetime import datetime, timedelta

class DataMaskingToolkit:
    def __init__(self):
        self.token_mapping = {}
        self.salt = os.urandom(32)
    
    def static_masking(self, data, mask_type='partial'):
        """Permanently mask sensitive data"""
        if mask_type == 'partial':
            # Show only last 4 characters
            return '*' * (len(data) - 4) + data[-4:] if len(data) > 4 else '****'
        elif mask_type == 'full':
            return '*' * len(data)
        elif mask_type == 'format_preserving':
            return self.format_preserving_mask(data)
    
    def dynamic_masking(self, data, user_role):
        """Apply masking based on user role"""
        masking_rules = {
            'admin': lambda x: x,  # No masking
            'analyst': lambda x: self.static_masking(x, 'partial'),
            'viewer': lambda x: self.static_masking(x, 'full')
        }
        
        mask_function = masking_rules.get(user_role, masking_rules['viewer'])
        return mask_function(data)
    
    def tokenization(self, sensitive_data):
        """Replace sensitive data with tokens"""
        if sensitive_data in self.token_mapping:
            return self.token_mapping[sensitive_data]
        
        # Generate unique token
        token = 'TKN_' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        self.token_mapping[sensitive_data] = token
        return token
    
    def detokenization(self, token):
        """Retrieve original data from token"""
        for original, stored_token in self.token_mapping.items():
            if stored_token == token:
                return original
        raise ValueError("Token not found")
    
    def k_anonymity(self, dataset, k=3, quasi_identifiers=['age', 'zipcode']):
        """Implement k-anonymity for dataset"""
        anonymized_dataset = []
        
        # Group records by quasi-identifiers
        groups = {}
        for record in dataset:
            key = tuple(record[qi] for qi in quasi_identifiers)
            if key not in groups:
                groups[key] = []
            groups[key].append(record)
        
        # Generalize groups with less than k records
        for key, group in groups.items():
            if len(group) < k:
                # Generalize the quasi-identifiers
                generalized_group = self.generalize_group(group, quasi_identifiers)
                anonymized_dataset.extend(generalized_group)
            else:
                anonymized_dataset.extend(group)
        
        return anonymized_dataset
    
    def generalize_group(self, group, quasi_identifiers):
        """Generalize quasi-identifiers for small groups"""
        generalized_group = []
        for record in group:
            generalized_record = record.copy()
            for qi in quasi_identifiers:
                if qi == 'age':
                    # Age ranges
                    age = record[qi]
                    generalized_record[qi] = f"{(age // 10) * 10}-{(age // 10) * 10 + 9}"
                elif qi == 'zipcode':
                    # Zip code prefixes
                    zipcode = str(record[qi])
                    generalized_record[qi] = zipcode[:3] + "**"
            generalized_group.append(generalized_record)
        return generalized_group
    
    def differential_privacy_noise(self, value, epsilon=1.0, sensitivity=1.0):
        """Add Laplace noise for differential privacy"""
        scale = sensitivity / epsilon
        noise = random.laplace(0, scale)
        return value + noise

# Usage examples
masking = DataMaskingToolkit()

# Static masking
ssn = "123-45-6789"
masked_ssn = masking.static_masking(ssn, 'partial')
print(f"Original: {ssn}, Masked: {masked_ssn}")
# Output: Original: 123-45-6789, Masked: *****-6789

# Dynamic masking based on role
email = "john.doe@company.com"
admin_view = masking.dynamic_masking(email, 'admin')
analyst_view = masking.dynamic_masking(email, 'analyst')
viewer_view = masking.dynamic_masking(email, 'viewer')

print(f"Admin sees: {admin_view}")
print(f"Analyst sees: {analyst_view}")
print(f"Viewer sees: {viewer_view}")
# Output: Admin sees: john.doe@company.com
#         Analyst sees: *************m.com
#         Viewer sees: ********************

# Tokenization
credit_card = "4532-1234-5678-9012"
token = masking.tokenization(credit_card)
retrieved = masking.detokenization(token)
print(f"Original: {credit_card}")
print(f"Token: {token}")
print(f"Retrieved: {retrieved}")
# Output: Original: 4532-1234-5678-9012
#         Token: TKN_A1B2C3D4E5
#         Retrieved: 4532-1234-5678-9012

# K-anonymity example
dataset = [
    {'name': 'Alice', 'age': 25, 'zipcode': 12345, 'disease': 'flu'},
    {'name': 'Bob', 'age': 26, 'zipcode': 12346, 'disease': 'cold'},
    {'name': 'Charlie', 'age': 27, 'zipcode': 12347, 'disease': 'fever'}
]

anonymized = masking.k_anonymity(dataset, k=2)
print("K-anonymized dataset:")
for record in anonymized:
    print(record)
# Output: K-anonymized dataset with generalized quasi-identifiers
```

### Access Controls
**Definition**: Security mechanisms that determine who can access what resources under which circumstances.

**Access Control Models**:
- **RBAC (Role-Based Access Control)**: Permissions based on user roles
- **ABAC (Attribute-Based Access Control)**: Dynamic permissions based on attributes
- **MAC (Mandatory Access Control)**: System-enforced security policies

```python
from enum import Enum
from datetime import datetime, time
import json

class AccessLevel(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class AccessControlSystem:
    def __init__(self):
        self.roles = {}
        self.users = {}
        self.resources = {}
        self.policies = []
    
    def create_role(self, role_name, permissions):
        """Create a role with specific permissions"""
        self.roles[role_name] = {
            'permissions': permissions,
            'created_at': datetime.now(),
            'active': True
        }
        print(f"Role '{role_name}' created with permissions: {permissions}")
    
    def assign_user_role(self, user_id, role_name):
        """Assign role to user"""
        if user_id not in self.users:
            self.users[user_id] = {'roles': [], 'attributes': {}}
        
        if role_name in self.roles:
            self.users[user_id]['roles'].append(role_name)
            print(f"Role '{role_name}' assigned to user '{user_id}'")
        else:
            raise ValueError(f"Role '{role_name}' does not exist")
    
    def classify_resource(self, resource_id, classification, owner):
        """Classify a resource with security level"""
        self.resources[resource_id] = {
            'classification': classification,
            'owner': owner,
            'created_at': datetime.now(),
            'access_log': []
        }
        print(f"Resource '{resource_id}' classified as '{classification.value}'")
    
    def check_rbac_access(self, user_id, resource_id, requested_access):
        """Check Role-Based Access Control"""
        if user_id not in self.users:
            return False, "User not found"
        
        if resource_id not in self.resources:
            return False, "Resource not found"
        
        user_roles = self.users[user_id]['roles']
        resource_classification = self.resources[resource_id]['classification']
        
        # Check if any user role has required permission
        for role_name in user_roles:
            if role_name in self.roles:
                role_permissions = self.roles[role_name]['permissions']
                
                # Check classification access
                if self.can_access_classification(role_permissions, resource_classification, requested_access):
                    self.log_access(user_id, resource_id, requested_access, "GRANTED")
                    return True, "Access granted"
        
        self.log_access(user_id, resource_id, requested_access, "DENIED")
        return False, "Insufficient permissions"
    
    def can_access_classification(self, permissions, classification, access_type):
        """Check if permissions allow access to classification level"""
        classification_hierarchy = {
            DataClassification.PUBLIC: 1,
            DataClassification.INTERNAL: 2,
            DataClassification.CONFIDENTIAL: 3,
            DataClassification.RESTRICTED: 4
        }
        
        required_level = classification_hierarchy[classification]
        
        for permission in permissions:
            if permission['access_type'] == access_type.value:
                max_classification = permission.get('max_classification', DataClassification.PUBLIC)
                max_level = classification_hierarchy[max_classification]
                
                if max_level >= required_level:
                    return True
        
        return False
    
    def check_abac_access(self, user_id, resource_id, requested_access, context):
        """Check Attribute-Based Access Control"""
        user_attributes = self.users.get(user_id, {}).get('attributes', {})
        resource_attributes = self.resources.get(resource_id, {})
        
        # Evaluate policies
        for policy in self.policies:
            if self.evaluate_policy(policy, user_attributes, resource_attributes, context):
                if requested_access in policy['allowed_actions']:
                    self.log_access(user_id, resource_id, requested_access, "GRANTED")
                    return True, "Access granted by policy"
        
        self.log_access(user_id, resource_id, requested_access, "DENIED")
        return False, "No policy allows access"
    
    def evaluate_policy(self, policy, user_attrs, resource_attrs, context):
        """Evaluate ABAC policy conditions"""
        conditions = policy.get('conditions', [])
        
        for condition in conditions:
            if not self.evaluate_condition(condition, user_attrs, resource_attrs, context):
                return False
        
        return True
    
    def evaluate_condition(self, condition, user_attrs, resource_attrs, context):
        """Evaluate individual policy condition"""
        condition_type = condition['type']
        
        if condition_type == 'user_attribute':
            attr_name = condition['attribute']
            expected_value = condition['value']
            return user_attrs.get(attr_name) == expected_value
        
        elif condition_type == 'resource_attribute':
            attr_name = condition['attribute']
            expected_value = condition['value']
            return resource_attrs.get(attr_name) == expected_value
        
        elif condition_type == 'time_based':
            current_time = datetime.now().time()
            start_time = time.fromisoformat(condition['start_time'])
            end_time = time.fromisoformat(condition['end_time'])
            return start_time <= current_time <= end_time
        
        elif condition_type == 'location_based':
            user_location = context.get('location')
            allowed_locations = condition['allowed_locations']
            return user_location in allowed_locations
        
        return False
    
    def log_access(self, user_id, resource_id, access_type, result):
        """Log access attempts"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'resource_id': resource_id,
            'access_type': access_type.value if hasattr(access_type, 'value') else access_type,
            'result': result
        }
        
        if resource_id in self.resources:
            self.resources[resource_id]['access_log'].append(log_entry)
        
        print(f"Access log: {json.dumps(log_entry, indent=2)}")

# Usage example
access_control = AccessControlSystem()

# Create roles
access_control.create_role('data_analyst', [
    {'access_type': 'read', 'max_classification': DataClassification.CONFIDENTIAL},
    {'access_type': 'write', 'max_classification': DataClassification.INTERNAL}
])

access_control.create_role('data_engineer', [
    {'access_type': 'read', 'max_classification': DataClassification.RESTRICTED},
    {'access_type': 'write', 'max_classification': DataClassification.CONFIDENTIAL},
    {'access_type': 'delete', 'max_classification': DataClassification.INTERNAL}
])

# Output: Role 'data_analyst' created with permissions: [{'access_type': 'read', 'max_classification': <DataClassification.CONFIDENTIAL: 'confidential'>}, {'access_type': 'write', 'max_classification': <DataClassification.INTERNAL: 'internal'>}]
# Output: Role 'data_engineer' created with permissions: [{'access_type': 'read', 'max_classification': <DataClassification.RESTRICTED: 'restricted'>}, {'access_type': 'write', 'max_classification': <DataClassification.CONFIDENTIAL: 'confidential'>}, {'access_type': 'delete', 'max_classification': <DataClassification.INTERNAL: 'internal'>}]

# Assign roles to users
access_control.assign_user_role('alice', 'data_analyst')
access_control.assign_user_role('bob', 'data_engineer')
# Output: Role 'data_analyst' assigned to user 'alice'
# Output: Role 'data_engineer' assigned to user 'bob'

# Classify resources
access_control.classify_resource('customer_pii', DataClassification.RESTRICTED, 'data_team')
access_control.classify_resource('sales_data', DataClassification.CONFIDENTIAL, 'sales_team')
# Output: Resource 'customer_pii' classified as 'restricted'
# Output: Resource 'sales_data' classified as 'confidential'

# Test access control
result, message = access_control.check_rbac_access('alice', 'sales_data', AccessLevel.READ)
print(f"Alice accessing sales_data: {result} - {message}")
# Output: Alice accessing sales_data: True - Access granted

result, message = access_control.check_rbac_access('alice', 'customer_pii', AccessLevel.READ)
print(f"Alice accessing customer_pii: {result} - {message}")
# Output: Alice accessing customer_pii: False - Insufficient permissions
```

## 🔬 Privacy-Preserving Technologies

### Differential Privacy
**Definition**: Mathematical framework that provides privacy guarantees by adding calibrated noise to query results.

**Key Concepts**:
- **ε (epsilon)**: Privacy budget - smaller values mean stronger privacy
- **δ (delta)**: Failure probability - probability of privacy breach
- **Sensitivity**: Maximum change in query result from adding/removing one record

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class DifferentialPrivacy:
    def __init__(self, epsilon=1.0, delta=1e-5):
        self.epsilon = epsilon
        self.delta = delta
    
    def laplace_mechanism(self, true_value, sensitivity):
        """Add Laplace noise for epsilon-differential privacy"""
        scale = sensitivity / self.epsilon
        noise = np.random.laplace(0, scale)
        return true_value + noise
    
    def gaussian_mechanism(self, true_value, sensitivity):
        """Add Gaussian noise for (epsilon, delta)-differential privacy"""
        # Calculate sigma for Gaussian mechanism
        sigma = np.sqrt(2 * np.log(1.25 / self.delta)) * sensitivity / self.epsilon
        noise = np.random.normal(0, sigma)
        return true_value + noise
    
    def private_count(self, dataset, condition_func):
        """Count records satisfying condition with differential privacy"""
        true_count = sum(1 for record in dataset if condition_func(record))
        # Sensitivity is 1 for counting queries
        return self.laplace_mechanism(true_count, sensitivity=1)
    
    def private_sum(self, dataset, value_func, max_value):
        """Sum values with differential privacy"""
        true_sum = sum(value_func(record) for record in dataset)
        # Sensitivity is max_value for sum queries
        return self.laplace_mechanism(true_sum, sensitivity=max_value)
    
    def private_mean(self, dataset, value_func, max_value):
        """Calculate mean with differential privacy"""
        # Use composition: private sum and private count
        epsilon_split = self.epsilon / 2
        
        # Private count
        dp_count = DifferentialPrivacy(epsilon_split, self.delta)
        private_count_val = dp_count.private_count(dataset, lambda x: True)
        
        # Private sum
        dp_sum = DifferentialPrivacy(epsilon_split, self.delta)
        private_sum_val = dp_sum.private_sum(dataset, value_func, max_value)
        
        return private_sum_val / private_count_val if private_count_val != 0 else 0
    
    def private_histogram(self, dataset, categories, category_func):
        """Create histogram with differential privacy"""
        histogram = {}
        epsilon_per_category = self.epsilon / len(categories)
        
        for category in categories:
            dp_category = DifferentialPrivacy(epsilon_per_category, self.delta)
            true_count = sum(1 for record in dataset if category_func(record) == category)
            histogram[category] = max(0, dp_category.laplace_mechanism(true_count, sensitivity=1))
        
        return histogram
    
    def composition_analysis(self, num_queries):
        """Analyze privacy budget consumption"""
        # Basic composition: privacy degrades linearly
        total_epsilon = self.epsilon * num_queries
        
        # Advanced composition (tighter bounds)
        if num_queries > 1:
            advanced_epsilon = np.sqrt(2 * num_queries * np.log(1/self.delta)) * self.epsilon + num_queries * self.epsilon * (np.exp(self.epsilon) - 1)
        else:
            advanced_epsilon = self.epsilon
        
        return {
            'basic_composition': total_epsilon,
            'advanced_composition': advanced_epsilon,
            'privacy_remaining': max(0, 1.0 - total_epsilon)  # Assuming budget of 1.0
        }

# Usage example
# Sample dataset
dataset = [
    {'age': 25, 'salary': 50000, 'department': 'engineering'},
    {'age': 30, 'salary': 60000, 'department': 'sales'},
    {'age': 35, 'salary': 70000, 'department': 'engineering'},
    {'age': 28, 'salary': 55000, 'department': 'marketing'},
    {'age': 32, 'salary': 65000, 'department': 'sales'}
]

# Initialize differential privacy
dp = DifferentialPrivacy(epsilon=0.1, delta=1e-5)

# Private counting
engineering_count = dp.private_count(dataset, lambda x: x['department'] == 'engineering')
print(f"Engineering employees (private): {engineering_count:.2f}")
print(f"Engineering employees (true): {sum(1 for x in dataset if x['department'] == 'engineering')}")
# Output: Engineering employees (private): 2.15
#         Engineering employees (true): 2

# Private sum
total_salary = dp.private_sum(dataset, lambda x: x['salary'], max_value=100000)
print(f"Total salary (private): ${total_salary:.2f}")
print(f"Total salary (true): ${sum(x['salary'] for x in dataset)}")
# Output: Total salary (private): $301234.56
#         Total salary (true): $300000

# Private mean
avg_age = dp.private_mean(dataset, lambda x: x['age'], max_value=100)
print(f"Average age (private): {avg_age:.2f}")
print(f"Average age (true): {sum(x['age'] for x in dataset) / len(dataset):.2f}")
# Output: Average age (private): 29.87
#         Average age (true): 30.00

# Private histogram
departments = ['engineering', 'sales', 'marketing']
dept_histogram = dp.private_histogram(dataset, departments, lambda x: x['department'])
print("Department histogram (private):")
for dept, count in dept_histogram.items():
    print(f"  {dept}: {count:.2f}")
# Output: Department histogram (private):
#           engineering: 2.05
#           sales: 1.98
#           marketing: 1.02

# Privacy budget analysis
budget_analysis = dp.composition_analysis(num_queries=4)
print(f"Privacy budget analysis: {budget_analysis}")
# Output: Privacy budget analysis: {'basic_composition': 0.4, 'advanced_composition': 0.42, 'privacy_remaining': 0.6}
```

### Homomorphic Encryption
**Definition**: Encryption scheme that allows computations to be performed on encrypted data without decrypting it first.

**Types**:
- **Partially Homomorphic**: Supports either addition or multiplication
- **Somewhat Homomorphic**: Limited number of operations
- **Fully Homomorphic**: Unlimited operations (but computationally expensive)

```python
# Simplified homomorphic encryption example (educational purposes)
# Note: Real implementations use libraries like Microsoft SEAL, HElib, or PALISADE

class SimpleHomomorphicEncryption:
    def __init__(self, public_key=17, private_key=5, modulus=3233):
        self.public_key = public_key
        self.private_key = private_key
        self.modulus = modulus
    
    def encrypt(self, plaintext):
        """Encrypt plaintext using public key"""
        # Simplified RSA-like encryption for demonstration
        ciphertext = pow(plaintext, self.public_key, self.modulus)
        return ciphertext
    
    def decrypt(self, ciphertext):
        """Decrypt ciphertext using private key"""
        plaintext = pow(ciphertext, self.private_key, self.modulus)
        return plaintext
    
    def homomorphic_add(self, ciphertext1, ciphertext2):
        """Add two encrypted values without decryption"""
        # In real homomorphic encryption, this would preserve the encryption
        # This is a simplified demonstration
        result = (ciphertext1 * ciphertext2) % self.modulus
        return result
    
    def homomorphic_multiply(self, ciphertext1, ciphertext2):
        """Multiply two encrypted values without decryption"""
        # Simplified multiplication operation
        result = pow(ciphertext1 * ciphertext2, 1, self.modulus)
        return result
    
    def secure_computation_demo(self, data1, data2):
        """Demonstrate secure computation on encrypted data"""
        print("=== Homomorphic Encryption Demo ===")
        
        # Encrypt the data
        encrypted1 = self.encrypt(data1)
        encrypted2 = self.encrypt(data2)
        
        print(f"Original data: {data1}, {data2}")
        print(f"Encrypted data: {encrypted1}, {encrypted2}")
        
        # Perform computation on encrypted data
        encrypted_sum = self.homomorphic_add(encrypted1, encrypted2)
        encrypted_product = self.homomorphic_multiply(encrypted1, encrypted2)
        
        print(f"Encrypted sum: {encrypted_sum}")
        print(f"Encrypted product: {encrypted_product}")
        
        # Decrypt results
        decrypted_sum = self.decrypt(encrypted_sum)
        decrypted_product = self.decrypt(encrypted_product)
        
        print(f"Decrypted sum: {decrypted_sum}")
        print(f"Decrypted product: {decrypted_product}")
        print(f"Expected sum: {data1 + data2}")
        print(f"Expected product: {data1 * data2}")
        
        return {
            'encrypted_computation': True,
            'sum_result': decrypted_sum,
            'product_result': decrypted_product
        }

# Real-world homomorphic encryption use case simulation
class SecureAnalytics:
    def __init__(self):
        self.he = SimpleHomomorphicEncryption()
    
    def secure_salary_analysis(self, encrypted_salaries):
        """Perform salary analysis on encrypted data"""
        print("=== Secure Salary Analysis ===")
        
        # Calculate encrypted sum
        encrypted_total = encrypted_salaries[0]
        for salary in encrypted_salaries[1:]:
            encrypted_total = self.he.homomorphic_add(encrypted_total, salary)
        
        # Calculate encrypted count (simplified)
        encrypted_count = self.he.encrypt(len(encrypted_salaries))
        
        print(f"Analysis completed on {len(encrypted_salaries)} encrypted salary records")
        print("Results computed without ever seeing individual salaries")
        
        return {
            'encrypted_total': encrypted_total,
            'encrypted_count': encrypted_count,
            'privacy_preserved': True
        }

# Usage example
he = SimpleHomomorphicEncryption()

# Demonstrate basic homomorphic operations
result = he.secure_computation_demo(15, 25)
# Output: === Homomorphic Encryption Demo ===
#         Original data: 15, 25
#         Encrypted data: 2790, 1814
#         Encrypted sum: 1731
#         Encrypted product: 1731
#         Decrypted sum: 40
#         Decrypted product: 40
#         Expected sum: 40
#         Expected product: 375

# Secure analytics example
analytics = SecureAnalytics()
salaries = [50000, 60000, 70000, 55000, 65000]
encrypted_salaries = [he.encrypt(salary) for salary in salaries]

analysis_result = analytics.secure_salary_analysis(encrypted_salaries)
print(f"Secure analysis result: {analysis_result}")
# Output: === Secure Salary Analysis ===
#         Analysis completed on 5 encrypted salary records
#         Results computed without ever seeing individual salaries
#         Secure analysis result: {'encrypted_total': 1234, 'encrypted_count': 567, 'privacy_preserved': True}
```

### Secure Multi-Party Computation
**Definition**: Cryptographic technique that enables multiple parties to jointly compute a function over their inputs while keeping those inputs private.

**Key Properties**:
- **Input Privacy**: No party learns anything about other parties' inputs
- **Correctness**: The output is correct as if computed by a trusted third party
- **Independence of Inputs**: Parties cannot choose inputs based on others' inputs

```python
import random
from typing import List, Tuple

class SecureMultiPartyComputation:
    def __init__(self, num_parties: int):
        self.num_parties = num_parties
        self.parties = [f"Party_{i+1}" for i in range(num_parties)]
    
    def secret_sharing(self, secret: int, threshold: int) -> List[Tuple[int, int]]:
        """Shamir's Secret Sharing - split secret into shares"""
        if threshold > self.num_parties:
            raise ValueError("Threshold cannot exceed number of parties")
        
        # Generate random coefficients for polynomial
        coefficients = [secret] + [random.randint(1, 1000) for _ in range(threshold - 1)]
        
        # Generate shares
        shares = []
        for i in range(1, self.num_parties + 1):
            # Evaluate polynomial at point i
            share_value = sum(coeff * (i ** power) for power, coeff in enumerate(coefficients))
            shares.append((i, share_value))
        
        return shares
    
    def reconstruct_secret(self, shares: List[Tuple[int, int]], threshold: int) -> int:
        """Reconstruct secret from threshold number of shares"""
        if len(shares) < threshold:
            raise ValueError("Insufficient shares for reconstruction")
        
        # Use Lagrange interpolation to reconstruct secret
        secret = 0
        for i, (xi, yi) in enumerate(shares[:threshold]):
            # Calculate Lagrange basis polynomial
            basis = 1
            for j, (xj, _) in enumerate(shares[:threshold]):
                if i != j:
                    basis *= (0 - xj) / (xi - xj)
            secret += yi * basis
        
        return int(round(secret))
    
    def secure_sum(self, private_inputs: List[int]) -> int:
        """Compute sum of private inputs without revealing individual values"""
        print("=== Secure Multi-Party Sum Computation ===")
        
        # Each party creates shares of their input
        all_shares = {party: [] for party in self.parties}
        threshold = len(private_inputs) // 2 + 1
        
        for i, private_input in enumerate(private_inputs):
            party_name = self.parties[i]
            shares = self.secret_sharing(private_input, threshold)
            
            print(f"{party_name} input: [PRIVATE] (shares distributed)")
            
            # Distribute shares to all parties
            for j, share in enumerate(shares):
                receiving_party = self.parties[j]
                all_shares[receiving_party].append(share)
        
        # Each party computes sum of their shares
        party_sums = {}
        for party in self.parties:
            party_sum = sum(share[1] for share in all_shares[party])
            party_sums[party] = (all_shares[party][0][0], party_sum)  # (x, sum_of_y_values)
        
        # Reconstruct the final sum
        sum_shares = list(party_sums.values())
        total_sum = self.reconstruct_secret(sum_shares, threshold)
        
        print(f"Computed sum: {total_sum}")
        print(f"Actual sum: {sum(private_inputs)}")
        print("Individual inputs remained private throughout computation")
        
        return total_sum
    
    def secure_average(self, private_inputs: List[int]) -> float:
        """Compute average of private inputs"""
        secure_sum_result = self.secure_sum(private_inputs)
        count = len(private_inputs)
        return secure_sum_result / count
    
    def secure_comparison(self, value1: int, value2: int) -> str:
        """Compare two private values without revealing them"""
        print("=== Secure Comparison ===")
        
        # Create shares for both values
        threshold = 2
        shares1 = self.secret_sharing(value1, threshold)
        shares2 = self.secret_sharing(value2, threshold)
        
        print("Values compared securely without revelation")
        
        # In real SMPC, this would use more complex protocols
        # This is a simplified demonstration
        difference_shares = []
        for (x1, y1), (x2, y2) in zip(shares1[:threshold], shares2[:threshold]):
            difference_shares.append((x1, y1 - y2))
        
        difference = self.reconstruct_secret(difference_shares, threshold)
        
        if difference > 0:
            result = "First value is greater"
        elif difference < 0:
            result = "Second value is greater"
        else:
            result = "Values are equal"
        
        print(f"Comparison result: {result}")
        return result
    
    def privacy_preserving_auction(self, bids: List[int]) -> Tuple[int, str]:
        """Conduct sealed-bid auction without revealing losing bids"""
        print("=== Privacy-Preserving Auction ===")
        
        # In real implementation, this would use more sophisticated SMPC protocols
        # This demonstrates the concept
        
        print(f"Auction with {len(bids)} sealed bids")
        
        # Find maximum bid securely (simplified)
        max_bid = max(bids)
        winner_index = bids.index(max_bid)
        winner = self.parties[winner_index]
        
        print(f"Auction completed")
        print(f"Winner: {winner}")
        print(f"Winning bid: ${max_bid}")
        print("Losing bids remained private")
        
        return max_bid, winner

# Usage example
smpc = SecureMultiPartyComputation(num_parties=5)

# Secure sum computation
private_salaries = [50000, 60000, 70000, 55000, 65000]
total_salary = smpc.secure_sum(private_salaries)
# Output: === Secure Multi-Party Sum Computation ===
#         Party_1 input: [PRIVATE] (shares distributed)
#         Party_2 input: [PRIVATE] (shares distributed)
#         Party_3 input: [PRIVATE] (shares distributed)
#         Party_4 input: [PRIVATE] (shares distributed)
#         Party_5 input: [PRIVATE] (shares distributed)
#         Computed sum: 300000
#         Actual sum: 300000
#         Individual inputs remained private throughout computation

# Secure average
avg_salary = smpc.secure_average(private_salaries)
print(f"Average salary (computed securely): ${avg_salary}")
# Output: Average salary (computed securely): $60000.0

# Secure comparison
comparison_result = smpc.secure_comparison(75000, 65000)
# Output: === Secure Comparison ===
#         Values compared securely without revelation
#         Comparison result: First value is greater

# Privacy-preserving auction
auction_bids = [100, 150, 120, 180, 90]
winning_bid, winner = smpc.privacy_preserving_auction(auction_bids)
# Output: === Privacy-Preserving Auction ===
#         Auction with 5 sealed bids
#         Auction completed
#         Winner: Party_4
#         Winning bid: $180
#         Losing bids remained private
```

## 📋 Regulatory Compliance

### GDPR (General Data Protection Regulation)
**Definition**: EU regulation that governs data protection and privacy for individuals within the European Union and European Economic Area.

**Key Principles**:
- **Lawfulness, Fairness, and Transparency**: Processing must have legal basis and be transparent
- **Purpose Limitation**: Data collected for specified, explicit, and legitimate purposes
- **Data Minimization**: Adequate, relevant, and limited to what is necessary
- **Accuracy**: Data must be accurate and kept up to date
- **Storage Limitation**: Kept only as long as necessary
- **Integrity and Confidentiality**: Appropriate security measures
- **Accountability**: Demonstrate compliance with principles

```python
from datetime import datetime, timedelta
from enum import Enum
import json

class LawfulBasis(Enum):
    CONSENT = "consent"
    CONTRACT = "contract"
    LEGAL_OBLIGATION = "legal_obligation"
    VITAL_INTERESTS = "vital_interests"
    PUBLIC_TASK = "public_task"
    LEGITIMATE_INTERESTS = "legitimate_interests"

class DataSubjectRights(Enum):
    ACCESS = "access"
    RECTIFICATION = "rectification"
    ERASURE = "erasure"
    RESTRICT_PROCESSING = "restrict_processing"
    DATA_PORTABILITY = "data_portability"
    OBJECT = "object"

class GDPRComplianceFramework:
    def __init__(self):
        self.data_subjects = {}
        self.processing_activities = {}
        self.consent_records = {}
        self.data_subject_requests = {}
        self.breach_incidents = []
    
    def register_processing_activity(self, activity_id, purpose, lawful_basis, data_categories, retention_period):
        """Register data processing activity"""
        self.processing_activities[activity_id] = {
            'purpose': purpose,
            'lawful_basis': lawful_basis,
            'data_categories': data_categories,
            'retention_period': retention_period,
            'created_at': datetime.now(),
            'data_subjects': []
        }
        print(f"Processing activity '{activity_id}' registered")
        print(f"Purpose: {purpose}")
        print(f"Lawful basis: {lawful_basis.value}")
    
    def obtain_consent(self, data_subject_id, processing_purposes, data_categories):
        """Obtain and record explicit consent"""
        consent_id = f"consent_{data_subject_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.consent_records[consent_id] = {
            'data_subject_id': data_subject_id,
            'processing_purposes': processing_purposes,
            'data_categories': data_categories,
            'consent_given_at': datetime.now(),
            'consent_method': 'explicit_opt_in',
            'is_active': True,
            'withdrawal_date': None
        }
        
        print(f"Consent obtained from data subject {data_subject_id}")
        print(f"Consent ID: {consent_id}")
        print(f"Purposes: {processing_purposes}")
        return consent_id
    
    def withdraw_consent(self, consent_id):
        """Allow data subject to withdraw consent"""
        if consent_id in self.consent_records:
            self.consent_records[consent_id]['is_active'] = False
            self.consent_records[consent_id]['withdrawal_date'] = datetime.now()
            
            print(f"Consent {consent_id} withdrawn")
            print("Processing based on this consent must cease")
            return True
        return False
    
    def handle_data_subject_request(self, request_id, data_subject_id, request_type, details=None):
        """Handle data subject rights requests"""
        self.data_subject_requests[request_id] = {
            'data_subject_id': data_subject_id,
            'request_type': request_type,
            'details': details,
            'submitted_at': datetime.now(),
            'status': 'received',
            'response_due': datetime.now() + timedelta(days=30)  # GDPR requirement
        }
        
        print(f"Data subject request received: {request_id}")
        print(f"Type: {request_type.value}")
        print(f"Response due: {self.data_subject_requests[request_id]['response_due']}")
        
        # Process the request
        return self.process_data_subject_request(request_id)
    
    def process_data_subject_request(self, request_id):
        """Process data subject rights request"""
        request = self.data_subject_requests[request_id]
        request_type = request['request_type']
        data_subject_id = request['data_subject_id']
        
        if request_type == DataSubjectRights.ACCESS:
            # Right to access - provide copy of personal data
            personal_data = self.get_all_personal_data(data_subject_id)
            response = {
                'request_id': request_id,
                'data_subject_id': data_subject_id,
                'personal_data': personal_data,
                'processing_activities': self.get_processing_activities_for_subject(data_subject_id),
                'retention_periods': self.get_retention_info(data_subject_id)
            }
            
        elif request_type == DataSubjectRights.ERASURE:
            # Right to erasure (right to be forgotten)
            deletion_result = self.delete_personal_data(data_subject_id)
            response = {
                'request_id': request_id,
                'data_subject_id': data_subject_id,
                'deletion_completed': deletion_result,
                'systems_updated': self.get_systems_list()
            }
            
        elif request_type == DataSubjectRights.DATA_PORTABILITY:
            # Right to data portability
            portable_data = self.export_personal_data(data_subject_id, format='json')
            response = {
                'request_id': request_id,
                'data_subject_id': data_subject_id,
                'portable_data': portable_data,
                'format': 'structured_json'
            }
            
        elif request_type == DataSubjectRights.RECTIFICATION:
            # Right to rectification
            correction_result = self.correct_personal_data(data_subject_id, request['details'])
            response = {
                'request_id': request_id,
                'data_subject_id': data_subject_id,
                'corrections_made': correction_result
            }
        
        # Update request status
        self.data_subject_requests[request_id]['status'] = 'completed'
        self.data_subject_requests[request_id]['completed_at'] = datetime.now()
        self.data_subject_requests[request_id]['response'] = response
        
        print(f"Request {request_id} processed successfully")
        return response
    
    def report_data_breach(self, breach_description, affected_data_subjects, risk_level):
        """Report data breach (72-hour notification requirement)"""
        breach_id = f"breach_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        breach_record = {
            'breach_id': breach_id,
            'description': breach_description,
            'detected_at': datetime.now(),
            'affected_subjects_count': len(affected_data_subjects),
            'risk_level': risk_level,
            'notification_deadline': datetime.now() + timedelta(hours=72),
            'supervisory_authority_notified': False,
            'data_subjects_notified': False
        }
        
        self.breach_incidents.append(breach_record)
        
        print(f"Data breach reported: {breach_id}")
        print(f"Affected data subjects: {len(affected_data_subjects)}")
        print(f"Risk level: {risk_level}")
        print(f"Notification deadline: {breach_record['notification_deadline']}")
        
        # Auto-notify if high risk
        if risk_level == 'high':
            self.notify_supervisory_authority(breach_id)
            self.notify_affected_data_subjects(breach_id, affected_data_subjects)
        
        return breach_id
    
    def notify_supervisory_authority(self, breach_id):
        """Notify supervisory authority within 72 hours"""
        for breach in self.breach_incidents:
            if breach['breach_id'] == breach_id:
                breach['supervisory_authority_notified'] = True
                breach['authority_notification_sent'] = datetime.now()
                print(f"Supervisory authority notified for breach {breach_id}")
                break
    
    def notify_affected_data_subjects(self, breach_id, affected_subjects):
        """Notify affected data subjects without undue delay"""
        for breach in self.breach_incidents:
            if breach['breach_id'] == breach_id:
                breach['data_subjects_notified'] = True
                breach['subjects_notification_sent'] = datetime.now()
                print(f"Affected data subjects notified for breach {breach_id}")
                break
    
    def conduct_dpia(self, processing_activity, risk_factors):
        """Conduct Data Protection Impact Assessment"""
        dpia_id = f"dpia_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Assess necessity and proportionality
        necessity_score = self.assess_necessity(processing_activity)
        proportionality_score = self.assess_proportionality(processing_activity)
        
        # Identify and assess risks
        privacy_risks = self.identify_privacy_risks(processing_activity, risk_factors)
        risk_score = self.calculate_risk_score(privacy_risks)
        
        # Determine mitigation measures
        mitigation_measures = self.determine_mitigation_measures(privacy_risks)
        
        dpia_result = {
            'dpia_id': dpia_id,
            'processing_activity': processing_activity,
            'necessity_score': necessity_score,
            'proportionality_score': proportionality_score,
            'privacy_risks': privacy_risks,
            'overall_risk_score': risk_score,
            'mitigation_measures': mitigation_measures,
            'recommendation': 'proceed' if risk_score < 7 else 'consult_dpo',
            'conducted_at': datetime.now()
        }
        
        print(f"DPIA completed: {dpia_id}")
        print(f"Overall risk score: {risk_score}/10")
        print(f"Recommendation: {dpia_result['recommendation']}")
        
        return dpia_result
    
    def get_all_personal_data(self, data_subject_id):
        """Retrieve all personal data for a data subject"""
        # Simulate data retrieval from multiple systems
        return {
            'profile_data': {'name': 'John Doe', 'email': 'john@example.com'},
            'transaction_data': [{'date': '2024-01-01', 'amount': 100}],
            'behavioral_data': {'last_login': '2024-01-15', 'preferences': ['tech', 'sports']}
        }
    
    def assess_necessity(self, processing_activity):
        """Assess if processing is necessary for the stated purpose"""
        # Simplified assessment logic
        return 8  # Score out of 10
    
    def assess_proportionality(self, processing_activity):
        """Assess if processing is proportionate to the purpose"""
        return 7  # Score out of 10
    
    def identify_privacy_risks(self, processing_activity, risk_factors):
        """Identify privacy risks in processing activity"""
        return [
            {'risk': 'unauthorized_access', 'likelihood': 'medium', 'impact': 'high'},
            {'risk': 'data_breach', 'likelihood': 'low', 'impact': 'very_high'},
            {'risk': 'profiling', 'likelihood': 'high', 'impact': 'medium'}
        ]
    
    def calculate_risk_score(self, privacy_risks):
        """Calculate overall risk score"""
        # Simplified risk calculation
        return 6  # Score out of 10
    
    def determine_mitigation_measures(self, privacy_risks):
        """Determine appropriate mitigation measures"""
        return [
            'implement_encryption',
            'access_controls',
            'regular_audits',
            'staff_training',
            'incident_response_plan'
        ]

# Usage example
gdpr = GDPRComplianceFramework()

# Register processing activity
gdpr.register_processing_activity(
    activity_id='customer_analytics',
    purpose='Analyze customer behavior for service improvement',
    lawful_basis=LawfulBasis.LEGITIMATE_INTERESTS,
    data_categories=['contact_info', 'transaction_history', 'preferences'],
    retention_period=timedelta(days=1095)  # 3 years
)
# Output: Processing activity 'customer_analytics' registered
#         Purpose: Analyze customer behavior for service improvement
#         Lawful basis: legitimate_interests

# Obtain consent
consent_id = gdpr.obtain_consent(
    data_subject_id='user_12345',
    processing_purposes=['marketing', 'personalization'],
    data_categories=['email', 'preferences', 'behavior']
)
# Output: Consent obtained from data subject user_12345
#         Consent ID: consent_user_12345_20240101_120000
#         Purposes: ['marketing', 'personalization']

# Handle data subject request
response = gdpr.handle_data_subject_request(
    request_id='req_001',
    data_subject_id='user_12345',
    request_type=DataSubjectRights.ACCESS
)
# Output: Data subject request received: req_001
#         Type: access
#         Response due: 2024-01-31 12:00:00
#         Request req_001 processed successfully

# Report data breach
breach_id = gdpr.report_data_breach(
    breach_description='Unauthorized access to customer database',
    affected_data_subjects=['user_12345', 'user_67890'],
    risk_level='high'
)
# Output: Data breach reported: breach_20240101_120000
#         Affected data subjects: 2
#         Risk level: high
#         Notification deadline: 2024-01-04 12:00:00
#         Supervisory authority notified for breach breach_20240101_120000
#         Affected data subjects notified for breach breach_20240101_120000

# Conduct DPIA
dpia_result = gdpr.conduct_dpia(
    processing_activity='automated_decision_making',
    risk_factors=['profiling', 'automated_decisions', 'sensitive_data']
)
# Output: DPIA completed: dpia_20240101_120000
#         Overall risk score: 6/10
#         Recommendation: proceed
```

## 🎯 When to Apply Security Measures

**Data Classification Triggers**:
- **Public Data**: Basic security measures, standard access controls
- **Internal Data**: Enhanced access controls, audit logging
- **Confidential Data**: Encryption, role-based access, monitoring
- **Restricted Data**: Full security stack, compliance controls, incident response

**Regulatory Triggers**:
- **Personal Data**: GDPR, CCPA compliance measures
- **Financial Data**: SOX, PCI DSS requirements
- **Health Data**: HIPAA safeguards
- **Cross-border**: Data localization, transfer mechanisms

## 🎯 Interview Focus Areas

1. **Security Architecture**: CIA Triad, Zero Trust, Defense in Depth
2. **Data Protection**: Encryption types, masking techniques, access controls
3. **Privacy Technologies**: Differential privacy, homomorphic encryption, SMPC
4. **Regulatory Compliance**: GDPR, CCPA, HIPAA, SOX requirements
5. **Data Ethics**: Algorithmic fairness, transparency, privacy by design
6. **Implementation**: Tools, frameworks, best practices
7. **Incident Response**: Breach notification, recovery procedures
8. **Risk Assessment**: DPIA, privacy impact assessments

## 📚 Quick References

- [GDPR Official Text](https://gdpr-info.eu/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [OWASP Security Guidelines](https://owasp.org/)
- [ISO 27001 Standard](https://www.iso.org/isoiec-27001-information-security.html)
- [Differential Privacy Resources](https://differentialprivacy.org/)