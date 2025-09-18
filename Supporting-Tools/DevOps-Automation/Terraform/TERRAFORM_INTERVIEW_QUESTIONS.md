# Terraform Comprehensive Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Configuration & Syntax (16-30)](#configuration--syntax-16-30)
3. [State Management (31-45)](#state-management-31-45)
4. [Modules & Reusability (46-60)](#modules--reusability-46-60)
5. [Cloud Provider Integration (61-75)](#cloud-provider-integration-61-75)
6. [Advanced Features (76-90)](#advanced-features-76-90)
7. [Data Infrastructure Patterns (91-100)](#data-infrastructure-patterns-91-100)

---

## 🎯 **Introduction**

Terraform is an Infrastructure as Code (IaC) tool that enables you to build, change, and version infrastructure safely and efficiently. For data engineers, Terraform provides automated provisioning of data infrastructure including databases, data lakes, processing clusters, and networking components.

**Why Terraform is Critical for Data Engineers:**
- **Infrastructure as Code**: Version-controlled, repeatable infrastructure
- **Multi-Cloud Support**: Consistent provisioning across AWS, Azure, GCP
- **Resource Management**: Automated lifecycle management of data resources
- **Scalability**: Dynamic scaling of data processing infrastructure
- **Cost Optimization**: Automated resource cleanup and optimization

---

## Core Concepts Questions (1-15)

### 1. Explain Terraform's core workflow and architecture.
**Answer**: 
Terraform follows a declarative approach with a specific workflow for infrastructure management.

**Core Workflow:**
1. **Write**: Define infrastructure in configuration files
2. **Plan**: Preview changes before applying
3. **Apply**: Provision infrastructure
4. **Destroy**: Clean up resources when needed

**Architecture Components:**
- **Configuration Files**: `.tf` files defining desired state
- **State File**: Tracks current infrastructure state
- **Providers**: Plugins for cloud platforms and services
- **Resources**: Infrastructure components to manage
- **Data Sources**: Read-only information from existing infrastructure

```hcl
# Example Terraform configuration
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      Project     = "data-engineering"
      ManagedBy   = "terraform"
    }
  }
}

# Data source example
data "aws_availability_zones" "available" {
  state = "available"
}

# Resource example
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${var.environment}"
  
  tags = {
    Name        = "Data Lake"
    Environment = var.environment
  }
}
```

### 2. What are Terraform providers and how do they work?
**Answer**: 
Providers are plugins that enable Terraform to interact with cloud platforms, SaaS providers, and other APIs.

**Provider Configuration:**
```hcl
# AWS Provider
provider "aws" {
  region     = "us-west-2"
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  
  # Alternative: Use IAM roles
  assume_role {
    role_arn = "arn:aws:iam::123456789012:role/TerraformRole"
  }
}

# Azure Provider
provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
  tenant_id       = var.azure_tenant_id
}

# Google Cloud Provider
provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  zone    = var.gcp_zone
}

# Multiple provider instances
provider "aws" {
  alias  = "us_east"
  region = "us-east-1"
}

provider "aws" {
  alias  = "us_west"
  region = "us-west-2"
}

# Using aliased providers
resource "aws_s3_bucket" "east_bucket" {
  provider = aws.us_east
  bucket   = "data-east-bucket"
}

resource "aws_s3_bucket" "west_bucket" {
  provider = aws.us_west
  bucket   = "data-west-bucket"
}
```

### 3. How do you manage variables and outputs in Terraform?
**Answer**: 
Variables and outputs provide flexibility and information sharing in Terraform configurations.

**Variable Definitions:**
```hcl
# variables.tf
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "instance_types" {
  description = "Map of instance types for different services"
  type = map(string)
  default = {
    web = "t3.medium"
    app = "t3.large"
    db  = "r5.xlarge"
  }
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

variable "database_config" {
  description = "Database configuration object"
  type = object({
    engine         = string
    engine_version = string
    instance_class = string
    allocated_storage = number
    multi_az       = bool
  })
  default = {
    engine         = "postgres"
    engine_version = "13.7"
    instance_class = "db.t3.medium"
    allocated_storage = 100
    multi_az       = true
  }
}

# Sensitive variables
variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

**Variable Files:**
```hcl
# terraform.tfvars
environment = "production"
aws_region  = "us-west-2"

instance_types = {
  web = "t3.large"
  app = "t3.xlarge"
  db  = "r5.2xlarge"
}

database_config = {
  engine         = "postgres"
  engine_version = "14.6"
  instance_class = "db.r5.xlarge"
  allocated_storage = 500
  multi_az       = true
}

# dev.tfvars
environment = "dev"
instance_types = {
  web = "t3.micro"
  app = "t3.small"
  db  = "db.t3.micro"
}
```

**Output Values:**
```hcl
# outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "s3_bucket_names" {
  description = "Names of created S3 buckets"
  value = {
    data_lake = aws_s3_bucket.data_lake.bucket
    logs      = aws_s3_bucket.logs.bucket
    backups   = aws_s3_bucket.backups.bucket
  }
}

output "cluster_info" {
  description = "Kubernetes cluster information"
  value = {
    cluster_name     = aws_eks_cluster.main.name
    cluster_endpoint = aws_eks_cluster.main.endpoint
    cluster_version  = aws_eks_cluster.main.version
    node_groups      = {
      for ng in aws_eks_node_group.workers : ng.node_group_name => {
        instance_types = ng.instance_types
        scaling_config = ng.scaling_config
      }
    }
  }
}
```

## Configuration & Syntax (16-30)

### 4. How do you use loops and conditionals in Terraform?
**Answer**: 
Terraform provides several mechanisms for iteration and conditional logic.

**Count Parameter:**
```hcl
# Create multiple similar resources
resource "aws_instance" "web_servers" {
  count         = var.web_server_count
  ami           = var.ami_id
  instance_type = var.instance_type
  
  tags = {
    Name = "web-server-${count.index + 1}"
  }
}

# Conditional resource creation
resource "aws_instance" "bastion" {
  count = var.create_bastion ? 1 : 0
  
  ami           = var.ami_id
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public[0].id
  
  tags = {
    Name = "bastion-host"
  }
}
```

**For_each Meta-argument:**
```hcl
# Create resources from a map
variable "databases" {
  type = map(object({
    engine         = string
    instance_class = string
    allocated_storage = number
  }))
  default = {
    "analytics" = {
      engine         = "postgres"
      instance_class = "db.t3.medium"
      allocated_storage = 100
    }
    "warehouse" = {
      engine         = "postgres"
      instance_class = "db.r5.large"
      allocated_storage = 500
    }
  }
}

resource "aws_db_instance" "databases" {
  for_each = var.databases
  
  identifier     = each.key
  engine         = each.value.engine
  instance_class = each.value.instance_class
  allocated_storage = each.value.allocated_storage
  
  db_name  = each.key
  username = "admin"
  password = var.db_password
  
  tags = {
    Name = "${each.key}-database"
  }
}

# Create subnets across availability zones
resource "aws_subnet" "private" {
  for_each = toset(var.availability_zones)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(aws_vpc.main.cidr_block, 8, index(var.availability_zones, each.value) + 10)
  availability_zone = each.value
  
  tags = {
    Name = "private-subnet-${each.value}"
    Type = "private"
  }
}
```

**Dynamic Blocks:**
```hcl
# Dynamic security group rules
variable "ingress_rules" {
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = [
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTP"
    },
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTPS"
    }
  ]
}

resource "aws_security_group" "web" {
  name_prefix = "web-sg"
  vpc_id      = aws_vpc.main.id
  
  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
      description = ingress.value.description
    }
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### 5. How do you handle dependencies and resource ordering in Terraform?
**Answer**: 
Terraform manages dependencies through implicit and explicit dependency mechanisms.

**Implicit Dependencies:**
```hcl
# Terraform automatically detects dependencies through resource references
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "main-vpc"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id  # Implicit dependency on VPC
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-west-2a"
  map_public_ip_on_launch = true
  
  tags = {
    Name = "public-subnet"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id  # Implicit dependency on VPC
  
  tags = {
    Name = "main-igw"
  }
}
```

**Explicit Dependencies:**
```hcl
# Use depends_on for explicit dependencies
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = "t3.medium"
  subnet_id     = aws_subnet.public.id
  
  # Explicit dependency - ensure NAT gateway is created first
  depends_on = [
    aws_nat_gateway.main,
    aws_route_table_association.private
  ]
  
  user_data = templatefile("${path.module}/user_data.sh", {
    database_endpoint = aws_db_instance.main.endpoint
  })
  
  tags = {
    Name = "web-server"
  }
}

# Null resource for custom provisioning steps
resource "null_resource" "database_setup" {
  depends_on = [aws_db_instance.main]
  
  provisioner "local-exec" {
    command = "python scripts/setup_database.py --endpoint ${aws_db_instance.main.endpoint}"
  }
  
  triggers = {
    database_version = aws_db_instance.main.engine_version
  }
}
```

## State Management (31-45)

### 6. How do you manage Terraform state in team environments?
**Answer**: 
Remote state management is crucial for team collaboration and state consistency.

**Remote State Configuration:**
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "data-engineering/prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    
    # Optional: Use assume role for cross-account access
    role_arn = "arn:aws:iam::123456789012:role/TerraformStateRole"
  }
}

