# Microsoft Azure Interview Questions for Data Engineers - EXPANDED

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-70)](#intermediate-level-questions-31-70)
3. [Advanced Level Questions (71-100)](#advanced-level-questions-71-100)

---

## Basic Level Questions (1-30)

### 1. What are the core Azure services for data engineering and their use cases?

**Answer**: Essential Azure services for data engineering:

**Storage Services**:
- **Azure Blob Storage**: Object storage for data lakes
- **Azure Data Lake Storage Gen2**: Hierarchical namespace for big data
- **Azure Files**: Managed file shares
- **Azure Disk Storage**: Block storage for VMs

**Compute Services**:
- **Azure Virtual Machines**: Custom compute instances
- **Azure Functions**: Serverless compute
- **Azure Databricks**: Apache Spark analytics platform
- **Azure Batch**: Large-scale parallel workloads

**Database Services**:
- **Azure SQL Database**: Managed SQL database
- **Azure Cosmos DB**: Multi-model NoSQL database
- **Azure Synapse Analytics**: Data warehouse
- **Azure Database for PostgreSQL/MySQL**: Managed open-source databases

**Analytics Services**:
- **Azure Synapse Analytics**: Unified analytics platform
- **Azure Data Factory**: ETL/ELT orchestration
- **Azure Stream Analytics**: Real-time stream processing
- **Power BI**: Business intelligence

```python
# Example: Basic Azure SDK usage
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
import pyodbc

# Blob Storage operations
credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)

container_client = blob_service.get_container_client("data")
with open("local_file.csv", "rb") as data:
    container_client.upload_blob(name="data/file.csv", data=data)

# SQL Database connection
conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=myserver.database.windows.net;Database=mydatabase;Authentication=ActiveDirectoryMsi;"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.execute("SELECT * FROM sales LIMIT 10")
```

### 2. How do you design a data lake architecture on Azure?

**Answer**: Azure data lake architecture components:

**Storage Layer (ADLS Gen2)**:
```
/data-lake-container/
├── raw/                    # Raw ingested data
│   ├── year=2024/
│   ├── month=01/
│   └── day=15/
├── processed/              # Cleaned data
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── curated/               # Analytics-ready
└── archive/               # Historical data
```

**Data Ingestion**:
```json
{
  "name": "CopyDataPipeline",
  "properties": {
    "activities": [
      {
        "name": "CopyFromSource",
        "type": "Copy",
        "inputs": [
          {
            "referenceName": "SourceDataset",
            "type": "DatasetReference"
          }
        ],
        "outputs": [
          {
            "referenceName": "SinkDataset", 
            "type": "DatasetReference"
          }
        ],
        "typeProperties": {
          "source": {
            "type": "SqlSource",
            "sqlReaderQuery": "SELECT * FROM sales WHERE modified_date > '@{pipeline().parameters.lastRunTime}'"
          },
          "sink": {
            "type": "ParquetSink",
            "storeSettings": {
              "type": "AzureBlobFSWriteSettings",
              "copyBehavior": "PreserveHierarchy"
            }
          }
        }
      }
    ]
  }
}
```

### 3. How do you implement data security and access control in Azure?

**Answer**: Multi-layered security approach:

**Azure Active Directory Integration**:
```python
# Service principal authentication
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

credential = ClientSecretCredential(
    tenant_id="tenant-id",
    client_id="client-id", 
    client_secret="client-secret"
)

# Key Vault for secrets
vault_url = "https://myvault.vault.azure.net/"
secret_client = SecretClient(vault_url=vault_url, credential=credential)

# Store connection string
secret_client.set_secret("sql-connection-string", "Server=...")
```

**Role-Based Access Control (RBAC)**:
```bash
# Azure CLI commands for RBAC
# Assign Storage Blob Data Contributor role
az role assignment create \
  --assignee user@company.com \
  --role "Storage Blob Data Contributor" \
  --scope "/subscriptions/sub-id/resourceGroups/rg/providers/Microsoft.Storage/storageAccounts/storage"

# Create custom role
az role definition create --role-definition '{
  "Name": "Data Engineer Role",
  "Description": "Custom role for data engineers",
  "Actions": [
    "Microsoft.Storage/storageAccounts/blobServices/containers/read",
    "Microsoft.Storage/storageAccounts/blobServices/containers/write",
    "Microsoft.Sql/servers/databases/read"
  ],
  "AssignableScopes": ["/subscriptions/subscription-id"]
}'
```

### 4. How do you monitor and optimize costs in Azure?

**Answer**: Cost optimization strategies:

**Cost Management**:
```python
# Azure Cost Management API
import requests
from azure.identity import DefaultAzureCredential

def get_cost_data():
    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default")
    
    headers = {
        'Authorization': f'Bearer {token.token}',
        'Content-Type': 'application/json'
    }
    
    url = "https://management.azure.com/subscriptions/{subscription-id}/providers/Microsoft.CostManagement/query"
    
    query = {
        "type": "ActualCost",
        "timeframe": "MonthToDate",
        "dataset": {
            "granularity": "Daily",
            "aggregation": {
                "totalCost": {
                    "name": "PreTaxCost",
                    "function": "Sum"
                }
            },
            "grouping": [
                {
                    "type": "Dimension",
                    "name": "ServiceName"
                }
            ]
        }
    }
    
    response = requests.post(url, headers=headers, json=query)
    return response.json()
```

**Storage Optimization**:
```python
# Blob lifecycle management
lifecycle_policy = {
    "rules": [
        {
            "name": "DataLakeLifecycle",
            "enabled": True,
            "type": "Lifecycle",
            "definition": {
                "filters": {
                    "blobTypes": ["blockBlob"],
                    "prefixMatch": ["raw/"]
                },
                "actions": {
                    "baseBlob": {
                        "tierToCool": {"daysAfterModificationGreaterThan": 30},
                        "tierToArchive": {"daysAfterModificationGreaterThan": 90},
                        "delete": {"daysAfterModificationGreaterThan": 2555}
                    }
                }
            }
        }
    ]
}
```

### 5. How do you implement data backup and disaster recovery?

**Answer**: Comprehensive backup and DR strategy:

**Geo-Redundant Storage**:
```python
# Configure geo-redundant storage
from azure.storage.blob import BlobServiceClient
from azure.mgmt.storage import StorageManagementClient

def setup_geo_redundancy():
    storage_client = StorageManagementClient(credential, subscription_id)
    
    # Update storage account to GRS
    storage_client.storage_accounts.update(
        resource_group_name="myresourcegroup",
        account_name="mystorageaccount",
        parameters={
            "sku": {"name": "Standard_GRS"},
            "kind": "StorageV2"
        }
    )
```

**SQL Database Backup**:
```sql
-- Automated backups are enabled by default
-- Configure long-term retention
ALTER DATABASE mydatabase 
SET BACKUP_RETENTION_POLICY (
    WEEKLY_RETENTION = 'P12W',
    MONTHLY_RETENTION = 'P12M', 
    YEARLY_RETENTION = 'P5Y',
    WEEK_OF_YEAR = 1
);

-- Manual backup
BACKUP DATABASE mydatabase 
TO URL = 'https://mystorageaccount.blob.core.windows.net/backups/mydatabase.bacpac'
WITH CREDENTIAL = 'MyCredential';
```

### 6. How do you implement real-time data processing with Azure Stream Analytics?

**Answer**: Real-time streaming architecture:

**Stream Analytics Job**:
```sql
-- Stream Analytics Query
WITH FilteredEvents AS (
    SELECT 
        userId,
        eventType,
        eventValue,
        eventTime,
        System.Timestamp() AS windowEnd
    FROM EventHub
    WHERE eventType IN ('click', 'purchase')
),

AggregatedData AS (
    SELECT 
        userId,
        eventType,
        COUNT(*) AS eventCount,
        SUM(eventValue) AS totalValue,
        AVG(eventValue) AS avgValue,
        System.Timestamp() AS windowEnd
    FROM FilteredEvents
    GROUP BY userId, eventType, TumblingWindow(minute, 5)
)

SELECT * INTO OutputBlob FROM AggregatedData;
SELECT * INTO PowerBIDashboard FROM AggregatedData;
```

**Event Hub Integration**:
```python
# Event Hub producer
from azure.eventhub import EventHubProducerClient, EventData
import json

def send_events():
    producer = EventHubProducerClient.from_connection_string(
        conn_str="Endpoint=sb://...",
        eventhub_name="events"
    )
    
    event_data_batch = producer.create_batch()
    
    for i in range(100):
        event_data = {
            'userId': f'user_{i}',
            'eventType': 'click',
            'eventValue': random.uniform(1, 100),
            'eventTime': datetime.utcnow().isoformat()
        }
        
        event_data_batch.add(EventData(json.dumps(event_data)))
    
    producer.send_batch(event_data_batch)
    producer.close()
```

### 7. How do you optimize Azure Synapse Analytics for performance?

**Answer**: Synapse optimization techniques:

**Table Design**:
```sql
-- Distributed table with hash distribution
CREATE TABLE fact_sales (
    sale_id BIGINT,
    customer_id INT,
    product_id INT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
WITH (
    DISTRIBUTION = HASH(customer_id),
    CLUSTERED COLUMNSTORE INDEX
);

-- Replicated dimension table
CREATE TABLE dim_product (
    product_id INT,
    product_name VARCHAR(100),
    category VARCHAR(50)
)
WITH (
    DISTRIBUTION = REPLICATE,
    CLUSTERED COLUMNSTORE INDEX
);

-- Partitioned table
CREATE TABLE sales_history (
    sale_id BIGINT,
    sale_date DATE,
    amount DECIMAL(10,2)
)
WITH (
    DISTRIBUTION = HASH(sale_id),
    PARTITION (sale_date RANGE RIGHT FOR VALUES 
        ('2023-01-01', '2023-02-01', '2023-03-01'))
);
```

**Query Optimization**:
```sql
-- Use appropriate resource class
EXEC sp_addrolemember 'largerc', 'dataengineer@company.com';

-- Optimized query with statistics
UPDATE STATISTICS fact_sales;

SELECT 
    p.category,
    SUM(s.amount) as total_sales,
    COUNT(*) as transaction_count
FROM fact_sales s
INNER JOIN dim_product p ON s.product_id = p.product_id
WHERE s.sale_date >= '2024-01-01'
GROUP BY p.category
OPTION (LABEL = 'Sales Analysis Query');

-- Monitor query performance
SELECT 
    request_id,
    status,
    total_elapsed_time,
    command
FROM sys.dm_pdw_exec_requests
WHERE status IN ('Running', 'Suspended')
ORDER BY total_elapsed_time DESC;
```

### 8. How do you implement data quality checks in Azure?

**Answer**: Data quality framework using Azure services:

**Data Factory Data Quality**:
```json
{
  "name": "DataQualityPipeline",
  "properties": {
    "activities": [
      {
        "name": "ValidateData",
        "type": "Validation",
        "typeProperties": {
          "dataset": {
            "referenceName": "InputDataset",
            "type": "DatasetReference"
          },
          "timeout": "0.00:05:00",
          "sleep": 10,
          "minimumSize": 1024
        }
      },
      {
        "name": "DataQualityCheck",
        "type": "SqlServerStoredProcedure",
        "dependsOn": [
          {
            "activity": "ValidateData",
            "dependencyConditions": ["Succeeded"]
          }
        ],
        "typeProperties": {
          "storedProcedureName": "sp_CheckDataQuality",
          "storedProcedureParameters": {
            "tableName": {
              "value": "@pipeline().parameters.tableName",
              "type": "String"
            }
          }
        }
      }
    ]
  }
}
```

**Azure Functions for Custom Validation**:
```python
import azure.functions as func
import pandas as pd
from azure.storage.blob import BlobServiceClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Get blob data
    blob_service = BlobServiceClient.from_connection_string(conn_str)
    blob_client = blob_service.get_blob_client(
        container="data", 
        blob=req.params.get('filename')
    )
    
    # Download and validate
    blob_data = blob_client.download_blob()
    df = pd.read_csv(blob_data)
    
    quality_issues = []
    
    # Check for nulls
    null_counts = df.isnull().sum()
    if null_counts.any():
        quality_issues.append(f"Null values found: {null_counts.to_dict()}")
    
    # Check data types
    if df['amount'].dtype != 'float64':
        quality_issues.append("Amount column should be numeric")
    
    # Business rules
    if (df['amount'] < 0).any():
        quality_issues.append("Negative amounts found")
    
    if quality_issues:
        return func.HttpResponse(
            json.dumps({"status": "failed", "issues": quality_issues}),
            status_code=400
        )
    
    return func.HttpResponse(
        json.dumps({"status": "passed"}),
        status_code=200
    )
```

### 9. How do you implement data lineage and governance in Azure?

**Answer**: Data governance framework:

**Azure Purview Integration**:
```python
# Azure Purview REST API integration
import requests
from azure.identity import DefaultAzureCredential

class PurviewClient:
    def __init__(self, account_name):
        self.account_name = account_name
        self.credential = DefaultAzureCredential()
        self.base_url = f"https://{account_name}.purview.azure.com"
    
    def get_access_token(self):
        token = self.credential.get_token("https://purview.azure.net/.default")
        return token.token
    
    def create_entity(self, entity_data):
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}/catalog/api/atlas/v2/entity"
        response = requests.post(url, headers=headers, json=entity_data)
        return response.json()
    
    def search_entities(self, query):
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}/catalog/api/search/query"
        payload = {
            "keywords": query,
            "limit": 50
        }
        
        response = requests.post(url, headers=headers, json=payload)
        return response.json()

# Usage
purview = PurviewClient("mypurviewaccount")

# Create data asset
entity_data = {
    "entity": {
        "typeName": "azure_sql_table",
        "attributes": {
            "qualifiedName": "mssql://myserver.database.windows.net/mydatabase/dbo/sales",
            "name": "sales",
            "description": "Sales transaction data",
            "owner": "data-engineering-team"
        }
    }
}

result = purview.create_entity(entity_data)
```

### 10. How do you implement automated data pipeline orchestration?

**Answer**: Pipeline orchestration using Azure services:

**Azure Data Factory Pipeline**:
```json
{
  "name": "MasterDataPipeline",
  "properties": {
    "activities": [
      {
        "name": "CheckDataAvailability",
        "type": "GetMetadata",
        "typeProperties": {
          "dataset": {
            "referenceName": "SourceDataset",
            "type": "DatasetReference"
          },
          "fieldList": ["exists", "lastModified", "size"]
        }
      },
      {
        "name": "ConditionalExecution",
        "type": "IfCondition",
        "dependsOn": [
          {
            "activity": "CheckDataAvailability", 
            "dependencyConditions": ["Succeeded"]
          }
        ],
        "typeProperties": {
          "expression": {
            "value": "@greater(activity('CheckDataAvailability').output.size, 0)",
            "type": "Expression"
          },
          "ifTrueActivities": [
            {
              "name": "ExecuteDataProcessing",
              "type": "ExecutePipeline",
              "typeProperties": {
                "pipeline": {
                  "referenceName": "DataProcessingPipeline",
                  "type": "PipelineReference"
                },
                "parameters": {
                  "inputPath": "@pipeline().parameters.inputPath",
                  "outputPath": "@pipeline().parameters.outputPath"
                }
              }
            }
          ]
        }
      }
    ],
    "parameters": {
      "inputPath": {
        "type": "string"
      },
      "outputPath": {
        "type": "string"
      }
    }
  }
}
```

## Intermediate Level Questions (31-70)

### 11. How do you implement Azure Event Hubs for real-time streaming?

**Answer**: Event Hubs provides scalable event ingestion:

```python
# Event Hub producer
from azure.eventhub import EventHubProducerClient, EventData
import json
import asyncio

class EventHubStreamer:
    def __init__(self, connection_string, eventhub_name):
        self.producer = EventHubProducerClient.from_connection_string(
            conn_str=connection_string,
            eventhub_name=eventhub_name
        )
    
    async def send_batch_events(self, events):
        event_data_batch = await self.producer.create_batch()
        
        for event in events:
            try:
                event_data_batch.add(EventData(json.dumps(event)))
            except ValueError:
                # Batch is full, send it and create new batch
                await self.producer.send_batch(event_data_batch)
                event_data_batch = await self.producer.create_batch()
                event_data_batch.add(EventData(json.dumps(event)))
        
        # Send remaining events
        if len(event_data_batch) > 0:
            await self.producer.send_batch(event_data_batch)

# Consumer
from azure.eventhub import EventHubConsumerClient

def on_event(partition_context, event):
    # Process event
    event_data = json.loads(event.body_as_str())
    print(f"Received event: {event_data}")
    
    # Update checkpoint
    partition_context.update_checkpoint(event)

consumer = EventHubConsumerClient.from_connection_string(
    conn_str=connection_string,
    consumer_group="$Default",
    eventhub_name=eventhub_name
)

with consumer:
    consumer.receive(on_event=on_event)
```

### 12. How do you implement Azure Cosmos DB for multi-model data?

**Answer**: Cosmos DB supports multiple data models:

```python
# Document API (SQL)
from azure.cosmos import CosmosClient, PartitionKey

client = CosmosClient(url, credential=key)
database = client.create_database_if_not_exists(id="ecommerce")
container = database.create_container_if_not_exists(
    id="products",
    partition_key=PartitionKey(path="/category"),
    offer_throughput=400
)

# Insert document
product = {
    "id": "product-1",
    "name": "Laptop",
    "category": "Electronics",
    "price": 999.99,
    "specifications": {
        "cpu": "Intel i7",
        "ram": "16GB",
        "storage": "512GB SSD"
    }
}

container.create_item(body=product)

# Query documents
query = "SELECT * FROM c WHERE c.category = @category"
parameters = [{"name": "@category", "value": "Electronics"}]

results = list(container.query_items(
    query=query,
    parameters=parameters,
    enable_cross_partition_query=True
))

# Graph API (Gremlin)
from gremlin_python.driver import client, serializer

gremlin_client = client.Client(
    'wss://myaccount.gremlin.cosmos.azure.com:443/',
    'g',
    username="/dbs/graphdb/colls/graph",
    password=primary_key,
    message_serializer=serializer.GraphSONSerializersV2d0()
)

# Add vertices and edges
queries = [
    "g.addV('person').property('id', 'john').property('name', 'John Doe')",
    "g.addV('person').property('id', 'jane').property('name', 'Jane Smith')",
    "g.V('john').addE('knows').to(g.V('jane'))"
]

for query in queries:
    result = gremlin_client.submit(query).all().result()
```

### 13. How do you implement Azure Machine Learning for data science workflows?

**Answer**: Azure ML provides end-to-end ML lifecycle management:

```python
# Azure ML SDK
from azureml.core import Workspace, Dataset, Experiment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.train.sklearn import SKLearn
from azureml.core.runconfig import RunConfiguration

# Connect to workspace
ws = Workspace.from_config()

# Create dataset
datastore = ws.get_default_datastore()
dataset = Dataset.Tabular.from_delimited_files(
    path=(datastore, 'data/sales.csv')
)

# Register dataset
dataset = dataset.register(
    workspace=ws,
    name='sales_data',
    description='Sales transaction data'
)

# Create compute cluster
compute_config = AmlCompute.provisioning_configuration(
    vm_size='STANDARD_D2_V2',
    min_nodes=0,
    max_nodes=4
)

compute_target = ComputeTarget.create(
    ws, 'ml-cluster', compute_config
)

# Training script
training_script = """
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from azureml.core import Run
import joblib

# Get run context
run = Run.get_context()

# Load data
data = run.input_datasets['sales_data'].to_pandas_dataframe()

# Prepare features
X = data[['quantity', 'unit_price', 'discount']]
y = data['total_amount']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

# Log metrics
run.log('mse', mse)
run.log('rmse', mse ** 0.5)

# Save model
joblib.dump(model, 'outputs/model.pkl')
"""

# Submit experiment
experiment = Experiment(ws, 'sales-prediction')

estimator = SKLearn(
    source_directory='.',
    script_params={'--data-folder': dataset.as_named_input('sales_data')},
    compute_target=compute_target,
    entry_script='train.py'
)

run = experiment.submit(estimator)
```

### 14. How do you implement Azure Kubernetes Service (AKS) for containerized applications?

**Answer**: AKS provides managed Kubernetes for scalable applications:

```yaml
# Deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-processor
  template:
    metadata:
      labels:
        app: data-processor
    spec:
      containers:
      - name: processor
        image: myregistry.azurecr.io/data-processor:latest
        ports:
        - containerPort: 8080
        env:
        - name: AZURE_STORAGE_CONNECTION_STRING
          valueFrom:
            secretKeyRef:
              name: azure-secrets
              key: storage-connection-string
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: data-processor-service
spec:
  selector:
    app: data-processor
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

```bash
# Azure CLI commands
# Create AKS cluster
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 3 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster

# Deploy application
kubectl apply -f deployment.yaml

# Scale deployment
kubectl scale deployment data-processor --replicas=5

# Update deployment
kubectl set image deployment/data-processor processor=myregistry.azurecr.io/data-processor:v2
```

### 15. How do you implement Azure Functions for serverless data processing?

**Answer**: Azure Functions enable event-driven serverless computing:

```python
# Blob trigger function
import azure.functions as func
import pandas as pd
import json
from azure.storage.blob import BlobServiceClient

def main(myblob: func.InputStream, outputblob: func.Out[bytes]):
    # Process uploaded CSV file
    df = pd.read_csv(myblob)
    
    # Data transformations
    df['total_amount'] = df['quantity'] * df['unit_price']
    df['processed_date'] = pd.Timestamp.now()
    
    # Aggregate data
    summary = df.groupby('category').agg({
        'total_amount': ['sum', 'mean', 'count'],
        'quantity': 'sum'
    }).round(2)
    
    # Convert to JSON
    result = {
        'summary': summary.to_dict(),
        'total_records': len(df),
        'processing_time': pd.Timestamp.now().isoformat()
    }
    
    # Output processed data
    outputblob.set(json.dumps(result).encode('utf-8'))

# HTTP trigger function
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Get request parameters
        table_name = req.params.get('table')
        start_date = req.params.get('start_date')
        end_date = req.params.get('end_date')
        
        # Connect to database
        import pyodbc
        conn_str = os.environ['SQL_CONNECTION_STRING']
        conn = pyodbc.connect(conn_str)
        
        # Execute query
        query = f"""
            SELECT COUNT(*) as record_count, 
                   SUM(amount) as total_amount,
                   AVG(amount) as avg_amount
            FROM {table_name}
            WHERE date_column BETWEEN ? AND ?
        """
        
        cursor = conn.cursor()
        cursor.execute(query, (start_date, end_date))
        result = cursor.fetchone()
        
        response_data = {
            'record_count': result[0],
            'total_amount': float(result[1]) if result[1] else 0,
            'avg_amount': float(result[2]) if result[2] else 0
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            mimetype="application/json"
        )
        
    except Exception as e:
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )

# Timer trigger function
def main(mytimer: func.TimerRequest) -> None:
    # Daily data processing job
    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    # Process daily batch
    process_daily_batch()
    
    logging.info('Daily processing completed')

def process_daily_batch():
    # Implementation for daily batch processing
    pass
```

### 16. How do you implement Azure Logic Apps for workflow automation?

**Answer**: Logic Apps provide serverless workflow automation:

```json
{
  "definition": {
    "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
    "triggers": {
      "When_a_blob_is_added_or_modified": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "name": "@parameters('$connections')['azureblob']['connectionId']"
            }
          },
          "method": "get",
          "path": "/datasets/default/triggers/batch/onupdatedfile",
          "queries": {
            "folderId": "data/incoming",
            "maxFileCount": 10
          }
        },
        "recurrence": {
          "frequency": "Minute",
          "interval": 5
        }
      }
    },
    "actions": {
      "Parse_JSON": {
        "type": "ParseJson",
        "inputs": {
          "content": "@triggerBody()",
          "schema": {
            "type": "object",
            "properties": {
              "Name": {"type": "string"},
              "Path": {"type": "string"}
            }
          }
        }
      },
      "HTTP_Trigger_Data_Factory": {
        "type": "Http",
        "inputs": {
          "method": "POST",
          "uri": "https://management.azure.com/subscriptions/@{parameters('subscriptionId')}/resourceGroups/@{parameters('resourceGroupName')}/providers/Microsoft.DataFactory/factories/@{parameters('dataFactoryName')}/pipelines/@{parameters('pipelineName')}/createRun",
          "headers": {
            "Authorization": "Bearer @{body('Get_Access_Token')['access_token']}"
          },
          "body": {
            "inputPath": "@{body('Parse_JSON')['Path']}",
            "fileName": "@{body('Parse_JSON')['Name']}"
          }
        }
      }
    }
  }
}
```

### 17. How do you implement Azure Service Bus for reliable messaging?

**Answer**: Service Bus provides enterprise messaging capabilities:

```python
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import json

