#!/usr/bin/env python3
"""
AWS Data Engineering Pipeline with Expected Outputs

Demonstrates S3, Glue, Athena, and Lambda integration with clear output examples.
"""

import boto3
import json
from datetime import datetime
import pandas as pd

# AWS Configuration
AWS_REGION = 'us-east-1'
S3_BUCKET = 'my-data-engineering-bucket'
GLUE_DATABASE = 'sales_analytics_db'

# Initialize AWS clients
s3_client = boto3.client('s3', region_name=AWS_REGION)
glue_client = boto3.client('glue', region_name=AWS_REGION)
athena_client = boto3.client('athena', region_name=AWS_REGION)

# =====================================================
# 1. S3 DATA OPERATIONS
# =====================================================

def upload_sample_data():
    """Upload sample sales data to S3."""
    
    # Sample data
    sales_data = [
        {"transaction_id": "TXN_001", "date": "2023-01-15", "customer_id": "CUST_001", "amount": 1299.99, "category": "Electronics"},
        {"transaction_id": "TXN_002", "date": "2023-01-15", "customer_id": "CUST_002", "amount": 89.50, "category": "Clothing"},
        {"transaction_id": "TXN_003", "date": "2023-01-16", "customer_id": "CUST_001", "amount": 599.99, "category": "Electronics"},
        {"transaction_id": "TXN_004", "date": "2023-01-16", "customer_id": "CUST_003", "amount": 29.99, "category": "Books"}
    ]
    
    # Convert to JSON Lines format
    json_data = '\n'.join([json.dumps(record) for record in sales_data])
    
    # Upload to S3
    s3_key = f'raw-data/sales/year=2023/month=01/sales_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=json_data,
            ContentType='application/json'
        )
        print(f"✓ Data uploaded to s3://{S3_BUCKET}/{s3_key}")
        return s3_key
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        return None

def list_s3_objects():
    """List objects in S3 bucket."""
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix='raw-data/')
        
        print("\nS3 Objects:")
        for obj in response.get('Contents', []):
            print(f"  {obj['Key']} ({obj['Size']} bytes, {obj['LastModified']})")
            
        return response.get('Contents', [])
    except Exception as e:
        print(f"✗ List failed: {e}")
        return []

"""
EXPECTED OUTPUT:
✓ Data uploaded to s3://my-data-engineering-bucket/raw-data/sales/year=2023/month=01/sales_data_20231215_103045.json

S3 Objects:
  raw-data/sales/year=2023/month=01/sales_data_20231215_103045.json (312 bytes, 2023-12-15 15:30:45+00:00)
  raw-data/sales/year=2023/month=01/sales_data_20231215_103123.json (312 bytes, 2023-12-15 15:31:23+00:00)
"""

# =====================================================
# 2. AWS GLUE OPERATIONS
# =====================================================

def create_glue_database():
    """Create Glue database for data catalog."""
    try:
        glue_client.create_database(
            DatabaseInput={
                'Name': GLUE_DATABASE,
                'Description': 'Sales analytics database for data engineering pipeline'
            }
        )
        print(f"✓ Created Glue database: {GLUE_DATABASE}")
    except glue_client.exceptions.AlreadyExistsException:
        print(f"✓ Glue database {GLUE_DATABASE} already exists")
    except Exception as e:
        print(f"✗ Database creation failed: {e}")

def create_glue_table():
    """Create Glue table for sales data."""
    table_input = {
        'Name': 'sales_transactions',
        'StorageDescriptor': {
            'Columns': [
                {'Name': 'transaction_id', 'Type': 'string'},
                {'Name': 'date', 'Type': 'string'},
                {'Name': 'customer_id', 'Type': 'string'},
                {'Name': 'amount', 'Type': 'double'},
                {'Name': 'category', 'Type': 'string'}
            ],
            'Location': f's3://{S3_BUCKET}/raw-data/sales/',
            'InputFormat': 'org.apache.hadoop.mapred.TextInputFormat',
            'OutputFormat': 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
            'SerdeInfo': {
                'SerializationLibrary': 'org.openx.data.jsonserde.JsonSerDe'
            }
        },
        'PartitionKeys': [
            {'Name': 'year', 'Type': 'string'},
            {'Name': 'month', 'Type': 'string'}
        ]
    }
    
    try:
        glue_client.create_table(
            DatabaseName=GLUE_DATABASE,
            TableInput=table_input
        )
        print("✓ Created Glue table: sales_transactions")
    except glue_client.exceptions.AlreadyExistsException:
        print("✓ Glue table sales_transactions already exists")
    except Exception as e:
        print(f"✗ Table creation failed: {e}")