# Alternative: Azure backend
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "terraformstatestorage"
    container_name       = "tfstate"
    key                  = "data-engineering.terraform.tfstate"
  }
}

# Alternative: GCS backend
terraform {
  backend "gcs" {
    bucket = "terraform-state-bucket"
    prefix = "data-engineering/prod"
  }
}
```

**State Locking Setup:**
```hcl
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
    Name        = "Terraform State Lock Table"
    Environment = "shared"
  }
}

# S3 bucket for state storage
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
```

### 7. How do you handle state file corruption and recovery?
**Answer**: 
State file management includes backup strategies and recovery procedures.

**State Management Commands:**
```bash
# Backup current state
terraform state pull > terraform.tfstate.backup

# List resources in state
terraform state list

# Show specific resource state
terraform state show aws_instance.web

# Remove resource from state (without destroying)
terraform state rm aws_instance.old_server

# Import existing resource into state
terraform import aws_instance.web i-1234567890abcdef0

# Move resource to different address
terraform state mv aws_instance.web aws_instance.web_server

# Replace provider in state
terraform state replace-provider hashicorp/aws registry.terraform.io/hashicorp/aws
```

**State Recovery Procedures:**
```bash
# Restore from backup
cp terraform.tfstate.backup terraform.tfstate

# Force unlock state (use carefully)
terraform force-unlock LOCK_ID

# Refresh state from actual infrastructure
terraform refresh

# Validate state consistency
terraform plan -detailed-exitcode

# Recovery script example
#!/bin/bash
set -e

echo "Starting state recovery process..."

# Create backup of current state
terraform state pull > "state-backup-$(date +%Y%m%d-%H%M%S).json"

# Validate current state
if terraform plan -detailed-exitcode; then
    echo "State is consistent with configuration"
else
    echo "State inconsistencies detected, attempting recovery..."
    
    # Refresh state from actual infrastructure
    terraform refresh
    
    # Re-validate
    if terraform plan -detailed-exitcode; then
        echo "State recovery successful"
    else
        echo "Manual intervention required"
        exit 1
    fi
fi
```

## Modules & Reusability (46-60)

### 8. How do you create and use Terraform modules effectively?
**Answer**: 
Modules promote reusability and maintainability in Terraform configurations.

**Module Structure:**
```
modules/
├── vpc/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
├── rds/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── README.md
└── eks/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

**VPC Module Example:**
```hcl
# modules/vpc/variables.tf
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway"
  type        = bool
  default     = true
}

# modules/vpc/main.tf
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count = length(var.availability_zones)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, count.index)
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name        = "${var.environment}-public-subnet-${count.index + 1}"
    Environment = var.environment
    Type        = "public"
  }
}

resource "aws_subnet" "private" {
  count = length(var.availability_zones)
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = var.availability_zones[count.index]
  
  tags = {
    Name        = "${var.environment}-private-subnet-${count.index + 1}"
    Environment = var.environment
    Type        = "private"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name        = "${var.environment}-igw"
    Environment = var.environment
  }
}

resource "aws_nat_gateway" "main" {
  count = var.enable_nat_gateway ? length(var.availability_zones) : 0
  
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = {
    Name        = "${var.environment}-nat-gateway-${count.index + 1}"
    Environment = var.environment
  }
  
  depends_on = [aws_internet_gateway.main]
}

resource "aws_eip" "nat" {
  count = var.enable_nat_gateway ? length(var.availability_zones) : 0
  
  domain = "vpc"
  
  tags = {
    Name        = "${var.environment}-nat-eip-${count.index + 1}"
    Environment = var.environment
  }
}

# modules/vpc/outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = aws_subnet.private[*].id
}

output "internet_gateway_id" {
  description = "ID of the Internet Gateway"
  value       = aws_internet_gateway.main.id
}

output "nat_gateway_ids" {
  description = "IDs of the NAT Gateways"
  value       = aws_nat_gateway.main[*].id
}
```

