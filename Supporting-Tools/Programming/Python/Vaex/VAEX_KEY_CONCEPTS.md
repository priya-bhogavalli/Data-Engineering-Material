# Vaex - Key Concepts

## Overview
Vaex is a Python library for lazy, out-of-core dataframe operations on large datasets, designed for interactive exploration and visualization of billion-row datasets.

## Core Features
- **Out-of-core processing**: Handle datasets larger than RAM
- **Lazy evaluation**: Computations executed only when needed
- **Interactive visualization**: Real-time plotting of large datasets
- **Memory mapping**: Efficient memory-mapped file access
- **Fast aggregations**: Optimized statistical computations
- **Streaming**: Process data streams efficiently

## Key Capabilities
- **Billion-row datasets**: Handle datasets with billions of rows
- **Real-time visualization**: Interactive plots and histograms
- **Statistical operations**: Fast mean, std, percentiles, correlations
- **Filtering**: Efficient boolean indexing and filtering
- **Groupby operations**: Fast groupby aggregations
- **Machine learning**: Integration with scikit-learn and other ML libraries

## Data Formats
- **HDF5**: Native support for HDF5 format
- **Apache Arrow**: Arrow format support
- **Parquet**: Read Parquet files efficiently
- **CSV**: Read large CSV files
- **FITS**: Astronomical data format support
- **Custom formats**: Extensible format support

## Performance Optimizations
- **Memory mapping**: Zero-copy data access
- **Columnar storage**: Efficient column-oriented operations
- **Vectorized operations**: SIMD optimized computations
- **Caching**: Intelligent caching of computed results
- **Parallel processing**: Multi-threaded operations
- **GPU acceleration**: Optional GPU acceleration support