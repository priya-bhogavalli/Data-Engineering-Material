# Airflow CLI Commands Quick Reference

## DAG Commands
```bash
# List all DAGs
airflow dags list

# List DAG import errors
airflow dags list-import-errors

# Trigger a DAG run
airflow dags trigger dag_id

# Pause/unpause a DAG
airflow dags pause dag_id
airflow dags unpause dag_id

# Show DAG details
airflow dags show dag_id

# Backfill a DAG
airflow dags backfill -s START_DATE -e END_DATE dag_id
```

## Task Commands
```bash
# Test a task
airflow tasks test dag_id task_id 2023-01-01

# List tasks in a DAG
airflow tasks list dag_id

# Clear task instances
airflow tasks clear -t task_id dag_id

# View task logs
airflow tasks logs dag_id task_id 2023-01-01

# Mark task success/failed
airflow tasks success dag_id task_id 2023-01-01
airflow tasks fail dag_id task_id 2023-01-01
```

## Variables & Connections
```bash
# List variables
airflow variables list

# Get/set variables
airflow variables get var_key
airflow variables set var_key var_value

# Import/export variables
airflow variables import vars.json
airflow variables export vars.json

# List connections
airflow connections list

# Add connection
airflow connections add conn_id \
  --conn-type conn_type \
  --conn-host host \
  --conn-login login \
  --conn-password password \
  --conn-port port
```

## Admin Commands
```bash
# Initialize database
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --firstname FIRST_NAME \
  --lastname LAST_NAME \
  --role Admin \
  --email admin@example.com

# Start webserver/scheduler
airflow webserver -p 8080
airflow scheduler

# Check Airflow version
airflow version

# Get config value
airflow config get-value core executor
```

## Pools & SLAs
```bash
# List pools
airflow pools list

# Create pool
airflow pools set pool_name slots "description"

# List SLAs
airflow slas list
```

## Troubleshooting
```bash
# Check health
airflow health

# Check database connection
airflow db check

# Show configuration
airflow config list

# Show plugins
airflow plugins
```