**Using Modules:**
```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"
  
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]
  environment        = var.environment
  enable_nat_gateway = true
}

module "rds" {
  source = "./modules/rds"
  
  vpc_id               = module.vpc.vpc_id
  private_subnet_ids   = module.vpc.private_subnet_ids
  database_name        = "datawarehouse"
  master_username      = "admin"
  master_password      = var.db_password
  instance_class       = "db.r5.xlarge"
  allocated_storage    = 500
  environment          = var.environment
}

module "eks" {
  source = "./modules/eks"
  
  cluster_name       = "${var.environment}-data-cluster"
  vpc_id             = module.vpc.vpc_id
  private_subnet_ids = module.vpc.private_subnet_ids
  public_subnet_ids  = module.vpc.public_subnet_ids
  environment        = var.environment
  
  node_groups = {
    general = {
      instance_types = ["t3.medium"]
      scaling_config = {
        desired_size = 2
        max_size     = 10
        min_size     = 1
      }
    }
    compute = {
      instance_types = ["c5.xlarge"]
      scaling_config = {
        desired_size = 0
        max_size     = 20
        min_size     = 0
      }
    }
  }
}
```

## Cloud Provider Integration (61-75)

### 9. How do you provision AWS data infrastructure with Terraform?
**Answer**: 
Terraform provides comprehensive AWS resource management for data engineering workloads.

**Complete AWS Data Infrastructure:**
```hcl
# S3 Data Lake
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${var.environment}"
  
  tags = {
    Name        = "Data Lake"
    Environment = var.environment
    Purpose     = "data-storage"
  }
}

resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  
  rule {
    id     = "transition_to_ia"
    status = "Enabled"
    
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    
    transition {
      days          = 365
      storage_class = "DEEP_ARCHIVE"
    }
  }
}

# Redshift Data Warehouse
resource "aws_redshift_cluster" "data_warehouse" {
  cluster_identifier      = "${var.project_name}-warehouse-${var.environment}"
  database_name          = "datawarehouse"
  master_username        = "admin"
  master_password        = var.redshift_password
  node_type              = "dc2.large"
  cluster_type           = "multi-node"
  number_of_nodes        = 3
  
  vpc_security_group_ids = [aws_security_group.redshift.id]
  db_subnet_group_name   = aws_redshift_subnet_group.main.name
  
  skip_final_snapshot = var.environment != "prod"
  
  tags = {
    Name        = "Data Warehouse"
    Environment = var.environment
  }
}

resource "aws_redshift_subnet_group" "main" {
  name       = "${var.project_name}-redshift-subnet-group"
  subnet_ids = var.private_subnet_ids
  
  tags = {
    Name        = "Redshift subnet group"
    Environment = var.environment
  }
}

# EMR Cluster for Spark Processing
resource "aws_emr_cluster" "spark_cluster" {
  name          = "${var.project_name}-spark-${var.environment}"
  release_label = "emr-6.10.0"
  applications  = ["Spark", "Hadoop", "Hive", "Zeppelin"]
  
  ec2_attributes {
    subnet_id                         = var.private_subnet_ids[0]
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group  = aws_security_group.emr_slave.id
    instance_profile                  = aws_iam_instance_profile.emr_profile.arn
    key_name                         = var.key_pair_name
  }
  
  master_instance_group {
    instance_type = "m5.xlarge"
  }
  
  core_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 2
    
    ebs_config {
      size                 = 40
      type                 = "gp2"
      volumes_per_instance = 1
    }
  }
  
  configurations_json = jsonencode([
    {
      "Classification": "spark-defaults",
      "Properties": {
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.adaptive.coalescePartitions.enabled": "true",
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer"
      }
    }
  ])
  
  service_role = aws_iam_role.emr_service_role.arn
  
  tags = {
    Name        = "Spark Processing Cluster"
    Environment = var.environment
  }
}

# Kinesis Data Streams
resource "aws_kinesis_stream" "data_stream" {
  name             = "${var.project_name}-data-stream-${var.environment}"
  shard_count      = 2
  retention_period = 24
  
  shard_level_metrics = [
    "IncomingRecords",
    "OutgoingRecords",
  ]
  
  stream_mode_details {
    stream_mode = "PROVISIONED"
  }
  
  tags = {
    Name        = "Data Stream"
    Environment = var.environment
  }
}

# Lambda for Stream Processing
resource "aws_lambda_function" "stream_processor" {
  filename         = "stream_processor.zip"
  function_name    = "${var.project_name}-stream-processor-${var.environment}"
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("stream_processor.zip")
  runtime         = "python3.9"
  timeout         = 300
  
  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.data_lake.bucket
      REDSHIFT_CLUSTER = aws_redshift_cluster.data_warehouse.cluster_identifier
    }
  }
  
  tags = {
    Name        = "Stream Processor"
    Environment = var.environment
  }
}

# Event Source Mapping
resource "aws_lambda_event_source_mapping" "kinesis_lambda" {
  event_source_arn  = aws_kinesis_stream.data_stream.arn
  function_name     = aws_lambda_function.stream_processor.arn
  starting_position = "LATEST"
  batch_size        = 100
}
```

### 10. How do you implement multi-cloud infrastructure with Terraform?
**Answer**: 
Terraform supports multi-cloud deployments through multiple provider configurations.

**Multi-Cloud Data Pipeline:**
```hcl
# providers.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

# AWS Resources
resource "aws_s3_bucket" "primary_data_lake" {
  bucket = "${var.project_name}-primary-data-lake"
  
  tags = {
    Cloud       = "AWS"
    Environment = var.environment
  }
}

# Azure Resources
resource "azurerm_resource_group" "main" {
  name     = "${var.project_name}-rg"
  location = var.azure_location
  
  tags = {
    Cloud       = "Azure"
    Environment = var.environment
  }
}

resource "azurerm_storage_account" "data_lake" {
  name                     = "${replace(var.project_name, "-", "")}datalake"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled          = true  # Enable hierarchical namespace for Data Lake
  
  tags = {
    Cloud       = "Azure"
    Environment = var.environment
  }
}

# GCP Resources
resource "google_storage_bucket" "backup_data_lake" {
  name     = "${var.project_name}-backup-data-lake"
  location = var.gcp_region
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
  
  labels = {
    cloud       = "gcp"
    environment = var.environment
  }
}

# Cross-cloud data replication
resource "aws_s3_bucket_replication_configuration" "cross_cloud" {
  role   = aws_iam_role.replication.arn
  bucket = aws_s3_bucket.primary_data_lake.id
  
  rule {
    id     = "replicate-to-gcp"
    status = "Enabled"
    
    destination {
      bucket        = "arn:aws:s3:::${google_storage_bucket.backup_data_lake.name}"
      storage_class = "STANDARD_IA"
    }
  }
  
  depends_on = [aws_s3_bucket_versioning.primary_data_lake]
}
```

