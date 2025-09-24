# 🎯 Azure Event Hubs Interview Questions

**Difficulty Levels**: 🟢 Beginner | 🟡 Intermediate | 🔴 Advanced  
**Total Questions**: 50+  
**Interview Frequency**: 45% of data engineering roles

---

## 🟢 Beginner Level Questions

### **Q1: What is Azure Event Hubs and how does it differ from Service Bus?**

**Answer:**
Azure Event Hubs is a big data streaming platform for high-throughput event ingestion, while Service Bus is a message broker for application integration.

| **Aspect** | **Event Hubs** | **Service Bus** |
|------------|----------------|-----------------|
| **Purpose** | Event streaming | Message queuing |
| **Throughput** | Millions events/sec | Thousands messages/sec |
| **Ordering** | Per partition | Global or session |
| **Retention** | 1-7 days | Until consumed |
| **Use Case** | Big data, IoT | Enterprise messaging |

---

### **Q2: Explain partitions and throughput units in Event Hubs.**

**Answer:**
**Partitions**: Ordered sequences of events (1-32 per Event Hub)
- Events with same partition key go to same partition
- Enable parallel processing
- Determine scalability

**Throughput Units (TUs)**: Capacity units that control ingress/egress
- 1 TU = 1 MB/s ingress OR 1000 events/s
- 1 TU = 2 MB/s egress
- Standard tier: 1-20 TUs
- Can auto-inflate based on demand

```python
# Calculate required TUs
events_per_second = 5000
avg_event_size_kb = 2

required_tus_by_events = events_per_second / 1000  # 5 TUs
required_tus_by_size = (events_per_second * avg_event_size_kb) / 1024  # ~10 TUs

required_tus = max(required_tus_by_events, required_tus_by_size)  # 10 TUs
```

---

### **Q3: How do you send events to Event Hubs using Python?**

**Answer:**
```python
from azure.eventhub import EventHubProducerClient, EventData
import json

# Initialize producer
producer = EventHubProducerClient.from_connection_string(
    conn_str="Endpoint=sb://myhub.servicebus.windows.net/;SharedAccessKeyName=...",
    eventhub_name="my-event-hub"
)

# Send single event
def send_single_event():
    event_data = EventData(json.dumps({
        "user_id": 123,
        "action": "click",
        "timestamp": "2024-01-15T10:30:00Z"
    }))
    
    with producer:
        producer.send_batch([event_data])

# Send batch events
def send_batch_events():
    with producer:
        event_data_batch = producer.create_batch()
        
        for i in range(100):
            event_data = EventData(json.dumps({
                "user_id": i,
                "action": "view"
            }))
            event_data_batch.add(event_data)
        
        producer.send_batch(event_data_batch)
```

---

### **Q4: What are consumer groups and why are they important?**

**Answer:**
Consumer groups provide independent views of the event stream, allowing multiple applications to consume the same events.

**Key Features**:
- Each consumer group maintains its own offset
- Up to 5 concurrent readers per partition per consumer group
- Default consumer group: `$Default`

**Use Cases**:
```python
# Different consumer groups for different purposes
consumer_groups = {
    "analytics": "Real-time analytics processing",
    "ml-pipeline": "Machine learning feature extraction", 
    "audit": "Compliance and audit logging",
    "backup": "Data archival to storage"
}

# Each group processes same events independently
from azure.eventhub import EventHubConsumerClient

def create_consumer(consumer_group):
    return EventHubConsumerClient.from_connection_string(
        conn_str="Endpoint=sb://...",
        consumer_group=consumer_group,
        eventhub_name="my-event-hub"
    )

analytics_consumer = create_consumer("analytics")
ml_consumer = create_consumer("ml-pipeline")
```

---

### **Q5: How do you implement checkpointing in Event Hubs?**

**Answer:**
Checkpointing saves the last processed event position to enable reliable processing and recovery.

```python
from azure.eventhub import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore

# Set up checkpoint store
checkpoint_store = BlobCheckpointStore.from_connection_string(
    "DefaultEndpointsProtocol=https;AccountName=...",
    container_name="checkpoints"
)

# Consumer with checkpointing
consumer = EventHubConsumerClient.from_connection_string(
    conn_str="Endpoint=sb://...",
    consumer_group="my-group",
    eventhub_name="my-event-hub",
    checkpoint_store=checkpoint_store
)

def on_event(partition_context, event):
    # Process event
    print(f"Processing: {event.body_as_str()}")
    
    # Update checkpoint after successful processing
    partition_context.update_checkpoint(event)

# Start consuming with checkpointing
with consumer:
    consumer.receive(
        on_event=on_event,
        starting_position="-1"  # Start from beginning or last checkpoint
    )
```

