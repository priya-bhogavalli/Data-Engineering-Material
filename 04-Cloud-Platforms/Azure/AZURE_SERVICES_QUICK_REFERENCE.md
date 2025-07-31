# Azure Services Quick Reference for Data Engineers

## Storage Services

### Azure Blob Storage
**Use Case**: Object storage for data lakes
```bash
# Azure CLI Commands
az storage blob upload --account-name mystorageaccount --container-name data --name file.csv --file local_file.csv
az storage blob list --account-name mystorageaccount --container-name data
az storage blob download --account-name mystorageaccount --container-name data --name file.csv --file downloaded_file.csv
```

### Azure Data Lake Storage Gen2
**Use Case**: Big data analytics storage
```python
from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
service_client = DataLakeServiceClient(
    account_url="https://mystorageaccount.dfs.core.windows.net",
    credential=credential
)

file_system_client = service_client.get_file_system_client("data")
file_client = file_system_client.get_file_client("path/to/file.csv")
file_client.upload_data("Hello World", overwrite=True)
```

## Compute Services

### Azure Virtual Machines
**Use Case**: Custom compute instances
```bash
# Create VM
az vm create --resource-group myResourceGroup --name myVM --image UbuntuLTS --admin-username azureuser --generate-ssh-keys
# Start/Stop VM
az vm start --resource-group myResourceGroup --name myVM
az vm stop --resource-group myResourceGroup --name myVM
```

### Azure Functions
**Use Case**: Serverless compute
```python
import azure.functions as func
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    return func.HttpResponse("Hello World!")
```

### Azure Databricks
**Use Case**: Apache Spark analytics
```python
# Databricks notebook cell
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

df = spark.read.format("csv").option("header", "true").load("/mnt/data/input.csv")
df.groupBy("category").count().write.mode("overwrite").parquet("/mnt/data/output")
```

## Database Services

### Azure SQL Database
**Use Case**: Managed SQL database
```sql
-- Create database
CREATE DATABASE mydatabase;

-- Create table
CREATE TABLE sales (
    id INT IDENTITY(1,1) PRIMARY KEY,
    amount DECIMAL(10,2),
    sale_date DATE
);

-- Insert data
INSERT INTO sales (amount, sale_date) VALUES (100.50, '2024-01-01');
```

### Azure Cosmos DB
**Use Case**: Multi-model NoSQL database
```python
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = CosmosClient("https://mycosmosaccount.documents.azure.com:443/", credential)

database = client.get_database_client("mydatabase")
container = database.get_container_client("mycontainer")

# Insert document
container.create_item({"id": "1", "name": "John", "age": 30})

# Query documents
items = list(container.query_items("SELECT * FROM c WHERE c.age > 25"))
```

### Azure Synapse Analytics
**Use Case**: Data warehouse
```sql
-- Create external table
CREATE EXTERNAL TABLE sales_external (
    id INT,
    amount DECIMAL(10,2),
    sale_date DATE
)
WITH (
    LOCATION = 'sales/',
    DATA_SOURCE = external_data_source,
    FILE_FORMAT = parquet_file_format
);

-- Create materialized view
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    YEAR(sale_date) as year,
    MONTH(sale_date) as month,
    SUM(amount) as total_sales
FROM sales_external
GROUP BY YEAR(sale_date), MONTH(sale_date);
```

## Analytics Services

### Azure Data Factory
**Use Case**: ETL/ELT orchestration
```json
{
  "name": "CopyPipeline",
  "properties": {
    "activities": [
      {
        "name": "CopyData",
        "type": "Copy",
        "inputs": [{"referenceName": "SourceDataset", "type": "DatasetReference"}],
        "outputs": [{"referenceName": "SinkDataset", "type": "DatasetReference"}],
        "typeProperties": {
          "source": {"type": "BlobSource"},
          "sink": {"type": "SqlSink"}
        }
      }
    ]
  }
}
```

### Azure Stream Analytics
**Use Case**: Real-time stream processing
```sql
-- Stream Analytics Query
SELECT 
    userId,
    COUNT(*) as eventCount,
    AVG(value) as avgValue,
    System.Timestamp() as windowEnd
FROM EventHub
GROUP BY userId, TumblingWindow(minute, 5)
```

### Azure Event Hubs
**Use Case**: Big data streaming
```python
from azure.eventhub import EventHubProducerClient, EventData

producer = EventHubProducerClient.from_connection_string(
    conn_str="Endpoint=sb://...",
    eventhub_name="events"
)

event_data_batch = producer.create_batch()
event_data_batch.add(EventData('{"user": "john", "action": "click"}'))
producer.send_batch(event_data_batch)
```

## Machine Learning Services

