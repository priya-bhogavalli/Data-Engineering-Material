# Azure Key Concepts for Data Engineering

## 1. Azure Data Services Overview
**Core Data Services**:
- **Azure Data Factory**: ETL/ELT orchestration
- **Azure Synapse Analytics**: Data warehouse and analytics
- **Azure Data Lake Storage**: Scalable data lake
- **Azure Databricks**: Apache Spark analytics platform
- **Azure Stream Analytics**: Real-time stream processing
- **Azure Cosmos DB**: Multi-model NoSQL database

```python
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

# Azure authentication
credential = DefaultAzureCredential()
blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)
```

## 2. Azure Data Factory
```json
{
  "name": "CopyDataPipeline",
  "properties": {
    "activities": [
      {
        "name": "CopyFromSQLToBlob",
        "type": "Copy",
        "inputs": [
          {
            "referenceName": "SqlServerDataset",
            "type": "DatasetReference"
          }
        ],
        "outputs": [
          {
            "referenceName": "BlobDataset",
            "type": "DatasetReference"
          }
        ],
        "typeProperties": {
          "source": {
            "type": "SqlSource",
            "sqlReaderQuery": "SELECT * FROM Sales WHERE ModifiedDate >= '@{formatDateTime(pipeline().parameters.windowStart, 'yyyy-MM-dd')}'"
          },
          "sink": {
            "type": "BlobSink",
            "blobWriterOverwriteFiles": true
          }
        }
      }
    ],
    "parameters": {
      "windowStart": {
        "type": "String"
      }
    }
  }
}

// Data Factory REST API
POST https://management.azure.com/subscriptions/{subscription-id}/resourceGroups/{resource-group}/providers/Microsoft.DataFactory/factories/{factory-name}/pipelines/{pipeline-name}/createRun?api-version=2018-06-01
```

```python
# Azure Data Factory SDK
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *

# Create pipeline run
adf_client = DataFactoryManagementClient(credential, subscription_id)

run_response = adf_client.pipeline_runs.create_run(
    resource_group_name="myResourceGroup",
    factory_name="myDataFactory",
    pipeline_name="CopyDataPipeline",
    parameters={"windowStart": "2024-01-15"}
)

print(f"Pipeline run ID: {run_response.run_id}")
```

## 3. Azure Synapse Analytics
```sql
-- Create dedicated SQL pool
CREATE DATABASE SynapseDataWarehouse
(
    EDITION = 'DataWarehouse',
    SERVICE_OBJECTIVE = 'DW100c'
);

-- Create external data source
CREATE EXTERNAL DATA SOURCE AzureDataLakeStore
WITH (
    TYPE = HADOOP,
    LOCATION = 'abfss://container@storageaccount.dfs.core.windows.net',
    CREDENTIAL = AzureStorageCredential
);

-- Create external file format
CREATE EXTERNAL FILE FORMAT ParquetFileFormat
WITH (
    FORMAT_TYPE = PARQUET,
    DATA_COMPRESSION = 'org.apache.hadoop.io.compress.SnappyCodec'
);

-- Create external table
CREATE EXTERNAL TABLE ext_sales (
    SaleID INT,
    CustomerID INT,
    ProductID INT,
    SaleDate DATE,
    Amount DECIMAL(10,2)
)
WITH (
    LOCATION = '/sales/',
    DATA_SOURCE = AzureDataLakeStore,
    FILE_FORMAT = ParquetFileFormat
);

-- CTAS (Create Table As Select)
CREATE TABLE sales_summary
WITH (
    DISTRIBUTION = HASH(CustomerID),
    CLUSTERED COLUMNSTORE INDEX
)
AS
SELECT 
    CustomerID,
    YEAR(SaleDate) as SaleYear,
    SUM(Amount) as TotalSales,
    COUNT(*) as TransactionCount
FROM ext_sales
GROUP BY CustomerID, YEAR(SaleDate);

-- Workload management
CREATE WORKLOAD GROUP DataEngineering
WITH (
    MIN_PERCENTAGE_RESOURCE = 25,
    CAP_PERCENTAGE_RESOURCE = 50,
    REQUEST_MIN_RESOURCE_GRANT_PERCENT = 3
);

CREATE WORKLOAD CLASSIFIER ETLClassifier
WITH (
    WORKLOAD_GROUP = 'DataEngineering',
    MEMBERNAME = 'ETLUser'
);
```

## 4. Azure Data Lake Storage
```python
from azure.storage.filedatalake import DataLakeServiceClient

# Initialize Data Lake client
service_client = DataLakeServiceClient(
    account_url="https://mydatalake.dfs.core.windows.net",
    credential=credential
)

# Create file system (container)
file_system_client = service_client.create_file_system("raw-data")

# Upload file
with open("sales_data.csv", "rb") as data:
    file_client = file_system_client.create_file("sales/2024/01/sales_data.csv")
    file_client.upload_data(data, overwrite=True)

# Set metadata and properties
file_client.set_metadata({"source": "sales_system", "format": "csv"})

# List files with hierarchy
paths = file_system_client.get_paths(path="sales", recursive=True)
for path in paths:
    print(f"Path: {path.name}, Size: {path.content_length}")

# Download file
download = file_client.download_file()
downloaded_bytes = download.readall()

# Set up lifecycle management
from azure.storage.blob import BlobServiceClient, StandardBlobTier

blob_service = BlobServiceClient(
    account_url="https://mystorageaccount.blob.core.windows.net",
    credential=credential
)

# Move to cool tier after 30 days
blob_client = blob_service.get_blob_client("container", "blob_name")
blob_client.set_standard_blob_tier(StandardBlobTier.Cool)
```

