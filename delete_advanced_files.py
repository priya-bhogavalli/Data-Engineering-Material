#!/usr/bin/env python3
"""
Script to delete the advanced documentation files that were created.
"""

import os
from pathlib import Path

# Tools that had advanced files created
TOOLS_WITH_ADVANCED_FILES = [
    # Cloud Services
    ("Core-Data-Engineering/Cloud", "Cloud"),
    ("Core-Data-Engineering/Cloud/AWS", "AWS"),
    ("Core-Data-Engineering/Cloud/AWS/Amazon-SageMaker", "Amazon SageMaker"),
    ("Core-Data-Engineering/Cloud/AWS/AWS-Glue", "AWS Glue"),
    ("Core-Data-Engineering/Cloud/AWS/EMR", "Amazon EMR"),
    ("Core-Data-Engineering/Cloud/Azure", "Azure"),
    ("Core-Data-Engineering/Cloud/Azure/Azure-Event-Hubs", "Azure Event Hubs"),
    ("Core-Data-Engineering/Cloud/Azure/Azure-Stream-Analytics", "Azure Stream Analytics"),
    ("Core-Data-Engineering/Cloud/GCP", "Google Cloud Platform"),
    ("Core-Data-Engineering/Cloud/GCP/BigQuery", "BigQuery"),
    ("Core-Data-Engineering/Cloud/GCP/Google-Cloud-Dataflow", "Google Cloud Dataflow"),
    ("Core-Data-Engineering/Cloud/GCP/Vertex-AI", "Vertex AI"),
    
    # Data Architecture
    ("Core-Data-Engineering/Data-Architecture", "Data Architecture"),
    ("Core-Data-Engineering/Data-Architecture/Apache-Iceberg", "Apache Iceberg"),
    ("Core-Data-Engineering/Data-Architecture/Applying-Analytical-Patterns", "Analytical Patterns"),
    ("Core-Data-Engineering/Data-Architecture/Data-Mesh", "Data Mesh"),
    ("Core-Data-Engineering/Data-Architecture/Data-Modeling", "Data Modeling"),
    ("Core-Data-Engineering/Data-Architecture/Data-Vault-2.0", "Data Vault 2.0"),
    ("Core-Data-Engineering/Data-Architecture/DataOps", "DataOps"),
    ("Core-Data-Engineering/Data-Architecture/Delta-Lake", "Delta Lake"),
    ("Core-Data-Engineering/Data-Architecture/Dimensional-Data-Modeling", "Dimensional Data Modeling"),
    ("Core-Data-Engineering/Data-Architecture/Fact-Data-Modeling", "Fact Data Modeling"),
    ("Core-Data-Engineering/Data-Architecture/KPIs-and-Experimentation", "KPIs and Experimentation"),
    ("Core-Data-Engineering/Data-Architecture/Master-Data-Management", "Master Data Management"),
    
    # Data Governance
    ("Core-Data-Engineering/Data-Governance/Amundsen", "Amundsen"),
    ("Core-Data-Engineering/Data-Governance/Apache-Atlas", "Apache Atlas"),
    ("Core-Data-Engineering/Data-Governance/Collibra", "Collibra"),
    ("Core-Data-Engineering/Data-Governance/DataHub", "DataHub"),
    ("Core-Data-Engineering/Data-Governance/Secoda", "Secoda"),
    
    # Data Processing
    ("Core-Data-Engineering/Data-Processing", "Data Processing"),
    ("Core-Data-Engineering/Data-Processing/Apache-Beam", "Apache Beam"),
    ("Core-Data-Engineering/Data-Processing/Apache-Flume", "Apache Flume"),
    ("Core-Data-Engineering/Data-Processing/Apache-Hadoop", "Apache Hadoop"),
    ("Core-Data-Engineering/Data-Processing/Apache-Hive", "Apache Hive"),
    ("Core-Data-Engineering/Data-Processing/Apache-Hudi", "Apache Hudi"),
    ("Core-Data-Engineering/Data-Processing/Apache-Impala", "Apache Impala"),
    ("Core-Data-Engineering/Data-Processing/Apache-Pig", "Apache Pig"),
    ("Core-Data-Engineering/Data-Processing/Apache-Sqoop", "Apache Sqoop"),
    ("Core-Data-Engineering/Data-Processing/Apache-ZooKeeper", "Apache ZooKeeper"),
    ("Core-Data-Engineering/Data-Processing/Databricks", "Databricks"),
    
    # ETL Tools
    ("Core-Data-Engineering/Data-Processing/ETL/Informatica", "Informatica"),
    ("Core-Data-Engineering/Data-Processing/ETL/Snaplogic", "SnapLogic"),
    
    # Orchestration
    ("Core-Data-Engineering/Data-Processing/Orchestration/Apache-Airflow", "Apache Airflow"),
    ("Core-Data-Engineering/Data-Processing/Orchestration/DBT", "dbt"),
    
    # Streaming
    ("Core-Data-Engineering/Data-Processing/Streaming/Apache-Flink", "Apache Flink"),
    ("Core-Data-Engineering/Data-Processing/Streaming/Apache-Kafka", "Apache Kafka"),
    ("Core-Data-Engineering/Data-Processing/Streaming/Confluent-Kafka", "Confluent Kafka"),
    
    # Data Quality
    ("Core-Data-Engineering/Data-Quality/Great-Expectations", "Great Expectations"),
    
    # Data Warehousing
    ("Core-Data-Engineering/Data-Warehousing/Redshift", "Amazon Redshift"),
    ("Core-Data-Engineering/Data-Warehousing/Snowflake", "Snowflake"),
    
    # Databases
    ("Core-Data-Engineering/Databases/Athena", "Amazon Athena"),
    ("Core-Data-Engineering/Databases/Graph-Databases/Neo4j", "Neo4j"),
    ("Core-Data-Engineering/Databases/Graph-Databases/Amazon-Neptune", "Amazon Neptune"),
    ("Core-Data-Engineering/Databases/In-Memory/Redis", "Redis"),
    ("Core-Data-Engineering/Databases/In-Memory/Memcached", "Memcached"),
    ("Core-Data-Engineering/Databases/MS-SQL-Server", "Microsoft SQL Server"),
    ("Core-Data-Engineering/Databases/MySQL", "MySQL"),
    ("Core-Data-Engineering/Databases/NewSQL/CockroachDB", "CockroachDB"),
    ("Core-Data-Engineering/Databases/NewSQL/TiDB", "TiDB"),
    ("Core-Data-Engineering/Databases/NoSQL/Cassandra", "Apache Cassandra"),
    ("Core-Data-Engineering/Databases/NoSQL/CouchDB", "Apache CouchDB"),
    ("Core-Data-Engineering/Databases/NoSQL/DynamoDB", "Amazon DynamoDB"),
    ("Core-Data-Engineering/Databases/NoSQL/HBase", "Apache HBase"),
    ("Core-Data-Engineering/Databases/NoSQL/MongoDB", "MongoDB"),
    ("Core-Data-Engineering/Databases/Oracle", "Oracle Database"),
    ("Core-Data-Engineering/Databases/PostgreSQL", "PostgreSQL"),
    ("Core-Data-Engineering/Databases/Search-Engines/Elasticsearch", "Elasticsearch"),
    ("Core-Data-Engineering/Databases/Search-Engines/Solr", "Apache Solr"),
    ("Core-Data-Engineering/Databases/Time-Series/InfluxDB", "InfluxDB"),
    ("Core-Data-Engineering/Databases/Time-Series/TimescaleDB", "TimescaleDB"),
    
    # Programming Languages
    ("Core-Data-Engineering/Programming-Languages/PySpark", "PySpark"),
    ("Core-Data-Engineering/Programming-Languages/Python", "Python"),
    ("Core-Data-Engineering/Programming-Languages/SQL", "SQL"),
]

def main():
    """Main function to delete advanced files."""
    base_path = Path("c:/Users/z00542ky/Data-Engineering-Material")
    
    deleted_files = []
    
    for tool_path, tool_name in TOOLS_WITH_ADVANCED_FILES:
        full_path = base_path / tool_path
        
        if not full_path.exists():
            continue
            
        # Create file name prefix
        file_prefix = tool_name.upper().replace(' ', '_').replace('-', '_')
        
        # Define files to delete
        files_to_delete = [
            f"{file_prefix}_ALL_FEATURES_REFERENCE.md",
            f"{file_prefix}_BEST_PRACTICES.md",
            f"{file_prefix}_QUICK_REFERENCE.md",
            f"{file_prefix}_RESOURCES.md",
        ]
        
        for filename in files_to_delete:
            file_path = full_path / filename
            
            if file_path.exists():
                try:
                    file_path.unlink()
                    deleted_files.append(str(file_path))
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
    
    print(f"\nSummary: Deleted {len(deleted_files)} advanced documentation files")

if __name__ == "__main__":
    main()