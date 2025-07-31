# AWS RDS Key Concepts

## 1. Managed Relational Database Service
**What it is**: Fully managed relational database service that handles routine database tasks.

**Supported Engines**:
- **MySQL**: Open-source relational database
- **PostgreSQL**: Advanced open-source database
- **MariaDB**: MySQL-compatible database
- **Oracle**: Enterprise database system
- **SQL Server**: Microsoft's database platform
- **Amazon Aurora**: AWS-native high-performance database

## 2. DB Instances and Classes
**Instance Classes**:
```bash
# General Purpose (burstable performance)
db.t3.micro, db.t3.small, db.t3.medium, db.t3.large

# General Purpose (fixed performance)
db.m5.large, db.m5.xlarge, db.m5.2xlarge

# Memory Optimized
db.r5.large, db.r5.xlarge, db.r5.2xlarge

# Compute Optimized
db.c5.large, db.c5.xlarge, db.c5.2xlarge
```

**Creating DB Instance**:
```bash
# Create MySQL instance
aws rds create-db-instance \
    --db-instance-identifier mydb-instance \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --engine-version 8.0.35 \
    --master-username admin \
    --master-user-password MySecurePassword123! \
    --allocated-storage 20 \
    --storage-type gp2 \
    --vpc-security-group-ids sg-12345678 \
    --db-subnet-group-name my-db-subnet-group \
    --backup-retention-period 7 \
    --multi-az \
    --storage-encrypted
```

## 3. Storage Types and Performance
**Storage Options**:
```bash
# General Purpose SSD (gp2)
- 3 IOPS per GB, burstable to 3,000 IOPS
- Cost-effective for most workloads

# General Purpose SSD (gp3)
- Baseline 3,000 IOPS, scalable to 16,000 IOPS
- Independent IOPS and throughput scaling

# Provisioned IOPS SSD (io1)
- Up to 64,000 IOPS
- Consistent performance for I/O-intensive workloads

# Magnetic (standard)
- Legacy option, not recommended for new deployments
```

**Storage Scaling**:
```bash
# Modify storage
aws rds modify-db-instance \
    --db-instance-identifier mydb-instance \
    --allocated-storage 100 \
    --storage-type gp3 \
    --iops 4000 \
    --apply-immediately
```

## 4. High Availability and Multi-AZ
**Multi-AZ Deployment**:
```bash
# Enable Multi-AZ
aws rds modify-db-instance \
    --db-instance-identifier mydb-instance \
    --multi-az \
    --apply-immediately

# Multi-AZ benefits:
- Automatic failover to standby
- Enhanced durability and availability
- Maintenance performed on standby first
- Backups taken from standby
```

**Read Replicas**:
```bash
# Create read replica
aws rds create-db-instance-read-replica \
    --db-instance-identifier mydb-replica \
    --source-db-instance-identifier mydb-instance \
    --db-instance-class db.t3.small

# Cross-region read replica
aws rds create-db-instance-read-replica \
    --db-instance-identifier mydb-replica-west \
    --source-db-instance-identifier mydb-instance \
    --db-instance-class db.t3.small \
    --source-region us-east-1
```

## 5. Backup and Recovery
**Automated Backups**:
```bash
# Configure backup retention
aws rds modify-db-instance \
    --db-instance-identifier mydb-instance \
    --backup-retention-period 14 \
    --preferred-backup-window "03:00-04:00" \
    --preferred-maintenance-window "sun:04:00-sun:05:00"

# Point-in-time recovery
aws rds restore-db-instance-to-point-in-time \
    --source-db-instance-identifier mydb-instance \
    --target-db-instance-identifier mydb-restored \
    --restore-time 2024-01-15T10:30:00.000Z
```

**Manual Snapshots**:
```bash
# Create snapshot
aws rds create-db-snapshot \
    --db-instance-identifier mydb-instance \
    --db-snapshot-identifier mydb-snapshot-20240115

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier mydb-restored \
    --db-snapshot-identifier mydb-snapshot-20240115 \
    --db-instance-class db.t3.small
```

## 6. Security Features
**Encryption**:
```bash
# Create encrypted instance
aws rds create-db-instance \
    --db-instance-identifier encrypted-db \
    --storage-encrypted \
    --kms-key-id arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012 \
    --engine mysql \
    --db-instance-class db.t3.micro \
    --master-username admin \
    --master-user-password MySecurePassword123!
```

