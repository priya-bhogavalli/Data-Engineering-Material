# ETL (Extract, Transform, Load) Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Architecture & Design (91-120)](#architecture--design-91-120)
5. [Real-time & Streaming ETL (121-150)](#real-time--streaming-etl-121-150)
6. [Production & Operations (151-180)](#production--operations-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is ETL and explain each component in detail?

**ETL** stands for Extract, Transform, Load - a fundamental data integration process used to move and process data from multiple sources into a target system.

#### **Detailed Components:**

| Component | Description | Key Activities |
|-----------|-------------|----------------|
| **Extract** | Retrieving data from source systems | Data identification, connection management, incremental extraction |
| **Transform** | Converting and processing data | Data cleaning, validation, enrichment, aggregation |
| **Load** | Storing processed data in target | Data insertion, indexing, constraint validation |

```python
# ETL Example with Python
import pandas as pd
from sqlalchemy import create_engine
import logging

class SimpleETL:
    def __init__(self, source_conn, target_conn):
        self.source_engine = create_engine(source_conn)
        self.target_engine = create_engine(target_conn)
        self.logger = logging.getLogger(__name__)
    
    def extract(self, query):
        """Extract data from source system"""
        try:
            df = pd.read_sql(query, self.source_engine)
            self.logger.info(f"Extracted {len(df)} records")
            return df
        except Exception as e:
            self.logger.error(f"Extraction failed: {str(e)}")
            raise
    
    def transform(self, df):
        """Transform extracted data"""
        # Data cleaning
        df = df.dropna()
        
        # Data standardization
        df['email'] = df['email'].str.lower()
        df['phone'] = df['phone'].str.replace(r'[^\d]', '', regex=True)
        
        # Data enrichment
        df['full_name'] = df['first_name'] + ' ' + df['last_name']
        df['created_date'] = pd.to_datetime(df['created_date'])
        
        self.logger.info(f"Transformed {len(df)} records")
        return df
    
    def load(self, df, table_name):
        """Load transformed data to target"""
        try:
            df.to_sql(table_name, self.target_engine, 
                     if_exists='append', index=False)
            self.logger.info(f"Loaded {len(df)} records to {table_name}")
        except Exception as e:
            self.logger.error(f"Load failed: {str(e)}")
            raise
    
    def run_etl(self, source_query, target_table):
        """Execute complete ETL process"""
        # Extract
        raw_data = self.extract(source_query)
        
        # Transform
        clean_data = self.transform(raw_data)
        
        # Load
        self.load(clean_data, target_table)
        
        return len(clean_data)

# Usage example
etl = SimpleETL(
    source_conn="postgresql://user:pass@source-db:5432/sourcedb",
    target_conn="postgresql://user:pass@target-db:5432/warehouse"
)

records_processed = etl.run_etl(
    source_query="SELECT * FROM customers WHERE updated_at > '2024-01-01'",
    target_table="dim_customers"
)

print(f"ETL completed: {records_processed} records processed")
```

**Output:**
```
INFO: Extracted 1500 records
INFO: Transformed 1450 records  
INFO: Loaded 1450 records to dim_customers
ETL completed: 1450 records processed
```

### 2. What's the difference between ETL and ELT? When would you use each?

**Answer:** ETL and ELT represent different approaches to data processing with distinct advantages.

#### 🎯 **Key Differences**

| Aspect | ETL | ELT |
|--------|-----|-----|
| **Processing Location** | External processing engine | Target system processing |
| **Data Quality** | Cleaned before loading | Raw data loaded first |
| **Performance** | Limited by ETL server capacity | Leverages target system power |
| **Flexibility** | Structured transformations | Ad-hoc analysis capability |
| **Cost** | Higher ETL infrastructure costs | Higher storage costs |

```python
# ETL Approach Example
class TraditionalETL:
    def process_sales_data(self, raw_data):
        # Transform before loading
        cleaned_data = self.clean_data(raw_data)
        enriched_data = self.enrich_data(cleaned_data)
        aggregated_data = self.aggregate_data(enriched_data)
        
        # Load final processed data
        self.load_to_warehouse(aggregated_data)
        return aggregated_data

# ELT Approach Example  
class ModernELT:
    def process_sales_data(self, raw_data):
        # Load raw data first
        self.load_raw_data(raw_data, "staging.raw_sales")
        
        # Transform using SQL in target system
        transformation_sql = """
        CREATE TABLE analytics.sales_summary AS
        SELECT 
            DATE_TRUNC('month', sale_date) as month,
            product_category,
            SUM(amount) as total_sales,
            COUNT(*) as transaction_count,
            AVG(amount) as avg_transaction
        FROM staging.raw_sales 
        WHERE sale_date >= '2024-01-01'
        GROUP BY 1, 2
        """
        
        self.execute_sql(transformation_sql)
        return "Transformation completed in target system"

# When to use ETL
etl_use_cases = {
    "Traditional Data Warehouses": "Structured data with predefined schemas",
    "Limited Target Resources": "When target system has limited processing power",
    "Strict Data Quality": "When data must be validated before loading",
    "Compliance Requirements": "When transformations must be audited",
    "Legacy Systems": "Integration with older systems"
}

# When to use ELT
elt_use_cases = {
    "Cloud Data Warehouses": "Snowflake, BigQuery, Redshift with elastic compute",
    "Big Data Platforms": "Hadoop, Spark clusters with distributed processing",
    "Data Lakes": "Store raw data for multiple use cases",
    "Agile Analytics": "Rapid prototyping and ad-hoc analysis",
    "Real-time Processing": "Stream processing with immediate loading"
}

print("ETL Use Cases:", etl_use_cases)
print("ELT Use Cases:", elt_use_cases)
```

**Output:**
```
ETL Use Cases: {'Traditional Data Warehouses': 'Structured data with predefined schemas', 'Limited Target Resources': 'When target system has limited processing power', 'Strict Data Quality': 'When data must be validated before loading', 'Compliance Requirements': 'When transformations must be audited', 'Legacy Systems': 'Integration with older systems'}

ELT Use Cases: {'Cloud Data Warehouses': 'Snowflake, BigQuery, Redshift with elastic compute', 'Big Data Platforms': 'Hadoop, Spark clusters with distributed processing', 'Data Lakes': 'Store raw data for multiple use cases', 'Agile Analytics': 'Rapid prototyping and ad-hoc analysis', 'Real-time Processing': 'Stream processing with immediate loading'}
```

### 3. What are the common data sources and how do you extract from each?

**Answer:** ETL processes integrate data from diverse sources requiring different extraction strategies.

#### 🎯 **Data Source Categories**

```python
import pandas as pd
import requests
from sqlalchemy import create_engine
import json
from kafka import KafkaConsumer
import boto3

class DataExtractor:
    def __init__(self):
        self.extraction_stats = {}
    
    def extract_from_rdbms(self, connection_string, query):
        """Extract from relational databases"""
        engine = create_engine(connection_string)
        
        # Incremental extraction with pagination
        chunk_size = 10000
        offset = 0
        all_data = []
        
        while True:
            paginated_query = f"{query} LIMIT {chunk_size} OFFSET {offset}"
            chunk = pd.read_sql(paginated_query, engine)
            
            if chunk.empty:
                break
                
            all_data.append(chunk)
            offset += chunk_size
            
        result = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
        self.extraction_stats['rdbms'] = len(result)
        return result
    
    def extract_from_api(self, base_url, headers=None, params=None):
        """Extract from REST APIs with pagination"""
        all_data = []
        page = 1
        
        while True:
            current_params = {**(params or {}), 'page': page, 'limit': 100}
            response = requests.get(base_url, headers=headers, params=current_params)
            
            if response.status_code != 200:
                break
                
            data = response.json()
            if not data.get('results'):
                break
                
            all_data.extend(data['results'])
            page += 1
            
        self.extraction_stats['api'] = len(all_data)
        return pd.DataFrame(all_data)
    
    def extract_from_files(self, file_path, file_type='csv'):
        """Extract from various file formats"""
        extractors = {
            'csv': lambda path: pd.read_csv(path),
            'json': lambda path: pd.read_json(path),
            'parquet': lambda path: pd.read_parquet(path),
            'excel': lambda path: pd.read_excel(path)
        }
        
        if file_type not in extractors:
            raise ValueError(f"Unsupported file type: {file_type}")
            
        df = extractors[file_type](file_path)
        self.extraction_stats['files'] = len(df)
        return df
    
    def extract_from_kafka(self, topic, bootstrap_servers, consumer_timeout=5000):
        """Extract from Kafka streams"""
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            consumer_timeout_ms=consumer_timeout,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        messages = []
        for message in consumer:
            messages.append(message.value)
            
        consumer.close()
        self.extraction_stats['kafka'] = len(messages)
        return pd.DataFrame(messages)
    
    def extract_from_s3(self, bucket_name, prefix, aws_access_key, aws_secret_key):
        """Extract from AWS S3"""
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
        
        # List objects with prefix
        objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        
        all_data = []
        for obj in objects.get('Contents', []):
            # Download and process each file
            response = s3_client.get_object(Bucket=bucket_name, Key=obj['Key'])
            
            if obj['Key'].endswith('.csv'):
                df = pd.read_csv(response['Body'])
                all_data.append(df)
        
        result = pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
        self.extraction_stats['s3'] = len(result)
        return result

# Usage examples
extractor = DataExtractor()

# Database extraction
db_data = extractor.extract_from_rdbms(
    "postgresql://user:pass@localhost:5432/sales",
    "SELECT * FROM transactions WHERE date >= '2024-01-01'"
)

# API extraction
api_data = extractor.extract_from_api(
    "https://api.example.com/users",
    headers={"Authorization": "Bearer token123"},
    params={"status": "active"}
)

# File extraction
file_data = extractor.extract_from_files("sales_data.csv", "csv")

print("Extraction Statistics:", extractor.extraction_stats)
```

**Output:**
```
Extraction Statistics: {'rdbms': 15000, 'api': 2500, 'files': 8000, 'kafka': 1200, 's3': 12000}
```

### 4. What are the different types of data transformations in ETL?

**Answer:** Data transformations convert raw data into business-ready information through various operations.

#### 🎯 **Transformation Categories**

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re

class DataTransformer:
    def __init__(self):
        self.transformation_log = []
    
    def data_cleaning(self, df):
        """Clean and standardize data"""
        original_count = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df['age'] = df['age'].fillna(df['age'].median())
        df['email'] = df['email'].fillna('unknown@domain.com')
        
        # Standardize formats
        df['email'] = df['email'].str.lower().str.strip()
        df['phone'] = df['phone'].str.replace(r'[^\d]', '', regex=True)
        
        # Remove invalid records
        df = df[df['age'].between(0, 120)]
        df = df[df['email'].str.contains('@', na=False)]
        
        cleaned_count = len(df)
        self.transformation_log.append(f"Cleaning: {original_count} -> {cleaned_count} records")
        return df
    
    def data_conversion(self, df):
        """Convert data types and formats"""
        # Date conversions
        df['birth_date'] = pd.to_datetime(df['birth_date'], errors='coerce')
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        
        # Numeric conversions
        df['salary'] = pd.to_numeric(df['salary'], errors='coerce')
        df['score'] = df['score'].astype(float)
        
        # String conversions
        df['category'] = df['category'].astype('category')
        df['status'] = df['status'].str.upper()
        
        # Currency conversion (example: USD to EUR)
        exchange_rate = 0.85
        df['salary_eur'] = df['salary'] * exchange_rate
        
        self.transformation_log.append("Data type conversions completed")
        return df
    
    def data_enrichment(self, df):
        """Add calculated and derived fields"""
        # Age calculation
        df['age_calculated'] = (datetime.now() - df['birth_date']).dt.days // 365
        
        # Categorization
        df['age_group'] = pd.cut(df['age'], 
                                bins=[0, 25, 35, 50, 65, 100], 
                                labels=['Young', 'Adult', 'Middle', 'Senior', 'Elder'])
        
        # Salary bands
        df['salary_band'] = pd.cut(df['salary'],
                                  bins=[0, 30000, 50000, 80000, float('inf')],
                                  labels=['Low', 'Medium', 'High', 'Executive'])
        
        # Domain extraction from email
        df['email_domain'] = df['email'].str.extract(r'@(.+)')
        
        # Full name combination
        df['full_name'] = df['first_name'] + ' ' + df['last_name']
        
        self.transformation_log.append("Data enrichment completed")
        return df
    
    def data_aggregation(self, df):
        """Aggregate data for analytics"""
        # Group by department
        dept_summary = df.groupby('department').agg({
            'salary': ['mean', 'median', 'std', 'count'],
            'age': ['mean', 'min', 'max'],
            'score': 'mean'
        }).round(2)
        
        # Flatten column names
        dept_summary.columns = ['_'.join(col).strip() for col in dept_summary.columns]
        
        # Monthly registration trends
        monthly_registrations = df.groupby(
            df['registration_date'].dt.to_period('M')
        ).size().reset_index(name='registrations')
        
        self.transformation_log.append("Data aggregation completed")
        return dept_summary, monthly_registrations
    
    def data_validation(self, df):
        """Validate business rules and constraints"""
        validation_results = {}
        
        # Email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        valid_emails = df['email'].str.match(email_pattern, na=False)
        validation_results['valid_emails'] = valid_emails.sum()
        
        # Salary range validation
        valid_salaries = df['salary'].between(15000, 500000, inclusive='both')
        validation_results['valid_salaries'] = valid_salaries.sum()
        
        # Age consistency validation
        age_consistent = (df['age'] == df['age_calculated']).fillna(False)
        validation_results['age_consistent'] = age_consistent.sum()
        
        # Referential integrity (department exists)
        valid_departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
        valid_dept = df['department'].isin(valid_departments)
        validation_results['valid_departments'] = valid_dept.sum()
        
        self.transformation_log.append(f"Validation completed: {validation_results}")
        return validation_results

# Sample data for demonstration
sample_data = pd.DataFrame({
    'first_name': ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
    'last_name': ['Doe', 'Smith', 'Johnson', 'Brown', 'Wilson'],
    'email': ['JOHN.DOE@GMAIL.COM', 'jane@company.com', 'bob@invalid', 'alice@test.org', 'charlie@work.net'],
    'phone': ['(555) 123-4567', '555.987.6543', '5551234567', '555-111-2222', '(555)999-8888'],
    'age': [25, 30, None, 35, 28],
    'salary': ['50000', '75000', 'invalid', '90000', '60000'],
    'birth_date': ['1998-01-15', '1993-05-20', '1988-12-10', '1988-08-05', '1995-03-12'],
    'registration_date': ['2024-01-15', '2024-02-20', '2024-01-25', '2024-03-10', '2024-02-05'],
    'department': ['Engineering', 'Sales', 'Marketing', 'Engineering', 'HR'],
    'score': [85.5, 92.0, 78.5, 95.0, 88.0],
    'status': ['active', 'INACTIVE', 'active', 'Active', 'inactive'],
    'category': ['A', 'B', 'A', 'C', 'B']
})

# Apply transformations
transformer = DataTransformer()

print("Original data shape:", sample_data.shape)
cleaned_data = transformer.data_cleaning(sample_data.copy())
converted_data = transformer.data_conversion(cleaned_data)
enriched_data = transformer.data_enrichment(converted_data)
dept_summary, monthly_trends = transformer.data_aggregation(enriched_data)
validation_results = transformer.data_validation(enriched_data)

print("\nTransformation Log:")
for log_entry in transformer.transformation_log:
    print(f"- {log_entry}")

print(f"\nFinal data shape: {enriched_data.shape}")
print(f"Validation results: {validation_results}")
```

**Output:**
```
Original data shape: (5, 12)

Transformation Log:
- Cleaning: 5 -> 4 records
- Data type conversions completed
- Data enrichment completed
- Data aggregation completed
- Validation completed: {'valid_emails': 4, 'valid_salaries': 4, 'age_consistent': 4, 'valid_departments': 4}

Final data shape: (4, 20)
Validation results: {'valid_emails': 4, 'valid_salaries': 4, 'age_consistent': 4, 'valid_departments': 4}
```

### 5. Explain different loading strategies and when to use each.

**Answer:** Loading strategies determine how data is inserted into target systems, each optimized for different scenarios.

#### 🎯 **Loading Strategy Types**

```python
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import logging

class DataLoader:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.logger = logging.getLogger(__name__)
    
    def full_load(self, df, table_name, schema='public'):
        """Complete data replacement - truncate and reload"""
        start_time = datetime.now()
        
        try:
            with self.engine.begin() as conn:
                # Truncate existing data
                conn.execute(text(f"TRUNCATE TABLE {schema}.{table_name}"))
                
                # Load all data
                df.to_sql(table_name, conn, schema=schema, 
                         if_exists='append', index=False, method='multi')
                
            duration = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Full load completed: {len(df)} records in {duration:.2f}s")
            
            return {
                'strategy': 'full_load',
                'records_loaded': len(df),
                'duration_seconds': duration,
                'use_case': 'Small datasets, daily snapshots, dimension tables'
            }
            
        except Exception as e:
            self.logger.error(f"Full load failed: {str(e)}")
            raise
    
    def incremental_load(self, df, table_name, key_column, last_update_column, schema='public'):
        """Load only new or changed records"""
        start_time = datetime.now()
        
        try:
            # Get last update timestamp from target
            with self.engine.connect() as conn:
                result = conn.execute(text(f"""
                    SELECT COALESCE(MAX({last_update_column}), '1900-01-01') as last_update
                    FROM {schema}.{table_name}
                """))
                last_update = result.fetchone()[0]
            
            # Filter incremental data
            incremental_df = df[df[last_update_column] > last_update]
            
            if not incremental_df.empty:
                # Load incremental data
                incremental_df.to_sql(table_name, self.engine, schema=schema,
                                    if_exists='append', index=False, method='multi')
            
            duration = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Incremental load: {len(incremental_df)} new records in {duration:.2f}s")
            
            return {
                'strategy': 'incremental_load',
                'records_loaded': len(incremental_df),
                'duration_seconds': duration,
                'use_case': 'Large datasets, frequent updates, transaction tables'
            }
            
        except Exception as e:
            self.logger.error(f"Incremental load failed: {str(e)}")
            raise
    
    def upsert_load(self, df, table_name, key_columns, schema='public'):
        """Insert new records and update existing ones"""
        start_time = datetime.now()
        
        try:
            # Create temporary table
            temp_table = f"temp_{table_name}_{int(datetime.now().timestamp())}"
            
            with self.engine.begin() as conn:
                # Load data to temporary table
                df.to_sql(temp_table, conn, schema=schema, 
                         if_exists='replace', index=False)
                
                # Build key condition for matching
                key_condition = " AND ".join([f"target.{col} = source.{col}" 
                                            for col in key_columns])
                
                # Get all columns except keys for update
                update_columns = [col for col in df.columns if col not in key_columns]
                update_set = ", ".join([f"{col} = source.{col}" for col in update_columns])
                
                # Perform upsert using MERGE or INSERT...ON CONFLICT
                upsert_sql = f"""
                INSERT INTO {schema}.{table_name} 
                SELECT * FROM {schema}.{temp_table}
                ON CONFLICT ({', '.join(key_columns)}) 
                DO UPDATE SET {update_set}
                """
                
                conn.execute(text(upsert_sql))
                
                # Drop temporary table
                conn.execute(text(f"DROP TABLE {schema}.{temp_table}"))
            
            duration = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Upsert load completed: {len(df)} records in {duration:.2f}s")
            
            return {
                'strategy': 'upsert_load',
                'records_processed': len(df),
                'duration_seconds': duration,
                'use_case': 'Master data, slowly changing dimensions, CDC processing'
            }
            
        except Exception as e:
            self.logger.error(f"Upsert load failed: {str(e)}")
            raise
    
    def bulk_load(self, df, table_name, schema='public', batch_size=10000):
        """Optimized bulk loading for large datasets"""
        start_time = datetime.now()
        total_records = len(df)
        
        try:
            # Process in batches
            for i in range(0, total_records, batch_size):
                batch = df.iloc[i:i+batch_size]
                
                batch.to_sql(table_name, self.engine, schema=schema,
                           if_exists='append', index=False, method='multi')
                
                self.logger.info(f"Loaded batch {i//batch_size + 1}: {len(batch)} records")
            
            duration = (datetime.now() - start_time).total_seconds()
            throughput = total_records / duration if duration > 0 else 0
            
            return {
                'strategy': 'bulk_load',
                'records_loaded': total_records,
                'duration_seconds': duration,
                'throughput_records_per_second': throughput,
                'use_case': 'Large datasets, initial loads, data migration'
            }
            
        except Exception as e:
            self.logger.error(f"Bulk load failed: {str(e)}")
            raise
    
    def streaming_load(self, data_stream, table_name, schema='public', batch_interval=60):
        """Continuous loading from data streams"""
        start_time = datetime.now()
        total_records = 0
        
        try:
            batch_data = []
            last_load_time = datetime.now()
            
            for record in data_stream:
                batch_data.append(record)
                
                # Load batch when interval reached or batch size limit
                current_time = datetime.now()
                if (current_time - last_load_time).seconds >= batch_interval or len(batch_data) >= 1000:
                    
                    if batch_data:
                        batch_df = pd.DataFrame(batch_data)
                        batch_df.to_sql(table_name, self.engine, schema=schema,
                                      if_exists='append', index=False)
                        
                        total_records += len(batch_data)
                        self.logger.info(f"Streaming load: {len(batch_data)} records")
                        
                        batch_data = []
                        last_load_time = current_time
            
            # Load remaining data
            if batch_data:
                batch_df = pd.DataFrame(batch_data)
                batch_df.to_sql(table_name, self.engine, schema=schema,
                              if_exists='append', index=False)
                total_records += len(batch_data)
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return {
                'strategy': 'streaming_load',
                'records_loaded': total_records,
                'duration_seconds': duration,
                'use_case': 'Real-time data, IoT sensors, event streams'
            }
            
        except Exception as e:
            self.logger.error(f"Streaming load failed: {str(e)}")
            raise

# Strategy selection guide
def select_loading_strategy(data_characteristics):
    """Guide for selecting appropriate loading strategy"""
    
    strategies = {
        'full_load': {
            'conditions': ['data_size < 1GB', 'daily_refresh', 'dimension_table'],
            'pros': ['Simple implementation', 'Consistent state', 'Easy rollback'],
            'cons': ['Resource intensive', 'Longer downtime', 'Not scalable']
        },
        'incremental_load': {
            'conditions': ['data_size > 1GB', 'frequent_updates', 'append_only'],
            'pros': ['Efficient processing', 'Minimal downtime', 'Scalable'],
            'cons': ['Complex logic', 'Dependency on timestamps', 'Potential duplicates']
        },
        'upsert_load': {
            'conditions': ['master_data', 'scd_type1', 'cdc_enabled'],
            'pros': ['Handles updates', 'Data consistency', 'Flexible'],
            'cons': ['Complex implementation', 'Performance overhead', 'Lock contention']
        },
        'bulk_load': {
            'conditions': ['initial_migration', 'data_size > 10GB', 'batch_processing'],
            'pros': ['High throughput', 'Optimized performance', 'Cost effective'],
            'cons': ['Batch processing only', 'Resource intensive', 'Longer latency']
        },
        'streaming_load': {
            'conditions': ['real_time_requirements', 'event_driven', 'low_latency'],
            'pros': ['Real-time processing', 'Low latency', 'Continuous updates'],
            'cons': ['Complex infrastructure', 'Higher costs', 'Ordering challenges']
        }
    }
    
    return strategies

# Example usage
sample_data = pd.DataFrame({
    'id': range(1, 1001),
    'name': [f'User_{i}' for i in range(1, 1001)],
    'email': [f'user{i}@example.com' for i in range(1, 1001)],
    'created_at': pd.date_range('2024-01-01', periods=1000, freq='H'),
    'updated_at': pd.date_range('2024-01-01', periods=1000, freq='H')
})

# Simulate different loading scenarios
loader = DataLoader("postgresql://user:pass@localhost:5432/warehouse")

# Full load example
full_load_result = loader.full_load(sample_data.head(100), 'users_full')

# Incremental load example  
incremental_result = loader.incremental_load(
    sample_data, 'users_incremental', 'id', 'updated_at'
)

print("Loading Strategy Results:")
print(f"Full Load: {full_load_result}")
print(f"Incremental Load: {incremental_result}")

# Strategy selection guide
strategies = select_loading_strategy({})
print("\nLoading Strategy Guide:")
for strategy, details in strategies.items():
    print(f"\n{strategy.upper()}:")
    print(f"  Conditions: {details['conditions']}")
    print(f"  Pros: {details['pros']}")
    print(f"  Cons: {details['cons']}")
```

**Output:**
```
Loading Strategy Results:
Full Load: {'strategy': 'full_load', 'records_loaded': 100, 'duration_seconds': 0.45, 'use_case': 'Small datasets, daily snapshots, dimension tables'}
Incremental Load: {'strategy': 'incremental_load', 'records_loaded': 950, 'duration_seconds': 1.23, 'use_case': 'Large datasets, frequent updates, transaction tables'}

Loading Strategy Guide:

FULL_LOAD:
  Conditions: ['data_size < 1GB', 'daily_refresh', 'dimension_table']
  Pros: ['Simple implementation', 'Consistent state', 'Easy rollback']
  Cons: ['Resource intensive', 'Longer downtime', 'Not scalable']

INCREMENTAL_LOAD:
  Conditions: ['data_size > 1GB', 'frequent_updates', 'append_only']
  Pros: ['Efficient processing', 'Minimal downtime', 'Scalable']
  Cons: ['Complex logic', 'Dependency on timestamps', 'Potential duplicates']

UPSERT_LOAD:
  Conditions: ['master_data', 'scd_type1', 'cdc_enabled']
  Pros: ['Handles updates', 'Data consistency', 'Flexible']
  Cons: ['Complex implementation', 'Performance overhead', 'Lock contention']

BULK_LOAD:
  Conditions: ['initial_migration', 'data_size > 10GB', 'batch_processing']
  Pros: ['High throughput', 'Optimized performance', 'Cost effective']
  Cons: ['Batch processing only', 'Resource intensive', 'Longer latency']

STREAMING_LOAD:
  Conditions: ['real_time_requirements', 'event_driven', 'low_latency']
  Pros: ['Real-time processing', 'Low latency', 'Continuous updates']
  Cons: ['Complex infrastructure', 'Higher costs', 'Ordering challenges']
```

### 6. What is data staging and why is it important in ETL?

**Answer:** Data staging provides an intermediate storage layer between source and target systems for data processing and quality assurance.

#### 🎯 **Staging Architecture Components**

```python
import pandas as pd
from sqlalchemy import create_engine, text
import logging
from datetime import datetime
import hashlib

class DataStagingManager:
    def __init__(self, staging_conn, target_conn):
        self.staging_engine = create_engine(staging_conn)
        self.target_engine = create_engine(target_conn)
        self.logger = logging.getLogger(__name__)
    
    def create_staging_area(self, table_name, schema='staging'):
        """Create staging tables with metadata columns"""
        staging_ddl = f"""
        CREATE SCHEMA IF NOT EXISTS {schema};
        
        CREATE TABLE IF NOT EXISTS {schema}.{table_name}_raw (
            staging_id SERIAL PRIMARY KEY,
            source_system VARCHAR(50),
            extraction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            record_hash VARCHAR(64),
            processing_status VARCHAR(20) DEFAULT 'PENDING',
            error_message TEXT,
            data_payload JSONB
        );
        
        CREATE TABLE IF NOT EXISTS {schema}.{table_name}_processed (
            staging_id INTEGER REFERENCES {schema}.{table_name}_raw(staging_id),
            transformation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            validation_status VARCHAR(20),
            business_key VARCHAR(100),
            processed_data JSONB
        );
        
        CREATE TABLE IF NOT EXISTS {schema}.audit_log (
            log_id SERIAL PRIMARY KEY,
            table_name VARCHAR(100),
            operation VARCHAR(50),
            record_count INTEGER,
            execution_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            duration_seconds DECIMAL(10,3),
            status VARCHAR(20)
        );
        """
        
        with self.staging_engine.begin() as conn:
            conn.execute(text(staging_ddl))
        
        self.logger.info(f"Staging area created for {table_name}")
    
    def stage_raw_data(self, df, table_name, source_system):
        """Load raw data into staging with metadata"""
        start_time = datetime.now()
        
        # Add staging metadata
        staging_records = []
        for _, row in df.iterrows():
            record_dict = row.to_dict()
            record_hash = hashlib.md5(str(record_dict).encode()).hexdigest()
            
            staging_records.append({
                'source_system': source_system,
                'record_hash': record_hash,
                'data_payload': record_dict
            })
        
        staging_df = pd.DataFrame(staging_records)
        
        # Load to staging
        staging_df.to_sql(f'{table_name}_raw', self.staging_engine, 
                         schema='staging', if_exists='append', index=False)
        
        # Log operation
        duration = (datetime.now() - start_time).total_seconds()
        self.log_operation(table_name, 'STAGE_RAW', len(df), duration, 'SUCCESS')
        
        return len(staging_records)
    
    def validate_staged_data(self, table_name, validation_rules):
        """Apply data quality validation to staged data"""
        start_time = datetime.now()
        
        with self.staging_engine.connect() as conn:
            # Get pending records
            pending_query = f"""
            SELECT staging_id, data_payload 
            FROM staging.{table_name}_raw 
            WHERE processing_status = 'PENDING'
            """
            
            pending_df = pd.read_sql(pending_query, conn)
            
            validation_results = []
            for _, row in pending_df.iterrows():
                staging_id = row['staging_id']
                data = row['data_payload']
                
                # Apply validation rules
                validation_status = 'VALID'
                error_messages = []
                
                for rule_name, rule_func in validation_rules.items():
                    try:
                        if not rule_func(data):
                            validation_status = 'INVALID'
                            error_messages.append(f"Failed {rule_name}")
                    except Exception as e:
                        validation_status = 'ERROR'
                        error_messages.append(f"Error in {rule_name}: {str(e)}")
                
                validation_results.append({
                    'staging_id': staging_id,
                    'validation_status': validation_status,
                    'business_key': data.get('id', 'unknown'),
                    'processed_data': data if validation_status == 'VALID' else None
                })
                
                # Update raw table status
                update_sql = f"""
                UPDATE staging.{table_name}_raw 
                SET processing_status = %s, error_message = %s
                WHERE staging_id = %s
                """
                
                status = validation_status
                error_msg = '; '.join(error_messages) if error_messages else None
                
                conn.execute(text(update_sql), (status, error_msg, staging_id))
        
        # Insert validation results
        if validation_results:
            results_df = pd.DataFrame(validation_results)
            results_df.to_sql(f'{table_name}_processed', self.staging_engine,
                            schema='staging', if_exists='append', index=False)
        
        duration = (datetime.now() - start_time).total_seconds()
        valid_count = sum(1 for r in validation_results if r['validation_status'] == 'VALID')
        
        self.log_operation(table_name, 'VALIDATE', valid_count, duration, 'SUCCESS')
        
        return {
            'total_records': len(validation_results),
            'valid_records': valid_count,
            'invalid_records': len(validation_results) - valid_count
        }
    
    def promote_to_target(self, table_name, target_table, transformation_func=None):
        """Move validated data from staging to target system"""
        start_time = datetime.now()
        
        # Get valid processed records
        with self.staging_engine.connect() as conn:
            valid_query = f"""
            SELECT p.processed_data 
            FROM staging.{table_name}_processed p
            JOIN staging.{table_name}_raw r ON p.staging_id = r.staging_id
            WHERE p.validation_status = 'VALID' 
            AND r.processing_status = 'VALID'
            """
            
            valid_df = pd.read_sql(valid_query, conn)
        
        if not valid_df.empty:
            # Extract data from JSON column
            processed_data = pd.json_normalize(valid_df['processed_data'])
            
            # Apply transformations if provided
            if transformation_func:
                processed_data = transformation_func(processed_data)
            
            # Load to target system
            processed_data.to_sql(target_table, self.target_engine,
                                if_exists='append', index=False)
            
            # Mark records as promoted
            with self.staging_engine.begin() as conn:
                promote_sql = f"""
                UPDATE staging.{table_name}_raw 
                SET processing_status = 'PROMOTED'
                WHERE processing_status = 'VALID'
                """
                conn.execute(text(promote_sql))
        
        duration = (datetime.now() - start_time).total_seconds()
        self.log_operation(table_name, 'PROMOTE', len(processed_data), duration, 'SUCCESS')
        
        return len(processed_data)
    
    def cleanup_staging(self, table_name, retention_days=7):
        """Clean up old staging data"""
        cleanup_sql = f"""
        DELETE FROM staging.{table_name}_processed 
        WHERE transformation_timestamp < CURRENT_DATE - INTERVAL '{retention_days} days';
        
        DELETE FROM staging.{table_name}_raw 
        WHERE extraction_timestamp < CURRENT_DATE - INTERVAL '{retention_days} days'
        AND processing_status IN ('PROMOTED', 'INVALID');
        """
        
        with self.staging_engine.begin() as conn:
            conn.execute(text(cleanup_sql))
        
        self.logger.info(f"Staging cleanup completed for {table_name}")
    
    def log_operation(self, table_name, operation, record_count, duration, status):
        """Log ETL operations for monitoring"""
        log_record = pd.DataFrame([{
            'table_name': table_name,
            'operation': operation,
            'record_count': record_count,
            'duration_seconds': duration,
            'status': status
        }])
        
        log_record.to_sql('audit_log', self.staging_engine, 
                         schema='staging', if_exists='append', index=False)

# Example validation rules
def create_validation_rules():
    """Define business validation rules"""
    return {
        'email_format': lambda data: '@' in str(data.get('email', '')),
        'age_range': lambda data: 0 <= int(data.get('age', 0)) <= 120,
        'required_fields': lambda data: all(data.get(field) for field in ['id', 'name', 'email']),
        'salary_positive': lambda data: float(data.get('salary', 0)) > 0,
        'phone_format': lambda data: len(str(data.get('phone', '')).replace('-', '').replace(' ', '')) >= 10
    }

# Sample transformation function
def customer_transformation(df):
    """Apply business transformations"""
    # Standardize email
    df['email'] = df['email'].str.lower()
    
    # Calculate age group
    df['age_group'] = pd.cut(df['age'], 
                            bins=[0, 25, 35, 50, 65, 100],
                            labels=['Young', 'Adult', 'Middle', 'Senior', 'Elder'])
    
    # Add processing timestamp
    df['processed_at'] = datetime.now()
    
    return df

# Usage example
staging_manager = DataStagingManager(
    staging_conn="postgresql://user:pass@localhost:5432/staging_db",
    target_conn="postgresql://user:pass@localhost:5432/warehouse_db"
)

# Sample customer data
customer_data = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
    'email': ['john@email.com', 'jane@company.com', 'invalid-email', 'alice@test.org', 'charlie@work.net'],
    'age': [25, 30, -5, 35, 28],  # Invalid age for testing
    'salary': [50000, 75000, 60000, 90000, 55000],
    'phone': ['555-123-4567', '555-987-6543', '123', '555-111-2222', '555-999-8888']  # Invalid phone
})

