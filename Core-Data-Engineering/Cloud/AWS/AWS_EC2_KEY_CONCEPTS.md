# AWS EC2 Key Concepts

## 🎯 **Overview**
Amazon Elastic Compute Cloud (EC2) provides scalable virtual servers in the cloud, serving as the foundation for data processing, analytics workloads, and custom applications in data engineering pipelines.

**What You'll Learn:**
- EC2 instance types and selection criteria for data workloads
- Storage options and performance optimization
- Networking and security configurations
- Auto scaling and load balancing strategies
- Cost optimization techniques
- Monitoring and troubleshooting approaches

**Target Audience:**
- Data Engineers managing compute infrastructure
- DevOps Engineers supporting data platforms
- Solution Architects designing scalable systems
- Data Scientists requiring custom compute environments

## 1. Virtual Computing in the Cloud
**What it is**: Scalable virtual servers in AWS cloud providing compute capacity.

**Core Benefits**:
- **Elasticity**: Scale up/down based on demand
- **Pay-as-you-go**: Only pay for what you use
- **Global**: Available in multiple regions worldwide
- **Secure**: Built-in security features and compliance

## 2. Instance Types & Families
**Choosing the right instance type for data engineering workloads**

### General Purpose Instances
**Balanced compute, memory, and networking for versatile workloads**

**T3/T4g Family (Burstable Performance)**:
- **Use Cases**: Development environments, small databases, web servers
- **Data Engineering Fit**: ETL development, testing pipelines, small-scale processing
- **Performance**: Baseline CPU with burst capability
- **Cost**: Most cost-effective for variable workloads
```bash
# T3 instances with burst credits
t3.nano    # 2 vCPU, 0.5 GB RAM - Development/testing
t3.micro   # 2 vCPU, 1 GB RAM - Small scripts, monitoring
t3.small   # 2 vCPU, 2 GB RAM - Light data processing
t3.medium  # 2 vCPU, 4 GB RAM - Small ETL jobs
t3.large   # 2 vCPU, 8 GB RAM - Medium data processing
```

**M5/M6i Family (Fixed Performance)**:
- **Use Cases**: Web applications, microservices, enterprise applications
- **Data Engineering Fit**: Steady-state data processing, application servers
- **Performance**: Consistent CPU performance
- **Networking**: Up to 25 Gbps network performance
```bash
# M5 instances for consistent workloads
m5.large     # 2 vCPU, 8 GB RAM - Small data applications
m5.xlarge    # 4 vCPU, 16 GB RAM - Medium ETL jobs
m5.2xlarge   # 8 vCPU, 32 GB RAM - Data processing nodes
m5.4xlarge   # 16 vCPU, 64 GB RAM - Large data applications
m5.8xlarge   # 32 vCPU, 128 GB RAM - High-performance processing
```

### Compute Optimized Instances
**High-performance processors for CPU-intensive workloads**

**C5/C6i Family**:
- **Use Cases**: High-performance computing, scientific modeling, batch processing
- **Data Engineering Fit**: CPU-intensive ETL, data transformation, compression
- **Performance**: Up to 3.5 GHz Intel processors
- **Best For**: Compute-bound data processing tasks
```bash
# C5 instances for CPU-intensive workloads
c5.large     # 2 vCPU, 4 GB RAM - Light compute tasks
c5.xlarge    # 4 vCPU, 8 GB RAM - Medium compute processing
c5.2xlarge   # 8 vCPU, 16 GB RAM - Heavy data transformation
c5.4xlarge   # 16 vCPU, 32 GB RAM - Parallel processing
c5.9xlarge   # 36 vCPU, 72 GB RAM - Large-scale compute
c5.18xlarge  # 72 vCPU, 144 GB RAM - Maximum compute power
```

### Memory Optimized Instances
**High memory-to-vCPU ratio for memory-intensive applications**

**R5/R6i Family (Memory Optimized)**:
- **Use Cases**: In-memory databases, real-time analytics, caching
- **Data Engineering Fit**: Spark clusters, in-memory processing, large datasets
- **Memory**: Up to 768 GB RAM per instance
- **Best For**: Memory-bound data processing
```bash
# R5 instances for memory-intensive workloads
r5.large     # 2 vCPU, 16 GB RAM - Small in-memory processing
r5.xlarge    # 4 vCPU, 32 GB RAM - Medium memory workloads
r5.2xlarge   # 8 vCPU, 64 GB RAM - Large datasets in memory
r5.4xlarge   # 16 vCPU, 128 GB RAM - Big data analytics
r5.8xlarge   # 32 vCPU, 256 GB RAM - Large Spark executors
r5.12xlarge  # 48 vCPU, 384 GB RAM - Very large memory needs
r5.24xlarge  # 96 vCPU, 768 GB RAM - Maximum memory capacity
```

