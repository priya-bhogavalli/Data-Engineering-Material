# Docker Complete Guide for Data Engineering

## 🎯 What is Docker?

Docker is a **containerization platform** that packages applications and their dependencies into lightweight, portable containers. For data engineers, Docker provides consistent environments across development, testing, and production.

### Key Characteristics
- **Containerization**: Isolate applications in lightweight containers
- **Portability**: Run anywhere Docker is installed
- **Consistency**: Same environment across all stages
- **Scalability**: Easy horizontal scaling
- **Resource Efficiency**: Share OS kernel, minimal overhead

## 💾 Core Concepts

### 1. Docker Fundamentals
```bash
# Basic Docker commands
docker --version
docker info

# Container lifecycle
docker run hello-world
docker ps                    # Running containers
docker ps -a                 # All containers
docker stop <container_id>
docker rm <container_id>

# Image management
docker images
docker pull ubuntu:20.04
docker rmi <image_id>
```

### 2. Dockerfile Basics
```dockerfile
# Data engineering Python environment
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
```

### 3. Multi-stage Builds
```dockerfile
# Multi-stage build for data pipeline
FROM python:3.9 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim AS runtime

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app
COPY . .

CMD ["python", "pipeline.py"]
```

## 🔧 Data Engineering Use Cases

### 1. Spark Application Container
```dockerfile
FROM openjdk:8-jdk-slim

# Install Python and Spark
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install Spark
ENV SPARK_VERSION=3.4.0
ENV HADOOP_VERSION=3
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Install PySpark
RUN pip3 install pyspark==${SPARK_VERSION}

WORKDIR /app
COPY spark_job.py .

CMD ["spark-submit", "spark_job.py"]
```

### 2. Database Container Setup
```yaml
# docker-compose.yml for data stack
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: datawarehouse
      POSTGRES_USER: dataeng
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  airflow:
    image: apache/airflow:2.7.0
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://dataeng:secure_password@postgres/datawarehouse
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
    ports:
      - "8080:8080"
    depends_on:
      - postgres

volumes:
  postgres_data:
  redis_data:
```

### 3. ETL Pipeline Container
```dockerfile
FROM python:3.9-slim

# Install system dependencies for data processing
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ETL scripts
COPY etl/ ./etl/
COPY config/ ./config/

# Set environment variables
ENV PYTHONPATH=/app
ENV LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

CMD ["python", "etl/main.py"]
```

## 🚀 Best Practices

### 1. Dockerfile Optimization
```dockerfile
# Optimized Dockerfile for data engineering
FROM python:3.9-slim

# Use non-root user for security
RUN groupadd -r dataeng && useradd -r -g dataeng dataeng

# Install dependencies in single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better caching
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

# Create app directory and set ownership
RUN mkdir -p /app && chown -R dataeng:dataeng /app
WORKDIR /app

# Switch to non-root user
USER dataeng

# Copy application code
COPY --chown=dataeng:dataeng . .

# Use exec form for CMD
CMD ["python", "-m", "app"]
```

### 2. Environment Configuration
```bash
# .env file for development
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=datawarehouse
POSTGRES_USER=dataeng
POSTGRES_PASSWORD=dev_password
REDIS_URL=redis://localhost:6379
LOG_LEVEL=DEBUG
```

```dockerfile
# Use environment variables in Dockerfile
FROM python:3.9-slim

# Set default environment variables
ENV POSTGRES_HOST=postgres \
    POSTGRES_PORT=5432 \
    POSTGRES_DB=datawarehouse \
    LOG_LEVEL=INFO

WORKDIR /app
COPY . .

CMD ["python", "app.py"]
```

### 3. Volume Management
```yaml
# docker-compose.yml with proper volumes
version: '3.8'

services:
  etl_pipeline:
    build: .
    volumes:
      # Bind mount for development
      - ./src:/app/src:ro
      # Named volume for data persistence
      - etl_data:/app/data
      # Bind mount for configuration
      - ./config:/app/config:ro
    environment:
      - DATA_PATH=/app/data
      - CONFIG_PATH=/app/config

volumes:
  etl_data:
    driver: local
```

## 📊 Monitoring and Logging

### 1. Container Health Checks
```dockerfile
# Health check for data pipeline
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python /app/health_check.py || exit 1
```

```python
# health_check.py
import sys
import psycopg2
import redis

def check_postgres():
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD')
        )
        conn.close()
        return True
    except:
        return False

def check_redis():
    try:
        r = redis.Redis.from_url(os.getenv('REDIS_URL'))
        r.ping()
        return True
    except:
        return False

if __name__ == "__main__":
    if check_postgres() and check_redis():
        sys.exit(0)
    else:
        sys.exit(1)
```

### 2. Logging Configuration
```python
# logging_config.py
import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set specific log levels
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
```

## 🔒 Security Best Practices

### 1. Secure Container Configuration
```dockerfile
# Security-focused Dockerfile
FROM python:3.9-slim

# Update packages and remove package manager
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove gcc

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set secure permissions
COPY --chown=appuser:appuser . /app
WORKDIR /app

# Switch to non-root user
USER appuser

# Remove unnecessary files
RUN find /app -name "*.pyc" -delete \
    && find /app -name "__pycache__" -delete

CMD ["python", "app.py"]
```

### 2. Secrets Management
```yaml
# docker-compose.yml with secrets
version: '3.8'

services:
  app:
    build: .
    secrets:
      - db_password
      - api_key
    environment:
      - DB_PASSWORD_FILE=/run/secrets/db_password
      - API_KEY_FILE=/run/secrets/api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

## 🎯 Production Deployment

### 1. Multi-environment Setup
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - NODE_ENV=production
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

### 2. Container Orchestration
```bash
# Docker Swarm deployment
docker swarm init
docker stack deploy -c docker-compose.prod.yml data_pipeline

# Scale services
docker service scale data_pipeline_worker=3

# Update service
docker service update --image myapp:v2 data_pipeline_app
```

This guide provides essential Docker knowledge for data engineering workflows. Focus on containerizing data pipelines, managing dependencies, and implementing proper security practices.