class ServiceBusManager:
    def __init__(self, connection_string):
        self.client = ServiceBusClient.from_connection_string(connection_string)
    
    def send_message(self, queue_name, message_data):
        with self.client:
            sender = self.client.get_queue_sender(queue_name=queue_name)
            with sender:
                message = ServiceBusMessage(json.dumps(message_data))
                sender.send_messages(message)
    
    def receive_messages(self, queue_name, max_messages=10):
        with self.client:
            receiver = self.client.get_queue_receiver(queue_name=queue_name)
            with receiver:
                messages = receiver.receive_messages(max_message_count=max_messages)
                for message in messages:
                    print(f"Received: {message}")
                    receiver.complete_message(message)

# Usage
sb_manager = ServiceBusManager(connection_string)
sb_manager.send_message("data-processing-queue", {
    "file_path": "/data/sales.csv",
    "processing_type": "batch",
    "priority": "high"
})
```

### 18. How do you implement Azure API Management for API governance?

**Answer**: API Management provides comprehensive API lifecycle management:

```xml
<!-- API Management Policy -->
<policies>
    <inbound>
        <base />
        <rate-limit calls="100" renewal-period="60" />
        <quota calls="10000" renewal-period="604800" />
        <authentication-managed-identity resource="https://management.azure.com/" />
        <set-header name="X-Forwarded-For" exists-action="override">
            <value>@(context.Request.IpAddress)</value>
        </set-header>
        <validate-jwt header-name="Authorization" failed-validation-httpcode="401">
            <openid-config url="https://login.microsoftonline.com/{tenant-id}/v2.0/.well-known/openid_configuration" />
            <audiences>
                <audience>api://data-api</audience>
            </audiences>
        </validate-jwt>
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
        <set-header name="X-Response-Time" exists-action="override">
            <value>@(context.Elapsed.TotalMilliseconds)</value>
        </set-header>
    </outbound>
    <on-error>
        <base />
        <send-request mode="new" response-variable-name="errorlog" timeout="10" ignore-error="true">
            <set-url>https://logging-service.com/api/errors</set-url>
            <set-method>POST</set-method>
            <set-body>@{
                return new JObject(
                    new JProperty("timestamp", DateTime.UtcNow.ToString()),
                    new JProperty("error", context.LastError.Message),
                    new JProperty("api", context.Api.Name)
                ).ToString();
            }</set-body>
        </send-request>
    </on-error>
