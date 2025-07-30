# ServiceNow Key Concepts

## 1. IT Service Management Platform
**What it is**: Cloud-based platform for IT service management, workflow automation, and business process management.

**Core Modules**:
- **Incident Management**: Handle service disruptions
- **Problem Management**: Root cause analysis
- **Change Management**: Control system changes
- **Service Catalog**: Self-service portal
- **CMDB**: Configuration management database

## 2. Incident Management
**Incident Lifecycle**:
```yaml
New → In Progress → Resolved → Closed

# Priority Matrix
Priority 1: Critical business impact, no workaround
Priority 2: High impact, workaround available  
Priority 3: Medium impact, some users affected
Priority 4: Low impact, minimal business effect
```

**Incident Creation**:
```javascript
// Create incident via REST API
var incident = new GlideRecord('incident');
incident.initialize();
incident.short_description = 'Data pipeline failure';
incident.description = 'ETL job failed at 2:00 AM, affecting daily reports';
incident.priority = '2';
incident.category = 'Software';
incident.subcategory = 'Data Processing';
incident.assignment_group = 'Data Engineering Team';
incident.insert();
```

## 3. Problem Management
**Problem vs Incident**:
```yaml
# Incident
- Unplanned interruption
- Restore service quickly
- Reactive approach

# Problem  
- Root cause of incidents
- Prevent future occurrences
- Proactive approach
```

**Problem Record**:
```javascript
// Create problem record
var problem = new GlideRecord('problem');
problem.initialize();
problem.short_description = 'Recurring database connection timeouts';
problem.description = 'Multiple incidents related to DB timeouts';
problem.state = '1'; // New
problem.priority = '3';
problem.assignment_group = 'Database Team';
problem.insert();
```

## 4. Change Management
**Change Types**:
```yaml
# Standard Change
- Pre-approved, low risk
- Automated workflow
- Minimal approval required

# Normal Change
- Requires CAB approval
- Risk assessment needed
- Detailed planning required

# Emergency Change
- Urgent business need
- Expedited approval
- Post-implementation review
```

**Change Request**:
```javascript
// Create change request
var change = new GlideRecord('change_request');
change.initialize();
change.short_description = 'Upgrade data warehouse schema';
change.description = 'Add new tables for customer analytics';
change.type = 'normal';
change.risk = '3'; // Moderate
change.impact = '2'; // Medium
change.priority = '3';
change.planned_start_date = '2024-02-01 02:00:00';
change.planned_end_date = '2024-02-01 06:00:00';
change.assignment_group = 'Data Engineering Team';
change.insert();
```

## 5. Service Catalog
**Catalog Items**:
```yaml
# Data Services Catalog
- New Database Access Request
- Data Pipeline Development
- Report Generation Request
- Data Quality Assessment
- Analytics Dashboard Creation
```

**Catalog Item Configuration**:
```javascript
// Service catalog item
var catalogItem = {
    name: 'Database Access Request',
    category: 'Data Services',
    description: 'Request access to production databases',
    variables: [
        {
            name: 'database_name',
            type: 'string',
            mandatory: true,
            question: 'Which database do you need access to?'
        },
        {
            name: 'access_level',
            type: 'choice',
            choices: ['Read Only', 'Read/Write', 'Admin'],
            question: 'What level of access do you need?'
        },
        {
            name: 'business_justification',
            type: 'string',
            mandatory: true,
            question: 'Business justification for access'
        }
    ]
};
```

## 6. Configuration Management Database (CMDB)
**CI Relationships**:
```yaml
# Configuration Items
- Servers (physical/virtual)
- Applications
- Databases  
- Network devices
- Business services

# Relationship Types
- Runs on (Application → Server)
- Connects to (Application → Database)
- Depends on (Service → Application)
- Contains (Server → CPU/Memory)
```

**CI Record**:
```javascript
// Create CI for data pipeline
var ci = new GlideRecord('cmdb_ci_appl');
ci.initialize();
ci.name = 'Customer Analytics Pipeline';
ci.operational_status = '1'; // Operational
ci.install_status = '1'; // Installed
ci.environment = 'Production';
ci.version = '2.1.0';
ci.owned_by = 'data.team@company.com';
ci.supported_by = 'Data Engineering Team';
ci.insert();
```

## 7. Workflow and Business Rules
**Workflow Example**:
```javascript
// Incident assignment workflow
if (current.assignment_group.changes()) {
    // Send notification to new assignment group
    var notification = new GlideRecord('sysevent_email_action');
    notification.initialize();
    notification.event = 'incident.assigned';
    notification.recipient = current.assignment_group.manager;
    notification.insert();
    
    // Update state to In Progress
    current.state = '2';
    current.update();
}
```

**Business Rule**:
```javascript
// Auto-escalate high priority incidents
(function executeRule(current, previous) {
    if (current.priority == '1' && current.state == '1') {
        // Create escalation task
        var task = new GlideRecord('task');
        task.initialize();
        task.short_description = 'Escalation: ' + current.short_description;
        task.parent = current.sys_id;
        task.assignment_group = 'IT Management';
        task.insert();
        
        // Send notification
        gs.eventQueue('incident.escalated', current, current.assigned_to, current.assignment_group);
    }
})(current, previous);
```