**Network Security**:
```bash
# Security group rules
aws ec2 authorize-security-group-ingress \
    --group-id sg-12345678 \
    --protocol tcp \
    --port 3306 \
    --source-group sg-87654321

# DB subnet group
aws rds create-db-subnet-group \
    --db-subnet-group-name private-db-subnet \
    --db-subnet-group-description "Private subnets for RDS" \
    --subnet-ids subnet-12345678 subnet-87654321
```

**IAM Database Authentication**:
```bash
# Enable IAM authentication
aws rds modify-db-instance \
    --db-instance-identifier mydb-instance \
    --enable-iam-database-authentication

# Generate auth token
aws rds generate-db-auth-token \
    --hostname mydb-instance.cluster-xyz.us-east-1.rds.amazonaws.com \
    --port 3306 \
    --username iamuser
```

## 7. Monitoring and Performance
**CloudWatch Metrics**:
```bash
# Key metrics to monitor:
CPUUtilization
DatabaseConnections
FreeableMemory
ReadLatency / WriteLatency
ReadIOPS / WriteIOPS
FreeStorageSpace
```

**Performance Insights**:
```bash
# Enable Performance Insights
aws rds modify-db-instance \
    --db-instance-identifier mydb-instance \
    --enable-performance-insights \
    --performance-insights-retention-period 7

# Query Performance Insights
aws pi get-resource-metrics \
    --service-type RDS \
    --identifier mydb-instance \
    --start-time 2024-01-15T00:00:00Z \
    --end-time 2024-01-15T23:59:59Z \
    --period-in-seconds 300 \
    --metric-queries MetricType=db.SQL.Innodb_rows_read.avg
```

## 8. Parameter Groups
**Custom Parameter Groups**:
```bash
# Create parameter group
aws rds create-db-parameter-group \
    --db-parameter-group-name custom-mysql-params \
    --db-parameter-group-family mysql8.0 \
    --description "Custom MySQL parameters"

# Modify parameters
aws rds modify-db-parameter-group \
    --db-parameter-group-name custom-mysql-params \
    --parameters ParameterName=max_connections,ParameterValue=200,ApplyMethod=immediate \
                 ParameterName=innodb_buffer_pool_size,ParameterValue='{DBInstanceClassMemory*3/4}',ApplyMethod=pending-reboot

# Apply parameter group
aws rds modify-db-instance \
    --db-instance-identifier mydb-instance \
    --db-parameter-group-name custom-mysql-params
```

## 9. Aurora Specific Features
**Aurora Clusters**:
```bash
# Create Aurora cluster
aws rds create-db-cluster \
    --db-cluster-identifier aurora-cluster \
    --engine aurora-mysql \
    --engine-version 8.0.mysql_aurora.3.02.0 \
    --master-username admin \
    --master-user-password MySecurePassword123! \
    --database-name myapp \
    --storage-encrypted

# Add cluster instances
aws rds create-db-instance \
    --db-instance-identifier aurora-writer \
    --db-cluster-identifier aurora-cluster \
    --db-instance-class db.r5.large \
    --engine aurora-mysql
```

**Aurora Serverless**:
```bash
# Create serverless cluster
aws rds create-db-cluster \
    --db-cluster-identifier aurora-serverless \
    --engine aurora-mysql \
    --engine-mode serverless \
    --scaling-configuration MinCapacity=2,MaxCapacity=16,AutoPause=true,SecondsUntilAutoPause=300 \
    --master-username admin \
    --master-user-password MySecurePassword123!
```

## 10. Cost Optimization
**Reserved Instances**:
```bash
# Purchase reserved instance
aws rds purchase-reserved-db-instances-offering \
    --reserved-db-instances-offering-id 12345678-1234-1234-1234-123456789012 \
    --reserved-db-instance-id my-reserved-instance

# List available offerings
aws rds describe-reserved-db-instances-offerings \
    --db-instance-class db.t3.micro \
    --duration 31536000 \
    --offering-type "All Upfront"
```

**Storage Optimization**:
```bash
# Enable storage autoscaling
aws rds modify-db-instance \
    --db-instance-identifier mydb-instance \
    --max-allocated-storage 1000 \
    --apply-immediately

# Monitor storage usage
aws cloudwatch get-metric-statistics \
    --namespace AWS/RDS \
    --metric-name FreeStorageSpace \
    --dimensions Name=DBInstanceIdentifier,Value=mydb-instance \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-15T23:59:59Z \
    --period 3600 \
    --statistics Average
```