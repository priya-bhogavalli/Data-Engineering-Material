# Complete Data Engineering Pipeline with Apache Airflow
# This DAG demonstrates a production-ready data pipeline with error handling,
# data quality checks, monitoring, and notifications

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.dummy import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sensors.filesystem import FileSensor
from airflow.models import Variable
from datetime import datetime, timedelta
import pandas as pd
import logging
import json
import os

# =============================================================================
# DAG Configuration
# =============================================================================

default_args = {
    'owner': 'data-engineering-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['data-team@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,
    'catchup': False
}

dag = DAG(
    'complete_data_pipeline',
    default_args=default_args,
    description='Complete data engineering pipeline with quality checks',
    schedule_interval='@daily',
    tags=['production', 'etl', 'data-quality'],
    doc_md="""
    # Complete Data Engineering Pipeline
    
    This DAG implements a comprehensive data pipeline including:
    - Data extraction from multiple sources
    - Data quality validation
    - Data transformation and enrichment
    - Loading to data warehouse
    - Monitoring and alerting
    
    ## Pipeline Flow
    1. Wait for input files
    2. Extract data from sources
    3. Run data quality checks
    4. Transform and enrich data
    5. Load to warehouse
    6. Send notifications
    """
)

# =============================================================================
# Utility Functions
# =============================================================================

def get_config(key, default=None):
    """Get configuration from Airflow Variables"""
    try:
        return Variable.get(key)
    except KeyError:
        if default is not None:
            return default
        raise ValueError(f"Required configuration '{key}' not found")

def log_task_info(task_name, **context):
    """Log task execution information"""
    execution_date = context['execution_date']
    dag_run_id = context['dag_run'].run_id
    
    logging.info(f"Task: {task_name}")
    logging.info(f"Execution Date: {execution_date}")
    logging.info(f"DAG Run ID: {dag_run_id}")

# =============================================================================
# Data Extraction Functions
# =============================================================================

