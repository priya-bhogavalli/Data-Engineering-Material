# 🎯 Google Pub/Sub Interview Questions

**Difficulty Levels**: 🟢 Beginner | 🟡 Intermediate | 🔴 Advanced  
**Total Questions**: 50+  
**Interview Frequency**: 40% of data engineering roles

---

## 🟢 Beginner Level Questions

### **Q1: What is Google Pub/Sub and how does it work?**

**Answer:**
Google Pub/Sub is a fully managed real-time messaging service that enables asynchronous communication between applications using a publish-subscribe pattern.

**Core Components**:
- **Topics**: Named channels where messages are published
- **Subscriptions**: Named resources that represent message streams from topics
- **Publishers**: Applications that send messages to topics
- **Subscribers**: Applications that receive messages from subscriptions

**Message Flow**:
```
Publisher → Topic → Subscription → Subscriber
```

**Key Features**:
- At-least-once delivery guarantee
- Global scale with automatic scaling
- Message retention up to 7 days
- Dead letter queues for failed messages
- Exactly-once delivery (premium feature)

---

### **Q2: What's the difference between pull and push subscriptions?**

**Answer:**
Pub/Sub offers two delivery methods for subscriptions:

| **Aspect** | **Pull Subscription** | **Push Subscription** |
|------------|----------------------|----------------------|
| **Delivery** | Subscriber requests messages | Pub/Sub sends to HTTP endpoint |
| **Control** | Subscriber controls rate | Pub/Sub controls delivery |
| **Scalability** | Manual scaling | Automatic scaling |
| **Latency** | Higher (polling) | Lower (immediate push) |
| **Error Handling** | Client-side | HTTP response codes |

**Pull Example**:
```python
def pull_messages():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("project", "subscription")
    
    def callback(message):
        print(f"Received: {message.data.decode('utf-8')}")
        message.ack()
    
    subscriber.subscribe(subscription_path, callback=callback)
```

**Push Example**:
```python
# Push endpoint configuration
push_config = pubsub_v1.PushConfig(
    push_endpoint="https://myapp.com/webhook"
)

subscriber.create_subscription(
    request={
        "name": subscription_path,
        "topic": topic_path,
        "push_config": push_config
    }
)
```

---

### **Q3: How do you publish messages to Pub/Sub?**

**Answer:**
Messages can be published synchronously or asynchronously:

**Basic Publishing**:
```python
from google.cloud import pubsub_v1
import json

def publish_message():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("my-project", "my-topic")
    
    # Message data
    data = json.dumps({
        "user_id": 123,
        "event": "user_login",
        "timestamp": "2024-01-15T10:30:00Z"
    }).encode("utf-8")
    
    # Publish with attributes
    future = publisher.publish(
        topic_path,
        data,
        user_id="123",
        event_type="login"
    )
    
    message_id = future.result()  # Block until published
    print(f"Published message ID: {message_id}")
```

**Batch Publishing**:
```python
def publish_batch():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("my-project", "events")
    
    futures = []
    for i in range(100):
        data = json.dumps({"id": i, "data": f"message-{i}"}).encode("utf-8")
        future = publisher.publish(topic_path, data)
        futures.append(future)
    
    # Wait for all messages
    for future in futures:
        message_id = future.result()
        print(f"Published: {message_id}")
```

---

### **Q4: What are message attributes and when would you use them?**

**Answer:**
Message attributes are key-value pairs that provide metadata about messages without being part of the message payload.

**Use Cases**:
- **Filtering**: Subscribers can filter messages based on attributes
- **Routing**: Route messages to different handlers
- **Metadata**: Store additional information without parsing payload

**Example**:
```python
def publish_with_attributes():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("my-project", "user-events")
    
    # Message with attributes
    data = json.dumps({"action": "purchase", "amount": 99.99}).encode("utf-8")
    
    future = publisher.publish(
        topic_path,
        data,
        # Attributes for filtering/routing
        user_type="premium",
        region="us-east",
        event_category="transaction",
        priority="high"
    )
    
    return future.result()

# Subscriber can filter based on attributes
def filtered_subscriber():
    def callback(message):
        # Access attributes
        user_type = message.attributes.get("user_type")
        region = message.attributes.get("region")
        
        if user_type == "premium":
            process_premium_user(message)
        
        message.ack()
```

