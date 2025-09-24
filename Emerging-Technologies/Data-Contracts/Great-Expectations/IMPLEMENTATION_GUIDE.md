# 📋 Great Expectations Implementation Guide

> **Complete guide to implementing data contracts and quality validation with Great Expectations**

## 🚀 **Quick Start Implementation**

### **Installation & Setup**
```bash
pip install great_expectations
great_expectations init
```

### **Basic Data Contract Example**
```python
import great_expectations as gx

context = gx.get_context()

# Create expectation suite (data contract)
suite = context.create_expectation_suite(
    expectation_suite_name="user_events_contract",
    overwrite_existing=True
)

# Define data expectations
expectations = [
    {
        "expectation_type": "expect_column_to_exist",
        "kwargs": {"column": "user_id"}
    },
    {
        "expectation_type": "expect_column_values_to_not_be_null",
        "kwargs": {"column": "user_id"}
    },
    {
        "expectation_type": "expect_column_values_to_match_regex",
        "kwargs": {
            "column": "email",
            "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        }
    }
]

# Add expectations to suite
for expectation in expectations:
    suite.add_expectation(**expectation)

context.save_expectation_suite(suite)
```

---

## 🏗️ **Database Integration**
```python
# PostgreSQL connection
postgres_datasource = context.sources.add_postgres(
    name="postgres_db",
    connection_string="postgresql://user:password@localhost:5432/mydb"
)

table_asset = postgres_datasource.add_table_asset(
    name="user_events",
    table_name="user_events"
)

# Validate data
validator = context.get_validator(
    batch_request=table_asset.build_batch_request(),
    expectation_suite_name="user_events_contract"
)

results = validator.validate()
print(f"Validation success: {results.success}")
```

---

## 🔄 **CI/CD Integration**

### **GitHub Actions Workflow**
```yaml
name: Data Quality Validation
on:
  schedule:
    - cron: '0 */6 * * *'

jobs:
  validate-data:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: pip install great_expectations pandas sqlalchemy
    - name: Run data validation
      run: python scripts/validate_data.py
```

### **Validation Script**
```python
# scripts/validate_data.py
import great_expectations as gx
import sys

def main():
    context = gx.get_context()
    
    checkpoints = [
        "user_events_checkpoint",
        "sales_data_checkpoint"
    ]
    
    all_passed = True
    
    for checkpoint_name in checkpoints:
        results = context.run_checkpoint(checkpoint_name=checkpoint_name)
        
        if not results.success:
            print(f"❌ Checkpoint {checkpoint_name} failed")
            all_passed = False
        else:
            print(f"✅ Checkpoint {checkpoint_name} passed")
    
    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## 📊 **Custom Expectations**
```python
from great_expectations.expectations import Expectation

class ExpectColumnValuesToBeValidJSON(Expectation):
    expectation_type = "expect_column_values_to_be_valid_json"
    
    def _validate(self, configuration, metrics, runtime_configuration=None, execution_engine=None):
        column = configuration.kwargs.get("column")
        
        def is_valid_json(value):
            try:
                json.loads(value)
                return True
            except (ValueError, TypeError):
                return False
        
        column_values = metrics.get("column_values")
        valid_count = sum(1 for value in column_values if is_valid_json(value))
        total_count = len(column_values)
        
        return {
            "success": valid_count == total_count,
            "result": {
                "observed_value": valid_count / total_count if total_count > 0 else 0
            }
        }

# Register and use
context.expectations.add_expectation(ExpectColumnValuesToBeValidJSON)
```

---

## 🎯 **Best Practices**

### **1. Specific Expectations**
```python
# Good: Specific and actionable
suite.add_expectation(
    expectation_type="expect_column_values_to_be_between",
    kwargs={
        "column": "order_amount",
        "min_value": 0.01,
        "max_value": 10000.00
    }
)
```

### **2. Performance Optimization**
```python
# Use sampling for large datasets
batch_request = asset.build_batch_request(
    options={
        "sampling_method": "random",
        "sampling_kwargs": {"n": 10000}
    }
)
```

### **3. Comprehensive Documentation**
```python
suite_meta = {
    "notes": "Data contract for user events stream",
    "owner": "data-platform-team@company.com",
    "version": "1.2.0",
    "sla": {
        "freshness": "< 5 minutes",
        "completeness": "> 99%"
    }
}
suite.meta = suite_meta
```

---

**📋 Great Expectations provides robust data contract implementation with automated validation, documentation, and monitoring capabilities.**