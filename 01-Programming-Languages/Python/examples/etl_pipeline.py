"""
ETL Pipeline Example - Complete data processing workflow
"""

import pandas as pd
import logging
from typing import Dict, List, Optional
import boto3
from sqlalchemy import create_engine
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataPipeline:
    """Complete ETL pipeline for data processing"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.s3_client = boto3.client('s3') if config.get('use_s3') else None
        self.db_engine = create_engine(config['database_url']) if config.get('database_url') else None
        
    def extract_from_csv(self, file_path: str) -> pd.DataFrame:
        """Extract data from CSV file"""
        try:
            logger.info(f"Extracting data from {file_path}")
            df = pd.read_csv(file_path)
            logger.info(f"Extracted {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Failed to extract from CSV: {e}")
            raise
    
    def extract_from_s3(self, bucket: str, key: str) -> pd.DataFrame:
        """Extract data from S3 bucket"""
        try:
            logger.info(f"Extracting data from s3://{bucket}/{key}")
            obj = self.s3_client.get_object(Bucket=bucket, Key=key)
            df = pd.read_csv(obj['Body'])
            logger.info(f"Extracted {len(df)} records from S3")
            return df
        except Exception as e:
            logger.error(f"Failed to extract from S3: {e}")
            raise
    
    def extract_from_api(self, api_url: str, headers: Optional[Dict] = None) -> pd.DataFrame:
        """Extract data from REST API"""
        import requests
        
        try:
            logger.info(f"Extracting data from API: {api_url}")
            response = requests.get(api_url, headers=headers or {})
            response.raise_for_status()
            
            data = response.json()
            df = pd.DataFrame(data)
            logger.info(f"Extracted {len(df)} records from API")
            return df
        except Exception as e:
            logger.error(f"Failed to extract from API: {e}")
            raise
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform and clean data"""
        logger.info("Starting data transformation")
        
        # Data quality checks
        initial_count = len(df)
        
        # Remove duplicates
        df = df.drop_duplicates()
        logger.info(f"Removed {initial_count - len(df)} duplicate records")
        
        # Handle missing values
        numeric_columns = df.select_dtypes(include=['number']).columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        # Fill numeric nulls with median
        for col in numeric_columns:
            if df[col].isnull().any():
                median_val = df[col].median()
                df[col].fillna(median_val, inplace=True)
                logger.info(f"Filled {col} nulls with median: {median_val}")
        
        # Fill categorical nulls with mode
        for col in categorical_columns:
            if df[col].isnull().any():
                mode_val = df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown'
                df[col].fillna(mode_val, inplace=True)
                logger.info(f"Filled {col} nulls with mode: {mode_val}")
        
        # Data type conversions
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            logger.info("Converted date column to datetime")
        
        # Add calculated columns
        if 'revenue' in df.columns and 'cost' in df.columns:
            df['profit'] = df['revenue'] - df['cost']
            df['profit_margin'] = (df['profit'] / df['revenue']) * 100
            logger.info("Added calculated profit columns")
        
        # Add metadata
        df['processed_at'] = datetime.now()
        df['pipeline_version'] = self.config.get('version', '1.0')
        
        logger.info(f"Transformation complete. Final record count: {len(df)}")
        return df
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """Validate data quality"""
        logger.info("Starting data validation")
        
        validation_rules = [
            (len(df) > 0, "Dataset should not be empty"),
            (df.isnull().sum().sum() == 0, "No null values allowed after transformation"),
            (len(df.columns) >= self.config.get('min_columns', 1), "Minimum column count check")
        ]
        
        for rule, message in validation_rules:
            if not rule:
                logger.error(f"Validation failed: {message}")
                return False
            logger.info(f"Validation passed: {message}")
        
        return True
    
    def load_to_csv(self, df: pd.DataFrame, file_path: str):
        """Load data to CSV file"""
        try:
            logger.info(f"Loading data to CSV: {file_path}")
            df.to_csv(file_path, index=False)
            logger.info(f"Successfully loaded {len(df)} records to CSV")
        except Exception as e:
            logger.error(f"Failed to load to CSV: {e}")
            raise
    
    def load_to_database(self, df: pd.DataFrame, table_name: str):
        """Load data to database"""
        try:
            logger.info(f"Loading data to database table: {table_name}")
            df.to_sql(table_name, self.db_engine, if_exists='replace', index=False)
            logger.info(f"Successfully loaded {len(df)} records to database")
        except Exception as e:
            logger.error(f"Failed to load to database: {e}")
            raise
    
    def load_to_s3(self, df: pd.DataFrame, bucket: str, key: str):
        """Load data to S3 as CSV"""
        try:
            logger.info(f"Loading data to S3: s3://{bucket}/{key}")
            csv_buffer = df.to_csv(index=False)
            self.s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=csv_buffer,
                ContentType='text/csv'
            )
            logger.info(f"Successfully loaded {len(df)} records to S3")
        except Exception as e:
            logger.error(f"Failed to load to S3: {e}")
            raise
    
    def run_pipeline(self, source_config: Dict, target_config: Dict):
        """Execute the complete ETL pipeline"""
        try:
            logger.info("Starting ETL pipeline execution")
            
            # Extract phase
            if source_config['type'] == 'csv':
                raw_data = self.extract_from_csv(source_config['path'])
            elif source_config['type'] == 's3':
                raw_data = self.extract_from_s3(source_config['bucket'], source_config['key'])
            elif source_config['type'] == 'api':
                raw_data = self.extract_from_api(source_config['url'], source_config.get('headers'))
            else:
                raise ValueError(f"Unsupported source type: {source_config['type']}")
            
            # Transform phase
            processed_data = self.transform_data(raw_data)
            
            # Validate phase
            if not self.validate_data(processed_data):
                raise ValueError("Data validation failed")
            
            # Load phase
            if target_config['type'] == 'csv':
                self.load_to_csv(processed_data, target_config['path'])
            elif target_config['type'] == 'database':
                self.load_to_database(processed_data, target_config['table'])
            elif target_config['type'] == 's3':
                self.load_to_s3(processed_data, target_config['bucket'], target_config['key'])
            else:
                raise ValueError(f"Unsupported target type: {target_config['type']}")
            
            logger.info("ETL pipeline completed successfully")
            
            # Return summary statistics
            return {
                'status': 'success',
                'records_processed': len(processed_data),
                'columns': list(processed_data.columns),
                'processing_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'processing_time': datetime.now().isoformat()
            }

# Usage example
if __name__ == "__main__":
    # Configuration
    config = {
        'database_url': 'postgresql://user:password@localhost:5432/datawarehouse',
        'use_s3': True,
        'min_columns': 3,
        'version': '2.0'
    }
    
    # Source configuration
    source_config = {
        'type': 'csv',
        'path': 'data/raw_sales_data.csv'
    }
    
    # Target configuration
    target_config = {
        'type': 'database',
        'table': 'processed_sales'
    }
    
    # Execute pipeline
    pipeline = DataPipeline(config)
    result = pipeline.run_pipeline(source_config, target_config)
    
    print(f"Pipeline result: {json.dumps(result, indent=2)}")