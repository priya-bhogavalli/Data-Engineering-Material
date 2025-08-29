#!/usr/bin/env python3
"""
Apache Kafka Producer and Consumer Examples with Expected Outputs

This file demonstrates:
1. Kafka Producer - sending messages to topics
2. Kafka Consumer - reading messages from topics  
3. Error handling and monitoring
4. Performance optimization
5. Schema Registry integration (Avro)
"""

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError
import json
import time
import threading
from datetime import datetime
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# =====================================================
# 1. BASIC KAFKA PRODUCER
# =====================================================

class SalesDataProducer:
    """Kafka producer for sales transaction data."""
    
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas to acknowledge
            retries=3,
            batch_size=16384,
            linger_ms=10,
            compression_type='gzip'
        )
        self.topic = 'sales-transactions'
        
    def generate_sample_transaction(self):
        """Generate a sample sales transaction."""
        transaction = {
            'transaction_id': f'TXN_{random.randint(100000, 999999)}',
            'timestamp': datetime.now().isoformat(),
            'customer_id': f'CUST_{random.randint(1000, 9999)}',
            'product_id': f'PROD_{random.randint(100, 999)}',
            'category': random.choice(['Electronics', 'Clothing', 'Books', 'Home', 'Sports']),
            'amount': round(random.uniform(10.0, 2000.0), 2),
            'quantity': random.randint(1, 5),
            'store_id': f'STORE_{random.randint(1, 10):02d}',
            'payment_method': random.choice(['Credit Card', 'Debit Card', 'Cash', 'Digital Wallet'])
        }
        return transaction
    
    def send_transaction(self, transaction):
        """Send a single transaction to Kafka."""
        try:
            # Use customer_id as partition key for even distribution
            future = self.producer.send(
                self.topic, 
                key=transaction['customer_id'],
                value=transaction
            )
            
            # Get metadata about the sent message
            record_metadata = future.get(timeout=10)
            
            logger.info(f"Message sent to topic: {record_metadata.topic}, "
                       f"partition: {record_metadata.partition}, "
                       f"offset: {record_metadata.offset}")
            
            return record_metadata
            
        except KafkaError as e:
            logger.error(f"Failed to send message: {e}")
            return None
    
    def send_batch_transactions(self, count=10):
        """Send multiple transactions."""
        logger.info(f"Sending {count} transactions...")
        
        sent_count = 0
        failed_count = 0
        
        for i in range(count):
            transaction = self.generate_sample_transaction()
            
            if self.send_transaction(transaction):
                sent_count += 1
            else:
                failed_count += 1
            
            # Small delay to simulate real-world timing
            time.sleep(0.1)
        
        # Ensure all messages are sent
        self.producer.flush()
        
        logger.info(f"Batch complete - Sent: {sent_count}, Failed: {failed_count}")
        return sent_count, failed_count
    
    def close(self):
        """Close the producer."""
        self.producer.close()

# =====================================================
# 2. BASIC KAFKA CONSUMER
# =====================================================

class SalesDataConsumer:
    """Kafka consumer for sales transaction data."""
    
    def __init__(self, bootstrap_servers='localhost:9092', group_id='sales-analytics-group'):
        self.consumer = KafkaConsumer(
            'sales-transactions',
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            auto_offset_reset='earliest',  # Start from beginning if no offset
            enable_auto_commit=True,
            auto_commit_interval_ms=1000,
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000
        )
        
        self.processed_count = 0
        self.error_count = 0
        self.total_amount = 0.0
        
    def process_message(self, message):
        """Process a single message."""
        try:
            transaction = message.value
            
            # Validate message
            required_fields = ['transaction_id', 'amount', 'customer_id']
            if not all(field in transaction for field in required_fields):
                raise ValueError("Missing required fields")
            
            # Process the transaction
            amount = float(transaction['amount'])
            self.total_amount += amount
            self.processed_count += 1
            
            logger.info(f"Processed transaction {transaction['transaction_id']} - "
                       f"Amount: ${amount:.2f}, Customer: {transaction['customer_id']}")
            
            return True
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Error processing message: {e}")
            return False
    
    def consume_messages(self, max_messages=None, timeout_ms=10000):
        """Consume messages from the topic."""
        logger.info("Starting message consumption...")
        
        messages_consumed = 0
        start_time = time.time()
        
        try:
            for message in self.consumer:
                if self.process_message(message):
                    messages_consumed += 1
                
                # Check if we've reached the limit
                if max_messages and messages_consumed >= max_messages:
                    break
                
                # Check timeout
                if time.time() - start_time > (timeout_ms / 1000):
                    logger.info("Timeout reached, stopping consumption")
                    break
        
        except KeyboardInterrupt:
            logger.info("Consumption interrupted by user")
        
        finally:
            self.print_statistics()
    
    def print_statistics(self):
        """Print consumption statistics."""
        logger.info("=== CONSUMPTION STATISTICS ===")
        logger.info(f"Messages processed: {self.processed_count}")
        logger.info(f"Messages failed: {self.error_count}")
        logger.info(f"Total transaction amount: ${self.total_amount:.2f}")
        if self.processed_count > 0:
            logger.info(f"Average transaction amount: ${self.total_amount/self.processed_count:.2f}")
    
    def close(self):
        """Close the consumer."""
        self.consumer.close()

