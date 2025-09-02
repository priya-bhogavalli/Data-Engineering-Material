"""
Essential Python Examples for Data Engineering
Minimal, focused code snippets demonstrating key concepts
"""

import pandas as pd
import logging
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Basic ETL Pattern
def simple_etl():
    """Minimal ETL example"""
    # Extract
    data = pd.read_csv('input.csv')
    
    # Transform
    data['processed'] = data['value'] * 2
    data = data.dropna()
    
    # Load
    data.to_csv('output.csv', index=False)
    logger.info(f"Processed {len(data)} records")

# 2. Error Handling Pattern
def safe_processing(data: List[Dict]) -> List[Dict]:
    """Process data with error handling"""
    results = []
    for item in data:
        try:
            processed = transform_item(item)
            results.append(processed)
        except Exception as e:
            logger.error(f"Failed to process {item}: {e}")
    return results

def transform_item(item: Dict) -> Dict:
    """Transform single item"""
    return {
        'id': item['id'],
        'value': item['value'] * 2,
        'category': item.get('category', 'unknown')
    }

# 3. Batch Processing Pattern
def process_in_batches(data: List, batch_size: int = 1000):
    """Process large datasets in batches"""
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        process_batch(batch)
        logger.info(f"Processed batch {i//batch_size + 1}")

def process_batch(batch: List):
    """Process a single batch"""
    # Simulate processing
    processed = [item for item in batch if item.get('valid', True)]
    return processed

# 4. Configuration Pattern
class PipelineConfig:
    """Simple configuration class"""
    def __init__(self):
        self.input_path = 'data/input.csv'
        self.output_path = 'data/output.csv'
        self.batch_size = 1000
        self.max_retries = 3

# 5. Database Connection Pattern
def get_data_from_db(query: str, connection_string: str) -> pd.DataFrame:
    """Get data from database"""
    import sqlalchemy as sa
    engine = sa.create_engine(connection_string)
    return pd.read_sql(query, engine)

def save_data_to_db(df: pd.DataFrame, table: str, connection_string: str):
    """Save data to database"""
    import sqlalchemy as sa
    engine = sa.create_engine(connection_string)
    df.to_sql(table, engine, if_exists='append', index=False)

# 6. Data Validation Pattern
def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic data validation"""
    # Check required columns
    required_cols = ['id', 'value', 'date']
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")
    
    # Remove invalid records
    df = df.dropna(subset=required_cols)
    df = df[df['value'] > 0]  # Business rule
    
    return df

# Usage Examples
if __name__ == "__main__":
    # Example data
    sample_data = [
        {'id': 1, 'value': 10, 'category': 'A'},
        {'id': 2, 'value': 20, 'category': 'B'},
        {'id': 3, 'value': 30}  # Missing category
    ]
    
    # Process data
    results = safe_processing(sample_data)
    print(f"Processed {len(results)} items")
    
    # Batch processing
    large_data = [{'id': i, 'value': i*10} for i in range(5000)]
    process_in_batches(large_data, batch_size=1000)