## 5. Azure Databricks
```python
# Databricks notebook cell
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

# Initialize Spark session
spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

# Read from Azure Data Lake
df = spark.read.format("delta").load("abfss://container@storage.dfs.core.windows.net/delta/sales")

# Data transformation
transformed_df = df \
    .filter(col("amount") > 0) \
    .withColumn("year", year(col("sale_date"))) \
    .withColumn("month", month(col("sale_date"))) \
    .groupBy("year", "month", "product_category") \
    .agg(
        sum("amount").alias("total_sales"),
        count("*").alias("transaction_count"),
        avg("amount").alias("avg_transaction")
    )

# Write to Delta Lake
transformed_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save("abfss://container@storage.dfs.core.windows.net/delta/sales_summary")

# Create Delta table
spark.sql("""
    CREATE TABLE sales_summary
    USING DELTA
    LOCATION 'abfss://container@storage.dfs.core.windows.net/delta/sales_summary'
""")

# Optimize Delta table
spark.sql("OPTIMIZE sales_summary ZORDER BY (year, month)")
```

```scala
// Scala notebook cell
import org.apache.spark.sql.functions._
import io.delta.tables._

// Read streaming data
val streamingDF = spark
  .readStream
  .format("eventhubs")
  .options(Map(
    "eventhubs.connectionString" -> "Endpoint=sb://...",
    "eventhubs.consumerGroup" -> "$Default"
  ))
  .load()

// Process streaming data
val processedStream = streamingDF
  .select(from_json(col("body").cast("string"), schema).as("data"))
  .select("data.*")
  .withColumn("processing_time", current_timestamp())

// Write to Delta table
val query = processedStream
  .writeStream
  .format("delta")
  .outputMode("append")
  .option("checkpointLocation", "/mnt/delta/checkpoints/events")
  .table("events")

query.start()
```

## 6. Azure Stream Analytics
```sql
-- Stream Analytics Query Language
WITH SalesAggregates AS (
    SELECT
        ProductCategory,
        System.Timestamp() AS WindowEnd,
        SUM(Amount) AS TotalSales,
        COUNT(*) AS TransactionCount,
        AVG(Amount) AS AvgTransactionValue
    FROM SalesInputStream TIMESTAMP BY EventTime
    GROUP BY ProductCategory, TumblingWindow(minute, 5)
)

SELECT
    ProductCategory,
    WindowEnd,
    TotalSales,
    TransactionCount,
    AvgTransactionValue,
    CASE 
        WHEN TotalSales > 10000 THEN 'High'
        WHEN TotalSales > 5000 THEN 'Medium'
        ELSE 'Low'
    END AS SalesVolume
INTO SalesOutput
FROM SalesAggregates;

-- Anomaly detection
SELECT
    ProductID,
    Amount,
    AnomalyDetection_SpikeAndDip(Amount, 95, 120, 'spikesanddips') 
        OVER(LIMIT DURATION(second, 120)) AS SpikeAndDipScores
INTO AnomalyOutput
FROM SalesInputStream TIMESTAMP BY EventTime;

-- Reference data join
SELECT
    s.CustomerID,
    s.Amount,
    r.CustomerTier,
    r.Region
INTO EnrichedSalesOutput
FROM SalesInputStream s TIMESTAMP BY EventTime
JOIN CustomerReferenceData r
ON s.CustomerID = r.CustomerID;
```

## 7. Azure Cosmos DB
```python
from azure.cosmos import CosmosClient, PartitionKey

# Initialize Cosmos client
client = CosmosClient("https://mycosmosdb.documents.azure.com:443/", credential)

# Create database and container
database = client.create_database_if_not_exists("SalesDB")
container = database.create_container_if_not_exists(
    id="Sales",
    partition_key=PartitionKey(path="/customerId"),
    offer_throughput=400
)

# Insert document
sales_record = {
    "id": "sale_001",
    "customerId": "CUST_123",
    "productId": "PROD_456",
    "amount": 299.99,
    "saleDate": "2024-01-15T10:30:00Z",
    "region": "US-West"
}

container.create_item(sales_record)

# Query documents
query = "SELECT * FROM c WHERE c.customerId = @customerId AND c.amount > @minAmount"
parameters = [
    {"name": "@customerId", "value": "CUST_123"},
    {"name": "@minAmount", "value": 100}
]

items = list(container.query_items(
    query=query,
    parameters=parameters,
    enable_cross_partition_query=True
))

# Bulk operations
import asyncio
from azure.cosmos.aio import CosmosClient as AsyncCosmosClient

async def bulk_insert():
    async with AsyncCosmosClient("https://mycosmosdb.documents.azure.com:443/", credential) as client:
        database = client.get_database_client("SalesDB")
        container = database.get_container_client("Sales")
        
        operations = []
        for i in range(1000):
            operations.append(("create", {
                "id": f"sale_{i}",
                "customerId": f"CUST_{i % 100}",
                "amount": 100 + i
            }))
        
        await container.execute_item_batch(operations)

# Change feed processing
def process_change_feed():
    change_feed_iter = container.query_items_change_feed(
        start_time="Beginning"
    )
    
    for change in change_feed_iter:
        for item in change:
            print(f"Changed item: {item}")
```