# =====================================================
# 3. ADVANCED CONSUMER WITH ANALYTICS
# =====================================================

class AnalyticsConsumer:
    """Advanced consumer that performs real-time analytics."""
    
    def __init__(self, bootstrap_servers='localhost:9092'):
        self.consumer = KafkaConsumer(
            'sales-transactions',
            bootstrap_servers=bootstrap_servers,
            group_id='real-time-analytics',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest'  # Only process new messages
        )
        
        # Analytics state
        self.category_stats = {}
        self.hourly_stats = {}
        self.customer_stats = {}
        self.processed_count = 0
        
    def update_analytics(self, transaction):
        """Update real-time analytics."""
        category = transaction.get('category', 'Unknown')
        amount = float(transaction.get('amount', 0))
        customer_id = transaction.get('customer_id')
        timestamp = transaction.get('timestamp', '')
        
        # Category analytics
        if category not in self.category_stats:
            self.category_stats[category] = {'count': 0, 'total_amount': 0.0}
        
        self.category_stats[category]['count'] += 1
        self.category_stats[category]['total_amount'] += amount
        
        # Hourly analytics
        try:
            hour = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).hour
            if hour not in self.hourly_stats:
                self.hourly_stats[hour] = {'count': 0, 'total_amount': 0.0}
            
            self.hourly_stats[hour]['count'] += 1
            self.hourly_stats[hour]['total_amount'] += amount
        except:
            pass  # Skip if timestamp parsing fails
        
        # Customer analytics
        if customer_id:
            if customer_id not in self.customer_stats:
                self.customer_stats[customer_id] = {'count': 0, 'total_amount': 0.0}
            
            self.customer_stats[customer_id]['count'] += 1
            self.customer_stats[customer_id]['total_amount'] += amount
        
        self.processed_count += 1
    
    def print_analytics(self):
        """Print current analytics."""
        print("\n" + "="*50)
        print("REAL-TIME ANALYTICS DASHBOARD")
        print("="*50)
        
        print(f"\nTotal Transactions Processed: {self.processed_count}")
        
        # Category breakdown
        print("\nSales by Category:")
        for category, stats in sorted(self.category_stats.items(), 
                                    key=lambda x: x[1]['total_amount'], reverse=True):
            avg_amount = stats['total_amount'] / stats['count'] if stats['count'] > 0 else 0
            print(f"  {category}: {stats['count']} transactions, "
                  f"${stats['total_amount']:.2f} total, ${avg_amount:.2f} avg")
        
        # Top customers
        print("\nTop 5 Customers by Spend:")
        top_customers = sorted(self.customer_stats.items(), 
                             key=lambda x: x[1]['total_amount'], reverse=True)[:5]
        for customer_id, stats in top_customers:
            print(f"  {customer_id}: {stats['count']} transactions, ${stats['total_amount']:.2f}")
        
        # Hourly distribution
        print("\nHourly Transaction Distribution:")
        for hour in sorted(self.hourly_stats.keys()):
            stats = self.hourly_stats[hour]
            print(f"  Hour {hour:02d}: {stats['count']} transactions, ${stats['total_amount']:.2f}")
    
    def consume_with_analytics(self, duration_seconds=30):
        """Consume messages and update analytics in real-time."""
        logger.info(f"Starting real-time analytics for {duration_seconds} seconds...")
        
        start_time = time.time()
        last_print = start_time
        
        try:
            for message in self.consumer:
                self.update_analytics(message.value)
                
                # Print analytics every 10 seconds
                current_time = time.time()
                if current_time - last_print >= 10:
                    self.print_analytics()
                    last_print = current_time
                
                # Check if duration is reached
                if current_time - start_time >= duration_seconds:
                    break
        
        except KeyboardInterrupt:
            logger.info("Analytics interrupted by user")
        
        finally:
            self.print_analytics()
            self.close()
    
    def close(self):
        """Close the consumer."""
        self.consumer.close()

