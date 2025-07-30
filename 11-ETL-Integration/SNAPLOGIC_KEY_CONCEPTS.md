# SnapLogic Key Concepts

## 1. Integration Platform as a Service (iPaaS)
**What it is**: Cloud-based integration platform for connecting applications, data, and APIs across on-premises and cloud environments.

**Core Components**:
- **Designer**: Visual pipeline development interface
- **Manager**: Pipeline management and monitoring
- **Snaplex**: Execution engine for running pipelines
- **Snaps**: Pre-built connectors and transformations

## 2. Snaps and Snap Packs
**What are Snaps**: Pre-built connectors that perform specific integration tasks.

**Common Snap Categories**:
```yaml
# Database Snaps
- MySQL Select/Insert/Update/Delete
- PostgreSQL Select/Insert/Update/Delete
- Oracle Select/Insert/Update/Delete
- SQL Server Select/Insert/Update/Delete

# Cloud Storage Snaps
- Amazon S3 Read/Write
- Azure Blob Read/Write
- Google Cloud Storage Read/Write

# File Snaps
- File Reader/Writer
- CSV Parser/Formatter
- JSON Parser/Formatter
- XML Parser/Formatter

# Transform Snaps
- Mapper
- Filter
- Sort
- Join
- Aggregate
- Union
```

**Snap Configuration Example**:
```json
{
  "class_id": "com.snaplogic.snaps.mysql.select",
  "class_version": 1,
  "instance_id": "mysql_select_1",
  "property_map": {
    "account": "MySQL_Account",
    "sql": "SELECT customer_id, name, email FROM customers WHERE created_date >= ?",
    "parameters": ["$start_date"],
    "fetch_size": 1000,
    "auto_commit": true
  }
}
```

## 3. Pipelines
**Pipeline Structure**:
```yaml
# Basic ETL Pipeline
Extract (Source) → Transform (Mapper/Filter) → Load (Target)

# Example: Customer Data Pipeline
File Reader → CSV Parser → Mapper → Filter → Database Insert
```

**Pipeline Configuration**:
```json
{
  "pipeline_name": "Customer_Data_ETL",
  "description": "Extract customer data from CSV and load to database",
  "parameters": {
    "input_file_path": "/data/customers.csv",
    "target_table": "customers",
    "batch_size": 1000
  },
  "error_handling": {
    "error_view": "error_output",
    "continue_on_error": true
  }
}
```

## 4. Data Mapping and Transformation
**Mapper Snap Configuration**:
```json
{
  "mappings": [
    {
      "source": "$customer_id",
      "target": "id",
      "type": "integer"
    },
    {
      "source": "$first_name + ' ' + $last_name",
      "target": "full_name",
      "type": "string"
    },
    {
      "source": "$email.toLowerCase()",
      "target": "email",
      "type": "string"
    },
    {
      "source": "Date.now()",
      "target": "processed_date",
      "type": "datetime"
    }
  ]
}
```

**Expression Language**:
```javascript
// String operations
$customer_name.toUpperCase()
$email.toLowerCase()
$phone.replace(/[^0-9]/g, '')

// Date operations
Date.now()
Date.parse($date_string)
$date_field.getYear()

// Conditional logic
$status == 'active' ? 'ACTIVE' : 'INACTIVE'
$amount > 1000 ? 'HIGH' : 'LOW'

// Array operations
$items.length
$items[0]
$items.filter(x => x.status == 'active')
```

## 5. Error Handling
**Error View Configuration**:
```json
{
  "error_handling": {
    "error_view_enabled": true,
    "error_view_name": "error_output",
    "error_actions": [
      {
        "condition": "error_type == 'validation'",
        "action": "route_to_error_file"
      },
      {
        "condition": "error_type == 'connection'",
        "action": "retry",
        "retry_count": 3,
        "retry_interval": 30
      }
    ]
  }
}
```

**Try-Catch Pattern**:
```yaml
# Pipeline with error handling
Main Flow:
  Source → Transform → Target
  
Error Flow:
  Error View → Error Logger → Error File Writer
```

## 6. Snaplex (Execution Engine)
**Snaplex Types**:
```yaml
# Cloudplex (SnapLogic-managed)
- Hosted in SnapLogic cloud
- Automatic scaling and maintenance
- Suitable for cloud-to-cloud integrations

# Groundplex (Customer-managed)
- Deployed on-premises or in customer cloud
- Full control over resources
- Required for on-premises data access

# FeedMaster (High-volume processing)
- Optimized for large data volumes
- Parallel processing capabilities
- Suitable for big data scenarios
```

