# Data Profiling - Interview Questions

## 1. What is data profiling?

**Answer:**
Data profiling is the process of examining and analyzing data to understand its structure, content, quality, and relationships.

**Key Components:**

**Structure Analysis:**
- Column data types and formats
- Null value patterns
- Data length and precision
- Schema validation

**Content Analysis:**
- Value distributions and frequencies
- Min/max/average values
- Unique value counts
- Pattern recognition

**Quality Assessment:**
- Completeness (missing values)
- Validity (format compliance)
- Consistency (cross-field validation)
- Accuracy (business rule compliance)

**Relationship Discovery:**
- Foreign key relationships
- Functional dependencies
- Data correlations
- Referential integrity

**Example Implementation:**
```python
import pandas as pd
import numpy as np

def profile_dataset(df):
    profile = {}
    
    for column in df.columns:
        profile[column] = {
            'data_type': str(df[column].dtype),
            'null_count': df[column].isnull().sum(),
            'null_percentage': (df[column].isnull().sum() / len(df)) * 100,
            'unique_count': df[column].nunique(),
            'unique_percentage': (df[column].nunique() / len(df)) * 100
        }
        
        if df[column].dtype in ['int64', 'float64']:
            profile[column].update({
                'min': df[column].min(),
                'max': df[column].max(),
                'mean': df[column].mean(),
                'std': df[column].std()
            })
    
    return profile
```

## 2. What tools are used for data profiling?

**Answer:**
Various tools support automated data profiling:

**Open Source:**
- **Pandas Profiling**: Python library for automated reports
- **Great Expectations**: Data validation and profiling
- **Apache Griffin**: Data quality platform

**Commercial:**
- **Informatica Data Quality**: Enterprise data profiling
- **Talend Data Quality**: Integrated profiling tools
- **IBM InfoSphere**: Comprehensive data analysis

**Cloud Native:**
- **AWS Glue DataBrew**: Visual data preparation with profiling
- **Google Cloud Dataprep**: Data profiling and preparation
- **Azure Data Factory**: Data profiling capabilities

**Benefits:**
- Automated quality assessment
- Data discovery and understanding
- Issue identification before processing
- Compliance and governance support