## 8. Reporting and Analytics
**Key Metrics**:
```yaml
# Incident Metrics
- Mean Time to Resolution (MTTR)
- Mean Time to Acknowledge (MTTA)
- First Call Resolution Rate
- Incident Volume by Category

# Change Metrics
- Change Success Rate
- Emergency Change Percentage
- Change Volume Trends
- Implementation Time

# Problem Metrics
- Problem Resolution Time
- Recurring Incident Reduction
- Root Cause Analysis Completion
```

**Custom Report**:
```javascript
// Data team incident report
var report = new GlideAggregate('incident');
report.addQuery('assignment_group.name', 'Data Engineering Team');
report.addQuery('opened_at', '>=', gs.daysAgoStart(30));
report.groupBy('priority');
report.addAggregate('COUNT');
report.query();

while (report.next()) {
    gs.log('Priority ' + report.priority + ': ' + report.getAggregate('COUNT'));
}
```

## 9. Integration and APIs
**REST API Examples**:
```python
import requests
import json

# ServiceNow API configuration
instance = 'company.service-now.com'
username = 'api_user'
password = 'api_password'
headers = {'Content-Type': 'application/json'}

# Create incident
def create_incident(summary, description, priority='3'):
    url = f'https://{instance}/api/now/table/incident'
    data = {
        'short_description': summary,
        'description': description,
        'priority': priority,
        'assignment_group': 'Data Engineering Team'
    }
    response = requests.post(url, auth=(username, password), 
                           headers=headers, data=json.dumps(data))
    return response.json()

# Query incidents
def get_incidents(assignment_group):
    url = f'https://{instance}/api/now/table/incident'
    params = {
        'sysparm_query': f'assignment_group.name={assignment_group}',
        'sysparm_fields': 'number,short_description,state,priority'
    }
    response = requests.get(url, auth=(username, password), params=params)
    return response.json()
```

## 10. Automation and Orchestration
**Flow Designer**:
```yaml
# Automated Incident Response Flow
Trigger: Incident Created (Priority 1)
Actions:
  1. Send SMS to on-call engineer
  2. Create Slack notification
  3. Open conference bridge
  4. Update incident with bridge details
  5. Start timer for escalation
```

**Orchestration Workflow**:
```javascript
// Server provisioning workflow
var workflow = {
    name: 'Provision Database Server',
    steps: [
        {
            name: 'Validate Request',
            type: 'approval',
            approver: 'database.admin@company.com'
        },
        {
            name: 'Create VM',
            type: 'rest_call',
            endpoint: 'https://vmware-api/create-vm',
            method: 'POST'
        },
        {
            name: 'Install Database',
            type: 'ansible_playbook',
            playbook: 'install-postgresql.yml'
        },
        {
            name: 'Update CMDB',
            type: 'script',
            script: 'updateCMDB(server_details)'
        }
    ]
};
```

## 11. Performance Analytics
**KPI Dashboards**:
```yaml
# IT Service Metrics
- Service Availability
- Incident Resolution Time
- Change Success Rate
- Customer Satisfaction Score

# Operational Metrics
- Ticket Volume Trends
- Team Workload Distribution
- SLA Compliance
- Cost per Ticket
```

**Custom Dashboard**:
```javascript
// Data team performance dashboard
var dashboard = {
    title: 'Data Engineering Team Dashboard',
    widgets: [
        {
            type: 'scorecard',
            title: 'Open Incidents',
            query: 'assignment_group.name=Data Engineering Team^state!=6'
        },
        {
            type: 'chart',
            title: 'Incident Trend (30 days)',
            query: 'assignment_group.name=Data Engineering Team^opened_at>=javascript:gs.daysAgoStart(30)'
        },
        {
            type: 'list',
            title: 'High Priority Items',
            query: 'assignment_group.name=Data Engineering Team^priority<=2^state!=6'
        }
    ]
};
```

## 12. Mobile and Self-Service
**Mobile App Features**:
```yaml
# ServiceNow Mobile
- View and update tickets
- Approve requests
- Access knowledge base
- Receive push notifications
- Offline capability

# Self-Service Portal
- Submit requests
- Track ticket status
- Browse service catalog
- Access knowledge articles
- Chat with virtual agent
```

**Virtual Agent Configuration**:
```javascript
// Chatbot for common data requests
var virtualAgent = {
    name: 'Data Helper',
    topics: [
        {
            name: 'Database Access',
            trigger: ['database', 'access', 'permission'],
            response: 'I can help you request database access. What database do you need access to?',
            followUp: 'createDatabaseAccessRequest'
        },
        {
            name: 'Report Issue',
            trigger: ['report', 'dashboard', 'broken'],
            response: 'I can help you report a data issue. Can you describe the problem?',
            followUp: 'createIncident'
        }
    ]
};
```