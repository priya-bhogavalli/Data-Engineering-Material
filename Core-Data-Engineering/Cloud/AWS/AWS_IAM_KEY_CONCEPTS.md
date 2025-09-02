# AWS IAM Key Concepts

## 🎯 **Overview**
AWS Identity and Access Management (IAM) is the foundation of security in AWS, controlling who can access what resources and under what conditions. For data engineering, IAM is critical for securing data pipelines, managing service permissions, and ensuring compliance.

**What You'll Learn:**
- IAM users, groups, roles, and policies
- Security best practices for data engineering
- Service-to-service authentication
- Cross-account access patterns
- Compliance and auditing strategies
- Troubleshooting access issues
- Automation and infrastructure as code

**Key Security Principles:**
- **Least Privilege**: Grant minimum necessary permissions
- **Defense in Depth**: Multiple layers of security
- **Zero Trust**: Verify every access request
- **Principle of Separation**: Separate duties and environments
- **Regular Auditing**: Continuous monitoring and review

**Target Audience:**
- Data Engineers securing data pipelines
- Security Engineers managing access controls
- DevOps Engineers implementing infrastructure security
- Compliance Officers ensuring regulatory adherence
- Solution Architects designing secure systems

## 1. Identity and Access Management
**What it is**: Service that controls access to AWS resources through authentication and authorization.

**Core Components**:
- **Users**: Individual identities with credentials
- **Groups**: Collections of users with shared permissions
- **Roles**: Temporary credentials for services/applications
- **Policies**: Documents defining permissions

## 2. Users and Authentication
**IAM Users**:
```bash
# Create user
aws iam create-user --user-name DataEngineer

# Create access keys
aws iam create-access-key --user-name DataEngineer

# Set password for console access
aws iam create-login-profile \
    --user-name DataEngineer \
    --password TempPassword123! \
    --password-reset-required
```

**Multi-Factor Authentication (MFA)**:
```bash
# Enable MFA device
aws iam enable-mfa-device \
    --user-name DataEngineer \
    --serial-number arn:aws:iam::123456789012:mfa/DataEngineer \
    --authentication-code-1 123456 \
    --authentication-code-2 789012
```

## 3. Groups and User Management
**IAM Groups**:
```bash
# Create group
aws iam create-group --group-name DataEngineers

# Add user to group
aws iam add-user-to-group \
    --group-name DataEngineers \
    --user-name DataEngineer

# Attach policy to group
aws iam attach-group-policy \
    --group-name DataEngineers \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

## 4. Policies and Permissions
**Policy Structure**:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowS3Access",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::my-data-bucket/*"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:x-amz-server-side-encryption": "AES256"
                }
            }
        }
    ]
}
```

**Policy Types**:
```bash
# AWS Managed Policies (maintained by AWS)
arn:aws:iam::aws:policy/AmazonS3FullAccess
arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess

# Customer Managed Policies (custom policies)
# Inline Policies (embedded directly in user/group/role)
```

**Common Policy Examples**:
```json
// Data Engineer Policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "glue:*",
                "athena:*",
                "redshift:*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Deny",
            "Action": [
                "s3:DeleteBucket"
            ],
            "Resource": "*"
        }
    ]
}

// Read-only Analyst Policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket",
                "athena:StartQueryExecution",
                "athena:GetQueryResults"
            ],
            "Resource": "*"
        }
    ]
}
```

## 5. Roles and Temporary Credentials
**IAM Roles**:
```bash
# Create role for EC2
aws iam create-role \
    --role-name EC2-S3-Access-Role \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "ec2.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }'

# Attach policy to role
aws iam attach-role-policy \
    --role-name EC2-S3-Access-Role \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess

# Create instance profile
aws iam create-instance-profile \
    --instance-profile-name EC2-S3-Profile

# Add role to instance profile
aws iam add-role-to-instance-profile \
    --instance-profile-name EC2-S3-Profile \
    --role-name EC2-S3-Access-Role
```

**Cross-Account Access**:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::ACCOUNT-B:user/DataAnalyst"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "unique-external-id"
                }
            }
        }
    ]
}
```

## 6. Security Best Practices
**Principle of Least Privilege**:
```json
// Instead of broad permissions
{
    "Effect": "Allow",
    "Action": "s3:*",
    "Resource": "*"
}