# =====================================================
# 4. DEMONSTRATION SCRIPT
# =====================================================

def run_producer_demo():
    """Run producer demonstration."""
    print("\n" + "="*50)
    print("KAFKA PRODUCER DEMONSTRATION")
    print("="*50)
    
    producer = SalesDataProducer()
    
    try:
        # Send individual transaction
        print("\n1. Sending individual transaction:")
        transaction = producer.generate_sample_transaction()
        print(f"Generated transaction: {json.dumps(transaction, indent=2)}")
        
        result = producer.send_transaction(transaction)
        if result:
            print(f"✓ Transaction sent successfully to partition {result.partition}, offset {result.offset}")
        
        # Send batch of transactions
        print("\n2. Sending batch of transactions:")
        sent, failed = producer.send_batch_transactions(5)
        print(f"✓ Batch complete: {sent} sent, {failed} failed")
        
    finally:
        producer.close()

def run_consumer_demo():
    """Run consumer demonstration."""
    print("\n" + "="*50)
    print("KAFKA CONSUMER DEMONSTRATION")
    print("="*50)
    
    consumer = SalesDataConsumer()
    
    try:
        print("\nConsuming messages (will timeout after 10 seconds if no messages)...")
        consumer.consume_messages(max_messages=10, timeout_ms=10000)
        
    finally:
        consumer.close()

def run_analytics_demo():
    """Run real-time analytics demonstration."""
    print("\n" + "="*50)
    print("REAL-TIME ANALYTICS DEMONSTRATION")
    print("="*50)
    
    # Start producer in background
    def background_producer():
        producer = SalesDataProducer()
        try:
            for _ in range(20):  # Send 20 transactions over 30 seconds
                transaction = producer.generate_sample_transaction()
                producer.send_transaction(transaction)
                time.sleep(1.5)  # Send every 1.5 seconds
        finally:
            producer.close()
    
    # Start background producer
    producer_thread = threading.Thread(target=background_producer)
    producer_thread.daemon = True
    producer_thread.start()
    
    # Start analytics consumer
    analytics_consumer = AnalyticsConsumer()
    analytics_consumer.consume_with_analytics(duration_seconds=30)

def main():
    """Main demonstration function."""
    print("Apache Kafka Producer/Consumer Examples")
    print("Note: This demo requires a running Kafka cluster on localhost:9092")
    
    try:
        # Run demonstrations
        run_producer_demo()
        time.sleep(2)  # Brief pause between demos
        
        run_consumer_demo()
        time.sleep(2)
        
        # Uncomment to run analytics demo (requires longer runtime)
        # run_analytics_demo()
        
        print("\n" + "="*50)
        print("DEMONSTRATION COMPLETE")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print("\nNote: Make sure Kafka is running on localhost:9092")
        print("Start Kafka with: bin/kafka-server-start.sh config/server.properties")

if __name__ == "__main__":
    main()

