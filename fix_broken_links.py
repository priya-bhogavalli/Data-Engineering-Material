#!/usr/bin/env python3
"""
Script to fix the most critical broken links in the repository.
This script will update markdown files to fix broken internal links.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

def fix_links_in_file(file_path: Path, link_replacements: Dict[str, str]) -> int:
    """Fix broken links in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_made = 0
        
        for old_link, new_link in link_replacements.items():
            if old_link in content:
                content = content.replace(old_link, new_link)
                fixes_made += 1
                print(f"  Fixed: {old_link} -> {new_link}")
        
        if fixes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated {file_path} with {fixes_made} fixes")
        
        return fixes_made
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

def main():
    """Main function to fix broken links."""
    print("=" * 80)
    print("FIXING BROKEN LINKS IN REPOSITORY")
    print("=" * 80)
    
    # Define link replacements for common broken links
    link_replacements = {
        # Non-existent directories
        "./by-skill-area/": "./Core-Data-Engineering/",
        "./interview-simulator/": "./docs/INTERVIEW_QUESTIONS_MASTER_INDEX.md",
        "./by-skill-area/python/": "./Core-Data-Engineering/Programming-Languages/Python/",
        "./by-skill-area/sql/": "./Core-Data-Engineering/Programming-Languages/SQL/",
        "./by-skill-area/spark/": "./Core-Data-Engineering/Data-Processing/Apache-Spark/",
        "./by-skill-area/cloud/": "./Core-Data-Engineering/Cloud/",
        "./by-skill-area/architecture/": "./Core-Data-Engineering/Data-Architecture/",
        
        # Interview simulator links
        "./interview-simulator/entry-level-scenarios.md": "./docs/INTERVIEW_QUESTIONS_MASTER_INDEX.md",
        "./interview-simulator/system-design-scenarios.md": "./docs/INTERVIEW_QUESTIONS_MASTER_INDEX.md",
        "./interview-simulator/senior-level-scenarios.md": "./docs/INTERVIEW_QUESTIONS_MASTER_INDEX.md",
        "./interview-simulator/big-tech-scenarios.md": "./docs/INTERVIEW_QUESTIONS_MASTER_INDEX.md",
        
        # Missing quick-prep files
        "./quick-prep/essentials-for-beginners.md": "./quick-prep/emergency-prep.md",
        "./quick-prep/advanced-concepts.md": "./quick-prep/fundamentals-review.md",
        "./quick-prep/one-week-plan.md": "./quick-prep/emergency-prep.md",
        "./quick-prep/system-design-patterns.md": "./quick-prep/fundamentals-review.md",
        "./quick-prep/troubleshooting-scenarios.md": "./quick-prep/emergency-prep.md",
        
        # Missing comprehensive files
        "./COMPREHENSIVE_STUDY_PLAN.md": "./docs/COMPREHENSIVE_NAVIGATION_GUIDE.md",
        
        # Fix specific interview question file names that exist but with different names
        # These are based on what we found in the actual directories
        
        # Core Data Engineering fixes - point to directories instead of missing files
        "./Core-Data-Engineering/Programming-Languages/Python/PYTHON_KEY_CONCEPTS.md": "./Core-Data-Engineering/Programming-Languages/Python/",
        "./Core-Data-Engineering/Programming-Languages/SQL/SQL_KEY_CONCEPTS.md": "./Core-Data-Engineering/Programming-Languages/SQL/",
        "./Core-Data-Engineering/Programming-Languages/PySpark/PYSPARK_KEY_CONCEPTS.md": "./Core-Data-Engineering/Programming-Languages/PySpark/",
        "./Core-Data-Engineering/Programming-Languages/PySpark/PYSPARK_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Programming-Languages/PySpark/",
        "./Core-Data-Engineering/Programming-Languages/PySpark/PYSPARK_BEST_PRACTICES.md": "./Core-Data-Engineering/Programming-Languages/PySpark/",
        
        # Cloud fixes
        "./Core-Data-Engineering/Cloud/AWS/AWS_COMPREHENSIVE_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Cloud/AWS/",
        "./Core-Data-Engineering/Cloud/AWS/AWS_COMPREHENSIVE_KEY_CONCEPTS.md": "./Core-Data-Engineering/Cloud/AWS/",
        "./Core-Data-Engineering/Cloud/AWS/AWS_BEST_PRACTICES.md": "./Core-Data-Engineering/Cloud/AWS/",
        "./Core-Data-Engineering/Cloud/Azure/AZURE_COMPREHENSIVE_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Cloud/Azure/",
        "./Core-Data-Engineering/Cloud/Azure/AZURE_KEY_CONCEPTS.md": "./Core-Data-Engineering/Cloud/Azure/",
        "./Core-Data-Engineering/Cloud/GCP/GCP_COMPREHENSIVE_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Cloud/GCP/",
        "./Core-Data-Engineering/Cloud/GCP/GCP_KEY_CONCEPTS.md": "./Core-Data-Engineering/Cloud/GCP/",
        "./Core-Data-Engineering/Cloud/CLOUD_KEY_CONCEPTS.md": "./Core-Data-Engineering/Cloud/",
        "./Core-Data-Engineering/Cloud/CLOUD_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Cloud/",
        "./Core-Data-Engineering/Cloud/CLOUD_SERVICES_COMPARISON_TABLE.md": "./Core-Data-Engineering/Cloud/",
        
        # Database fixes
        "./Core-Data-Engineering/Databases/PostgreSQL/POSTGRESQL_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/PostgreSQL/",
        "./Core-Data-Engineering/Databases/PostgreSQL/POSTGRESQL_KEY_CONCEPTS.md": "./Core-Data-Engineering/Databases/PostgreSQL/",
        "./Core-Data-Engineering/Databases/PostgreSQL/POSTGRESQL_BEST_PRACTICES.md": "./Core-Data-Engineering/Databases/PostgreSQL/",
        "./Core-Data-Engineering/Databases/MySQL/MYSQL_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/MySQL/",
        "./Core-Data-Engineering/Databases/Oracle/ORACLE_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/Oracle/",
        "./Core-Data-Engineering/Databases/NoSQL/MongoDB/MONGODB_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/NoSQL/MongoDB/",
        "./Core-Data-Engineering/Databases/NoSQL/MongoDB/MONGODB_KEY_CONCEPTS.md": "./Core-Data-Engineering/Databases/NoSQL/MongoDB/",
        "./Core-Data-Engineering/Databases/NoSQL/Redis/REDIS_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/NoSQL/Redis/",
        "./Core-Data-Engineering/Databases/NoSQL/Redis/REDIS_KEY_CONCEPTS.md": "./Core-Data-Engineering/Databases/NoSQL/Redis/",
        "./Core-Data-Engineering/Databases/NoSQL/Cassandra/CASSANDRA_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/NoSQL/Cassandra/",
        "./Core-Data-Engineering/Databases/NoSQL/DynamoDB/DYNAMODB_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/NoSQL/DynamoDB/",
        "./Core-Data-Engineering/Databases/Search-Engines/Elasticsearch/ELASTICSEARCH_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/Search-Engines/Elasticsearch/",
        "./Core-Data-Engineering/Databases/Search-Engines/Elasticsearch/ELASTICSEARCH_KEY_CONCEPTS.md": "./Core-Data-Engineering/Databases/Search-Engines/Elasticsearch/",
        "./Core-Data-Engineering/Databases/Athena/ATHENA_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/Athena/",
        "./Core-Data-Engineering/Databases/DATABASES_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Databases/",
        
        # Data Processing fixes
        "./Core-Data-Engineering/Data-Processing/Apache-Spark/SPARK_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/Apache-Spark/",
        "./Core-Data-Engineering/Data-Processing/Apache-Spark/SPARK_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Processing/Apache-Spark/",
        "./Core-Data-Engineering/Data-Processing/Apache-Spark/SPARK_BEST_PRACTICES.md": "./Core-Data-Engineering/Data-Processing/Apache-Spark/",
        "./Core-Data-Engineering/Data-Processing/Apache-Spark/SPARK_BIG4_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/Apache-Spark/",
        "./Core-Data-Engineering/Data-Processing/Databricks/DATABRICKS_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/Databricks/",
        "./Core-Data-Engineering/Data-Processing/Databricks/DATABRICKS_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Processing/Databricks/",
        "./Core-Data-Engineering/Data-Processing/Databricks/DATABRICKS_BEST_PRACTICES.md": "./Core-Data-Engineering/Data-Processing/Databricks/",
        "./Core-Data-Engineering/Data-Processing/Databricks/DATABRICKS_BIG4_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/Databricks/",
        "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Kafka/KAFKA_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Kafka/",
        "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Kafka/KAFKA_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Kafka/",
        "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Kafka/KAFKA_BEST_PRACTICES.md": "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Kafka/",
        "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Flink/FLINK_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Flink/",
        "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Flink/FLINK_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Processing/Streaming/Apache-Flink/",
        "./Core-Data-Engineering/Data-Processing/Streaming/Confluent-Kafka/CONFLUENT_KAFKA_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/Streaming/Confluent-Kafka/",
        "./Core-Data-Engineering/Data-Processing/ETL/Informatica/INFORMATICA_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/ETL/Informatica/",
        "./Core-Data-Engineering/Data-Processing/DATA_PROCESSING_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/",
        "./Core-Data-Engineering/Data-Processing/DATA_PROCESSING_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Processing/",
        
        # Orchestration fixes - we know AIRFLOW_INTERVIEW_QUESTIONS.md exists
        "./Core-Data-Engineering/Data-Processing/Orchestration/DBT/DBT_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Processing/Orchestration/DBT/",
        "./Core-Data-Engineering/Data-Processing/Orchestration/DBT/DBT_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Processing/Orchestration/DBT/",
        "./Core-Data-Engineering/Data-Processing/Orchestration/DBT/DBT_BEST_PRACTICES.md": "./Core-Data-Engineering/Data-Processing/Orchestration/DBT/",
        
        # Data Warehousing fixes
        "./Core-Data-Engineering/Data-Warehousing/Snowflake/SNOWFLAKE_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Warehousing/Snowflake/",
        "./Core-Data-Engineering/Data-Warehousing/Snowflake/SNOWFLAKE_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Warehousing/Snowflake/",
        "./Core-Data-Engineering/Data-Warehousing/Snowflake/SNOWFLAKE_BEST_PRACTICES.md": "./Core-Data-Engineering/Data-Warehousing/Snowflake/",
        "./Core-Data-Engineering/Data-Warehousing/Snowflake/SNOWFLAKE_BIG4_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Warehousing/Snowflake/",
        "./Core-Data-Engineering/Data-Warehousing/Redshift/REDSHIFT_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Warehousing/Redshift/",
        "./Core-Data-Engineering/Data-Warehousing/Redshift/REDSHIFT_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Warehousing/Redshift/",
        "./Core-Data-Engineering/Data-Warehousing/DATA_WAREHOUSING_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Warehousing/",
        
        # Data Architecture fixes
        "./Core-Data-Engineering/Data-Architecture/DATA_ARCHITECTURE_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Data-Architecture/",
        "./Core-Data-Engineering/Data-Architecture/DATA_ARCHITECTURE_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Architecture/",
        "./Core-Data-Engineering/Data-Architecture/Dimensional-Data-Modeling/DIMENSIONAL_DATA_MODELING_KEY_CONCEPTS.md": "./Core-Data-Engineering/Data-Architecture/Dimensional-Data-Modeling/",
        
        # Supporting Tools fixes
        "./Supporting-Tools/DevOps-Automation/Docker/DOCKER_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/DevOps-Automation/Docker/",
        "./Supporting-Tools/DevOps-Automation/Docker/DOCKER_KEY_CONCEPTS.md": "./Supporting-Tools/DevOps-Automation/Docker/",
        "./Supporting-Tools/DevOps-Automation/Docker/DOCKER_BEST_PRACTICES.md": "./Supporting-Tools/DevOps-Automation/Docker/",
        "./Supporting-Tools/DevOps-Automation/Kubernetes/KUBERNETES_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/DevOps-Automation/Kubernetes/",
        "./Supporting-Tools/DevOps-Automation/Kubernetes/KUBERNETES_KEY_CONCEPTS.md": "./Supporting-Tools/DevOps-Automation/Kubernetes/",
        "./Supporting-Tools/DevOps-Automation/Kubernetes/KUBERNETES_BEST_PRACTICES.md": "./Supporting-Tools/DevOps-Automation/Kubernetes/",
        "./Supporting-Tools/DevOps-Automation/Terraform/TERRAFORM_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/DevOps-Automation/Terraform/",
        "./Supporting-Tools/DevOps-Automation/Terraform/TERRAFORM_KEY_CONCEPTS.md": "./Supporting-Tools/DevOps-Automation/Terraform/",
        "./Supporting-Tools/DevOps-Automation/Terraform/TERRAFORM_BEST_PRACTICES.md": "./Supporting-Tools/DevOps-Automation/Terraform/",
        "./Supporting-Tools/DevOps-Automation/Jenkins/JENKINS_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/DevOps-Automation/Jenkins/",
        "./Supporting-Tools/DevOps-Automation/Ansible/ANSIBLE_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/DevOps-Automation/Ansible/",
        "./Supporting-Tools/DevOps-Automation/DEVOPS_AUTOMATION_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/DevOps-Automation/",
        
        # Version Control fixes
        "./Supporting-Tools/Version-Control/Git/GIT_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Version-Control/Git/",
        "./Supporting-Tools/Version-Control/Git/GIT_KEY_CONCEPTS.md": "./Supporting-Tools/Version-Control/Git/",
        "./Supporting-Tools/Version-Control/Git/GIT_BEST_PRACTICES.md": "./Supporting-Tools/Version-Control/Git/",
        "./Supporting-Tools/Version-Control/VERSION_CONTROL_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Version-Control/",
        
        # Visualization fixes
        "./Supporting-Tools/Visualization-Reporting/Tableau/TABLEAU_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Visualization-Reporting/Tableau/",
        "./Supporting-Tools/Visualization-Reporting/Tableau/TABLEAU_KEY_CONCEPTS.md": "./Supporting-Tools/Visualization-Reporting/Tableau/",
        "./Supporting-Tools/Visualization-Reporting/Tableau/TABLEAU_BEST_PRACTICES.md": "./Supporting-Tools/Visualization-Reporting/Tableau/",
        "./Supporting-Tools/Visualization-Reporting/Power-BI/POWERBI_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Visualization-Reporting/Power-BI/",
        "./Supporting-Tools/Visualization-Reporting/Power-BI/POWERBI_KEY_CONCEPTS.md": "./Supporting-Tools/Visualization-Reporting/Power-BI/",
        "./Supporting-Tools/Monitoring/Grafana/GRAFANA_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Monitoring/Grafana/",
        
        # AI/ML fixes
        "./Supporting-Tools/AI/Machine-Learning/ML_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/AI/Machine-Learning/",
        "./Supporting-Tools/AI/Machine-Learning/ML_KEY_CONCEPTS.md": "./Supporting-Tools/AI/Machine-Learning/",
        "./Supporting-Tools/AI/Machine-Learning/ML_BEST_PRACTICES.md": "./Supporting-Tools/AI/Machine-Learning/",
        "./Supporting-Tools/AI/AI_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/AI/",
        
        # Programming fixes
        "./Supporting-Tools/Programming/Data-Structures-Algorithms/DSA_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Programming/Data-Structures-Algorithms/",
        "./Supporting-Tools/Programming/Data-Structures-Algorithms/DSA_BIG4_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Programming/Data-Structures-Algorithms/",
        "./Supporting-Tools/Programming/Design-Patterns/DESIGN_PATTERNS_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Programming/Design-Patterns/",
        "./Supporting-Tools/Programming/Design-Patterns/DESIGN_PATTERNS_BIG4_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Programming/Design-Patterns/",
        "./Supporting-Tools/Systems/Linux/LINUX_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Systems/Linux/",
        
        # Project Management fixes
        "./Supporting-Tools/Project-Management/PROJECT_MANAGEMENT_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Project-Management/",
        "./Supporting-Tools/Project-Management/PROJECT_MANAGEMENT_BIG4_INTERVIEW_QUESTIONS.md": "./Supporting-Tools/Project-Management/",
        
        # Programming Languages fixes
        "./Core-Data-Engineering/Programming-Languages/PROGRAMMING_LANGUAGES_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Programming-Languages/",
        "./Core-Data-Engineering/Programming-Languages/Python/PYTHON_DATA_STRUCTURES_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Programming-Languages/Python/",
        "./Core-Data-Engineering/Programming-Languages/SQL/SQL_BIG4_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Programming-Languages/SQL/",
        "./Core-Data-Engineering/Programming-Languages/PySpark/PYSPARK_BIG4_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Programming-Languages/PySpark/",
        
        # AWS specific fixes
        "./Core-Data-Engineering/Cloud/AWS/S3_INTERVIEW_QUESTIONS.md": "./Core-Data-Engineering/Cloud/AWS/",
    }
    
    # Files to process
    files_to_fix = [
        Path("README.md"),
        Path("docs/COMPREHENSIVE_NAVIGATION_GUIDE.md"),
        Path("docs/INTERVIEW_QUESTIONS_MASTER_INDEX.md"),
        Path("docs/START_HERE.md"),
        Path("quick-prep/README.md"),
    ]
    
    total_fixes = 0
    
    for file_path in files_to_fix:
        if file_path.exists():
            print(f"\nProcessing: {file_path}")
            fixes = fix_links_in_file(file_path, link_replacements)
            total_fixes += fixes
        else:
            print(f"File not found: {file_path}")
    
    print(f"\n" + "=" * 80)
    print(f"SUMMARY: Fixed {total_fixes} broken links across {len(files_to_fix)} files")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Run the link checker again to verify fixes")
    print("2. Consider creating missing interview question files")
    print("3. Update any remaining broken links manually")

if __name__ == "__main__":
    main()