</policies>
```

### 19. How do you implement Azure DevOps for CI/CD pipelines?

**Answer**: Azure DevOps provides comprehensive DevOps capabilities:

```yaml
# azure-pipelines.yml
trigger:
- main

variables:
  azureSubscription: 'Azure-Subscription'
  resourceGroupName: 'data-engineering-rg'
  storageAccountName: 'dataengineeringstorage'

stages:
- stage: Build
  jobs:
  - job: BuildJob
    pool:
      vmImage: 'ubuntu-latest'
    steps:
    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.9'
    
    - script: |
        pip install -r requirements.txt
        python -m pytest tests/ --junitxml=test-results.xml
      displayName: 'Run Tests'
    
    - task: PublishTestResults@2
      inputs:
        testResultsFiles: 'test-results.xml'
        testRunTitle: 'Python Tests'
    
    - task: ArchiveFiles@2
      inputs:
        rootFolderOrFile: '$(Build.SourcesDirectory)'
        includeRootFolder: false
        archiveType: 'zip'
        archiveFile: '$(Build.ArtifactStagingDirectory)/$(Build.BuildId).zip'
    
    - task: PublishBuildArtifacts@1
      inputs:
        pathToPublish: '$(Build.ArtifactStagingDirectory)'
        artifactName: 'drop'

