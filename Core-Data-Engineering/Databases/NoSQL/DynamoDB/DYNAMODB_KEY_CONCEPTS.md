# Amazon DynamoDB Key Concepts

## 🎯 What is DynamoDB?
Fully managed NoSQL database service by AWS with single-digit millisecond performance at any scale.

## 🏗️ Core Architecture

### Table Structure
```json
{
  "TableName": "Users",
  "KeySchema": [
    {"AttributeName": "userId", "KeyType": "HASH"},
    {"AttributeName": "timestamp", "KeyType": "RANGE"}
  ],
  "AttributeDefinitions": [
    {"AttributeName": "userId", "AttributeType": "S"},
    {"AttributeName": "timestamp", "AttributeType": "N"}
  ]
}
```

### Key Components
- **Table** - Collection of items
- **Item** - Individual record (max 400KB)
- **Attribute** - Name-value pair
- **Partition Key** - Primary hash key
- **Sort Key** - Optional range key

## 🔧 DynamoDB Operations

### Basic Operations
```python
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Users')

# Put Item
table.put_item(
    Item={
        'userId': 'user123',
        'name': 'John Doe',
        'email': 'john@example.com'
    }
)

# Get Item
response = table.get_item(
    Key={'userId': 'user123'}
)

# Query
response = table.query(
    KeyConditionExpression=Key('userId').eq('user123')
)

# Scan
response = table.scan(
    FilterExpression=Attr('age').gt(18)
)
```

## 📊 Advanced Features

### Global Secondary Indexes (GSI)
```python
# Create GSI
table.create_global_secondary_index(
    IndexName='email-index',
    KeySchema=[
        {'AttributeName': 'email', 'KeyType': 'HASH'}
    ],
    Projection={'ProjectionType': 'ALL'}
)
```

### DynamoDB Streams
```python
# Enable streams
table.modify(
    StreamSpecification={
        'StreamEnabled': True,
        'StreamViewType': 'NEW_AND_OLD_IMAGES'
    }
)
```

## 🚀 Performance & Scaling

### Capacity Modes
```python
# On-Demand
table = dynamodb.create_table(
    BillingMode='PAY_PER_REQUEST'
)

# Provisioned
table = dynamodb.create_table(
    BillingMode='PROVISIONED',
    ProvisionedThroughput={
        'ReadCapacityUnits': 100,
        'WriteCapacityUnits': 100
    }
)
```

### Auto Scaling
- Automatic capacity adjustment
- Target utilization percentage
- Min/max capacity limits

## 🔒 Security Features

### Access Control
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem"
      ],
      "Resource": "arn:aws:dynamodb:region:account:table/Users"
    }
  ]
}
```

### Encryption
- Encryption at rest (AWS KMS)
- Encryption in transit (TLS)
- Point-in-time recovery

## 🎯 Best Practices

### Data Modeling
- Design for access patterns
- Use single-table design when possible
- Avoid hot partitions
- Implement proper key distribution

### Cost Optimization
- Choose appropriate capacity mode
- Use sparse indexes
- Implement data lifecycle policies
- Monitor CloudWatch metrics

## 🎯 Use Cases
- Gaming leaderboards
- IoT data collection
- Real-time bidding
- Shopping carts
- Session management
- Mobile backends

## ⚠️ Limitations
- 400KB item size limit
- No complex queries (no JOINs)
- Eventually consistent reads by default
- Limited query flexibility without GSI