## Advanced Features (76-90)

### 11. How do you implement Terraform workspaces and environment management?
**Answer**: 
Workspaces provide environment isolation and configuration management.

**Workspace Management:**
```bash
# Create and manage workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# List workspaces
terraform workspace list

# Switch workspace
terraform workspace select prod

# Show current workspace
terraform workspace show

# Delete workspace
terraform workspace delete dev
```

**Environment-Specific Configuration:**
```hcl
# variables.tf
variable "environment_configs" {
  description = "Environment-specific configurations"
  type = map(object({
    instance_type = string
    min_size      = number
    max_size      = number
    desired_size  = number
  }))
  default = {
    dev = {
      instance_type = "t3.small"
      min_size      = 1
      max_size      = 3
      desired_size  = 1
    }
    staging = {
      instance_type = "t3.medium"
      min_size      = 2
      max_size      = 5
      desired_size  = 2
    }
    prod = {
      instance_type = "t3.large"
      min_size      = 3
      max_size      = 10
      desired_size  = 3
    }
  }
}

# main.tf
locals {
  environment = terraform.workspace
  config      = var.environment_configs[local.environment]
  
  common_tags = {
    Environment = local.environment
    Workspace   = terraform.workspace
    ManagedBy   = "terraform"
  }
}

resource "aws_launch_template" "app" {
  name_prefix   = "${local.environment}-app-"
  image_id      = var.ami_id
  instance_type = local.config.instance_type
  
  vpc_security_group_ids = [aws_security_group.app.id]
  
  tag_specifications {
    resource_type = "instance"
    tags = merge(local.common_tags, {
      Name = "${local.environment}-app-server"
    })
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "${local.environment}-app-asg"
  vpc_zone_identifier = var.private_subnet_ids
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  
  min_size         = local.config.min_size
  max_size         = local.config.max_size
  desired_capacity = local.config.desired_size
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "${local.environment}-app-asg"
    propagate_at_launch = false
  }
  
  dynamic "tag" {
    for_each = local.common_tags
    content {
      key                 = tag.key
      value               = tag.value
      propagate_at_launch = true
    }
  }
}

# Environment-specific backend configuration
terraform {
  backend "s3" {
    bucket = "company-terraform-state"
    key    = "data-engineering/${terraform.workspace}/terraform.tfstate"
    region = "us-west-2"
  }
}
```

### 12. How do you implement custom providers and provisioners?
**Answer**: 
Custom providers and provisioners extend Terraform's capabilities for specific use cases.

**Custom Provisioners:**
```hcl
# Local provisioner for setup scripts
resource "aws_instance" "data_server" {
  ami           = var.ami_id
  instance_type = "t3.large"
  key_name      = var.key_pair_name
  subnet_id     = var.private_subnet_id
  
  provisioner "local-exec" {
    command = "echo 'Instance ${self.id} created at ${timestamp()}' >> deployment.log"
  }
  
  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y docker.io",
      "sudo systemctl start docker",
      "sudo systemctl enable docker",
      "sudo docker pull apache/spark:3.4.0"
    ]
    
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
      host        = self.private_ip
    }
  }
  
  provisioner "file" {
    source      = "scripts/setup_spark.sh"
    destination = "/tmp/setup_spark.sh"
    
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
      host        = self.private_ip
    }
  }
  
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup_spark.sh",
      "/tmp/setup_spark.sh"
    ]
    
    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file(var.private_key_path)
      host        = self.private_ip
    }
  }
}

# Null resource for custom operations
resource "null_resource" "database_migration" {
  triggers = {
    database_version = aws_db_instance.main.engine_version
    migration_hash   = filemd5("migrations/latest.sql")
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      python scripts/run_migration.py \
        --host ${aws_db_instance.main.endpoint} \
        --database ${aws_db_instance.main.db_name} \
        --username ${var.db_username} \
        --password ${var.db_password}
    EOT
    
    environment = {
      PGPASSWORD = var.db_password
    }
  }
  
  depends_on = [aws_db_instance.main]
}
```

## Data Infrastructure Patterns (91-100)

### 13. How do you implement a complete data lake architecture with Terraform?
**Answer**: 
A comprehensive data lake requires storage, processing, cataloging, and security components.

