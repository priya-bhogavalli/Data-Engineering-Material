# Apache Beam Quick Reference

## Core Concepts

### Pipeline Creation
```python
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

# Direct Runner (local)
options = PipelineOptions(['--runner=DirectRunner'])

# Dataflow Runner (Google Cloud)
options = PipelineOptions([
    '--runner=DataflowRunner',
    '--project=my-project',
    '--region=us-central1',
    '--temp_location=gs://my-bucket/temp'
])

with beam.Pipeline(options=options) as pipeline:
    # Pipeline logic here
    pass
```

### Basic Transforms
```python
# Create data
data = pipeline | 'Create' >> beam.Create([1, 2, 3, 4, 5])

# Map transform
squared = data | 'Square' >> beam.Map(lambda x: x * x)

# Filter transform
evens = data | 'Filter Evens' >> beam.Filter(lambda x: x % 2 == 0)

# FlatMap transform
words = pipeline | 'Create Text' >> beam.Create(['hello world', 'apache beam'])
all_words = words | 'Split Words' >> beam.FlatMap(lambda x: x.split())

# Combine transforms
total = data | 'Sum' >> beam.CombineGlobally(sum)
per_key_sum = keyed_data | 'Sum Per Key' >> beam.CombinePerKey(sum)
```

### Key-Value Operations
```python
# Create key-value pairs
keyed = data | 'Add Keys' >> beam.Map(lambda x: (x % 2, x))

# Group by key
grouped = keyed | 'Group' >> beam.GroupByKey()

# Combine per key
combined = keyed | 'Combine' >> beam.CombinePerKey(sum)

# CoGroupByKey (join)
from apache_beam import pvalue

result = {'left': left_pcoll, 'right': right_pcoll} | beam.CoGroupByKey()
```

## Windowing

### Window Types
```python
from apache_beam import window

# Fixed windows
windowed = data | 'Fixed Windows' >> beam.WindowInto(window.FixedWindows(60))  # 60 seconds

# Sliding windows
windowed = data | 'Sliding Windows' >> beam.WindowInto(
    window.SlidingWindows(size=300, period=60))  # 5-min window, 1-min slide

# Session windows
windowed = data | 'Session Windows' >> beam.WindowInto(
    window.Sessions(gap_size=600))  # 10-min gap

# Global windows
windowed = data | 'Global Windows' >> beam.WindowInto(window.GlobalWindows())
```

### Triggers
```python
from apache_beam.transforms import trigger

# Watermark trigger
trigger_spec = trigger.AfterWatermark()

# Processing time trigger
trigger_spec = trigger.AfterProcessingTime(delay=60)  # 60 seconds

# Count trigger
trigger_spec = trigger.AfterCount(100)  # After 100 elements

# Complex trigger
trigger_spec = trigger.AfterWatermark(
    early=trigger.AfterProcessingTime(60),
    late=trigger.AfterProcessingTime(300)
)

# Apply trigger
windowed = data | beam.WindowInto(
    window.FixedWindows(300),
    trigger=trigger_spec,
    accumulation_mode=trigger.AccumulationMode.DISCARDING
)
```

## I/O Operations

### Text I/O
```python
# Read text files
lines = pipeline | 'Read' >> beam.io.ReadFromText('gs://bucket/input/*.txt')

# Write text files
lines | 'Write' >> beam.io.WriteToText('gs://bucket/output/results')
```

### Pub/Sub I/O
```python
# Read from Pub/Sub
messages = pipeline | 'Read PubSub' >> beam.io.ReadFromPubSub(
    topic='projects/my-project/topics/input-topic')

# Write to Pub/Sub
messages | 'Write PubSub' >> beam.io.WriteToPubSub(
    topic='projects/my-project/topics/output-topic')
```

### BigQuery I/O
```python
# Read from BigQuery
rows = pipeline | 'Read BigQuery' >> beam.io.ReadFromBigQuery(
    query='SELECT * FROM `project.dataset.table` WHERE date = CURRENT_DATE()',
    use_standard_sql=True)

# Write to BigQuery
rows | 'Write BigQuery' >> beam.io.WriteToBigQuery(
    table='project:dataset.output_table',
    schema='field1:STRING,field2:INTEGER',
    write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
```

