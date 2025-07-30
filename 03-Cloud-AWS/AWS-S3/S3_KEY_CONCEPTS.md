# AWS S3 Key Concepts

## 1. S3 Fundamentals
**What is S3**: Object storage service with unlimited capacity and 99.999999999% durability.

**Key Concepts**:
- **Buckets**: Containers for objects (globally unique names)
- **Objects**: Files stored in buckets (up to 5TB each)
- **Keys**: Unique identifiers for objects within buckets
- **Regions**: Geographic locations for data storage

```python
import boto3

s3 = boto3.client('s3')
s3_resource = boto3.resource('s3')
```

## 2. Bucket Operations
```python
# Create bucket
s3.create_bucket(
    Bucket='my-data-lake-bucket',
    CreateBucketConfiguration={'LocationConstraint': 'us-west-2'}
)

# List buckets
response = s3.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'])

# Delete bucket
s3.delete_bucket(Bucket='my-bucket')

# Bucket policies
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"AWS": "arn:aws:iam::123456789012:user/DataEngineer"},
        "Action": "s3:GetObject",
        "Resource": "arn:aws:s3:::my-bucket/*"
    }]
}

s3.put_bucket_policy(
    Bucket='my-bucket',
    Policy=json.dumps(bucket_policy)
)
```

## 3. Object Operations
```python
# Upload object
s3.put_object(
    Bucket='my-bucket',
    Key='data/sales/2024/sales.csv',
    Body=open('sales.csv', 'rb'),
    ContentType='text/csv'
)

# Upload with metadata
s3.put_object(
    Bucket='my-bucket',
    Key='processed/data.parquet',
    Body=data,
    Metadata={
        'processed-date': '2024-01-15',
        'source': 'daily-etl'
    }
)

# Download object
s3.download_file('my-bucket', 'data/file.csv', 'local_file.csv')

# Get object
response = s3.get_object(Bucket='my-bucket', Key='data/file.json')
content = response['Body'].read()

# List objects
response = s3.list_objects_v2(
    Bucket='my-bucket',
    Prefix='data/2024/',
    MaxKeys=1000
)
```

## 4. Storage Classes
```python
# Standard storage (default)
s3.put_object(
    Bucket='my-bucket',
    Key='active-data.csv',
    Body=data,
    StorageClass='STANDARD'
)

# Infrequent Access
s3.put_object(
    Bucket='my-bucket',
    Key='archive-data.csv',
    Body=data,
    StorageClass='STANDARD_IA'
)

# Glacier for long-term archival
s3.put_object(
    Bucket='my-bucket',
    Key='historical-data.csv',
    Body=data,
    StorageClass='GLACIER'
)

# Intelligent Tiering
s3.put_object(
    Bucket='my-bucket',
    Key='variable-access-data.csv',
    Body=data,
    StorageClass='INTELLIGENT_TIERING'
)
```

## 5. Lifecycle Management
```python
lifecycle_config = {
    'Rules': [{
        'ID': 'DataLakeLifecycle',
        'Status': 'Enabled',
        'Filter': {'Prefix': 'raw-data/'},
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
        ],
        'Expiration': {'Days': 2555}  # 7 years
    }]
}

s3.put_bucket_lifecycle_configuration(
    Bucket='my-data-lake',
    LifecycleConfiguration=lifecycle_config
)
```

## 6. Versioning and Replication
```python
# Enable versioning
s3.put_bucket_versioning(
    Bucket='my-bucket',
    VersioningConfiguration={'Status': 'Enabled'}
)

# Cross-region replication
replication_config = {
    'Role': 'arn:aws:iam::123456789012:role/replication-role',
    'Rules': [{
        'ID': 'ReplicateToBackup',
        'Status': 'Enabled',
        'Filter': {'Prefix': 'important-data/'},
        'Destination': {
            'Bucket': 'arn:aws:s3:::backup-bucket',
            'StorageClass': 'STANDARD_IA'
        }
    }]
}

s3.put_bucket_replication(
    Bucket='my-bucket',
    ReplicationConfiguration=replication_config
)
```