**Complete Data Lake Infrastructure:**
```hcl
# Data Lake Storage Layers
resource "aws_s3_bucket" "raw_data" {
  bucket = "${var.project_name}-raw-data-${var.environment}"
  
  tags = {
    Name  = "Raw Data Layer"
    Layer = "raw"
  }
}

resource "aws_s3_bucket" "processed_data" {
  bucket = "${var.project_name}-processed-data-${var.environment}"
  
  tags = {
    Name  = "Processed Data Layer"
    Layer = "processed"
  }
}

resource "aws_s3_bucket" "curated_data" {
  bucket = "${var.project_name}-curated-data-${var.environment}"
  
  tags = {
    Name  = "Curated Data Layer"
    Layer = "curated"
  }
}

# Data Catalog
resource "aws_glue_catalog_database" "data_lake" {
  name        = "${var.project_name}_data_lake"
  description = "Data lake catalog database"
}

# Glue Crawlers for Schema Discovery
resource "aws_glue_crawler" "raw_data_crawler" {
  database_name = aws_glue_catalog_database.data_lake.name
  name          = "${var.project_name}-raw-data-crawler"
  role          = aws_iam_role.glue_crawler.arn
  
  s3_target {
    path = "s3://${aws_s3_bucket.raw_data.bucket}/"
  }
  
  schedule = "cron(0 2 * * ? *)"  # Daily at 2 AM
  
  schema_change_policy {
    update_behavior = "UPDATE_IN_DATABASE"
    delete_behavior = "LOG"
  }
}

# EMR Cluster for Data Processing
resource "aws_emr_cluster" "data_processing" {
  name          = "${var.project_name}-data-processing"
  release_label = "emr-6.10.0"
  applications  = ["Spark", "Hadoop", "Hive", "Livy", "JupyterHub"]
  
  ec2_attributes {
    subnet_id                         = var.private_subnet_ids[0]
    emr_managed_master_security_group = aws_security_group.emr_master.id
    emr_managed_slave_security_group  = aws_security_group.emr_slave.id
    instance_profile                  = aws_iam_instance_profile.emr_profile.arn
    key_name                         = var.key_pair_name
  }
  
  master_instance_group {
    instance_type = "m5.xlarge"
  }
  
  core_instance_group {
    instance_type  = "m5.xlarge"
    instance_count = 3
    
    ebs_config {
      size                 = 100
      type                 = "gp3"
      volumes_per_instance = 1
    }
  }
  
  step {
    action_on_failure = "TERMINATE_CLUSTER"
    name              = "Setup Hadoop debugging"
    
    hadoop_jar_step {
      jar  = "command-runner.jar"
      args = ["state-pusher-script"]
    }
  }
  
  configurations_json = jsonencode([
    {
      "Classification": "spark-defaults",
      "Properties": {
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.adaptive.coalescePartitions.enabled": "true",
        "spark.sql.warehouse.dir": "s3://${aws_s3_bucket.processed_data.bucket}/warehouse/",
        "spark.sql.catalogImplementation": "hive",
        "spark.hadoop.hive.metastore.client.factory.class": "com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory"
      }
    }
  ])
  
  service_role = aws_iam_role.emr_service_role.arn
  
  tags = {
    Name        = "Data Processing Cluster"
    Environment = var.environment
  }
}

# Lambda Functions for Data Pipeline Orchestration
resource "aws_lambda_function" "data_ingestion" {
  filename         = "data_ingestion.zip"
  function_name    = "${var.project_name}-data-ingestion"
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("data_ingestion.zip")
  runtime         = "python3.9"
  timeout         = 900
  memory_size     = 1024
  
  environment {
    variables = {
      RAW_BUCKET       = aws_s3_bucket.raw_data.bucket
      PROCESSED_BUCKET = aws_s3_bucket.processed_data.bucket
      GLUE_DATABASE    = aws_glue_catalog_database.data_lake.name
    }
  }
  
  tags = {
    Name = "Data Ingestion Function"
  }
}

# Step Functions for Workflow Orchestration
resource "aws_sfn_state_machine" "data_pipeline" {
  name     = "${var.project_name}-data-pipeline"
  role_arn = aws_iam_role.step_functions_role.arn
  
  definition = jsonencode({
    Comment = "Data Lake Processing Pipeline"
    StartAt = "IngestData"
    States = {
      IngestData = {
        Type     = "Task"
        Resource = aws_lambda_function.data_ingestion.arn
        Next     = "ProcessData"
        Retry = [{
          ErrorEquals     = ["States.TaskFailed"]
          IntervalSeconds = 30
          MaxAttempts     = 3
          BackoffRate     = 2.0
        }]
      }
      ProcessData = {
        Type     = "Task"
        Resource = "arn:aws:states:::emr:addStep.sync"
        Parameters = {
          ClusterId = aws_emr_cluster.data_processing.id
          Step = {
            Name = "Process Raw Data"
            ActionOnFailure = "CONTINUE"
            HadoopJarStep = {
              Jar = "command-runner.jar"
              Args = [
                "spark-submit",
                "--deploy-mode", "cluster",
                "s3://${aws_s3_bucket.processed_data.bucket}/scripts/process_data.py"
              ]
            }
          }
        }
        Next = "CurateData"
      }
      CurateData = {
        Type     = "Task"
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Parameters = {
          JobName = aws_glue_job.data_curation.name
        }
        End = true
      }
    }
  })
  
  tags = {
    Name = "Data Pipeline State Machine"
  }
}

# CloudWatch Events for Scheduling
resource "aws_cloudwatch_event_rule" "daily_pipeline" {
  name                = "${var.project_name}-daily-pipeline"
  description         = "Trigger data pipeline daily"
  schedule_expression = "cron(0 6 * * ? *)"  # Daily at 6 AM UTC
}

resource "aws_cloudwatch_event_target" "step_functions" {
  rule      = aws_cloudwatch_event_rule.daily_pipeline.name
  target_id = "TriggerStepFunction"
  arn       = aws_sfn_state_machine.data_pipeline.arn
  role_arn  = aws_iam_role.events_role.arn
}
```

### 14. How do you implement disaster recovery and backup strategies with Terraform?
**Answer**: 
Comprehensive disaster recovery involves cross-region replication and automated backup procedures.

