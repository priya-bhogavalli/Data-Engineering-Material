"""
Data Pipeline Example - ETL Process with Python
"""

import pandas as pd
import logging
from typing import Dict, List
import boto3
from sqlalchemy import create_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataPipeline:
    """Simple ETL pipeline for data processing"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.s3_client = boto3.client('s3')
        self.db_engine = create_engine(config['database_url'])
    
    def extract_from_s3(self, bucket: str, key: str) -> pd.DataFrame:
        """Extract data from S3 bucket"""
        try:
            logger.info(f"Extracting data from s3://{bucket}/{key}")
            obj = self.s3_client.get_object(Bucket=bucket, Key=key)
            df = pd.read_csv(obj['Body'])
            logger.info(f"Extracted {len(df)} records")
            return df
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            raise
    
    def transform_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform and clean data"""
        logger.info("Starting data transformation")
        
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values
        df = df.fillna(method='forward')
        
        # Data type conversions
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Add calculated columns
        if 'revenue' in df.columns and 'cost' in df.columns:
            df['profit'] = df['revenue'] - df['cost']
        
        logger.info(f"Transformation complete. {len(df)} records processed")
        return df
    
    def load_to_database(self, df: pd.DataFrame, table_name: str):
        """Load data to database"""
        try:
            logger.info(f"Loading data to table: {table_name}")
            df.to_sql(table_name, self.db_engine, if_exists='replace', index=False)
            logger.info(f"Successfully loaded {len(df)} records")
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise
    
    def run_pipeline(self, bucket: str, key: str, table_name: str):
        """Execute the complete ETL pipeline"""
        try:
            # Extract
            raw_data = self.extract_from_s3(bucket, key)
            
            # Transform
            processed_data = self.transform_data(raw_data)
            
            # Load
            self.load_to_database(processed_data, table_name)
            
            logger.info("Pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            raise

# Usage example
if __name__ == "__main__":
    config = {
        'database_url': 'postgresql://user:password@localhost:5432/datawarehouse'
    }
    
    pipeline = DataPipeline(config)
    pipeline.run_pipeline(
        bucket='my-data-bucket',
        key='raw-data/sales_data.csv',
        table_name='processed_sales'
    )