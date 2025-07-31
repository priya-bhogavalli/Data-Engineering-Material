# DataOps Key Concepts

## 🎯 What is DataOps?
Methodology that combines DevOps practices with data engineering to improve data pipeline reliability, speed, and quality.

## 🏗️ Core Principles

### 1. Continuous Integration/Continuous Deployment (CI/CD)
```yaml
# .github/workflows/data-pipeline.yml
name: Data Pipeline CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest great-expectations
      
      - name: Run data quality tests
        run: |
          pytest tests/
          great_expectations checkpoint run data_quality_checkpoint
      
      - name: Deploy to staging
        if: github.ref == 'refs/heads/main'
        run: |
          python deploy.py --env staging
```

### 2. Infrastructure as Code
```python
# Terraform for data infrastructure
import boto3
from pulumi import export, ResourceOptions
import pulumi_aws as aws

# S3 bucket for data lake
data_lake_bucket = aws.s3.Bucket("data-lake",
    versioning=aws.s3.BucketVersioningArgs(enabled=True),
    server_side_encryption_configuration=aws.s3.BucketServerSideEncryptionConfigurationArgs(
        rule=aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
            apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
                sse_algorithm="AES256"
            )
        )
    )
)

# Glue job for ETL
glue_job = aws.glue.Job("etl-job",
    role_arn=glue_role.arn,
    command=aws.glue.JobCommandArgs(
        script_location=f"s3://{scripts_bucket.bucket}/etl_script.py",
        python_version="3"
    ),
    default_arguments={
        "--job-language": "python",
        "--enable-metrics": "",
        "--enable-continuous-cloudwatch-log": "true"
    }
)

export("data_lake_bucket", data_lake_bucket.bucket)
export("glue_job_name", glue_job.name)
```

### 3. Monitoring and Observability
```python
# Data pipeline monitoring
import logging
import time
from datadog import initialize, statsd
from great_expectations.core import ExpectationSuite

class DataPipelineMonitor:
    def __init__(self):
        initialize(api_key='your-api-key', app_key='your-app-key')
        self.logger = logging.getLogger(__name__)
    
    def monitor_pipeline_execution(self, pipeline_name):
        """Monitor pipeline execution with metrics"""
        start_time = time.time()
        
        try:
            # Execute pipeline
            result = self.execute_pipeline(pipeline_name)
            
            # Record success metrics
            statsd.increment(f'pipeline.{pipeline_name}.success')
            execution_time = time.time() - start_time
            statsd.histogram(f'pipeline.{pipeline_name}.duration', execution_time)
            
            self.logger.info(f"Pipeline {pipeline_name} completed successfully")
            return result
            
        except Exception as e:
            # Record failure metrics
            statsd.increment(f'pipeline.{pipeline_name}.failure')
            self.logger.error(f"Pipeline {pipeline_name} failed: {str(e)}")
            
            # Send alert
            self.send_alert(pipeline_name, str(e))
            raise
    
    def validate_data_quality(self, dataset, expectations_suite):
        """Validate data quality with Great Expectations"""
        context = self.get_ge_context()
        
        # Run validation
        results = context.run_validation_operator(
            "action_list_operator",
            assets_to_validate=[dataset],
            run_id=f"validation_{int(time.time())}"
        )
        
        # Record quality metrics
        success_rate = results.list_validation_results()[0].success
        statsd.gauge('data_quality.success_rate', success_rate)
        
        return results
```

### 4. Version Control for Data
```python
# Data versioning with DVC
import dvc.api
import pandas as pd
from datetime import datetime

class DataVersionControl:
    def __init__(self, repo_path):
        self.repo_path = repo_path
    
    def save_dataset_version(self, df, dataset_name, version_tag=None):
        """Save dataset with version control"""
        if version_tag is None:
            version_tag = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save data
        file_path = f"data/{dataset_name}_{version_tag}.parquet"
        df.to_parquet(file_path)
        
        # Add to DVC
        dvc.api.add(file_path)
        
        # Git commit
        import subprocess
        subprocess.run(["git", "add", f"{file_path}.dvc"])
        subprocess.run(["git", "commit", "-m", f"Add {dataset_name} version {version_tag}"])
        subprocess.run(["git", "tag", f"{dataset_name}-{version_tag}"])
        
        return version_tag
    
    def load_dataset_version(self, dataset_name, version_tag):
        """Load specific dataset version"""
        file_path = f"data/{dataset_name}_{version_tag}.parquet"
        
        with dvc.api.open(file_path, mode='rb') as f:
            return pd.read_parquet(f)
```

## 🔧 DataOps Tools & Practices

### Automated Testing
```python
# Data pipeline tests
import pytest
import pandas as pd
from unittest.mock import Mock

class TestDataPipeline:
    def test_data_transformation(self):
        """Test data transformation logic"""
        # Arrange
        input_data = pd.DataFrame({
            'customer_id': [1, 2, 3],
            'purchase_amount': [100, 200, 300]
        })
        
        # Act
        result = transform_customer_data(input_data)
        
        # Assert
        assert len(result) == 3
        assert 'customer_id' in result.columns
        assert result['purchase_amount'].sum() == 600
    
    def test_data_quality_checks(self):
        """Test data quality validation"""
        data = pd.DataFrame({
            'email': ['test@example.com', 'invalid-email', 'user@domain.com']
        })
        
        quality_results = validate_email_format(data)
        
        assert quality_results['valid_emails'] == 2
        assert quality_results['invalid_emails'] == 1
    
    @pytest.fixture
    def mock_database(self):
        """Mock database for testing"""
        db = Mock()
        db.execute.return_value = [{'count': 100}]
        return db
```

### Environment Management
```yaml
# docker-compose.yml for local development
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: dataops_dev
      POSTGRES_USER: dev_user
      POSTGRES_PASSWORD: dev_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  airflow:
    image: apache/airflow:2.5.0
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql://dev_user:dev_pass@postgres:5432/dataops_dev
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
    ports:
      - "8080:8080"
    depends_on:
      - postgres

volumes:
  postgres_data:
```

## 🎯 Benefits
- Faster deployment cycles
- Improved data quality
- Reduced manual errors
- Better collaboration
- Automated monitoring
- Reproducible results

## 🔧 Best Practices
- Implement comprehensive testing
- Use version control for everything
- Automate quality checks
- Monitor pipeline performance
- Document processes and decisions
- Practice continuous improvement

## 🛠️ Tools & Technologies
- **CI/CD**: Jenkins, GitHub Actions, GitLab CI
- **Infrastructure**: Terraform, Pulumi, CloudFormation
- **Monitoring**: Datadog, Prometheus, Grafana
- **Testing**: pytest, Great Expectations
- **Orchestration**: Apache Airflow, Prefect
- **Version Control**: Git, DVC