**X1e Family (High Memory)**:
- **Use Cases**: SAP HANA, Apache Spark, high-performance databases
- **Memory**: Up to 3,904 GB RAM
- **Best For**: Extremely large in-memory datasets
```bash
# X1e instances for extreme memory requirements
x1e.xlarge   # 4 vCPU, 122 GB RAM - Large in-memory databases
x1e.2xlarge  # 8 vCPU, 244 GB RAM - Very large datasets
x1e.4xlarge  # 16 vCPU, 488 GB RAM - Massive in-memory processing
```

### Storage Optimized Instances
**High sequential read/write access to large datasets**

**I3/I4i Family (NVMe SSD)**:
- **Use Cases**: Distributed file systems, data warehousing, search engines
- **Data Engineering Fit**: High-performance databases, fast data processing
- **Storage**: NVMe SSD instance storage
- **Performance**: Up to 3.3 million random IOPS
```bash
# I3 instances with NVMe SSD storage
i3.large     # 2 vCPU, 15.25 GB RAM, 475 GB NVMe SSD
i3.xlarge    # 4 vCPU, 30.5 GB RAM, 950 GB NVMe SSD
i3.2xlarge   # 8 vCPU, 61 GB RAM, 1,900 GB NVMe SSD
i3.4xlarge   # 16 vCPU, 122 GB RAM, 3,800 GB NVMe SSD
i3.8xlarge   # 32 vCPU, 244 GB RAM, 7,600 GB NVMe SSD
```

**D2/D3 Family (Dense HDD)**:
- **Use Cases**: MapReduce workloads, distributed file systems
- **Storage**: Up to 48 TB HDD storage per instance
- **Best For**: High sequential I/O, large-scale data processing
```bash
# D2 instances with dense HDD storage
d2.xlarge    # 4 vCPU, 30.5 GB RAM, 3 x 2 TB HDD
d2.2xlarge   # 8 vCPU, 61 GB RAM, 6 x 2 TB HDD
d2.4xlarge   # 16 vCPU, 122 GB RAM, 12 x 2 TB HDD
d2.8xlarge   # 36 vCPU, 244 GB RAM, 24 x 2 TB HDD
```

### Accelerated Computing Instances
**Hardware accelerators for specialized workloads**

**P3/P4 Family (GPU for ML)**:
- **Use Cases**: Machine learning training, high-performance computing
- **Data Engineering Fit**: ML model training, GPU-accelerated analytics
- **GPUs**: NVIDIA V100/A100 Tensor Core GPUs
```bash
# P3 instances with NVIDIA V100 GPUs
p3.2xlarge   # 8 vCPU, 61 GB RAM, 1 x V100 GPU
p3.8xlarge   # 32 vCPU, 244 GB RAM, 4 x V100 GPU
p3.16xlarge  # 64 vCPU, 488 GB RAM, 8 x V100 GPU
```

**G4 Family (GPU for Graphics)**:
- **Use Cases**: Machine learning inference, video processing
- **GPUs**: NVIDIA T4 Tensor Core GPUs
- **Best For**: ML inference, data visualization
```bash
# G4 instances with NVIDIA T4 GPUs
g4dn.xlarge   # 4 vCPU, 16 GB RAM, 1 x T4 GPU
g4dn.2xlarge  # 8 vCPU, 32 GB RAM, 1 x T4 GPU
g4dn.4xlarge  # 16 vCPU, 64 GB RAM, 1 x T4 GPU
```

**Naming Convention**:
```
m5.xlarge
│ │  │
│ │  └── Size (nano, micro, small, medium, large, xlarge, 2xlarge, etc.)
│ └───── Generation (5 = 5th generation)
└─────── Family (m = general purpose)
```

## 3. Amazon Machine Images (AMI)
**What it is**: Pre-configured template for EC2 instances containing OS and software.

**AMI Types**:
```bash
# AWS-provided AMIs
Amazon Linux 2
Ubuntu Server 20.04 LTS
Windows Server 2019
Red Hat Enterprise Linux 8

# Community AMIs
Deep Learning AMI
Docker CE AMI
WordPress AMI

# Custom AMIs
Your own configured images
```

**Creating Custom AMI**:
```bash
# Create AMI from running instance
aws ec2 create-image \
    --instance-id i-1234567890abcdef0 \
    --name "MyCustomAMI" \
    --description "Web server with custom configuration"
```