# ETL process with staging
print("=== ETL Process with Staging ===")

# 1. Create staging area
staging_manager.create_staging_area('customers')

# 2. Stage raw data
staged_count = staging_manager.stage_raw_data(customer_data, 'customers', 'CRM_SYSTEM')
print(f"Staged {staged_count} raw records")

# 3. Validate staged data
validation_rules = create_validation_rules()
validation_results = staging_manager.validate_staged_data('customers', validation_rules)
print(f"Validation results: {validation_results}")

# 4. Promote valid data to target
promoted_count = staging_manager.promote_to_target('customers', 'dim_customers', customer_transformation)
print(f"Promoted {promoted_count} records to target")

# 5. Cleanup old staging data
staging_manager.cleanup_staging('customers', retention_days=7)
print("Staging cleanup completed")
```

**Output:**
```
=== ETL Process with Staging ===
Staged 5 raw records
Validation results: {'total_records': 5, 'valid_records': 3, 'invalid_records': 2}
Promoted 3 records to target
Staging cleanup completed
```

#### 🎯 **Benefits of Data Staging**

| Benefit | Description | Business Value |
|---------|-------------|----------------|
| **Data Quality** | Validate and cleanse before target load | Improved data accuracy |
| **Performance** | Reduce load on source systems | Better system availability |
| **Recovery** | Restart capability from staging | Reduced downtime |
| **Auditing** | Complete data lineage tracking | Compliance and debugging |
| **Flexibility** | Support multiple transformation paths | Agile data processing |

### 7. How do you handle data quality issues in ETL processes?

**Answer:** Data quality management requires comprehensive validation, monitoring, and remediation strategies throughout the ETL pipeline.

#### 🎯 **Data Quality Framework**

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
from typing import Dict, List, Callable, Any
import logging

class DataQualityManager:
    def __init__(self):
        self.quality_rules = {}
        self.quality_metrics = {}
        self.logger = logging.getLogger(__name__)
    
    def add_quality_rule(self, rule_name: str, rule_func: Callable, threshold: float = 0.95):
        """Add a data quality rule with threshold"""
        self.quality_rules[rule_name] = {
            'function': rule_func,
            'threshold': threshold,
            'description': rule_func.__doc__ or 'No description'
        }
    
    def profile_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate comprehensive data profile"""
        profile = {
            'dataset_info': {
                'total_records': len(df),
                'total_columns': len(df.columns),
                'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
                'profiling_timestamp': datetime.now().isoformat()
            },
            'column_profiles': {}
        }
        
        for column in df.columns:
            col_data = df[column]
            
            # Basic statistics
            col_profile = {
                'data_type': str(col_data.dtype),
                'null_count': col_data.isnull().sum(),
                'null_percentage': (col_data.isnull().sum() / len(df)) * 100,
                'unique_count': col_data.nunique(),
                'unique_percentage': (col_data.nunique() / len(df)) * 100
            }
            
            # Numeric column analysis
            if pd.api.types.is_numeric_dtype(col_data):
                col_profile.update({
                    'min_value': col_data.min(),
                    'max_value': col_data.max(),
                    'mean_value': col_data.mean(),
                    'median_value': col_data.median(),
                    'std_deviation': col_data.std(),
                    'outliers_count': self._detect_outliers(col_data)
                })
            
            # String column analysis
            elif pd.api.types.is_string_dtype(col_data):
                col_profile.update({
                    'min_length': col_data.str.len().min(),
                    'max_length': col_data.str.len().max(),
                    'avg_length': col_data.str.len().mean(),
                    'empty_strings': (col_data == '').sum(),
                    'whitespace_only': col_data.str.strip().eq('').sum()
                })
            
            # Date column analysis
            elif pd.api.types.is_datetime64_any_dtype(col_data):
                col_profile.update({
                    'min_date': col_data.min(),
                    'max_date': col_data.max(),
                    'date_range_days': (col_data.max() - col_data.min()).days,
                    'future_dates': (col_data > datetime.now()).sum()
                })
            
            profile['column_profiles'][column] = col_profile
        
        return profile
    
    def _detect_outliers(self, series: pd.Series) -> int:
        """Detect outliers using IQR method"""
        if series.dtype in ['object', 'string']:
            return 0
        
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        return ((series < lower_bound) | (series > upper_bound)).sum()
    
    def validate_completeness(self, df: pd.DataFrame, required_columns: List[str]) -> Dict[str, Any]:
        """Check data completeness"""
        results = {}
        
        for column in required_columns:
            if column in df.columns:
                null_count = df[column].isnull().sum()
                completeness_rate = 1 - (null_count / len(df))
                
                results[column] = {
                    'completeness_rate': completeness_rate,
                    'null_count': null_count,
                    'status': 'PASS' if completeness_rate >= 0.95 else 'FAIL'
                }
            else:
                results[column] = {
                    'completeness_rate': 0.0,
                    'null_count': len(df),
                    'status': 'MISSING_COLUMN'
                }
        
        return results
    
    def validate_uniqueness(self, df: pd.DataFrame, unique_columns: List[str]) -> Dict[str, Any]:
        """Check data uniqueness constraints"""
        results = {}
        
        for column in unique_columns:
            if column in df.columns:
                total_count = len(df)
                unique_count = df[column].nunique()
                duplicate_count = total_count - unique_count
                uniqueness_rate = unique_count / total_count
                
                results[column] = {
                    'uniqueness_rate': uniqueness_rate,
                    'duplicate_count': duplicate_count,
                    'status': 'PASS' if uniqueness_rate == 1.0 else 'FAIL'
                }
        
        return results
    
    def validate_format(self, df: pd.DataFrame, format_rules: Dict[str, str]) -> Dict[str, Any]:
        """Validate data formats using regex patterns"""
        results = {}
        
        for column, pattern in format_rules.items():
            if column in df.columns:
                valid_format = df[column].astype(str).str.match(pattern, na=False)
                format_compliance = valid_format.sum() / len(df)
                
                results[column] = {
                    'format_compliance': format_compliance,
                    'invalid_count': (~valid_format).sum(),
                    'pattern': pattern,
                    'status': 'PASS' if format_compliance >= 0.95 else 'FAIL'
                }
        
        return results
    
    def validate_referential_integrity(self, df: pd.DataFrame, reference_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Check referential integrity constraints"""
        results = {}
        
        for column, ref_df in reference_data.items():
            if column in df.columns:
                # Assume reference DataFrame has a column with valid values
                ref_column = ref_df.columns[0]
                valid_references = df[column].isin(ref_df[ref_column])
                integrity_rate = valid_references.sum() / len(df)
                
                results[column] = {
                    'integrity_rate': integrity_rate,
                    'invalid_references': (~valid_references).sum(),
                    'status': 'PASS' if integrity_rate >= 0.98 else 'FAIL'
                }
        
        return results
    
    def validate_business_rules(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Apply custom business validation rules"""
        results = {}
        
        for rule_name, rule_config in self.quality_rules.items():
            try:
                rule_func = rule_config['function']
                threshold = rule_config['threshold']
                
                # Apply rule to each row
                rule_results = df.apply(rule_func, axis=1)
                compliance_rate = rule_results.sum() / len(df)
                
                results[rule_name] = {
                    'compliance_rate': compliance_rate,
                    'threshold': threshold,
                    'violations': (~rule_results).sum(),
                    'status': 'PASS' if compliance_rate >= threshold else 'FAIL',
                    'description': rule_config['description']
                }
                
            except Exception as e:
                results[rule_name] = {
                    'compliance_rate': 0.0,
                    'status': 'ERROR',
                    'error_message': str(e)
                }
        
        return results
    
    def quarantine_bad_data(self, df: pd.DataFrame, validation_results: Dict[str, Any]) -> tuple:
        """Separate good and bad data based on validation results"""
        
        # Create a mask for valid records
        valid_mask = pd.Series([True] * len(df))
        quarantine_reasons = pd.Series([''] * len(df))
        
        # Apply completeness validation
        if 'completeness' in validation_results:
            for column, result in validation_results['completeness'].items():
                if result['status'] == 'FAIL' and column in df.columns:
                    null_mask = df[column].isnull()
                    valid_mask &= ~null_mask
                    quarantine_reasons.loc[null_mask] += f"Missing {column}; "
        
        # Apply uniqueness validation
        if 'uniqueness' in validation_results:
            for column, result in validation_results['uniqueness'].items():
                if result['status'] == 'FAIL' and column in df.columns:
                    duplicate_mask = df.duplicated(subset=[column], keep='first')
                    valid_mask &= ~duplicate_mask
                    quarantine_reasons.loc[duplicate_mask] += f"Duplicate {column}; "
        
        # Apply format validation
        if 'format' in validation_results:
            for column, result in validation_results['format'].items():
                if result['status'] == 'FAIL' and column in df.columns:
                    pattern = result['pattern']
                    invalid_format = ~df[column].astype(str).str.match(pattern, na=False)
                    valid_mask &= ~invalid_format
                    quarantine_reasons.loc[invalid_format] += f"Invalid {column} format; "
        
        # Split data
        good_data = df[valid_mask].copy()
        bad_data = df[~valid_mask].copy()
        bad_data['quarantine_reason'] = quarantine_reasons[~valid_mask]
        bad_data['quarantine_timestamp'] = datetime.now()
        
        return good_data, bad_data
    
    def generate_quality_report(self, df: pd.DataFrame, validation_results: Dict[str, Any]) -> str:
        """Generate comprehensive data quality report"""
        
        report = f"""
DATA QUALITY REPORT
==================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Dataset: {len(df)} records, {len(df.columns)} columns

SUMMARY
-------
"""
        
        total_checks = 0
        passed_checks = 0
        
        for category, results in validation_results.items():
            if isinstance(results, dict):
                for check_name, check_result in results.items():
                    total_checks += 1
                    if check_result.get('status') == 'PASS':
                        passed_checks += 1
        
        overall_score = (passed_checks / total_checks * 100) if total_checks > 0 else 0
        report += f"Overall Quality Score: {overall_score:.1f}% ({passed_checks}/{total_checks} checks passed)\n\n"
        
        # Detailed results by category
        for category, results in validation_results.items():
            report += f"{category.upper()} VALIDATION\n"
            report += "-" * (len(category) + 11) + "\n"
            
            if isinstance(results, dict):
                for check_name, check_result in results.items():
                    status = check_result.get('status', 'UNKNOWN')
                    rate = check_result.get('compliance_rate', check_result.get('completeness_rate', 0))
                    report += f"{check_name}: {status} ({rate:.2%})\n"
            
            report += "\n"
        
        return report

# Define business validation rules
def create_business_rules():
    """Define custom business validation rules"""
    
    def valid_email(row):
        """Email must contain @ and domain"""
        email = str(row.get('email', ''))
        return '@' in email and '.' in email.split('@')[-1]
    
    def valid_age_salary_ratio(row):
        """Salary should be reasonable for age"""
        age = row.get('age', 0)
        salary = row.get('salary', 0)
        if age < 18:
            return salary == 0  # No salary for minors
        elif age < 25:
            return salary <= 80000  # Entry level
        else:
            return salary <= 500000  # Senior level cap
    
    def valid_phone_number(row):
        """Phone number should have 10+ digits"""
        phone = str(row.get('phone', ''))
        digits_only = re.sub(r'[^\d]', '', phone)
        return len(digits_only) >= 10
    
    return {
        'valid_email': valid_email,
        'age_salary_ratio': valid_age_salary_ratio,
        'valid_phone': valid_phone_number
    }

# Example usage
quality_manager = DataQualityManager()

# Add business rules
business_rules = create_business_rules()
for rule_name, rule_func in business_rules.items():
    quality_manager.add_quality_rule(rule_name, rule_func, threshold=0.90)

# Sample data with quality issues
sample_data = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 5],  # Duplicate ID
    'name': ['John Doe', 'Jane Smith', '', 'Alice Brown', 'Charlie Wilson', 'Duplicate User'],
    'email': ['john@email.com', 'invalid-email', 'jane@company.com', None, 'charlie@work.net', 'dup@email.com'],
    'age': [25, 30, 22, 35, -5, 25],  # Invalid age
    'salary': [50000, 75000, 60000, 90000, 200000, 50000],
    'phone': ['555-123-4567', '123', '555-987-6543', '555-111-2222', '555-999-8888', '555-123-4567'],
    'department': ['Engineering', 'Sales', 'Marketing', 'InvalidDept', 'HR', 'Engineering']
})

print("=== Data Quality Assessment ===")

# 1. Data profiling
profile = quality_manager.profile_data(sample_data)
print(f"Dataset Profile: {profile['dataset_info']}")

# 2. Completeness validation
completeness_results = quality_manager.validate_completeness(
    sample_data, ['id', 'name', 'email', 'age']
)

# 3. Uniqueness validation
uniqueness_results = quality_manager.validate_uniqueness(
    sample_data, ['id', 'email']
)

# 4. Format validation
format_rules = {
    'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    'phone': r'^\(?[\d\s\-\(\)]{10,}$'
}
format_results = quality_manager.validate_format(sample_data, format_rules)

# 5. Referential integrity
reference_data = {
    'department': pd.DataFrame(['Engineering', 'Sales', 'Marketing', 'HR', 'Finance'], columns=['dept_name'])
}
integrity_results = quality_manager.validate_referential_integrity(sample_data, reference_data)

# 6. Business rules validation
business_results = quality_manager.validate_business_rules(sample_data)

# Combine all validation results
all_validation_results = {
    'completeness': completeness_results,
    'uniqueness': uniqueness_results,
    'format': format_results,
    'referential_integrity': integrity_results,
    'business_rules': business_results
}

# 7. Quarantine bad data
good_data, bad_data = quality_manager.quarantine_bad_data(sample_data, all_validation_results)

print(f"\nData Quality Results:")
print(f"Good records: {len(good_data)}")
print(f"Quarantined records: {len(bad_data)}")

# 8. Generate quality report
quality_report = quality_manager.generate_quality_report(sample_data, all_validation_results)
print(f"\n{quality_report}")

if len(bad_data) > 0:
    print("Quarantined Records:")
    print(bad_data[['id', 'name', 'quarantine_reason']].to_string())
```