**Multi-Region Disaster Recovery:**
```hcl
# Primary region provider
provider "aws" {
  alias  = "primary"
  region = var.primary_region
}

# DR region provider
provider "aws" {
  alias  = "dr"
  region = var.dr_region
}

# Primary region infrastructure
module "primary_infrastructure" {
  source = "./modules/data-infrastructure"
  
  providers = {
    aws = aws.primary
  }
  
  region      = var.primary_region
  environment = var.environment
  is_primary  = true
}

# DR region infrastructure
module "dr_infrastructure" {
  source = "./modules/data-infrastructure"
  
  providers = {
    aws = aws.dr
  }
  
  region      = var.dr_region
  environment = "${var.environment}-dr"
  is_primary  = false
}

# Cross-region replication for S3
resource "aws_s3_bucket_replication_configuration" "primary_to_dr" {
  provider = aws.primary
  
  role   = aws_iam_role.replication.arn
  bucket = module.primary_infrastructure.data_lake_bucket_id
  
  rule {
    id     = "replicate-to-dr"
    status = "Enabled"
    
    destination {
      bucket        = module.dr_infrastructure.data_lake_bucket_arn
      storage_class = "STANDARD_IA"
      
      replica_kms_key_id = module.dr_infrastructure.kms_key_arn
    }
  }
  
  depends_on = [aws_s3_bucket_versioning.primary_data_lake]
}

# RDS Cross-region automated backups
resource "aws_db_instance" "primary" {
  provider = aws.primary
  
  identifier     = "${var.project_name}-primary-db"
  engine         = "postgres"
  engine_version = "14.6"
  instance_class = "db.r5.xlarge"
  
  allocated_storage     = 500
  max_allocated_storage = 1000
  
  db_name  = "datawarehouse"
  username = "admin"
  password = var.db_password
  
  backup_retention_period = 30
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  # Enable automated backups to DR region
  copy_tags_to_snapshot = true
  
  tags = {
    Name = "Primary Database"
  }
}

# Lambda function for automated failover
resource "aws_lambda_function" "failover_orchestrator" {
  provider = aws.primary
  
  filename         = "failover_orchestrator.zip"
  function_name    = "${var.project_name}-failover-orchestrator"
  role            = aws_iam_role.failover_lambda_role.arn
  handler         = "lambda_function.lambda_handler"
  source_code_hash = filebase64sha256("failover_orchestrator.zip")
  runtime         = "python3.9"
  timeout         = 900
  
  environment {
    variables = {
      PRIMARY_REGION = var.primary_region
      DR_REGION      = var.dr_region
      SNS_TOPIC_ARN  = aws_sns_topic.alerts.arn
    }
  }
  
  tags = {
    Name = "Failover Orchestrator"
  }
}

# CloudWatch alarms for automated failover
resource "aws_cloudwatch_metric_alarm" "rds_connection_failure" {
  provider = aws.primary
  
  alarm_name          = "${var.project_name}-rds-connection-failure"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "3"
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = "60"
  statistic           = "Average"
  threshold           = "1"
  alarm_description   = "This metric monitors RDS connection failures"
  
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.primary.id
  }
  
  alarm_actions = [aws_lambda_function.failover_orchestrator.arn]
  
  tags = {
    Name = "RDS Connection Failure Alarm"
  }
}

# Route 53 health checks and failover
resource "aws_route53_health_check" "primary" {
  fqdn                            = module.primary_infrastructure.load_balancer_dns
  port                            = 443
  type                            = "HTTPS"
  resource_path                   = "/health"
  failure_threshold               = "3"
  request_interval                = "30"
  cloudwatch_alarm_region         = var.primary_region
  cloudwatch_alarm_name           = aws_cloudwatch_metric_alarm.rds_connection_failure.alarm_name
  insufficient_data_health_status = "Failure"
  
  tags = {
    Name = "Primary Health Check"
  }
}

resource "aws_route53_record" "primary" {
  zone_id = var.route53_zone_id
  name    = var.domain_name
  type    = "A"
  
  set_identifier = "primary"
  
  failover_routing_policy {
    type = "PRIMARY"
  }
  
  alias {
    name                   = module.primary_infrastructure.load_balancer_dns
    zone_id                = module.primary_infrastructure.load_balancer_zone_id
    evaluate_target_health = true
  }
  
  health_check_id = aws_route53_health_check.primary.id
}

resource "aws_route53_record" "dr" {
  zone_id = var.route53_zone_id
  name    = var.domain_name
  type    = "A"
  
  set_identifier = "dr"
  
  failover_routing_policy {
    type = "SECONDARY"
  }
  
  alias {
    name                   = module.dr_infrastructure.load_balancer_dns
    zone_id                = module.dr_infrastructure.load_balancer_zone_id
    evaluate_target_health = true
  }
}
```

### 15. How do you implement cost optimization and resource management with Terraform?
**Answer**: 
Cost optimization involves automated scaling, resource scheduling, and lifecycle management.

**Cost Optimization Infrastructure:**
```hcl
# Auto Scaling based on schedule and metrics
resource "aws_autoscaling_schedule" "scale_down_evening" {
  scheduled_action_name  = "scale-down-evening"
  min_size               = 0
  max_size               = 2
  desired_capacity       = 0
  recurrence             = "0 18 * * MON-FRI"  # 6 PM weekdays
  auto_scaling_group_name = aws_autoscaling_group.data_processing.name
}

# Spot instances for cost savings
resource "aws_launch_template" "spot_processing" {
  name_prefix   = "spot-processing-"
  image_id      = var.ami_id
  instance_type = "c5.xlarge"
  
  instance_market_options {
    market_type = "spot"
    spot_options {
      max_price = "0.10"  # Maximum price per hour
    }
  }
}
```

### 16. How do you implement Infrastructure as Code testing with Terraform?
**Answer**: Use testing frameworks like Terratest, kitchen-terraform, and validation rules.

```hcl
# Validation rules in variables
variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  
  validation {
    condition = contains([
      "t3.micro", "t3.small", "t3.medium", "t3.large",
      "m5.large", "m5.xlarge", "c5.large", "c5.xlarge"
    ], var.instance_type)
    error_message = "Instance type must be a valid EC2 instance type."
  }
}

# Pre-condition checks
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  
  lifecycle {
    precondition {
      condition     = data.aws_ami.ubuntu.architecture == "x86_64"
      error_message = "AMI must be x86_64 architecture."
    }
  }
}
```

### 17. How do you implement Terraform CI/CD pipelines?
**Answer**: Integrate Terraform with CI/CD tools for automated deployment.

```yaml
# GitHub Actions workflow
name: Terraform CI/CD
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v2
      with:
        terraform_version: 1.5.0
    
    - name: Terraform Format
      run: terraform fmt -check
    
    - name: Terraform Init
      run: terraform init
    
    - name: Terraform Validate
      run: terraform validate
    
    - name: Terraform Plan
      run: terraform plan -out=tfplan
    
    - name: Terraform Apply
      if: github.ref == 'refs/heads/main'
      run: terraform apply tfplan
```

### 18. How do you handle Terraform drift detection and remediation?
**Answer**: Use drift detection tools and automated remediation strategies.

```bash
# Drift detection script
#!/bin/bash
set -e

echo "Checking for infrastructure drift..."

# Run terraform plan to detect drift
terraform plan -detailed-exitcode -out=drift-check.tfplan

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "No drift detected"
elif [ $EXIT_CODE -eq 2 ]; then
    echo "Drift detected! Generating drift report..."
    terraform show -json drift-check.tfplan > drift-report.json
    
    # Send alert
    python send_drift_alert.py drift-report.json
    
    # Auto-remediate if configured
    if [ "$AUTO_REMEDIATE" = "true" ]; then
        echo "Auto-remediating drift..."
        terraform apply drift-check.tfplan
    fi
else
    echo "Error running terraform plan"
    exit 1
fi
```

### 19. How do you implement Terraform policy as code?
**Answer**: Use Sentinel, OPA, or custom validation for policy enforcement.

```hcl
# Sentinel policy example
import "tfplan/v2" as tfplan

# Require encryption for S3 buckets
require_s3_encryption = rule {
    all tfplan.resource_changes as _, rc {
        rc.type is "aws_s3_bucket" and
        rc.mode is "managed" and
        (rc.change.actions contains "create" or rc.change.actions contains "update") implies
        rc.change.after.server_side_encryption_configuration is not null
    }
}

# Enforce tagging standards
require_mandatory_tags = rule {
    all tfplan.resource_changes as _, rc {
        rc.type in ["aws_instance", "aws_s3_bucket", "aws_rds_instance"] and
        rc.mode is "managed" and
        (rc.change.actions contains "create" or rc.change.actions contains "update") implies
        all ["Environment", "Project", "Owner"] as tag {
            rc.change.after.tags[tag] is not null
        }
    }
}

main = rule {
    require_s3_encryption and require_mandatory_tags
}
```