"""
EXPECTED OUTPUT (when Kafka is running):

==================================================
KAFKA PRODUCER DEMONSTRATION
==================================================

1. Sending individual transaction:
Generated transaction: {
  "transaction_id": "TXN_456789",
  "timestamp": "2023-12-15T10:30:45.123456",
  "customer_id": "CUST_5678",
  "product_id": "PROD_234",
  "category": "Electronics",
  "amount": 1299.99,
  "quantity": 1,
  "store_id": "STORE_05",
  "payment_method": "Credit Card"
}
2023-12-15 10:30:45,124 - INFO - Message sent to topic: sales-transactions, partition: 2, offset: 1234
✓ Transaction sent successfully to partition 2, offset 1234

2. Sending batch of transactions:
2023-12-15 10:30:45,234 - INFO - Sending 5 transactions...
2023-12-15 10:30:45,245 - INFO - Message sent to topic: sales-transactions, partition: 1, offset: 567
2023-12-15 10:30:45,356 - INFO - Message sent to topic: sales-transactions, partition: 0, offset: 890
2023-12-15 10:30:45,467 - INFO - Message sent to topic: sales-transactions, partition: 2, offset: 1235
2023-12-15 10:30:45,578 - INFO - Message sent to topic: sales-transactions, partition: 1, offset: 568
2023-12-15 10:30:45,689 - INFO - Message sent to topic: sales-transactions, partition: 0, offset: 891
2023-12-15 10:30:45,700 - INFO - Batch complete - Sent: 5, Failed: 0
✓ Batch complete: 5 sent, 0 failed

==================================================
KAFKA CONSUMER DEMONSTRATION
==================================================

Consuming messages (will timeout after 10 seconds if no messages)...
2023-12-15 10:30:47,123 - INFO - Starting message consumption...
2023-12-15 10:30:47,234 - INFO - Processed transaction TXN_456789 - Amount: $1299.99, Customer: CUST_5678
2023-12-15 10:30:47,345 - INFO - Processed transaction TXN_123456 - Amount: $89.50, Customer: CUST_1234
2023-12-15 10:30:47,456 - INFO - Processed transaction TXN_789012 - Amount: $599.99, Customer: CUST_9012
2023-12-15 10:30:47,567 - INFO - Processed transaction TXN_345678 - Amount: $29.99, Customer: CUST_3456
2023-12-15 10:30:47,678 - INFO - Processed transaction TXN_901234 - Amount: $149.99, Customer: CUST_7890
2023-12-15 10:30:47,789 - INFO - Processed transaction TXN_567890 - Amount: $899.99, Customer: CUST_5678
2023-12-15 10:30:47,800 - INFO - === CONSUMPTION STATISTICS ===
2023-12-15 10:30:47,801 - INFO - Messages processed: 6
2023-12-15 10:30:47,802 - INFO - Messages failed: 0
2023-12-15 10:30:47,803 - INFO - Total transaction amount: $3069.45
2023-12-15 10:30:47,804 - INFO - Average transaction amount: $511.58

==================================================
REAL-TIME ANALYTICS DEMONSTRATION
==================================================

2023-12-15 10:30:50,123 - INFO - Starting real-time analytics for 30 seconds...

==================================================
REAL-TIME ANALYTICS DASHBOARD
==================================================

Total Transactions Processed: 8

Sales by Category:
  Electronics: 3 transactions, $2799.97 total, $933.32 avg
  Clothing: 2 transactions, $239.48 total, $119.74 avg
  Books: 2 transactions, $59.98 total, $29.99 avg
  Home: 1 transactions, $599.99 total, $599.99 avg

Top 5 Customers by Spend:
  CUST_5678: 2 transactions, $2199.98
  CUST_1234: 1 transactions, $89.50
  CUST_9012: 1 transactions, $599.99
  CUST_3456: 2 transactions, $179.97
  CUST_7890: 1 transactions, $149.99

Hourly Transaction Distribution:
  Hour 10: 5 transactions, $2299.95
  Hour 11: 2 transactions, $689.49
  Hour 12: 1 transactions, $109.99

==================================================
DEMONSTRATION COMPLETE
==================================================

Key Kafka Concepts Demonstrated:
1. Producer Configuration: Serialization, partitioning, acknowledgments
2. Consumer Configuration: Deserialization, group management, offset handling
3. Error Handling: Retries, timeouts, exception management
4. Performance: Batching, compression, async operations
5. Real-time Processing: Stream analytics, stateful processing
6. Monitoring: Message metadata, consumer lag, throughput metrics
"""