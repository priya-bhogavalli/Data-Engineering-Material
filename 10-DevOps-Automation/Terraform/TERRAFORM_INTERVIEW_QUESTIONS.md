# Terraform Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is Terraform and why is it used in data engineering?
**Answer**: Terraform is an Infrastructure as Code (IaC) tool that allows you to define and provision infrastructure using declarative configuration files.

**Key Benefits for Data Engineering**:
- **Infrastructure as Code**: Version control and reproducible infrastructure
- **Multi-Cloud Support**: Deploy across AWS, Azure, GCP, and other providers
- **Resource Management**: Automated provisioning and deprovisioning
- **State Management**: Track infrastructure changes and dependencies

```hcl
# Example: Data pipeline infrastructure
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

# S3 bucket for data storage
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${var.environment}"
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    Purpose     = "Data Lake"
  }
}

# RDS instance for metadata
resource "aws_db_instance" "metadata_db" {
  identifier = "${var.project_name}-metadata-${var.environment}"
  
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.t3.micro"
  
  allocated_storage = 20
  storage_encrypted = true
  
  db_name  = "metadata"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}
```

### 2. Explain Terraform's core concepts
**Answer**: Terraform uses several key concepts to manage infrastructure.

**Core Components**:
- **Provider**: Plugin that interacts with APIs (AWS, Azure, GCP)
- **Resource**: Infrastructure component (EC2 instance, S3 bucket)
- **Data Source**: Read-only information from existing infrastructure
- **Variable**: Input parameters for configurations
- **Output**: Return values from configurations
- **Module**: Reusable configuration components

```hcl
# Variables
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "instance_count" {
  description = "Number of instances"
  type        = number
  default     = 2
}

# Data source
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

# Resource
resource "aws_instance" "data_processor" {
  count = var.instance_count
  
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  
  tags = {
    Name        = "data-processor-${count.index + 1}"
    Environment = var.environment
  }
}

# Output
output "instance_ips" {
  description = "IP addresses of data processor instances"
  value       = aws_instance.data_processor[*].public_ip
}
```

### 3. How does Terraform state management work?
**Answer**: Terraform state tracks the current state of infrastructure and maps configuration to real-world resources.

```hcl
# Backend configuration for remote state
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "data-pipeline/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# State locking with DynamoDB
resource "aws_dynamodb_table" "terraform_state_lock" {
  name           = "terraform-state-lock"
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

**State Management Commands**:
```bash
# Initialize Terraform
terraform init

# Plan changes
terraform plan

# Apply changes
terraform apply

# Show current state
terraform show

# List resources in state
terraform state list

# Import existing resource
terraform import aws_instance.example i-1234567890abcdef0

# Remove resource from state
terraform state rm aws_instance.example

# Refresh state
terraform refresh
```

### 4. What are Terraform modules and how do you use them?
**Answer**: Modules are reusable Terraform configurations that encapsulate related resources.

```hcl
# Module structure
# modules/data-pipeline/
# ├── main.tf
# ├── variables.tf
# ├── outputs.tf
# └── README.md

# modules/data-pipeline/main.tf
resource "aws_s3_bucket" "data_bucket" {
  bucket = "${var.project_name}-${var.environment}-data"
  
  tags = var.tags
}

resource "aws_glue_job" "etl_job" {
  name     = "${var.project_name}-etl-${var.environment}"
  role_arn = aws_iam_role.glue_role.arn
  
  command {
    script_location = "s3://${aws_s3_bucket.data_bucket.bucket}/scripts/etl.py"
    python_version  = "3"
  }
  
  default_arguments = {
    "--job-language" = "python"
    "--job-bookmark-option" = "job-bookmark-enable"
  }
  
  tags = var.tags
}

# modules/data-pipeline/variables.tf
variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

# modules/data-pipeline/outputs.tf
output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.data_bucket.bucket
}

output "glue_job_name" {
  description = "Name of the Glue job"
  value       = aws_glue_job.etl_job.name
}
```

**Using the Module**:
```hcl
# main.tf
module "data_pipeline" {
  source = "./modules/data-pipeline"
  
  project_name = "customer-analytics"
  environment  = "production"
  
  tags = {
    Owner       = "data-team"
    Environment = "production"
    Project     = "customer-analytics"
  }
}

# Access module outputs
output "pipeline_bucket" {
  value = module.data_pipeline.bucket_name
}
```

### 5. How do you handle different environments with Terraform?
**Answer**: Use workspaces, variable files, and conditional logic to manage multiple environments.

```hcl
# terraform.tfvars.dev
environment = "dev"
instance_type = "t3.micro"
min_size = 1
max_size = 2

# terraform.tfvars.prod
environment = "prod"
instance_type = "t3.large"
min_size = 3
max_size = 10

# main.tf with conditional logic
resource "aws_instance" "app" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"
  
  tags = {
    Name        = "${var.project_name}-${var.environment}"
    Environment = var.environment
  }
}