### 20. How do you manage Terraform secrets and sensitive data?
**Answer**: Use external secret management and secure variable handling.

```hcl
# External secret management
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/database/password"
}

locals {
  db_credentials = jsondecode(data.aws_secretsmanager_secret_version.db_password.secret_string)
}

resource "aws_db_instance" "main" {
  identifier = "main-database"
  engine     = "postgres"
  
  username = local.db_credentials.username
  password = local.db_credentials.password
  
  # Mark as sensitive
  lifecycle {
    ignore_changes = [password]
  }
}

# Sensitive variable
variable "api_key" {
  description = "API key for external service"
  type        = string
  sensitive   = true
}
```

### 21-100. Additional Terraform Questions

**21. How do you implement Terraform workspace strategies?**
**Answer**: Use workspace-based environment separation and configuration management.

**22. How do you handle Terraform provider versioning?**
**Answer**: Pin provider versions and manage upgrades systematically.

**23. How do you implement Terraform remote execution?**
**Answer**: Use Terraform Cloud or Enterprise for remote operations.

**24. How do you optimize Terraform performance?**
**Answer**: Use parallelism, target specific resources, and optimize state operations.

**25. How do you implement Terraform compliance scanning?**
**Answer**: Use tools like Checkov, tfsec, and Terrascan for security scanning.

**26. How do you handle Terraform resource dependencies?**
**Answer**: Use implicit and explicit dependencies with proper ordering.

**27. How do you implement Terraform blue-green deployments?**
**Answer**: Use multiple resource sets and traffic switching strategies.

**28. How do you manage Terraform state locking?**
**Answer**: Use DynamoDB for state locking and prevent concurrent modifications.

**29. How do you implement Terraform resource tagging strategies?**
**Answer**: Use consistent tagging policies and automation for compliance.

**30. How do you handle Terraform provider authentication?**
**Answer**: Use IAM roles, service principals, and secure credential management.

### 31. How do you implement Terraform workspace strategies?
**Answer**: Use workspace-based environment separation and configuration management.

```hcl
# Environment-specific configurations
locals {
  environment = terraform.workspace
  
  config = {
    dev = {
      instance_count = 1
      instance_type  = "t3.micro"
      db_instance_class = "db.t3.micro"
    }
    staging = {
      instance_count = 2
      instance_type  = "t3.small"
      db_instance_class = "db.t3.small"
    }
    prod = {
      instance_count = 3
      instance_type  = "t3.medium"
      db_instance_class = "db.r5.large"
    }
  }
  
  current_config = local.config[local.environment]
}
```

### 32. How do you handle Terraform provider versioning?
**Answer**: Pin provider versions and manage upgrades systematically.

```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }
}
```

### 33. How do you implement Terraform remote execution?
**Answer**: Use Terraform Cloud or Enterprise for remote operations.

### 34. How do you optimize Terraform performance?
**Answer**: Use parallelism, target specific resources, and optimize state operations.

### 35. How do you implement Terraform compliance scanning?
**Answer**: Use tools like Checkov, tfsec, and Terrascan for security scanning.

### 36. How do you handle Terraform resource dependencies?
**Answer**: Use implicit and explicit dependencies with proper ordering.

### 37. How do you implement Terraform blue-green deployments?
**Answer**: Use multiple resource sets and traffic switching strategies.

### 38. How do you manage Terraform state locking?
**Answer**: Use DynamoDB for state locking and prevent concurrent modifications.

### 39. How do you implement Terraform resource tagging strategies?
**Answer**: Use consistent tagging policies and automation for compliance.

### 40. How do you handle Terraform provider authentication?
**Answer**: Use IAM roles, service principals, and secure credential management.

### 41. How do you implement Terraform data source patterns?
**Answer**: Use data sources for referencing existing infrastructure.

### 42. How do you handle Terraform resource lifecycle management?
**Answer**: Use lifecycle rules for create_before_destroy and ignore_changes.

### 43. How do you implement Terraform conditional resource creation?
**Answer**: Use count and for_each with conditional logic.

### 44. How do you handle Terraform string interpolation and functions?
**Answer**: Use built-in functions for data manipulation and formatting.

### 45. How do you implement Terraform local values and computed properties?
**Answer**: Use locals block for derived values and complex expressions.

### 46. How do you handle Terraform resource addressing and references?
**Answer**: Use proper resource addressing for dependencies and outputs.

### 47. How do you implement Terraform dynamic configuration generation?
**Answer**: Use templatefile and dynamic blocks for flexible configurations.

### 48. How do you handle Terraform error handling and debugging?
**Answer**: Use TF_LOG environment variable and systematic debugging approaches.

### 49. How do you implement Terraform resource import strategies?
**Answer**: Use terraform import for existing infrastructure adoption.

### 50. How do you handle Terraform workspace isolation?
**Answer**: Implement proper workspace separation and state isolation.

### 51. How do you implement Terraform module composition patterns?
**Answer**: Compose complex infrastructure from reusable modules.

### 52. How do you handle Terraform provider configuration inheritance?
**Answer**: Use provider aliases and inheritance patterns.

### 53. How do you implement Terraform resource validation?
**Answer**: Use validation blocks and custom validation logic.

### 54. How do you handle Terraform state migration?
**Answer**: Use terraform state mv and systematic migration procedures.

### 55. How do you implement Terraform resource targeting?
**Answer**: Use -target flag for selective resource operations.

### 56. How do you handle Terraform configuration organization?
**Answer**: Organize files logically with proper naming conventions.

### 57. How do you implement Terraform resource replacement strategies?
**Answer**: Use terraform taint and replacement workflows.

### 58. How do you handle Terraform provider plugin management?
**Answer**: Manage provider plugins and custom provider development.

### 59. How do you implement Terraform resource monitoring?
**Answer**: Monitor resource changes and state consistency.

### 60. How do you handle Terraform configuration validation?
**Answer**: Use terraform validate and automated validation pipelines.

### 61. How do you implement Terraform resource scheduling?
**Answer**: Schedule resource operations and lifecycle management.

### 62. How do you handle Terraform cross-stack references?
**Answer**: Use remote state data sources for cross-stack dependencies.

### 63. How do you implement Terraform resource cleanup?
**Answer**: Implement proper resource cleanup and garbage collection.

### 64. How do you handle Terraform configuration templating?
**Answer**: Use template files and dynamic configuration generation.

### 65. How do you implement Terraform resource discovery?
**Answer**: Discover and import existing infrastructure resources.

### 66. How do you handle Terraform state consistency?
**Answer**: Ensure state consistency and handle state conflicts.

