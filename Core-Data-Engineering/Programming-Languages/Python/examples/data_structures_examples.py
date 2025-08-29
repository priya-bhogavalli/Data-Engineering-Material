"""
Python Data Structures - Practical Examples
"""

from collections import Counter, defaultdict, deque, namedtuple
import heapq
from queue import Queue, PriorityQueue

# 1. LIST EXAMPLES
def list_operations():
    """Common list operations for data processing"""
    
    # Data cleaning
    data = [1, 2, None, 4, 5, None, 7]
    cleaned = [x for x in data if x is not None]
    
    # Batch processing
    batch_size = 3
    batches = [data[i:i+batch_size] for i in range(0, len(data), batch_size)]
    
    # Finding duplicates
    numbers = [1, 2, 3, 2, 4, 1, 5]
    seen = set()
    duplicates = [x for x in numbers if x in seen or seen.add(x)]
    
    print(f"Cleaned data: {cleaned}")
    print(f"Batches: {batches}")
    print(f"Unique numbers: {list(seen)}")
    # Output: Cleaned data: [1, 2, 4, 5, 7]
    # Output: Batches: [[1, 2, None], [4, 5, None], [7]]
    # Output: Unique numbers: [1, 2, 3, 4, 5]
    
    return cleaned, batches, list(seen)

# 2. DICTIONARY EXAMPLES
def dict_operations():
    """Dictionary patterns for data engineering"""
    
    # Data aggregation
    sales_data = [
        {"region": "North", "amount": 100},
        {"region": "South", "amount": 150},
        {"region": "North", "amount": 200}
    ]
    
    # Group by region
    region_totals = {}
    for sale in sales_data:
        region = sale["region"]
        region_totals[region] = region_totals.get(region, 0) + sale["amount"]
    
    # Configuration mapping
    config = {
        "database": {"host": "localhost", "port": 5432},
        "api": {"timeout": 30, "retries": 3}
    }
    
    print(f"Region totals: {region_totals}")
    print(f"Database config: {config['database']}")
    # Output: Region totals: {'North': 300, 'South': 150}
    # Output: Database config: {'host': 'localhost', 'port': 5432}
    
    return region_totals, config

# 3. SET EXAMPLES
def set_operations():
    """Set operations for data deduplication and analysis"""
    
    # Data deduplication
    user_ids_day1 = {1, 2, 3, 4, 5}
    user_ids_day2 = {4, 5, 6, 7, 8}
    
    # Analytics
    returning_users = user_ids_day1 & user_ids_day2
    new_users = user_ids_day2 - user_ids_day1
    total_unique = user_ids_day1 | user_ids_day2
    
    print(f"Returning users: {returning_users}")
    print(f"New users: {new_users}")
    print(f"Total unique users: {total_unique}")
    # Output: Returning users: {4, 5}
    # Output: New users: {6, 7, 8}
    # Output: Total unique users: {1, 2, 3, 4, 5, 6, 7, 8}
    
    return returning_users, new_users, total_unique

# 4. COUNTER EXAMPLES
def counter_operations():
    """Counter for frequency analysis"""
    
    # Word frequency
    text = "the quick brown fox jumps over the lazy dog"
    word_counts = Counter(text.split())
    
    # Event counting
    events = ["login", "logout", "login", "purchase", "login"]
    event_counts = Counter(events)
    
    # Top N analysis
    top_words = word_counts.most_common(3)
    
    print(f"Word counts: {dict(word_counts)}")
    print(f"Event counts: {dict(event_counts)}")
    print(f"Top 3 words: {top_words}")
    # Output: Word counts: {'the': 2, 'quick': 1, 'brown': 1, 'fox': 1, 'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1}
    # Output: Event counts: {'login': 3, 'logout': 1, 'purchase': 1}
    # Output: Top 3 words: [('the', 2), ('quick', 1), ('brown', 1)]
    
    return word_counts, event_counts, top_words

