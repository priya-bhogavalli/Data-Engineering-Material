# Data Security, Ethics, and Compliance - Interview Questions

## 📋 Table of Contents
1. [Data Security](#-data-security)
2. [Data Privacy & Protection](#-data-privacy--protection)
3. [Regulatory Compliance](#-regulatory-compliance)
4. [Data Ethics](#-data-ethics)
5. [Security Architecture](#-security-architecture)
6. [Incident Response](#-incident-response)
7. [Scenario-Based Questions](#-scenario-based-questions)

---

## 🔒 Data Security

### Q1: What are the key principles of data security in data engineering?
**Answer:**
The **CIA Triad** forms the foundation:

**Confidentiality:**
- Data encryption (at rest and in transit)
- Access controls and authentication
- Data masking and tokenization
- Network security (VPNs, firewalls)

**Integrity:**
- Data validation and checksums
- Audit trails and logging
- Version control for data
- Digital signatures

**Availability:**
- Redundancy and backup strategies
- Disaster recovery planning
- Load balancing and failover
- Monitoring and alerting

### Q2: How do you implement encryption in data pipelines?
**Answer:**

**Encryption at Rest:**
```python
import boto3

s3_client = boto3.client('s3')
s3_client.put_object(
    Bucket='my-bucket',
    Key='sensitive-data.parquet',
    Body=data,
    ServerSideEncryption='AES256'
)
```

**Encryption in Transit:**
```python
import requests
response = requests.get('https://api.example.com/data', verify=True)

import psycopg2
conn = psycopg2.connect(
    host="localhost",
    database="mydb",
    user="user",
    password="password",
    sslmode="require"
)
```

### Q3: What is data masking and when should you use it?
**Answer:**

**Static Data Masking:**
```sql
UPDATE customers 
SET email = CONCAT('user', id, '@example.com'),
    phone = '555-0000'
WHERE environment = 'test';
```

**Dynamic Data Masking:**
```python
def mask_pii(data, user_role):
    if user_role != 'admin':
        data['ssn'] = 'XXX-XX-' + data['ssn'][-4:]
        data['email'] = data['email'][:3] + '***@' + data['email'].split('@')[1]
    return data
```

**Use Cases:**
- Development and testing environments
- Analytics on non-production data
- Third-party data sharing
- Compliance with privacy regulations

### Q4: How do you implement access controls in data systems?
**Answer:**

**Role-Based Access Control (RBAC):**
```sql
CREATE ROLE data_analyst;
CREATE ROLE data_engineer;

GRANT SELECT ON sales_data TO data_analyst;
GRANT SELECT, INSERT, UPDATE ON staging_tables TO data_engineer;

GRANT data_analyst TO john_doe;
```

**AWS IAM Example:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:PutObject"],
      "Resource": "arn:aws:s3:::data-lake/department/${aws:username}/*"
    }
  ]
}
```

---

## 🛡️ Data Privacy & Protection

### Q5: What is PII and how do you handle it in data pipelines?
**Answer:**

**Types of PII:**
- **Direct Identifiers:** Full name, SSN, email addresses
- **Quasi-Identifiers:** ZIP code, birth date, gender

**Handling Strategies:**
```python
import hashlib
import uuid

def anonymize_pii(data):
    if 'ssn' in data:
        data['ssn_hash'] = hashlib.sha256(data['ssn'].encode()).hexdigest()
        del data['ssn']
    
    if 'birth_date' in data:
        data['birth_year'] = data['birth_date'].year
        del data['birth_date']
    
    data['anonymous_id'] = str(uuid.uuid4())
    return data
```

### Q6: Explain differential privacy and its implementation.
**Answer:**

**Mathematical Definition:**
```
ε-differential privacy: For datasets D1, D2 differing by one record:
Pr[M(D1) ∈ S] ≤ e^ε × Pr[M(D2) ∈ S]
```

**Implementation:**
```python
import numpy as np

def laplace_mechanism(query_result, sensitivity, epsilon):
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale)
    return query_result + noise

def private_count(data, condition, epsilon=1.0):
    true_count = len(data[condition])
    return laplace_mechanism(true_count, sensitivity=1, epsilon=epsilon)
```

### Q7: How do you implement data retention and deletion policies?
**Answer:**

```python
from datetime import datetime, timedelta
import boto3

class DataRetentionManager:
    def __init__(self):
        self.retention_policies = {
            'transaction_data': timedelta(days=2555),  # 7 years
            'user_activity': timedelta(days=365),      # 1 year
            'pii_data': timedelta(days=1095)           # 3 years
        }
    
    def apply_retention_policy(self, bucket, data_type):
        retention_period = self.retention_policies.get(data_type)
        cutoff_date = datetime.now() - retention_period
        
        # Delete expired objects
        s3_client = boto3.client('s3')
        response = s3_client.list_objects_v2(Bucket=bucket, Prefix=f'{data_type}/')
        
        for obj in response.get('Contents', []):
            if obj['LastModified'].replace(tzinfo=None) < cutoff_date:
                s3_client.delete_object(Bucket=bucket, Key=obj['Key'])
```

---

## 📋 Regulatory Compliance

### Q8: How do you ensure GDPR compliance in data pipelines?
**Answer:**

**Key Requirements:**

**1. Lawful Basis for Processing:**
```python
class GDPRProcessor:
    LAWFUL_BASIS = {
        'consent': 'User has given consent',
        'contract': 'Processing necessary for contract',
        'legal_obligation': 'Required by law'
    }
    
    def process_data(self, data, lawful_basis, purpose):
        if lawful_basis not in self.LAWFUL_BASIS:
            raise ValueError("Invalid lawful basis")
        self.log_processing_activity(data, lawful_basis, purpose)
        return self._process(data)
```

**2. Data Subject Rights:**
```python
def handle_data_subject_request(request_type, user_id):
    if request_type == 'access':
        return get_all_user_data(user_id)
    elif request_type == 'erasure':
        return delete_all_user_data(user_id)
    elif request_type == 'portability':
        return export_user_data(user_id, format='json')
```

### Q9: What are the key requirements of CCPA and SOX compliance?
**Answer:**

**CCPA (California Consumer Privacy Act):**
```python
class CCPACompliance:
    def handle_consumer_request(self, request):
        if request.type == 'right_to_know':
            return {
                'categories_collected': self.get_data_categories(),
                'sources': self.get_data_sources(),
                'business_purposes': self.get_business_purposes()
            }
        elif request.type == 'right_to_delete':
            return self.delete_consumer_data(request.consumer_id)
```

**SOX (Sarbanes-Oxley) Compliance:**
```python
class SOXCompliance:
    def financial_data_pipeline(self, data):
        # Section 302: Management certification
        self.certify_data_accuracy(data)
        
        # Section 404: Internal controls
        if not self.validate_internal_controls():
            raise Exception("Internal controls validation failed")
        
        # Audit trail for all changes
        self.create_audit_trail(data, 'financial_processing')
        return self.process_financial_data(data)
```

### Q10: How do you implement data lineage for compliance?
**Answer:**

```python
class DataLineageTracker:
    def __init__(self):
        self.lineage_graph = {}
    
    def track_transformation(self, source, target, transformation, metadata):
        lineage_record = {
            'source': source,
            'target': target,
            'transformation': transformation,
            'timestamp': datetime.utcnow(),
            'user': self.get_current_user(),
            'metadata': metadata
        }
        
        if target not in self.lineage_graph:
            self.lineage_graph[target] = []
        self.lineage_graph[target].append(lineage_record)
    
    def get_data_lineage(self, dataset):
        lineage = []
        self._traverse_lineage(dataset, lineage)
        return lineage
```

---

## ⚖️ Data Ethics

### Q11: What are the key principles of ethical data use?
**Answer:**

**Core Ethical Principles:**

**1. Fairness and Non-Discrimination:**
```python
def check_algorithmic_bias(model, test_data, protected_attributes):
    results = {}
    
    for attribute in protected_attributes:
        groups = test_data.groupby(attribute)
        
        for group_name, group_data in groups:
            predictions = model.predict(group_data)
            results[f'{attribute}_{group_name}'] = {
                'accuracy': accuracy_score(group_data['target'], predictions),
                'precision': precision_score(group_data['target'], predictions)
            }
    
    return analyze_fairness_metrics(results)
```

**2. Transparency and Explainability:**
```python
import shap

def explain_model_decisions(model, data, feature_names):
    explainer = shap.Explainer(model)
    shap_values = explainer(data)
    
    explanations = []
    for i, instance in enumerate(data):
        explanation = {
            'prediction': model.predict([instance])[0],
            'feature_contributions': dict(zip(feature_names, shap_values[i]))
        }
        explanations.append(explanation)
    
    return explanations
```

### Q12: How do you handle algorithmic bias in data pipelines?
**Answer:**

**Bias Detection and Mitigation:**

```python
def analyze_data_representation(dataset, demographic_columns):
    analysis = {}
    
    for column in demographic_columns:
        distribution = dataset[column].value_counts(normalize=True)
        population_dist = get_population_distribution(column)
        
        analysis[column] = {
            'dataset_distribution': distribution.to_dict(),
            'population_distribution': population_dist,
            'representation_ratio': calculate_representation_ratio(
                distribution, population_dist
            )
        }
    
    return analysis

def ensure_fairness_constraints(model, training_data, protected_attribute):
    def demographic_parity_loss(y_true, y_pred, sensitive_attr):
        groups = np.unique(sensitive_attr)
        group_rates = [np.mean(y_pred[sensitive_attr == group]) for group in groups]
        return np.var(group_rates)
    
    def fair_loss(y_true, y_pred, sensitive_attr, lambda_fair=0.1):
        original_loss = log_loss(y_true, y_pred)
        fairness_loss = demographic_parity_loss(y_true, y_pred, sensitive_attr)
        return original_loss + lambda_fair * fairness_loss
    
    return train_with_custom_loss(model, training_data, fair_loss)
```

---

## 🏗️ Security Architecture

### Q13: How do you design a secure data architecture?
**Answer:**

**Layered Security Architecture:**

```python
class SecureDataArchitecture:
    def design_secure_pipeline(self, requirements):

### Q14: How do you handle a data breach incident?
**Answer:**

**Data Breach Response Plan:**

```python
class DataBreachResponseManager:
    def handle_breach_incident(self, incident):
        # Phase 1: Immediate Response (0-1 hour)
        self.immediate_response(incident)
        
        # Phase 2: Assessment and Containment (1-24 hours)
        self.assess_and_contain(incident)
        
        # Phase 3: Investigation and Recovery (1-7 days)
        self.investigate_and_recover(incident)
        
        # Phase 4: Post-Incident Activities (ongoing)
        self.post_incident_activities(incident)
    
    def immediate_response(self, incident):
        # 1. Activate incident response team
        self.activate_response_team(incident.severity)
        
        # 2. Contain the breach
        affected_systems = self.identify_affected_systems(incident)
        for system in affected_systems:
            self.isolate_system(system)
        
        # 3. Preserve evidence
        self.preserve_digital_evidence(affected_systems)
        
        # 4. Initial notification
        self.notify_stakeholders(incident, notification_type='initial')
```

---

## 🎭 Scenario-Based Questions

### Q15: A data scientist requests access to production customer data for model training. How do you handle this request?
**Answer:**

```python
class SecureDataAccessManager:
    def handle_data_access_request(self, request):
        # 1. Validate request
        validation_result = self.validate_request(request)
        if not validation_result.valid:
            return self.deny_request(request, validation_result.reason)
        
        # 2. Risk assessment
        risk_score = self.assess_risk(request)
        
        # 3. Determine appropriate data access method
        if risk_score < 0.3:
            return self.provide_anonymized_data(request)
        elif risk_score < 0.6:
            return self.provide_synthetic_data(request)
        else:
            return self.provide_secure_environment_access(request)
    
    def provide_anonymized_data(self, request):
        original_data = self.fetch_data(request.data_source)
        
        anonymized_data = self.anonymization_pipeline(
            data=original_data,
            techniques=['k_anonymity', 'l_diversity', 'differential_privacy']
        )
        
        secure_location = self.create_secure_transfer_location()
        self.transfer_data(anonymized_data, secure_location)
        
        return {
            'access_granted': True,
            'data_location': secure_location,
            'restrictions': ['no_reidentification', 'no_redistribution']
        }
```

### Q16: Your organization needs to share data with a third-party vendor. What security measures do you implement?
**Answer:**

```python
class ThirdPartyDataSharingManager:
    def establish_secure_data_sharing(self, vendor, data_requirements):
        # 1. Vendor risk assessment
        risk_assessment = self.conduct_vendor_risk_assessment(vendor)
        
        # 2. Data classification and minimization
        classified_data = self.classify_requested_data(data_requirements)
        minimized_data = self.apply_data_minimization(classified_data)
        
        # 3. Technical security controls
        security_controls = {
            'encryption': {
                'method': 'AES-256-GCM',
                'key_management': 'customer_managed_keys'
            },
            'transfer': {
                'method': 'SFTP_with_client_certificates',
                'network': 'dedicated_vpn_tunnel'
            },
            'access': {
                'authentication': 'mutual_tls_certificates',
                'authorization': 'role_based_access_control'
            },
            'monitoring': {
                'access_logging': 'comprehensive_audit_logs',
                'anomaly_detection': 'ml_based_behavior_analysis'
            }
        }
        
        # 4. Data sharing agreement
        dsa = self.create_data_sharing_agreement(vendor, minimized_data, security_controls)
        
        return {
            'risk_assessment': risk_assessment,
            'data_sharing_agreement': dsa,
            'security_controls': security_controls
        }
```

### Q17: How do you ensure data quality while maintaining privacy in a data pipeline?
**Answer:**

```python
class PrivacyPreservingDataQuality:
    def assess_quality_with_privacy(self, data, privacy_budget):
        quality_assessment = {}
        
        # 1. Completeness check with differential privacy
        quality_assessment['completeness'] = self.private_completeness_check(
            data, privacy_budget * 0.25
        )
        
        # 2. Accuracy assessment using secure computation
        quality_assessment['accuracy'] = self.secure_accuracy_assessment(
            data, privacy_budget * 0.25
        )
        
        return quality_assessment
    
    def private_completeness_check(self, data, epsilon):
        missing_counts = {}
        
        for column in data.columns:
            true_missing_count = data[column].isnull().sum()
            
            # Add Laplace noise for differential privacy
            noisy_missing_count = self.laplace_mechanism(
                true_missing_count, sensitivity=1, epsilon=epsilon/len(data.columns)
            )
            
            missing_counts[column] = max(0, noisy_missing_count)
        
        # Calculate completeness scores
        completeness_scores = {}
        for column, missing_count in missing_counts.items():
            completeness_scores[column] = 1 - (missing_count / len(data))
        
        return completeness_scores
    
    def implement_privacy_preserving_data_cleaning(self, data):
        cleaned_data = data.copy()
        
        # Private data imputation
        for column in data.columns:
            if data[column].dtype in ['int64', 'float64']:
                private_mean = self.calculate_private_mean(
                    data[column].dropna(), epsilon=0.1
                )
                cleaned_data[column].fillna(private_mean, inplace=True)
        
        return cleaned_data
```

---

## 📚 Additional Resources

### Key Frameworks and Standards
- **NIST Cybersecurity Framework**
- **ISO 27001/27002**
- **COBIT 2019**
- **FAIR (Factor Analysis of Information Risk)**

### Privacy Engineering Tools
- **Google's Differential Privacy Library**
- **Microsoft's SmartNoise**
- **IBM's Differential Privacy Library**
- **Apache Beam Privacy**

### Compliance Automation
- **AWS Config Rules**
- **Azure Policy**
- **GCP Security Command Center**
- **Terraform Compliance**