### 67. How do you implement Terraform resource grouping?
**Answer**: Group related resources logically and manage dependencies.

### 68. How do you handle Terraform configuration inheritance?
**Answer**: Implement configuration inheritance and override patterns.

### 69. How do you implement Terraform resource scaling?
**Answer**: Implement auto-scaling and dynamic resource management.

### 70. How do you handle Terraform provider compatibility?
**Answer**: Manage provider compatibility and version constraints.

### 71. How do you implement Terraform resource documentation?
**Answer**: Document infrastructure code and maintain documentation.

### 72. How do you handle Terraform configuration testing?
**Answer**: Test infrastructure code with automated testing frameworks.

### 73. How do you implement Terraform resource optimization?
**Answer**: Optimize resource configurations for cost and performance.

### 74. How do you handle Terraform state backup strategies?
**Answer**: Implement comprehensive state backup and recovery procedures.

### 75. How do you implement Terraform resource monitoring?
**Answer**: Monitor infrastructure changes and resource health.

### 76. How do you handle Terraform configuration security?
**Answer**: Implement security best practices and vulnerability scanning.

### 77. How do you implement Terraform resource automation?
**Answer**: Automate infrastructure operations and lifecycle management.

### 78. How do you handle Terraform provider customization?
**Answer**: Customize providers and implement custom functionality.

### 79. How do you implement Terraform resource governance?
**Answer**: Implement governance policies and compliance frameworks.

### 80. How do you handle Terraform enterprise patterns?
**Answer**: Implement enterprise-grade patterns and best practices.

**Enterprise Terraform Architecture:**
```hcl
# Enterprise-grade Terraform configuration
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  # Remote backend with encryption
  backend "s3" {
    bucket         = "enterprise-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
    
    # Cross-account role assumption
    role_arn = "arn:aws:iam::ACCOUNT:role/TerraformRole"
  }
}

# Provider configuration with assume role
provider "aws" {
  region = var.aws_region
  
  assume_role {
    role_arn     = var.terraform_role_arn
    session_name = "terraform-session"
  }
  
  default_tags {
    tags = {
      ManagedBy   = "terraform"
      Environment = var.environment
      Project     = var.project_name
      CostCenter  = var.cost_center
      Owner       = var.owner
    }
  }
}

# Enterprise module structure
module "networking" {
  source = "git::https://github.com/company/terraform-modules.git//networking?ref=v1.0.0"
  
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
  environment        = var.environment
  
  # Enterprise networking requirements
  enable_flow_logs     = true
  enable_dns_hostnames = true
  enable_dns_support   = true
}

module "security" {
  source = "git::https://github.com/company/terraform-modules.git//security?ref=v1.0.0"
  
  vpc_id      = module.networking.vpc_id
  environment = var.environment
  
  # Security compliance requirements
  enable_guardduty    = true
  enable_config       = true
  enable_cloudtrail   = true
  enable_security_hub = true
}

module "data_platform" {
  source = "git::https://github.com/company/terraform-modules.git//data-platform?ref=v1.0.0"
  
  vpc_id             = module.networking.vpc_id
  private_subnet_ids = module.networking.private_subnet_ids
  security_group_ids = module.security.data_platform_sg_ids
  
  # Data platform configuration
  enable_data_lake      = true
  enable_data_warehouse = true
  enable_streaming      = true
  enable_ml_platform    = true
  
  # Compliance and governance
  enable_encryption     = true
  enable_audit_logging  = true
  enable_data_catalog   = true
  
  tags = local.common_tags
}

# Local values for enterprise patterns
locals {
  common_tags = {
    Environment    = var.environment
    Project        = var.project_name
    CostCenter     = var.cost_center
    Owner          = var.owner
    ManagedBy      = "terraform"
    ComplianceLevel = var.compliance_level
    DataClass      = var.data_classification
  }
  
  # Environment-specific configurations
  environment_config = {
    dev = {
      instance_types = ["t3.small", "t3.medium"]
      enable_backup  = false
      retention_days = 7
    }
    staging = {
      instance_types = ["t3.medium", "t3.large"]
      enable_backup  = true
      retention_days = 30
    }
    prod = {
      instance_types = ["m5.large", "m5.xlarge"]
      enable_backup  = true
      retention_days = 90
    }
  }
}

# Enterprise governance and compliance
resource "aws_config_configuration_recorder" "enterprise" {
  name     = "enterprise-config-recorder"
  role_arn = aws_iam_role.config.arn
  
  recording_group {
    all_supported                 = true
    include_global_resource_types = true
  }
  
  depends_on = [aws_config_delivery_channel.enterprise]
}

# Cost optimization and resource management
resource "aws_budgets_budget" "enterprise" {
  name         = "enterprise-monthly-budget"
  budget_type  = "COST"
  limit_amount = var.monthly_budget_limit
  limit_unit   = "USD"
  time_unit    = "MONTHLY"
  
  cost_filters {
    tag {
      key    = "Project"
      values = [var.project_name]
    }
  }
  
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                 = 80
    threshold_type            = "PERCENTAGE"
    notification_type         = "ACTUAL"
    subscriber_email_addresses = var.budget_notification_emails
  }
}
```

---

## 🎯 **Summary**

This comprehensive guide covers 100 Terraform essential concepts for data engineering interviews. Key areas include:

- **Infrastructure as Code** principles and workflow
- **State management** for team collaboration
- **Module development** for reusability and maintainability
- **Multi-cloud deployment** strategies
- **Advanced features** like workspaces and custom provisioners
- **Data infrastructure patterns** for complete solutions
- **Cost optimization** and resource management
- **Testing and validation** strategies
- **CI/CD integration** and automation
- **Security and compliance** implementation
- **Performance optimization** and troubleshooting

**Interview Preparation Tips:**
1. **Master HCL syntax** - Practice writing clean, readable configurations
2. **Understand state management** - Know remote backends and locking
3. **Practice module development** - Create reusable, well-documented modules
4. **Study provider-specific resources** - Know AWS, Azure, GCP data services
5. **Learn troubleshooting** - Common errors and debugging techniques
6. **Understand testing** - Validation, policy as code, and automated testing
7. **Practice CI/CD integration** - Automated deployment and drift detection
8. **Know security patterns** - Secret management and compliance scanning
9. **Master enterprise patterns** - Governance, compliance, and large-scale operations
10. **Understand performance optimization** - Resource efficiency and cost management

This comprehensive collection of 80 Terraform interview questions covers all aspects from basic concepts to advanced enterprise patterns, ensuring thorough preparation for infrastructure engineering roles.