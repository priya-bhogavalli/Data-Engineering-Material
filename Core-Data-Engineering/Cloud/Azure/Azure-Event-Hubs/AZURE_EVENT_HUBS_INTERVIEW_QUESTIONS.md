# Azure Event Hubs Interview Questions

## 📋 Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Architecture & Components](#architecture--components)
3. [Event Processing](#event-processing)
4. [Partitioning & Scaling](#partitioning--scaling)
5. [Security & Access Control](#security--access-control)
6. [Integration & SDKs](#integration--sdks)
7. [Monitoring & Management](#monitoring--management)
8. [Performance & Optimization](#performance--optimization)
9. [Best Practices](#best-practices)
10. [Scenario-Based Questions](#scenario-based-questions)

---

## Basic Concepts

### Q1: What is Azure Event Hubs and what problems does it solve?
**Answer:**
Azure Event Hubs is a fully managed, real-time data ingestion service that can receive and process millions of events per second.

**Key Problems Solved:**
- **High-Volume Ingestion**: Handle millions of events per second
- **Real-time Processing**: Low-latency event streaming
- **Scalability**: Auto-scale based on throughput needs
- **Integration**: Connect with Azure ecosystem services
- **Reliability**: Built-in redundancy and disaster recovery

**Core Features:**
- Massive scale event ingestion
- Multiple consumer groups
- Event retention and replay
- Integration with Azure services
- Apache Kafka compatibility
- Capture to storage accounts

### Q2: How does Event Hubs differ from other messaging services?
**Answer:**
**vs Service Bus:**
- Event Hubs: High-throughput streaming, simple pub-sub
- Service Bus: Enterprise messaging, complex routing, transactions

**vs Storage Queues:**
- Event Hubs: Real-time streaming, multiple consumers
- Storage Queues: Simple queuing, single consumer

**vs Apache Kafka:**
- Event Hubs: Managed service, Azure integration
- Kafka: Self-managed, more configuration options

---

## Architecture & Components

### Q3: What are the core components of Event Hubs architecture?
**Answer:**
**Core Components:**
- **Event Hub**: Container for event streams
- **Partitions**: Ordered sequence of events
- **Consumer Groups**: Independent views of event stream
- **Throughput Units**: Capacity units for ingress/egress
- **Event Processors**: Applications that consume events
- **Checkpoints**: Track processing progress

**Architecture Flow:**
```
Event Producers → Event Hub → Partitions → Consumer Groups → Event Processors
```

### Q4: How do partitions work in Event Hubs?
**Answer:**
**Partition Characteristics:**
- **Ordered Sequence**: Events within partition are ordered
- **Partition Key**: Determines which partition receives event
- **Parallel Processing**: Each partition can be consumed independently
- **Retention**: Events retained for configured period
- **Scaling**: More partitions = higher throughput

**Partition Strategy:**
```python
# Partition key examples
partition_key = user_id  # Events from same user go to same partition
partition_key = device_id  # Events from same device stay ordered
partition_key = region  # Geographic partitioning
```

---

## Event Processing

### Q5: How do you send events to Event Hubs?
**Answer:**
**Using Azure SDK:**
```python
from azure.eventhub import EventHubProducerClient, EventData

# Create producer client
producer = EventHubProducerClient.from_connection_string(
    conn_str="Endpoint=sb://...",
    eventhub_name="my-event-hub"
)

# Send single event
event_data = EventData("Hello World")
with producer:
    producer.send_batch([event_data])

# Send batch with partition key
batch = producer.create_batch(partition_key="user123")
batch.add(EventData("Event 1"))
batch.add(EventData("Event 2"))
with producer:
    producer.send_batch(batch)
```

### Q6: How do you consume events from Event Hubs?
**Answer:**
**Event Consumer Example:**
```python
from azure.eventhub import EventHubConsumerClient

def on_event(partition_context, event):
    print(f"Received event: {event.body_as_str()}")
    print(f"Partition: {partition_context.partition_id}")
    print(f"Offset: {event.offset}")
    
    # Update checkpoint
    partition_context.update_checkpoint(event)

# Create consumer client
consumer = EventHubConsumerClient.from_connection_string(
    conn_str="Endpoint=sb://...",
    consumer_group="$Default",
    eventhub_name="my-event-hub"
)

# Start consuming
with consumer:
    consumer.receive(on_event=on_event, starting_position="-1")
```

---

## Partitioning & Scaling

### Q7: How do you scale Event Hubs?
**Answer:**
**Scaling Mechanisms:**
- **Throughput Units (TUs)**: Standard tier scaling
- **Processing Units (PUs)**: Dedicated tier scaling
- **Auto-Inflate**: Automatic TU scaling
- **Partition Count**: Fixed at creation time

**Scaling Configuration:**
```json
{
  "throughputUnits": 10,
  "autoInflateEnabled": true,
  "maximumThroughputUnits": 20,
  "partitionCount": 32
}
```

**Scaling Best Practices:**
- Plan partition count for future growth
- Use auto-inflate for variable workloads
- Monitor throughput metrics
- Consider dedicated clusters for high volume

### Q8: What are consumer groups and how do they work?
**Answer:**
**Consumer Group Concepts:**
- **Independent Views**: Each group sees all events
- **Parallel Processing**: Multiple consumers per group
- **Checkpointing**: Track progress per group
- **Isolation**: Groups don't affect each other

**Consumer Group Usage:**
```python
# Different consumer groups for different purposes
analytics_consumer = EventHubConsumerClient.from_connection_string(
    conn_str="...",
    consumer_group="analytics",
    eventhub_name="events"
)

alerts_consumer = EventHubConsumerClient.from_connection_string(
    conn_str="...",
    consumer_group="alerts", 
    eventhub_name="events"
)
```

---

## Security & Access Control

### Q9: How do you secure Event Hubs?
**Answer:**
**Security Features:**
- **Shared Access Signatures (SAS)**: Token-based access
- **Azure Active Directory**: Identity-based authentication
- **IP Filtering**: Network-level restrictions
- **Virtual Networks**: Private connectivity
- **Encryption**: At rest and in transit

**Authentication Examples:**
```python
# SAS token authentication
from azure.eventhub import EventHubProducerClient

producer = EventHubProducerClient.from_connection_string(
    "Endpoint=sb://namespace.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=..."
)

# Azure AD authentication
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
producer = EventHubProducerClient(
    fully_qualified_namespace="namespace.servicebus.windows.net",
    eventhub_name="my-hub",
    credential=credential
)
```

### Q10: How do you implement access control policies?
**Answer:**
**Access Control Levels:**
- **Namespace Level**: Control access to entire namespace
- **Event Hub Level**: Control access to specific hub
- **Consumer Group Level**: Control consumer access

**Policy Configuration:**
```json
{
  "accessPolicies": [
    {
      "name": "SendPolicy",
      "rights": ["Send"],
      "primaryKey": "...",
      "secondaryKey": "..."
    },
    {
      "name": "ListenPolicy", 
      "rights": ["Listen"],
      "primaryKey": "...",
      "secondaryKey": "..."
    }
  ]
}
```

---

## Integration & SDKs

### Q11: How does Event Hubs integrate with other Azure services?
**Answer:**
**Common Integrations:**
- **Azure Functions**: Event-driven processing
- **Stream Analytics**: Real-time analytics
- **Logic Apps**: Workflow automation
- **Azure Storage**: Event capture and archival
- **Power BI**: Real-time dashboards
- **Azure Synapse**: Data warehousing

**Azure Functions Integration:**
```python
import azure.functions as func

def main(events: func.EventHubEvent):
    for event in events:
        logging.info(f'Event Hub trigger: {event.get_body().decode()}')
        
        # Process event
        data = json.loads(event.get_body().decode())
        process_telemetry_data(data)
```

### Q12: How do you use Event Hubs Capture?
**Answer:**
**Capture Configuration:**
```json
{
  "capture": {
    "enabled": true,
    "encoding": "Avro",
    "intervalInSeconds": 300,
    "sizeLimitInBytes": 314572800,
    "destination": {
      "name": "EventHubArchive.AzureBlockBlob",
      "properties": {
        "storageAccountResourceId": "/subscriptions/.../storageAccounts/storage",
        "blobContainer": "eventhub-capture",
        "archiveNameFormat": "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}"
      }
    }
  }
}
```

**Benefits:**
- Automatic data archival
- No code changes required
- Avro format for schema evolution
- Time and size-based triggers

---

## Monitoring & Management

### Q13: How do you monitor Event Hubs performance?
**Answer:**
**Key Metrics:**
- **Incoming Messages**: Events received per second
- **Outgoing Messages**: Events sent to consumers
- **Throttled Requests**: Rate limiting indicators
- **Server Errors**: Processing failures
- **User Errors**: Client-side errors

**Monitoring Setup:**
```python
# Custom metrics collection
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import metrics

configure_azure_monitor()
meter = metrics.get_meter(__name__)

# Create custom counters
events_processed = meter.create_counter("events_processed")
processing_errors = meter.create_counter("processing_errors")

def process_event(event):
    try:
        # Process event
        events_processed.add(1)
    except Exception as e:
        processing_errors.add(1)
        raise
```

### Q14: How do you troubleshoot Event Hubs issues?
**Answer:**
**Common Issues:**
- **Throttling**: Exceeded throughput units
- **Consumer Lag**: Slow event processing
- **Connection Errors**: Network or authentication issues
- **Partition Imbalance**: Uneven event distribution

**Troubleshooting Steps:**
```python
# Check consumer lag
def check_consumer_lag():
    from azure.eventhub import EventHubConsumerClient
    
    consumer = EventHubConsumerClient.from_connection_string(...)
    
    # Get partition information
    partition_ids = consumer.get_partition_ids()
    
    for partition_id in partition_ids:
        partition_props = consumer.get_partition_properties(partition_id)
        print(f"Partition {partition_id}:")
        print(f"  Last enqueued sequence number: {partition_props.last_enqueued_sequence_number}")
        print(f"  Last enqueued offset: {partition_props.last_enqueued_offset}")
```

---

## Performance & Optimization

### Q15: How do you optimize Event Hubs performance?
**Answer:**
**Performance Optimization:**
- **Batch Processing**: Send events in batches
- **Partition Strategy**: Distribute load evenly
- **Connection Pooling**: Reuse connections
- **Async Processing**: Use async/await patterns
- **Proper Sizing**: Right-size throughput units

**Optimization Example:**
```python
import asyncio
from azure.eventhub.aio import EventHubProducerClient

async def send_events_optimized():
    producer = EventHubProducerClient.from_connection_string(...)
    
    async with producer:
        # Create batch for efficiency
        batch = await producer.create_batch()
        
        for i in range(1000):
            try:
                batch.add(EventData(f"Event {i}"))
            except ValueError:
                # Batch is full, send it
                await producer.send_batch(batch)
                batch = await producer.create_batch()
                batch.add(EventData(f"Event {i}"))
        
        # Send remaining events
        if len(batch) > 0:
            await producer.send_batch(batch)
```

---

## Best Practices

### Q16: What are Event Hubs best practices?
**Answer:**
**Design Best Practices:**
- Use meaningful partition keys
- Plan for partition count growth
- Implement proper error handling
- Use consumer groups effectively
- Monitor performance metrics

**Code Best Practices:**
```python
# Proper error handling and retry logic
import time
from azure.core.exceptions import ServiceBusError

def send_with_retry(producer, event_data, max_retries=3):
    for attempt in range(max_retries):
        try:
            with producer:
                producer.send_batch([event_data])
            return True
        except ServiceBusError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
    return False
```

---

## Scenario-Based Questions

### Q17: How would you design a real-time IoT data ingestion system using Event Hubs?
**Answer:**
**Architecture Design:**
```
IoT Devices → Event Hubs → Stream Analytics → Storage/Analytics
     ↓            ↓              ↓              ↓
Device Data → Partitioned → Real-time → Cosmos DB
             by Device    Processing   Time Series DB
                                      Power BI
```

**Implementation:**
```python
# IoT device simulator
import json
import random
from azure.eventhub import EventHubProducerClient, EventData

async def simulate_iot_device(device_id, producer):
    while True:
        # Generate telemetry data
        telemetry = {
            "deviceId": device_id,
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": random.uniform(20, 30),
            "humidity": random.uniform(40, 60),
            "pressure": random.uniform(1000, 1020)
        }
        
        # Send to Event Hub with device ID as partition key
        event = EventData(json.dumps(telemetry))
        await producer.send_batch([event], partition_key=device_id)
        
        await asyncio.sleep(10)  # Send every 10 seconds
```

### Q18: How would you implement event replay and recovery in Event Hubs?
**Answer:**
**Replay Strategy:**
```python
from datetime import datetime, timedelta

def replay_events_from_timestamp(start_time):
    consumer = EventHubConsumerClient.from_connection_string(
        conn_str="...",
        consumer_group="replay-group",
        eventhub_name="events"
    )
    
    # Convert timestamp to Event Hub position
    starting_position = start_time.isoformat()
    
    def on_event(partition_context, event):
        # Process replayed event
        print(f"Replaying event from {event.enqueued_time}: {event.body_as_str()}")
        
        # Don't update checkpoint during replay
        # partition_context.update_checkpoint(event)
    
    with consumer:
        consumer.receive(
            on_event=on_event,
            starting_position=starting_position
        )

# Replay events from 1 hour ago
replay_start = datetime.utcnow() - timedelta(hours=1)
replay_events_from_timestamp(replay_start)
```

---

## 🎯 Key Takeaways

- **Massive Scale**: Handle millions of events per second
- **Real-time Processing**: Low-latency event streaming
- **Azure Integration**: Seamless integration with Azure services
- **Kafka Compatible**: Support for Kafka protocols
- **Managed Service**: No infrastructure management required
- **Flexible Consumption**: Multiple consumer groups and patterns
- **Enterprise Security**: Comprehensive security and compliance features

Remember: Azure Event Hubs excels at high-throughput event ingestion and integrates seamlessly with the Azure ecosystem for building comprehensive real-time analytics solutions.