### Database I/O
```python
# JDBC Read
rows = pipeline | 'Read JDBC' >> beam.io.ReadFromJdbc(
    driver_class_name='com.mysql.jdbc.Driver',
    jdbc_url='jdbc:mysql://localhost:3306/db',
    username='user',
    password='password',
    query='SELECT * FROM table')

# JDBC Write
rows | 'Write JDBC' >> beam.io.WriteToJdbc(
    driver_class_name='com.mysql.jdbc.Driver',
    jdbc_url='jdbc:mysql://localhost:3306/db',
    username='user',
    password='password',
    table_name='output_table')
```

## Custom Transforms

### DoFn (Element-wise processing)
```python
class MyDoFn(beam.DoFn):
    def setup(self):
        # Initialize resources
        self.client = create_client()
    
    def process(self, element):
        # Process single element
        result = self.transform(element)
        yield result
    
    def teardown(self):
        # Clean up resources
        self.client.close()

# Usage
processed = data | 'Custom Transform' >> beam.ParDo(MyDoFn())
```

### PTransform (Composite transform)
```python
class MyCompositeTransform(beam.PTransform):
    def __init__(self, param1, param2):
        self.param1 = param1
        self.param2 = param2
    
    def expand(self, pcoll):
        return (pcoll
               | 'Step 1' >> beam.Map(lambda x: x * self.param1)
               | 'Step 2' >> beam.Filter(lambda x: x > self.param2)
               | 'Step 3' >> beam.Map(str))

# Usage
result = data | 'My Transform' >> MyCompositeTransform(2, 5)
```

### CombineFn (Aggregation)
```python
class AverageFn(beam.CombineFn):
    def create_accumulator(self):
        return (0.0, 0)  # (sum, count)
    
    def add_input(self, accumulator, input):
        sum_val, count = accumulator
        return (sum_val + input, count + 1)
    
    def merge_accumulators(self, accumulators):
        sums, counts = zip(*accumulators)
        return (sum(sums), sum(counts))
    
    def extract_output(self, accumulator):
        sum_val, count = accumulator
        return sum_val / count if count > 0 else 0

# Usage
average = data | 'Average' >> beam.CombineGlobally(AverageFn())
```

## Side Inputs and Outputs

### Side Inputs
```python
# Create side input
side_data = pipeline | 'Create Side' >> beam.Create([('key1', 'value1'), ('key2', 'value2')])
side_dict = side_data | 'As Dict' >> beam.combiners.ToDict()

# Use side input
def enrich_with_side_input(element, side_dict):
    key, value = element
    enriched_value = side_dict.get(key, 'default')
    return (key, value, enriched_value)

enriched = main_data | 'Enrich' >> beam.Map(
    enrich_with_side_input, 
    side_dict=beam.pvalue.AsDict(side_dict))
```

### Side Outputs
```python
from apache_beam import pvalue

# Define output tags
success_tag = 'success'
error_tag = 'error'

def process_with_side_outputs(element):
    try:
        result = process_element(element)
        yield pvalue.TaggedOutput(success_tag, result)
    except Exception as e:
        yield pvalue.TaggedOutput(error_tag, str(e))

# Apply transform with side outputs
results = data | 'Process' >> beam.FlatMap(process_with_side_outputs).with_outputs(
    success_tag, error_tag, main='success')

success_data = results[success_tag]
error_data = results[error_tag]
```

## Testing

### Unit Testing
```python
import apache_beam as beam
from apache_beam.testing.test_pipeline import TestPipeline
from apache_beam.testing.util import assert_that, equal_to

def test_my_transform():
    with TestPipeline() as p:
        input_data = p | beam.Create([1, 2, 3, 4, 5])
        output = input_data | 'Square' >> beam.Map(lambda x: x * x)
        
        assert_that(output, equal_to([1, 4, 9, 16, 25]))
```