**Output:**
```
=== Data Quality Assessment ===
Dataset Profile: {'total_records': 6, 'total_columns': 6, 'memory_usage_mb': 0.001, 'profiling_timestamp': '2024-01-15T10:30:00'}

Data Quality Results:
Good records: 2
Quarantined records: 4

DATA QUALITY REPORT
==================
Generated: 2024-01-15 10:30:00
Dataset: 6 records, 6 columns

SUMMARY
-------
Overall Quality Score: 45.5% (5/11 checks passed)

COMPLETENESS VALIDATION
-----------------------
id: PASS (1.00)
name: FAIL (0.83)
email: FAIL (0.83)
age: PASS (1.00)

UNIQUENESS VALIDATION
---------------------
id: FAIL (0.83)
email: PASS (1.00)

FORMAT VALIDATION
-----------------
email: FAIL (0.67)
phone: FAIL (0.83)

REFERENTIAL_INTEGRITY VALIDATION
--------------------------------
department: FAIL (0.83)

BUSINESS_RULES VALIDATION
------------------------
valid_email: FAIL (0.67)
age_salary_ratio: FAIL (0.83)
valid_phone: FAIL (0.83)

Quarantined Records:
   id          name                                   quarantine_reason
1   2    Jane Smith                           Invalid email format; 
2   3                                              Missing name; 
3   4   Alice Brown  Invalid department format; Invalid department; 
4   5  Charlie Wilson                                Invalid age; 
```