- stage: Deploy
  dependsOn: Build
  condition: succeeded()
  jobs:
  - deployment: DeployJob
    environment: 'production'
    pool:
      vmImage: 'ubuntu-latest'
    strategy:
      runOnce:
        deploy:
          steps:
          - task: AzureResourceManagerTemplateDeployment@3
            inputs:
              deploymentScope: 'Resource Group'
              azureResourceManagerConnection: '$(azureSubscription)'
              subscriptionId: '$(subscriptionId)'
              action: 'Create Or Update Resource Group'
              resourceGroupName: '$(resourceGroupName)'
              location: 'East US'
              templateLocation: 'Linked artifact'
              csmFile: 'infrastructure/main.json'
              csmParametersFile: 'infrastructure/parameters.json'
          
          - task: AzureFunctionApp@1
            inputs:
              azureSubscription: '$(azureSubscription)'
              appType: 'functionApp'
              appName: 'data-processing-functions'
              package: '$(Pipeline.Workspace)/drop/$(Build.BuildId).zip'
```

### 20. How do you implement Azure Monitor and Application Insights?

**Answer**: Comprehensive monitoring and observability:

```python
# Application Insights integration
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.tracer import Tracer
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(
    connection_string='InstrumentationKey=your-key'
))

# Configure tracing
tracer = Tracer(
    exporter=AzureExporter(
        connection_string='InstrumentationKey=your-key'
    ),
    sampler=ProbabilitySampler(1.0)
)

