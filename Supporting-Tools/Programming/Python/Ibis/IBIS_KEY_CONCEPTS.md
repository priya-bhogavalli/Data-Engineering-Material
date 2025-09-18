# Ibis - Key Concepts

## Overview
Ibis is a Python library that provides a pandas-like interface for querying large datasets across different backends without loading data into memory.

## Core Features
- **Backend agnostic**: Single API for multiple database backends
- **Lazy evaluation**: Build query expressions without immediate execution
- **Pandas-like API**: Familiar interface for pandas users
- **SQL generation**: Automatic SQL query generation
- **Type system**: Strong typing for data operations
- **Composable queries**: Build complex queries from simple operations

## Supported Backends
- **SQL databases**: PostgreSQL, MySQL, SQLite, SQL Server
- **Big data**: Apache Spark, Apache Impala, Presto, Trino
- **Cloud warehouses**: BigQuery, Snowflake, Redshift
- **Analytics**: ClickHouse, Apache Drill
- **In-memory**: Pandas, DuckDB
- **File formats**: Parquet, CSV via DuckDB

## Key Capabilities
- **Cross-backend queries**: Write once, run on multiple backends
- **Query optimization**: Automatic query optimization
- **Type inference**: Automatic schema and type inference
- **Window functions**: Advanced analytical window functions
- **Aggregations**: Complex groupby and aggregation operations
- **Joins**: Various join operations across tables

## Expression System
- **Lazy expressions**: Build expression trees before execution
- **Type checking**: Compile-time type validation
- **Composability**: Combine expressions into complex queries
- **Reusability**: Reuse expressions across different contexts
- **Optimization**: Expression-level optimizations
- **Debugging**: Clear error messages and query inspection