"""
EXPECTED OUTPUT:
✓ Created Glue database: sales_analytics_db
✓ Created Glue table: sales_transactions
"""

# =====================================================
# 3. ATHENA QUERIES
# =====================================================

def execute_athena_query(query, output_location):
    """Execute Athena query and return results."""
    try:
        response = athena_client.start_query_execution(
            QueryString=query,
            ResultConfiguration={'OutputLocation': output_location},
            WorkGroup='primary'
        )
        
        query_execution_id = response['QueryExecutionId']
        print(f"✓ Query started: {query_execution_id}")
        
        # Wait for query completion (simplified)
        import time
        while True:
            result = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            status = result['QueryExecution']['Status']['State']
            
            if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                break
            time.sleep(2)
        
        if status == 'SUCCEEDED':
            print(f"✓ Query completed successfully")
            return query_execution_id
        else:
            print(f"✗ Query failed: {status}")
            return None
            
    except Exception as e:
        print(f"✗ Query execution failed: {e}")
        return None

def run_sample_queries():
    """Run sample Athena queries."""
    output_location = f's3://{S3_BUCKET}/athena-results/'
    
    queries = [
        {
            'name': 'Total Sales by Category',
            'sql': f"""
                SELECT category, 
                       COUNT(*) as transaction_count,
                       SUM(amount) as total_amount,
                       AVG(amount) as avg_amount
                FROM {GLUE_DATABASE}.sales_transactions 
                WHERE year = '2023' AND month = '01'
                GROUP BY category 
                ORDER BY total_amount DESC
            """
        },
        {
            'name': 'Daily Sales Summary',
            'sql': f"""
                SELECT date,
                       COUNT(*) as daily_transactions,
                       SUM(amount) as daily_revenue
                FROM {GLUE_DATABASE}.sales_transactions 
                WHERE year = '2023' AND month = '01'
                GROUP BY date 
                ORDER BY date
            """
        }
    ]
    
    for query_info in queries:
        print(f"\nExecuting: {query_info['name']}")
        query_id = execute_athena_query(query_info['sql'], output_location)
        if query_id:
            print(f"Results available at: {output_location}{query_id}.csv")

"""
EXPECTED OUTPUT:

Executing: Total Sales by Category
✓ Query started: 12345678-1234-1234-1234-123456789012
✓ Query completed successfully
Results available at: s3://my-data-engineering-bucket/athena-results/12345678-1234-1234-1234-123456789012.csv

Query Results (Total Sales by Category):
category     | transaction_count | total_amount | avg_amount
-------------|-------------------|--------------|------------
Electronics  |                 2 |      1899.98 |     949.99
Clothing     |                 1 |        89.50 |      89.50
Books        |                 1 |        29.99 |      29.99

Executing: Daily Sales Summary
✓ Query started: 87654321-4321-4321-4321-210987654321
✓ Query completed successfully
Results available at: s3://my-data-engineering-bucket/athena-results/87654321-4321-4321-4321-210987654321.csv

Query Results (Daily Sales Summary):
date       | daily_transactions | daily_revenue
-----------|-------------------|---------------
2023-01-15 |                 2 |       1389.49
2023-01-16 |                 2 |        629.98
"""

# =====================================================
# 4. LAMBDA FUNCTION SIMULATION
# =====================================================

def lambda_data_processor(event, context):
    """Simulate Lambda function for data processing."""
    
    # Parse S3 event
    records_processed = 0
    total_amount = 0.0
    
    for record in event.get('Records', []):
        if record['eventSource'] == 'aws:s3':
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']
            
            print(f"Processing S3 object: s3://{bucket}/{key}")
            
            try:
                # Get object from S3
                response = s3_client.get_object(Bucket=bucket, Key=key)
                content = response['Body'].read().decode('utf-8')
                
                # Process each line
                for line in content.strip().split('\n'):
                    if line:
                        data = json.loads(line)
                        total_amount += data.get('amount', 0)
                        records_processed += 1
                
                print(f"✓ Processed {records_processed} records, total amount: ${total_amount:.2f}")
                
            except Exception as e:
                print(f"✗ Processing failed: {e}")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'records_processed': records_processed,
            'total_amount': total_amount,
            'timestamp': datetime.now().isoformat()
        })
    }

# Simulate Lambda event
sample_s3_event = {
    'Records': [{
        'eventSource': 'aws:s3',
        'eventName': 'ObjectCreated:Put',
        's3': {
            'bucket': {'name': S3_BUCKET},
            'object': {'key': 'raw-data/sales/year=2023/month=01/sales_data_20231215_103045.json'}
        }
    }]
}

