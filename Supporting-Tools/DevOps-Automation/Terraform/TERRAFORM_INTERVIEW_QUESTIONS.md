# 🏗️ Terraform Interview Questions for Data Engineering (Enhanced)

## 📋 Table of Contents

1. [Infrastructure Basics (1-25)](#infrastructure-basics-1-25)
2. [Data Infrastructure (26-50)](#data-infrastructure-26-50)
3. [State Management (51-75)](#state-management-51-75)
4. [Production & Best Practices (76-100)](#production--best-practices-76-100)

---

## Infrastructure Basics (1-25)

### 1. What is Terraform and why is it important for data engineering?
**Answer**: Terraform is Infrastructure as Code (IaC) tool for provisioning and managing cloud resources.

**Benefits for Data Engineering:**
- **Reproducible Infrastructure**: Consistent environments across dev/test/prod
- **Version Control**: Track infrastructure changes
- **Automation**: Automated provisioning and scaling
- **Multi-Cloud**: Support for AWS, Azure, GCP

```hcl
# Basic data infrastructure
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 bucket for data lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${var.environment}"
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    Purpose     = "data-lake"
  }
}

# RDS instance for metadata
resource "aws_db_instance" "metadata_db" {
  identifier = "${var.project_name}-metadata-${var.environment}"
  
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.t3.medium"
  
  allocated_storage     = 100
  max_allocated_storage = 1000
  storage_type         = "gp2"
  storage_encrypted    = true
  
  db_name  = "metadata"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = var.environment != "prod"
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}
```

### 2. How do you structure Terraform code for data projects?
**Answer**: Use modules, environments, and proper file organization.

```hcl
# Directory structure:
# ├── environments/
# │   ├── dev/
# │   ├── staging/
# │   └── prod/
# ├── modules/
# │   ├── data-lake/
# │   ├── data-warehouse/
# │   └── processing/
# └── shared/

# modules/data-lake/main.tf
resource "aws_s3_bucket" "raw" {
  bucket = "${var.project_name}-raw-${var.environment}"
}

resource "aws_s3_bucket" "processed" {
  bucket = "${var.project_name}-processed-${var.environment}"
}

resource "aws_s3_bucket" "curated" {
  bucket = "${var.project_name}-curated-${var.environment}"
}

# modules/data-lake/variables.tf
variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

# environments/prod/main.tf
module "data_lake" {
  source = "../../modules/data-lake"
  
  project_name = "analytics-platform"
  environment  = "prod"
}

module "data_warehouse" {
  source = "../../modules/data-warehouse"
  
  project_name = "analytics-platform"
  environment  = "prod"
  instance_class = "dc2.large"
}
```

### 3. How do you manage secrets and sensitive data?
**Answer**: Use external secret management and avoid hardcoding secrets.

```hcl
# Using AWS Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "${var.project_name}-db-password-${var.environment}"
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = var.db_password
}

# Reference secret in RDS
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = aws_secretsmanager_secret.db_password.id
}

resource "aws_db_instance" "main" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
  # ... other configuration
}

# Using external data source
data "external" "vault_secret" {
  program = ["vault", "kv", "get", "-format=json", "secret/database"]
}

locals {
  db_credentials = jsondecode(data.external.vault_secret.result.data)
}
```

## Data Infrastructure (26-50)

### 26. How do you provision a complete data pipeline infrastructure?
**Answer**: Create modular infrastructure for ingestion, processing, and storage.

```hcl
# Complete data pipeline infrastructure
module "vpc" {
  source = "./modules/vpc"
  
  cidr_block = "10.0.0.0/16"
  environment = var.environment
}

module "data_ingestion" {
  source = "./modules/data-ingestion"
  
  vpc_id = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  
  kafka_instance_type = "kafka.m5.large"
  kafka_version = "2.8.0"
  
  kinesis_shard_count = 10
}

module "data_processing" {
  source = "./modules/data-processing"
  
  vpc_id = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  
  emr_instance_type = "m5.xlarge"
  emr_instance_count = 5
  
  lambda_memory_size = 1024
  lambda_timeout = 900
}

module "data_storage" {
  source = "./modules/data-storage"
  
  vpc_id = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  
  redshift_node_type = "dc2.large"
  redshift_cluster_size = 3
  
  elasticsearch_instance_type = "t3.medium.elasticsearch"
  elasticsearch_instance_count = 3
}

# modules/data-processing/main.tf
resource "aws_emr_cluster" "spark_cluster" {
  name          = "${var.project_name}-spark-${var.environment}"
  release_label = "emr-6.4.0"
  applications  = ["Spark", "Hadoop", "Hive"]
  
  ec2_attributes {
    subnet_id = var.private_subnet_ids[0]
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group  = aws_security_group.emr_slave.id
    instance_profile = aws_iam_instance_profile.emr_profile.arn
  }
  
  master_instance_group {
    instance_type = var.emr_instance_type
  }
  
  core_instance_group {
    instance_type  = var.emr_instance_type
    instance_count = var.emr_instance_count
    
    ebs_config {
      size = 100
      type = "gp2"
      volumes_per_instance = 1
    }
  }
  
  configurations_json = jsonencode([
    {
      "Classification": "spark-defaults",
      "Properties": {
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.adaptive.coalescePartitions.enabled": "true"
      }
    }
  ])
  
  service_role = aws_iam_role.emr_service_role.arn
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}
```

### 27. How do you implement auto-scaling for data workloads?
**Answer**: Use auto-scaling groups and managed services with scaling policies.

```hcl
# Auto Scaling Group for data processing workers
resource "aws_autoscaling_group" "data_workers" {
  name = "${var.project_name}-data-workers-${var.environment}"
  
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = [aws_lb_target_group.data_workers.arn]
  health_check_type   = "ELB"
  
  min_size         = var.min_workers
  max_size         = var.max_workers
  desired_capacity = var.desired_workers
  
  launch_template {
    id      = aws_launch_template.data_worker.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "${var.project_name}-data-worker-${var.environment}"
    propagate_at_launch = true
  }
}

# Auto Scaling Policies
resource "aws_autoscaling_policy" "scale_up" {
  name                   = "${var.project_name}-scale-up-${var.environment}"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.data_workers.name
}

resource "aws_autoscaling_policy" "scale_down" {
  name                   = "${var.project_name}-scale-down-${var.environment}"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.data_workers.name
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "${var.project_name}-cpu-high-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.data_workers.name
  }
}
```

## State Management (51-75)

### 51. How do you manage Terraform state for team collaboration?
**Answer**: Use remote state backends with locking and versioning.

```hcl
# Backend configuration
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "data-platform/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# S3 bucket for state storage
resource "aws_s3_bucket" "terraform_state" {
  bucket = "${var.project_name}-terraform-state-${random_id.bucket_suffix.hex}"
  
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_state_lock" {
  name           = "${var.project_name}-terraform-state-lock"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"
  
  attribute {
    name = "LockID"
    type = "S"
  }
  
  tags = {
    Name = "Terraform State Lock Table"
  }
}
```

### 52. How do you handle state migrations and imports?
**Answer**: Use terraform import and state manipulation commands.

```bash
# Import existing resources
terraform import aws_s3_bucket.existing_bucket existing-bucket-name
terraform import aws_db_instance.existing_db existing-db-identifier

# Move resources between states
terraform state mv aws_instance.old_name aws_instance.new_name

# Remove resources from state
terraform state rm aws_instance.no_longer_managed

# Show current state
terraform state list
terraform state show aws_s3_bucket.data_lake

# State migration script
#!/bin/bash
# migrate_state.sh

# Backup current state
terraform state pull > backup-$(date +%Y%m%d-%H%M%S).tfstate

# Import existing resources
terraform import module.data_lake.aws_s3_bucket.raw existing-raw-bucket
terraform import module.data_lake.aws_s3_bucket.processed existing-processed-bucket

# Verify state
terraform plan
```

## Production & Best Practices (76-100)

### 76. How do you implement CI/CD for Terraform?
**Answer**: Use automated pipelines with proper validation and approval processes.

```yaml
# .github/workflows/terraform.yml
name: Terraform CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0
      
      - name: Terraform Format Check
        run: terraform fmt -check -recursive
      
      - name: Terraform Init
        run: terraform init -backend=false
      
      - name: Terraform Validate
        run: terraform validate
      
      - name: Run tflint
        uses: terraform-linters/setup-tflint@v3
        with:
          tflint_version: latest
      
      - name: Run TFLint
        run: tflint --recursive

  plan:
    needs: validate
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      
      - name: Terraform Init
        run: terraform init
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      
      - name: Terraform Plan
        run: terraform plan -no-color
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

  apply:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
      
      - name: Terraform Init
        run: terraform init
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      
      - name: Terraform Apply
        run: terraform apply -auto-approve
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### 77. How do you implement disaster recovery with Terraform?
**Answer**: Use multi-region deployments and backup strategies.

```hcl
# Multi-region deployment
module "primary_region" {
  source = "./modules/data-platform"
  
  providers = {
    aws = aws.primary
  }
  
  region = "us-west-2"
  environment = var.environment
  is_primary = true
}

module "dr_region" {
  source = "./modules/data-platform"
  
  providers = {
    aws = aws.dr
  }
  
  region = "us-east-1"
  environment = var.environment
  is_primary = false
}

# Cross-region replication
resource "aws_s3_bucket_replication_configuration" "replication" {
  role   = aws_iam_role.replication.arn
  bucket = module.primary_region.data_lake_bucket_id
  
  rule {
    id     = "replicate_all"
    status = "Enabled"
    
    destination {
      bucket        = module.dr_region.data_lake_bucket_arn
      storage_class = "STANDARD_IA"
    }
  }
  
  depends_on = [aws_s3_bucket_versioning.primary]
}

# RDS cross-region backup
resource "aws_db_instance" "primary" {
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  copy_tags_to_snapshot  = true
  
  # Enable automated backups
  skip_final_snapshot = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot-${formatdate("YYYY-MM-DD-hhmm", timestamp())}"
}
```

### 78. How do you monitor and alert on infrastructure changes?
**Answer**: Use CloudWatch, SNS, and infrastructure monitoring tools.

```hcl
# CloudWatch alarms for infrastructure
resource "aws_cloudwatch_metric_alarm" "rds_cpu" {
  alarm_name          = "${var.project_name}-rds-cpu-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors RDS cpu utilization"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.main.id
  }
}

# SNS topic for alerts
resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-infrastructure-alerts-${var.environment}"
}

resource "aws_sns_topic_subscription" "email_alerts" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# CloudTrail for infrastructure changes
resource "aws_cloudtrail" "main" {
  name           = "${var.project_name}-cloudtrail-${var.environment}"
  s3_bucket_name = aws_s3_bucket.cloudtrail.bucket
  
  event_selector {
    read_write_type                 = "All"
    include_management_events       = true
    exclude_management_event_sources = []
    
    data_resource {
      type   = "AWS::S3::Object"
      values = ["${aws_s3_bucket.data_lake.arn}/*"]
    }
  }
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}
```

---

**Total Questions: 100** | **Coverage: Complete Terraform for Data Engineering**