---

### **Q5: How do you handle message acknowledgments?**

**Answer:**
Message acknowledgment tells Pub/Sub that a message has been successfully processed:

**Acknowledgment Types**:
- **ack()**: Message processed successfully
- **nack()**: Message processing failed, redeliver
- **modify_ack_deadline()**: Extend processing time

**Example**:
```python
def handle_acknowledgments():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("project", "subscription")
    
    def callback(message):
        try:
            # Process message
            result = process_message(message.data)
            
            if result.success:
                message.ack()  # Success
            else:
                message.nack()  # Failed, redeliver
                
        except Exception as e:
            print(f"Processing error: {e}")
            # Extend deadline if need more time
            message.modify_ack_deadline(60)  # 60 seconds
            
            # Or nack to redeliver
            message.nack()
    
    # Configure acknowledgment deadline
    subscriber.subscribe(
        subscription_path, 
        callback=callback,
        flow_control=pubsub_v1.types.FlowControl(max_messages=10)
    )
```

---

## 🟡 Intermediate Level Questions

### **Q6: How do you implement exactly-once delivery in Pub/Sub?**

**Answer:**
Pub/Sub offers exactly-once delivery as a premium feature, but you can also implement it at the application level:

**1. Enable Exactly-Once Delivery**:
```python
def create_exactly_once_subscription():
    subscriber = pubsub_v1.SubscriberClient()
    
    subscription = subscriber.create_subscription(
        request={
            "name": subscriber.subscription_path("project", "exactly-once-sub"),
            "topic": publisher.topic_path("project", "topic"),
            "enable_exactly_once_delivery": True
        }
    )
    
    return subscription
```

**2. Application-Level Deduplication**:
```python
import hashlib
from google.cloud import firestore

class ExactlyOnceProcessor:
    def __init__(self):
        self.db = firestore.Client()
        self.processed_collection = self.db.collection('processed_messages')
    
    def generate_message_id(self, message):
        # Create deterministic ID from message content
        content = f"{message.message_id}-{message.data.decode('utf-8')}"
        return hashlib.sha256(content.encode()).hexdigest()
    
    def process_exactly_once(self, message):
        message_id = self.generate_message_id(message)
        
        # Check if already processed
        doc_ref = self.processed_collection.document(message_id)
        doc = doc_ref.get()
        
        if doc.exists:
            print(f"Message {message_id} already processed")
            message.ack()
            return
        
        try:
            # Process message
            result = self.process_business_logic(message)
            
            # Mark as processed atomically
            doc_ref.set({
                'message_id': message_id,
                'processed_at': firestore.SERVER_TIMESTAMP,
                'result': result
            })
            
            message.ack()
            
        except Exception as e:
            print(f"Processing failed: {e}")
            message.nack()
```

---

### **Q7: How do you implement message ordering in Pub/Sub?**

**Answer:**
Pub/Sub supports message ordering using ordering keys:

**1. Publishing with Ordering Keys**:
```python
def publish_ordered_messages():
    # Enable message ordering
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("my-project", "ordered-topic")
    
    # Messages with same ordering key are delivered in order
    user_id = "user-123"
    
    # Publish sequence of events for same user
    events = [
        {"event": "login", "timestamp": 1},
        {"event": "view_page", "timestamp": 2},
        {"event": "purchase", "timestamp": 3},
        {"event": "logout", "timestamp": 4}
    ]
    
    futures = []
    for event in events:
        data = json.dumps(event).encode("utf-8")
        
        future = publisher.publish(
            topic_path,
            data,
            ordering_key=user_id  # Same ordering key
        )
        futures.append(future)
    
    # Wait for all messages
    for future in futures:
        future.result()
```

