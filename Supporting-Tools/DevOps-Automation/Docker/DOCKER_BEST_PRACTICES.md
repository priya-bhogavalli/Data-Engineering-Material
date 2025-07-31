# Docker Best Practices for Data Engineering

## Dockerfile Optimization

### Multi-stage Builds
```dockerfile
# Build stage
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

### Layer Optimization
```dockerfile
FROM python:3.9-slim

# Install system dependencies first (changes less frequently)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (leverage Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code last
COPY . .
CMD ["python", "app.py"]
```

## Data Pipeline Containers

### Spark Container
```dockerfile
FROM openjdk:11-jre-slim

ENV SPARK_VERSION=3.4.0
ENV HADOOP_VERSION=3

# Install Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin

COPY spark-app.py /app/
WORKDIR /app
CMD ["spark-submit", "spark-app.py"]
```

### Airflow Container
```dockerfile
FROM apache/airflow:2.7.0-python3.9

USER root
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
```

## Container Orchestration

### Docker Compose for Development
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: datawarehouse
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  airflow-webserver:
    build: .
    depends_on:
      - postgres
      - redis
    environment:
      AIRFLOW__CORE__EXECUTOR: CeleryExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://admin:password@postgres/datawarehouse
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs

volumes:
  postgres_data:
```

### Production Deployment
```yaml
version: '3.8'
services:
  data-pipeline:
    image: myregistry/data-pipeline:latest
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/prod
    secrets:
      - db_password
    networks:
      - data-network

secrets:
  db_password:
    external: true

networks:
  data-network:
    driver: overlay
```

## Security Best Practices

### Non-root User
```dockerfile
FROM python:3.9-slim

# Create non-root user
RUN groupadd -r datauser && useradd -r -g datauser datauser

# Install dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER datauser
WORKDIR /home/datauser/app
COPY --chown=datauser:datauser . .

CMD ["python", "app.py"]
```

### Secrets Management
```dockerfile
# Use build secrets
# syntax=docker/dockerfile:1
FROM python:3.9-slim

RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) && \
    # Use API_KEY for setup
```

```bash
# Build with secrets
echo "secret-api-key" | docker build --secret id=api_key,src=- .
```

## Monitoring and Logging

### Health Checks
```dockerfile
FROM python:3.9-slim

COPY app.py .
COPY health_check.py .

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python health_check.py

CMD ["python", "app.py"]
```

### Logging Configuration
```python
# health_check.py
import requests
import sys

try:
    response = requests.get('http://localhost:8000/health', timeout=5)
    if response.status_code == 200:
        sys.exit(0)
    else:
        sys.exit(1)
except:
    sys.exit(1)
```

## Performance Optimization

### Resource Limits
```yaml
services:
  data-processor:
    image: data-processor:latest
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
        reservations:
          memory: 2G
          cpus: '1.0'
```

### Volume Optimization
```yaml
services:
  database:
    image: postgres:13
    volumes:
      # Use named volumes for better performance
      - db_data:/var/lib/postgresql/data
      # Use bind mounts for development only
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro

volumes:
  db_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/postgres-data
```