# Apache Hive - Key Concepts

## Overview
Apache Hive is a data warehouse software that facilitates reading, writing, and managing large datasets in distributed storage using SQL-like queries.

## Core Architecture
- **Metastore**: Stores metadata about tables and partitions
- **Query engine**: Translates HiveQL to MapReduce/Tez/Spark jobs
- **Storage**: Uses HDFS or other compatible file systems
- **SerDe**: Serializer/Deserializer for different data formats
- **Driver**: Manages query lifecycle and execution
- **Compiler**: Compiles HiveQL to execution plans

## Key Features
- **SQL-like interface**: HiveQL for familiar SQL operations
- **Schema on read**: Apply schema when reading data
- **Partitioning**: Organize data for efficient querying
- **Bucketing**: Distribute data across files for joins
- **ACID transactions**: Support for INSERT, UPDATE, DELETE
- **Vectorization**: Optimized execution for analytical queries

## Data Types
- **Primitive**: TINYINT, SMALLINT, INT, BIGINT, FLOAT, DOUBLE, BOOLEAN, STRING
- **Complex**: ARRAY, MAP, STRUCT for nested data
- **Date/Time**: DATE, TIMESTAMP for temporal data
- **Decimal**: DECIMAL for precise numeric calculations
- **Binary**: BINARY for binary data storage
- **Union**: UNIONTYPE for variant data types

## Storage Formats
- **TextFile**: Plain text format, human-readable
- **SequenceFile**: Binary format for key-value pairs
- **RCFile**: Record Columnar File for analytical queries
- **ORC**: Optimized Row Columnar format with compression
- **Parquet**: Columnar format with efficient compression
- **Avro**: Schema evolution support with JSON metadata

## Execution Engines
- **MapReduce**: Traditional Hadoop execution engine
- **Tez**: Directed Acyclic Graph execution framework
- **Spark**: In-memory processing for faster queries
- **LLAP**: Live Long and Process for interactive queries
- **Vectorization**: SIMD operations for performance
- **Cost-based optimization**: Intelligent query planning