**2. Consuming Ordered Messages**:
```python
def consume_ordered_messages():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path("project", "ordered-sub")
    
    def callback(message):
        ordering_key = message.ordering_key
        data = json.loads(message.data.decode('utf-8'))
        
        print(f"Processing ordered message for {ordering_key}: {data}")
        
        # Process in order
        process_user_event(ordering_key, data)
        message.ack()
    
    # Enable receive settings for ordering
    subscriber.subscribe(
        subscription_path,
        callback=callback,
        flow_control=pubsub_v1.types.FlowControl(
            max_messages=100,
            use_legacy_flow_control=True
        )
    )
```

**3. Handling Ordering Key Failures**:
```python
def handle_ordering_failures():
    def callback(message):
        try:
            process_message(message)
            message.ack()
        except Exception as e:
            print(f"Failed to process message: {e}")
            
            # For ordered messages, nack stops delivery for that ordering key
            # Consider dead letter queue for persistent failures
            if should_retry(e):
                message.nack()
            else:
                # Send to dead letter queue and ack
                send_to_dead_letter_queue(message)
                message.ack()
```

---

### **Q8: How do you implement dead letter queues in Pub/Sub?**

**Answer:**
Dead letter queues handle messages that can't be processed successfully:

**1. Create Dead Letter Queue Setup**:
```python
def setup_dead_letter_queue():
    publisher = pubsub_v1.PublisherClient()
    subscriber = pubsub_v1.SubscriberClient()
    
    # Create dead letter topic
    dead_letter_topic_path = publisher.topic_path("project", "dead-letter-topic")
    publisher.create_topic(request={"name": dead_letter_topic_path})
    
    # Create main subscription with dead letter policy
    main_subscription_path = subscriber.subscription_path("project", "main-sub")
    
    dead_letter_policy = pubsub_v1.DeadLetterPolicy(
        dead_letter_topic=dead_letter_topic_path,
        max_delivery_attempts=5
    )
    
    subscription = subscriber.create_subscription(
        request={
            "name": main_subscription_path,
            "topic": publisher.topic_path("project", "main-topic"),
            "dead_letter_policy": dead_letter_policy,
            "ack_deadline_seconds": 60
        }
    )
    
    # Create dead letter subscription
    dead_letter_sub_path = subscriber.subscription_path("project", "dead-letter-sub")
    subscriber.create_subscription(
        request={
            "name": dead_letter_sub_path,
            "topic": dead_letter_topic_path
        }
    )
```

**2. Process Dead Letter Messages**:
```python
def process_dead_letter_messages():
    subscriber = pubsub_v1.SubscriberClient()
    dead_letter_sub_path = subscriber.subscription_path("project", "dead-letter-sub")
    
    def dead_letter_callback(message):
        print(f"Processing dead letter message: {message.message_id}")
        
        # Extract original message info
        original_data = message.data.decode('utf-8')
        delivery_attempt = message.delivery_attempt
        
        # Log for analysis
        log_failed_message(original_data, delivery_attempt)
        
        # Optionally retry with different logic
        if should_retry_dead_letter(message):
            republish_to_main_topic(original_data)
        
        message.ack()
    
    subscriber.subscribe(dead_letter_sub_path, callback=dead_letter_callback)
```

---

## 🔴 Advanced Level Questions

### **Q9: How would you design a multi-region Pub/Sub architecture?**

**Answer:**
Multi-region Pub/Sub architecture for global applications:

