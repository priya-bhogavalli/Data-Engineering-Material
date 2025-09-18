# DuckDB - Key Concepts

## Overview
DuckDB is an in-process SQL OLAP database management system designed for analytical workloads with a focus on simplicity and performance.

## Core Features
- **In-process database**: Embedded database, no server required
- **Columnar storage**: Optimized for analytical queries
- **Vectorized execution**: SIMD-optimized query processing
- **ACID transactions**: Full ACID compliance
- **SQL compatibility**: Extensive SQL standard support
- **Zero dependencies**: Single binary with no external dependencies

## Architecture
- **Embedded design**: Runs within application process
- **Columnar engine**: Column-oriented storage and processing
- **Vectorized execution**: Process data in batches using SIMD
- **Parallel processing**: Multi-threaded query execution
- **Memory management**: Efficient memory usage and spilling
- **Optimizer**: Cost-based query optimizer

## Data Types
- **Numeric**: TINYINT, SMALLINT, INTEGER, BIGINT, DECIMAL, REAL, DOUBLE
- **Text**: VARCHAR, CHAR, TEXT
- **Binary**: BLOB, BYTEA
- **Date/Time**: DATE, TIME, TIMESTAMP, INTERVAL
- **Boolean**: BOOLEAN
- **Complex**: ARRAY, STRUCT, MAP, JSON
- **Spatial**: Geometry types with PostGIS compatibility

## File Format Support
- **Parquet**: Native Parquet support with predicate pushdown
- **CSV**: Efficient CSV reading with automatic type detection
- **JSON**: JSON and NDJSON file support
- **Excel**: Direct Excel file reading
- **Arrow**: Apache Arrow integration
- **SQLite**: Read SQLite databases directly

## Integration Ecosystem
- **Python**: Native Python integration with pandas
- **R**: R package for data analysis
- **Java**: JDBC driver for Java applications
- **Node.js**: JavaScript/TypeScript integration
- **CLI**: Command-line interface for interactive queries
- **Jupyter**: Jupyter notebook integration