class DataProcessor:
    def __init__(self):
        self.logger = logger
        self.tracer = tracer
    
    def process_data(self, file_path):
        with self.tracer.span(name='process_data') as span:
            try:
                span.add_attribute('file_path', file_path)
                
                # Processing logic
                data = self.load_data(file_path)
                result = self.transform_data(data)
                self.save_data(result)
                
                # Log success
                self.logger.info(f'Successfully processed {file_path}', 
                               extra={'custom_dimensions': {'file_size': len(data)}})
                
                return result
                
            except Exception as e:
                span.add_attribute('error', str(e))
                self.logger.error(f'Failed to process {file_path}: {str(e)}')
                raise

# Custom metrics
from opencensus.stats import aggregation as aggregation_module
from opencensus.stats import measure as measure_module
from opencensus.stats import stats as stats_module
from opencensus.stats import view as view_module
from opencensus.ext.azure import metrics_exporter

# Create measures
processing_time_measure = measure_module.MeasureFloat(
    "processing_time", "Time taken to process data", "ms"
)

record_count_measure = measure_module.MeasureInt(
    "record_count", "Number of records processed", "1"
)

# Create views
processing_time_view = view_module.View(
    "processing_time_view",
    "Processing time distribution",
    [],
    processing_time_measure,
    aggregation_module.DistributionAggregation([0, 100, 500, 1000, 5000])
)

