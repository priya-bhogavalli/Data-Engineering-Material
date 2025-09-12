# Apache Beam - Comprehensive Interview Questions

## 📋 Table of Contents

1. [Core Concepts](#core-concepts)
2. [Programming Model](#programming-model)
3. [Pipelines & Transforms](#pipelines--transforms)
4. [Windowing & Triggers](#windowing--triggers)
5. [Runners & Execution](#runners--execution)
6. [I/O Connectors](#io-connectors)
7. [Performance & Optimization](#performance--optimization)
8. [Best Practices](#best-practices)

---

## Core Concepts

### 1. What is Apache Beam and how does it unify batch and streaming processing?

**Answer:**
Apache Beam is a unified programming model that provides a single API for both batch and streaming data processing, allowing the same code to run on different execution engines.

**Key Features:**
- **Unified Model**: Single API for batch and streaming
- **Portability**: Runs on multiple execution engines (runners)
- **Expressiveness**: Rich set of transforms and windowing functions
- **Extensibility**: Custom transforms and I/O connectors

```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

# Unified pipeline that works for both batch and streaming
def create_unified_pipeline():
    pipeline_options = PipelineOptions([
        '--runner=DirectRunner',  # Can be changed to DataflowRunner, FlinkRunner, etc.
        '--streaming'  # Enable streaming mode
    ])
    
    with beam.Pipeline(options=pipeline_options) as pipeline:
        # Read from source (works for both batch files and streaming topics)
        data = (pipeline 
                | 'Read' >> beam.io.ReadFromText('input/*')  # Batch
                # | 'Read' >> beam.io.ReadFromPubSub(topic='projects/my-project/topics/input')  # Streaming
                )
        
        # Transform data (same logic for batch and streaming)
        processed = (data
                    | 'Parse' >> beam.Map(parse_json)
                    | 'Filter' >> beam.Filter(lambda x: x['amount'] > 100)
                    | 'Transform' >> beam.Map(enrich_data)
                    | 'Window' >> beam.WindowInto(beam.window.FixedWindows(60))  # 1-minute windows
                    | 'Aggregate' >> beam.CombinePerKey(sum)
                    )
        
        # Write to sink
        (processed 
         | 'Write' >> beam.io.WriteToText('output/results')  # Batch
         # | 'Write' >> beam.io.WriteToPubSub(topic='projects/my-project/topics/output')  # Streaming
         )

def parse_json(element):
    import json
    return json.loads(element)

def enrich_data(element):
    # Add processing timestamp
    element['processed_at'] = beam.utils.timestamp.Timestamp.now()
    return element
```

### 2. Explain the core abstractions in Apache Beam's programming model.

**Answer:**
**Core Abstractions:**

| Abstraction | Description | Purpose |
|-------------|-------------|---------|
| **Pipeline** | Encapsulates entire data processing task | Defines the computation graph |
| **PCollection** | Immutable collection of data | Represents data at any stage |
| **Transform** | Processing operation on PCollections | Defines data transformations |
| **Runner** | Execution engine that runs the pipeline | Provides portability across platforms |

```python
# Core abstractions example
class BeamProgrammingModel:
    def demonstrate_abstractions(self):
        # 1. Pipeline - Top-level container
        pipeline_options = PipelineOptions()
        pipeline = beam.Pipeline(options=pipeline_options)
        
        # 2. PCollection - Immutable data collection
        input_pcollection = (pipeline 
                           | 'Create Data' >> beam.Create([1, 2, 3, 4, 5]))
        
        # 3. Transform - Data processing operations
        transformed_pcollection = (input_pcollection
                                 | 'Square Numbers' >> beam.Map(lambda x: x * x)
                                 | 'Filter Even' >> beam.Filter(lambda x: x % 2 == 0)
                                 | 'Sum All' >> beam.CombineGlobally(sum))
        
        # 4. Runner - Execution engine (specified in pipeline options)
        # --runner=DirectRunner (local)
        # --runner=DataflowRunner (Google Cloud)
        # --runner=FlinkRunner (Apache Flink)
        # --runner=SparkRunner (Apache Spark)
        
        return pipeline

# Advanced transform patterns
class AdvancedTransforms:
    def composite_transform_example(self):
        """Create reusable composite transforms."""
        
        class ProcessSalesData(beam.PTransform):
            def expand(self, pcoll):
                return (pcoll
                       | 'Parse JSON' >> beam.Map(json.loads)
                       | 'Validate' >> beam.Filter(self.is_valid_sale)
                       | 'Enrich' >> beam.Map(self.enrich_with_metadata)
                       | 'Format' >> beam.Map(self.format_output))
            
            def is_valid_sale(self, record):
                return record.get('amount', 0) > 0 and record.get('customer_id')
            
            def enrich_with_metadata(self, record):
                record['processed_timestamp'] = time.time()
                record['region'] = self.get_region(record.get('zip_code'))
                return record
            
            def format_output(self, record):
                return f"{record['customer_id']},{record['amount']},{record['region']}"
        
        # Usage
        with beam.Pipeline() as pipeline:
            sales_data = (pipeline
                         | 'Read Sales' >> beam.io.ReadFromText('sales/*.json')
                         | 'Process Sales' >> ProcessSalesData()
                         | 'Write Results' >> beam.io.WriteToText('output/processed_sales'))
```

## Windowing & Triggers

### 3. How do you implement windowing and triggers in Apache Beam?

**Answer:**
Windowing divides unbounded data into finite chunks for processing, while triggers determine when to emit results.

```python
import apache_beam as beam
from apache_beam import window
from apache_beam.transforms.trigger import AfterWatermark, AfterProcessingTime, AfterCount

class WindowingAndTriggers:
    def fixed_windows_example(self):
        """Fixed time windows with different trigger strategies."""
        
        with beam.Pipeline() as pipeline:
            events = (pipeline 
                     | 'Read Events' >> beam.io.ReadFromPubSub(topic='events')
                     | 'Parse' >> beam.Map(json.loads)
                     | 'Add Timestamps' >> beam.Map(lambda x: beam.window.TimestampedValue(x, x['timestamp'])))
            
            # Fixed windows with watermark trigger
            windowed_events = (events
                             | 'Fixed Windows' >> beam.WindowInto(
                                 window.FixedWindows(300),  # 5-minute windows
                                 trigger=AfterWatermark(early=AfterProcessingTime(60)),  # Early firing every minute
                                 accumulation_mode=beam.transforms.trigger.AccumulationMode.ACCUMULATING
                             ))
            
            # Aggregate within windows
            aggregated = (windowed_events
                         | 'Group by Key' >> beam.GroupByKey()
                         | 'Count Events' >> beam.Map(lambda kv: (kv[0], len(kv[1]))))
    
    def sliding_windows_example(self):
        """Sliding windows for moving averages."""
        
        with beam.Pipeline() as pipeline:
            metrics = (pipeline
                      | 'Read Metrics' >> beam.io.ReadFromPubSub(topic='metrics')
                      | 'Parse' >> beam.Map(json.loads))
            
            # Sliding windows for moving average
            moving_avg = (metrics
                         | 'Add Timestamps' >> beam.Map(lambda x: beam.window.TimestampedValue(
                             (x['metric_name'], x['value']), x['timestamp']))
                         | 'Sliding Windows' >> beam.WindowInto(
                             window.SlidingWindows(size=600, period=60),  # 10-min window, 1-min slide
                             trigger=AfterWatermark()
                         )
                         | 'Calculate Average' >> beam.CombinePerKey(beam.combiners.MeanCombineFn()))
    
    def session_windows_example(self):
        """Session windows for user activity analysis."""
        
        with beam.Pipeline() as pipeline:
            user_events = (pipeline
                          | 'Read User Events' >> beam.io.ReadFromPubSub(topic='user_events')
                          | 'Parse' >> beam.Map(json.loads))
            
            # Session windows with 30-minute gap
            user_sessions = (user_events
                           | 'Key by User' >> beam.Map(lambda x: (x['user_id'], x))
                           | 'Add Timestamps' >> beam.Map(lambda kv: beam.window.TimestampedValue(kv, kv[1]['timestamp']))
                           | 'Session Windows' >> beam.WindowInto(
                               window.Sessions(gap_size=1800),  # 30-minute session gap
                               trigger=AfterWatermark()
                           )
                           | 'Aggregate Session' >> beam.GroupByKey()
                           | 'Session Stats' >> beam.Map(self.calculate_session_stats))
    
    def calculate_session_stats(self, user_events):
        user_id, events = user_events
        events_list = list(events)
        return {
            'user_id': user_id,
            'session_duration': max(e['timestamp'] for e in events_list) - min(e['timestamp'] for e in events_list),
            'event_count': len(events_list),
            'session_start': min(e['timestamp'] for e in events_list)
        }

# Custom trigger implementation
class CustomTriggers:
    def complex_trigger_example(self):
        """Complex trigger combining multiple conditions."""
        
        # Trigger that fires:
        # 1. After watermark passes end of window
        # 2. Early firing after 1000 elements
        # 3. Late firing every 5 minutes after watermark
        complex_trigger = AfterWatermark(
            early=AfterCount(1000),
            late=AfterProcessingTime(300)  # 5 minutes
        )
        
        with beam.Pipeline() as pipeline:
            data = (pipeline
                   | 'Read' >> beam.io.ReadFromPubSub(topic='high_volume_events')
                   | 'Parse' >> beam.Map(json.loads)
                   | 'Window with Complex Trigger' >> beam.WindowInto(
                       window.FixedWindows(3600),  # 1-hour windows
                       trigger=complex_trigger,
                       accumulation_mode=beam.transforms.trigger.AccumulationMode.DISCARDING,
                       allowed_lateness=1800  # Allow 30 minutes of late data
                   )
                   | 'Process' >> beam.GroupByKey())
```

## Runners & Execution

### 4. How do you choose and configure different runners in Apache Beam?

**Answer:**
Runners execute Beam pipelines on different processing engines. Each runner has specific capabilities and configuration options.

```python
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, WorkerOptions

class RunnerConfiguration:
    def direct_runner_config(self):
        """Local execution for development and testing."""
        options = PipelineOptions([
            '--runner=DirectRunner',
            '--direct_num_workers=4',
            '--direct_running_mode=multi_threading'
        ])
        return options
    
    def dataflow_runner_config(self):
        """Google Cloud Dataflow runner configuration."""
        options = PipelineOptions([
            '--runner=DataflowRunner',
            '--project=my-gcp-project',
            '--region=us-central1',
            '--temp_location=gs://my-bucket/temp',
            '--staging_location=gs://my-bucket/staging',
            '--job_name=beam-pipeline-job',
            '--max_num_workers=10',
            '--autoscaling_algorithm=THROUGHPUT_BASED',
            '--worker_machine_type=n1-standard-4',
            '--disk_size_gb=100',
            '--use_public_ips=false',
            '--network=projects/my-project/global/networks/my-vpc',
            '--subnetwork=projects/my-project/regions/us-central1/subnetworks/my-subnet'
        ])
        
        # Additional Dataflow-specific options
        google_cloud_options = options.view_as(GoogleCloudOptions)
        google_cloud_options.project = 'my-gcp-project'
        google_cloud_options.job_name = 'beam-pipeline-job'
        google_cloud_options.staging_location = 'gs://my-bucket/staging'
        google_cloud_options.temp_location = 'gs://my-bucket/temp'
        
        worker_options = options.view_as(WorkerOptions)
        worker_options.max_num_workers = 10
        worker_options.autoscaling_algorithm = 'THROUGHPUT_BASED'
        
        return options
    
    def flink_runner_config(self):
        """Apache Flink runner configuration."""
        options = PipelineOptions([
            '--runner=FlinkRunner',
            '--flink_master=localhost:8081',
            '--parallelism=4',
            '--checkpointing_interval=30000',
            '--flink_submit_uber_jar'
        ])
        return options
    
    def spark_runner_config(self):
        """Apache Spark runner configuration."""
        options = PipelineOptions([
            '--runner=SparkRunner',
            '--spark_master_url=spark://localhost:7077',
            '--spark_submit_uber_jar'
        ])
        return options

# Runner-specific optimizations
class RunnerOptimizations:
    def dataflow_optimizations(self):
        """Dataflow-specific optimization patterns."""
        
        # Use Dataflow templates for reusability
        template_options = PipelineOptions([
            '--runner=DataflowRunner',
            '--project=my-project',
            '--template_location=gs://my-bucket/templates/my-template',
            '--staging_location=gs://my-bucket/staging'
        ])
        
        # Streaming pipeline with Dataflow
        streaming_options = PipelineOptions([
            '--runner=DataflowRunner',
            '--streaming',
            '--enable_streaming_engine',  # Use Dataflow Streaming Engine
            '--experiments=use_runner_v2',  # Use Dataflow Runner v2
            '--worker_machine_type=n1-highmem-2',
            '--max_num_workers=20'
        ])
        
        return template_options, streaming_options
    
    def performance_tuning_example(self):
        """Performance tuning across different runners."""
        
        def create_optimized_pipeline(runner_type):
            if runner_type == 'dataflow':
                options = PipelineOptions([
                    '--runner=DataflowRunner',
                    '--experiments=shuffle_mode=service',  # Use Dataflow Shuffle service
                    '--experiments=use_runner_v2',
                    '--worker_disk_type=compute.googleapis.com/projects//zones//diskTypes/pd-ssd'
                ])
            elif runner_type == 'flink':
                options = PipelineOptions([
                    '--runner=FlinkRunner',
                    '--parallelism=8',
                    '--checkpointing_interval=60000',
                    '--flink_conf_dir=/opt/flink/conf'
                ])
            elif runner_type == 'spark':
                options = PipelineOptions([
                    '--runner=SparkRunner',
                    '--spark_conf=spark.sql.adaptive.enabled=true',
                    '--spark_conf=spark.sql.adaptive.coalescePartitions.enabled=true'
                ])
            
            with beam.Pipeline(options=options) as pipeline:
                # Pipeline logic here
                pass
```

## I/O Connectors

### 5. How do you implement custom I/O connectors in Apache Beam?

**Answer:**
Custom I/O connectors allow reading from and writing to custom data sources not covered by built-in connectors.

```python
import apache_beam as beam
from apache_beam.io import iobase
from apache_beam.transforms import PTransform

class CustomDatabaseSource(iobase.BoundedSource):
    """Custom source for reading from a database."""
    
    def __init__(self, connection_string, query, batch_size=1000):
        self.connection_string = connection_string
        self.query = query
        self.batch_size = batch_size
    
    def estimate_size(self):
        """Estimate the size of data to be read."""
        # Connect to database and estimate row count
        with self._get_connection() as conn:
            count_query = f"SELECT COUNT(*) FROM ({self.query}) as subquery"
            cursor = conn.cursor()
            cursor.execute(count_query)
            row_count = cursor.fetchone()[0]
            return row_count * 100  # Estimate 100 bytes per row
    
    def split(self, desired_bundle_size, start_position=None, stop_position=None):
        """Split the source into multiple bundles for parallel processing."""
        # Get total row count
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM ({self.query}) as subquery")
            total_rows = cursor.fetchone()[0]
        
        # Calculate number of bundles
        rows_per_bundle = max(1, desired_bundle_size // 100)  # Assuming 100 bytes per row
        num_bundles = (total_rows + rows_per_bundle - 1) // rows_per_bundle
        
        bundles = []
        for i in range(num_bundles):
            start = i * rows_per_bundle
            end = min((i + 1) * rows_per_bundle, total_rows)
            bundles.append(CustomDatabaseSourceBundle(
                self.connection_string, 
                self.query, 
                start, 
                end
            ))
        
        return bundles
    
    def get_range_tracker(self, start_position, stop_position):
        """Create a range tracker for this source."""
        return iobase.OffsetRangeTracker(start_position, stop_position)
    
    def read(self, range_tracker):
        """Read data from the source."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Add LIMIT and OFFSET to query
            paginated_query = f"{self.query} LIMIT {self.batch_size} OFFSET {range_tracker.start_position()}"
            cursor.execute(paginated_query)
            
            for row in cursor.fetchall():
                if not range_tracker.try_claim(range_tracker.last_attempted_record_start + 1):
                    break
                yield dict(zip([desc[0] for desc in cursor.description], row))
    
    def _get_connection(self):
        """Create database connection."""
        import psycopg2
        return psycopg2.connect(self.connection_string)

class ReadFromCustomDatabase(PTransform):
    """PTransform for reading from custom database."""
    
    def __init__(self, connection_string, query):
        self.connection_string = connection_string
        self.query = query
    
    def expand(self, pcoll):
        return pcoll | iobase.Read(CustomDatabaseSource(self.connection_string, self.query))

# Custom sink implementation
class CustomDatabaseSink(iobase.Sink):
    """Custom sink for writing to a database."""
    
    def __init__(self, connection_string, table_name, batch_size=1000):
        self.connection_string = connection_string
        self.table_name = table_name
        self.batch_size = batch_size
    
    def create_write_operation(self):
        """Create a write operation."""
        return CustomDatabaseWriteOperation(self)
    
    def open_writer(self, init_result, uid):
        """Open a writer for this sink."""
        return CustomDatabaseWriter(self, init_result, uid)

class CustomDatabaseWriter(iobase.Writer):
    """Writer implementation for custom database sink."""
    
    def __init__(self, sink, init_result, uid):
        self.sink = sink
        self.uid = uid
        self.connection = None
        self.batch = []
    
    def open(self, init_result):
        """Open the writer."""
        import psycopg2
        self.connection = psycopg2.connect(self.sink.connection_string)
        self.cursor = self.connection.cursor()
    
    def write(self, value):
        """Write a single record."""
        self.batch.append(value)
        
        if len(self.batch) >= self.sink.batch_size:
            self._flush_batch()
    
    def close(self):
        """Close the writer."""
        if self.batch:
            self._flush_batch()
        
        if self.connection:
            self.connection.commit()
            self.connection.close()
    
    def _flush_batch(self):
        """Flush the current batch to database."""
        if not self.batch:
            return
        
        # Prepare batch insert
        columns = list(self.batch[0].keys())
        placeholders = ','.join(['%s'] * len(columns))
        query = f"INSERT INTO {self.sink.table_name} ({','.join(columns)}) VALUES ({placeholders})"
        
        # Execute batch insert
        values = [[record[col] for col in columns] for record in self.batch]
        self.cursor.executemany(query, values)
        
        self.batch.clear()

# Usage example
class CustomIOExample:
    def pipeline_with_custom_io(self):
        """Pipeline using custom I/O connectors."""
        
        with beam.Pipeline() as pipeline:
            # Read from custom database
            source_data = (pipeline
                          | 'Read from DB' >> ReadFromCustomDatabase(
                              connection_string='postgresql://user:pass@localhost/db',
                              query='SELECT id, name, amount FROM transactions WHERE date >= CURRENT_DATE'
                          ))
            
            # Process data
            processed_data = (source_data
                            | 'Transform' >> beam.Map(lambda x: {
                                'id': x['id'],
                                'name': x['name'].upper(),
                                'amount': x['amount'] * 1.1,
                                'processed_at': beam.utils.timestamp.Timestamp.now()
                            }))
            
            # Write to custom sink
            (processed_data
             | 'Write to DB' >> beam.io.Write(CustomDatabaseSink(
                 connection_string='postgresql://user:pass@localhost/target_db',
                 table_name='processed_transactions'
             )))
```

This comprehensive Apache Beam interview questions file covers the essential concepts for unified batch and streaming processing that data engineers need to understand.