**1. Regional Topic Strategy**:
```python
class MultiRegionPubSub:
    def __init__(self):
        self.regions = ["us-central1", "europe-west1", "asia-east1"]
        self.publishers = {}
        self.subscribers = {}
        
        for region in self.regions:
            # Create regional clients
            self.publishers[region] = pubsub_v1.PublisherClient()
            self.subscribers[region] = pubsub_v1.SubscriberClient()
    
    def publish_to_nearest_region(self, user_location, message_data):
        # Determine nearest region based on user location
        nearest_region = self.get_nearest_region(user_location)
        
        publisher = self.publishers[nearest_region]
        topic_path = publisher.topic_path("project", f"events-{nearest_region}")
        
        # Add region metadata
        future = publisher.publish(
            topic_path,
            message_data,
            source_region=nearest_region,
            user_location=user_location
        )
        
        return future.result()
    
    def setup_cross_region_replication(self):
        # Replicate messages across regions for disaster recovery
        for source_region in self.regions:
            for target_region in self.regions:
                if source_region != target_region:
                    self.setup_replication_subscription(source_region, target_region)
    
    def setup_replication_subscription(self, source_region, target_region):
        subscriber = self.subscribers[source_region]
        publisher = self.publishers[target_region]
        
        source_topic = f"events-{source_region}"
        target_topic = f"events-{target_region}-replica"
        
        subscription_path = subscriber.subscription_path(
            "project", f"replication-{source_region}-to-{target_region}"
        )
        
        def replication_callback(message):
            # Add replication metadata
            replicated_data = {
                "original_data": message.data.decode('utf-8'),
                "source_region": source_region,
                "replicated_at": time.time()
            }
            
            # Publish to target region
            target_topic_path = publisher.topic_path("project", target_topic)
            publisher.publish(
                target_topic_path,
                json.dumps(replicated_data).encode('utf-8'),
                replication_source=source_region
            )
            
            message.ack()
        
        subscriber.subscribe(subscription_path, callback=replication_callback)
```

**2. Global Message Routing**:
```python
class GlobalMessageRouter:
    def __init__(self):
        self.region_mappings = {
            "US": "us-central1",
            "EU": "europe-west1", 
            "ASIA": "asia-east1"
        }
    
    def route_message_globally(self, message, routing_strategy="nearest"):
        if routing_strategy == "nearest":
            return self.route_to_nearest_region(message)
        elif routing_strategy == "broadcast":
            return self.broadcast_to_all_regions(message)
        elif routing_strategy == "primary_backup":
            return self.route_with_backup(message)
    
    def route_to_nearest_region(self, message):
        user_region = message.attributes.get("user_region", "US")
        target_region = self.region_mappings.get(user_region, "us-central1")
        
        publisher = self.publishers[target_region]
        topic_path = publisher.topic_path("project", f"events-{target_region}")
        
        return publisher.publish(topic_path, message.data)
    
    def broadcast_to_all_regions(self, message):
        futures = []
        for region in self.regions:
            publisher = self.publishers[region]
            topic_path = publisher.topic_path("project", f"events-{region}")
            future = publisher.publish(topic_path, message.data)
            futures.append(future)
        
        return futures
```

---

### **Q10: How do you implement complex event processing with Pub/Sub?**

**Answer:**
Complex event processing (CEP) with Pub/Sub for real-time analytics:

**1. Event Correlation Engine**:
```python
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Event:
    user_id: str
    event_type: str
    timestamp: float
    data: dict

class ComplexEventProcessor:
    def __init__(self):
        self.user_sessions = defaultdict(deque)  # Store events per user
        self.pattern_rules = []
        self.time_window = 300  # 5 minutes
    
    def add_pattern_rule(self, pattern_name, events_sequence, time_window, action):
        """Add a pattern rule for event correlation"""
        self.pattern_rules.append({
            'name': pattern_name,
            'sequence': events_sequence,
            'window': time_window,
            'action': action
        })
    
    def process_event(self, message):
        event_data = json.loads(message.data.decode('utf-8'))
        event = Event(
            user_id=event_data['user_id'],
            event_type=event_data['event_type'],
            timestamp=time.time(),
            data=event_data
        )
        
        # Add to user session
        self.user_sessions[event.user_id].append(event)
        
        # Clean old events
        self.cleanup_old_events(event.user_id)
        
        # Check for pattern matches
        self.check_patterns(event.user_id)
        
        message.ack()
    
    def check_patterns(self, user_id):
        user_events = list(self.user_sessions[user_id])
        
        for rule in self.pattern_rules:
            if self.matches_pattern(user_events, rule):
                rule['action'](user_id, user_events, rule)
    
    def matches_pattern(self, events, rule):
        """Check if events match the pattern sequence"""
        sequence = rule['sequence']
        window = rule['window']
        
        if len(events) < len(sequence):
            return False
        
        # Find matching sequence within time window
        for i in range(len(events) - len(sequence) + 1):
            window_events = events[i:i+len(sequence)]
            
            # Check if events are within time window
            if window_events[-1].timestamp - window_events[0].timestamp <= window:
                # Check if sequence matches
                if all(event.event_type == expected_type 
                      for event, expected_type in zip(window_events, sequence)):
                    return True
        
        return False

# Usage example
def setup_fraud_detection():
    processor = ComplexEventProcessor()
    
    # Define fraud pattern: login -> high_value_purchase -> logout within 2 minutes
    def fraud_alert_action(user_id, events, rule):
        print(f"FRAUD ALERT: Suspicious pattern detected for user {user_id}")
        
        # Publish alert to fraud detection topic
        publisher = pubsub_v1.PublisherClient()
        alert_topic = publisher.topic_path("project", "fraud-alerts")
        
        alert_data = {
            "user_id": user_id,
            "pattern": rule['name'],
            "events": [{"type": e.event_type, "timestamp": e.timestamp} for e in events],
            "risk_score": calculate_risk_score(events)
        }
        
        publisher.publish(alert_topic, json.dumps(alert_data).encode('utf-8'))
    
    processor.add_pattern_rule(
        pattern_name="rapid_high_value_transaction",
        events_sequence=["login", "high_value_purchase", "logout"],
        time_window=120,  # 2 minutes
        action=fraud_alert_action
    )
    
    return processor
```