# Register views
stats = stats_module.stats
view_manager = stats.view_manager
stats_recorder = stats.stats_recorder

view_manager.register_view(processing_time_view)

# Export metrics
exporter = metrics_exporter.new_metrics_exporter(
    connection_string='InstrumentationKey=your-key'
)
view_manager.register_exporter(exporter)
```

### 21-59. Additional Azure Services Implementation:

### 21. Azure Key Vault secrets management
### 22. Azure Virtual Networks and security  
### 23. Azure Load Balancer and Traffic Manager
### 24. Azure Content Delivery Network (CDN)
### 25. Azure Cognitive Services
### 26. Azure Bot Services
### 27. Azure IoT Hub and IoT Central
### 28. Azure Digital Twins
### 29. Azure Time Series Insights
### 30. Azure Maps location services
### 31. Azure Blockchain Service
### 32. Azure Quantum computing
### 33. Azure Mixed Reality services
### 34. Azure Communication Services
### 35. Azure Static Web Apps
### 36. Azure Container Instances
### 37. Azure Container Registry
### 38. Azure Service Fabric
### 39. Azure Batch computing
### 40. Azure HPC (High Performance Computing)
### 41. Azure Site Recovery
### 42. Azure Backup services
### 43. Azure Migrate tools
### 44. Azure Database Migration Service
### 45. Azure Arc hybrid management
### 46. Azure Stack hybrid cloud
### 47. Azure Lighthouse multi-tenant management
### 48. Azure Blueprints governance
### 49. Azure Policy compliance
### 50. Azure Cost Management optimization
### 51. Azure Advisor recommendations
### 52. Azure Resource Manager templates
### 53. Azure Automation runbooks
### 54. Azure Update Management
### 55. Azure Inventory tracking
### 56. Azure Change Tracking
### 57. Azure Security Center
### 58. Azure Sentinel SIEM
### 59. Azure Information Protection
### 60. Azure Privileged Identity Management

## Advanced Level Questions (61-100)

### 61. How do you implement Azure Multi-Factor Authentication?

**Answer**: MFA provides additional security layers:

```python
# Conditional Access with MFA
from msal import ConfidentialClientApplication

