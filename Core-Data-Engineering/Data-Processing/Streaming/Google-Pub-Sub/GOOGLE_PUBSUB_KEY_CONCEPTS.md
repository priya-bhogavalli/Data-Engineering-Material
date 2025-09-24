# 🚀 Google Pub/Sub - Key Concepts

**Category**: GCP Real-time Messaging Platform  
**Market Share**: 40% of GCP messaging workloads  
**Interview Frequency**: 40% of data engineering roles  
**Learning Time**: 2-3 weeks

---

## 🎯 What is Google Pub/Sub?

Google Pub/Sub is a fully managed real-time messaging service that allows you to send and receive messages between independent applications. It's designed for reliable, many-to-many, asynchronous messaging.

### **Core Value Proposition**
- **Global scale** with automatic scaling
- **At-least-once delivery** guarantee
- **Exactly-once delivery** option available
- **Dead letter queues** for failed messages
- **Message ordering** within message keys

---

## 🏗️ Architecture Overview

```
Publishers → Topics → Subscriptions → Subscribers
                ↓
           Message Storage (7 days)
```

### **Key Components**

1. **Topics**: Named channels for messages
2. **Subscriptions**: Named resources representing message streams
3. **Publishers**: Applications that send messages
4. **Subscribers**: Applications that receive messages
5. **Messages**: Data and attributes sent through topics

---

## 🔧 Core Concepts

### **1. Topics and Subscriptions**
```python
from google.cloud import pubsub_v1

# Create topic
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("my-project", "my-topic")
topic = publisher.create_topic(request={"name": topic_path})

# Create subscription
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path("my-project", "my-subscription")
subscription = subscriber.create_subscription(
    request={"name": subscription_path, "topic": topic_path}
)
```

### **2. Message Structure**
```python
# Message format
message = {
    "data": b"Hello World",  # Message payload (bytes)
    "attributes": {          # Key-value metadata
        "user_id": "123",
        "event_type": "click"
    },
    "message_id": "12345",   # Unique identifier
    "publish_time": "2024-01-15T10:30:00Z",
    "ordering_key": "user-123"  # For ordered delivery
}
```

### **3. Delivery Types**
- **Pull**: Subscriber requests messages
- **Push**: Pub/Sub sends messages to HTTP endpoint
- **Exactly-once**: Guarantees no duplicates (premium feature)

---

## 🚀 Implementation

### **Publishing Messages**
```python
import json
from google.cloud import pubsub_v1

def publish_messages():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("my-project", "events")
    
    # Publish single message
    data = json.dumps({"user_id": 123, "action": "click"}).encode("utf-8")
    future = publisher.publish(topic_path, data, user_id="123")
    message_id = future.result()
    
    # Publish with ordering key
    future = publisher.publish(
        topic_path, 
        data, 
        ordering_key="user-123",
        event_type="click"
    )
    
    return message_id
```

### **Subscribing to Messages**
```python
def receive_messages():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("my-project", "my-sub")
    
    def callback(message):
        print(f"Received: {message.data.decode('utf-8')}")
        print(f"Attributes: {message.attributes}")
        message.ack()  # Acknowledge message
    
    # Pull messages
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    
    try:
        streaming_pull_future.result()  # Block indefinitely
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
```

---

## 📊 Performance & Scaling

### **Throughput Limits**
| **Resource** | **Limit** | **Scalable** |
|--------------|-----------|--------------|
| **Topic throughput** | 1 GB/s | Auto-scales |
| **Subscription throughput** | 1 GB/s | Auto-scales |
| **Message size** | 10 MB | Fixed |
| **Message retention** | 7 days | Configurable |

### **Optimization Strategies**
```python
# Batch publishing for higher throughput
def publish_batch():
    publisher = pubsub_v1.PublisherClient(
        batch_settings=pubsub_v1.types.BatchSettings(
            max_messages=1000,
            max_bytes=1024*1024,  # 1MB
            max_latency=0.1       # 100ms
        )
    )
    
    topic_path = publisher.topic_path("my-project", "events")
    
    futures = []
    for i in range(1000):
        data = json.dumps({"id": i}).encode("utf-8")
        future = publisher.publish(topic_path, data)
        futures.append(future)
    
    # Wait for all messages to be published
    for future in futures:
        future.result()
```

---

## 🔐 Security Features

- **IAM integration** for access control
- **VPC Service Controls** for network security
- **Customer-managed encryption keys** (CMEK)
- **Audit logging** for compliance
- **Private Google Access** for VPC networks

---

## 🛠️ Common Use Cases

### **1. Event-Driven Architecture**
```
Microservices → Pub/Sub Topics → Event Handlers
```

### **2. Data Pipeline**
```
Data Sources → Pub/Sub → Dataflow → BigQuery
```

### **3. Real-time Analytics**
```
Applications → Pub/Sub → Cloud Functions → Monitoring
```

---

## 💡 Best Practices

1. **Use appropriate subscription types** (pull vs push)
2. **Implement proper error handling** and dead letter queues
3. **Monitor message age** and subscription backlog
4. **Use ordering keys** for ordered processing when needed
5. **Set appropriate acknowledgment deadlines**

### **Error Handling**
```python
def robust_subscriber():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("my-project", "my-sub")
    
    def callback(message):
        try:
            # Process message
            process_message(message.data)
            message.ack()
        except Exception as e:
            print(f"Error processing message: {e}")
            message.nack()  # Negative acknowledgment
    
    # Configure flow control
    flow_control = pubsub_v1.types.FlowControl(max_messages=100)
    
    streaming_pull_future = subscriber.subscribe(
        subscription_path, 
        callback=callback,
        flow_control=flow_control
    )
```

---

## 🎯 When to Choose Pub/Sub

### **✅ Choose Pub/Sub When:**
- Building on **GCP ecosystem**
- Need **global scale** messaging
- Require **exactly-once delivery**
- Want **fully managed** service
- Need **message ordering** capabilities

### **❌ Consider Alternatives When:**
- Need **multi-cloud** deployment
- Require **complex routing** logic
- Want **open-source** solution
- Need **very low latency** (<1ms)

---

**🎯 Next Steps**: Check out [Interview Questions](./GOOGLE_PUBSUB_INTERVIEW_QUESTIONS.md)