### Azure Machine Learning
**Use Case**: ML platform
```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential

ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="subscription-id",
    resource_group_name="resource-group",
    workspace_name="workspace"
)

# Submit training job
from azure.ai.ml import command
job = command(
    inputs={"training_data": "azureml:my-dataset:1"},
    code="./src",
    command="python train.py --data ${{inputs.training_data}}",
    environment="azureml:sklearn-env:1",
    compute="cpu-cluster"
)

ml_client.create_or_update(job)
```

### Azure Cognitive Services
**Use Case**: AI services
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

# Analyze image
analyze_results = computervision_client.analyze_image(image_url, visual_features=['Categories', 'Description'])
```

## Security Services

### Azure Key Vault
**Use Case**: Secrets management
```python
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)

# Set secret
client.set_secret("database-password", "mypassword")

# Get secret
secret = client.get_secret("database-password")
print(secret.value)
```

### Azure Active Directory
**Use Case**: Identity and access management
```bash
# Create service principal
az ad sp create-for-rbac --name myServicePrincipal --role contributor --scopes /subscriptions/subscription-id

# Assign role
az role assignment create --assignee user@company.com --role "Storage Blob Data Contributor" --scope /subscriptions/subscription-id
```

## Monitoring Services

### Azure Monitor
**Use Case**: Monitoring and alerting
```python
from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = LogsQueryClient(credential)

# Query logs
response = client.query_workspace(
    workspace_id="workspace-id",
    query="AzureActivity | where TimeGenerated > ago(1h) | limit 10"
)

for table in response.tables:
    for row in table.rows:
        print(row)
```

### Application Insights
**Use Case**: Application monitoring
```python
from applicationinsights import TelemetryClient

tc = TelemetryClient('instrumentation-key')
tc.track_event('Custom Event', {'property': 'value'})
tc.track_metric('Custom Metric', 42)
tc.flush()
```

## Networking Services

### Azure Virtual Network
**Use Case**: Network isolation
```bash
# Create VNet
az network vnet create --resource-group myResourceGroup --name myVNet --address-prefix 10.0.0.0/16

# Create subnet
az network vnet subnet create --resource-group myResourceGroup --vnet-name myVNet --name mySubnet --address-prefix 10.0.1.0/24
```

### Azure Private Link
**Use Case**: Private connectivity
```bash
# Create private endpoint
az network private-endpoint create --resource-group myResourceGroup --name myPrivateEndpoint --vnet-name myVNet --subnet mySubnet --private-connection-resource-id /subscriptions/subscription-id/resourceGroups/myResourceGroup/providers/Microsoft.Storage/storageAccounts/mystorageaccount --connection-name myConnection --group-ids blob
```

## Management Services

### Azure Resource Manager
**Use Case**: Infrastructure as code
```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2021-04-01",
      "name": "mystorageaccount",
      "location": "[resourceGroup().location]",
      "sku": {
        "name": "Standard_LRS"
      },
      "kind": "StorageV2"
    }
  ]
}
```

### Azure DevOps
**Use Case**: CI/CD pipelines
```yaml
# azure-pipelines.yml
trigger:
- main

pool:
  vmImage: 'ubuntu-latest'

steps:
- task: AzureCLI@2
  inputs:
    azureSubscription: 'myServiceConnection'
    scriptType: 'bash'
    scriptLocation: 'inlineScript'
    inlineScript: |
      az storage blob upload --account-name mystorageaccount --container-name data --name file.csv --file data.csv
```

## Cost Management

### Azure Cost Management
**Use Case**: Cost monitoring and optimization
```bash
# Get cost data
az consumption usage list --top 10

# Create budget
az consumption budget create --budget-name myBudget --amount 1000 --time-grain Monthly --start-date 2024-01-01 --end-date 2024-12-31
```

## Common CLI Commands

### Resource Management
```bash
# List resources
az resource list --resource-group myResourceGroup

# Create resource group
az group create --name myResourceGroup --location eastus

# Delete resource group
az group delete --name myResourceGroup --yes --no-wait
```

### Authentication
```bash
# Login
az login

# Set subscription
az account set --subscription "subscription-id"

# Show current account
az account show
```

### Storage Operations
```bash
# Create storage account
az storage account create --name mystorageaccount --resource-group myResourceGroup --location eastus --sku Standard_LRS

# Create container
az storage container create --name data --account-name mystorageaccount

# Upload file
az storage blob upload --account-name mystorageaccount --container-name data --name file.csv --file local_file.csv
```

## Best Practices

### Security
- Use Azure AD for authentication
- Store secrets in Key Vault
- Implement network security groups
- Enable encryption at rest and in transit
- Use managed identities

### Cost Optimization
- Use reserved instances for predictable workloads
- Implement auto-scaling
- Set up cost alerts and budgets
- Use appropriate storage tiers
- Monitor and optimize resource usage

### Performance
- Choose appropriate service tiers
- Use caching strategies
- Implement CDN for global distribution
- Monitor performance metrics
- Optimize database queries

### Reliability
- Design for high availability
- Implement backup and disaster recovery
- Use availability zones
- Monitor health and set up alerts
- Test failover procedures