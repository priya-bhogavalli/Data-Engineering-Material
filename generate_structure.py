#!/usr/bin/env python3
"""
Script to generate the complete folder structure and placeholder files
for the Data Engineering Interview Preparation repository.
"""

import os
from pathlib import Path

# Define the complete structure
STRUCTURE = {
    "01-Project-Management": {
        "Agile-DevOps": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Jira-Confluence": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Scrum-Kanban": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "02-Programming-Scripting": {
        "SQL": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "CSharp": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "PySpark": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "JavaScript": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "C-CPP": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "MATLAB": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "03-Databases-ORMs": {
        "PostgreSQL": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Oracle": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "MS-SQL-Server": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "MySQL": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Athena": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "04-Cloud-Platforms": {
        "AWS": {
            "EC2": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
            "Glue": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
            "Athena": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
            "Redshift": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
            "RDS": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
            "IAM": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
        },
        "Azure": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "GCP": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "05-Version-Control": {
        "Git": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Bitbucket": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "GitLab": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "06-GenAI-LLMs": {
        "GenAI-Concepts": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "RAGs-Embeddings": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "LangChain": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "OpenAI-APIs": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Vector-Databases": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "07-Workflow-Orchestration": {
        "Apache-Airflow": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "DBT": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "08-Data-Engineering-BigData": {
        "Databricks": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Apache-Spark": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "09-Data-Warehousing": {
        "Snowflake": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Redshift": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "10-DevOps-Automation": {
        "Ansible": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Terraform": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Docker": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Kubernetes": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Jenkins": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "CircleCI": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "CI-CD": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "11-ETL-Integration": {
        "Snaplogic": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Informatica": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "12-Streaming-RealTime": {
        "Confluent-Kafka": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Apache-Kafka": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Apache-Flink": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "13-Data-Architecture": {
        "Data-Vault": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Data-Mesh": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "DataOps": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "14-ITSM-Workflow": {
        "ServiceNow": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "15-Visualization-Reporting": {
        "Tableau": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Power-BI": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Kibana": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Elastic-Search": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "16-AI-ML-MLOps": {
        "Machine-Learning": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "MLOps": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "17-Web-Development": {
        "JavaScript-Frameworks": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Node-GraphQL": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    },
    "18-Cloud-Monitoring": {
        "Datadog": ["concepts.md", "interview-questions.md", "resources.md", "examples/"],
        "Grafana": ["concepts.md", "interview-questions.md", "resources.md", "examples/"]
    }
}

def create_placeholder_content(file_type, topic_name):
    """Generate placeholder content for different file types."""
    
    if file_type == "concepts.md":
        return f"""# {topic_name} - Core Concepts

## Overview
[Add overview of {topic_name} and its role in data engineering]

## Key Concepts
[List and explain the fundamental concepts]

## Architecture
[Describe the architecture and components]

## Use Cases in Data Engineering
[Explain how this technology is used in data engineering contexts]

## Best Practices
[List best practices and recommendations]

## Common Patterns
[Describe common implementation patterns]

## Integration with Other Tools
[Explain how this integrates with other data engineering tools]
"""
    
    elif file_type == "interview-questions.md":
        return f"""# {topic_name} Interview Questions

## Basic Questions

### Q1: What is {topic_name}?
**Answer:** [Provide comprehensive answer]

### Q2: What are the key features of {topic_name}?
**Answer:** [List and explain key features]

## Intermediate Questions

### Q3: How does {topic_name} handle [specific scenario]?
**Answer:** [Provide detailed explanation with examples]

### Q4: What are the advantages and disadvantages of {topic_name}?
**Answer:** [Compare pros and cons]

## Advanced Questions

### Q5: How would you optimize {topic_name} for large-scale data processing?
**Answer:** [Provide optimization strategies]

### Q6: Describe a complex scenario where you used {topic_name}.
**Answer:** [Provide real-world example]

## Scenario-Based Questions

### Q7: Design a solution using {topic_name} for [specific use case].
**Answer:** [Provide architectural solution]

## Troubleshooting Questions

### Q8: How would you debug performance issues in {topic_name}?
**Answer:** [Provide debugging strategies]
"""
    
    elif file_type == "resources.md":
        return f"""# {topic_name} Resources

## Official Documentation
- [Official {topic_name} Documentation](https://example.com)
- [API Reference](https://example.com)
- [Getting Started Guide](https://example.com)

## Learning Resources

### Books
- [Add relevant books]

### Online Courses
- [Add relevant courses]

### Tutorials
- [Add tutorial links]

## Community Resources
- [Official Forum/Community](https://example.com)
- [Stack Overflow Tag](https://stackoverflow.com/questions/tagged/{topic_name.lower()})
- [Reddit Community](https://reddit.com/r/{topic_name})

## Tools and Extensions
- [List related tools]

## Best Practices Guides
- [Add links to best practices]

## Sample Projects
- [Add GitHub repositories with examples]

## Certification Programs
- [List relevant certifications]

## Conferences and Events
- [List relevant conferences]

## Blogs and Articles
- [Add relevant blog links]
"""
    
    return ""

def create_structure(base_path):
    """Create the complete folder structure with placeholder files."""
    
    base_path = Path(base_path)
    
    for category, subcategories in STRUCTURE.items():
        category_path = base_path / category
        category_path.mkdir(exist_ok=True)
        
        if isinstance(subcategories, dict):
            for subcategory, files in subcategories.items():
                subcategory_path = category_path / subcategory
                subcategory_path.mkdir(exist_ok=True)
                
                if isinstance(files, dict):
                    # Handle nested structure (like AWS services)
                    for subsubcategory, subfiles in files.items():
                        subsubcategory_path = subcategory_path / subsubcategory
                        subsubcategory_path.mkdir(exist_ok=True)
                        
                        for file_item in subfiles:
                            if file_item.endswith('/'):
                                # Create directory
                                (subsubcategory_path / file_item.rstrip('/')).mkdir(exist_ok=True)
                            else:
                                # Create file with placeholder content
                                file_path = subsubcategory_path / file_item
                                if not file_path.exists():
                                    content = create_placeholder_content(file_item, subsubcategory)
                                    file_path.write_text(content, encoding='utf-8')
                else:
                    # Handle regular structure
                    for file_item in files:
                        if file_item.endswith('/'):
                            # Create directory
                            (subcategory_path / file_item.rstrip('/')).mkdir(exist_ok=True)
                        else:
                            # Create file with placeholder content
                            file_path = subcategory_path / file_item
                            if not file_path.exists():
                                content = create_placeholder_content(file_item, subcategory)
                                file_path.write_text(content, encoding='utf-8')

if __name__ == "__main__":
    # Get the current directory (should be the repo root)
    current_dir = Path.cwd()
    
    print("Creating Data Engineering Interview Preparation structure...")
    create_structure(current_dir)
    print("Structure created successfully!")
    
    # Create a .gitkeep file in empty directories
    for root, dirs, files in os.walk(current_dir):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            if dir_name == "examples" and not any(dir_path.iterdir()):
                (dir_path / ".gitkeep").touch()
    
    print("Added .gitkeep files to empty directories.")
    print("Repository structure is ready!")