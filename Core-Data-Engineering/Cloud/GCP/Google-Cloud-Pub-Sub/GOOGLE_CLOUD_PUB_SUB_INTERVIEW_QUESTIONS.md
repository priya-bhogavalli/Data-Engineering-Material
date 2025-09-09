
### Q1: What is Google Cloud Pub/Sub and what problems does it solve?
**Answer:**
Google Cloud Pub/Sub is a fully managed messaging service that enables asynchronous communication between applications.

**Key Problems Solved:**
- **Decoupling**: Separate message producers from consumers
- **Scalability**: Handle millions of messages per second
- **Reliability**: Guaranteed message delivery with durability
- **Global Distribution**: Multi-region message delivery
- **Integration**: Connect diverse systems and services

**Core Features:**
- At-least-once message delivery
- Global message ordering (optional)
- Dead letter queues
- Message filtering
- Schema validation
- Push and pull delivery

### Q2: How does Pub/Sub differ from other messaging systems?
**Answer:**
**vs Apache Kafka:**
- Pub/Sub: Fully managed, serverless, global
- Kafka: Self-managed, more control, higher throughput

**vs RabbitMQ:**
- Pub/Sub: Cloud-native, auto-scaling
- RabbitMQ: More routing options, complex topologies

**vs Amazon SQS:**
- Pub/Sub: True pub-sub model, global ordering
- SQS: Queue-based, simpler model

**Key Differentiators:**
- Serverless and fully managed
- Global availability and durability
- Automatic scaling and load balancing
- Integration with Google Cloud ecosystem

---

## Architecture & Components

### Q3: What are the core components of Pub/Sub architecture?
**Answer:**
**Core Components:**
- **Topics**: Named channels for messages
- **Subscriptions**: Named endpoints that receive messages
- **Publishers**: Applications that send messages
- **Subscribers**: Applications that receive messages
- **Messages**: Data payloads with attributes
- **Snapshots**: Point-in-time subscription states

**Architecture Flow:**
```
Publishers → Topics → Subscriptions → Subscribers
                ↓
            Message Storage
```

### Q4: How do topics and subscriptions work together?
**Answer:**
**Topic-Subscription Relationship:**
- **One-to-Many**: One topic can have multiple subscriptions
- **Independent Delivery**: Each subscription receives all messages
- **Separate Processing**: Subscriptions can have different consumers
- **Retention**: Messages retained until acknowledged by all subscriptions

**Example Setup:**
```python
from google.cloud import pubsub_v1

# Create topic
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project-id', 'my-topic')
publisher.create_topic(request={"name": topic_path})

# Create subscriptions
subscriber = pubsub_v1.SubscriberClient()

# Analytics subscription
analytics_sub = subscriber.subscription_path('project-id', 'analytics-sub')
subscriber.create_subscription(
    request={"name": analytics_sub, "topic": topic_path}
)

# Alerts subscription  
alerts_sub = subscriber.subscription_path('project-id', 'alerts-sub')
subscriber.create_subscription(
    request={"name": alerts_sub, "topic": topic_path}
)
```

---

## Publishing & Subscribing

### Q5: How do you publish messages to Pub/Sub?
**Answer:**
**Publishing Messages:**
```python
from google.cloud import pubsub_v1
import json

# Initialize publisher
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('project-id', 'my-topic')

# Publish single message
data = json.dumps({"user_id": "123", "action": "login"})
future = publisher.publish(
    topic_path, 
    data.encode('utf-8'),
    user_id="123",  # Message attributes
    timestamp=str(time.time())
)
message_id = future.result()

# Publish batch messages
futures = []
for i in range(100):
    data = json.dumps({"event_id": i, "data": f"event_{i}"})
    future = publisher.publish(topic_path, data.encode('utf-8'))
    futures.append(future)

# Wait for all messages to be published
for future in futures:
    message_id = future.result()
```