## 7. Security and Access Control
```python
# Server-side encryption
s3.put_object(
    Bucket='my-bucket',
    Key='sensitive-data.csv',
    Body=data,
    ServerSideEncryption='AES256'
)

# KMS encryption
s3.put_object(
    Bucket='my-bucket',
    Key='encrypted-data.csv',
    Body=data,
    ServerSideEncryption='aws:kms',
    SSEKMSKeyId='arn:aws:kms:us-west-2:123456789012:key/12345678-1234-1234-1234-123456789012'
)

# Pre-signed URLs
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket', 'Key': 'data.csv'},
    ExpiresIn=3600  # 1 hour
)
```

## 8. Event Notifications
```python
# Lambda trigger configuration
notification_config = {
    'LambdaConfigurations': [{
        'Id': 'ProcessNewFiles',
        'LambdaFunctionArn': 'arn:aws:lambda:us-west-2:123456789012:function:ProcessS3File',
        'Events': ['s3:ObjectCreated:*'],
        'Filter': {
            'Key': {
                'FilterRules': [{
                    'Name': 'prefix',
                    'Value': 'incoming/'
                }, {
                    'Name': 'suffix',
                    'Value': '.csv'
                }]
            }
        }
    }]
}

s3.put_bucket_notification_configuration(
    Bucket='my-bucket',
    NotificationConfiguration=notification_config
)
```

## 9. Data Lake Patterns
```python
# Partitioned data structure
def upload_partitioned_data(df, bucket, base_key):
    """Upload data with date partitioning"""
    for date in df['date'].unique():
        partition_key = f"{base_key}/year={date.year}/month={date.month:02d}/day={date.day:02d}/data.parquet"
        partition_data = df[df['date'] == date]
        
        s3.put_object(
            Bucket=bucket,
            Key=partition_key,
            Body=partition_data.to_parquet()
        )

# Multi-format storage
def store_in_multiple_formats(data, bucket, key_prefix):
    """Store same data in different formats"""
    formats = {
        'csv': data.to_csv(),
        'json': data.to_json(),
        'parquet': data.to_parquet()
    }
    
    for format_type, content in formats.items():
        s3.put_object(
            Bucket=bucket,
            Key=f"{key_prefix}.{format_type}",
            Body=content
        )
```

## 10. Performance Optimization
```python
# Multipart upload for large files
def multipart_upload(bucket, key, file_path):
    """Upload large files in parts"""
    multipart = s3.create_multipart_upload(Bucket=bucket, Key=key)
    upload_id = multipart['UploadId']
    
    parts = []
    part_size = 100 * 1024 * 1024  # 100MB
    
    with open(file_path, 'rb') as f:
        part_number = 1
        while True:
            data = f.read(part_size)
            if not data:
                break
                
            response = s3.upload_part(
                Bucket=bucket,
                Key=key,
                PartNumber=part_number,
                UploadId=upload_id,
                Body=data
            )
            
            parts.append({
                'ETag': response['ETag'],
                'PartNumber': part_number
            })
            part_number += 1
    
    s3.complete_multipart_upload(
        Bucket=bucket,
        Key=key,
        UploadId=upload_id,
        MultipartUpload={'Parts': parts}
    )

# Transfer acceleration
s3_accelerated = boto3.client(
    's3',
    config=boto3.session.Config(
        s3={'use_accelerate_endpoint': True}
    )
)

# Batch operations
def batch_copy_objects(source_bucket, dest_bucket, keys):
    """Copy multiple objects efficiently"""
    for key in keys:
        copy_source = {'Bucket': source_bucket, 'Key': key}
        s3.copy_object(
            CopySource=copy_source,
            Bucket=dest_bucket,
            Key=key
        )
```