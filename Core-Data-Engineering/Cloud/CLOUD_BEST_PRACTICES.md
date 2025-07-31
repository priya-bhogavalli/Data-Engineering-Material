# Cloud Best Practices for Data Engineering

## 1. Cost Optimization

### Resource Right-Sizing
```python
# AWS EC2 instance optimization
def optimize_ec2_instances():
    """Monitor and optimize EC2 instance usage."""
    
    # Use CloudWatch metrics to analyze utilization
    cloudwatch = boto3.client('cloudwatch')
    
    # Get CPU utilization for instances
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}],
        StartTime=datetime.utcnow() - timedelta(days=7),
        EndTime=datetime.utcnow(),
        Period=3600,
        Statistics=['Average']
    )
    
    # Recommend instance type changes based on utilization
    avg_cpu = sum(point['Average'] for point in response['Datapoints']) / len(response['Datapoints'])
    
    if avg_cpu < 20:
        return "Consider downsizing instance"
    elif avg_cpu > 80:
        return "Consider upsizing instance"
    else:
        return "Instance size is appropriate"

# Storage optimization
def optimize_s3_storage():
    """Implement S3 storage optimization strategies."""
    
    # Lifecycle policy for automatic tiering
    lifecycle_policy = {
        'Rules': [
            {
                'ID': 'DataArchiving',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'data/'},
                'Transitions': [
                    {
                        'Days': 30,
                        'StorageClass': 'STANDARD_IA'
                    },
                    {
                        'Days': 90,
                        'StorageClass': 'GLACIER'
                    },
                    {
                        'Days': 365,
                        'StorageClass': 'DEEP_ARCHIVE'
                    }
                ]
            }
        ]
    }
    
    s3 = boto3.client('s3')
    s3.put_bucket_lifecycle_configuration(
        Bucket='my-data-bucket',
        LifecycleConfiguration=lifecycle_policy
    )
```

### Auto-Scaling Configuration
```yaml
# AWS Auto Scaling Group configuration
AutoScalingGroup:
  Type: AWS::AutoScaling::AutoScalingGroup
  Properties:
    MinSize: 1
    MaxSize: 10
    DesiredCapacity: 2
    TargetGroupARNs:
      - !Ref ApplicationLoadBalancerTargetGroup
    LaunchTemplate:
      LaunchTemplateId: !Ref LaunchTemplate
      Version: !GetAtt LaunchTemplate.LatestVersionNumber
    VPCZoneIdentifier:
      - !Ref PrivateSubnet1
      - !Ref PrivateSubnet2

# Scaling policies
ScaleUpPolicy:
  Type: AWS::AutoScaling::ScalingPolicy
  Properties:
    AdjustmentType: ChangeInCapacity
    AutoScalingGroupName: !Ref AutoScalingGroup
    Cooldown: 300
    ScalingAdjustment: 1

ScaleDownPolicy:
  Type: AWS::AutoScaling::ScalingPolicy
  Properties:
    AdjustmentType: ChangeInCapacity
    AutoScalingGroupName: !Ref AutoScalingGroup
    Cooldown: 300
    ScalingAdjustment: -1
```

## 2. Security Best Practices

### Identity and Access Management
```python
# AWS IAM policy for data engineering roles
def create_data_engineer_policy():
    """Create least-privilege IAM policy for data engineers."""
    
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:DeleteObject"
                ],
                "Resource": [
                    "arn:aws:s3:::data-lake-bucket/*",
                    "arn:aws:s3:::processed-data-bucket/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "glue:GetJob",
                    "glue:StartJobRun",
                    "glue:GetJobRun",
                    "glue:GetJobRuns"
                ],
                "Resource": "arn:aws:glue:*:*:job/data-processing-*"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "rds:DescribeDBInstances",
                    "rds:Connect"
                ],
                "Resource": "arn:aws:rds:*:*:db:data-warehouse"
            }
        ]
    }
    
    return policy_document

# Role-based access with conditions
def create_conditional_policy():
    """Create IAM policy with conditions for enhanced security."""
    
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "s3:*",
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "s3:x-amz-server-side-encryption": "AES256"
                    },
                    "IpAddress": {
                        "aws:SourceIp": ["203.0.113.0/24", "198.51.100.0/24"]
                    },
                    "DateGreaterThan": {
                        "aws:CurrentTime": "2024-01-01T00:00:00Z"
                    }
                }
            }
        ]
    }
    
    return policy_document
```