### Q6: How do you consume messages from Pub/Sub?
**Answer:**
**Pull Subscription:**
```python
from google.cloud import pubsub_v1

def callback(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    print(f"Attributes: {message.attributes}")
    
    # Process message
    try:
        process_message(message.data)
        message.ack()  # Acknowledge successful processing
    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()  # Negative acknowledgment

# Create subscriber
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('project-id', 'my-subscription')

# Configure flow control
flow_control = pubsub_v1.types.FlowControl(max_messages=1000)

# Start listening
streaming_pull_future = subscriber.subscribe(
    subscription_path, 
    callback=callback,
    flow_control=flow_control
)

try:
    streaming_pull_future.result()  # Block indefinitely
except KeyboardInterrupt:
    streaming_pull_future.cancel()
```

**Synchronous Pull:**
```python
# Pull messages synchronously
response = subscriber.pull(
    request={
        "subscription": subscription_path,
        "max_messages": 10,
    }
)

for received_message in response.received_messages:
    print(f"Received: {received_message.message.data.decode('utf-8')}")
    
    # Acknowledge message
    subscriber.acknowledge(
        request={
            "subscription": subscription_path,
            "ack_ids": [received_message.ack_id],
        }
    )
```

---

## Message Delivery & Acknowledgment

### Q7: How does Pub/Sub ensure message delivery?
**Answer:**
**Delivery Guarantees:**
- **At-least-once**: Messages delivered at least once
- **Durability**: Messages persisted until acknowledged
- **Retry Logic**: Automatic retry for failed deliveries
- **Dead Letter Queues**: Handle persistently failing messages

**Acknowledgment Flow:**
```python
def reliable_message_handler(message):
    try:
        # Process message with idempotency
        result = process_with_idempotency_key(
            message.data, 
            message.message_id
        )
        
        if result.success:
            message.ack()
        else:
            # Temporary failure, let it retry
            message.nack()
            
    except PermanentError as e:
        # Permanent failure, acknowledge to prevent retry
        log_error(f"Permanent error: {e}")
        message.ack()
        
    except Exception as e:
        # Temporary error, nack for retry
        log_error(f"Temporary error: {e}")
        message.nack()
```

### Q8: What are dead letter queues and how do you use them?
**Answer:**
**Dead Letter Queue Setup:**
```python
# Create dead letter topic and subscription
dead_letter_topic = publisher.topic_path('project-id', 'dead-letter-topic')
publisher.create_topic(request={"name": dead_letter_topic})

dead_letter_sub = subscriber.subscription_path('project-id', 'dead-letter-sub')
subscriber.create_subscription(
    request={"name": dead_letter_sub, "topic": dead_letter_topic}
)

# Create main subscription with dead letter policy
main_subscription = subscriber.subscription_path('project-id', 'main-sub')
dead_letter_policy = {
    "dead_letter_topic": dead_letter_topic,
    "max_delivery_attempts": 5
}

subscriber.create_subscription(
    request={
        "name": main_subscription,
        "topic": topic_path,
        "dead_letter_policy": dead_letter_policy
    }
)
```

---

## Scaling & Performance

### Q9: How does Pub/Sub handle scaling?
**Answer:**
**Auto-scaling Features:**
- **Automatic Partitioning**: Messages distributed across partitions
- **Dynamic Scaling**: Resources scale based on load
- **Global Load Balancing**: Traffic distributed globally
- **Flow Control**: Prevent subscriber overload

**Performance Optimization:**
```python
# Configure subscriber for high throughput
from google.cloud.pubsub_v1.types import FlowControl

flow_control = FlowControl(
    max_messages=10000,  # Maximum outstanding messages
    max_bytes=1024 * 1024 * 1024,  # 1GB max outstanding bytes
)

# Configure threading
subscriber_options = pubsub_v1.subscriber.types.SubscriberOptions(
    message_retention_duration={"seconds": 600}  # 10 minutes
)

streaming_pull_future = subscriber.subscribe(
    subscription_path,
    callback=callback,
    flow_control=flow_control,
    subscriber_options=subscriber_options
)
```

