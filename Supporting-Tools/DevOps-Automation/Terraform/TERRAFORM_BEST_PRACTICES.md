# Terraform Best Practices for Data Engineering

## Project Structure

### Directory Organization
```
terraform/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
├── modules/
│   ├── s3-bucket/
│   ├── glue-job/
│   └── redshift-cluster/
├── shared/
│   ├── variables.tf
│   └── outputs.tf
└── main.tf
```

### Module Design
```hcl
# modules/s3-bucket/main.tf
resource "aws_s3_bucket" "data_bucket" {
  bucket = var.bucket_name
  
  tags = merge(var.common_tags, {
    Name = var.bucket_name
    Type = "DataLake"
  })
}

resource "aws_s3_bucket_versioning" "data_bucket_versioning" {
  bucket = aws_s3_bucket.data_bucket.id
  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Disabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "data_bucket_encryption" {
  bucket = aws_s3_bucket.data_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
```

## State Management

### Remote State Configuration
```hcl
# backend.tf
terraform {
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "data-platform/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

# Create state bucket and lock table
resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-bucket"
  
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name           = "terraform-locks"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

### Workspace Management
```bash
# Create and manage workspaces
terraform workspace new dev
terraform workspace new staging
terraform workspace new prod

# Switch between workspaces
terraform workspace select prod
terraform plan -var-file="environments/prod/terraform.tfvars"
```

## Data Infrastructure Modules

### Glue Job Module
```hcl
# modules/glue-job/main.tf
resource "aws_glue_job" "etl_job" {
  name         = var.job_name
  role_arn     = aws_iam_role.glue_role.arn
  glue_version = "3.0"

  command {
    script_location = "s3://${var.scripts_bucket}/${var.script_path}"
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"                     = "python"
    "--job-bookmark-option"              = "job-bookmark-enable"
    "--enable-metrics"                   = ""
    "--enable-continuous-cloudwatch-log" = "true"
    "--TempDir"                         = "s3://${var.temp_bucket}/temp/"
  }

  execution_property {
    max_concurrent_runs = var.max_concurrent_runs
  }

  worker_type       = var.worker_type
  number_of_workers = var.number_of_workers
}

# IAM role for Glue job
resource "aws_iam_role" "glue_role" {
  name = "${var.job_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}
```

### Redshift Cluster Module
```hcl
# modules/redshift-cluster/main.tf
resource "aws_redshift_cluster" "data_warehouse" {
  cluster_identifier      = var.cluster_identifier
  database_name          = var.database_name
  master_username        = var.master_username
  master_password        = var.master_password
  node_type              = var.node_type
  cluster_type           = var.cluster_type
  number_of_nodes        = var.number_of_nodes
  
  vpc_security_group_ids = [aws_security_group.redshift_sg.id]
  db_subnet_group_name   = aws_redshift_subnet_group.redshift_subnet_group.name
  
  skip_final_snapshot = var.skip_final_snapshot
  encrypted          = true
  
  tags = var.common_tags
}

resource "aws_redshift_subnet_group" "redshift_subnet_group" {
  name       = "${var.cluster_identifier}-subnet-group"
  subnet_ids = var.subnet_ids
  
  tags = var.common_tags
}
```

## Environment Configuration

### Variable Management
```hcl
# environments/prod/terraform.tfvars
environment = "prod"
region      = "us-east-1"

# S3 Configuration
data_lake_bucket = "company-data-lake-prod"
enable_versioning = true

# Redshift Configuration
redshift_cluster_identifier = "data-warehouse-prod"
redshift_node_type         = "dc2.large"
redshift_number_of_nodes   = 3

# Glue Configuration
glue_jobs = {
  "customer-etl" = {
    script_path = "scripts/customer_etl.py"
    worker_type = "G.1X"
    number_of_workers = 10
  }
  "sales-etl" = {
    script_path = "scripts/sales_etl.py"
    worker_type = "G.2X"
    number_of_workers = 5
  }
}

common_tags = {
  Environment = "prod"
  Project     = "DataPlatform"
  Owner       = "DataTeam"
}
```

### Conditional Resources
```hcl
# Create resources based on environment
resource "aws_redshift_cluster" "data_warehouse" {
  count = var.environment == "prod" ? 1 : 0
  
  cluster_identifier = var.cluster_identifier
  node_type         = var.environment == "prod" ? "dc2.large" : "dc2.small"
  number_of_nodes   = var.environment == "prod" ? 3 : 1
}

# Use locals for complex logic
locals {
  is_production = var.environment == "prod"
  
  redshift_config = {
    node_type = local.is_production ? "dc2.large" : "dc2.small"
    node_count = local.is_production ? 3 : 1
    backup_retention = local.is_production ? 7 : 1
  }
}
```

## Security Best Practices

### Resource Policies
```hcl
# S3 bucket policy
data "aws_iam_policy_document" "s3_policy" {
  statement {
    sid    = "DenyInsecureConnections"
    effect = "Deny"
    
    principals {
      type        = "*"
      identifiers = ["*"]
    }
    
    actions = ["s3:*"]
    
    resources = [
      aws_s3_bucket.data_bucket.arn,
      "${aws_s3_bucket.data_bucket.arn}/*"
    ]
    
    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "data_bucket_policy" {
  bucket = aws_s3_bucket.data_bucket.id
  policy = data.aws_iam_policy_document.s3_policy.json
}
```

### Secrets Management
```hcl
# Store sensitive data in AWS Secrets Manager
resource "aws_secretsmanager_secret" "db_password" {
  name = "${var.environment}-redshift-password"
  
  tags = var.common_tags
}

resource "aws_secretsmanager_secret_version" "db_password" {
  secret_id     = aws_secretsmanager_secret.db_password.id
  secret_string = var.master_password
}

# Reference secret in Redshift cluster
resource "aws_redshift_cluster" "data_warehouse" {
  manage_master_password = true
  master_password_secret_kms_key_id = aws_kms_key.redshift_key.arn
}
```

## Monitoring and Observability

### CloudWatch Integration
```hcl
# CloudWatch log group for Glue jobs
resource "aws_cloudwatch_log_group" "glue_logs" {
  name              = "/aws-glue/jobs/${var.job_name}"
  retention_in_days = var.log_retention_days
  
  tags = var.common_tags
}

# CloudWatch alarms
resource "aws_cloudwatch_metric_alarm" "glue_job_failure" {
  alarm_name          = "${var.job_name}-failure"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "glue.driver.aggregate.numFailedTasks"
  namespace           = "Glue"
  period              = "300"
  statistic           = "Sum"
  threshold           = "0"
  alarm_description   = "This metric monitors glue job failures"
  
  dimensions = {
    JobName = aws_glue_job.etl_job.name
  }
  
  alarm_actions = [aws_sns_topic.alerts.arn]
}
```