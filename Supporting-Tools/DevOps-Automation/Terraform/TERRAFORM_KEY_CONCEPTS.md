# Terraform Key Concepts

## 1. Infrastructure as Code (IaC)
**What is Terraform**: An open-source tool for building, changing, and versioning infrastructure safely and efficiently using declarative configuration files.

**Core Principles**:
- **Declarative**: Describe desired end state, not steps
- **Idempotent**: Same configuration produces same result
- **Plan before Apply**: Preview changes before execution
- **State Management**: Track infrastructure state
- **Provider Agnostic**: Works with multiple cloud providers

**Terraform Workflow**:
```bash
terraform init      # Initialize working directory
terraform plan      # Create execution plan
terraform apply     # Execute the plan
terraform destroy   # Destroy infrastructure
```

## 2. Configuration Language (HCL)
**HashiCorp Configuration Language**: Human-readable configuration syntax.

**Basic Syntax**:
```hcl
# Resource block
resource "aws_instance" "web_server" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t3.micro"
  
  tags = {
    Name        = "WebServer"
    Environment = "Production"
  }
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

# Variable
variable "instance_count" {
  description = "Number of instances to create"
  type        = number
  default     = 2
}

# Output
output "instance_ip" {
  description = "Public IP of the instance"
  value       = aws_instance.web_server.public_ip
}
```

**Complex Data Types**:
```hcl
# List
variable "availability_zones" {
  type    = list(string)
  default = ["us-west-2a", "us-west-2b", "us-west-2c"]
}

# Map
variable "instance_types" {
  type = map(string)
  default = {
    dev  = "t3.micro"
    prod = "t3.large"
  }
}

# Object
variable "database_config" {
  type = object({
    engine         = string
    engine_version = string
    instance_class = string
    allocated_storage = number
  })
  default = {
    engine         = "mysql"
    engine_version = "8.0"
    instance_class = "db.t3.micro"
    allocated_storage = 20
  }
}
```

## 3. Providers
**What they are**: Plugins that interact with APIs of cloud providers and other services.

**Provider Configuration**:
```hcl
# AWS Provider
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.0"
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "DataPlatform"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

# Multiple provider instances
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

provider "aws" {
  alias  = "us_west_2"
  region = "us-west-2"
}
```

**Multi-Cloud Example**:
```hcl
# AWS resources
resource "aws_s3_bucket" "data_lake" {
  bucket = "my-data-lake-${random_id.bucket_suffix.hex}"
}

# Azure resources
resource "azurerm_storage_account" "backup" {
  name                     = "backupstorage${random_id.storage_suffix.hex}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Google Cloud resources
resource "google_storage_bucket" "archive" {
  name     = "archive-bucket-${random_id.bucket_suffix.hex}"
  location = "US"
}
```

## 4. Resources and Data Sources
**Resources**: Infrastructure objects managed by Terraform.

```hcl
# VPC Resource
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "main-vpc"
  }
}

# Subnet Resource
resource "aws_subnet" "public" {
  count = length(var.availability_zones)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "public-subnet-${count.index + 1}"
    Type = "Public"
  }
}
```

**Data Sources**: Query existing infrastructure.

```hcl
# Query existing VPC
data "aws_vpc" "existing" {
  filter {
    name   = "tag:Name"
    values = ["existing-vpc"]
  }
}

# Query AMI
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Use data source in resource
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  subnet_id     = data.aws_vpc.existing.id
}
```

## 5. Variables and Outputs
**Input Variables**:
```hcl
# variables.tf
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "database_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "instance_config" {
  description = "Instance configuration"
  type = object({
    instance_type = string
    key_name      = string
    monitoring    = bool
  })
  default = {
    instance_type = "t3.micro"
    key_name      = "default-key"
    monitoring    = false
  }
}
```

**Variable Files**:
```hcl
# terraform.tfvars
environment = "production"
instance_config = {
  instance_type = "t3.large"
  key_name      = "prod-key"
  monitoring    = true
}

# dev.tfvars
environment = "dev"
instance_config = {
  instance_type = "t3.micro"
  key_name      = "dev-key"
  monitoring    = false
}
```

**Outputs**:
```hcl
# outputs.tf
output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "database_endpoint" {
  description = "Database endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "instance_details" {
  description = "Instance details"
  value = {
    id         = aws_instance.web.id
    public_ip  = aws_instance.web.public_ip
    private_ip = aws_instance.web.private_ip
  }
}
```

## 6. State Management
**Terraform State**: JSON file tracking infrastructure state.

**Local State**:
```hcl
# terraform.tfstate (automatically created)
{
  "version": 4,
  "terraform_version": "1.6.0",
  "serial": 1,
  "lineage": "abc123",
  "outputs": {},
  "resources": [
    {
      "mode": "managed",
      "type": "aws_instance",
      "name": "web",
      "provider": "provider[\"registry.terraform.io/hashicorp/aws\"]",
      "instances": [...]
    }
  ]
}
```

**Remote State**:
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

# Alternative: Azure backend
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "terraformstatestorage"
    container_name       = "tfstate"
    key                  = "infrastructure.tfstate"
  }
}
```

**State Commands**:
```bash
# View state
terraform state list
terraform state show aws_instance.web

# Move resources in state
terraform state mv aws_instance.old aws_instance.new

# Remove from state (without destroying)
terraform state rm aws_instance.web

# Import existing resource
terraform import aws_instance.web i-1234567890abcdef0

# Refresh state
terraform refresh
```

## 7. Modules
**What they are**: Reusable Terraform configurations.

**Module Structure**:
```
modules/
└── vpc/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