### Q10: How do you optimize Pub/Sub performance?
**Answer:**
**Publisher Optimization:**
```python
# Batch publishing for better throughput
from google.cloud.pubsub_v1 import BatchSettings

batch_settings = BatchSettings(
    max_messages=1000,  # Maximum messages per batch
    max_bytes=1024 * 1024,  # 1MB max batch size
    max_latency=0.1,  # 100ms max batching delay
)

publisher = pubsub_v1.PublisherClient(batch_settings=batch_settings)

# Async publishing
import asyncio

async def publish_async():
    futures = []
    for i in range(1000):
        data = f"message_{i}".encode('utf-8')
        future = publisher.publish(topic_path, data)
        futures.append(future)
    
    # Wait for all publishes to complete
    results = await asyncio.gather(*[
        asyncio.wrap_future(future) for future in futures
    ])
    return results
```

---

## Security & Access Control

### Q11: How do you secure Pub/Sub resources?
**Answer:**
**Security Features:**
- **IAM Integration**: Role-based access control
- **Service Accounts**: Application authentication
- **VPC Service Controls**: Network-level security
- **Encryption**: At rest and in transit
- **Audit Logging**: Track all operations

**IAM Configuration:**
```python
from google.cloud import pubsub_v1
from google.iam.v1 import policy_pb2

# Grant publish permission
policy = publisher.get_iam_policy(request={"resource": topic_path})

binding = policy_pb2.Binding(
    role="roles/pubsub.publisher",
    members=["serviceAccount:publisher@project.iam.gserviceaccount.com"]
)
policy.bindings.append(binding)

publisher.set_iam_policy(request={"resource": topic_path, "policy": policy})

# Grant subscription access
subscriber_policy = subscriber.get_iam_policy(request={"resource": subscription_path})

subscriber_binding = policy_pb2.Binding(
    role="roles/pubsub.subscriber", 
    members=["serviceAccount:subscriber@project.iam.gserviceaccount.com"]
)
subscriber_policy.bindings.append(subscriber_binding)

subscriber.set_iam_policy(
    request={"resource": subscription_path, "policy": subscriber_policy}
)
```

### Q12: How do you implement message-level security?
**Answer:**
**Message Encryption:**
```python
import base64
from cryptography.fernet import Fernet

class SecurePublisher:
    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)
        self.publisher = pubsub_v1.PublisherClient()
    
    def publish_encrypted(self, topic_path, data, **attributes):
        # Encrypt message data
        encrypted_data = self.cipher.encrypt(data.encode('utf-8'))
        
        # Add encryption metadata
        attributes['encrypted'] = 'true'
        attributes['encryption_version'] = '1'
        
        return self.publisher.publish(
            topic_path, 
            encrypted_data, 
            **attributes
        )

class SecureSubscriber:
    def __init__(self, encryption_key):
        self.cipher = Fernet(encryption_key)
    
    def decrypt_message(self, message):
        if message.attributes.get('encrypted') == 'true':
            decrypted_data = self.cipher.decrypt(message.data)
            return decrypted_data.decode('utf-8')
        return message.data.decode('utf-8')
```

---

## Integration & SDKs

### Q13: How does Pub/Sub integrate with other Google Cloud services?
**Answer:**
**Common Integrations:**
- **Cloud Functions**: Event-driven processing
- **Dataflow**: Stream processing pipelines
- **BigQuery**: Data warehousing
- **Cloud Storage**: File processing triggers
- **Cloud Run**: Containerized message processing

**Cloud Functions Integration:**
```python
import functions_framework
from google.cloud import pubsub_v1
import base64
import json

@functions_framework.cloud_event
def process_pubsub_message(cloud_event):
    # Decode Pub/Sub message
    message_data = base64.b64decode(cloud_event.data["message"]["data"])
    message_json = json.loads(message_data.decode('utf-8'))
    
    # Process message
    result = process_business_logic(message_json)
    
    # Optionally publish result to another topic
    if result:
        publisher = pubsub_v1.PublisherClient()
        result_topic = publisher.topic_path('project-id', 'results-topic')
        publisher.publish(result_topic, json.dumps(result).encode('utf-8'))
    
    return 'OK'
```