def extract_customer_data(**context):
    """Extract customer data from source database"""
    log_task_info("extract_customer_data", **context)
    
    try:
        # Get database connection
        postgres_hook = PostgresHook(postgres_conn_id='source_db')
        
        # Extract customer data
        sql_query = """
            SELECT 
                customer_id,
                customer_name,
                email,
                registration_date,
                customer_segment,
                lifetime_value,
                is_active
            FROM customers
            WHERE updated_date >= %s
        """
        
        execution_date = context['execution_date'].strftime('%Y-%m-%d')
        df = postgres_hook.get_pandas_df(sql_query, parameters=[execution_date])
        
        # Save to temporary location
        output_path = f"/tmp/customers_{context['ds']}.csv"
        df.to_csv(output_path, index=False)
        
        logging.info(f"Extracted {len(df)} customer records")
        
        # Return metadata
        return {
            'file_path': output_path,
            'record_count': len(df),
            'extraction_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Customer data extraction failed: {str(e)}")
        raise

def extract_order_data(**context):
    """Extract order data from source database"""
    log_task_info("extract_order_data", **context)
    
    try:
        postgres_hook = PostgresHook(postgres_conn_id='source_db')
        
        sql_query = """
            SELECT 
                order_id,
                customer_id,
                order_date,
                order_amount,
                product_category,
                payment_method,
                order_status
            FROM orders
            WHERE order_date = %s
        """
        
        execution_date = context['execution_date'].strftime('%Y-%m-%d')
        df = postgres_hook.get_pandas_df(sql_query, parameters=[execution_date])
        
        output_path = f"/tmp/orders_{context['ds']}.csv"
        df.to_csv(output_path, index=False)
        
        logging.info(f"Extracted {len(df)} order records")
        
        return {
            'file_path': output_path,
            'record_count': len(df),
            'extraction_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Order data extraction failed: {str(e)}")
        raise

# =============================================================================
# Data Quality Functions
# =============================================================================

def run_data_quality_checks(**context):
    """Run comprehensive data quality checks"""
    log_task_info("data_quality_checks", **context)
    
    # Get file paths from previous tasks
    customer_metadata = context['ti'].xcom_pull(task_ids='extract_customer_data')
    order_metadata = context['ti'].xcom_pull(task_ids='extract_order_data')
    
    quality_results = {
        'customer_data': {},
        'order_data': {},
        'overall_score': 0,
        'passed': False
    }
    
    try:
        # Check customer data quality
        customer_df = pd.read_csv(customer_metadata['file_path'])
        quality_results['customer_data'] = check_data_quality(
            customer_df, 
            'customer_data',
            required_columns=['customer_id', 'customer_name', 'email'],
            unique_columns=['customer_id', 'email']
        )
        
        # Check order data quality
        order_df = pd.read_csv(order_metadata['file_path'])
        quality_results['order_data'] = check_data_quality(
            order_df,
            'order_data',
            required_columns=['order_id', 'customer_id', 'order_amount'],
            unique_columns=['order_id'],
            numeric_columns=['order_amount']
        )
        
        # Calculate overall quality score
        customer_score = quality_results['customer_data']['quality_score']
        order_score = quality_results['order_data']['quality_score']
        overall_score = (customer_score + order_score) / 2
        
        quality_results['overall_score'] = overall_score
        quality_results['passed'] = overall_score >= 80  # 80% threshold
        
        logging.info(f"Data quality check completed. Overall score: {overall_score}%")
        
        # Store results for downstream tasks
        context['ti'].xcom_push(key='quality_results', value=quality_results)
        
        return quality_results
        
    except Exception as e:
        logging.error(f"Data quality check failed: {str(e)}")
        raise

def check_data_quality(df, dataset_name, required_columns=None, unique_columns=None, numeric_columns=None):
    """Perform data quality checks on a DataFrame"""
    
    results = {
        'dataset_name': dataset_name,
        'total_records': len(df),
        'checks': {},
        'quality_score': 0
    }
    
    passed_checks = 0
    total_checks = 0
    
    # Null value checks
    if required_columns:
        for column in required_columns:
            if column in df.columns:
                null_count = df[column].isnull().sum()
                null_percentage = (null_count / len(df)) * 100
                
                check_passed = null_percentage < 5  # Less than 5% nulls allowed
                results['checks'][f'{column}_null_check'] = {
                    'null_count': null_count,
                    'null_percentage': round(null_percentage, 2),
                    'passed': check_passed
                }
                
                if check_passed:
                    passed_checks += 1
                total_checks += 1
    
    # Uniqueness checks
    if unique_columns:
        for column in unique_columns:
            if column in df.columns:
                duplicate_count = df[column].duplicated().sum()
                
                check_passed = duplicate_count == 0
                results['checks'][f'{column}_uniqueness_check'] = {
                    'duplicate_count': duplicate_count,
                    'passed': check_passed
                }
                
                if check_passed:
                    passed_checks += 1
                total_checks += 1
    
    # Numeric range checks
    if numeric_columns:
        for column in numeric_columns:
            if column in df.columns and pd.api.types.is_numeric_dtype(df[column]):
                negative_count = (df[column] < 0).sum()
                
                check_passed = negative_count == 0  # No negative values
                results['checks'][f'{column}_range_check'] = {
                    'negative_count': negative_count,
                    'min_value': df[column].min(),
                    'max_value': df[column].max(),
                    'passed': check_passed
                }
                
                if check_passed:
                    passed_checks += 1
                total_checks += 1
    
    # Calculate quality score
    if total_checks > 0:
        results['quality_score'] = (passed_checks / total_checks) * 100
    else:
        results['quality_score'] = 100
    
    return results

def decide_pipeline_path(**context):
    """Decide whether to continue pipeline based on data quality"""
    
    quality_results = context['ti'].xcom_pull(key='quality_results')
    
    if quality_results['passed']:
        logging.info("Data quality checks passed. Continuing pipeline.")
        return 'transform_data'
    else:
        logging.warning("Data quality checks failed. Stopping pipeline.")
        return 'data_quality_failed'

# =============================================================================
# Data Transformation Functions
# =============================================================================

def transform_data(**context):
    """Transform and enrich the extracted data"""
    log_task_info("transform_data", **context)
    
    try:
        # Get file paths from extraction tasks
        customer_metadata = context['ti'].xcom_pull(task_ids='extract_customer_data')
        order_metadata = context['ti'].xcom_pull(task_ids='extract_order_data')
        
        # Load data
        customer_df = pd.read_csv(customer_metadata['file_path'])
        order_df = pd.read_csv(order_metadata['file_path'])
        
        # Transform customer data
        customer_df['customer_name'] = customer_df['customer_name'].str.title()
        customer_df['email'] = customer_df['email'].str.lower()
        customer_df['registration_year'] = pd.to_datetime(customer_df['registration_date']).dt.year
        
        # Transform order data
        order_df['order_date'] = pd.to_datetime(order_df['order_date'])
        order_df['order_year'] = order_df['order_date'].dt.year
        order_df['order_month'] = order_df['order_date'].dt.month
        order_df['order_day_of_week'] = order_df['order_date'].dt.day_name()
        
        # Create enriched dataset by joining
        enriched_df = order_df.merge(
            customer_df[['customer_id', 'customer_name', 'customer_segment']], 
            on='customer_id', 
            how='left'
        )
        
        # Add calculated fields
        enriched_df['is_high_value'] = enriched_df['order_amount'] > 100
        enriched_df['processed_timestamp'] = datetime.now()
        
        # Save transformed data
        customer_output = f"/tmp/transformed_customers_{context['ds']}.csv"
        order_output = f"/tmp/transformed_orders_{context['ds']}.csv"
        enriched_output = f"/tmp/enriched_orders_{context['ds']}.csv"
        
        customer_df.to_csv(customer_output, index=False)
        order_df.to_csv(order_output, index=False)
        enriched_df.to_csv(enriched_output, index=False)
        
        logging.info(f"Data transformation completed:")
        logging.info(f"- Customers: {len(customer_df)} records")
        logging.info(f"- Orders: {len(order_df)} records")
        logging.info(f"- Enriched: {len(enriched_df)} records")
        
        return {
            'customer_file': customer_output,
            'order_file': order_output,
            'enriched_file': enriched_output,
            'transformation_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Data transformation failed: {str(e)}")
        raise

# =============================================================================
# Data Loading Functions
# =============================================================================

def load_to_warehouse(**context):
    """Load transformed data to data warehouse"""
    log_task_info("load_to_warehouse", **context)
    
    try:
        # Get transformed data paths
        transform_metadata = context['ti'].xcom_pull(task_ids='transform_data')
        
        # Get warehouse connection
        postgres_hook = PostgresHook(postgres_conn_id='warehouse_db')
        
        # Load customer data
        customer_df = pd.read_csv(transform_metadata['customer_file'])
        postgres_hook.insert_rows(
            table='dim_customers',
            rows=customer_df.values.tolist(),
            target_fields=customer_df.columns.tolist(),
            replace=True
        )
        
        # Load order data
        order_df = pd.read_csv(transform_metadata['order_file'])
        postgres_hook.insert_rows(
            table='fact_orders',
            rows=order_df.values.tolist(),
            target_fields=order_df.columns.tolist(),
            replace=False
        )
        
        # Load enriched data
        enriched_df = pd.read_csv(transform_metadata['enriched_file'])
        postgres_hook.insert_rows(
            table='fact_enriched_orders',
            rows=enriched_df.values.tolist(),
            target_fields=enriched_df.columns.tolist(),
            replace=False
        )
        
        logging.info("Data loading to warehouse completed successfully")
        
        return {
            'customers_loaded': len(customer_df),
            'orders_loaded': len(order_df),
            'enriched_loaded': len(enriched_df),
            'load_timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Data loading failed: {str(e)}")
        raise

# =============================================================================
# Monitoring and Notification Functions
# =============================================================================

def generate_pipeline_report(**context):
    """Generate comprehensive pipeline execution report"""
    log_task_info("generate_report", **context)
    
    try:
        # Collect metadata from all tasks
        customer_metadata = context['ti'].xcom_pull(task_ids='extract_customer_data')
        order_metadata = context['ti'].xcom_pull(task_ids='extract_order_data')
        quality_results = context['ti'].xcom_pull(key='quality_results')
        transform_metadata = context['ti'].xcom_pull(task_ids='transform_data')
        load_metadata = context['ti'].xcom_pull(task_ids='load_to_warehouse')
        
        # Create comprehensive report
        report = {
            'pipeline_execution': {
                'dag_id': context['dag'].dag_id,
                'execution_date': context['execution_date'].isoformat(),
                'dag_run_id': context['dag_run'].run_id,
                'status': 'SUCCESS'
            },
            'extraction_summary': {
                'customers_extracted': customer_metadata['record_count'],
                'orders_extracted': order_metadata['record_count'],
                'extraction_timestamp': customer_metadata['extraction_timestamp']
            },
            'data_quality_summary': {
                'overall_score': quality_results['overall_score'],
                'passed': quality_results['passed'],
                'customer_quality_score': quality_results['customer_data']['quality_score'],
                'order_quality_score': quality_results['order_data']['quality_score']
            },
            'transformation_summary': {
                'transformation_timestamp': transform_metadata['transformation_timestamp']
            },
            'loading_summary': {
                'customers_loaded': load_metadata['customers_loaded'],
                'orders_loaded': load_metadata['orders_loaded'],
                'enriched_loaded': load_metadata['enriched_loaded'],
                'load_timestamp': load_metadata['load_timestamp']
            }
        }
        
        # Save report
        report_path = f"/tmp/pipeline_report_{context['ds']}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logging.info(f"Pipeline report generated: {report_path}")
        
        # Store report for email notification
        context['ti'].xcom_push(key='pipeline_report', value=report)
        
        return report
        
    except Exception as e:
        logging.error(f"Report generation failed: {str(e)}")
        raise

def cleanup_temp_files(**context):
    """Clean up temporary files created during pipeline execution"""
    log_task_info("cleanup", **context)
    
    try:
        # List of temporary files to clean up
        temp_files = [
            f"/tmp/customers_{context['ds']}.csv",
            f"/tmp/orders_{context['ds']}.csv",
            f"/tmp/transformed_customers_{context['ds']}.csv",
            f"/tmp/transformed_orders_{context['ds']}.csv",
            f"/tmp/enriched_orders_{context['ds']}.csv",
            f"/tmp/pipeline_report_{context['ds']}.json"
        ]
        
        cleaned_files = 0
        for file_path in temp_files:
            if os.path.exists(file_path):
                os.remove(file_path)
                cleaned_files += 1
                logging.info(f"Cleaned up: {file_path}")
        
        logging.info(f"Cleanup completed. Removed {cleaned_files} temporary files.")
        
    except Exception as e:
        logging.warning(f"Cleanup failed (non-critical): {str(e)}")

# =============================================================================
# Task Definitions
# =============================================================================

# File sensor to wait for input data
wait_for_input = FileSensor(
    task_id='wait_for_input_files',
    filepath='/data/input/{{ ds }}/ready.flag',
    fs_conn_id='fs_default',
    poke_interval=60,
    timeout=3600,
    dag=dag
)

# Data extraction tasks
extract_customers = PythonOperator(
    task_id='extract_customer_data',
    python_callable=extract_customer_data,
    dag=dag
)

extract_orders = PythonOperator(
    task_id='extract_order_data',
    python_callable=extract_order_data,
    dag=dag
)

# Data quality check
quality_check = PythonOperator(
    task_id='data_quality_check',
    python_callable=run_data_quality_checks,
    dag=dag
)

# Quality gate decision
quality_gate = BranchPythonOperator(
    task_id='quality_gate',
    python_callable=decide_pipeline_path,
    dag=dag
)

# Data transformation
transform = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag
)

# Data loading
load_warehouse = PythonOperator(
    task_id='load_to_warehouse',
    python_callable=load_to_warehouse,
    dag=dag
)

# Quality failure handling
quality_failed = DummyOperator(
    task_id='data_quality_failed',
    dag=dag
)

# Report generation
generate_report = PythonOperator(
    task_id='generate_pipeline_report',
    python_callable=generate_pipeline_report,
    trigger_rule='none_failed_or_skipped',
    dag=dag
)

# Success notification
success_email = EmailOperator(
    task_id='send_success_notification',
    to=['data-team@company.com'],
    subject='✅ Data Pipeline Completed Successfully - {{ ds }}',
    html_content="""
    <h2>Data Pipeline Execution Report</h2>
    <p><strong>Status:</strong> ✅ SUCCESS</p>
    <p><strong>Execution Date:</strong> {{ ds }}</p>
    <p><strong>DAG Run ID:</strong> {{ dag_run.run_id }}</p>
    
    <h3>Summary</h3>
    <ul>
        <li>Customers Processed: {{ ti.xcom_pull(key='pipeline_report')['extraction_summary']['customers_extracted'] }}</li>
        <li>Orders Processed: {{ ti.xcom_pull(key='pipeline_report')['extraction_summary']['orders_extracted'] }}</li>
        <li>Data Quality Score: {{ ti.xcom_pull(key='pipeline_report')['data_quality_summary']['overall_score'] }}%</li>
    </ul>
    
    <p>Pipeline completed successfully. All data has been loaded to the warehouse.</p>
    """,
    dag=dag
)

# Cleanup task
cleanup = PythonOperator(
    task_id='cleanup_temp_files',
    python_callable=cleanup_temp_files,
    trigger_rule='all_done',  # Run regardless of upstream success/failure
    dag=dag
)

# =============================================================================
# Task Dependencies
# =============================================================================

# Main pipeline flow
wait_for_input >> [extract_customers, extract_orders]
[extract_customers, extract_orders] >> quality_check
quality_check >> quality_gate
quality_gate >> [transform, quality_failed]
transform >> load_warehouse
load_warehouse >> generate_report
generate_report >> success_email
success_email >> cleanup

# Cleanup runs after everything else
quality_failed >> cleanup