### Data Encryption
```python
# Encryption at rest and in transit
def setup_encryption():
    """Configure encryption for data at rest and in transit."""
    
    # S3 bucket encryption
    s3 = boto3.client('s3')
    s3.put_bucket_encryption(
        Bucket='my-data-bucket',
        ServerSideEncryptionConfiguration={
            'Rules': [
                {
                    'ApplyServerSideEncryptionByDefault': {
                        'SSEAlgorithm': 'aws:kms',
                        'KMSMasterKeyID': 'arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
                    },
                    'BucketKeyEnabled': True
                }
            ]
        }
    )
    
    # RDS encryption
    rds = boto3.client('rds')
    rds.create_db_instance(
        DBInstanceIdentifier='encrypted-db',
        DBInstanceClass='db.t3.micro',
        Engine='postgres',
        MasterUsername='admin',
        MasterUserPassword='secure-password',
        StorageEncrypted=True,
        KmsKeyId='arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012'
    )

# Application-level encryption
from cryptography.fernet import Fernet

class DataEncryption:
    def __init__(self, key=None):
        if key:
            self.key = key
        else:
            self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def encrypt_data(self, data):
        """Encrypt sensitive data before storage."""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher_suite.encrypt(data)
    
    def decrypt_data(self, encrypted_data):
        """Decrypt data for processing."""
        decrypted_data = self.cipher_suite.decrypt(encrypted_data)
        return decrypted_data.decode()

# Usage
encryptor = DataEncryption()
encrypted_ssn = encryptor.encrypt_data("123-45-6789")
decrypted_ssn = encryptor.decrypt_data(encrypted_ssn)
```

## 3. Performance Optimization

### Data Lake Architecture
```python
# Optimized data lake structure
def setup_data_lake_structure():
    """Create optimized data lake folder structure."""
    
    # Partitioned structure for better query performance
    structure = {
        'raw/': {
            'source_system_1/': {
                'year=2024/': {
                    'month=01/': {
                        'day=01/': 'data files'
                    }
                }
            }
        },
        'processed/': {
            'curated/': {
                'customers/': {
                    'year=2024/': {
                        'month=01/': 'processed customer data'
                    }
                }
            }
        },
        'analytics/': {
            'aggregated/': {
                'daily_sales/': {
                    'year=2024/': {
                        'month=01/': 'aggregated sales data'
                    }
                }
            }
        }
    }
    
    return structure

# Optimized file formats
def optimize_file_formats():
    """Use optimized file formats for better performance."""
    
    # Convert CSV to Parquet for better compression and query performance
    import pandas as pd
    
    # Read CSV
    df = pd.read_csv('large_dataset.csv')
    
    # Write as Parquet with compression
    df.to_parquet(
        'optimized_dataset.parquet',
        compression='snappy',
        index=False
    )
    
    # For Spark
    from pyspark.sql import SparkSession
    
    spark = SparkSession.builder.appName("Optimization").getOrCreate()
    
    # Read and optimize
    df = spark.read.csv('large_dataset.csv', header=True, inferSchema=True)
    
    # Write with optimal partitioning
    df.write \
        .partitionBy('year', 'month') \
        .mode('overwrite') \
        .parquet('s3://optimized-bucket/partitioned-data/')
```

### Caching Strategies
```python
# Redis caching for frequently accessed data
import redis
import json
import pickle
from datetime import timedelta

class DataCache:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
    
    def cache_dataframe(self, key, df, ttl_hours=24):
        """Cache pandas DataFrame with TTL."""
        serialized_df = pickle.dumps(df)
        self.redis_client.setex(
            key,
            timedelta(hours=ttl_hours),
            serialized_df
        )
    
    def get_cached_dataframe(self, key):
        """Retrieve cached DataFrame."""
        cached_data = self.redis_client.get(key)
        if cached_data:
            return pickle.loads(cached_data)
        return None
    
    def cache_query_result(self, query_hash, result, ttl_hours=1):
        """Cache database query results."""
        self.redis_client.setex(
            f"query:{query_hash}",
            timedelta(hours=ttl_hours),
            json.dumps(result, default=str)
        )
    
    def get_cached_query_result(self, query_hash):
        """Retrieve cached query result."""
        cached_result = self.redis_client.get(f"query:{query_hash}")
        if cached_result:
            return json.loads(cached_result)
        return None

# Usage with database queries
import hashlib

def execute_cached_query(query, params=None):
    """Execute query with caching."""
    cache = DataCache()
    
    # Create hash for query and parameters
    query_string = f"{query}_{str(params)}"
    query_hash = hashlib.md5(query_string.encode()).hexdigest()
    
    # Check cache first
    cached_result = cache.get_cached_query_result(query_hash)
    if cached_result:
        return cached_result
    
    # Execute query if not cached
    result = execute_database_query(query, params)
    
    # Cache the result
    cache.cache_query_result(query_hash, result)
    
    return result
```

## 4. Monitoring and Observability