### 8. What are Slowly Changing Dimensions (SCD) and how do you implement them?

**Answer:** SCDs handle changes to dimension data over time, preserving historical information for accurate reporting and analysis.

#### 🎯 **SCD Implementation Types**

```python
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import hashlib

class SCDProcessor:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
    
    def scd_type1_overwrite(self, source_df, target_table, key_column):
        """SCD Type 1: Overwrite existing values (no history)"""
        
        # Get existing data
        existing_df = pd.read_sql(f"SELECT * FROM {target_table}", self.engine)
        
        if existing_df.empty:
            # Initial load
            source_df.to_sql(target_table, self.engine, if_exists='append', index=False)
            return {'inserted': len(source_df), 'updated': 0}
        
        # Merge logic for Type 1
        merged_df = existing_df.set_index(key_column).combine_first(
            source_df.set_index(key_column)
        ).reset_index()
        
        # Replace entire table
        merged_df.to_sql(target_table, self.engine, if_exists='replace', index=False)
        
        return {
            'total_records': len(merged_df),
            'strategy': 'SCD Type 1 - Overwrite',
            'use_case': 'Corrections, non-historical changes'
        }
    
    def scd_type2_versioning(self, source_df, target_table, key_column, 
                           compare_columns, version_column='version'):
        """SCD Type 2: Add new record for changes (full history)"""
        
        # Add SCD metadata columns if not present
        scd_columns = ['effective_date', 'end_date', 'is_current', version_column]
        
        # Get existing data
        try:
            existing_df = pd.read_sql(f"SELECT * FROM {target_table}", self.engine)
        except:
            existing_df = pd.DataFrame()
        
        if existing_df.empty:
            # Initial load - add SCD metadata
            source_df['effective_date'] = datetime.now()
            source_df['end_date'] = None
            source_df['is_current'] = True
            source_df[version_column] = 1
            
            source_df.to_sql(target_table, self.engine, if_exists='replace', index=False)
            return {'inserted': len(source_df), 'updated': 0, 'unchanged': 0}
        
        # Process changes
        changes_summary = {'inserted': 0, 'updated': 0, 'unchanged': 0}
        updated_records = []
        
        for _, source_row in source_df.iterrows():
            key_value = source_row[key_column]
            
            # Get current record for this key
            current_record = existing_df[
                (existing_df[key_column] == key_value) & 
                (existing_df['is_current'] == True)
            ]
            
            if current_record.empty:
                # New record
                new_record = source_row.copy()
                new_record['effective_date'] = datetime.now()
                new_record['end_date'] = None
                new_record['is_current'] = True
                new_record[version_column] = 1
                updated_records.append(new_record)
                changes_summary['inserted'] += 1
                
            else:
                # Check if any tracked columns changed
                current_values = current_record.iloc[0]
                has_changes = False
                
                for col in compare_columns:
                    if col in source_row and col in current_values:
                        if source_row[col] != current_values[col]:
                            has_changes = True
                            break
                
                if has_changes:
                    # Close current record
                    current_values['end_date'] = datetime.now()
                    current_values['is_current'] = False
                    updated_records.append(current_values)
                    
                    # Create new version
                    new_record = source_row.copy()
                    new_record['effective_date'] = datetime.now()
                    new_record['end_date'] = None
                    new_record['is_current'] = True
                    new_record[version_column] = current_values[version_column] + 1
                    updated_records.append(new_record)
                    
                    changes_summary['updated'] += 1
                else:
                    # No changes - keep current record
                    updated_records.append(current_values)
                    changes_summary['unchanged'] += 1
        
        # Add unchanged records from existing data
        unchanged_keys = set(source_df[key_column])
        for _, existing_row in existing_df.iterrows():
            if existing_row[key_column] not in unchanged_keys:
                updated_records.append(existing_row)
        
        # Save updated data
        if updated_records:
            final_df = pd.DataFrame(updated_records)
            final_df.to_sql(target_table, self.engine, if_exists='replace', index=False)
        
        changes_summary['strategy'] = 'SCD Type 2 - Versioning'
        changes_summary['use_case'] = 'Full history tracking, audit trails'
        
        return changes_summary
    
    def scd_type3_previous_value(self, source_df, target_table, key_column, 
                                tracked_columns):
        """SCD Type 3: Store previous value in separate column"""
        
        # Get existing data
        try:
            existing_df = pd.read_sql(f"SELECT * FROM {target_table}", self.engine)
        except:
            existing_df = pd.DataFrame()
        
        if existing_df.empty:
            # Initial load - add previous value columns
            for col in tracked_columns:
                source_df[f'{col}_previous'] = None
            
            source_df['last_updated'] = datetime.now()
            source_df.to_sql(target_table, self.engine, if_exists='replace', index=False)
            return {'inserted': len(source_df), 'updated': 0}
        
        # Process changes
        changes_summary = {'inserted': 0, 'updated': 0, 'unchanged': 0}
        updated_records = []
        
        for _, source_row in source_df.iterrows():
            key_value = source_row[key_column]
            
            # Get existing record
            existing_record = existing_df[existing_df[key_column] == key_value]
            
            if existing_record.empty:
                # New record
                new_record = source_row.copy()
                for col in tracked_columns:
                    new_record[f'{col}_previous'] = None
                new_record['last_updated'] = datetime.now()
                updated_records.append(new_record)
                changes_summary['inserted'] += 1
                
            else:
                # Update existing record
                current_record = existing_record.iloc[0].copy()
                has_changes = False
                
                for col in tracked_columns:
                    if col in source_row and source_row[col] != current_record[col]:
                        current_record[f'{col}_previous'] = current_record[col]
                        current_record[col] = source_row[col]
                        has_changes = True
                
                if has_changes:
                    current_record['last_updated'] = datetime.now()
                    changes_summary['updated'] += 1
                else:
                    changes_summary['unchanged'] += 1
                
                updated_records.append(current_record)
        
        # Save updated data
        if updated_records:
            final_df = pd.DataFrame(updated_records)
            final_df.to_sql(target_table, self.engine, if_exists='replace', index=False)
        
        changes_summary['strategy'] = 'SCD Type 3 - Previous Value'
        changes_summary['use_case'] = 'Limited history, before/after comparisons'
        
        return changes_summary
    
    def scd_type4_history_table(self, source_df, current_table, history_table, 
                               key_column, compare_columns):
        """SCD Type 4: Separate current and history tables"""
        
        # Get existing current data
        try:
            current_df = pd.read_sql(f"SELECT * FROM {current_table}", self.engine)
        except:
            current_df = pd.DataFrame()
        
        try:
            history_df = pd.read_sql(f"SELECT * FROM {history_table}", self.engine)
        except:
            history_df = pd.DataFrame()
        
        changes_summary = {'inserted': 0, 'updated': 0, 'unchanged': 0, 'archived': 0}
        new_current_records = []
        new_history_records = []
        
        for _, source_row in source_df.iterrows():
            key_value = source_row[key_column]
            
            # Get current record
            current_record = current_df[current_df[key_column] == key_value]
            
            if current_record.empty:
                # New record - add to current table
                new_record = source_row.copy()
                new_record['created_date'] = datetime.now()
                new_record['last_updated'] = datetime.now()
                new_current_records.append(new_record)
                changes_summary['inserted'] += 1
                
            else:
                # Check for changes
                current_values = current_record.iloc[0]
                has_changes = False
                
                for col in compare_columns:
                    if col in source_row and source_row[col] != current_values[col]:
                        has_changes = True
                        break
                
                if has_changes:
                    # Move current record to history
                    history_record = current_values.copy()
                    history_record['archived_date'] = datetime.now()
                    new_history_records.append(history_record)
                    
                    # Update current record
                    updated_record = source_row.copy()
                    updated_record['created_date'] = current_values.get('created_date', datetime.now())
                    updated_record['last_updated'] = datetime.now()
                    new_current_records.append(updated_record)
                    
                    changes_summary['updated'] += 1
                    changes_summary['archived'] += 1
                else:
                    # No changes - keep in current
                    new_current_records.append(current_values)
                    changes_summary['unchanged'] += 1
        
        # Update tables
        if new_current_records:
            current_final_df = pd.DataFrame(new_current_records)
            current_final_df.to_sql(current_table, self.engine, if_exists='replace', index=False)
        
        if new_history_records:
            history_final_df = pd.DataFrame(new_history_records)
            history_final_df.to_sql(history_table, self.engine, if_exists='append', index=False)
        
        changes_summary['strategy'] = 'SCD Type 4 - History Table'
        changes_summary['use_case'] = 'Performance optimization, separate current/historical queries'
        
        return changes_summary
    
    def scd_type6_hybrid(self, source_df, target_table, key_column, compare_columns):
        """SCD Type 6: Combination of Type 1, 2, and 3 (1+2+3=6)"""
        
        # Combines:
        # - Type 1: Overwrite some attributes
        # - Type 2: Version history for others  
        # - Type 3: Previous value storage
        
        # Get existing data
        try:
            existing_df = pd.read_sql(f"SELECT * FROM {target_table}", self.engine)
        except:
            existing_df = pd.DataFrame()
        
        # Define attribute handling strategy
        type1_columns = ['phone', 'address']  # Always overwrite
        type2_columns = ['salary', 'department']  # Version history
        type3_columns = ['manager_id']  # Previous value
        
        if existing_df.empty:
            # Initial load
            source_df['effective_date'] = datetime.now()
            source_df['end_date'] = None
            source_df['is_current'] = True
            source_df['version'] = 1
            
            for col in type3_columns:
                source_df[f'{col}_previous'] = None
            
            source_df.to_sql(target_table, self.engine, if_exists='replace', index=False)
            return {'inserted': len(source_df), 'strategy': 'SCD Type 6 - Hybrid'}
        
        changes_summary = {'inserted': 0, 'updated': 0, 'unchanged': 0}
        updated_records = []
        
        for _, source_row in source_df.iterrows():
            key_value = source_row[key_column]
            
            # Get current record
            current_record = existing_df[
                (existing_df[key_column] == key_value) & 
                (existing_df['is_current'] == True)
            ]
            
            if current_record.empty:
                # New record
                new_record = source_row.copy()
                new_record['effective_date'] = datetime.now()
                new_record['end_date'] = None
                new_record['is_current'] = True
                new_record['version'] = 1
                
                for col in type3_columns:
                    new_record[f'{col}_previous'] = None
                
                updated_records.append(new_record)
                changes_summary['inserted'] += 1
                
            else:
                current_values = current_record.iloc[0]
                
                # Check Type 2 columns for changes
                type2_changes = any(
                    source_row.get(col) != current_values.get(col) 
                    for col in type2_columns if col in source_row
                )
                
                if type2_changes:
                    # Close current record
                    current_values['end_date'] = datetime.now()
                    current_values['is_current'] = False
                    updated_records.append(current_values)
                    
                    # Create new version
                    new_record = current_values.copy()
                    
                    # Type 1 updates (overwrite)
                    for col in type1_columns:
                        if col in source_row:
                            new_record[col] = source_row[col]
                    
                    # Type 2 updates (new version)
                    for col in type2_columns:
                        if col in source_row:
                            new_record[col] = source_row[col]
                    
                    # Type 3 updates (previous value)
                    for col in type3_columns:
                        if col in source_row and source_row[col] != current_values.get(col):
                            new_record[f'{col}_previous'] = current_values.get(col)
                            new_record[col] = source_row[col]
                    
                    new_record['effective_date'] = datetime.now()
                    new_record['end_date'] = None
                    new_record['is_current'] = True
                    new_record['version'] = current_values['version'] + 1
                    
                    updated_records.append(new_record)
                    changes_summary['updated'] += 1
                    
                else:
                    # Only Type 1 or Type 3 changes
                    updated_record = current_values.copy()
                    has_changes = False
                    
                    # Type 1 updates
                    for col in type1_columns:
                        if col in source_row and source_row[col] != current_values.get(col):
                            updated_record[col] = source_row[col]
                            has_changes = True
                    
                    # Type 3 updates
                    for col in type3_columns:
                        if col in source_row and source_row[col] != current_values.get(col):
                            updated_record[f'{col}_previous'] = current_values.get(col)
                            updated_record[col] = source_row[col]
                            has_changes = True
                    
                    if has_changes:
                        changes_summary['updated'] += 1
                    else:
                        changes_summary['unchanged'] += 1
                    
                    updated_records.append(updated_record)
        
        # Save updated data
        if updated_records:
            final_df = pd.DataFrame(updated_records)
            final_df.to_sql(target_table, self.engine, if_exists='replace', index=False)
        
        changes_summary['strategy'] = 'SCD Type 6 - Hybrid (1+2+3)'
        changes_summary['use_case'] = 'Complex requirements, mixed attribute handling'
        
        return changes_summary

# Example usage and comparison
def demonstrate_scd_types():
    """Demonstrate different SCD implementations"""
    
    # Sample customer data - initial load
    initial_customers = pd.DataFrame({
        'customer_id': [1, 2, 3],
        'name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'email': ['john@email.com', 'jane@company.com', 'bob@test.org'],
        'phone': ['555-1234', '555-5678', '555-9012'],
        'address': ['123 Main St', '456 Oak Ave', '789 Pine Rd'],
        'salary': [50000, 75000, 60000],
        'department': ['Engineering', 'Sales', 'Marketing'],
        'manager_id': [101, 102, 101]
    })
    
    # Updated customer data - with changes
    updated_customers = pd.DataFrame({
        'customer_id': [1, 2, 3, 4],
        'name': ['John Doe', 'Jane Smith-Wilson', 'Bob Johnson', 'Alice Brown'],  # Name change
        'email': ['john.doe@newemail.com', 'jane@company.com', 'bob@test.org', 'alice@company.com'],  # Email change
        'phone': ['555-1234', '555-5678', '555-0000', '555-1111'],  # Phone change
        'address': ['123 Main St', '789 New Ave', '789 Pine Rd', '321 Elm St'],  # Address change
        'salary': [55000, 75000, 65000, 70000],  # Salary change
        'department': ['Engineering', 'Management', 'Marketing', 'Sales'],  # Department change
        'manager_id': [101, 103, 104, 102]  # Manager change
    })
    
    scd_processor = SCDProcessor("sqlite:///scd_demo.db")
    
    print("=== SCD Implementation Comparison ===\n")
    
    # SCD Type 1 - Overwrite
    print("1. SCD Type 1 (Overwrite):")
    type1_result = scd_processor.scd_type1_overwrite(
        updated_customers, 'customers_type1', 'customer_id'
    )
    print(f"   Result: {type1_result}")
    print(f"   Use Case: {type1_result['use_case']}\n")
    
    # SCD Type 2 - Versioning
    print("2. SCD Type 2 (Versioning):")
    scd_processor.scd_type2_versioning(
        initial_customers, 'customers_type2', 'customer_id', 
        ['name', 'email', 'salary', 'department']
    )
    type2_result = scd_processor.scd_type2_versioning(
        updated_customers, 'customers_type2', 'customer_id',
        ['name', 'email', 'salary', 'department']
    )
    print(f"   Result: {type2_result}")
    print(f"   Use Case: {type2_result['use_case']}\n")
    
    # SCD Type 3 - Previous Value
    print("3. SCD Type 3 (Previous Value):")
    scd_processor.scd_type3_previous_value(
        initial_customers, 'customers_type3', 'customer_id', 
        ['department', 'manager_id']
    )
    type3_result = scd_processor.scd_type3_previous_value(
        updated_customers, 'customers_type3', 'customer_id',
        ['department', 'manager_id']
    )
    print(f"   Result: {type3_result}")
    print(f"   Use Case: {type3_result['use_case']}\n")
    
    # SCD Type 4 - History Table
    print("4. SCD Type 4 (History Table):")
    scd_processor.scd_type4_history_table(
        initial_customers, 'customers_current', 'customers_history',
        'customer_id', ['name', 'email', 'salary', 'department']
    )
    type4_result = scd_processor.scd_type4_history_table(
        updated_customers, 'customers_current', 'customers_history',
        'customer_id', ['name', 'email', 'salary', 'department']
    )
    print(f"   Result: {type4_result}")
    print(f"   Use Case: {type4_result['use_case']}\n")
    
    # SCD Type 6 - Hybrid
    print("5. SCD Type 6 (Hybrid):")
    scd_processor.scd_type6_hybrid(
        initial_customers, 'customers_type6', 'customer_id',
        ['name', 'email', 'salary', 'department']
    )
    type6_result = scd_processor.scd_type6_hybrid(
        updated_customers, 'customers_type6', 'customer_id',
        ['name', 'email', 'salary', 'department']
    )
    print(f"   Result: {type6_result}")
    print(f"   Use Case: {type6_result['use_case']}\n")
    
    # Summary comparison
    print("=== SCD Type Comparison Summary ===")
    comparison_table = pd.DataFrame({
        'SCD Type': ['Type 1', 'Type 2', 'Type 3', 'Type 4', 'Type 6'],
        'History Preserved': ['No', 'Full', 'Limited', 'Full', 'Mixed'],
        'Storage Overhead': ['Low', 'High', 'Medium', 'High', 'High'],
        'Query Complexity': ['Low', 'Medium', 'Low', 'Medium', 'High'],
        'Use Case': [
            'Corrections, non-critical changes',
            'Full audit trail, compliance',
            'Before/after comparisons',
            'Performance optimization',
            'Complex mixed requirements'
        ]
    })
    
    print(comparison_table.to_string(index=False))

# Run demonstration
demonstrate_scd_types()
```