### Integration Testing
```python
from apache_beam.testing.test_stream import TestStream
from apache_beam.testing.util import assert_that, equal_to

def test_streaming_pipeline():
    with TestPipeline() as p:
        test_stream = (TestStream()
                      .add_elements(['a', 'b', 'c'])
                      .advance_watermark_to(100)
                      .add_elements(['d', 'e'])
                      .advance_watermark_to_infinity())
        
        output = (p 
                 | test_stream
                 | 'Upper' >> beam.Map(str.upper))
        
        assert_that(output, equal_to(['A', 'B', 'C', 'D', 'E']))
```

## Common Patterns

### Word Count
```python
def word_count_pipeline():
    with beam.Pipeline() as pipeline:
        lines = pipeline | 'Read' >> beam.io.ReadFromText('input.txt')
        
        counts = (lines
                 | 'Split' >> beam.FlatMap(lambda x: x.split())
                 | 'Pair with 1' >> beam.Map(lambda x: (x, 1))
                 | 'Group and Sum' >> beam.CombinePerKey(sum))
        
        counts | 'Write' >> beam.io.WriteToText('output')
```

### Streaming Analytics
```python
def streaming_analytics():
    with beam.Pipeline() as pipeline:
        events = (pipeline 
                 | 'Read Stream' >> beam.io.ReadFromPubSub(topic='events')
                 | 'Parse JSON' >> beam.Map(json.loads)
                 | 'Add Timestamps' >> beam.Map(
                     lambda x: beam.window.TimestampedValue(x, x['timestamp'])))
        
        windowed = (events
                   | 'Window' >> beam.WindowInto(beam.window.FixedWindows(60))
                   | 'Key by Type' >> beam.Map(lambda x: (x['type'], 1))
                   | 'Count' >> beam.CombinePerKey(sum))
        
        windowed | 'Write Results' >> beam.io.WriteToPubSub(topic='results')
```

### ETL Pipeline
```python
def etl_pipeline():
    with beam.Pipeline() as pipeline:
        # Extract
        raw_data = pipeline | 'Extract' >> beam.io.ReadFromBigQuery(
            query='SELECT * FROM source_table')
        
        # Transform
        transformed = (raw_data
                      | 'Clean' >> beam.Map(clean_data)
                      | 'Validate' >> beam.Filter(validate_data)
                      | 'Enrich' >> beam.Map(enrich_data))
        
        # Load
        transformed | 'Load' >> beam.io.WriteToBigQuery(
            table='project:dataset.target_table')

def clean_data(record):
    # Data cleaning logic
    return record

def validate_data(record):
    # Data validation logic
    return True

def enrich_data(record):
    # Data enrichment logic
    return record
```

## Performance Tips

### Optimization Patterns
```python
# Use efficient coders
from apache_beam.coders import PickleCoder, VarIntCoder

pcoll.set_coder(VarIntCoder())

# Reshuffle to break fusion
pcoll | 'Reshuffle' >> beam.Reshuffle()

# Use side inputs for small reference data
reference_data = pipeline | beam.Create(small_dataset)
reference_dict = reference_data | beam.combiners.ToDict()

main_data | beam.Map(enrich_function, 
                    ref_data=beam.pvalue.AsDict(reference_dict))

# Batch operations
pcoll | beam.io.WriteToText('output', num_shards=10)
```

### Memory Management
```python
class EfficientDoFn(beam.DoFn):
    def setup(self):
        # Initialize expensive resources once
        self.expensive_resource = create_resource()
    
    def process(self, element):
        # Reuse resources
        result = self.expensive_resource.process(element)
        yield result
    
    def teardown(self):
        # Clean up
        self.expensive_resource.close()
```

## Runner-Specific Options

### Dataflow Runner
```python
options = PipelineOptions([
    '--runner=DataflowRunner',
    '--project=my-project',
    '--region=us-central1',
    '--temp_location=gs://bucket/temp',
    '--staging_location=gs://bucket/staging',
    '--num_workers=5',
    '--max_num_workers=20',
    '--autoscaling_algorithm=THROUGHPUT_BASED',
    '--worker_machine_type=n1-standard-4'
])
```

### Flink Runner
```python
options = PipelineOptions([
    '--runner=FlinkRunner',
    '--flink_master=localhost:8081',
    '--parallelism=4'
])
```

### Spark Runner
```python
options = PipelineOptions([
    '--runner=SparkRunner',
    '--spark_master_url=local[4]'
])
```