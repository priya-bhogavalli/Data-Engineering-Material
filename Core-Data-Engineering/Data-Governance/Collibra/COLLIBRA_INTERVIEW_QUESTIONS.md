# Collibra Data Governance Platform - Comprehensive Interview Questions

## 📋 Table of Contents

1. [Basic Level Questions (1-50)](#basic-level-questions-1-50)
2. [Intermediate Level Questions (51-100)](#intermediate-level-questions-51-100)
3. [Advanced Level Questions (101-150)](#advanced-level-questions-101-150)
4. [Architecture & Performance (151-180)](#architecture--performance-151-180)
5. [Streaming & Real-time Processing (181-200)](#streaming--real-time-processing-181-200)
6. [Production & Operations (201-230)](#production--operations-201-230)
7. [Scenario-Based Questions (231-250)](#scenario-based-questions-231-250)

---

## Basic Level Questions (1-50)

### 1. What is Collibra and what are its core capabilities?

**Answer:** Collibra is a comprehensive data governance platform that helps organizations manage, govern, and derive value from their data assets through unified data cataloging, governance, quality management, and privacy compliance.

#### **Core Capabilities:**
- **Data Catalog**: Centralized repository for all data assets with automated discovery
- **Data Governance**: Policy management, workflows, and stewardship
- **Data Quality**: Profiling, monitoring, and quality rule management
- **Data Privacy**: GDPR/CCPA compliance and privacy management
- **Data Lineage**: End-to-end data flow visualization and impact analysis
- **Business Glossary**: Centralized business terminology management

```python
# Example: Basic Collibra API interaction
import requests
import json

class CollibraBasicClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.headers.update({'Content-Type': 'application/json'})
    
    def get_domains(self):
        """Get all domains in Collibra"""
        endpoint = f"{self.base_url}/rest/2.0/domains"
        response = self.session.get(endpoint)
        return response.json()
    
    def search_assets(self, query):
        """Search for assets by name"""
        endpoint = f"{self.base_url}/rest/2.0/assets"
        params = {'name': query, 'limit': 10}
        response = self.session.get(endpoint, params=params)
        return response.json()

# Usage
client = CollibraBasicClient("https://your-instance.collibra.com", "user", "pass")
domains = client.get_domains()
print(f"Found {len(domains.get('results', []))} domains")
```

### 2. What is the difference between a Data Catalog and a Business Glossary in Collibra?

**Answer:** Data Catalog and Business Glossary serve different but complementary purposes in data governance.

#### **Data Catalog:**
- **Technical Focus**: Contains actual data assets (tables, files, reports)
- **Metadata Storage**: Technical metadata, schema, statistics
- **Asset Discovery**: Searchable repository of data sources
- **Lineage Tracking**: Shows data flow and transformations
- **Integration**: Connects to actual data systems

#### **Business Glossary:**
- **Business Focus**: Contains business terms and definitions
- **Terminology Management**: Standardized business vocabulary
- **Conceptual Layer**: Abstract business concepts and rules
- **Governance**: Controlled vocabulary with approval workflows
- **Relationships**: Links business terms to data assets

```python
# Example: Creating business glossary terms and linking to data assets
class CollibraGlossaryManager:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_business_term(self, name, definition, domain_id):
        """Create a business glossary term"""
        term_data = {
            'name': name,
            'typeId': 'business-term-type-id',
            'domainId': domain_id,
            'attributes': [
                {
                    'typeId': 'definition-attribute-id',
                    'value': definition
                }
            ]
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/assets"
        response = self.client.session.post(endpoint, json=term_data)
        return response.json()
    
    def link_term_to_asset(self, term_id, asset_id):
        """Link business term to data asset"""
        relation_data = {
            'sourceId': term_id,
            'targetId': asset_id,
            'typeId': 'business-term-to-data-asset-relation-id'
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/relations"
        response = self.client.session.post(endpoint, json=relation_data)
        return response.json()

# Usage example
glossary = CollibraGlossaryManager(client)
term = glossary.create_business_term(
    name="Customer",
    definition="An individual or organization that purchases goods or services",
    domain_id="business-glossary-domain-id"
)
print(f"Created business term: {term['name']}")
```

### 3. How does Collibra handle data discovery and cataloging?

**Answer:** Collibra provides automated data discovery through connectors and scanners that identify and catalog data assets across the organization.

#### **Discovery Process:**
1. **Connection Setup**: Configure connectors to data sources
2. **Automated Scanning**: Scheduled or on-demand scanning
3. **Metadata Extraction**: Technical metadata, schema, statistics
4. **Asset Creation**: Automatic creation of catalog entries
5. **Classification**: AI-powered data classification and tagging
6. **Relationship Discovery**: Identification of asset relationships

```python
# Example: Setting up automated data discovery
class CollibraDataDiscovery:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_database_connection(self, name, connection_string, db_type):
        """Create a database connection for discovery"""
        connection_data = {
            'name': name,
            'connectionString': connection_string,
            'databaseType': db_type,
            'enabled': True,
            'scanSchedule': {
                'frequency': 'DAILY',
                'time': '02:00'
            }
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/connections"
        response = self.client.session.post(endpoint, json=connection_data)
        return response.json()
    
    def trigger_discovery_scan(self, connection_id):
        """Trigger an immediate discovery scan"""
        scan_data = {
            'connectionId': connection_id,
            'scanType': 'FULL',
            'includeData': True,
            'includeStatistics': True
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/discovery/scans"
        response = self.client.session.post(endpoint, json=scan_data)
        return response.json()
    
    def get_scan_results(self, scan_id):
        """Get results of a discovery scan"""
        endpoint = f"{self.client.base_url}/rest/2.0/discovery/scans/{scan_id}"
        response = self.client.session.get(endpoint)
        return response.json()

# Usage
discovery = CollibraDataDiscovery(client)
connection = discovery.create_database_connection(
    name="Production Database",
    connection_string="jdbc:postgresql://prod-db:5432/main",
    db_type="POSTGRESQL"
)
print(f"Created connection: {connection['name']}")
```

### 4. What are the key components of Collibra's data governance framework?

**Answer:** Collibra's governance framework consists of several interconnected components that work together to ensure comprehensive data governance.

#### **Key Components:**

**1. Domains and Communities**
- **Domains**: Logical groupings of related data assets
- **Communities**: Organizational units responsible for domains
- **Ownership**: Clear accountability and responsibility

**2. Policies and Standards**
- **Data Policies**: Rules governing data usage and management
- **Standards**: Technical and business standards for data
- **Compliance**: Regulatory and internal compliance requirements

**3. Roles and Responsibilities**
- **Data Stewards**: Day-to-day data management
- **Data Owners**: Business accountability for data
- **Data Custodians**: Technical responsibility for data systems

**4. Workflows and Processes**
- **Approval Workflows**: Controlled change management
- **Issue Management**: Problem identification and resolution
- **Request Management**: Data access and modification requests

```python
# Example: Implementing governance framework
class CollibraGovernanceFramework:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_governance_domain(self, name, description, community_id):
        """Create a governance domain"""
        domain_data = {
            'name': name,
            'description': description,
            'communityId': community_id,
            'typeId': 'governance-domain-type-id'
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/domains"
        response = self.client.session.post(endpoint, json=domain_data)
        return response.json()
    
    def assign_data_steward(self, asset_id, user_id):
        """Assign a data steward to an asset"""
        responsibility_data = {
            'resourceId': asset_id,
            'userId': user_id,
            'roleId': 'data-steward-role-id'
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/responsibilities"
        response = self.client.session.post(endpoint, json=responsibility_data)
        return response.json()
    
    def create_data_policy(self, name, description, domain_id):
        """Create a data governance policy"""
        policy_data = {
            'name': name,
            'typeId': 'policy-type-id',
            'domainId': domain_id,
            'attributes': [
                {
                    'typeId': 'policy-description-attribute-id',
                    'value': description
                }
            ]
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/assets"
        response = self.client.session.post(endpoint, json=policy_data)
        return response.json()

# Usage
governance = CollibraGovernanceFramework(client)
domain = governance.create_governance_domain(
    name="Customer Data Governance",
    description="Governance domain for customer-related data assets",
    community_id="customer-community-id"
)
print(f"Created governance domain: {domain['name']}")
```

### 5. How does Collibra implement data lineage tracking?

**Answer:** Collibra provides comprehensive data lineage tracking that shows the complete journey of data from source to consumption, including all transformations and dependencies.

#### **Lineage Components:**
- **Technical Lineage**: System-to-system data flow
- **Business Lineage**: Business process data flow
- **Column-level Lineage**: Field-level data transformations
- **Impact Analysis**: Downstream effect assessment
- **Visual Representation**: Interactive lineage diagrams

```python
# Example: Working with data lineage
class CollibraLineageManager:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def get_asset_lineage(self, asset_id, direction='BOTH', depth=3):
        """Get lineage for a specific asset"""
        params = {
            'direction': direction,  # UPSTREAM, DOWNSTREAM, BOTH
            'depth': depth,
            'includeColumns': True
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/assets/{asset_id}/lineage"
        response = self.client.session.get(endpoint, params=params)
        return response.json()
    
    def create_lineage_relation(self, source_id, target_id, transformation_logic=None):
        """Create a lineage relationship between assets"""
        relation_data = {
            'sourceId': source_id,
            'targetId': target_id,
            'typeId': 'data-flow-relation-id'
        }
        
        if transformation_logic:
            relation_data['attributes'] = [
                {
                    'typeId': 'transformation-logic-attribute-id',
                    'value': transformation_logic
                }
            ]
        
        endpoint = f"{self.client.base_url}/rest/2.0/relations"
        response = self.client.session.post(endpoint, json=relation_data)
        return response.json()
    
    def analyze_impact(self, asset_id, change_type):
        """Analyze impact of changes to an asset"""
        lineage = self.get_asset_lineage(asset_id, direction='DOWNSTREAM')
        
        impacted_assets = []
        for relation in lineage.get('relations', []):
            if relation['target']['id'] != asset_id:
                impacted_assets.append({
                    'asset_id': relation['target']['id'],
                    'asset_name': relation['target']['name'],
                    'impact_level': self._calculate_impact_level(relation, change_type)
                })
        
        return impacted_assets
    
    def _calculate_impact_level(self, relation, change_type):
        """Calculate impact level based on relation type and change"""
        # Simplified impact calculation
        if change_type == 'SCHEMA_CHANGE':
            return 'HIGH'
        elif change_type == 'DATA_QUALITY_ISSUE':
            return 'MEDIUM'
        else:
            return 'LOW'

# Usage
lineage = CollibraLineageManager(client)
asset_lineage = lineage.get_asset_lineage('customer-table-asset-id')
print(f"Found {len(asset_lineage.get('relations', []))} lineage relationships")

# Impact analysis
impact = lineage.analyze_impact('customer-table-asset-id', 'SCHEMA_CHANGE')
print(f"Schema change would impact {len(impact)} downstream assets")
```

### 6. What is the role of workflows in Collibra?

**Answer:** Workflows in Collibra automate governance processes, ensuring consistent application of policies and procedures across the organization.

#### **Workflow Types:**
- **Approval Workflows**: Multi-step approval processes
- **Issue Resolution**: Problem tracking and resolution
- **Data Request**: Access request and provisioning
- **Change Management**: Controlled asset modifications
- **Compliance**: Regulatory compliance processes

```python
# Example: Creating and managing workflows
class CollibraWorkflowManager:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_data_access_request(self, requester_id, asset_id, purpose, duration):
        """Create a data access request workflow"""
        workflow_data = {
            'workflowDefinitionId': 'data-access-request-workflow',
            'businessItems': [asset_id],
            'variables': {
                'requester': requester_id,
                'purpose': purpose,
                'duration_days': duration,
                'status': 'PENDING_APPROVAL'
            }
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/workflows"
        response = self.client.session.post(endpoint, json=workflow_data)
        return response.json()
    
    def get_pending_tasks(self, user_id):
        """Get pending workflow tasks for a user"""
        params = {
            'assignee': user_id,
            'status': 'OPEN'
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/workflows/tasks"
        response = self.client.session.get(endpoint, params=params)
        return response.json()
    
    def complete_task(self, task_id, action, comments=None):
        """Complete a workflow task"""
        task_data = {
            'action': action,  # APPROVE, REJECT, REQUEST_INFO
            'comments': comments or ''
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/workflows/tasks/{task_id}/complete"
        response = self.client.session.post(endpoint, json=task_data)
        return response.json()
    
    def track_workflow_progress(self, workflow_id):
        """Track the progress of a workflow"""
        endpoint = f"{self.client.base_url}/rest/2.0/workflows/{workflow_id}"
        response = self.client.session.get(endpoint)
        workflow = response.json()
        
        progress = {
            'workflow_id': workflow_id,
            'status': workflow.get('status'),
            'current_step': workflow.get('currentActivity'),
            'completed_tasks': len([t for t in workflow.get('tasks', []) if t['status'] == 'COMPLETED']),
            'pending_tasks': len([t for t in workflow.get('tasks', []) if t['status'] == 'OPEN'])
        }
        
        return progress

# Usage
workflow_mgr = CollibraWorkflowManager(client)

# Create access request
request = workflow_mgr.create_data_access_request(
    requester_id='user-123',
    asset_id='customer-data-asset-id',
    purpose='Marketing analysis for Q4 campaign',
    duration=30
)
print(f"Created workflow: {request['id']}")

# Check pending tasks
pending = workflow_mgr.get_pending_tasks('data-steward-user-id')
print(f"Found {len(pending.get('results', []))} pending tasks")
```

### 7. How does Collibra handle data quality management?

**Answer:** Collibra provides comprehensive data quality management through automated profiling, configurable rules, continuous monitoring, and issue tracking.

#### **Data Quality Components:**
- **Data Profiling**: Automated analysis of data characteristics
- **Quality Rules**: Configurable validation rules
- **Quality Monitoring**: Continuous quality assessment
- **Quality Dashboards**: Visual quality reporting
- **Issue Management**: Quality issue tracking and resolution

```python
# Example: Data quality management implementation
class CollibraDataQuality:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_quality_rule(self, asset_id, rule_type, parameters):
        """Create a data quality rule"""
        rule_data = {
            'name': f"{rule_type}_rule_{asset_id}",
            'assetId': asset_id,
            'ruleType': rule_type,
            'parameters': parameters,
            'enabled': True,
            'schedule': {
                'frequency': 'DAILY',
                'time': '06:00'
            }
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/dataQuality/rules"
        response = self.client.session.post(endpoint, json=rule_data)
        return response.json()
    
    def run_data_profiling(self, asset_id):
        """Run data profiling on an asset"""
        profile_data = {
            'assetId': asset_id,
            'includeStatistics': True,
            'includePatterns': True,
            'sampleSize': 10000
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/dataQuality/profiling"
        response = self.client.session.post(endpoint, json=profile_data)
        return response.json()
    
    def get_quality_metrics(self, asset_id, start_date, end_date):
        """Get quality metrics for an asset"""
        params = {
            'assetId': asset_id,
            'startDate': start_date,
            'endDate': end_date
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/dataQuality/metrics"
        response = self.client.session.get(endpoint, params=params)
        return response.json()
    
    def create_quality_issue(self, asset_id, issue_type, description, severity):
        """Create a data quality issue"""
        issue_data = {
            'assetId': asset_id,
            'issueType': issue_type,
            'description': description,
            'severity': severity,
            'status': 'OPEN',
            'assignee': 'data-steward-user-id'
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/dataQuality/issues"
        response = self.client.session.post(endpoint, json=issue_data)
        return response.json()

# Usage
quality_mgr = CollibraDataQuality(client)

# Create completeness rule
completeness_rule = quality_mgr.create_quality_rule(
    asset_id='customer-table-id',
    rule_type='COMPLETENESS',
    parameters={
        'column': 'email',
        'threshold': 0.95,
        'operator': 'GREATER_THAN_OR_EQUAL'
    }
)
print(f"Created quality rule: {completeness_rule['name']}")

# Run profiling
profile_job = quality_mgr.run_data_profiling('customer-table-id')
print(f"Started profiling job: {profile_job['id']}")
```

### 8. What are the different types of users and roles in Collibra?

**Answer:** Collibra supports various user types and roles to accommodate different organizational needs and responsibilities in data governance.

#### **User Types:**
- **Business Users**: Consume data and participate in governance
- **Data Stewards**: Manage data quality and governance processes
- **Data Owners**: Business accountability for data domains
- **Technical Users**: Implement and maintain technical aspects
- **Administrators**: System configuration and management

#### **Key Roles:**
- **Data Steward**: Day-to-day data management and quality
- **Data Owner**: Business responsibility and decision-making
- **Data Custodian**: Technical implementation and maintenance
- **Data Consumer**: Uses data for business purposes
- **Data Analyst**: Analyzes data and creates insights

```python
# Example: User and role management
class CollibraUserManagement:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_user(self, username, email, first_name, last_name, roles):
        """Create a new user with specified roles"""
        user_data = {
            'userName': username,
            'emailAddress': email,
            'firstName': first_name,
            'lastName': last_name,
            'enabled': True,
            'roles': roles
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/users"
        response = self.client.session.post(endpoint, json=user_data)
        return response.json()
    
    def assign_responsibility(self, user_id, asset_id, role_type):
        """Assign a user responsibility for an asset"""
        responsibility_data = {
            'userId': user_id,
            'resourceId': asset_id,
            'roleId': role_type
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/responsibilities"
        response = self.client.session.post(endpoint, json=responsibility_data)
        return response.json()
    
    def get_user_responsibilities(self, user_id):
        """Get all responsibilities for a user"""
        params = {'userId': user_id}
        
        endpoint = f"{self.client.base_url}/rest/2.0/responsibilities"
        response = self.client.session.get(endpoint, params=params)
        return response.json()
    
    def create_custom_role(self, name, permissions):
        """Create a custom role with specific permissions"""
        role_data = {
            'name': name,
            'description': f"Custom role: {name}",
            'permissions': permissions
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/roles"
        response = self.client.session.post(endpoint, json=role_data)
        return response.json()

# Usage
user_mgr = CollibraUserManagement(client)

# Create data steward user
steward = user_mgr.create_user(
    username='john.steward',
    email='john.steward@company.com',
    first_name='John',
    last_name='Steward',
    roles=['DATA_STEWARD', 'CATALOG_USER']
)
print(f"Created user: {steward['userName']}")

# Assign responsibility
responsibility = user_mgr.assign_responsibility(
    user_id=steward['id'],
    asset_id='customer-domain-id',
    role_type='DATA_STEWARD'
)
print(f"Assigned stewardship responsibility")
```

### 9. How does Collibra integrate with external systems?

**Answer:** Collibra provides extensive integration capabilities through REST APIs, connectors, webhooks, and event-driven architecture to connect with various external systems.

#### **Integration Methods:**
- **REST APIs**: Comprehensive API for all platform functions
- **Connectors**: Pre-built connectors for popular systems
- **Webhooks**: Real-time event notifications
- **File Import/Export**: Bulk data exchange
- **JDBC/ODBC**: Database connectivity
- **Message Queues**: Event-driven integration

```python
# Example: External system integration
class CollibraIntegrationManager:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def sync_with_external_catalog(self, external_system_config):
        """Synchronize with external data catalog"""
        # Connect to external system
        external_client = self._create_external_client(external_system_config)
        
        # Get assets from external system
        external_assets = external_client.get_all_assets()
        
        synced_assets = []
        for ext_asset in external_assets:
            # Check if asset exists in Collibra
            existing = self.client.search_assets(ext_asset['name'])
            
            if not existing.get('results'):
                # Create new asset in Collibra
                collibra_asset = self._create_asset_from_external(ext_asset)
                synced_assets.append(collibra_asset)
            else:
                # Update existing asset
                updated_asset = self._update_asset_from_external(
                    existing['results'][0]['id'], 
                    ext_asset
                )
                synced_assets.append(updated_asset)
        
        return synced_assets
    
    def setup_webhook_listener(self, webhook_url, event_types):
        """Set up webhook for real-time notifications"""
        webhook_data = {
            'url': webhook_url,
            'eventTypes': event_types,
            'enabled': True,
            'authentication': {
                'type': 'BEARER_TOKEN',
                'token': 'your-webhook-token'
            }
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/webhooks"
        response = self.client.session.post(endpoint, json=webhook_data)
        return response.json()
    
    def export_metadata_to_external(self, domain_id, export_format='JSON'):
        """Export metadata to external system"""
        # Get all assets in domain
        assets = self.client.get_domain_assets(domain_id)
        
        # Transform to external format
        exported_data = []
        for asset in assets.get('results', []):
            exported_data.append({
                'id': asset['id'],
                'name': asset['name'],
                'type': asset['type']['name'],
                'description': asset.get('description', ''),
                'attributes': self._extract_attributes(asset),
                'relationships': self._extract_relationships(asset['id'])
            })
        
        # Send to external system
        if export_format == 'JSON':
            return json.dumps(exported_data, indent=2)
        elif export_format == 'CSV':
            return self._convert_to_csv(exported_data)
    
    def _create_external_client(self, config):
        """Create client for external system"""
        # Implementation depends on external system
        pass
    
    def _create_asset_from_external(self, external_asset):
        """Create Collibra asset from external asset"""
        asset_data = {
            'name': external_asset['name'],
            'typeId': self._map_asset_type(external_asset['type']),
            'domainId': external_asset.get('domain_id', 'default-domain-id'),
            'attributes': self._map_attributes(external_asset.get('attributes', {}))
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/assets"
        response = self.client.session.post(endpoint, json=asset_data)
        return response.json()

# Usage
integration_mgr = CollibraIntegrationManager(client)

# Set up webhook for asset changes
webhook = integration_mgr.setup_webhook_listener(
    webhook_url='https://your-system.com/webhook',
    event_types=['ASSET_CREATED', 'ASSET_UPDATED', 'ASSET_DELETED']
)
print(f"Created webhook: {webhook['id']}")
```

### 10. What is the difference between technical and business metadata in Collibra?

**Answer:** Technical and business metadata serve different purposes and audiences in the data governance ecosystem.

#### **Technical Metadata:**
- **System-Generated**: Automatically extracted from data systems
- **Technical Details**: Schema, data types, constraints, statistics
- **IT Focus**: Used by technical teams for system management
- **Structural Information**: How data is stored and processed
- **Examples**: Column names, data types, table relationships, file sizes

#### **Business Metadata:**
- **Human-Generated**: Created and maintained by business users
- **Business Context**: Definitions, rules, usage guidelines
- **Business Focus**: Used by business users for understanding data
- **Semantic Information**: What data means and how it's used
- **Examples**: Business definitions, data quality rules, usage policies

```python
# Example: Managing technical and business metadata
class CollibraMetadataManager:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def extract_technical_metadata(self, connection_id):
        """Extract technical metadata from data source"""
        scan_data = {
            'connectionId': connection_id,
            'extractTechnicalMetadata': True,
            'includeStatistics': True,
            'includeConstraints': True
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/discovery/scans"
        response = self.client.session.post(endpoint, json=scan_data)
        return response.json()
    
    def add_business_metadata(self, asset_id, business_metadata):
        """Add business metadata to an asset"""
        attributes = []
        
        # Business definition
        if business_metadata.get('definition'):
            attributes.append({
                'typeId': 'business-definition-attribute-id',
                'value': business_metadata['definition']
            })
        
        # Business rules
        if business_metadata.get('business_rules'):
            attributes.append({
                'typeId': 'business-rules-attribute-id',
                'value': business_metadata['business_rules']
            })
        
        # Data owner
        if business_metadata.get('data_owner'):
            attributes.append({
                'typeId': 'data-owner-attribute-id',
                'value': business_metadata['data_owner']
            })
        
        # Update asset with business metadata
        for attribute in attributes:
            endpoint = f"{self.client.base_url}/rest/2.0/assets/{asset_id}/attributes"
            response = self.client.session.post(endpoint, json=attribute)
        
        return True
    
    def get_complete_metadata(self, asset_id):
        """Get both technical and business metadata for an asset"""
        endpoint = f"{self.client.base_url}/rest/2.0/assets/{asset_id}"
        response = self.client.session.get(endpoint)
        asset = response.json()
        
        metadata = {
            'asset_id': asset_id,
            'name': asset['name'],
            'technical_metadata': {
                'type': asset['type']['name'],
                'domain': asset['domain']['name'],
                'created_date': asset.get('createdOn'),
                'modified_date': asset.get('lastModifiedOn')
            },
            'business_metadata': {}
        }
        
        # Extract business metadata from attributes
        for attribute in asset.get('attributes', []):
            attr_type = attribute['type']['name']
            if 'business' in attr_type.lower():
                metadata['business_metadata'][attr_type] = attribute['value']
        
        return metadata
    
    def compare_metadata_completeness(self, asset_id):
        """Compare technical vs business metadata completeness"""
        metadata = self.get_complete_metadata(asset_id)
        
        technical_fields = len([k for k in metadata['technical_metadata'].keys() 
                              if metadata['technical_metadata'][k] is not None])
        business_fields = len([k for k in metadata['business_metadata'].keys() 
                             if metadata['business_metadata'][k] is not None])
        
        return {
            'asset_id': asset_id,
            'technical_completeness': technical_fields,
            'business_completeness': business_fields,
            'total_completeness': technical_fields + business_fields,
            'needs_business_metadata': business_fields < 3  # Threshold
        }

# Usage
metadata_mgr = CollibraMetadataManager(client)

# Add business metadata
business_info = {
    'definition': 'Customer information including contact details and preferences',
    'business_rules': 'Email must be unique, phone number optional',
    'data_owner': 'Marketing Department'
}

metadata_mgr.add_business_metadata('customer-table-id', business_info)
print("Added business metadata to customer table")

# Get complete metadata view
complete_metadata = metadata_mgr.get_complete_metadata('customer-table-id')
print(f"Technical metadata fields: {len(complete_metadata['technical_metadata'])}")
print(f"Business metadata fields: {len(complete_metadata['business_metadata'])}")
```

### 11. How do you implement data classification in Collibra?

**Answer:** Data classification in Collibra involves categorizing data based on sensitivity, regulatory requirements, and business value.

```python
class CollibraDataClassification:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def classify_asset(self, asset_id, classification_level, tags):
        """Classify an asset with sensitivity level and tags"""
        classification_data = {
            'assetId': asset_id,
            'classificationLevel': classification_level,  # PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED
            'tags': tags,
            'autoClassification': False
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/assets/{asset_id}/classification"
        response = self.client.session.post(endpoint, json=classification_data)
        return response.json()

# Usage
classifier = CollibraDataClassification(client)
classifier.classify_asset('customer-table-id', 'CONFIDENTIAL', ['PII', 'GDPR'])
```

### 12. What are Collibra's data privacy management capabilities?

**Answer:** Collibra provides comprehensive privacy management for GDPR, CCPA, and other regulations.

**Key Features:**
- Privacy Impact Assessments (PIA)
- Data Subject Rights management
- Consent tracking and management
- Privacy by Design workflows
- Regulatory reporting

```python
class CollibraPrivacyManager:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_privacy_assessment(self, asset_id, assessment_type):
        """Create a Privacy Impact Assessment"""
        pia_data = {
            'assetId': asset_id,
            'assessmentType': assessment_type,
            'status': 'IN_PROGRESS'
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/privacy/assessments"
        response = self.client.session.post(endpoint, json=pia_data)
        return response.json()

# Usage
privacy_mgr = CollibraPrivacyManager(client)
pia = privacy_mgr.create_privacy_assessment('customer-data-id', 'GDPR_PIA')
```

### 13. How does Collibra handle data stewardship workflows?

**Answer:** Data stewardship workflows automate the assignment, tracking, and management of data stewardship responsibilities.

```python
class CollibrarStewardshipWorkflow:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def assign_steward(self, asset_id, steward_id, stewardship_type):
        """Assign a data steward to an asset"""
        assignment_data = {
            'assetId': asset_id,
            'stewardId': steward_id,
            'stewardshipType': stewardship_type,
            'startDate': '2024-01-01'
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/stewardship/assignments"
        response = self.client.session.post(endpoint, json=assignment_data)
        return response.json()
```

### 14. What is the role of communities and domains in Collibra?

**Answer:** Communities and domains provide organizational structure for data governance.

**Communities:** Organizational units (departments, teams)
**Domains:** Logical groupings of related data assets

```python
class CollibraOrganizationStructure:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_community(self, name, description):
        """Create a new community"""
        community_data = {
            'name': name,
            'description': description
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/communities"
        response = self.client.session.post(endpoint, json=community_data)
        return response.json()
```

### 15. How do you configure data quality rules in Collibra?

**Answer:** Data quality rules are configured to automatically validate data against business requirements.

```python
class CollibraQualityRules:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_completeness_rule(self, asset_id, column_name, threshold):
        """Create a completeness quality rule"""
        rule_data = {
            'assetId': asset_id,
            'ruleType': 'COMPLETENESS',
            'column': column_name,
            'threshold': threshold,
            'enabled': True
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/dataQuality/rules"
        response = self.client.session.post(endpoint, json=rule_data)
        return response.json()
```

### 16. What are the different asset types in Collibra?

**Answer:** Collibra supports various asset types to represent different kinds of data resources.

**Common Asset Types:**
- Tables, Views, Columns
- Files, Reports, Dashboards
- Business Terms, Policies
- Systems, Applications
- Data Sets, Data Elements

### 17. How does Collibra support regulatory compliance?

**Answer:** Collibra provides built-in compliance frameworks and automated reporting capabilities.

**Compliance Features:**
- GDPR compliance workflows
- CCPA privacy management
- SOX financial controls
- BCBS 239 risk data aggregation
- Custom regulatory frameworks

### 18. What is the Collibra REST API and how is it used?

**Answer:** The Collibra REST API provides programmatic access to all platform functionality.

```python
class CollibraAPIClient:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (username, password)
    
    def get_asset(self, asset_id):
        """Get asset details"""
        endpoint = f"{self.base_url}/rest/2.0/assets/{asset_id}"
        response = self.session.get(endpoint)
        return response.json()
```

### 19. How do you implement data lineage automation in Collibra?

**Answer:** Data lineage can be automated through connectors, APIs, and integration with ETL tools.

```python
class CollibraLineageAutomation:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_automated_lineage(self, source_id, target_id, transformation):
        """Create automated lineage relationship"""
        lineage_data = {
            'sourceId': source_id,
            'targetId': target_id,
            'transformation': transformation,
            'automated': True
        }
        
        endpoint = f"{self.client.base_url}/rest/2.0/lineage"
        response = self.client.session.post(endpoint, json=lineage_data)
        return response.json()
```

### 20. What are the key performance considerations for Collibra?

**Answer:** Performance optimization involves proper configuration, indexing, and resource management.

**Performance Factors:**
- Database optimization
- Search index management
- Connector configuration
- User session management
- API rate limiting

### 21. How do you manage data access requests in Collibra?

**Answer:** Data access requests are managed through automated workflows with approval chains.

```python
class CollibraAccessManager:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_access_request(self, user_id, asset_id, access_type, justification):
        """Create data access request"""
        request_data = {
            'requesterId': user_id,
            'assetId': asset_id,
            'accessType': access_type,
            'justification': justification,
            'status': 'PENDING'
        }
        
        endpoint = f"{self.base_url}/rest/2.0/access/requests"
        response = self.session.post(endpoint, json=request_data)
        return response.json()
```

### 22. What is the difference between attributes and relations in Collibra?

**Answer:** Attributes store properties of assets, while relations define connections between assets.

**Attributes:** Single-valued or multi-valued properties (description, owner, classification)
**Relations:** Connections between assets (lineage, dependencies, associations)

### 23. How does Collibra handle schema evolution and versioning?

**Answer:** Collibra tracks schema changes through automated discovery and version management.

```python
class CollibraSchemaEvolution:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def track_schema_change(self, asset_id, old_schema, new_schema):
        """Track schema evolution"""
        change_data = {
            'assetId': asset_id,
            'changeType': 'SCHEMA_EVOLUTION',
            'oldSchema': old_schema,
            'newSchema': new_schema,
            'timestamp': '2024-01-01T00:00:00Z'
        }
        
        endpoint = f"{self.base_url}/rest/2.0/assets/{asset_id}/changes"
        response = self.session.post(endpoint, json=change_data)
        return response.json()
```

### 24. What are the different types of connectors available in Collibra?

**Answer:** Collibra provides various connectors for different data sources and systems.

**Connector Types:**
- Database connectors (Oracle, SQL Server, PostgreSQL)
- Cloud connectors (AWS, Azure, GCP)
- File system connectors (HDFS, S3, Azure Blob)
- BI tool connectors (Tableau, Power BI, Qlik)
- ETL tool connectors (Informatica, Talend, SSIS)

### 25. How do you implement custom workflows in Collibra?

**Answer:** Custom workflows are created using Collibra's workflow designer and BPMN 2.0 standard.

```python
class CollibraCustomWorkflow:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_custom_workflow(self, workflow_definition):
        """Create custom workflow"""
        workflow_data = {
            'name': workflow_definition['name'],
            'definition': workflow_definition['bpmn_xml'],
            'enabled': True
        }
        
        endpoint = f"{self.base_url}/rest/2.0/workflows/definitions"
        response = self.session.post(endpoint, json=workflow_data)
        return response.json()
```

### 26. What is the role of the Collibra Data Intelligence Cloud?

**Answer:** Collibra DIC is the cloud-native platform providing scalable data governance capabilities.

**Key Features:**
- Multi-tenant architecture
- Automatic scaling
- Built-in security
- Regular updates
- Global availability

### 27. How does Collibra support data discovery and search?

**Answer:** Collibra provides advanced search capabilities with AI-powered recommendations.

```python
class CollibraSearch:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def advanced_search(self, query, filters=None):
        """Perform advanced search"""
        search_params = {
            'query': query,
            'limit': 50,
            'offset': 0
        }
        
        if filters:
            search_params.update(filters)
        
        endpoint = f"{self.base_url}/rest/2.0/search"
        response = self.session.get(endpoint, params=search_params)
        return response.json()
```

### 28. What are the security features in Collibra?

**Answer:** Collibra provides comprehensive security features for enterprise data governance.

**Security Features:**
- Role-based access control (RBAC)
- Single sign-on (SSO) integration
- Data encryption at rest and in transit
- Audit logging and monitoring
- API security and rate limiting

### 29. How do you monitor and troubleshoot Collibra performance?

**Answer:** Performance monitoring involves system metrics, user activity, and application logs.

**Monitoring Areas:**
- System resource utilization
- Database performance
- Search index performance
- User session metrics
- API response times

### 30. What is the Collibra Catalog and how does it differ from other catalogs?

**Answer:** Collibra Catalog is an integrated component of the broader governance platform.

**Differentiators:**
- Integrated governance workflows
- Business context and glossary
- Automated quality monitoring
- Privacy and compliance features
- Collaborative data stewardship

### 31. How do you implement data retention policies in Collibra?

**Answer:** Data retention policies are implemented through governance workflows and automated processes.

```python
class CollibraRetentionManager:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_retention_policy(self, asset_id, retention_period, action):
        """Create data retention policy"""
        policy_data = {
            'assetId': asset_id,
            'retentionPeriod': retention_period,
            'action': action,  # DELETE, ARCHIVE, ANONYMIZE
            'enabled': True
        }
        
        endpoint = f"{self.base_url}/rest/2.0/retention/policies"
        response = self.session.post(endpoint, json=policy_data)
        return response.json()
```

### 32. What are the different deployment options for Collibra?

**Answer:** Collibra offers multiple deployment options to meet different organizational needs.

**Deployment Options:**
- Collibra Cloud (SaaS)
- Private Cloud deployment
- On-premises installation
- Hybrid deployment models

### 33. How does Collibra handle multi-language support?

**Answer:** Collibra provides internationalization support for global organizations.

**Multi-language Features:**
- Localized user interface
- Multi-language metadata
- Unicode support
- Regional date/time formats
- Localized workflows

### 34. What is the Collibra Marketplace and its purpose?

**Answer:** Collibra Marketplace provides pre-built accelerators, connectors, and solutions.

**Marketplace Components:**
- Industry-specific templates
- Connector packages
- Workflow templates
- Best practice guides
- Integration patterns

### 35. How do you backup and restore Collibra data?

**Answer:** Backup and restore procedures ensure data protection and business continuity.

**Backup Components:**
- Database backups
- Configuration exports
- File system backups
- Metadata exports
- User and role configurations

### 36. How does Collibra support data modeling and design?

**Answer:** Collibra provides conceptual and logical data modeling capabilities.

**Modeling Features:**
- Entity-relationship diagrams
- Conceptual data models
- Logical data models
- Model versioning and comparison
- Model-to-implementation mapping

### 37. What are the key metrics and KPIs for Collibra governance?

**Answer:** Governance metrics track the effectiveness of data governance initiatives.

**Key Metrics:**
- Catalog completeness percentage
- Data quality scores
- Policy compliance rates
- User adoption metrics
- Issue resolution times

### 38. How do you configure notifications and alerts in Collibra?

**Answer:** Notifications keep stakeholders informed of important governance events.

```python
class CollibraNotifications:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_notification_rule(self, event_type, recipients, conditions):
        """Create notification rule"""
        rule_data = {
            'eventType': event_type,
            'recipients': recipients,
            'conditions': conditions,
            'enabled': True
        }
        
        endpoint = f"{self.base_url}/rest/2.0/notifications/rules"
        response = self.session.post(endpoint, json=rule_data)
        return response.json()
```

### 39. What is the role of tags and labels in Collibra?

**Answer:** Tags and labels provide flexible categorization and organization of assets.

**Use Cases:**
- Data classification
- Project organization
- Compliance marking
- Custom categorization
- Search enhancement

### 40. How does Collibra handle data profiling automation?

**Answer:** Automated data profiling provides continuous insights into data characteristics.

```python
class CollibraAutomatedProfiling:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def schedule_profiling(self, asset_id, schedule):
        """Schedule automated profiling"""
        profile_config = {
            'assetId': asset_id,
            'schedule': schedule,
            'includeStatistics': True,
            'includePatterns': True
        }
        
        endpoint = f"{self.base_url}/rest/2.0/profiling/schedules"
        response = self.session.post(endpoint, json=profile_config)
        return response.json()
```

### 41-50. Additional Basic Questions

**41. What are the licensing models for Collibra?**
**Answer:** User-based, asset-based, and enterprise licensing options.

**42. How does Collibra support data virtualization?**
**Answer:** Integration with data virtualization platforms for unified data access.

**43. What is the Collibra mobile application?**
**Answer:** Mobile app for on-the-go data governance and catalog access.

**44. How do you manage data dictionaries in Collibra?**
**Answer:** Centralized data dictionary management with business glossary integration.

**45. What are the reporting capabilities in Collibra?**
**Answer:** Built-in dashboards, custom reports, and API-based reporting.

**46. How does Collibra handle data anonymization?**
**Answer:** Privacy workflows with anonymization and pseudonymization capabilities.

**47. What is the role of data contracts in Collibra?**
**Answer:** Formal agreements defining data usage, quality, and delivery expectations.

**48. How do you implement data observability in Collibra?**
**Answer:** Monitoring data health, usage patterns, and quality metrics.

**49. What are the disaster recovery options for Collibra?**
**Answer:** Multi-region deployment, backup strategies, and failover procedures.

**50. How does Collibra support agile data governance?**
**Answer:** Iterative governance implementation with rapid value delivery.

---

## Intermediate Level Questions (51-100)

### 51. How do you implement advanced data lineage with business context?

**Answer:** Advanced lineage combines technical data flow with business process context.

```python
class AdvancedLineageManager:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_business_lineage(self, business_process_id, data_assets, transformations):
        """Create business process lineage"""
        lineage_data = {
            'businessProcessId': business_process_id,
            'dataAssets': data_assets,
            'transformations': transformations,
            'businessContext': True
        }
        
        endpoint = f"{self.base_url}/rest/2.0/lineage/business"
        response = self.session.post(endpoint, json=lineage_data)
        return response.json()
    
    def analyze_business_impact(self, asset_id, change_scenario):
        """Analyze business impact of data changes"""
        impact_analysis = {
            'assetId': asset_id,
            'changeScenario': change_scenario,
            'includeBusinessProcesses': True,
            'includeDownstreamReports': True
        }
        
        endpoint = f"{self.base_url}/rest/2.0/lineage/impact-analysis"
        response = self.session.post(endpoint, json=impact_analysis)
        return response.json()
```

### 52. How do you configure complex data quality monitoring with custom rules?

**Answer:** Complex quality monitoring involves custom rule engines and multi-dimensional quality assessment.

```python
class ComplexQualityMonitoring:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_composite_quality_rule(self, asset_id, rule_definition):
        """Create composite quality rule with multiple conditions"""
        composite_rule = {
            'assetId': asset_id,
            'ruleType': 'COMPOSITE',
            'conditions': rule_definition['conditions'],
            'aggregationMethod': rule_definition['aggregation'],
            'threshold': rule_definition['threshold'],
            'severity': rule_definition['severity']
        }
        
        endpoint = f"{self.base_url}/rest/2.0/dataQuality/composite-rules"
        response = self.session.post(endpoint, json=composite_rule)
        return response.json()
    
    def setup_quality_monitoring_pipeline(self, assets, quality_dimensions):
        """Set up comprehensive quality monitoring pipeline"""
        pipeline_config = {
            'assets': assets,
            'qualityDimensions': quality_dimensions,
            'monitoringFrequency': 'HOURLY',
            'alertThresholds': {
                'critical': 0.8,
                'warning': 0.9
            }
        }
        
        endpoint = f"{self.base_url}/rest/2.0/dataQuality/monitoring-pipeline"
        response = self.session.post(endpoint, json=pipeline_config)
        return response.json()
```

### 53. How do you implement enterprise-scale data governance policies?

**Answer:** Enterprise governance requires hierarchical policies, automated enforcement, and compliance tracking.

```python
class EnterpriseGovernancePolicies:
    def __init__(self, collibra_client):
        self.client = collibra_client
    
    def create_policy_hierarchy(self, parent_policy_id, child_policies):
        """Create hierarchical policy structure"""
        hierarchy_data = {
            'parentPolicyId': parent_policy_id,
            'childPolicies': child_policies,
            'inheritanceRules': {
                'overrideAllowed': True,
                'mandatoryAttributes': ['classification', 'retention']
            }
        }
        
        endpoint = f"{self.base_url}/rest/2.0/policies/hierarchy"
        response = self.session.post(endpoint, json=hierarchy_data)
        return response.json()
    
    def implement_automated_policy_enforcement(self, policy_id, enforcement_rules):
        """Implement automated policy enforcement"""
        enforcement_config = {
            'policyId': policy_id,
            'enforcementRules': enforcement_rules,
            'automatedActions': {
                'violation_detected': 'CREATE_ISSUE',
                'critical_violation': 'BLOCK_ACCESS'
            }
        }
        
        endpoint = f"{self.base_url}/rest/2.0/policies/enforcement"
        response = self.session.post(endpoint, json=enforcement_config)
        return response.json()
```

---

*Questions 36-53 completed. Continuing with remaining intermediate questions in next batch.*