### Q14: How do you use Pub/Sub with Dataflow?
**Answer:**
**Dataflow Pipeline:**
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def run_pipeline():
    pipeline_options = PipelineOptions([
        '--project=my-project',
        '--runner=DataflowRunner',
        '--streaming=true',
        '--region=us-central1'
    ])
    
    with beam.Pipeline(options=pipeline_options) as pipeline:
        messages = (
            pipeline
            | 'Read from Pub/Sub' >> beam.io.ReadFromPubSub(
                subscription='projects/my-project/subscriptions/my-sub'
            )
            | 'Parse JSON' >> beam.Map(json.loads)
            | 'Transform Data' >> beam.Map(transform_message)
            | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                table='my-project:dataset.table',
                schema=table_schema
            )
        )

def transform_message(message):
    # Transform message for BigQuery
    return {
        'timestamp': message.get('timestamp'),
        'user_id': message.get('user_id'),
        'event_type': message.get('event_type'),
        'processed_at': datetime.utcnow().isoformat()
    }
```

---

## Monitoring & Management

### Q15: How do you monitor Pub/Sub performance?
**Answer:**
**Key Metrics:**
- **Message Throughput**: Messages per second
- **Subscription Backlog**: Unprocessed messages
- **Acknowledgment Rate**: Processing success rate
- **Delivery Latency**: End-to-end message latency
- **Error Rates**: Failed deliveries and processing

**Monitoring Setup:**
```python
from google.cloud import monitoring_v3
import time

def create_custom_metrics():
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    
    # Create custom metric for processing time
    descriptor = monitoring_v3.MetricDescriptor(
        type="custom.googleapis.com/pubsub/processing_time",
        metric_kind=monitoring_v3.MetricDescriptor.MetricKind.GAUGE,
        value_type=monitoring_v3.MetricDescriptor.ValueType.DOUBLE,
        description="Time taken to process Pub/Sub messages"
    )
    
    client.create_metric_descriptor(
        name=project_name, 
        metric_descriptor=descriptor
    )

def record_processing_time(processing_time):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"
    
    series = monitoring_v3.TimeSeries()
    series.metric.type = "custom.googleapis.com/pubsub/processing_time"
    series.resource.type = "global"
    
    point = monitoring_v3.Point()
    point.value.double_value = processing_time
    point.interval.end_time.seconds = int(time.time())
    series.points = [point]
    
    client.create_time_series(name=project_name, time_series=[series])
```

---

## Advanced Features

### Q16: How do you implement message ordering in Pub/Sub?
**Answer:**
**Ordering Keys:**
```python
# Publisher with ordering
publisher = pubsub_v1.PublisherClient()

# Enable message ordering for topic
topic_path = publisher.topic_path('project-id', 'ordered-topic')

# Publish messages with ordering key
for i in range(10):
    data = f"message_{i}".encode('utf-8')
    future = publisher.publish(
        topic_path,
        data,
        ordering_key="user_123"  # Messages with same key are ordered
    )
    message_id = future.result()

# Subscriber with ordering
def ordered_callback(message):
    print(f"Received ordered message: {message.data.decode('utf-8')}")
    print(f"Ordering key: {message.ordering_key}")
    message.ack()

# Create subscription with ordering enabled
subscription_path = subscriber.subscription_path('project-id', 'ordered-sub')
subscriber.create_subscription(
    request={
        "name": subscription_path,
        "topic": topic_path,
        "enable_message_ordering": True
    }
)
```

### Q17: How do you use message filtering in Pub/Sub?
**Answer:**
**Subscription Filters:**
```python
# Create subscription with filter
filter_expression = 'attributes.event_type="user_action" AND attributes.priority="high"'

subscriber.create_subscription(
    request={
        "name": subscription_path,
        "topic": topic_path,
        "filter": filter_expression
    }
)

# Publish messages with attributes for filtering
publisher.publish(
    topic_path,
    b"High priority user action",
    event_type="user_action",
    priority="high",
    user_id="123"
)

