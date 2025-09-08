# Data Types - Interview Questions

## 1. What is structured, semi-structured, and unstructured data?

**Answer:**
Data classification based on organization and format defines how we store and process information.

**Structured Data:**
- **Definition**: Highly organized data with predefined schema
- **Format**: Rows and columns, fixed fields
- **Examples**: Relational databases, CSV files, spreadsheets
- **Storage**: RDBMS (PostgreSQL, MySQL)
- **Processing**: SQL queries, traditional ETL

```sql
-- Structured data example
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_date DATE
);
```

**Semi-Structured Data:**
- **Definition**: Partially organized with some structure but flexible schema
- **Format**: Key-value pairs, nested objects, tags
- **Examples**: JSON, XML, YAML, NoSQL documents
- **Storage**: Document databases (MongoDB), data lakes
- **Processing**: Schema-on-read, flexible parsing

```json
{
  "customer_id": 123,
  "name": "John Doe",
  "addresses": [
    {"type": "home", "city": "New York"},
    {"type": "work", "city": "Boston"}
  ],
  "preferences": {
    "newsletter": true,
    "notifications": false
  }
}
```

**Unstructured Data:**
- **Definition**: No predefined structure or organization
- **Format**: Free-form text, binary files, multimedia
- **Examples**: Emails, documents, images, videos, social media posts
- **Storage**: Object storage (S3), data lakes, file systems
- **Processing**: NLP, computer vision, machine learning

**Comparison:**
```
Aspect          | Structured | Semi-Structured | Unstructured
----------------|------------|-----------------|-------------
Schema          | Fixed      | Flexible        | None
Query Language  | SQL        | NoSQL/JSON      | Search/ML
Storage Cost    | High       | Medium          | Low
Processing      | Fast       | Medium          | Complex
Scalability     | Vertical   | Horizontal      | Horizontal
```

## 2. How do you process each type of data in data engineering?

**Answer:**
Different data types require different processing approaches:

**Structured Data Processing:**
- Traditional ETL pipelines
- SQL-based transformations
- ACID transactions
- Batch processing

**Semi-Structured Data Processing:**
- Schema-on-read approaches
- JSON/XML parsing
- Document databases
- Flexible ETL/ELT

**Unstructured Data Processing:**
- Machine learning pipelines
- Text analytics and NLP
- Computer vision for images
- Search and indexing engines