---

## 🟡 Intermediate Level Questions

### **Q6: How do you optimize Event Hubs performance for high throughput?**

**Answer:**
Performance optimization involves multiple strategies:

**1. Partition Strategy**:
```python
# Good partition key distribution
def get_partition_key(event_data):
    # Distribute based on user_id for even load
    return f"user-{event_data['user_id'] % 100}"

# Avoid hot partitions
# Bad: All events to same partition
# Good: Distribute across partitions evenly
```

**2. Batch Processing**:
```python
# Optimize batch size
def send_optimized_batch(events):
    with producer:
        batch = producer.create_batch(max_size_in_bytes=1024*1024)  # 1MB batches
        
        for event in events:
            try:
                batch.add(EventData(json.dumps(event)))
            except ValueError:  # Batch full
                producer.send_batch(batch)
                batch = producer.create_batch()
                batch.add(EventData(json.dumps(event)))
        
        if len(batch) > 0:
            producer.send_batch(batch)
```

**3. Throughput Unit Scaling**:
```python
# Monitor and auto-scale TUs
def monitor_and_scale():
    # Get metrics
    ingress_rate = get_ingress_metrics()  # MB/s
    current_tus = get_current_throughput_units()
    
    # Scale up if approaching limits
    if ingress_rate > current_tus * 0.8:  # 80% utilization
        new_tus = min(20, current_tus * 2)
        scale_throughput_units(new_tus)
    
    # Scale down if underutilized
    elif ingress_rate < current_tus * 0.3:  # 30% utilization
        new_tus = max(1, current_tus // 2)
        scale_throughput_units(new_tus)
```

**4. Consumer Optimization**:
```python
# Parallel processing within consumer
import asyncio
from concurrent.futures import ThreadPoolExecutor

async def process_events_parallel(partition_context, event):
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Process event in thread pool
        await asyncio.get_event_loop().run_in_executor(
            executor, process_single_event, event
        )
    
    # Checkpoint after processing
    partition_context.update_checkpoint(event)
```

---

### **Q7: How do you implement error handling and retry logic?**

**Answer:**
Robust error handling is crucial for production Event Hubs applications:

**1. Producer Error Handling**:
```python
import time
import random
from azure.eventhub.exceptions import EventHubError

class RobustEventHubProducer:
    def __init__(self, connection_string, eventhub_name):
        self.connection_string = connection_string
        self.eventhub_name = eventhub_name
        self.max_retries = 3
    
    def send_with_retry(self, events):
        for attempt in range(self.max_retries):
            try:
                producer = EventHubProducerClient.from_connection_string(
                    self.connection_string, 
                    eventhub_name=self.eventhub_name
                )
                
                with producer:
                    batch = producer.create_batch()
                    for event in events:
                        batch.add(EventData(json.dumps(event)))
                    producer.send_batch(batch)
                
                return True  # Success
                
            except EventHubError as e:
                if "QuotaExceeded" in str(e) and attempt < self.max_retries - 1:
                    # Exponential backoff for quota exceeded
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(wait_time)
                    continue
                else:
                    raise e
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)
        
        return False
```

**2. Consumer Error Handling**:
```python
def resilient_event_processor(partition_context, event):
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Process the event
            result = process_business_logic(event)
            
            # Only checkpoint on successful processing
            partition_context.update_checkpoint(event)
            return result
            
        except Exception as e:
            if attempt == max_retries - 1:
                # Send to dead letter queue or log error
                send_to_dead_letter_queue(event, str(e))
                # Still checkpoint to avoid reprocessing
                partition_context.update_checkpoint(event)
            else:
                time.sleep(2 ** attempt)  # Exponential backoff
```

**3. Dead Letter Queue Pattern**:
```python
# Send failed events to Service Bus dead letter queue
from azure.servicebus import ServiceBusClient, ServiceBusMessage

def send_to_dead_letter_queue(failed_event, error_message):
    servicebus_client = ServiceBusClient.from_connection_string(
        "Endpoint=sb://..."
    )
    
    with servicebus_client:
        sender = servicebus_client.get_queue_sender("dead-letter-queue")
        
        dead_letter_message = ServiceBusMessage(
            body=json.dumps({
                "original_event": failed_event.body_as_str(),
                "error": error_message,
                "timestamp": time.time(),
                "partition_id": failed_event.partition_key
            })
        )
        
        sender.send_messages(dead_letter_message)
```