publisher.publish(
    topic_path, 
    b"Low priority system event",
    event_type="system_event",
    priority="low"
)
# Only the first message will be delivered to the filtered subscription
```

---

## Best Practices

### Q18: What are Pub/Sub best practices?
**Answer:**
**Design Best Practices:**
- Use meaningful topic and subscription names
- Implement idempotent message processing
- Handle duplicate messages gracefully
- Use appropriate message retention periods
- Monitor subscription backlogs

**Code Best Practices:**
```python
import hashlib
import json

class IdempotentProcessor:
    def __init__(self):
        self.processed_messages = set()
    
    def process_message(self, message):
        # Create idempotency key from message content
        content_hash = hashlib.sha256(message.data).hexdigest()
        
        if content_hash in self.processed_messages:
            print(f"Duplicate message detected: {content_hash}")
            message.ack()  # Acknowledge duplicate
            return
        
        try:
            # Process message
            result = self.business_logic(message.data)
            
            # Mark as processed
            self.processed_messages.add(content_hash)
            message.ack()
            
        except Exception as e:
            print(f"Processing failed: {e}")
            message.nack()
```

---

## Scenario-Based Questions

### Q19: How would you design a real-time analytics pipeline using Pub/Sub?
**Answer:**
**Architecture Design:**
```
Data Sources → Pub/Sub Topics → Dataflow → BigQuery → Data Studio
     ↓              ↓              ↓          ↓          ↓
Web Apps       Event Routing   Stream      Data       Real-time
Mobile Apps    & Filtering     Processing  Warehouse  Dashboards
IoT Devices
```

**Implementation:**
```python
# Multi-topic publisher for different event types
class AnalyticsPublisher:
    def __init__(self, project_id):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = project_id
        
        # Different topics for different event types
        self.topics = {
            'user_events': self.publisher.topic_path(project_id, 'user-events'),
            'system_events': self.publisher.topic_path(project_id, 'system-events'),
            'business_events': self.publisher.topic_path(project_id, 'business-events')
        }
    
    def publish_user_event(self, user_id, event_type, data):
        message_data = json.dumps({
            'user_id': user_id,
            'event_type': event_type,
            'data': data,
            'timestamp': time.time()
        })
        
        self.publisher.publish(
            self.topics['user_events'],
            message_data.encode('utf-8'),
            user_id=user_id,
            event_type=event_type
        )
```

### Q20: How would you implement a microservices communication pattern with Pub/Sub?
**Answer:**
**Event-Driven Architecture:**
```python
# Service A publishes events
class OrderService:
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic = self.publisher.topic_path('project-id', 'order-events')
    
    def create_order(self, order_data):
        # Create order in database
        order = self.save_order(order_data)
        
        # Publish order created event
        event = {
            'event_type': 'order_created',
            'order_id': order.id,
            'customer_id': order.customer_id,
            'total_amount': order.total,
            'timestamp': time.time()
        }
        
        self.publisher.publish(
            self.topic,
            json.dumps(event).encode('utf-8'),
            event_type='order_created',
            order_id=str(order.id)
        )

# Service B subscribes to events
class InventoryService:
    def __init__(self):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription = self.subscriber.subscription_path(
            'project-id', 'inventory-order-events'
        )
    
    def handle_order_event(self, message):
        event = json.loads(message.data.decode('utf-8'))
        
        if event['event_type'] == 'order_created':
            self.reserve_inventory(event['order_id'])
            
        message.ack()
    
    def start_listening(self):
        self.subscriber.subscribe(
            self.subscription,
            callback=self.handle_order_event
        )
```

---

## 🎯 Key Takeaways

- **Fully Managed**: Serverless messaging with automatic scaling
- **Global Scale**: Handle millions of messages per second globally
- **Reliable Delivery**: At-least-once delivery with durability guarantees
- **Flexible Patterns**: Support for pub-sub, push, and pull patterns
- **Rich Integration**: Seamless integration with Google Cloud services
- **Advanced Features**: Message ordering, filtering, and dead letter queues
- **Enterprise Security**: Comprehensive IAM and encryption support

Remember: Google Cloud Pub/Sub excels at building scalable, event-driven architectures with its fully managed, globally distributed messaging capabilities.