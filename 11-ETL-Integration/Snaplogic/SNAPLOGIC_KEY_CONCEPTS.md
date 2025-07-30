# SnapLogic Key Concepts

## 1. SnapLogic Platform Overview
**What is SnapLogic**: Cloud-native integration platform for connecting applications, data, and APIs using visual, drag-and-drop interface.

**Core Components**:
- **Designer**: Visual pipeline development environment
- **Manager**: Pipeline management and monitoring
- **Snaps**: Pre-built connectors and transformations
- **Snaplex**: Execution engine (cloud or on-premises)
- **Pipeline**: Data integration workflow

**Architecture**:
```
Data Sources → Snaps → Pipeline → Snaplex → Target Systems
```

## 2. Snaps and Connectors
```json
// Database Read Snap Configuration
{
  "snap_type": "PostgreSQL - Select",
  "settings": {
    "account": "PostgreSQL_Account",
    "sql_statement": "SELECT customer_id, name, email, created_date FROM customers WHERE created_date >= ?",
    "parameters": ["$start_date"],
    "fetch_size": 1000,
    "auto_commit": true
  },
  "output_views": [
    {
      "name": "output0",
      "schema": {
        "customer_id": "INTEGER",
        "name": "STRING",
        "email": "STRING", 
        "created_date": "DATETIME"
      }
    }
  ]
}

// REST API Snap Configuration
{
  "snap_type": "REST Get",
  "settings": {
    "url": "https://api.example.com/customers",
    "headers": {
      "Authorization": "Bearer $api_token",
      "Content-Type": "application/json"
    },
    "query_parameters": {
      "limit": "1000",
      "offset": "$offset"
    },
    "timeout": 30,
    "retry_count": 3
  }
}

// File Reader Snap
{
  "snap_type": "File Reader",
  "settings": {
    "file_path": "/data/input/sales_*.csv",
    "file_format": "CSV",
    "delimiter": ",",
    "header": true,
    "encoding": "UTF-8",
    "quote_character": "\"",
    "escape_character": "\\"
  }
}
```

## 3. Data Transformation
```javascript
// Mapper Snap - Field Mapping
{
  "snap_type": "Mapper",
  "settings": {
    "mappings": [
      {
        "target_path": "$.customer_id",
        "expression": "$customer_id"
      },
      {
        "target_path": "$.full_name", 
        "expression": "$first_name + ' ' + $last_name"
      },
      {
        "target_path": "$.email_domain",
        "expression": "$email.split('@')[1]"
      },
      {
        "target_path": "$.registration_year",
        "expression": "Date.parse($created_date).getFullYear()"
      },
      {
        "target_path": "$.customer_tier",
        "expression": "$total_spent >= 10000 ? 'PREMIUM' : ($total_spent >= 5000 ? 'GOLD' : 'STANDARD')"
      }
    ]
  }
}

// Filter Snap
{
  "snap_type": "Filter",
  "settings": {
    "filter_expression": "$amount > 0 && $customer_id != null && $email.contains('@')",
    "pass_through": false
  }
}

// Aggregate Snap
{
  "snap_type": "Aggregate",
  "settings": {
    "group_by": ["customer_id", "product_category"],
    "aggregations": [
      {
        "field": "amount",
        "operation": "SUM",
        "alias": "total_spent"
      },
      {
        "field": "order_id",
        "operation": "COUNT",
        "alias": "order_count"
      },
      {
        "field": "amount",
        "operation": "AVG",
        "alias": "avg_order_value"
      },
      {
        "field": "order_date",
        "operation": "MAX",
        "alias": "last_order_date"
      }
    ]
  }
}

// Sort Snap
{
  "snap_type": "Sort",
  "settings": {
    "sort_fields": [
      {
        "field": "total_spent",
        "order": "DESC"
      },
      {
        "field": "customer_id",
        "order": "ASC"
      }
    ]
  }
}
```