// Use specific permissions
{
    "Effect": "Allow",
    "Action": [
        "s3:GetObject",
        "s3:PutObject"
    ],
    "Resource": [
        "arn:aws:s3:::specific-bucket/*"
    ]
}
```

**Conditional Access**:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*",
            "Condition": {
                "IpAddress": {
                    "aws:SourceIp": "203.0.113.0/24"
                },
                "DateGreaterThan": {
                    "aws:CurrentTime": "2024-01-01T00:00:00Z"
                },
                "Bool": {
                    "aws:SecureTransport": "true"
                }
            }
        }
    ]
}
```

## 7. Access Keys and Credentials
**Access Key Management**:
```bash
# Rotate access keys
aws iam create-access-key --user-name DataEngineer
aws iam update-access-key \
    --user-name DataEngineer \
    --access-key-id AKIAIOSFODNN7EXAMPLE \
    --status Inactive
aws iam delete-access-key \
    --user-name DataEngineer \
    --access-key-id AKIAIOSFODNN7EXAMPLE
```

**Temporary Credentials**:
```bash
# Assume role
aws sts assume-role \
    --role-arn arn:aws:iam::123456789012:role/DataProcessingRole \
    --role-session-name DataProcessingSession

# Get session token
aws sts get-session-token \
    --duration-seconds 3600 \
    --serial-number arn:aws:iam::123456789012:mfa/user \
    --token-code 123456
```

## 8. Monitoring and Auditing
**CloudTrail Integration**:
```json
// Example CloudTrail event
{
    "eventTime": "2024-01-15T10:30:00Z",
    "eventName": "AssumeRole",
    "eventSource": "sts.amazonaws.com",
    "userIdentity": {
        "type": "IAMUser",
        "principalId": "AIDACKCEVSQ6C2EXAMPLE",
        "arn": "arn:aws:iam::123456789012:user/DataEngineer",
        "accountId": "123456789012",
        "userName": "DataEngineer"
    },
    "requestParameters": {
        "roleArn": "arn:aws:iam::123456789012:role/DataProcessingRole",
        "roleSessionName": "DataProcessingSession"
    }
}
```

**Access Analyzer**:
```bash
# Create analyzer
aws accessanalyzer create-analyzer \
    --analyzer-name MyAnalyzer \
    --type ACCOUNT

# List findings
aws accessanalyzer list-findings \
    --analyzer-arn arn:aws:access-analyzer:us-east-1:123456789012:analyzer/MyAnalyzer
```

## 9. Federation and SSO
**SAML Federation**:
```xml
<!-- SAML Assertion Example -->
<saml:Assertion>
    <saml:AttributeStatement>
        <saml:Attribute Name="https://aws.amazon.com/SAML/Attributes/Role">
            <saml:AttributeValue>
                arn:aws:iam::123456789012:role/SAMLRole,
                arn:aws:iam::123456789012:saml-provider/CompanySAML
            </saml:AttributeValue>
        </saml:Attribute>
    </saml:AttributeStatement>
</saml:Assertion>
```

**AWS SSO (Identity Center)**:
```bash
# List accounts
aws sso-admin list-accounts-for-provisioned-permission-set \
    --instance-arn arn:aws:sso:::instance/ssoins-1234567890abcdef \
    --permission-set-arn arn:aws:sso:::permissionSet/ssoins-1234567890abcdef/ps-1234567890abcdef
```

## 10. Troubleshooting Access Issues
**Common Error Messages**:
```bash
# Access Denied
"User: arn:aws:iam::123456789012:user/DataEngineer is not authorized 
to perform: s3:GetObject on resource: arn:aws:s3:::my-bucket/file.txt"

# Invalid credentials
"The AWS Access Key Id you provided does not exist in our records"

# MFA required
"MultiFactorAuthentication failed with invalid MFA one time pass code"
```

**Policy Simulator**:
```bash
# Test policy
aws iam simulate-principal-policy \
    --policy-source-arn arn:aws:iam::123456789012:user/DataEngineer \
    --action-names s3:GetObject \
    --resource-arns arn:aws:s3:::my-bucket/file.txt
```