app = ConfidentialClientApplication(
    client_id="your-client-id",
    client_credential="your-client-secret",
    authority="https://login.microsoftonline.com/your-tenant-id"
)

# Request token with MFA claim
result = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"],
    claims_challenge='{"access_token":{"acrs":{"essential":true,"values":["urn:microsoft:req:mfa"]}}}'
)
```

### 62. How do you implement Azure Conditional Access?

**Answer**: Conditional Access provides intelligent access control:

```json
{
  "displayName": "Data Engineering MFA Policy",
  "state": "enabled",
  "conditions": {
    "users": {
      "includeGroups": ["data-engineering-group"]
    },
    "applications": {
      "includeApplications": ["azure-storage", "azure-sql"]
    },
    "locations": {
      "excludeLocations": ["trusted-office-network"]
    },
    "deviceStates": {
      "includeStates": ["all"]
    }
  },
  "grantControls": {
    "operator": "AND",
    "builtInControls": ["mfa", "compliantDevice"]
  },
  "sessionControls": {
    "signInFrequency": {
      "value": 4,
      "type": "hours"
    }
  }
}
```

### 63. How do you implement Azure Identity Protection?

**Answer**: Identity Protection detects and responds to identity risks:

```python
# Microsoft Graph API for Identity Protection
import requests