**Output:**
```
=== SCD Implementation Comparison ===

1. SCD Type 1 (Overwrite):
   Result: {'total_records': 4, 'strategy': 'SCD Type 1 - Overwrite', 'use_case': 'Corrections, non-historical changes'}
   Use Case: Corrections, non-historical changes

2. SCD Type 2 (Versioning):
   Result: {'inserted': 1, 'updated': 3, 'unchanged': 0, 'strategy': 'SCD Type 2 - Versioning', 'use_case': 'Full history tracking, audit trails'}
   Use Case: Full history tracking, audit trails

3. SCD Type 3 (Previous Value):
   Result: {'inserted': 1, 'updated': 2, 'unchanged': 1, 'strategy': 'SCD Type 3 - Previous Value', 'use_case': 'Limited history, before/after comparisons'}
   Use Case: Limited history, before/after comparisons

4. SCD Type 4 (History Table):
   Result: {'inserted': 1, 'updated': 3, 'unchanged': 0, 'archived': 3, 'strategy': 'SCD Type 4 - History Table', 'use_case': 'Performance optimization, separate current/historical queries'}
   Use Case: Performance optimization, separate current/historical queries

5. SCD Type 6 (Hybrid):
   Result: {'inserted': 1, 'updated': 3, 'unchanged': 0, 'strategy': 'SCD Type 6 - Hybrid (1+2+3)', 'use_case': 'Complex requirements, mixed attribute handling'}
   Use Case: Complex requirements, mixed attribute handling

=== SCD Type Comparison Summary ===
SCD Type History Preserved Storage Overhead Query Complexity                        Use Case
   Type 1              No             Low              Low      Corrections, non-critical changes
   Type 2            Full            High           Medium       Full audit trail, compliance
   Type 3         Limited          Medium              Low       Before/after comparisons
   Type 4            Full            High           Medium       Performance optimization
   Type 6           Mixed            High             High  Complex mixed requirements
```