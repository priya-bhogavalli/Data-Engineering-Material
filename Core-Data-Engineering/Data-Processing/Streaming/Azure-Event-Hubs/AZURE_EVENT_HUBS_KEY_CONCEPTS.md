# 🚀 Azure Event Hubs - Key Concepts

**Category**: Azure Real-time Streaming Platform  
**Market Share**: 45% of Azure streaming workloads  
**Interview Frequency**: 45% of data engineering roles  
**Learning Time**: 2-3 weeks

---

## 🎯 What is Azure Event Hubs?

Azure Event Hubs is a fully managed, real-time data ingestion service that can receive and process millions of events per second. It's designed for big data streaming scenarios and event-driven architectures.

### **Core Value Proposition**
- **Millions of events/second** throughput
- **Fully managed** Azure service
- **Apache Kafka compatibility** 
- **Auto-scaling** capabilities
- **Global availability** across Azure regions

---

## 🏗️ Architecture Overview

```
Event Producers → Event Hubs → Event Consumers
                     ↓
              Capture to Storage
```

### **Key Components**

1. **Event Hub**: Container for event streams
2. **Partitions**: Ordered sequence of events (1-32 partitions)
3. **Consumer Groups**: Views of entire event hub
4. **Throughput Units**: Capacity units for ingress/egress
5. **Event Receivers**: Applications consuming events

---

## 🔧 Core Concepts

### **1. Partitions and Throughput Units**
```python
# Partition configuration
partition_count = 4  # 1-32 partitions
throughput_units = 10  # Each TU = 1MB/s ingress, 2MB/s egress

# Capacity calculation
max_ingress = throughput_units * 1  # MB/s
max_egress = throughput_units * 2   # MB/s
```

### **2. Event Structure**
```json
{
  "body": "event data",
  "properties": {
    "user_id": "123",
    "event_type": "click"
  },
  "partition_key": "user-123",
  "sequence_number": 12345,
  "offset": "67890",
  "enqueued_time": "2024-01-15T10:30:00Z"
}
```

### **3. Consumer Groups**
```python
# Multiple consumer groups can read same events
consumer_groups = [
    "analytics-team",
    "ml-pipeline", 
    "real-time-dashboard"
]
```

---

## 🚀 Implementation

### **Creating Event Hub**
```python
from azure.eventhub import EventHubProducerClient, EventData

# Producer
producer = EventHubProducerClient.from_connection_string(
    conn_str="Endpoint=sb://...",
    eventhub_name="my-event-hub"
)

# Send events
with producer:
    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData('Event 1'))
    event_data_batch.add(EventData('Event 2'))
    producer.send_batch(event_data_batch)
```

### **Consuming Events**
```python
from azure.eventhub import EventHubConsumerClient

def on_event(partition_context, event):
    print(f"Received: {event.body_as_str()}")
    partition_context.update_checkpoint(event)

consumer = EventHubConsumerClient.from_connection_string(
    conn_str="Endpoint=sb://...",
    consumer_group="$Default",
    eventhub_name="my-event-hub"
)

with consumer:
    consumer.receive(on_event, starting_position="-1")
```

---

## 📊 Performance & Scaling

### **Throughput Units vs Auto-Inflate**
| **Mode** | **Capacity** | **Cost** | **Use Case** |
|----------|--------------|----------|--------------|
| **Standard TUs** | Fixed 1-20 TUs | $0.028/TU/hour | Predictable load |
| **Auto-Inflate** | Auto-scale to 20 TUs | Variable | Variable load |
| **Dedicated** | Dedicated cluster | $8/hour minimum | High volume |

### **Partition Strategy**
```python
# Good partition keys
partition_keys = {
    "user_based": f"user-{user_id}",
    "device_based": f"device-{device_id}",
    "region_based": f"region-{region_code}"
}

# Avoid hot partitions
# Bad: single partition key for all events
# Good: distribute events across partitions
```

---

## 🔐 Security Features

- **Shared Access Signatures (SAS)**
- **Azure Active Directory integration**
- **VNet integration**
- **Private endpoints**
- **Encryption at rest and in transit**

---

## 🛠️ Common Use Cases

### **1. IoT Telemetry**
```
IoT Devices → Event Hubs → Stream Analytics → Power BI
```

### **2. Log Aggregation**
```
Applications → Event Hubs → Azure Functions → Log Analytics
```

### **3. Real-time Analytics**
```
Web Apps → Event Hubs → Databricks → Cosmos DB
```

---

## 💡 Best Practices

1. **Choose appropriate partition count** (start with 4-8)
2. **Use meaningful partition keys** for even distribution
3. **Implement checkpointing** for reliable processing
4. **Monitor throughput metrics** and scale accordingly
5. **Use consumer groups** for multiple processing pipelines

---

## 🎯 When to Choose Event Hubs

### **✅ Choose Event Hubs When:**
- Building on **Azure ecosystem**
- Need **high throughput** (millions events/sec)
- Require **Kafka compatibility**
- Want **fully managed** service
- Need **global distribution**

### **❌ Consider Alternatives When:**
- Need **multi-cloud** (consider Kafka)
- Require **exactly-once** semantics
- Want **open-source** solution
- Need **complex routing** logic

---

**🎯 Next Steps**: Check out [Interview Questions](./AZURE_EVENT_HUBS_INTERVIEW_QUESTIONS.md)