## 4. Data Quality and Validation
```javascript
// Data Validator Snap
{
  "snap_type": "Data Validator",
  "settings": {
    "validations": [
      {
        "field": "email",
        "validation_type": "REGEX",
        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
        "error_message": "Invalid email format"
      },
      {
        "field": "amount",
        "validation_type": "RANGE",
        "min_value": 0,
        "max_value": 100000,
        "error_message": "Amount must be between 0 and 100000"
      },
      {
        "field": "customer_id",
        "validation_type": "NOT_NULL",
        "error_message": "Customer ID is required"
      }
    ],
    "error_handling": "ROUTE_TO_ERROR_VIEW"
  },
  "output_views": [
    {
      "name": "valid_output",
      "description": "Valid records"
    },
    {
      "name": "error_output", 
      "description": "Invalid records with error details"
    }
  ]
}

// Duplicate Detection
{
  "snap_type": "Duplicate Detection",
  "settings": {
    "key_fields": ["customer_id", "email"],
    "duplicate_handling": "KEEP_FIRST",
    "case_sensitive": false
  }
}

// Data Cleansing
{
  "snap_type": "Mapper",
  "settings": {
    "mappings": [
      {
        "target_path": "$.clean_name",
        "expression": "$name.trim().replace(/\\s+/g, ' ')"
      },
      {
        "target_path": "$.clean_email",
        "expression": "$email.toLowerCase().trim()"
      },
      {
        "target_path": "$.clean_phone",
        "expression": "$phone.replace(/[^0-9]/g, '')"
      },
      {
        "target_path": "$.standardized_country",
        "expression": "$country.toUpperCase() === 'USA' ? 'US' : ($country.toUpperCase() === 'UNITED KINGDOM' ? 'UK' : $country)"
      }
    ]
  }
}
```

## 5. Error Handling and Logging
```json
// Pipeline Error Handling
{
  "pipeline_settings": {
    "error_handling": {
      "global_error_handler": true,
      "error_snap_settings": {
        "snap_type": "File Writer",
        "settings": {
          "file_path": "/logs/errors/pipeline_errors_${date}.json",
          "file_format": "JSON"
        }
      }
    },
    "logging": {
      "log_level": "INFO",
      "log_to_file": true,
      "log_file_path": "/logs/pipeline_${pipeline_name}_${date}.log"
    }
  }
}

// Try-Catch Pattern
{
  "snap_type": "Pipeline Execute",
  "settings": {
    "pipeline_path": "/shared/data_processing_pipeline",
    "parameters": {
      "input_file": "$input_file",
      "processing_date": "$processing_date"
    },
    "error_handling": {
      "on_error": "CONTINUE",
      "error_pipeline": "/shared/error_notification_pipeline"
    }
  }
}

// Custom Error Handling with Script Snap
{
  "snap_type": "Script",
  "settings": {
    "language": "JavaScript",
    "script": `
      try {
        // Main processing logic
        var processedData = processRecord(input);
        output.write(processedData);
      } catch (error) {
        // Log error details
        var errorRecord = {
          original_record: input,
          error_message: error.message,
          error_timestamp: new Date().toISOString(),
          pipeline_name: snaplogic.pipeline_name
        };
        
        error_output.write(errorRecord);
      }
      
      function processRecord(record) {
        // Validation
        if (!record.customer_id) {
          throw new Error('Customer ID is required');
        }
        
        if (record.amount <= 0) {
          throw new Error('Amount must be positive');
        }
        
        // Processing
        return {
          ...record,
          processed: true,
          processed_at: new Date().toISOString()
        };
      }
    `
  }
}
```

## 6. Scheduling and Triggers
```json
// Scheduled Pipeline
{
  "schedule_settings": {
    "schedule_type": "CRON",
    "cron_expression": "0 2 * * *",  // Daily at 2 AM
    "timezone": "America/New_York",
    "enabled": true,
    "parameters": {
      "processing_date": "${date:yyyy-MM-dd}",
      "batch_id": "${uuid}"
    }
  }
}

// File Trigger
{
  "trigger_settings": {
    "trigger_type": "FILE_WATCHER",
    "watch_directory": "/data/incoming/",
    "file_pattern": "sales_*.csv",
    "trigger_action": "EXECUTE_PIPELINE",
    "pipeline_path": "/shared/file_processing_pipeline",
    "parameters": {
      "input_file": "${trigger.file_path}",
      "file_name": "${trigger.file_name}"
    }
  }
}

// API Trigger (Webhook)
{
  "trigger_settings": {
    "trigger_type": "WEBHOOK",
    "endpoint_url": "/api/trigger/data-pipeline",
    "authentication": {
      "type": "API_KEY",
      "api_key_header": "X-API-Key"
    },
    "pipeline_parameters": {
      "source_system": "${webhook.body.source}",
      "data_type": "${webhook.body.type}",
      "priority": "${webhook.body.priority}"
    }
  }
}

// Database Trigger
{
  "trigger_settings": {
    "trigger_type": "DATABASE_CHANGE",
    "database_account": "PostgreSQL_Account",
    "table_name": "customer_updates",
    "trigger_condition": "INSERT OR UPDATE",
    "polling_interval": 300,  // 5 minutes
    "pipeline_parameters": {
      "changed_records": "${trigger.changed_data}"
    }
  }
}
```