# Environment-specific configurations
locals {
  env_config = {
    dev = {
      instance_count = 1
      storage_size   = 20
    }
    staging = {
      instance_count = 2
      storage_size   = 50
    }
    prod = {
      instance_count = 5
      storage_size   = 100
    }
  }
  
  current_env = local.env_config[var.environment]
}

resource "aws_instance" "data_processor" {
  count = local.current_env.instance_count
  
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  
  root_block_device {
    volume_size = local.current_env.storage_size
  }
}
```

**Environment Management Commands**:
```bash
# Using variable files
terraform plan -var-file="terraform.tfvars.dev"
terraform apply -var-file="terraform.tfvars.prod"

# Using workspaces
terraform workspace new dev
terraform workspace new prod
terraform workspace select dev
terraform workspace list
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you implement data pipeline infrastructure with Terraform?
**Answer**: Create comprehensive data pipeline infrastructure including storage, compute, networking, and monitoring.

```hcl
# Complete data pipeline infrastructure
# VPC and networking
resource "aws_vpc" "data_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

resource "aws_subnet" "private_subnets" {
  count = length(var.availability_zones)
  
  vpc_id            = aws_vpc.data_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name = "${var.project_name}-private-${count.index + 1}"
  }
}

# S3 buckets for data lake
resource "aws_s3_bucket" "raw_data" {
  bucket = "${var.project_name}-raw-data-${random_id.bucket_suffix.hex}"
}

resource "aws_s3_bucket" "processed_data" {
  bucket = "${var.project_name}-processed-data-${random_id.bucket_suffix.hex}"
}

resource "aws_s3_bucket" "curated_data" {
  bucket = "${var.project_name}-curated-data-${random_id.bucket_suffix.hex}"
}

# EMR cluster for big data processing
resource "aws_emr_cluster" "data_processing" {
  name          = "${var.project_name}-emr-cluster"
  release_label = "emr-6.4.0"
  applications  = ["Spark", "Hadoop", "Hive"]
  
  ec2_attributes {
    subnet_id                         = aws_subnet.private_subnets[0].id
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group  = aws_security_group.emr_slave.id
    instance_profile                  = aws_iam_instance_profile.emr_profile.arn
  }
  
  master_instance_group {
    instance_type = "m5.xlarge"
  }
  
  core_instance_group {
    instance_type  = "m5.large"
    instance_count = var.core_instance_count
    
    ebs_config {
      size                 = 40
      type                 = "gp2"
      volumes_per_instance = 1
    }
  }
  
  service_role = aws_iam_role.emr_service_role.arn
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Glue Data Catalog
resource "aws_glue_catalog_database" "data_catalog" {
  name = "${var.project_name}_data_catalog"
  
  description = "Data catalog for ${var.project_name}"
}

# Glue Crawler
resource "aws_glue_crawler" "data_crawler" {
  database_name = aws_glue_catalog_database.data_catalog.name
  name          = "${var.project_name}-crawler"
  role          = aws_iam_role.glue_role.arn
  
  s3_target {
    path = "s3://${aws_s3_bucket.raw_data.bucket}/"
  }
  
  schedule = "cron(0 2 * * ? *)"  # Daily at 2 AM
}

# Lambda function for data processing triggers
resource "aws_lambda_function" "data_trigger" {
  filename         = "data_trigger.zip"
  function_name    = "${var.project_name}-data-trigger"
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 300
  
  environment {
    variables = {
      EMR_CLUSTER_ID = aws_emr_cluster.data_processing.id
      S3_BUCKET      = aws_s3_bucket.raw_data.bucket
    }
  }
}

# CloudWatch for monitoring
resource "aws_cloudwatch_log_group" "data_pipeline_logs" {
  name              = "/aws/lambda/${aws_lambda_function.data_trigger.function_name}"
  retention_in_days = 14
}

# SNS for notifications
resource "aws_sns_topic" "data_pipeline_alerts" {
  name = "${var.project_name}-pipeline-alerts"
}

resource "aws_sns_topic_subscription" "email_alerts" {
  topic_arn = aws_sns_topic.data_pipeline_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}
```

### 7. How do you manage secrets and sensitive data in Terraform?
**Answer**: Use AWS Secrets Manager, Parameter Store, and Terraform sensitive variables.

```hcl
# AWS Secrets Manager
resource "aws_secretsmanager_secret" "db_credentials" {
  name        = "${var.project_name}-db-credentials"
  description = "Database credentials for ${var.project_name}"
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
  })
}

# Parameter Store for configuration
resource "aws_ssm_parameter" "api_key" {
  name  = "/${var.project_name}/${var.environment}/api_key"
  type  = "SecureString"
  value = var.api_key
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Using secrets in resources
data "aws_secretsmanager_secret_version" "db_creds" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
}

locals {
  db_creds = jsondecode(data.aws_secretsmanager_secret_version.db_creds.secret_string)
}

resource "aws_db_instance" "main" {
  identifier = "${var.project_name}-db"
  
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.t3.micro"
  
  allocated_storage = 20
  
  db_name  = var.db_name
  username = local.db_creds.username
  password = local.db_creds.password
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# Sensitive variables
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "api_key" {
  description = "API key for external service"
  type        = string
  sensitive   = true
}
```