# 5. DEFAULTDICT EXAMPLES
def defaultdict_operations():
    """defaultdict for grouping and aggregation"""
    
    # Group transactions by user
    transactions = [
        {"user_id": 1, "amount": 100},
        {"user_id": 2, "amount": 50},
        {"user_id": 1, "amount": 75}
    ]
    
    user_transactions = defaultdict(list)
    for txn in transactions:
        user_transactions[txn["user_id"]].append(txn["amount"])
    
    # Count by category
    items = ["apple", "banana", "apple", "cherry", "banana"]
    category_counts = defaultdict(int)
    for item in items:
        category_counts[item] += 1
    
    print(f"User transactions: {dict(user_transactions)}")
    print(f"Category counts: {dict(category_counts)}")
    # Output: User transactions: {1: [100, 75], 2: [50]}
    # Output: Category counts: {'apple': 2, 'banana': 2, 'cherry': 1}
    
    return dict(user_transactions), dict(category_counts)

# 6. DEQUE EXAMPLES
def deque_operations():
    """deque for sliding windows and queues"""
    
    # Sliding window for moving average
    window_size = 3
    data_stream = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    window = deque(maxlen=window_size)
    moving_averages = []
    
    for value in data_stream:
        window.append(value)
        if len(window) == window_size:
            avg = sum(window) / len(window)
            moving_averages.append(avg)
    
    # Task queue
    task_queue = deque(["task1", "task2", "task3"])
    task_queue.appendleft("urgent_task")  # Add high priority
    
    print(f"Moving averages: {moving_averages}")
    print(f"Task queue: {list(task_queue)}")
    # Output: Moving averages: [2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    # Output: Task queue: ['urgent_task', 'task1', 'task2', 'task3']
    
    return moving_averages, list(task_queue)

# 7. HEAP EXAMPLES
def heap_operations():
    """Heap for priority processing"""
    
    # Top K elements
    numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    k = 3
    top_k = heapq.nlargest(k, numbers)
    bottom_k = heapq.nsmallest(k, numbers)
    
    # Priority task processing
    tasks = [(1, "critical"), (5, "low"), (2, "high"), (3, "medium")]
    heapq.heapify(tasks)
    
    processed_order = []
    while tasks:
        priority, task = heapq.heappop(tasks)
        processed_order.append(task)
    
    print(f"Top {k} elements: {top_k}")
    print(f"Bottom {k} elements: {bottom_k}")
    print(f"Task processing order: {processed_order}")
    # Output: Top 3 elements: [9, 6, 5]
    # Output: Bottom 3 elements: [1, 1, 2]
    # Output: Task processing order: ['critical', 'high', 'medium', 'low']
    
    return top_k, bottom_k, processed_order

# 8. NAMEDTUPLE EXAMPLES
def namedtuple_operations():
    """namedtuple for structured data"""
    
    # Data record
    Record = namedtuple("Record", ["id", "timestamp", "value"])
    
    # Create records
    records = [
        Record(1, "2024-01-01", 100),
        Record(2, "2024-01-02", 150),
        Record(3, "2024-01-03", 200)
    ]
    
    # Process records
    total_value = sum(record.value for record in records)
    
    # Configuration
    Config = namedtuple("Config", ["host", "port", "database"])
    db_config = Config("localhost", 5432, "mydb")
    
    print(f"Records: {records}")
    print(f"Total value: {total_value}")
    print(f"DB config: {db_config}")
    # Output: Records: [Record(id=1, timestamp='2024-01-01', value=100), Record(id=2, timestamp='2024-01-02', value=150), Record(id=3, timestamp='2024-01-03', value=200)]
    # Output: Total value: 450
    # Output: DB config: Config(host='localhost', port=5432, database='mydb')
    
    return records, total_value, db_config

