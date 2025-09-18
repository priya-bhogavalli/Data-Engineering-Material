# Snowplow - Key Concepts

## Overview
Snowplow is an open-source behavioral data platform that enables organizations to collect, process, and model event data from websites, mobile apps, and server-side applications.

## Core Architecture
- **Event collection**: Comprehensive event tracking
- **Real-time processing**: Stream processing pipeline
- **Data modeling**: Transform raw events into business logic
- **Data warehouse**: Load processed data into warehouses
- **Open source**: Fully open-source platform
- **Cloud deployment**: Available as managed service

## Pipeline Components
- **Trackers**: Collect events from various sources
- **Collectors**: Receive and validate events
- **Enrichment**: Add context and validate events
- **Storage**: Load events into data warehouse
- **Modeling**: Transform events into business entities
- **Analytics**: Query and analyze processed data

## Event Tracking
- **Structured events**: Predefined event schemas
- **Self-describing events**: Custom event schemas
- **Page views**: Web page tracking
- **Screen views**: Mobile app screen tracking
- **E-commerce**: Transaction and product tracking
- **Custom contexts**: Additional event context

## Data Processing
- **Real-time stream**: Kinesis/Kafka stream processing
- **Batch processing**: Scheduled batch jobs
- **Event validation**: Schema validation and enrichment
- **Data quality**: Built-in data quality checks
- **Deduplication**: Remove duplicate events
- **Failed events**: Handle and recover bad events

## Key Features
- **Schema registry**: Manage event schemas
- **Data modeling**: dbt-based data modeling
- **Identity resolution**: Track users across sessions
- **Privacy controls**: GDPR compliance features
- **Multi-cloud**: Deploy on AWS, GCP, Azure
- **Warehouse-native**: Optimized for modern warehouses