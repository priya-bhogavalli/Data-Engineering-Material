# Amazon S3 - Key Concepts

## Overview
Amazon Simple Storage Service (S3) is a scalable object storage service designed for data backup, archival, analytics, and content distribution.

## Core Features
- **Object storage**: Store and retrieve any amount of data
- **Scalability**: Virtually unlimited storage capacity
- **Durability**: 99.999999999% (11 9's) durability
- **Availability**: 99.99% availability SLA
- **Global accessibility**: Access from anywhere on the internet
- **Cost-effective**: Pay only for what you use

## Storage Classes
- **Standard**: General-purpose storage for frequently accessed data
- **Intelligent-Tiering**: Automatic cost optimization between access tiers
- **Standard-IA**: Infrequent access with lower storage cost
- **One Zone-IA**: Lower-cost option for infrequently accessed data
- **Glacier**: Long-term archival with retrieval times from minutes to hours
- **Glacier Deep Archive**: Lowest-cost storage for long-term retention

## Key Concepts
- **Buckets**: Containers for objects with globally unique names
- **Objects**: Files stored in buckets with unique keys
- **Keys**: Unique identifiers for objects within buckets
- **Regions**: Geographic locations where buckets are stored
- **Versioning**: Keep multiple versions of objects
- **Metadata**: Key-value pairs associated with objects

## Security Features
- **IAM integration**: Identity and Access Management policies
- **Bucket policies**: Resource-based access control
- **Access Control Lists**: Object-level permissions
- **Encryption**: Server-side and client-side encryption
- **VPC endpoints**: Private network access
- **Access logging**: Detailed access logs for auditing