**Module Definition** (`modules/vpc/main.tf`):
```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.cidr_block
  enable_dns_hostnames = var.enable_dns_hostnames
  enable_dns_support   = var.enable_dns_support
  
  tags = merge(var.tags, {
    Name = var.name
  })
}

resource "aws_subnet" "public" {
  count = length(var.public_subnets)
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnets[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  
  tags = merge(var.tags, {
    Name = "${var.name}-public-${count.index + 1}"
    Type = "Public"
  })
}
```

**Module Variables** (`modules/vpc/variables.tf`):
```hcl
variable "name" {
  description = "Name prefix for resources"
  type        = string
}

variable "cidr_block" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  description = "List of public subnet CIDR blocks"
  type        = list(string)
  default     = []
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}
```

**Using Modules**:
```hcl
# main.tf
module "vpc" {
  source = "./modules/vpc"
  
  name               = "production-vpc"
  cidr_block         = "10.0.0.0/16"
  availability_zones = ["us-west-2a", "us-west-2b", "us-west-2c"]
  public_subnets     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  
  tags = {
    Environment = "production"
    Project     = "data-platform"
  }
}

# Reference module outputs
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  subnet_id     = module.vpc.public_subnet_ids[0]
}
```

## 8. Functions and Expressions
**Built-in Functions**:
```hcl
locals {
  # String functions
  environment_upper = upper(var.environment)
  bucket_name       = lower("MyBucket-${random_id.suffix.hex}")
  
  # Collection functions
  subnet_count      = length(var.availability_zones)
  first_az          = element(var.availability_zones, 0)
  unique_tags       = distinct(var.tag_list)
  
  # Date/time functions
  current_time      = timestamp()
  formatted_date    = formatdate("YYYY-MM-DD", timestamp())
  
  # Encoding functions
  user_data_base64  = base64encode(file("${path.module}/user-data.sh"))
  
  # File functions
  ssh_key           = file("~/.ssh/id_rsa.pub")
  template_content  = templatefile("${path.module}/config.tpl", {
    database_url = aws_db_instance.main.endpoint
    api_key      = var.api_key
  })
}
```

**Conditional Expressions**:
```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"
  
  # Conditional resource creation
  count = var.create_instance ? 1 : 0
  
  tags = {
    Name = var.environment == "prod" ? "production-server" : "dev-server"
  }
}

# Conditional blocks
dynamic "ingress" {
  for_each = var.enable_ssh ? [1] : []
  content {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

## 9. Advanced Features
**For Expressions**:
```hcl
locals {
  # Transform list
  instance_names = [for i in range(var.instance_count) : "web-${i + 1}"]
  
  # Transform map
  instance_configs = {
    for k, v in var.environments : k => {
      instance_type = v.instance_type
      ami_id        = data.aws_ami.amazon_linux.id
    }
  }
  
  # Filter and transform
  production_instances = [
    for instance in aws_instance.web : instance.id
    if instance.tags.Environment == "production"
  ]
}
```

**Dynamic Blocks**:
```hcl
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
    }
  }
}
```

**Lifecycle Rules**:
```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type
  
  lifecycle {
    create_before_destroy = true    # Create new before destroying old
    prevent_destroy       = true    # Prevent accidental destruction
    ignore_changes       = [ami]    # Ignore changes to AMI
  }
}
```

## 10. Best Practices and Patterns
**Project Structure**:
```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   └── prod/
├── modules/
│   ├── vpc/
│   ├── database/
│   └── compute/
├── shared/
│   ├── data-sources.tf
│   └── providers.tf
└── scripts/
    ├── deploy.sh
    └── destroy.sh
```

**Data Engineering Infrastructure**:
```hcl
# Data Lake S3 Buckets
module "data_lake" {
  source = "./modules/s3-data-lake"
  
  environment = var.environment
  buckets = {
    raw        = "raw-data"
    processed  = "processed-data"
    curated    = "curated-data"
  }
  
  lifecycle_rules = {
    raw = {
      transition_to_ia_days      = 30
      transition_to_glacier_days = 90
      expiration_days           = 2555  # 7 years
    }
  }
}

# EMR Cluster for Spark Processing
module "emr_cluster" {
  source = "./modules/emr"
  
  cluster_name     = "${var.environment}-data-processing"
  release_label    = "emr-6.15.0"
  applications     = ["Spark", "Hadoop", "Hive"]
  instance_groups = {
    master = {
      instance_type  = "m5.xlarge"
      instance_count = 1
    }
    core = {
      instance_type  = "m5.2xlarge"
      instance_count = 2
    }
  }
  
  subnet_id = module.vpc.private_subnet_ids[0]
}

# Redshift Data Warehouse
module "redshift" {
  source = "./modules/redshift"
  
  cluster_identifier = "${var.environment}-dw"
  node_type         = var.environment == "prod" ? "dc2.large" : "dc2.small"
  number_of_nodes   = var.environment == "prod" ? 3 : 1
  
  subnet_group_name = aws_redshift_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.redshift.id]
}
```

**Security Best Practices**:
```hcl
# Secure S3 bucket
resource "aws_s3_bucket" "secure_data" {
  bucket = "secure-data-${random_id.suffix.hex}"
}

resource "aws_s3_bucket_encryption" "secure_data" {
  bucket = aws_s3_bucket.secure_data.id
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm     = "aws:kms"
        kms_master_key_id = aws_kms_key.s3.arn
      }
    }
  }
}

resource "aws_s3_bucket_public_access_block" "secure_data" {
  bucket = aws_s3_bucket.secure_data.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```