## 7. Advanced Pipeline Patterns
```json
// Parent-Child Pipeline Pattern
{
  "parent_pipeline": {
    "name": "Master_Data_Processing",
    "snaps": [
      {
        "snap_type": "File Reader",
        "settings": {
          "file_path": "/data/input/manifest.json"
        }
      },
      {
        "snap_type": "JSON Splitter",
        "settings": {
          "split_path": "$.files[*]"
        }
      },
      {
        "snap_type": "Pipeline Execute",
        "settings": {
          "pipeline_path": "/shared/child_file_processor",
          "execution_mode": "PARALLEL",
          "max_concurrent": 5,
          "parameters": {
            "file_path": "$file_path",
            "file_type": "$file_type"
          }
        }
      }
    ]
  }
}

// Conditional Processing
{
  "snap_type": "Router",
  "settings": {
    "routes": [
      {
        "route_name": "high_priority",
        "condition": "$priority === 'HIGH'",
        "target_pipeline": "/shared/high_priority_processor"
      },
      {
        "route_name": "standard_priority", 
        "condition": "$priority === 'STANDARD'",
        "target_pipeline": "/shared/standard_processor"
      },
      {
        "route_name": "batch_processing",
        "condition": "$batch_size > 1000",
        "target_pipeline": "/shared/batch_processor"
      }
    ],
    "default_route": "/shared/default_processor"
  }
}

// Loop Processing
{
  "snap_type": "For Each",
  "settings": {
    "iteration_path": "$.customers[*]",
    "child_pipeline": "/shared/customer_processor",
    "parameters": {
      "customer_data": "$",
      "processing_batch": "${parent.batch_id}"
    },
    "parallel_execution": true,
    "max_parallel": 10
  }
}

// Data Synchronization Pattern
{
  "sync_pipeline": {
    "source_snap": {
      "snap_type": "Salesforce - SOQL",
      "settings": {
        "query": "SELECT Id, Name, Email, LastModifiedDate FROM Contact WHERE LastModifiedDate >= YESTERDAY"
      }
    },
    "target_snap": {
      "snap_type": "PostgreSQL - Upsert",
      "settings": {
        "table": "contacts",
        "key_columns": ["salesforce_id"],
        "update_columns": ["name", "email", "last_modified"],
        "insert_columns": ["salesforce_id", "name", "email", "created_date", "last_modified"]
      }
    }
  }
}
```

## 8. Performance Optimization
```json
// Batch Processing Configuration
{
  "snap_type": "PostgreSQL - Bulk Load",
  "settings": {
    "table": "sales_data",
    "batch_size": 10000,
    "commit_interval": 5000,
    "parallel_threads": 4,
    "load_method": "COPY",
    "error_handling": "CONTINUE_ON_ERROR",
    "max_errors": 100
  }
}

// Memory Management
{
  "pipeline_settings": {
    "execution_mode": "STREAMING",
    "buffer_size": 1000,
    "memory_limit": "2GB",
    "disk_spillover": true,
    "spillover_directory": "/tmp/snaplogic_spillover"
  }
}

// Parallel Processing
{
  "snap_type": "Splitter",
  "settings": {
    "split_condition": "ROUND_ROBIN",
    "number_of_outputs": 4
  },
  "followed_by": [
    {
      "snap_type": "Pipeline Execute",
      "settings": {
        "pipeline_path": "/shared/parallel_processor",
        "execution_mode": "PARALLEL"
      }
    }
  ]
}

// Caching Strategy
{
  "snap_type": "Lookup",
  "settings": {
    "lookup_source": {
      "snap_type": "PostgreSQL - Select",
      "settings": {
        "sql": "SELECT product_id, product_name, category FROM products"
      }
    },
    "cache_settings": {
      "enable_cache": true,
      "cache_size": 10000,
      "cache_ttl": 3600,  // 1 hour
      "cache_refresh": "LAZY"
    },
    "lookup_key": "product_id",
    "return_fields": ["product_name", "category"]
  }
}
```