# 9. QUEUE EXAMPLES
def queue_operations():
    """Queue for thread-safe operations"""
    
    # Task processing queue
    task_queue = Queue()
    
    # Add tasks
    tasks = ["process_file1", "process_file2", "process_file3"]
    for task in tasks:
        task_queue.put(task)
    
    # Process tasks
    processed = []
    while not task_queue.empty():
        task = task_queue.get()
        processed.append(f"completed_{task}")
    
    # Priority queue for job scheduling
    job_queue = PriorityQueue()
    jobs = [(1, "backup"), (3, "cleanup"), (2, "sync")]
    
    for priority, job in jobs:
        job_queue.put((priority, job))
    
    job_order = []
    while not job_queue.empty():
        priority, job = job_queue.get()
        job_order.append(job)
    
    print(f"Processed tasks: {processed}")
    print(f"Job execution order: {job_order}")
    # Output: Processed tasks: ['completed_process_file1', 'completed_process_file2', 'completed_process_file3']
    # Output: Job execution order: ['backup', 'sync', 'cleanup']
    
    return processed, job_order

# 10. REAL-WORLD DATA PIPELINE EXAMPLE
def data_pipeline_example():
    """Complete data processing pipeline using multiple structures"""
    
    # Raw data
    raw_data = [
        {"user_id": 1, "event": "login", "timestamp": "2024-01-01"},
        {"user_id": 2, "event": "purchase", "timestamp": "2024-01-01"},
        {"user_id": 1, "event": "logout", "timestamp": "2024-01-01"},
        {"user_id": 3, "event": "login", "timestamp": "2024-01-02"},
        {"user_id": 2, "event": "login", "timestamp": "2024-01-02"}
    ]
    
    # 1. Deduplicate users
    unique_users = set(record["user_id"] for record in raw_data)
    
    # 2. Count events
    event_counts = Counter(record["event"] for record in raw_data)
    
    # 3. Group by user
    user_events = defaultdict(list)
    for record in raw_data:
        user_events[record["user_id"]].append(record["event"])
    
    # 4. Create user sessions
    Session = namedtuple("Session", ["user_id", "events", "event_count"])
    sessions = []
    for user_id, events in user_events.items():
        session = Session(user_id, events, len(events))
        sessions.append(session)
    
    # 5. Find top active users
    top_users = heapq.nlargest(2, sessions, key=lambda x: x.event_count)
    
    result = {
        "unique_users": len(unique_users),
        "event_counts": dict(event_counts),
        "user_sessions": len(sessions),
        "top_users": [(s.user_id, s.event_count) for s in top_users]
    }
    
    print(f"Pipeline analysis: {result}")
    # Output: Pipeline analysis: {'unique_users': 3, 'event_counts': {'login': 3, 'purchase': 1, 'logout': 1}, 'user_sessions': 3, 'top_users': [(1, 2), (2, 2)]}
    
    return result

if __name__ == "__main__":
    # Run examples
    print("=== LIST OPERATIONS ===")
    cleaned, batches, seen = list_operations()
    print(f"Cleaned: {cleaned}")
    print(f"Batches: {batches}")
    
    print("\n=== DICTIONARY OPERATIONS ===")
    totals, config = dict_operations()
    print(f"Region totals: {totals}")
    
    print("\n=== SET OPERATIONS ===")
    returning, new, total = set_operations()
    print(f"Returning users: {returning}")
    print(f"New users: {new}")
    
    print("\n=== COUNTER OPERATIONS ===")
    words, events, top = counter_operations()
    print(f"Top words: {top}")
    
    print("\n=== DEQUE OPERATIONS ===")
    averages, tasks = deque_operations()
    print(f"Moving averages: {averages[:3]}")
    
    print("\n=== HEAP OPERATIONS ===")
    top_k, bottom_k, order = heap_operations()
    print(f"Top 3: {top_k}")
    print(f"Processing order: {order}")
    
    print("\n=== DATA PIPELINE EXAMPLE ===")
    pipeline_result = data_pipeline_example()
    print(f"Pipeline result: {pipeline_result}")