"""
EXPECTED OUTPUT:
Processing S3 object: s3://my-data-engineering-bucket/raw-data/sales/year=2023/month=01/sales_data_20231215_103045.json
✓ Processed 4 records, total amount: $2019.47

Lambda Response:
{
  "statusCode": 200,
  "body": "{\"records_processed\": 4, \"total_amount\": 2019.47, \"timestamp\": \"2023-12-15T15:30:45.123456\"}"
}
"""

# =====================================================
# 5. MAIN PIPELINE EXECUTION
# =====================================================

def run_aws_pipeline():
    """Execute complete AWS data pipeline."""
    print("=== AWS DATA ENGINEERING PIPELINE ===")
    
    # Step 1: Upload data to S3
    print("\n1. Uploading data to S3...")
    s3_key = upload_sample_data()
    
    if s3_key:
        # Step 2: List S3 objects
        print("\n2. Listing S3 objects...")
        list_s3_objects()
        
        # Step 3: Create Glue catalog
        print("\n3. Setting up Glue Data Catalog...")
        create_glue_database()
        create_glue_table()
        
        # Step 4: Run Athena queries
        print("\n4. Running Athena queries...")
        run_sample_queries()
        
        # Step 5: Simulate Lambda processing
        print("\n5. Simulating Lambda data processing...")
        result = lambda_data_processor(sample_s3_event, {})
        print(f"Lambda Response: {json.dumps(result, indent=2)}")
        
        print("\n=== PIPELINE COMPLETE ===")
        print("✓ Data uploaded to S3")
        print("✓ Glue catalog configured")
        print("✓ Athena queries executed")
        print("✓ Lambda processing simulated")
    else:
        print("✗ Pipeline failed at S3 upload step")

if __name__ == "__main__":
    # Note: This requires AWS credentials and permissions
    print("AWS Data Pipeline Example")
    print("Note: Requires AWS credentials and appropriate permissions")
    
    # Uncomment to run (requires AWS setup)
    # run_aws_pipeline()
    
    # Show expected output structure
    print("\nExpected Pipeline Flow:")
    print("1. Raw data → S3 (JSON files)")
    print("2. S3 → Glue Catalog (schema discovery)")
    print("3. Glue → Athena (SQL queries)")
    print("4. S3 events → Lambda (real-time processing)")
    print("5. Results → S3/CloudWatch (monitoring)")

"""
COMPLETE EXPECTED OUTPUT:

=== AWS DATA ENGINEERING PIPELINE ===

1. Uploading data to S3...
✓ Data uploaded to s3://my-data-engineering-bucket/raw-data/sales/year=2023/month=01/sales_data_20231215_103045.json

2. Listing S3 objects...

S3 Objects:
  raw-data/sales/year=2023/month=01/sales_data_20231215_103045.json (312 bytes, 2023-12-15 15:30:45+00:00)

3. Setting up Glue Data Catalog...
✓ Created Glue database: sales_analytics_db
✓ Created Glue table: sales_transactions

4. Running Athena queries...

Executing: Total Sales by Category
✓ Query started: 12345678-1234-1234-1234-123456789012
✓ Query completed successfully
Results available at: s3://my-data-engineering-bucket/athena-results/12345678-1234-1234-1234-123456789012.csv

Executing: Daily Sales Summary
✓ Query started: 87654321-4321-4321-4321-210987654321
✓ Query completed successfully
Results available at: s3://my-data-engineering-bucket/athena-results/87654321-4321-4321-4321-210987654321.csv

5. Simulating Lambda data processing...
Processing S3 object: s3://my-data-engineering-bucket/raw-data/sales/year=2023/month=01/sales_data_20231215_103045.json
✓ Processed 4 records, total amount: $2019.47
Lambda Response: {
  "statusCode": 200,
  "body": "{\"records_processed\": 4, \"total_amount\": 2019.47, \"timestamp\": \"2023-12-15T15:30:45.123456\"}"
}

=== PIPELINE COMPLETE ===
✓ Data uploaded to S3
✓ Glue catalog configured  
✓ Athena queries executed
✓ Lambda processing simulated

AWS Services Used:
- S3: Data storage and event triggers
- Glue: Data catalog and ETL
- Athena: Serverless SQL queries
- Lambda: Real-time data processing
- CloudWatch: Monitoring and logging (implied)

Cost Estimate (approximate):
- S3 storage: $0.023/GB/month
- Athena queries: $5/TB scanned
- Lambda: $0.20/1M requests
- Glue: $0.44/DPU-hour
"""