**2. Real-time Aggregation**:
```python
class RealTimeAggregator:
    def __init__(self):
        self.time_windows = {
            "1min": 60,
            "5min": 300,
            "15min": 900
        }
        self.aggregations = defaultdict(lambda: defaultdict(dict))
    
    def process_metric_event(self, message):
        event_data = json.loads(message.data.decode('utf-8'))
        
        metric_name = event_data['metric']
        value = event_data['value']
        timestamp = time.time()
        
        # Update aggregations for all time windows
        for window_name, window_size in self.time_windows.items():
            window_start = int(timestamp // window_size) * window_size
            
            if window_start not in self.aggregations[metric_name][window_name]:
                self.aggregations[metric_name][window_name][window_start] = {
                    'count': 0,
                    'sum': 0,
                    'min': float('inf'),
                    'max': float('-inf')
                }
            
            agg = self.aggregations[metric_name][window_name][window_start]
            agg['count'] += 1
            agg['sum'] += value
            agg['min'] = min(agg['min'], value)
            agg['max'] = max(agg['max'], value)
            
            # Publish aggregated metrics
            if agg['count'] % 100 == 0:  # Every 100 events
                self.publish_aggregated_metric(metric_name, window_name, window_start, agg)
        
        message.ack()
    
    def publish_aggregated_metric(self, metric_name, window_name, window_start, agg):
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path("project", "aggregated-metrics")
        
        aggregated_data = {
            "metric": metric_name,
            "window": window_name,
            "window_start": window_start,
            "count": agg['count'],
            "sum": agg['sum'],
            "avg": agg['sum'] / agg['count'],
            "min": agg['min'],
            "max": agg['max']
        }
        
        publisher.publish(topic_path, json.dumps(aggregated_data).encode('utf-8'))
```

This advanced implementation demonstrates how Pub/Sub can be used for sophisticated real-time event processing scenarios.

---

## 🎯 Interview Tips

### **Preparation Strategy**
1. **Hands-on Experience**: Create topics/subscriptions and practice publishing/consuming
2. **Architecture Understanding**: Know topics, subscriptions, and delivery guarantees
3. **Integration Patterns**: Learn GCP ecosystem integrations (Dataflow, Cloud Functions)
4. **Performance Optimization**: Understand batching, flow control, and scaling
5. **Advanced Features**: Practice with ordering keys, dead letter queues, exactly-once delivery

### **Key Points to Emphasize**
- Fully managed GCP service
- Global scale with automatic scaling
- At-least-once and exactly-once delivery options
- Message ordering capabilities
- Integration with GCP ecosystem
- Dead letter queue support

---

**🎯 Ready for your interview?** Practice these scenarios and understand the trade-offs between different messaging patterns.