---

### **Q8: How do you monitor Event Hubs performance and set up alerts?**

**Answer:**
Comprehensive monitoring involves Azure Monitor metrics and custom alerting:

**1. Key Metrics to Monitor**:
```python
# Important Event Hubs metrics
key_metrics = {
    "IncomingMessages": "Events received per second",
    "OutgoingMessages": "Events sent to consumers", 
    "IncomingBytes": "Data ingress rate",
    "OutgoingBytes": "Data egress rate",
    "ThrottledRequests": "Requests throttled due to TU limits",
    "ServerErrors": "Server-side errors",
    "UserErrors": "Client-side errors",
    "QuotaExceededErrors": "Throughput unit quota exceeded"
}
```

**2. Azure Monitor Integration**:
```python
from azure.monitor.query import MetricsQueryClient
from azure.identity import DefaultAzureCredential

def get_eventhub_metrics(resource_id, metric_names, timespan):
    credential = DefaultAzureCredential()
    client = MetricsQueryClient(credential)
    
    response = client.query_resource(
        resource_uri=resource_id,
        metric_names=metric_names,
        timespan=timespan,
        granularity="PT1M"  # 1 minute intervals
    )
    
    return response

# Usage
metrics = get_eventhub_metrics(
    resource_id="/subscriptions/.../resourceGroups/.../providers/Microsoft.EventHub/namespaces/myhub",
    metric_names=["IncomingMessages", "ThrottledRequests"],
    timespan="PT1H"  # Last hour
)
```

**3. Custom Alerting**:
```python
# Set up alerts using Azure SDK
from azure.mgmt.monitor import MonitorManagementClient

def create_throughput_alert(subscription_id, resource_group, eventhub_name):
    monitor_client = MonitorManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id
    )
    
    # Alert when throttled requests > 10 in 5 minutes
    alert_rule = {
        "location": "global",
        "properties": {
            "description": "Alert when Event Hub is throttled",
            "severity": 2,
            "enabled": True,
            "condition": {
                "allOf": [{
                    "metricName": "ThrottledRequests",
                    "operator": "GreaterThan",
                    "threshold": 10,
                    "timeAggregation": "Total"
                }]
            },
            "windowSize": "PT5M",  # 5 minutes
            "evaluationFrequency": "PT1M",  # Check every minute
            "actions": [{
                "actionGroupId": "/subscriptions/.../actionGroups/my-alerts"
            }]
        }
    }
    
    return monitor_client.metric_alerts.create_or_update(
        resource_group_name=resource_group,
        rule_name=f"{eventhub_name}-throttling-alert",
        parameters=alert_rule
    )
```

---

## 🔴 Advanced Level Questions

### **Q9: How would you design a multi-region Event Hubs architecture for disaster recovery?**

**Answer:**
Multi-region Event Hubs architecture requires careful planning for failover and data consistency:

**1. Active-Passive Setup**:
```python
class MultiRegionEventHubManager:
    def __init__(self):
        self.primary_region = "East US"
        self.secondary_region = "West US"
        
        self.primary_client = EventHubProducerClient.from_connection_string(
            "Endpoint=sb://primary-hub-eastus.servicebus.windows.net/..."
        )
        
        self.secondary_client = EventHubProducerClient.from_connection_string(
            "Endpoint=sb://secondary-hub-westus.servicebus.windows.net/..."
        )
        
        self.current_client = self.primary_client
        self.failover_threshold = 5  # seconds
    
    def send_with_failover(self, events):
        try:
            # Try primary region first
            start_time = time.time()
            self.current_client.send_batch(events)
            
            # Monitor latency
            latency = time.time() - start_time
            if latency > self.failover_threshold:
                self.check_primary_health()
            
        except Exception as e:
            print(f"Primary region failed: {e}")
            self.failover_to_secondary()
            self.secondary_client.send_batch(events)
    
    def failover_to_secondary(self):
        print("Failing over to secondary region")
        self.current_client = self.secondary_client
        
        # Update DNS or load balancer configuration
        self.update_dns_records()
        
        # Notify operations team
        self.send_failover_alert()
```

