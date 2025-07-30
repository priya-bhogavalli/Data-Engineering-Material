import os
from pathlib import Path

tools = [
    "Client-Stakeholder-Management", "Agile-Methodologies", "DevOps-Practices",
    "Jira", "Confluence", "Scrum", "Kanban", "Python", "SQL", "CSharp", "PySpark",
    "PostgreSQL", "Oracle", "MS-SQL-Server", "MySQL", "Athena", "AWS-EC2", "AWS-S3",
    "AWS-Glue", "AWS-Athena", "AWS-Redshift", "AWS-RDS", "AWS-IAM", "Git", "Bitbucket",
    "GitLab", "Azure", "GCP", "GenAI", "RAGs", "Embeddings", "LangChain",
    "Azure-OpenAI-API", "OpenAI-API", "Vector-DB", "Apache-Airflow", "DBT",
    "Databricks", "Apache-Spark", "Snowflake", "Redshift", "Ansible", "Terraform",
    "CI-CD", "Docker", "Jenkins", "Kubernetes", "CircleCI", "Snaplogic", "Informatica",
    "Confluent-Kafka", "Apache-Kafka", "Apache-Flink", "Data-Vault-2.0", "Data-Mesh",
    "DataOps", "ServiceNow", "Tableau", "Power-BI", "Kibana", "Elastic-Search",
    "Machine-Learning", "AI-ML", "MLOps", "JavaScript", "HTML", "CSS", "C", "CPP",
    "MATLAB", "jQuery", "Node-js", "GraphQL", "Datadog", "Grafana"
]

for tool in tools:
    tool_path = Path(tool)
    if tool_path.exists():
        # Create standard files
        (tool_path / "concepts.md").write_text(f"# {tool} - Core Concepts\n\n## Overview\n[Add overview]\n\n## Key Features\n[List features]\n\n## Use Cases\n[Describe use cases]\n")
        (tool_path / "interview-questions.md").write_text(f"# {tool} Interview Questions\n\n## Basic Questions\n\n## Intermediate Questions\n\n## Advanced Questions\n")
        (tool_path / "resources.md").write_text(f"# {tool} Resources\n\n## Official Documentation\n\n## Learning Resources\n\n## Community\n")
        
        # Create .gitkeep in examples folder
        examples_path = tool_path / "examples"
        if examples_path.exists():
            (examples_path / ".gitkeep").touch()

print("Created files for all tools!")