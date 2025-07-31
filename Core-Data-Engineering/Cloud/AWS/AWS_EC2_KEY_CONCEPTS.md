# AWS EC2 Key Concepts

## 1. Virtual Computing in the Cloud
**What it is**: Scalable virtual servers in AWS cloud providing compute capacity.

**Core Benefits**:
- **Elasticity**: Scale up/down based on demand
- **Pay-as-you-go**: Only pay for what you use
- **Global**: Available in multiple regions worldwide
- **Secure**: Built-in security features and compliance

## 2. Instance Types & Families
**Instance Families**:
```bash
# General Purpose (balanced CPU, memory, networking)
t3.micro, t3.small, t3.medium, t3.large
m5.large, m5.xlarge, m5.2xlarge

# Compute Optimized (high-performance processors)
c5.large, c5.xlarge, c5.2xlarge

# Memory Optimized (fast performance for memory-intensive workloads)
r5.large, r5.xlarge, r5.2xlarge

# Storage Optimized (high sequential read/write access)
i3.large, i3.xlarge, d2.xlarge

# Accelerated Computing (hardware accelerators, GPUs)
p3.2xlarge, g4dn.xlarge
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