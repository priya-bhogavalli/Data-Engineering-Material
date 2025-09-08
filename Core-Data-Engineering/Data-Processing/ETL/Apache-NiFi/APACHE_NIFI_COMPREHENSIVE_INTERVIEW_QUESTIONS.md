# Apache NiFi - Comprehensive Interview Questions

## 📋 Table of Contents

1. [Core Concepts](#core-concepts)
2. [Flow Design & Architecture](#flow-design--architecture)
3. [Processors & Components](#processors--components)
4. [Data Routing & Transformation](#data-routing--transformation)
5. [Security & Access Control](#security--access-control)
6. [Monitoring & Management](#monitoring--management)
7. [Clustering & Scalability](#clustering--scalability)
8. [Best Practices](#best-practices)

---

## Core Concepts

### 1. What is Apache NiFi and what problems does it solve in data integration?

**Answer:**
Apache NiFi is a powerful, easy-to-use data integration platform that automates the flow of data between systems with a web-based user interface for designing, controlling, and monitoring data flows.

**Key Problems Solved:**
- **Data Movement**: Reliable data transfer between heterogeneous systems
- **Data Transformation**: Real-time data processing and enrichment
- **Data Routing**: Intelligent routing based on content and metadata
- **Data Lineage**: Complete tracking of data provenance
- **System Integration**: Connecting disparate systems and protocols

```python
# NiFi Flow Example (conceptual representation)
class NiFiFlowExample:
    def __init__(self):
        self.flow_components = {
            'processors': [],
            'connections': [],
            'process_groups': []
        }
    
    def create_basic_etl_flow(self):
        """Create a basic ETL flow in NiFi."""
        
        # Source: Get data from database
        get_database_processor = {
            'type': 'ExecuteSQL',
            'properties': {
                'Database Connection Pooling Service': 'DBCPConnectionPool',
                'SQL select query': 'SELECT * FROM customers WHERE updated_at > ?',
                'SQL Arguments': '${last_sync_time}'
            },
            'scheduling': {
                'run_schedule': '0 */5 * * * ?',  # Every 5 minutes
                'concurrent_tasks': 1
            }
        }
        
        # Transform: Convert to JSON
        convert_to_json = {
            'type': 'ConvertAvroToJSON',
            'properties': {
                'JSON container options': 'array'
            }
        }
        
        # Transform: Enrich data
        enrich_data = {
            'type': 'ExecuteScript',
            'properties': {
                'Script Engine': 'python',
                'Script Body': '''
                    import json
                    flowFile = session.get()
                    if flowFile is not None:
                        content = session.read(flowFile).decode('utf-8')
                        data = json.loads(content)
                        
                        # Enrich with additional fields
                        for record in data:
                            record['processed_timestamp'] = time.time()
                            record['source_system'] = 'customer_db'
                        
                        enriched_content = json.dumps(data)
                        flowFile = session.write(flowFile, enriched_content.encode('utf-8'))
                        session.transfer(flowFile, REL_SUCCESS)
                '''
            }
        }
        
        # Destination: Send to Kafka
        publish_to_kafka = {
            'type': 'PublishKafka_2_6',
            'properties': {
                'Kafka Brokers': 'localhost:9092',
                'Topic Name': 'customer-updates',
                'Message Key Field': 'customer_id',
                'Delivery Guarantee': 'Best Effort'
            }
        }
        
        # Define flow connections
        flow_connections = [
            {'from': 'ExecuteSQL', 'to': 'ConvertAvroToJSON', 'relationship': 'success'},
            {'from': 'ConvertAvroToJSON', 'to': 'ExecuteScript', 'relationship': 'success'},
            {'from': 'ExecuteScript', 'to': 'PublishKafka_2_6', 'relationship': 'success'}
        ]
        
        return {
            'processors': [get_database_processor, convert_to_json, enrich_data, publish_to_kafka],
            'connections': flow_connections
        }
```

### 2. Explain NiFi's fundamental concepts: FlowFiles, Processors, and Connections.

**Answer:**
**Core NiFi Concepts:**

| Component | Description | Purpose |
|-----------|-------------|---------|
| **FlowFile** | Data packet with attributes and content | Represents data moving through the system |
| **Processor** | Component that performs work on FlowFiles | Executes data processing logic |
| **Connection** | Queue between processors | Controls data flow and backpressure |
| **Process Group** | Container for processors and connections | Organizes and manages flow components |

```python
class NiFiCoreComponents:
    def flowfile_structure_example(self):
        """Demonstrate FlowFile structure and attributes."""
        
        flowfile_example = {
            'attributes': {
                # Standard attributes
                'filename': 'customer_data_20240115.json',
                'path': '/input/customers/',
                'uuid': '12345678-1234-1234-1234-123456789abc',
                'entryDate': '2024-01-15T10:30:00.000Z',
                'lineageStartDate': '2024-01-15T10:30:00.000Z',
                'fileSize': '1024',
                
                # Custom attributes
                'source.system': 'CRM',
                'data.type': 'customer',
                'processing.priority': 'high',
                'schema.version': '1.2'
            },
            'content': {
                'type': 'JSON',
                'data': '''[
                    {"id": 1, "name": "John Doe", "email": "john@example.com"},
                    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
                ]'''
            }
        }
        
        return flowfile_example
    
    def processor_configuration_example(self):
        """Example processor configurations for common use cases."""
        
        processors = {
            # File ingestion processor
            'GetFile': {
                'properties': {
                    'Input Directory': '/data/input',
                    'File Filter': '.*\\.json$',
                    'Keep Source File': 'false',
                    'Minimum File Age': '5 sec',
                    'Polling Interval': '10 sec',
                    'Batch Size': '50'
                },
                'relationships': ['success', 'failure']
            },
            
            # Data transformation processor
            'JoltTransformJSON': {
                'properties': {
                    'Jolt Specification': '''{
                        "operation": "shift",
                        "spec": {
                            "customer_id": "id",
                            "customer_name": "name",
                            "email_address": "email",
                            "created_date": "createdAt"
                        }
                    }'''
                },
                'relationships': ['success', 'failure']
            },
            
            # Routing processor
            'RouteOnAttribute': {
                'properties': {
                    'high_priority': "${processing.priority:equals('high')}",
                    'medium_priority': "${processing.priority:equals('medium')}",
                    'low_priority': "${processing.priority:equals('low')}"
                },
                'relationships': ['high_priority', 'medium_priority', 'low_priority', 'unmatched']
            }
        }
        
        return processors
    
    def connection_configuration_example(self):
        """Example connection configurations with backpressure settings."""
        
        connections = {
            'high_throughput_connection': {
                'source': 'GetFile',
                'destination': 'JoltTransformJSON',
                'relationships': ['success'],
                'settings': {
                    'FlowFile Expiration': '1 hour',
                    'Back Pressure Object Threshold': '10000',
                    'Back Pressure Data Size Threshold': '1 GB',
                    'Prioritizers': ['FirstInFirstOutPrioritizer']
                }
            },
            
            'priority_connection': {
                'source': 'RouteOnAttribute',
                'destination': 'PutKafka',
                'relationships': ['high_priority'],
                'settings': {
                    'FlowFile Expiration': '30 min',
                    'Back Pressure Object Threshold': '1000',
                    'Back Pressure Data Size Threshold': '100 MB',
                    'Prioritizers': ['PriorityAttributePrioritizer']
                }
            }
        }
        
        return connections
```

## Data Routing & Transformation

### 3. How do you implement complex data routing and transformation logic in NiFi?

**Answer:**
NiFi provides multiple approaches for data routing and transformation using processors, expression language, and custom scripts.

```python
class NiFiDataRouting:
    def attribute_based_routing(self):
        """Implement complex routing based on FlowFile attributes."""
        
        routing_logic = {
            'RouteOnAttribute': {
                'properties': {
                    # Route based on data type
                    'customer_data': "${data.type:equals('customer')}",
                    'order_data': "${data.type:equals('order')}",
                    'product_data': "${data.type:equals('product')}",
                    
                    # Route based on file size
                    'large_file': "${fileSize:toNumber():gt(1000000)}",  # > 1MB
                    'small_file': "${fileSize:toNumber():le(1000000)}",  # <= 1MB
                    
                    # Route based on content
                    'json_content': "${mime.type:equals('application/json')}",
                    'csv_content': "${mime.type:equals('text/csv')}",
                    
                    # Route based on time
                    'business_hours': "${now():format('HH'):toNumber():ge(9):and(${now():format('HH'):toNumber():lt(17)})}",
                    'after_hours': "${now():format('HH'):toNumber():lt(9):or(${now():format('HH'):toNumber():ge(17)})}"
                }
            }
        }
        
        return routing_logic
    
    def content_based_routing(self):
        """Route based on FlowFile content using QueryRecord."""
        
        content_routing = {
            'QueryRecord': {
                'properties': {
                    'Record Reader': 'JsonTreeReader',
                    'Record Writer': 'JsonRecordSetWriter',
                    
                    # Define routing queries
                    'high_value_customers': '''
                        SELECT * FROM FLOWFILE 
                        WHERE total_purchases > 10000
                    ''',
                    
                    'new_customers': '''
                        SELECT * FROM FLOWFILE 
                        WHERE registration_date >= CURRENT_DATE - INTERVAL '30' DAY
                    ''',
                    
                    'inactive_customers': '''
                        SELECT * FROM FLOWFILE 
                        WHERE last_purchase_date < CURRENT_DATE - INTERVAL '90' DAY
                    '''
                }
            }
        }
        
        return content_routing
    
    def data_transformation_pipeline(self):
        """Complex data transformation pipeline."""
        
        transformation_flow = {
            # Step 1: Parse and validate JSON
            'ValidateRecord': {
                'properties': {
                    'Record Reader': 'JsonTreeReader',
                    'Schema Access Strategy': 'Use Schema Text Property',
                    'Schema Text': '''{
                        "type": "record",
                        "name": "Customer",
                        "fields": [
                            {"name": "id", "type": "int"},
                            {"name": "name", "type": "string"},
                            {"name": "email", "type": "string"},
                            {"name": "registration_date", "type": "string"}
                        ]
                    }'''
                }
            },
            
            # Step 2: Transform data structure
            'JoltTransformJSON': {
                'properties': {
                    'Jolt Specification': '''{
                        "operation": "shift",
                        "spec": {
                            "id": "customer.customerId",
                            "name": "customer.fullName",
                            "email": "contact.emailAddress",
                            "registration_date": "metadata.registeredAt",
                            "*": "customer.&"
                        }
                    }'''
                }
            },
            
            # Step 3: Enrich with external data
            'InvokeHTTP': {
                'properties': {
                    'HTTP Method': 'POST',
                    'Remote URL': 'https://api.enrichment.com/customer/enrich',
                    'Content-Type': 'application/json',
                    'Request Body': '${content}',
                    'Connection Timeout': '30 sec',
                    'Read Timeout': '30 sec'
                }
            },
            
            # Step 4: Apply business rules
            'ExecuteScript': {
                'properties': {
                    'Script Engine': 'python',
                    'Script Body': '''
import json
from datetime import datetime, timedelta

flowFile = session.get()
if flowFile is not None:
    content = session.read(flowFile).decode('utf-8')
    customer_data = json.loads(content)
    
    # Apply business rules
    customer = customer_data['customer']
    
    # Calculate customer tier
    total_purchases = customer.get('totalPurchases', 0)
    if total_purchases > 10000:
        customer['tier'] = 'GOLD'
    elif total_purchases > 5000:
        customer['tier'] = 'SILVER'
    else:
        customer['tier'] = 'BRONZE'
    
    # Calculate days since registration
    reg_date = datetime.strptime(customer['registeredAt'], '%Y-%m-%d')
    days_since_reg = (datetime.now() - reg_date).days
    customer['daysSinceRegistration'] = days_since_reg
    
    # Add processing metadata
    customer_data['metadata']['processedAt'] = datetime.now().isoformat()
    customer_data['metadata']['processingVersion'] = '1.0'
    
    # Write back to FlowFile
    updated_content = json.dumps(customer_data, indent=2)
    flowFile = session.write(flowFile, updated_content.encode('utf-8'))
    
    # Add custom attributes
    flowFile = session.putAttribute(flowFile, 'customer.tier', customer['tier'])
    flowFile = session.putAttribute(flowFile, 'processing.completed', 'true')
    
    session.transfer(flowFile, REL_SUCCESS)
                    '''
                }
            }
        }
        
        return transformation_flow
```

## Security & Access Control

### 4. How do you implement security and access control in Apache NiFi?

**Answer:**
NiFi provides comprehensive security features including authentication, authorization, and data encryption.

```python
class NiFiSecurity:
    def authentication_configuration(self):
        """Configure various authentication methods."""
        
        auth_configs = {
            # LDAP Authentication
            'ldap_auth': {
                'nifi.properties': {
                    'nifi.security.user.login.identity.provider': 'ldap-provider',
                    'nifi.security.user.authorizer': 'managed-authorizer'
                },
                'login-identity-providers.xml': '''
                    <provider>
                        <identifier>ldap-provider</identifier>
                        <class>org.apache.nifi.ldap.LdapProvider</class>
                        <property name="Authentication Strategy">SIMPLE</property>
                        <property name="Manager DN">cn=admin,dc=example,dc=com</property>
                        <property name="Manager Password">password</property>
                        <property name="TLS - Keystore"></property>
                        <property name="TLS - Keystore Password"></property>
                        <property name="TLS - Keystore Type"></property>
                        <property name="TLS - Truststore"></property>
                        <property name="TLS - Truststore Password"></property>
                        <property name="TLS - Truststore Type"></property>
                        <property name="TLS - Client Auth"></property>
                        <property name="TLS - Protocol"></property>
                        <property name="TLS - Shutdown Gracefully"></property>
                        <property name="Referral Strategy">FOLLOW</property>
                        <property name="Connect Timeout">10 secs</property>
                        <property name="Read Timeout">10 secs</property>
                        <property name="Url">ldap://localhost:389</property>
                        <property name="User Search Base">ou=users,dc=example,dc=com</property>
                        <property name="User Search Filter">cn={0}</property>
                        <property name="Identity Strategy">USE_DN</property>
                        <property name="Authentication Expiration">12 hours</property>
                    </provider>
                '''
            },
            
            # Certificate-based Authentication
            'certificate_auth': {
                'nifi.properties': {
                    'nifi.security.keystore': '/path/to/keystore.jks',
                    'nifi.security.keystoreType': 'JKS',
                    'nifi.security.keystorePasswd': 'keystorePassword',
                    'nifi.security.keyPasswd': 'keyPassword',
                    'nifi.security.truststore': '/path/to/truststore.jks',
                    'nifi.security.truststoreType': 'JKS',
                    'nifi.security.truststorePasswd': 'truststorePassword',
                    'nifi.security.needClientAuth': 'true'
                }
            }
        }
        
        return auth_configs
    
    def authorization_policies(self):
        """Define authorization policies for different user roles."""
        
        authorization_config = {
            'authorizers.xml': '''
                <authorizers>
                    <userGroupProvider>
                        <identifier>file-user-group-provider</identifier>
                        <class>org.apache.nifi.authorization.FileUserGroupProvider</class>
                        <property name="Users File">./conf/users.xml</property>
                        <property name="Legacy Authorized Users File"></property>
                        <property name="Initial User Identity 1">CN=admin, OU=NiFi</property>
                        <property name="Initial User Identity 2">CN=dataengineer, OU=NiFi</property>
                    </userGroupProvider>
                    
                    <accessPolicyProvider>
                        <identifier>file-access-policy-provider</identifier>
                        <class>org.apache.nifi.authorization.FileAccessPolicyProvider</class>
                        <property name="User Group Provider">file-user-group-provider</property>
                        <property name="Authorizations File">./conf/authorizations.xml</property>
                        <property name="Initial Admin Identity">CN=admin, OU=NiFi</property>
                        <property name="Legacy Authorized Users File"></property>
                        <property name="Node Identity 1">CN=node1, OU=NiFi</property>
                        <property name="Node Identity 2">CN=node2, OU=NiFi</property>
                    </accessPolicyProvider>
                    
                    <authorizer>
                        <identifier>managed-authorizer</identifier>
                        <class>org.apache.nifi.authorization.StandardManagedAuthorizer</class>
                        <property name="Access Policy Provider">file-access-policy-provider</property>
                    </authorizer>
                </authorizers>
            '''
        }
        
        # Role-based access policies
        access_policies = {
            'admin_policies': [
                'view the user interface',
                'access the controller',
                'query provenance',
                'access restricted components',
                'access all policies',
                'access users/user groups',
                'retrieve site-to-site details',
                'view system diagnostics',
                'proxy user requests'
            ],
            
            'data_engineer_policies': [
                'view the user interface',
                'access the controller',
                'query provenance',
                'access restricted components',
                'retrieve site-to-site details'
            ],
            
            'read_only_policies': [
                'view the user interface',
                'view system diagnostics'
            ]
        }
        
        return authorization_config, access_policies
    
    def data_encryption_configuration(self):
        """Configure data encryption for sensitive data processing."""
        
        encryption_config = {
            # Sensitive Properties encryption
            'nifi.properties': {
                'nifi.sensitive.props.key': 'encryption_key_here',
                'nifi.sensitive.props.algorithm': 'PBEWITHMD5ANDDES',
                'nifi.sensitive.props.provider': 'BC'
            },
            
            # Encrypt/Decrypt processors configuration
            'EncryptContent': {
                'properties': {
                    'Mode': 'Encrypt',
                    'Key Derivation Function': 'PBKDF2',
                    'Encryption Algorithm': 'AES/CBC/PKCS7Padding',
                    'Password': '${encryption.password}',  # Reference to sensitive property
                    'Raw Key Encoding': 'HEX'
                }
            },
            
            'DecryptContent': {
                'properties': {
                    'Mode': 'Decrypt',
                    'Key Derivation Function': 'PBKDF2',
                    'Encryption Algorithm': 'AES/CBC/PKCS7Padding',
                    'Password': '${encryption.password}',
                    'Raw Key Encoding': 'HEX'
                }
            }
        }
        
        return encryption_config
    
    def secure_data_flow_example(self):
        """Example of a secure data processing flow."""
        
        secure_flow = {
            # Step 1: Secure data ingestion
            'GetSFTP': {
                'properties': {
                    'Hostname': 'secure-ftp.company.com',
                    'Port': '22',
                    'Username': '${sftp.username}',  # Sensitive property
                    'Password': '${sftp.password}',  # Sensitive property
                    'Remote Path': '/secure/data/',
                    'Private Key Path': '/path/to/private/key',
                    'Private Key Passphrase': '${key.passphrase}',
                    'Host Key File': '/path/to/known_hosts',
                    'Use Compression': 'true'
                }
            },
            
            # Step 2: Decrypt incoming data
            'DecryptContent': {
                'properties': {
                    'Mode': 'Decrypt',
                    'Encryption Algorithm': 'AES/GCM/NoPadding',
                    'Password': '${data.encryption.key}'
                }
            },
            
            # Step 3: Process sensitive data with restricted access
            'ExecuteScript': {
                'properties': {
                    'Script Engine': 'python',
                    'Script Body': '''
# This processor requires "access restricted components" permission
import json
import hashlib

flowFile = session.get()
if flowFile is not None:
    content = session.read(flowFile).decode('utf-8')
    data = json.loads(content)
    
    # Anonymize PII data
    for record in data:
        if 'ssn' in record:
            # Hash SSN for privacy
            record['ssn_hash'] = hashlib.sha256(record['ssn'].encode()).hexdigest()
            del record['ssn']
        
        if 'email' in record:
            # Mask email domain
            email_parts = record['email'].split('@')
            record['email'] = f"{email_parts[0]}@***masked***"
    
    processed_content = json.dumps(data)
    flowFile = session.write(flowFile, processed_content.encode('utf-8'))
    session.transfer(flowFile, REL_SUCCESS)
                    '''
                }
            },
            
            # Step 4: Encrypt before sending to destination
            'EncryptContent': {
                'properties': {
                    'Mode': 'Encrypt',
                    'Encryption Algorithm': 'AES/GCM/NoPadding',
                    'Password': '${destination.encryption.key}'
                }
            },
            
            # Step 5: Secure transmission
            'PutSFTP': {
                'properties': {
                    'Hostname': 'destination-server.com',
                    'Username': '${dest.username}',
                    'Password': '${dest.password}',
                    'Remote Path': '/secure/processed/',
                    'Create Directory': 'true',
                    'Use Compression': 'true'
                }
            }
        }
        
        return secure_flow
```

This comprehensive Apache NiFi interview questions file covers essential concepts for reliable data integration and processing that data engineers need to understand.