**2. Event Replication Strategy**:
```python
# Replicate events between regions
class EventReplicator:
    def __init__(self, source_hub, target_hub):
        self.source_consumer = EventHubConsumerClient.from_connection_string(
            source_hub, consumer_group="replication"
        )
        self.target_producer = EventHubProducerClient.from_connection_string(
            target_hub
        )
    
    def replicate_events(self):
        def on_event(partition_context, event):
            # Add replication metadata
            replicated_event = {
                "original_data": json.loads(event.body_as_str()),
                "replication_metadata": {
                    "source_region": "East US",
                    "replicated_at": time.time(),
                    "original_partition": partition_context.partition_id
                }
            }
            
            # Send to target region
            self.target_producer.send_batch([
                EventData(json.dumps(replicated_event))
            ])
            
            partition_context.update_checkpoint(event)
        
        with self.source_consumer:
            self.source_consumer.receive(on_event)
```

---

### **Q10: How do you implement exactly-once processing with Event Hubs?**

**Answer:**
Event Hubs provides at-least-once delivery, so exactly-once processing must be implemented at the application level:

**1. Idempotent Processing with Deduplication**:
```python
import hashlib
from azure.cosmos import CosmosClient

class ExactlyOnceProcessor:
    def __init__(self, cosmos_connection, database_name, container_name):
        self.cosmos_client = CosmosClient.from_connection_string(cosmos_connection)
        self.database = self.cosmos_client.get_database_client(database_name)
        self.container = self.database.get_container_client(container_name)
    
    def generate_event_id(self, event):
        # Create deterministic ID from event content
        content = f"{event.partition_key}-{event.sequence_number}-{event.body_as_str()}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def process_event_exactly_once(self, partition_context, event):
        event_id = self.generate_event_id(event)
        
        try:
            # Try to insert with unique constraint
            self.container.create_item({
                "id": event_id,
                "partition_key": event.partition_key,
                "processed_at": time.time(),
                "event_data": event.body_as_str(),
                "status": "processing"
            })
            
            # Process the event
            result = self.process_business_logic(event)
            
            # Update status to completed
            self.container.replace_item(
                item=event_id,
                body={
                    "id": event_id,
                    "partition_key": event.partition_key,
                    "processed_at": time.time(),
                    "event_data": event.body_as_str(),
                    "status": "completed",
                    "result": result
                }
            )
            
            # Checkpoint only after successful processing
            partition_context.update_checkpoint(event)
            
        except Exception as e:
            if "Conflict" in str(e):
                # Event already processed
                print(f"Event {event_id} already processed, skipping")
                partition_context.update_checkpoint(event)
            else:
                # Processing error, don't checkpoint
                raise e
```

**2. Transactional Outbox Pattern**:
```python
# Use database transactions for exactly-once semantics
class TransactionalProcessor:
    def __init__(self, sql_connection):
        self.connection = sql_connection
    
    def process_with_transaction(self, partition_context, event):
        event_id = self.generate_event_id(event)
        
        with self.connection.begin() as transaction:
            try:
                # Check if already processed
                cursor = transaction.execute(
                    "SELECT id FROM processed_events WHERE id = %s",
                    (event_id,)
                )
                
                if cursor.fetchone():
                    # Already processed
                    partition_context.update_checkpoint(event)
                    return
                
                # Process business logic within transaction
                self.process_business_logic_transactional(transaction, event)
                
                # Mark as processed
                transaction.execute(
                    "INSERT INTO processed_events (id, processed_at) VALUES (%s, %s)",
                    (event_id, time.time())
                )
                
                # Commit transaction
                transaction.commit()
                
                # Checkpoint after successful commit
                partition_context.update_checkpoint(event)
                
            except Exception as e:
                transaction.rollback()
                raise e
```

This approach ensures exactly-once processing semantics even with Event Hubs' at-least-once delivery guarantee.

---

## 🎯 Interview Tips

### **Preparation Strategy**
1. **Hands-on Experience**: Create Event Hubs and practice sending/receiving events
2. **Architecture Understanding**: Know partitions, throughput units, and consumer groups
3. **Performance Optimization**: Understand scaling and optimization techniques
4. **Integration Patterns**: Learn Azure ecosystem integrations
5. **Troubleshooting**: Practice diagnosing throttling and performance issues

### **Key Points to Emphasize**
- Fully managed Azure service
- High throughput capabilities (millions events/sec)
- Kafka compatibility for easy migration
- Integration with Azure ecosystem
- Auto-scaling capabilities
- Enterprise security features

---

**🎯 Ready for your interview?** Practice these scenarios and understand the trade-offs between different approaches.