### Comprehensive Monitoring Setup
```python
# CloudWatch custom metrics
import boto3
from datetime import datetime

class DataPipelineMonitoring:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
    
    def put_custom_metric(self, metric_name, value, unit='Count', namespace='DataPipeline'):
        """Send custom metrics to CloudWatch."""
        self.cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Value': value,
                    'Unit': unit,
                    'Timestamp': datetime.utcnow()
                }
            ]
        )
    
    def track_pipeline_execution(self, pipeline_name, execution_time, records_processed, errors=0):
        """Track pipeline execution metrics."""
        metrics = [
            ('ExecutionTime', execution_time, 'Seconds'),
            ('RecordsProcessed', records_processed, 'Count'),
            ('ErrorCount', errors, 'Count')
        ]
        
        for metric_name, value, unit in metrics:
            self.put_custom_metric(
                f"{pipeline_name}_{metric_name}",
                value,
                unit
            )
    
    def create_dashboard(self, dashboard_name):
        """Create CloudWatch dashboard for monitoring."""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["DataPipeline", "ExecutionTime"],
                            [".", "RecordsProcessed"],
                            [".", "ErrorCount"]
                        ],
                        "period": 300,
                        "stat": "Average",
                        "region": "us-east-1",
                        "title": "Pipeline Metrics"
                    }
                }
            ]
        }
        
        self.cloudwatch.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=json.dumps(dashboard_body)
        )

# Alerting setup
def setup_cloudwatch_alarms():
    """Set up CloudWatch alarms for critical metrics."""
    cloudwatch = boto3.client('cloudwatch')
    
    # High error rate alarm
    cloudwatch.put_metric_alarm(
        AlarmName='DataPipeline-HighErrorRate',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=2,
        MetricName='ErrorCount',
        Namespace='DataPipeline',
        Period=300,
        Statistic='Sum',
        Threshold=10.0,
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:us-east-1:123456789012:data-pipeline-alerts'
        ],
        AlarmDescription='Alert when error count exceeds threshold'
    )
    
    # Long execution time alarm
    cloudwatch.put_metric_alarm(
        AlarmName='DataPipeline-LongExecutionTime',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='ExecutionTime',
        Namespace='DataPipeline',
        Period=300,
        Statistic='Average',
        Threshold=3600.0,  # 1 hour
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:us-east-1:123456789012:data-pipeline-alerts'
        ],
        AlarmDescription='Alert when execution time exceeds 1 hour'
    )
```

## 5. Disaster Recovery and Backup

### Multi-Region Backup Strategy
```python
# Cross-region replication setup
def setup_cross_region_replication():
    """Set up cross-region replication for disaster recovery."""
    
    s3 = boto3.client('s3')
    
    # Enable versioning (required for replication)
    s3.put_bucket_versioning(
        Bucket='primary-data-bucket',
        VersioningConfiguration={'Status': 'Enabled'}
    )
    
    # Set up replication configuration
    replication_config = {
        'Role': 'arn:aws:iam::123456789012:role/replication-role',
        'Rules': [
            {
                'ID': 'ReplicateToSecondaryRegion',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'critical-data/'},
                'Destination': {
                    'Bucket': 'arn:aws:s3:::backup-data-bucket',
                    'StorageClass': 'STANDARD_IA'
                }
            }
        ]
    }
    
    s3.put_bucket_replication(
        Bucket='primary-data-bucket',
        ReplicationConfiguration=replication_config
    )

# Database backup automation
def setup_automated_db_backups():
    """Set up automated database backups."""
    
    rds = boto3.client('rds')
    
    # Enable automated backups
    rds.modify_db_instance(
        DBInstanceIdentifier='production-db',
        BackupRetentionPeriod=30,  # 30 days
        PreferredBackupWindow='03:00-04:00',  # UTC
        PreferredMaintenanceWindow='sun:04:00-sun:05:00'
    )
    
    # Create manual snapshot
    rds.create_db_snapshot(
        DBSnapshotIdentifier=f'manual-snapshot-{datetime.now().strftime("%Y%m%d")}',
        DBInstanceIdentifier='production-db'
    )

# Point-in-time recovery testing
def test_point_in_time_recovery():
    """Test point-in-time recovery capabilities."""
    
    rds = boto3.client('rds')
    
    # Restore to point in time
    restore_time = datetime.utcnow() - timedelta(hours=1)
    
    rds.restore_db_instance_to_point_in_time(
        SourceDBInstanceIdentifier='production-db',
        TargetDBInstanceIdentifier='test-restore-db',
        RestoreTime=restore_time,
        DBInstanceClass='db.t3.micro'
    )
```

## 6. Infrastructure as Code

### Terraform Best Practices
```hcl
# terraform/main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "terraform-state-bucket"
    key    = "data-platform/terraform.tfstate"
    region = "us-east-1"
    
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

# Data lake S3 buckets
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake-${var.environment}"
  
  tags = {
    Environment = var.environment
    Project     = "DataPlatform"
    Owner       = "DataEngineering"
  }
}

resource "aws_s3_bucket_versioning" "data_lake_versioning" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_lake_encryption" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.data_lake_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

# KMS key for encryption
resource "aws_kms_key" "data_lake_key" {
  description             = "KMS key for data lake encryption"
  deletion_window_in_days = 7
  
  tags = {
    Environment = var.environment
    Project     = "DataPlatform"
  }
}

# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

These best practices ensure secure, cost-effective, and performant cloud data engineering solutions while maintaining high availability and disaster recovery capabilities.