## 4. Storage Options
**EBS (Elastic Block Store)**:
```bash
# Volume Types
gp3    # General Purpose SSD (latest generation)
gp2    # General Purpose SSD
io2    # Provisioned IOPS SSD (high performance)
io1    # Provisioned IOPS SSD
st1    # Throughput Optimized HDD
sc1    # Cold HDD

# Create and attach EBS volume
aws ec2 create-volume \
    --size 100 \
    --volume-type gp3 \
    --availability-zone us-west-2a

aws ec2 attach-volume \
    --volume-id vol-1234567890abcdef0 \
    --instance-id i-1234567890abcdef0 \
    --device /dev/sdf
```

**Instance Store**:
- **Temporary**: Data lost when instance stops
- **High Performance**: Direct-attached storage
- **No Additional Cost**: Included with instance

## 5. Networking & Security
**Security Groups**:
```bash
# Create security group
aws ec2 create-security-group \
    --group-name web-servers \
    --description "Security group for web servers"

# Add inbound rules
aws ec2 authorize-security-group-ingress \
    --group-id sg-12345678 \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
    --group-id sg-12345678 \
    --protocol tcp \
    --port 22 \
    --source-group sg-87654321
```

**Key Pairs**:
```bash
# Create key pair
aws ec2 create-key-pair \
    --key-name MyKeyPair \
    --query 'KeyMaterial' \
    --output text > MyKeyPair.pem

# Set permissions
chmod 400 MyKeyPair.pem

# SSH to instance
ssh -i MyKeyPair.pem ec2-user@public-ip-address
```

## 6. Instance Lifecycle
**Instance States**:
```bash
# Launch instance
aws ec2 run-instances \
    --image-id ami-12345678 \
    --count 1 \
    --instance-type t3.micro \
    --key-name MyKeyPair \
    --security-group-ids sg-12345678

# Instance states
pending → running → stopping → stopped → terminating → terminated

# Control instances
aws ec2 start-instances --instance-ids i-1234567890abcdef0
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 reboot-instances --instance-ids i-1234567890abcdef0
aws ec2 terminate-instances --instance-ids i-1234567890abcdef0
```

## 7. Auto Scaling
**Auto Scaling Groups**:
```bash
# Create launch template
aws ec2 create-launch-template \
    --launch-template-name web-server-template \
    --launch-template-data '{
        "ImageId": "ami-12345678",
        "InstanceType": "t3.micro",
        "KeyName": "MyKeyPair",
        "SecurityGroupIds": ["sg-12345678"]
    }'

# Create Auto Scaling group
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name web-servers-asg \
    --launch-template LaunchTemplateName=web-server-template,Version=1 \
    --min-size 1 \
    --max-size 10 \
    --desired-capacity 2 \
    --availability-zones us-west-2a us-west-2b
```

**Scaling Policies**:
```bash
# Create scaling policy
aws autoscaling put-scaling-policy \
    --auto-scaling-group-name web-servers-asg \
    --policy-name scale-up-policy \
    --scaling-adjustment 1 \
    --adjustment-type ChangeInCapacity
```

## 8. Load Balancing
**Application Load Balancer**:
```bash
# Create load balancer
aws elbv2 create-load-balancer \
    --name web-servers-alb \
    --subnets subnet-12345678 subnet-87654321 \
    --security-groups sg-12345678

# Create target group
aws elbv2 create-target-group \
    --name web-servers-targets \
    --protocol HTTP \
    --port 80 \
    --vpc-id vpc-12345678

# Register targets
aws elbv2 register-targets \
    --target-group-arn arn:aws:elasticloadbalancing:... \
    --targets Id=i-1234567890abcdef0 Id=i-0987654321fedcba0
```

## 9. Monitoring & Logging
**CloudWatch Metrics**:
```bash
# Basic monitoring (5-minute intervals)
CPUUtilization
NetworkIn/NetworkOut
DiskReadOps/DiskWriteOps

# Detailed monitoring (1-minute intervals)
aws ec2 monitor-instances --instance-ids i-1234567890abcdef0
```

**CloudWatch Logs**:
```bash
# Install CloudWatch agent
sudo yum install amazon-cloudwatch-agent

# Configure agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

# Start agent
sudo systemctl start amazon-cloudwatch-agent
```

## 10. Cost Optimization
**Pricing Models**:
```bash
# On-Demand: Pay by hour/second
Standard pricing, no commitment

# Reserved Instances: 1-3 year commitment
Up to 75% savings compared to On-Demand

# Spot Instances: Bid on spare capacity
Up to 90% savings, can be interrupted

# Savings Plans: Flexible pricing model
Commitment to consistent usage
```

**Cost Management**:
```bash
# Right-sizing recommendations
aws compute-optimizer get-ec2-instance-recommendations

# Cost and usage reports
aws ce get-cost-and-usage \
    --time-period Start=2024-01-01,End=2024-01-31 \
    --granularity MONTHLY \
    --metrics BlendedCost
```