## 8. Azure Event Hubs
```python
from azure.eventhub import EventHubProducerClient, EventData
from azure.eventhub.aio import EventHubConsumerClient

# Producer
async def send_events():
    producer = EventHubProducerClient.from_connection_string(
        conn_str="Endpoint=sb://...",
        eventhub_name="sales-events"
    )
    
    async with producer:
        event_data_batch = await producer.create_batch()
        
        for i in range(100):
            event_data = EventData(f'{{"id": {i}, "amount": {100 + i}}}')
            event_data_batch.add(event_data)
        
        await producer.send_batch(event_data_batch)

# Consumer
async def process_events(partition_context, event):
    print(f"Received event: {event.body_as_str()}")
    await partition_context.update_checkpoint(event)

async def consume_events():
    consumer = EventHubConsumerClient.from_connection_string(
        conn_str="Endpoint=sb://...",
        consumer_group="$Default",
        eventhub_name="sales-events"
    )
    
    async with consumer:
        await consumer.receive(
            on_event=process_events,
            starting_position="-1"  # Start from beginning
        )

# Event Hubs Capture to Data Lake
# Configured through Azure portal or ARM template
```

## 9. Azure Machine Learning
```python
from azureml.core import Workspace, Dataset, Experiment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.pipeline.core import Pipeline, PipelineData
from azureml.pipeline.steps import PythonScriptStep

# Connect to workspace
ws = Workspace.from_config()

# Create dataset
datastore = ws.get_default_datastore()
dataset = Dataset.Tabular.from_delimited_files(
    path=(datastore, 'sales_data/*.csv')
)

# Create compute target
compute_config = AmlCompute.provisioning_configuration(
    vm_size="Standard_D2_v2",
    min_nodes=0,
    max_nodes=4
)

compute_target = ComputeTarget.create(ws, "aml-compute", compute_config)

# Create pipeline step
data_prep_step = PythonScriptStep(
    script_name="data_prep.py",
    arguments=["--input-data", dataset.as_named_input("raw_data")],
    outputs=[PipelineData("prepared_data", datastore=datastore)],
    compute_target=compute_target,
    source_directory="./scripts"
)

# Create and run pipeline
pipeline = Pipeline(workspace=ws, steps=[data_prep_step])
experiment = Experiment(ws, "data-pipeline")
pipeline_run = experiment.submit(pipeline)
```

## 10. Security and Governance
```python
# Azure Key Vault integration
from azure.keyvault.secrets import SecretClient

key_vault_client = SecretClient(
    vault_url="https://myvault.vault.azure.net/",
    credential=credential
)

# Store secret
key_vault_client.set_secret("database-connection-string", "Server=...")

# Retrieve secret
secret = key_vault_client.get_secret("database-connection-string")
connection_string = secret.value

# Azure Purview for data governance
from azure.purview.catalog import PurviewCatalogClient

purview_client = PurviewCatalogClient(
    endpoint="https://mypurview.purview.azure.com",
    credential=credential
)

# Create data asset
asset = {
    "entity": {
        "typeName": "DataSet",
        "attributes": {
            "name": "sales_data",
            "qualifiedName": "sales_data@cluster1",
            "description": "Daily sales transaction data"
        }
    }
}

purview_client.entity.create_or_update(entity=asset)

# Azure Policy for compliance
policy_definition = {
    "properties": {
        "displayName": "Require encryption for storage accounts",
        "policyType": "Custom",
        "mode": "All",
        "description": "Ensures storage accounts have encryption enabled",
        "policyRule": {
            "if": {
                "allOf": [
                    {"field": "type", "equals": "Microsoft.Storage/storageAccounts"},
                    {"field": "Microsoft.Storage/storageAccounts/encryption.services.blob.enabled", "notEquals": "true"}
                ]
            },
            "then": {"effect": "deny"}
        }
    }
}

# Role-based access control
from azure.mgmt.authorization import AuthorizationManagementClient

auth_client = AuthorizationManagementClient(credential, subscription_id)

# Assign role
role_assignment = {
    "properties": {
        "roleDefinitionId": f"/subscriptions/{subscription_id}/providers/Microsoft.Authorization/roleDefinitions/ba92f5b4-2d11-453d-a403-e96b0029c9fe",  # Storage Blob Data Contributor
        "principalId": "user-object-id"
    }
}

auth_client.role_assignments.create(
    scope=f"/subscriptions/{subscription_id}/resourceGroups/myResourceGroup",
    role_assignment_name="unique-guid",
    parameters=role_assignment
)
```