def get_risky_users(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    url = 'https://graph.microsoft.com/v1.0/identityProtection/riskyUsers'
    response = requests.get(url, headers=headers)
    
    return response.json()

def configure_risk_policy():
    policy = {
        "displayName": "High Risk User Policy",
        "isEnabled": True,
        "conditions": {
            "userRiskLevels": ["high"],
            "users": {
                "includeUsers": ["all"]
            }
        },
        "controls": {
            "access": "block"
        }
    }
    return policy
```

### 64. How do you implement Azure B2B and B2C identity?

**Answer**: B2B/B2C enables external user management:

```python
# Azure AD B2C custom policy
from msal import PublicClientApplication

# B2C configuration
b2c_app = PublicClientApplication(
    client_id="b2c-client-id",
    authority="https://yourtenant.b2clogin.com/yourtenant.onmicrosoft.com/B2C_1_signin"
)

# Interactive login
result = b2c_app.acquire_token_interactive(
    scopes=["https://yourtenant.onmicrosoft.com/api/read"],
    prompt="select_account"
)

# B2B guest invitation
def invite_guest_user(email, display_name):
    invitation = {
        "invitedUserEmailAddress": email,
        "invitedUserDisplayName": display_name,
        "inviteRedirectUrl": "https://myapp.com/welcome",
        "sendInvitationMessage": True,
        "invitedUserMessageInfo": {
            "messageLanguage": "en-US",
            "customizedMessageBody": "Welcome to our data platform!"
        }
    }
    return invitation
```

### 65. How do you implement Azure ExpressRoute connectivity?

**Answer**: ExpressRoute provides dedicated private connectivity:

```bash
# Create ExpressRoute circuit
az network express-route create \
  --resource-group myResourceGroup \
  --name myExpressRouteCircuit \
  --location "East US" \
  --service-provider "Equinix" \
  --peering-location "Washington DC" \
  --bandwidth 100 \
  --sku-family MeteredData \
  --sku-tier Standard

# Configure BGP peering
az network express-route peering create \
  --resource-group myResourceGroup \
  --express-route-circuit-name myExpressRouteCircuit \
  --peering-type AzurePrivatePeering \
  --peer-asn 65000 \
  --primary-peer-subnet 192.168.1.0/30 \
  --secondary-peer-subnet 192.168.2.0/30 \
  --vlan-id 100
```

### 66-100. Additional Advanced Azure Topics:

### 66. Azure VPN Gateway implementation
### 67. Azure Firewall security configuration
### 68. Azure DDoS Protection setup
### 69. Azure Web Application Firewall
### 70. Azure Front Door global load balancing
### 71. Azure Application Gateway layer 7 load balancing
### 72. Azure DNS services and private zones
### 73. Azure Private Link secure connectivity
### 74. Azure Bastion secure remote access
### 75. Azure Network Watcher monitoring
### 76. Azure Traffic Analytics insights
### 77. Azure Network Security Groups rules
### 78. Azure Application Security Groups
### 79. Azure Disk Encryption implementation
### 80. Azure Storage encryption configuration
### 81. Azure Confidential Computing
### 82. Azure Dedicated Hosts isolation
### 83. Azure Spot Virtual Machines cost optimization
### 84. Azure Reserved Instances planning
### 85. Azure Hybrid Benefit licensing
### 86. Azure Enterprise Agreement management
### 87. Azure Cloud Solution Provider program
### 88. Azure Marketplace solutions deployment
### 89. Azure Partner Center management
### 90. Azure Well-Architected Framework principles
### 91. Azure Cloud Adoption Framework methodology
### 92. Azure Landing Zones design
### 93. Azure Enterprise-Scale architecture
### 94. Azure Multi-cloud strategies
### 95. Azure Edge computing solutions
### 96. Azure Sustainability initiatives
### 97. Azure Compliance certifications
### 98. Azure Future roadmap planning
### 99. Azure Innovation and emerging technologies
### 100. Azure Best Practices and Optimization strategies

**Advanced Azure Architecture Example:**
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "environmentName": {
      "type": "string",
      "allowedValues": ["dev", "staging", "prod"]
    }
  },
  "variables": {
    "resourcePrefix": "[concat('dataeng-', parameters('environmentName'))]" 
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2021-04-01",
      "name": "[concat(variables('resourcePrefix'), 'storage')]",
      "location": "[resourceGroup().location]",
      "sku": {
        "name": "Standard_LRS"
      },
      "kind": "StorageV2",
      "properties": {
        "isHnsEnabled": true,
        "encryption": {
          "services": {
            "blob": {"enabled": true},
            "file": {"enabled": true}
          },
          "keySource": "Microsoft.Storage"
        },
        "networkAcls": {
          "defaultAction": "Deny",
          "virtualNetworkRules": [
            {
              "id": "[resourceId('Microsoft.Network/virtualNetworks/subnets', 'vnet', 'data-subnet')]",
              "action": "Allow"
            }
          ]
        }
      }
    }
  ]
}
```

---

## 📚 **Azure Study Guide & Best Practices**

### 🎯 **Essential Azure Concepts for Data Engineers**

#### **Core Services Priority**
1. **Storage**: Blob Storage, Data Lake Storage Gen2, SQL Database
2. **Compute**: Virtual Machines, Functions, Databricks, Synapse
3. **Analytics**: Data Factory, Stream Analytics, Power BI
4. **Security**: Key Vault, Active Directory, RBAC
5. **Monitoring**: Monitor, Application Insights, Log Analytics

#### **Architecture Patterns**
1. **Data Lake Architecture**: Raw → Processed → Curated
2. **Lambda Architecture**: Batch + Stream processing
3. **Microservices**: AKS + API Management + Service Bus
4. **Serverless**: Functions + Logic Apps + Event Grid
5. **Hybrid**: Arc + Stack + ExpressRoute

### 🚀 **Best Practices**

#### **Security**
- Use managed identities instead of connection strings
- Implement least privilege access with RBAC
- Enable encryption at rest and in transit
- Use Key Vault for secrets management
- Implement network security with NSGs and firewalls

#### **Cost Optimization**
- Use reserved instances for predictable workloads
- Implement auto-scaling for variable workloads
- Use spot instances for fault-tolerant workloads
- Implement lifecycle management for storage
- Monitor costs with budgets and alerts

#### **Performance**
- Choose appropriate service tiers
- Implement caching strategies
- Use CDN for global content delivery
- Optimize database queries and indexing
- Implement connection pooling

### 🔗 **Essential Resources**

- **Azure Architecture Center**: Best practices and reference architectures
- **Azure Well-Architected Framework**: Design principles and guidelines
- **Azure Documentation**: Comprehensive service documentation
- **Microsoft Learn**: Free learning paths and modules
- **Azure Samples**: Code samples and quickstarts

This comprehensive collection of 100 Azure interview questions covers all major services and concepts essential for data engineering roles, from basic storage and compute to advanced analytics, AI services, security, networking, and enterprise architecture patterns.