## 9. Monitoring and Analytics
```json
// Pipeline Monitoring Configuration
{
  "monitoring_settings": {
    "enable_metrics": true,
    "metrics_collection": {
      "record_count": true,
      "processing_time": true,
      "error_count": true,
      "throughput": true,
      "memory_usage": true
    },
    "alerts": [
      {
        "alert_type": "ERROR_THRESHOLD",
        "threshold": 10,
        "notification": {
          "type": "EMAIL",
          "recipients": ["admin@company.com"],
          "subject": "Pipeline Error Alert: ${pipeline_name}"
        }
      },
      {
        "alert_type": "EXECUTION_TIME",
        "threshold": 3600,  // 1 hour
        "notification": {
          "type": "SLACK",
          "webhook_url": "https://hooks.slack.com/...",
          "message": "Pipeline ${pipeline_name} exceeded execution time limit"
        }
      }
    ]
  }
}

// Custom Metrics Collection
{
  "snap_type": "Script",
  "settings": {
    "language": "JavaScript",
    "script": `
      // Collect custom metrics
      var metrics = {
        pipeline_name: snaplogic.pipeline_name,
        execution_id: snaplogic.execution_id,
        start_time: new Date().toISOString(),
        records_processed: 0,
        errors_encountered: 0,
        business_metrics: {
          total_sales: 0,
          unique_customers: new Set(),
          high_value_transactions: 0
        }
      };
      
      while (input.hasNext()) {
        var record = input.next();
        metrics.records_processed++;
        
        try {
          // Business logic processing
          if (record.amount > 1000) {
            metrics.business_metrics.high_value_transactions++;
          }
          
          metrics.business_metrics.total_sales += record.amount;
          metrics.business_metrics.unique_customers.add(record.customer_id);
          
          output.write(record);
        } catch (error) {
          metrics.errors_encountered++;
          error_output.write({
            record: record,
            error: error.message
          });
        }
      }
      
      // Convert Set to count for JSON serialization
      metrics.business_metrics.unique_customers = metrics.business_metrics.unique_customers.size;
      metrics.end_time = new Date().toISOString();
      
      // Send metrics to monitoring system
      metrics_output.write(metrics);
    `
  }
}
```

## 10. Security and Governance
```json
// Account Management
{
  "account_settings": {
    "account_type": "Database",
    "connection_details": {
      "host": "${vault.db_host}",
      "port": 5432,
      "database": "${vault.db_name}",
      "username": "${vault.db_username}",
      "password": "${vault.db_password}"
    },
    "security": {
      "ssl_enabled": true,
      "certificate_validation": true,
      "connection_timeout": 30,
      "max_connections": 10
    }
  }
}

// Data Masking
{
  "snap_type": "Mapper",
  "settings": {
    "mappings": [
      {
        "target_path": "$.customer_id",
        "expression": "$customer_id"
      },
      {
        "target_path": "$.masked_email",
        "expression": "$email.substring(0, 3) + '***@' + $email.split('@')[1]"
      },
      {
        "target_path": "$.masked_phone",
        "expression": "'***-***-' + $phone.substring($phone.length - 4)"
      },
      {
        "target_path": "$.masked_ssn",
        "expression": "'***-**-' + $ssn.substring($ssn.length - 4)"
      }
    ]
  }
}

// Access Control
{
  "pipeline_permissions": {
    "owner": "data_engineering_team",
    "permissions": [
      {
        "user_group": "data_analysts",
        "access_level": "READ"
      },
      {
        "user_group": "data_engineers", 
        "access_level": "READ_WRITE"
      },
      {
        "user_group": "administrators",
        "access_level": "FULL_CONTROL"
      }
    ],
    "execution_permissions": {
      "allowed_environments": ["DEV", "TEST", "PROD"],
      "approval_required": {
        "PROD": true,
        "approvers": ["senior_engineer", "team_lead"]
      }
    }
  }
}

// Audit Logging
{
  "audit_settings": {
    "enable_audit_log": true,
    "log_events": [
      "PIPELINE_EXECUTION",
      "DATA_ACCESS",
      "CONFIGURATION_CHANGE",
      "USER_LOGIN",
      "PERMISSION_CHANGE"
    ],
    "audit_destination": {
      "type": "DATABASE",
      "connection": "audit_db_account",
      "table": "snaplogic_audit_log"
    },
    "retention_policy": {
      "retention_days": 365,
      "archive_after_days": 90
    }
  }
}

// Data Lineage Tracking
{
  "lineage_settings": {
    "enable_lineage": true,
    "track_field_level": true,
    "lineage_metadata": {
      "source_system": "$source_system_name",
      "data_classification": "$data_classification",
      "business_owner": "$business_owner",
      "technical_owner": "$technical_owner"
    },
    "lineage_export": {
      "format": "JSON",
      "destination": "/shared/lineage/pipeline_lineage.json"
    }
  }
}
```