### 8. How do you implement CI/CD for Terraform?
**Answer**: Use automated pipelines with proper validation, planning, and approval processes.

```yaml
# .github/workflows/terraform.yml
name: Terraform CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  TF_VERSION: 1.5.0
  AWS_REGION: us-west-2

jobs:
  validate:
    name: Validate Terraform
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TF_VERSION }}
    
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
    name: Plan Terraform
    runs-on: ubuntu-latest
    needs: validate
    if: github.event_name == 'pull_request'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TF_VERSION }}
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Terraform Init
      run: terraform init
    
    - name: Terraform Plan
      run: terraform plan -var-file="environments/dev.tfvars" -out=tfplan
    
    - name: Save plan
      uses: actions/upload-artifact@v3
      with:
        name: terraform-plan
        path: tfplan

  apply:
    name: Apply Terraform
    runs-on: ubuntu-latest
    needs: validate
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: ${{ env.TF_VERSION }}
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Terraform Init
      run: terraform init
    
    - name: Terraform Apply
      run: terraform apply -var-file="environments/prod.tfvars" -auto-approve
```

### 9. How do you handle Terraform state in team environments?
**Answer**: Use remote backends, state locking, and proper access controls.

```hcl
# Remote backend configuration
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "data-pipeline/prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    
    # Role-based access
    role_arn = "arn:aws:iam::123456789012:role/TerraformStateRole"
  }
}

# State bucket with versioning and encryption
resource "aws_s3_bucket" "terraform_state" {
  bucket = "company-terraform-state"
  
  tags = {
    Name        = "Terraform State Bucket"
    Environment = "shared"
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

resource "aws_s3_bucket_public_access_block" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_state_lock" {
  name           = "terraform-state-lock"
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

### 10. How do you implement disaster recovery with Terraform?
**Answer**: Design multi-region infrastructure with automated failover and backup strategies.

```hcl
# Multi-region setup
locals {
  regions = {
    primary   = "us-west-2"
    secondary = "us-east-1"
  }
}

# Primary region resources
module "primary_infrastructure" {
  source = "./modules/data-infrastructure"
  
  providers = {
    aws = aws.primary
  }
  
  region      = local.regions.primary
  environment = var.environment
  is_primary  = true
  
  # Cross-region replication settings
  backup_region = local.regions.secondary
}

# Secondary region resources
module "secondary_infrastructure" {
  source = "./modules/data-infrastructure"
  
  providers = {
    aws = aws.secondary
  }
  
  region      = local.regions.secondary
  environment = var.environment
  is_primary  = false
  
  # Standby configuration
  primary_region = local.regions.primary
}

# Cross-region S3 replication
resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws.primary
  
  role   = aws_iam_role.replication.arn
  bucket = module.primary_infrastructure.data_bucket_id
  
  rule {
    id     = "replicate-to-secondary"
    status = "Enabled"
    
    destination {
      bucket        = module.secondary_infrastructure.data_bucket_arn
      storage_class = "STANDARD_IA"
    }
  }
  
  depends_on = [aws_s3_bucket_versioning.primary]
}

# Route 53 health checks and failover
resource "aws_route53_health_check" "primary" {
  fqdn                            = module.primary_infrastructure.api_endpoint
  port                            = 443
  type                            = "HTTPS"
  resource_path                   = "/health"
  failure_threshold               = 3
  request_interval                = 30
  
  tags = {
    Name = "Primary Region Health Check"
  }
}

resource "aws_route53_record" "api_primary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain_name}"
  type    = "A"
  
  set_identifier = "primary"
  
  failover_routing_policy {
    type = "PRIMARY"
  }
  
  health_check_id = aws_route53_health_check.primary.id
  
  alias {
    name                   = module.primary_infrastructure.load_balancer_dns
    zone_id                = module.primary_infrastructure.load_balancer_zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "api_secondary" {
  zone_id = aws_route53_zone.main.zone_id
  name    = "api.${var.domain_name}"
  type    = "A"
  
  set_identifier = "secondary"
  
  failover_routing_policy {
    type = "SECONDARY"
  }
  
  alias {
    name                   = module.secondary_infrastructure.load_balancer_dns
    zone_id                = module.secondary_infrastructure.load_balancer_zone_id
    evaluate_target_health = true
  }
}
```

This comprehensive set covers Terraform fundamentals through advanced infrastructure management concepts with practical data engineering examples.