**Snaplex Configuration**:
```json
{
  "snaplex_name": "Production_Groundplex",
  "node_count": 4,
  "memory_per_node": "8GB",
  "cpu_per_node": 4,
  "network_config": {
    "vpc_id": "vpc-12345678",
    "subnet_ids": ["subnet-12345678", "subnet-87654321"],
    "security_groups": ["sg-12345678"]
  }
}
```

## 7. Scheduling and Monitoring
**Task Scheduling**:
```json
{
  "schedule": {
    "type": "cron",
    "expression": "0 2 * * *",
    "timezone": "America/New_York"
  },
  "parameters": {
    "start_date": "@{Date.now() - 86400000}",
    "end_date": "@{Date.now()}"
  }
}
```

**Pipeline Monitoring**:
```json
{
  "monitoring": {
    "alerts": [
      {
        "condition": "execution_status == 'FAILED'",
        "notification": {
          "type": "email",
          "recipients": ["admin@company.com"],
          "subject": "Pipeline Failed: Customer_Data_ETL"
        }
      },
      {
        "condition": "execution_time > 3600",
        "notification": {
          "type": "slack",
          "webhook": "https://hooks.slack.com/...",
          "message": "Pipeline taking longer than expected"
        }
      }
    ]
  }
}
```

## 8. API Management
**REST API Snap Configuration**:
```json
{
  "rest_get": {
    "url": "https://api.example.com/customers",
    "headers": {
      "Authorization": "Bearer $api_token",
      "Content-Type": "application/json"
    },
    "query_parameters": {
      "limit": 1000,
      "offset": "$offset"
    },
    "pagination": {
      "type": "offset",
      "offset_field": "offset",
      "limit_field": "limit",
      "total_field": "total"
    }
  }
}
```

**API Response Handling**:
```json
{
  "response_mapping": {
    "data_path": "$.data",
    "mappings": [
      {
        "source": "$.id",
        "target": "customer_id"
      },
      {
        "source": "$.attributes.name",
        "target": "customer_name"
      },
      {
        "source": "$.attributes.email",
        "target": "email"
      }
    ]
  }
}
```

## 9. Data Quality and Validation
**Validation Rules**:
```json
{
  "validation_rules": [
    {
      "field": "email",
      "rule": "regex",
      "pattern": "^[\\w\\.-]+@[\\w\\.-]+\\.[a-zA-Z]{2,}$",
      "error_message": "Invalid email format"
    },
    {
      "field": "age",
      "rule": "range",
      "min": 0,
      "max": 120,
      "error_message": "Age must be between 0 and 120"
    },
    {
      "field": "customer_id",
      "rule": "not_null",
      "error_message": "Customer ID is required"
    }
  ]
}
```

**Data Profiling**:
```json
{
  "profiling": {
    "enabled": true,
    "metrics": [
      "record_count",
      "null_count",
      "unique_count",
      "min_value",
      "max_value",
      "avg_value"
    ],
    "output_location": "s3://data-quality/profiles/"
  }
}
```

## 10. Security and Compliance
**Account Management**:
```json
{
  "database_account": {
    "account_name": "MySQL_Production",
    "connection_string": "jdbc:mysql://prod-db:3306/sales",
    "username": "$db_username",
    "password": "$db_password",
    "encryption": "SSL",
    "connection_pool": {
      "min_connections": 5,
      "max_connections": 20,
      "timeout": 30
    }
  }
}
```

**Data Encryption**:
```json
{
  "encryption": {
    "at_rest": {
      "enabled": true,
      "algorithm": "AES-256",
      "key_management": "AWS_KMS"
    },
    "in_transit": {
      "enabled": true,
      "protocol": "TLS_1.2"
    }
  }
}
```

**Audit Logging**:
```json
{
  "audit_config": {
    "enabled": true,
    "log_level": "INFO",
    "events": [
      "pipeline_start",
      "pipeline_complete",
      "pipeline_error",
      "data_access",
      "account_usage"
    ],
    "retention_days": 90,
    "export_location": "s3://audit-logs/"
  }
}
```

## 11. Performance Optimization
**Pipeline Optimization**:
```json
{
  "performance_settings": {
    "batch_size": 10000,
    "parallel_processing": true,
    "thread_count": 4,
    "memory_allocation": "2GB",
    "connection_pooling": true,
    "compression": {
      "enabled": true,
      "algorithm": "gzip"
    }
  }
}
```

**Resource Management**:
```json
{
  "resource_limits": {
    "max_memory": "4GB",
    "max_cpu": "2 cores",
    "timeout": 3600,
    "retry_policy": {
      "max_retries": 3,
      "retry_interval": 60,
      "exponential_backoff": true
    }
  }
}
```