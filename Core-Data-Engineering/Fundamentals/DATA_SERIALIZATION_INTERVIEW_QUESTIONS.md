# Data Serialization - Interview Questions

## 1. What is data serialization and deserialization? What are different serialization formats?

**Answer:**
Serialization converts objects into a format for storage or transmission. Deserialization reverses this process.

**Common Serialization Formats:**

**JSON (JavaScript Object Notation):**
- Human-readable text format
- Language-independent
- Widely supported but verbose

**XML (eXtensible Markup Language):**
- Self-describing with metadata
- Verbose and slower parsing
- Good for complex hierarchical data

**Protocol Buffers (protobuf):**
- Binary format by Google
- Compact and fast
- Requires schema definition

**Apache Avro:**
- Schema evolution support
- Compact binary format
- Popular in big data ecosystems

**MessagePack:**
- Binary JSON-like format
- More compact than JSON
- Faster serialization/deserialization

**Parquet:**
- Columnar storage format
- Excellent compression
- Optimized for analytics

**Comparison:**
```python
# JSON
{"name": "John", "age": 30}

# XML
<person><name>John</name><age>30</age></person>

# Avro (schema + binary data)
# Schema: {"type": "record", "fields": [...]}
# Binary data: compressed format

# Parquet
# Columnar binary format with metadata
```

**Performance Comparison:**
```
Format      | Size | Speed | Schema Evolution
------------|------|-------|------------------
JSON        | Large| Medium| Manual
XML         | XLarge| Slow | Manual  
Protobuf    | Small| Fast  | Limited
Avro        | Small| Fast  | Excellent
Parquet     | XSmall| Fast | Good
```

## 2. When would you use each serialization format?

**Answer:**
Choose based on use case requirements:

**JSON**: REST APIs, configuration files, web applications
**XML**: Legacy systems, SOAP services, document markup
**Protobuf**: Microservices, gRPC, high-performance systems
**Avro**: Kafka messages, schema registry, data pipelines
**Parquet**: Data warehouses, analytics, columnar storage