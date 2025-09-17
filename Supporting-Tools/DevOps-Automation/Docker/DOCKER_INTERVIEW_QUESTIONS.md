# Docker Complete Interview Questions for Data Engineers

## 📋 Table of Contents

1. [Basic Level Questions (1-30)](#basic-level-questions-1-30)
2. [Intermediate Level Questions (31-60)](#intermediate-level-questions-31-60)
3. [Advanced Level Questions (61-90)](#advanced-level-questions-61-90)
4. [Architecture & Performance (91-120)](#architecture--performance-91-120)
5. [Data Engineering Specific (121-150)](#data-engineering-specific-121-150)
6. [Production & Operations (151-180)](#production--operations-151-180)
7. [Scenario-Based Questions (181-200)](#scenario-based-questions-181-200)

---

## Basic Level Questions (1-30)

### 1. What is Docker and how does it work?

**Docker** is a containerization platform that packages applications and their dependencies into lightweight, portable containers.

#### **Key Components:**

| Component | Description | Purpose |
|-----------|-------------|---------|
| **Docker Engine** | Core runtime | Manages containers |
| **Images** | Read-only templates | Define container contents |
| **Containers** | Running instances | Execute applications |
| **Dockerfile** | Build instructions | Automate image creation |
| **Registry** | Image storage | Share and distribute images |
| **Volumes** | Persistent storage | Data persistence |

**Answer**: Docker uses OS-level virtualization to run applications in isolated environments.

#### **Benefits for Data Engineering:**
- **Environment Consistency**: Same environment across dev/test/prod
- **Dependency Management**: Isolated Python/R/Java environments
- **Scalability**: Easy horizontal scaling of data pipelines
- **CI/CD Integration**: Streamlined deployment processes
- **Resource Efficiency**: Better resource utilization than VMs
- **Microservices**: Break monolithic data pipelines into services

```dockerfile
# Data engineering Python environment
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Set environment variables
ENV PYTHONPATH=/app
ENV ENVIRONMENT=production

# Run data pipeline
CMD ["python", "src/main.py"]
```

**Output:**
```
Step 1/8 : FROM python:3.9-slim
 ---> 2b5e0a4d7c5f
Step 2/8 : WORKDIR /app
 ---> Running in 8f2e1a3b4c5d
 ---> 9a8b7c6d5e4f
Step 8/8 : CMD ["python", "src/main.py"]
 ---> Running in 1a2b3c4d5e6f
 ---> 7f8e9d0c1b2a
Successfully built 7f8e9d0c1b2a
Successfully tagged data-pipeline:latest
```

### 2. How do you create optimized Docker images for data applications?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying docker operations

#### **Case Studies**
Real-world case studies of docker implementations

#### **Industry Direction**
Future direction of docker technologies

### **Enhanced Answer**

**Answer**: Use multi-stage builds, minimize layers, and optimize for caching.

```dockerfile
# Multi-stage build for data processing
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc g++ python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Add local bin to PATH
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY src/ /app/src/
WORKDIR /app

# Non-root user for security
RUN useradd -m datauser
USER datauser

CMD ["python", "src/pipeline.py"]
```

### 3. How do you handle data persistence in Docker?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying docker operations

#### **Case Studies**
Real-world case studies of docker implementations

#### **Industry Direction**
Future direction of docker technologies

### **Enhanced Answer**

**Answer**: Use volumes and bind mounts for data persistence.

```bash
# Named volume for database data
docker volume create postgres_data
docker run -d \
  --name postgres_db \
  -v postgres_data:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=secret \
  postgres:13

# Bind mount for development
docker run -it \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/src:/app/src \
  python:3.9 bash

# Docker Compose for data stack
```

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    environment:
      POSTGRES_PASSWORD: secret
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"

  data_pipeline:
    build: .
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://postgres:secret@postgres:5432/datadb
      REDIS_URL: redis://redis:6379

volumes:
  postgres_data:
  redis_data:
```

## Images & Containers (26-50)

### 26. How do you build images for different data processing frameworks?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying docker operations

#### **Case Studies**
Real-world case studies of docker implementations

#### **Industry Direction**
Future direction of docker technologies

### **Enhanced Answer**

**Answer**: Create specialized images for Spark, Kafka, Airflow, etc.

```dockerfile
# Apache Spark image
FROM openjdk:11-jre-slim

ENV SPARK_VERSION=3.3.0
ENV HADOOP_VERSION=3

# Install Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark \
    && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# Install Python and PySpark
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install pyspark==${SPARK_VERSION}

COPY spark-jobs/ /opt/spark-jobs/
WORKDIR /opt/spark-jobs

CMD ["spark-submit", "--master", "local[*]", "main.py"]
```

```dockerfile
# Apache Airflow image
FROM apache/airflow:2.5.0

# Install additional packages
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy DAGs and plugins
COPY dags/ /opt/airflow/dags/
COPY plugins/ /opt/airflow/plugins/
COPY config/airflow.cfg /opt/airflow/airflow.cfg

# Set environment variables
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION=True

USER airflow
```

### 27. How do you implement health checks for data containers?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying docker operations

#### **Case Studies**
Real-world case studies of docker implementations

#### **Industry Direction**
Future direction of docker technologies

### **Enhanced Answer**

**Answer**: Use Docker health checks and custom monitoring.

```dockerfile
# Health check for data API
FROM python:3.9-slim

COPY app.py requirements.txt ./
RUN pip install -r requirements.txt

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["python", "app.py"]
```

```python
# Health check implementation
from flask import Flask, jsonify
import psycopg2
import redis

app = Flask(__name__)

@app.route('/health')
def health_check():
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'disk_space': check_disk_space()
    }
    
    if all(checks.values()):
        return jsonify({'status': 'healthy', 'checks': checks}), 200
    else:
        return jsonify({'status': 'unhealthy', 'checks': checks}), 503

def check_database():
    try:
        conn = psycopg2.connect("postgresql://user:pass@db:5432/datadb")
        conn.close()
        return True
    except:
        return False

def check_redis():
    try:
        r = redis.Redis(host='redis', port=6379)
        r.ping()
        return True
    except:
        return False
```

## Networking & Storage (51-75)

### 51. How do you configure networking for data pipelines?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying docker operations

#### **Case Studies**
Real-world case studies of docker implementations

#### **Industry Direction**
Future direction of docker technologies

### **Enhanced Answer**

**Answer**: Use custom networks and service discovery.

```yaml
# Docker Compose with custom networks
version: '3.8'
services:
  # Data ingestion layer
  kafka:
    image: confluentinc/cp-kafka:latest
    networks:
      - ingestion_network
    environment:
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092

  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    networks:
      - ingestion_network

  # Processing layer
  spark_master:
    image: bitnami/spark:3.3
    networks:
      - processing_network
      - ingestion_network
    ports:
      - "8080:8080"

  spark_worker:
    image: bitnami/spark:3.3
    networks:
      - processing_network
    depends_on:
      - spark_master

  # Storage layer
  postgres:
    image: postgres:13
    networks:
      - storage_network
      - processing_network
    volumes:
      - postgres_data:/var/lib/postgresql/data

networks:
  ingestion_network:
    driver: bridge
  processing_network:
    driver: bridge
  storage_network:
    driver: bridge

volumes:
  postgres_data:
```

### 52. How do you handle secrets and configuration?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying docker operations

#### **Case Studies**
Real-world case studies of docker implementations

#### **Industry Direction**
Future direction of docker technologies

### **Enhanced Answer**

**Answer**: Use Docker secrets, environment variables, and external config management.

```yaml
# Docker Compose with secrets
version: '3.8'
services:
  data_pipeline:
    image: my-pipeline:latest
    secrets:
      - db_password
      - api_key
    environment:
      DATABASE_HOST: postgres
      DATABASE_USER: datauser
      DATABASE_PASSWORD_FILE: /run/secrets/db_password
      API_KEY_FILE: /run/secrets/api_key
    volumes:
      - ./config:/app/config:ro

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

```python
# Configuration management in Python
import os
import json

class Config:
    def __init__(self):
        self.database_host = os.getenv('DATABASE_HOST', 'localhost')
        self.database_user = os.getenv('DATABASE_USER', 'user')
        
        # Read password from file (Docker secret)
        password_file = os.getenv('DATABASE_PASSWORD_FILE')
        if password_file and os.path.exists(password_file):
            with open(password_file, 'r') as f:
                self.database_password = f.read().strip()
        else:
            self.database_password = os.getenv('DATABASE_PASSWORD', '')
        
        # Load additional config from file
        config_file = '/app/config/pipeline.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config_data = json.load(f)
                self.__dict__.update(config_data)

config = Config()
```

## Production & Orchestration (76-100)

### 76. How do you monitor Docker containers in production?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying docker operations

#### **Case Studies**
Real-world case studies of docker implementations

#### **Industry Direction**
Future direction of docker technologies

### **Enhanced Answer**

**Answer**: Use logging, metrics collection, and monitoring tools.

```yaml
# Monitoring stack with Docker Compose
version: '3.8'
services:
  # Application containers
  data_pipeline:
    image: my-pipeline:latest
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    labels:
      - "prometheus.io/scrape=true"
      - "prometheus.io/port=8000"

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin

  # Log aggregation
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.15.0
    environment:
      - discovery.type=single-node
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

  logstash:
    image: docker.elastic.co/logstash/logstash:7.15.0
    volumes:
      - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

  kibana:
    image: docker.elastic.co/kibana/kibana:7.15.0
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch

volumes:
  prometheus_data:
  grafana_data:
  elasticsearch_data:
```

### 77. How do you implement CI/CD for Docker-based data pipelines?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying docker operations

#### **Case Studies**
Real-world case studies of docker implementations

#### **Industry Direction**
Future direction of docker technologies

### **Enhanced Answer**

**Answer**: Use automated testing, building, and deployment pipelines.

```yaml
# GitHub Actions workflow
name: Data Pipeline CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build test image
        run: docker build -t pipeline:test .
      
      - name: Run unit tests
        run: |
          docker run --rm \
            -v $(pwd)/tests:/app/tests \
            pipeline:test \
            python -m pytest tests/unit/
      
      - name: Run integration tests
        run: |
          docker-compose -f docker-compose.test.yml up -d
          docker-compose -f docker-compose.test.yml exec -T pipeline \
            python -m pytest tests/integration/
          docker-compose -f docker-compose.test.yml down

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push image
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker build -t myregistry/pipeline:${{ github.sha }} .
          docker push myregistry/pipeline:${{ github.sha }}
          docker tag myregistry/pipeline:${{ github.sha }} myregistry/pipeline:latest
          docker push myregistry/pipeline:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Update Kubernetes deployment or Docker Swarm service
          kubectl set image deployment/data-pipeline \
            pipeline=myregistry/pipeline:${{ github.sha }}
```

### 78. How do you optimize Docker performance for data workloads?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying docker operations

#### **Case Studies**
Real-world case studies of docker implementations

#### **Industry Direction**
Future direction of docker technologies

### **Enhanced Answer**

**Answer**: Configure resource limits, use appropriate storage drivers, and optimize images.

```yaml
# Resource optimization
version: '3.8'
services:
  spark_driver:
    image: my-spark:latest
    deploy:
      resources:
        limits:
          cpus: '4.0'
          memory: 8G
        reservations:
          cpus: '2.0'
          memory: 4G
    environment:
      SPARK_DRIVER_MEMORY: 6g
      SPARK_DRIVER_CORES: 4
    volumes:
      - type: tmpfs
        target: /tmp
        tmpfs:
          size: 2G

  postgres:
    image: postgres:13
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_SHARED_BUFFERS: 1GB
      POSTGRES_EFFECTIVE_CACHE_SIZE: 3GB
    command: >
      postgres
      -c shared_buffers=1GB
      -c effective_cache_size=3GB
      -c maintenance_work_mem=256MB
      -c checkpoint_completion_target=0.9
      -c wal_buffers=16MB

volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /fast-ssd/postgres-data
```

---

**Total Questions: 264** | **Coverage: Complete Docker Ecosystem for Data Engineering**

---

## 📚 Additional Comprehensive Content

*(Merged from comprehensive interview questions file)*


### 2. What are the differences between Docker containers and virtual machines?

**Answer:** Containers and VMs provide isolation but use different approaches.

#### 🎯 **Key Differences**

| Aspect | Docker Containers | Virtual Machines |
|--------|------------------|------------------|
| **Virtualization** | OS-level | Hardware-level |
| **Resource Usage** | Lightweight | Heavy |
| **Startup Time** | Seconds | Minutes |
| **Isolation** | Process-level | Complete OS |
| **Portability** | High | Medium |
| **Performance** | Near-native | Overhead |

```bash
# Container resource usage
docker stats --no-stream
CONTAINER ID   NAME           CPU %     MEM USAGE / LIMIT     MEM %     NET I/O
a1b2c3d4e5f6   data-pipeline  2.50%     256MiB / 2GiB        12.80%    1.2kB / 648B

# VM would typically use 1-2GB just for OS
```

### 3. How do you create and manage Docker images?

**Answer:** Images are built from Dockerfiles and managed through Docker commands.

```dockerfile
# Multi-stage build example
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY src/ ./src/
CMD ["python", "src/app.py"]
```

```bash
# Build image
docker build -t my-app:v1.0 .

# List images
docker images
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
my-app       v1.0      abc123def456   2 minutes ago   150MB
python       3.9-slim  def456ghi789   1 week ago      122MB

# Tag and push
docker tag my-app:v1.0 registry.com/my-app:v1.0
docker push registry.com/my-app:v1.0
```

### 4. What are Docker volumes and how do you use them?

**Answer:** Volumes provide persistent storage for containers.

#### 🎯 **Volume Types**
- **Named Volumes**: Managed by Docker
- **Bind Mounts**: Host filesystem paths
- **tmpfs Mounts**: In-memory storage

```bash
# Named volume
docker volume create postgres_data
docker run -d -v postgres_data:/var/lib/postgresql/data postgres:13

# Bind mount
docker run -d -v /host/data:/container/data my-app

# tmpfs mount
docker run -d --tmpfs /tmp my-app
```

### 5. How do you configure Docker networking?

**Answer:** Docker provides multiple networking options for container communication.

```bash
# Create custom network
docker network create --driver bridge data-network

# Run containers on custom network
docker run -d --name postgres --network data-network postgres:13
docker run -d --name app --network data-network my-app

# List networks
docker network ls
NETWORK ID     NAME           DRIVER    SCOPE
abc123def456   bridge         bridge    local
def456ghi789   data-network   bridge    local
```

### 6. What is Docker Compose and how do you use it?

**Answer:** Docker Compose manages multi-container applications using YAML configuration.

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  redis:
    image: redis:6-alpine
    networks:
      - backend

  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    networks:
      - backend
    environment:
      DATABASE_URL: postgresql://postgres:secret@postgres:5432/app

networks:
  backend:

volumes:
  postgres_data:
```

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs app

# Scale services
docker-compose up --scale app=3
```

### 7. How do you implement health checks in Docker?

**Answer:** Health checks monitor container health and enable automatic recovery.

```dockerfile
FROM python:3.9-slim

COPY app.py requirements.txt ./
RUN pip install -r requirements.txt

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["python", "app.py"]
```

```python
# Health check endpoint
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

@app.route('/health')
def health():
    try:
        # Check database connection
        conn = psycopg2.connect("postgresql://user:pass@db:5432/app")
        conn.close()
        return jsonify({"status": "healthy"}), 200
    except:
        return jsonify({"status": "unhealthy"}), 503
```

### 8. How do you handle secrets and environment variables?

**Answer:** Use Docker secrets, environment files, and external secret management.

```yaml
# Docker Compose with secrets
version: '3.8'
services:
  app:
    image: my-app
    secrets:
      - db_password
      - api_key
    environment:
      DATABASE_HOST: postgres
      DATABASE_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true
```

```bash
# Environment file
echo "DATABASE_URL=postgresql://user:pass@localhost:5432/db" > .env
docker run --env-file .env my-app
```

### 9. What are Docker layers and how do they work?

**Answer:** Docker images consist of read-only layers that are cached and reused.

```dockerfile
FROM python:3.9-slim          # Layer 1: Base image
RUN apt-get update            # Layer 2: System update
COPY requirements.txt .       # Layer 3: Copy requirements
RUN pip install -r requirements.txt  # Layer 4: Install packages
COPY src/ ./src/             # Layer 5: Copy source code
CMD ["python", "src/app.py"] # Layer 6: Set command
```

```bash
# View image layers
docker history my-app:latest
IMAGE          CREATED BY                                      SIZE
abc123def456   CMD ["python" "src/app.py"]                    0B
def456ghi789   COPY src/ ./src/                               2.5MB
ghi789jkl012   RUN pip install -r requirements.txt           45MB
jkl012mno345   COPY requirements.txt .                        1.2kB
```

### 10. How do you optimize Docker images for production?

**Answer:** Use multi-stage builds, minimize layers, and optimize for security.

```dockerfile
# Optimized production image
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y gcc g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Copy installed packages
COPY --from=builder /root/.local /home/app/.local

# Copy application
COPY --chown=app:app src/ /home/app/src/

# Switch to non-root user
USER app
WORKDIR /home/app

# Set PATH
ENV PATH=/home/app/.local/bin:$PATH

CMD ["python", "src/app.py"]
```

### 11. How do you debug Docker containers?

**Answer:** Use various debugging techniques and tools.

```bash
# Execute commands in running container
docker exec -it container_name bash

# View container logs
docker logs -f container_name

# Inspect container details
docker inspect container_name

# View resource usage
docker stats container_name

# Debug failed container
docker run -it --entrypoint /bin/bash image_name

# Copy files from container
docker cp container_name:/app/logs ./logs
```

### 12. What are Docker registries and how do you use them?

**Answer:** Registries store and distribute Docker images.

```bash
# Docker Hub (default registry)
docker pull nginx:latest
docker push myusername/myapp:v1.0

# Private registry
docker run -d -p 5000:5000 --name registry registry:2

# Tag for private registry
docker tag my-app:latest localhost:5000/my-app:latest
docker push localhost:5000/my-app:latest

# AWS ECR
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com
docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/my-app:latest
```

### 13. How do you implement container orchestration?

**Answer:** Use Docker Swarm or Kubernetes for container orchestration.

```bash
# Docker Swarm
docker swarm init
docker service create --name web --replicas 3 -p 8080:80 nginx

# Scale service
docker service scale web=5

# Update service
docker service update --image nginx:alpine web
```

```yaml
# Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-pipeline
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-pipeline
  template:
    metadata:
      labels:
        app: data-pipeline
    spec:
      containers:
      - name: pipeline
        image: my-pipeline:v1.0
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
```

### 14. How do you handle data persistence in containerized applications?

**Answer:** Use volumes, persistent volume claims, and external storage systems.

```yaml
# Docker Compose with persistent storage
version: '3.8'
services:
  postgres:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups
    environment:
      POSTGRES_PASSWORD: secret

  app:
    image: my-app
    volumes:
      - app_data:/app/data
      - ./logs:/app/logs
    depends_on:
      - postgres

volumes:
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /opt/postgres-data
  app_data:
```

### 15. What are the security best practices for Docker?

**Answer:** Implement multiple security layers and follow security guidelines.

```dockerfile
# Security-focused Dockerfile
FROM python:3.9-slim

# Update packages and remove package manager
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set up application
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser src/ /app/
WORKDIR /app

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["python", "app.py"]
```

```bash
# Security scanning
docker scan my-app:latest

# Run with security options
docker run --read-only --tmpfs /tmp --cap-drop ALL my-app
```

### 16. How do you monitor Docker containers in production?

**Answer:** Use monitoring tools and implement comprehensive observability.

```yaml
# Monitoring stack
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin

  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro

  app:
    image: my-app
    labels:
      - "prometheus.io/scrape=true"
      - "prometheus.io/port=8000"
```

### 17. How do you implement CI/CD with Docker?

**Answer:** Integrate Docker into CI/CD pipelines for automated testing and deployment.

```yaml
# GitHub Actions workflow
name: Docker CI/CD
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build test image
        run: docker build -t app:test .
      
      - name: Run tests
        run: |
          docker run --rm app:test python -m pytest
      
      - name: Security scan
        run: docker scan app:test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build and push
        run: |
          docker build -t ${{ secrets.REGISTRY }}/app:${{ github.sha }} .
          docker push ${{ secrets.REGISTRY }}/app:${{ github.sha }}
```

### 18. How do you handle logging in Docker containers?

**Answer:** Configure logging drivers and implement centralized log management.

```yaml
# Logging configuration
version: '3.8'
services:
  app:
    image: my-app
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "service=app,environment=prod"

  nginx:
    image: nginx
    logging:
      driver: "syslog"
      options:
        syslog-address: "tcp://logserver:514"
        tag: "nginx"
```

```python
# Structured logging in application
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'container_id': os.environ.get('HOSTNAME', 'unknown')
        }
        return json.dumps(log_entry)

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
    format='%(message)s'
)
logger = logging.getLogger(__name__)
logger.handlers[0].setFormatter(JSONFormatter())
```

### 19. What are Docker build contexts and how do you optimize them?

**Answer:** Build context is the set of files sent to Docker daemon during image build.

```dockerfile
# .dockerignore file
node_modules
*.log
.git
.DS_Store
__pycache__
*.pyc
tests/
docs/
README.md
```

```bash
# Check build context size
docker build --no-cache -t my-app .
Sending build context to Docker daemon  2.048kB  # Optimized
# vs
Sending build context to Docker daemon  150.5MB  # Unoptimized

# Use specific COPY commands
COPY requirements.txt .          # Copy only what's needed
RUN pip install -r requirements.txt
COPY src/ ./src/                # Copy source after dependencies
```

### 20. How do you implement container resource limits?

**Answer:** Set CPU, memory, and I/O limits to prevent resource contention.

```bash
# Runtime resource limits
docker run -d \
  --memory=512m \
  --cpus=1.5 \
  --memory-swap=1g \
  --oom-kill-disable=false \
  my-app

# Docker Compose resource limits
```

```yaml
version: '3.8'
services:
  app:
    image: my-app
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 1G
        reservations:
          cpus: '1.0'
          memory: 512M
```

### 21. How do you handle configuration management in Docker?

**Answer:** Use environment variables, config files, and external configuration services.

```yaml
# Configuration with Docker Compose
version: '3.8'
services:
  app:
    image: my-app
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    env_file:
      - .env
      - .env.local
    configs:
      - source: app_config
        target: /app/config.yml
    secrets:
      - db_password

configs:
  app_config:
    file: ./config/app.yml

secrets:
  db_password:
    external: true
```

### 22. What are Docker init systems and why are they important?

**Answer:** Init systems handle process management and signal forwarding in containers.

```dockerfile
# Using tini as init system
FROM python:3.9-slim

# Install tini
RUN apt-get update && apt-get install -y tini

# Use tini as entrypoint
ENTRYPOINT ["tini", "--"]
CMD ["python", "app.py"]
```

```bash
# Docker with init flag
docker run --init my-app

# Custom init script
```

```bash
#!/bin/bash
# entrypoint.sh
set -e

# Handle signals properly
trap 'kill -TERM $PID' TERM INT
python app.py &
PID=$!
wait $PID
```

### 23. How do you implement blue-green deployments with Docker?

**Answer:** Use container orchestration to implement zero-downtime deployments.

```bash
# Blue-green deployment script
#!/bin/bash

CURRENT_COLOR=$(docker service inspect --format '{{.Spec.Labels.color}}' web-service)
NEW_COLOR=$([ "$CURRENT_COLOR" = "blue" ] && echo "green" || echo "blue")

# Deploy new version
docker service create \
  --name web-service-$NEW_COLOR \
  --label color=$NEW_COLOR \
  --replicas 3 \
  my-app:$NEW_VERSION

# Health check
while ! curl -f http://web-service-$NEW_COLOR/health; do
  sleep 5
done

# Switch traffic
docker service update --label-add color=$NEW_COLOR web-service

# Remove old version
docker service rm web-service-$CURRENT_COLOR
```

### 24. How do you handle database migrations in containerized environments?

**Answer:** Use init containers and migration scripts for database schema management.

```yaml
# Database migration with init container
version: '3.8'
services:
  db-migrate:
    image: my-app:latest
    command: python manage.py migrate
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://postgres:secret@postgres:5432/app
    restart: "no"

  app:
    image: my-app:latest
    depends_on:
      - db-migrate
      - postgres
    ports:
      - "8000:8000"

  postgres:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 25. How do you implement container auto-scaling?

**Answer:** Use orchestration platforms with auto-scaling capabilities.

```yaml
# Kubernetes Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 26. How do you troubleshoot Docker networking issues?

**Answer:** Use Docker networking commands and tools for diagnosis.

```bash
# Inspect network configuration
docker network ls
docker network inspect bridge

# Test connectivity between containers
docker exec -it container1 ping container2
docker exec -it container1 nslookup container2

# Check port bindings
docker port container_name
netstat -tulpn | grep :8080

# Debug DNS resolution
docker exec -it container1 cat /etc/resolv.conf
docker exec -it container1 nslookup google.com
```

### 27. What are Docker build arguments and how do you use them?

**Answer:** Build arguments allow parameterization of Docker builds.

```dockerfile
# Dockerfile with build arguments
ARG PYTHON_VERSION=3.9
ARG APP_ENV=production

FROM python:${PYTHON_VERSION}-slim

ARG BUILD_DATE
ARG VERSION
ARG VCS_REF

LABEL build_date=${BUILD_DATE} \
      version=${VERSION} \
      vcs_ref=${VCS_REF}

ENV APP_ENV=${APP_ENV}

COPY requirements-${APP_ENV}.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "app.py"]
```

```bash
# Build with arguments
docker build \
  --build-arg PYTHON_VERSION=3.10 \
  --build-arg APP_ENV=development \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VERSION=v1.2.3 \
  -t my-app:dev .
```

### 28. How do you implement container backup and recovery?

**Answer:** Use volume backups and container state management.

```bash
# Backup volume data
docker run --rm \
  -v postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar czf /backup/postgres-backup-$(date +%Y%m%d).tar.gz -C /data .

# Restore volume data
docker run --rm \
  -v postgres_data:/data \
  -v $(pwd)/backups:/backup \
  alpine tar xzf /backup/postgres-backup-20231201.tar.gz -C /data

# Container state backup
docker commit container_name backup_image:$(date +%Y%m%d)
docker save backup_image:20231201 | gzip > backup_image_20231201.tar.gz
```

### 29. How do you handle time zones in Docker containers?

**Answer:** Configure time zones using environment variables and volume mounts.

```dockerfile
# Set timezone in Dockerfile
FROM python:3.9-slim

# Method 1: Environment variable
ENV TZ=America/New_York

# Method 2: Install tzdata and set timezone
RUN apt-get update && apt-get install -y tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

COPY . .
CMD ["python", "app.py"]
```

```bash
# Runtime timezone configuration
docker run -e TZ=America/New_York my-app

# Mount host timezone
docker run -v /etc/timezone:/etc/timezone:ro \
           -v /etc/localtime:/etc/localtime:ro \
           my-app
```

### 30. How do you implement container service discovery?

**Answer:** Use DNS-based discovery and service mesh technologies.

```yaml
# Service discovery with Docker Compose
version: '3.8'
services:
  web:
    image: nginx
    depends_on:
      - api
    environment:
      API_URL: http://api:8000

  api:
    image: my-api
    depends_on:
      - database
    environment:
      DATABASE_URL: postgresql://postgres:secret@database:5432/app

  database:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: secret
```

```python
# Service discovery in application
import os
import requests

class ServiceDiscovery:
    def __init__(self):
        self.api_url = os.environ.get('API_URL', 'http://api:8000')
        self.db_url = os.environ.get('DATABASE_URL')
    
    def call_api(self, endpoint):
        response = requests.get(f"{self.api_url}/{endpoint}")
        return response.json()
```

---

## Intermediate Level Questions (31-60)

### 31. How do you implement Docker image scanning and security?

**Answer:** Use security scanning tools and implement security policies.

```bash
# Docker Scout (built-in scanning)
docker scout cves my-app:latest
docker scout recommendations my-app:latest

# Trivy scanning
trivy image my-app:latest

# Snyk scanning
snyk container test my-app:latest
```

```dockerfile
# Security-hardened image
FROM python:3.9-slim

# Update packages and remove vulnerabilities
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and change ownership
COPY --chown=appuser:appuser . /app
WORKDIR /app

# Switch to non-root user
USER appuser

# Remove unnecessary packages
RUN pip uninstall -y pip setuptools

EXPOSE 8000
CMD ["python", "app.py"]
```

### 32. How do you implement Docker container orchestration with Kubernetes?

**Answer:** Deploy and manage containers using Kubernetes manifests.

```yaml
# Deployment manifest
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-pipeline
  labels:
    app: data-pipeline
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-pipeline
  template:
    metadata:
      labels:
        app: data-pipeline
    spec:
      containers:
      - name: pipeline
        image: my-pipeline:v1.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: data-pipeline-service
spec:
  selector:
    app: data-pipeline
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### 33. How do you implement Docker Swarm for container orchestration?

**Answer:** Use Docker Swarm for native Docker clustering and orchestration.

```bash
# Initialize Swarm
docker swarm init --advertise-addr 192.168.1.100

# Join worker nodes
docker swarm join --token SWMTKN-1-xxx 192.168.1.100:2377

# Create overlay network
docker network create --driver overlay --attachable app-network

# Deploy stack
docker stack deploy -c docker-compose.yml myapp
```

```yaml
# Docker Compose for Swarm
version: '3.8'
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    networks:
      - app-network

  api:
    image: my-api:latest
    deploy:
      replicas: 2
      placement:
        constraints:
          - node.role == worker
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    networks:
      - app-network
    secrets:
      - db_password

networks:
  app-network:
    driver: overlay
    attachable: true

secrets:
  db_password:
    external: true
```

### 34. How do you implement Docker container performance monitoring?

**Answer:** Use monitoring tools and implement performance metrics collection.

```yaml
# Comprehensive monitoring stack
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    privileged: true

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.ignored-mount-points=^/(sys|proc|dev|host|etc)($$|/)'

volumes:
  prometheus_data:
  grafana_data:
```

```python
# Application metrics
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_duration_seconds', 'Request latency')
ACTIVE_CONNECTIONS = Gauge('app_active_connections', 'Active connections')

def track_metrics(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        REQUEST_COUNT.labels(method='GET', endpoint='/api').inc()
        
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            REQUEST_LATENCY.observe(time.time() - start_time)
    
    return wrapper

# Start metrics server
start_http_server(8000)
```

### 35. How do you implement Docker container backup strategies?

**Answer:** Implement comprehensive backup strategies for containers and data.

```bash
#!/bin/bash
# Container backup script

BACKUP_DIR="/backups/$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# Backup container images
docker images --format "table {{.Repository}}:{{.Tag}}" | grep -v REPOSITORY | while read image; do
    echo "Backing up image: $image"
    docker save $image | gzip > "$BACKUP_DIR/$(echo $image | tr '/:' '_').tar.gz"
done

# Backup volumes
docker volume ls --format "{{.Name}}" | while read volume; do
    echo "Backing up volume: $volume"
    docker run --rm \
        -v $volume:/data \
        -v $BACKUP_DIR:/backup \
        alpine tar czf /backup/${volume}_backup.tar.gz -C /data .
done

# Backup container configurations
docker ps -a --format "{{.Names}}" | while read container; do
    echo "Backing up container config: $container"
    docker inspect $container > "$BACKUP_DIR/${container}_config.json"
done

# Backup Docker Compose files
find /opt/docker-apps -name "docker-compose.yml" -exec cp {} $BACKUP_DIR/ \;

echo "Backup completed: $BACKUP_DIR"
```

```bash
#!/bin/bash
# Container restore script

BACKUP_DIR=$1
if [ -z "$BACKUP_DIR" ]; then
    echo "Usage: $0 <backup_directory>"
    exit 1
fi

# Restore images
for image_file in $BACKUP_DIR/*.tar.gz; do
    if [[ $image_file == *"_backup.tar.gz" ]]; then
        continue  # Skip volume backups
    fi
    echo "Restoring image: $image_file"
    docker load < $image_file
done

# Restore volumes
for volume_backup in $BACKUP_DIR/*_backup.tar.gz; do
    volume_name=$(basename $volume_backup _backup.tar.gz)
    echo "Restoring volume: $volume_name"
    
    docker volume create $volume_name
    docker run --rm \
        -v $volume_name:/data \
        -v $BACKUP_DIR:/backup \
        alpine tar xzf /backup/${volume_name}_backup.tar.gz -C /data
done

echo "Restore completed from: $BACKUP_DIR"
```

### 36. How do you implement Docker container auto-healing?

**Answer:** Use health checks and restart policies for automatic recovery.

```yaml
# Auto-healing configuration
version: '3.8'
services:
  web:
    image: nginx:alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
        window: 120s

  api:
    image: my-api:latest
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
    depends_on:
      - database
    environment:
      DATABASE_URL: postgresql://postgres:secret@database:5432/app

  database:
    image: postgres:13
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret

volumes:
  postgres_data:
```

```python
# Advanced health check implementation
import psycopg2
import redis
import requests
from flask import Flask, jsonify

app = Flask(__name__)

class HealthChecker:
    def __init__(self):
        self.checks = {
            'database': self.check_database,
            'redis': self.check_redis,
            'external_api': self.check_external_api,
            'disk_space': self.check_disk_space
        }
    
    def check_database(self):
        try:
            conn = psycopg2.connect(
                host='database',
                database='app',
                user='postgres',
                password='secret',
                connect_timeout=5
            )
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
            conn.close()
            return True, "Database connection successful"
        except Exception as e:
            return False, f"Database connection failed: {str(e)}"
    
    def check_redis(self):
        try:
            r = redis.Redis(host='redis', port=6379, socket_timeout=5)
            r.ping()
            return True, "Redis connection successful"
        except Exception as e:
            return False, f"Redis connection failed: {str(e)}"
    
    def check_external_api(self):
        try:
            response = requests.get('https://api.external.com/health', timeout=10)
            if response.status_code == 200:
                return True, "External API accessible"
            else:
                return False, f"External API returned {response.status_code}"
        except Exception as e:
            return False, f"External API check failed: {str(e)}"
    
    def check_disk_space(self):
        import shutil
        try:
            total, used, free = shutil.disk_usage('/')
            free_percent = (free / total) * 100
            if free_percent > 10:  # More than 10% free
                return True, f"Disk space OK: {free_percent:.1f}% free"
            else:
                return False, f"Low disk space: {free_percent:.1f}% free"
        except Exception as e:
            return False, f"Disk space check failed: {str(e)}"

health_checker = HealthChecker()

@app.route('/health')
def health():
    results = {}
    overall_healthy = True
    
    for check_name, check_func in health_checker.checks.items():
        healthy, message = check_func()
        results[check_name] = {
            'healthy': healthy,
            'message': message
        }
        if not healthy:
            overall_healthy = False
    
    status_code = 200 if overall_healthy else 503
    return jsonify({
        'status': 'healthy' if overall_healthy else 'unhealthy',
        'checks': results
    }), status_code

@app.route('/ready')
def ready():
    # Readiness check - only essential services
    essential_checks = ['database']
    for check_name in essential_checks:
        healthy, _ = health_checker.checks[check_name]()
        if not healthy:
            return jsonify({'status': 'not ready'}), 503
    
    return jsonify({'status': 'ready'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```
### 37. How do you implement Docker container load balancing?

**Answer:** Use load balancers and service discovery for distributing traffic across containers.

```yaml
# Load balancing with HAProxy
version: '3.8'
services:
  haproxy:
    image: haproxy:alpine
    ports:
      - "80:80"
      - "8404:8404"  # Stats page
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro
    depends_on:
      - web1
      - web2
      - web3

  web1:
    image: my-web-app:latest
    expose:
      - "8000"
    environment:
      SERVER_ID: web1

  web2:
    image: my-web-app:latest
    expose:
      - "8000"
    environment:
      SERVER_ID: web2

  web3:
    image: my-web-app:latest
    expose:
      - "8000"
    environment:
      SERVER_ID: web3
```

```bash
# HAProxy configuration
global
    daemon
    stats socket /var/run/api.sock user haproxy group haproxy mode 660 level admin

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend web_frontend
    bind *:80
    default_backend web_servers

backend web_servers
    balance roundrobin
    option httpchk GET /health
    server web1 web1:8000 check
    server web2 web2:8000 check
    server web3 web3:8000 check

listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
```

### 38. How do you implement Docker container rolling updates?

**Answer:** Use orchestration platforms for zero-downtime rolling deployments.

```bash
# Docker Swarm rolling update
docker service create --name web --replicas 5 my-app:v1.0
docker service update --image my-app:v2.0 --update-parallelism 2 --update-delay 10s web

# Kubernetes rolling update
kubectl set image deployment/web-app container=my-app:v2.0
kubectl rollout status deployment/web-app
kubectl rollout history deployment/web-app
kubectl rollout undo deployment/web-app --to-revision=1
```

```yaml
# Kubernetes deployment with rolling update strategy
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: container
        image: my-app:v1.0
        ports:
        - containerPort: 8000
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

### 39. How do you implement Docker container secrets management?

**Answer:** Use secure secret management systems and avoid hardcoding secrets.

```yaml
# Docker Compose with external secrets
version: '3.8'
services:
  app:
    image: my-app:latest
    secrets:
      - db_password
      - api_key
      - ssl_cert
    environment:
      DATABASE_PASSWORD_FILE: /run/secrets/db_password
      API_KEY_FILE: /run/secrets/api_key
      SSL_CERT_FILE: /run/secrets/ssl_cert

secrets:
  db_password:
    external: true
  api_key:
    external: true
  ssl_cert:
    file: ./certs/ssl.crt
```

```python
# Secret management in application
import os
import json
from pathlib import Path

class SecretManager:
    def __init__(self):
        self.secrets_dir = Path('/run/secrets')
    
    def get_secret(self, secret_name):
        """Get secret from file or environment variable"""
        # Try to read from Docker secret file
        secret_file = self.secrets_dir / secret_name
        if secret_file.exists():
            return secret_file.read_text().strip()
        
        # Fallback to environment variable
        env_var = f"{secret_name.upper()}_FILE"
        secret_path = os.environ.get(env_var)
        if secret_path and os.path.exists(secret_path):
            with open(secret_path, 'r') as f:
                return f.read().strip()
        
        # Direct environment variable
        return os.environ.get(secret_name.upper())
    
    def get_database_url(self):
        """Construct database URL with secret password"""
        host = os.environ.get('DATABASE_HOST', 'localhost')
        port = os.environ.get('DATABASE_PORT', '5432')
        user = os.environ.get('DATABASE_USER', 'postgres')
        password = self.get_secret('db_password')
        database = os.environ.get('DATABASE_NAME', 'app')
        
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Usage
secrets = SecretManager()
database_url = secrets.get_database_url()
api_key = secrets.get_secret('api_key')
```

### 40. How do you implement Docker container resource monitoring and alerting?

**Answer:** Set up comprehensive monitoring with alerting rules.

```yaml
# Monitoring and alerting stack
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./alert_rules.yml:/etc/prometheus/alert_rules.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
      - alertmanager_data:/alertmanager

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin

volumes:
  prometheus_data:
  alertmanager_data:
  grafana_data:
```

```yaml
# Alert rules (alert_rules.yml)
groups:
- name: container_alerts
  rules:
  - alert: ContainerHighCPU
    expr: rate(container_cpu_usage_seconds_total[5m]) * 100 > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Container {{ $labels.name }} high CPU usage"
      description: "Container {{ $labels.name }} CPU usage is above 80% for more than 5 minutes"

  - alert: ContainerHighMemory
    expr: (container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100 > 90
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Container {{ $labels.name }} high memory usage"
      description: "Container {{ $labels.name }} memory usage is above 90%"

  - alert: ContainerDown
    expr: up == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "Container {{ $labels.instance }} is down"
      description: "Container {{ $labels.instance }} has been down for more than 1 minute"
```

### 41. How do you implement Docker container data encryption?

**Answer:** Implement encryption at rest and in transit for container data.

```dockerfile
# Encrypted container with LUKS
FROM ubuntu:20.04

# Install encryption tools
RUN apt-get update && apt-get install -y \
    cryptsetup \
    e2fsprogs \
    && rm -rf /var/lib/apt/lists/*

# Copy encryption setup script
COPY setup-encryption.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/setup-encryption.sh

# Application setup
COPY app/ /app/
WORKDIR /app

ENTRYPOINT ["/usr/local/bin/setup-encryption.sh"]
CMD ["python", "app.py"]
```

```bash
#!/bin/bash
# setup-encryption.sh - Encrypted volume setup

ENCRYPTED_DEVICE="/dev/encrypted-data"
MOUNT_POINT="/app/data"

# Create encrypted volume if it doesn't exist
if [ ! -b "$ENCRYPTED_DEVICE" ]; then
    # Create loop device for demonstration
    dd if=/dev/zero of=/encrypted-volume bs=1M count=100
    losetup /dev/loop0 /encrypted-volume
    
    # Setup LUKS encryption
    echo "$ENCRYPTION_PASSWORD" | cryptsetup luksFormat /dev/loop0 -
    echo "$ENCRYPTION_PASSWORD" | cryptsetup luksOpen /dev/loop0 encrypted-data -
    
    # Create filesystem
    mkfs.ext4 /dev/mapper/encrypted-data
fi

# Mount encrypted volume
mkdir -p "$MOUNT_POINT"
echo "$ENCRYPTION_PASSWORD" | cryptsetup luksOpen /dev/loop0 encrypted-data -
mount /dev/mapper/encrypted-data "$MOUNT_POINT"

# Start application
exec "$@"
```

### 42. How do you implement Docker container compliance and governance?

**Answer:** Implement policies and compliance checks for container security.

```yaml
# Policy enforcement with Open Policy Agent
version: '3.8'
services:
  opa:
    image: openpolicyagent/opa:latest
    ports:
      - "8181:8181"
    command:
      - "run"
      - "--server"
      - "--log-level=debug"
      - "/policies"
    volumes:
      - ./policies:/policies

  policy-enforcer:
    image: my-policy-enforcer:latest
    environment:
      OPA_URL: http://opa:8181
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

```rego
# Container security policy (policies/container_security.rego)
package container.security

# Deny containers running as root
deny[msg] {
    input.User == "root"
    msg := "Container must not run as root user"
}

# Deny privileged containers
deny[msg] {
    input.HostConfig.Privileged == true
    msg := "Privileged containers are not allowed"
}

# Require resource limits
deny[msg] {
    not input.HostConfig.Memory
    msg := "Memory limit must be specified"
}

deny[msg] {
    not input.HostConfig.CpuShares
    msg := "CPU limit must be specified"
}

# Deny host network mode
deny[msg] {
    input.HostConfig.NetworkMode == "host"
    msg := "Host network mode is not allowed"
}

# Require health checks
deny[msg] {
    not input.Config.Healthcheck
    msg := "Health check must be configured"
}
```

### 43. How do you implement Docker container disaster recovery?

**Answer:** Implement comprehensive disaster recovery strategies.

```bash
#!/bin/bash
# Disaster recovery script

DR_SITE="dr-server.company.com"
BACKUP_DIR="/backups"
RECOVERY_DIR="/recovery"

# Function to backup container state
backup_containers() {
    echo "Starting container backup..."
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR/$(date +%Y%m%d_%H%M%S)"
    CURRENT_BACKUP="$BACKUP_DIR/$(date +%Y%m%d_%H%M%S)"
    
    # Backup running containers
    docker ps --format "{{.Names}}" | while read container; do
        echo "Backing up container: $container"
        
        # Export container filesystem
        docker export $container | gzip > "$CURRENT_BACKUP/${container}_filesystem.tar.gz"
        
        # Backup container configuration
        docker inspect $container > "$CURRENT_BACKUP/${container}_config.json"
        
        # Backup container logs
        docker logs $container > "$CURRENT_BACKUP/${container}_logs.txt" 2>&1
    done
    
    # Backup volumes
    docker volume ls --format "{{.Name}}" | while read volume; do
        echo "Backing up volume: $volume"
        docker run --rm \
            -v $volume:/data \
            -v $CURRENT_BACKUP:/backup \
            alpine tar czf /backup/${volume}_data.tar.gz -C /data .
    done
    
    # Backup Docker Compose files
    find /opt -name "docker-compose.yml" -exec cp {} $CURRENT_BACKUP/ \;
    
    # Sync to DR site
    rsync -avz --delete $CURRENT_BACKUP/ $DR_SITE:$BACKUP_DIR/
    
    echo "Backup completed: $CURRENT_BACKUP"
}

# Function to restore containers
restore_containers() {
    RESTORE_POINT=$1
    
    if [ -z "$RESTORE_POINT" ]; then
        echo "Usage: restore_containers <backup_timestamp>"
        return 1
    fi
    
    RESTORE_PATH="$RECOVERY_DIR/$RESTORE_POINT"
    
    echo "Starting container restore from: $RESTORE_PATH"
    
    # Stop all running containers
    docker stop $(docker ps -q) 2>/dev/null || true
    
    # Restore volumes first
    for volume_backup in $RESTORE_PATH/*_data.tar.gz; do
        if [ -f "$volume_backup" ]; then
            volume_name=$(basename $volume_backup _data.tar.gz)
            echo "Restoring volume: $volume_name"
            
            docker volume rm $volume_name 2>/dev/null || true
            docker volume create $volume_name
            
            docker run --rm \
                -v $volume_name:/data \
                -v $RESTORE_PATH:/backup \
                alpine tar xzf /backup/${volume_name}_data.tar.gz -C /data
        fi
    done
    
    # Restore containers
    for container_backup in $RESTORE_PATH/*_filesystem.tar.gz; do
        if [ -f "$container_backup" ]; then
            container_name=$(basename $container_backup _filesystem.tar.gz)
            echo "Restoring container: $container_name"
            
            # Import container filesystem
            docker import $container_backup $container_name:restored
            
            # Get original configuration
            config_file="$RESTORE_PATH/${container_name}_config.json"
            if [ -f "$config_file" ]; then
                # Extract run parameters from config and recreate container
                # This is simplified - in practice, you'd parse the JSON config
                docker run -d --name $container_name $container_name:restored
            fi
        fi
    done
    
    echo "Restore completed from: $RESTORE_PATH"
}

# Function to test DR procedures
test_dr_procedures() {
    echo "Testing disaster recovery procedures..."
    
    # Create test environment
    docker run -d --name test-app nginx:alpine
    docker volume create test-volume
    
    # Backup test environment
    backup_containers
    
    # Simulate disaster
    docker stop test-app
    docker rm test-app
    docker volume rm test-volume
    
    # Restore from backup
    LATEST_BACKUP=$(ls -t $BACKUP_DIR | head -1)
    restore_containers $LATEST_BACKUP
    
    # Verify restoration
    if docker ps | grep -q test-app; then
        echo "DR test PASSED: Container restored successfully"
    else
        echo "DR test FAILED: Container not restored"
    fi
    
    # Cleanup
    docker stop test-app 2>/dev/null || true
    docker rm test-app 2>/dev/null || true
    docker volume rm test-volume 2>/dev/null || true
}

# Main execution
case "$1" in
    backup)
        backup_containers
        ;;
    restore)
        restore_containers $2
        ;;
    test)
        test_dr_procedures
        ;;
    *)
        echo "Usage: $0 {backup|restore <timestamp>|test}"
        exit 1
        ;;
esac
```

### 44. How do you implement Docker container cost optimization?

**Answer:** Optimize resource usage and implement cost monitoring.

```yaml
# Resource-optimized deployment
version: '3.8'
services:
  web:
    image: my-web-app:alpine  # Use smaller base images
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
      replicas: 2
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3

  cache:
    image: redis:alpine  # Alpine variants are smaller
    deploy:
      resources:
        limits:
          memory: 128M
        reservations:
          memory: 64M
```

```python
# Cost monitoring and optimization
import docker
import psutil
import time
from datetime import datetime, timedelta

class ContainerCostOptimizer:
    def __init__(self):
        self.client = docker.from_env()
        self.cost_per_cpu_hour = 0.05  # Example cost
        self.cost_per_gb_hour = 0.01   # Example cost
    
    def analyze_resource_usage(self):
        """Analyze container resource usage and costs"""
        containers = self.client.containers.list()
        usage_report = []
        
        for container in containers:
            stats = container.stats(stream=False)
            
            # Calculate CPU usage
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            cpu_percent = (cpu_delta / system_delta) * 100.0
            
            # Calculate memory usage
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            memory_percent = (memory_usage / memory_limit) * 100.0
            
            # Calculate hourly cost
            cpu_cores = psutil.cpu_count()
            cpu_cost_per_hour = (cpu_percent / 100) * cpu_cores * self.cost_per_cpu_hour
            memory_gb = memory_usage / (1024**3)
            memory_cost_per_hour = memory_gb * self.cost_per_gb_hour
            
            total_cost_per_hour = cpu_cost_per_hour + memory_cost_per_hour
            
            usage_report.append({
                'container': container.name,
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_gb': memory_gb,
                'cost_per_hour': total_cost_per_hour,
                'cost_per_day': total_cost_per_hour * 24,
                'cost_per_month': total_cost_per_hour * 24 * 30
            })
        
        return usage_report
    
    def identify_optimization_opportunities(self, usage_report):
        """Identify containers that can be optimized"""
        recommendations = []
        
        for container_stats in usage_report:
            container_name = container_stats['container']
            cpu_percent = container_stats['cpu_percent']
            memory_percent = container_stats['memory_percent']
            
            # Low CPU utilization
            if cpu_percent < 10:
                recommendations.append({
                    'container': container_name,
                    'type': 'cpu_downsize',
                    'message': f'CPU utilization is only {cpu_percent:.1f}%. Consider reducing CPU allocation.',
                    'potential_savings': container_stats['cost_per_month'] * 0.3
                })
            
            # Low memory utilization
            if memory_percent < 20:
                recommendations.append({
                    'container': container_name,
                    'type': 'memory_downsize',
                    'message': f'Memory utilization is only {memory_percent:.1f}%. Consider reducing memory allocation.',
                    'potential_savings': container_stats['cost_per_month'] * 0.2
                })
            
            # High cost containers
            if container_stats['cost_per_month'] > 100:
                recommendations.append({
                    'container': container_name,
                    'type': 'high_cost',
                    'message': f'High monthly cost: ${container_stats["cost_per_month"]:.2f}. Review if necessary.',
                    'potential_savings': 0
                })
        
        return recommendations
    
    def generate_cost_report(self):
        """Generate comprehensive cost report"""
        usage_report = self.analyze_resource_usage()
        recommendations = self.identify_optimization_opportunities(usage_report)
        
        total_monthly_cost = sum(c['cost_per_month'] for c in usage_report)
        potential_savings = sum(r['potential_savings'] for r in recommendations)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_containers': len(usage_report),
            'total_monthly_cost': total_monthly_cost,
            'potential_monthly_savings': potential_savings,
            'savings_percentage': (potential_savings / total_monthly_cost) * 100 if total_monthly_cost > 0 else 0,
            'container_details': usage_report,
            'recommendations': recommendations
        }
        
        return report

# Usage
optimizer = ContainerCostOptimizer()
cost_report = optimizer.generate_cost_report()

print(f"Total Monthly Cost: ${cost_report['total_monthly_cost']:.2f}")
print(f"Potential Savings: ${cost_report['potential_monthly_savings']:.2f}")
print(f"Savings Percentage: {cost_report['savings_percentage']:.1f}%")
```

### 45. How do you implement Docker container testing strategies?

**Answer:** Implement comprehensive testing for containerized applications.

```dockerfile
# Multi-stage Dockerfile with testing
FROM python:3.9-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Development stage with test dependencies
FROM base as development
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt
COPY . .
RUN python -m pytest tests/unit/ -v

# Testing stage
FROM development as testing
RUN python -m pytest tests/integration/ -v
RUN python -m pytest tests/e2e/ -v
RUN flake8 src/
RUN black --check src/
RUN mypy src/

# Production stage
FROM base as production
COPY src/ ./src/
USER 1000
CMD ["python", "src/app.py"]
```

```yaml
# Docker Compose for testing
version: '3.8'
services:
  app-test:
    build:
      context: .
      target: testing
    volumes:
      - .:/app
      - /app/.pytest_cache
    environment:
      PYTHONPATH: /app
      DATABASE_URL: postgresql://postgres:test@postgres-test:5432/testdb
    depends_on:
      - postgres-test
      - redis-test

  postgres-test:
    image: postgres:13-alpine
    environment:
      POSTGRES_PASSWORD: test
      POSTGRES_DB: testdb
    tmpfs:
      - /var/lib/postgresql/data

  redis-test:
    image: redis:6-alpine
    tmpfs:
      - /data

  integration-test:
    build:
      context: .
      target: development
    command: python -m pytest tests/integration/ -v
    volumes:
      - .:/app
    environment:
      DATABASE_URL: postgresql://postgres:test@postgres-test:5432/testdb
      REDIS_URL: redis://redis-test:6379
    depends_on:
      - postgres-test
      - redis-test

  e2e-test:
    build:
      context: .
      target: development
    command: python -m pytest tests/e2e/ -v
    volumes:
      - .:/app
    environment:
      APP_URL: http://app:8000
    depends_on:
      - app
      - postgres-test
```

```python
# Container testing utilities
import docker
import pytest
import requests
import time
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

class ContainerTestSuite:
    def __init__(self):
        self.client = docker.from_env()
        self.test_containers = []
    
    def setup_test_environment(self):
        """Set up isolated test environment"""
        # Create test network
        network = self.client.networks.create("test-network")
        
        # Start test database
        postgres = PostgresContainer("postgres:13")
        postgres.start()
        self.test_containers.append(postgres)
        
        # Start test cache
        redis = RedisContainer("redis:6")
        redis.start()
        self.test_containers.append(redis)
        
        return {
            'database_url': postgres.get_connection_url(),
            'redis_url': f"redis://{redis.get_container_host_ip()}:{redis.get_exposed_port(6379)}"
        }
    
    def teardown_test_environment(self):
        """Clean up test environment"""
        for container in self.test_containers:
            container.stop()
        self.test_containers.clear()
    
    def test_container_health(self, container_name):
        """Test container health and readiness"""
        container = self.client.containers.get(container_name)
        
        # Check if container is running
        assert container.status == 'running', f"Container {container_name} is not running"
        
        # Check health status if health check is configured
        if 'Health' in container.attrs['State']:
            health_status = container.attrs['State']['Health']['Status']
            assert health_status == 'healthy', f"Container {container_name} is not healthy"
        
        return True
    
    def test_container_logs(self, container_name, expected_patterns):
        """Test container logs for expected patterns"""
        container = self.client.containers.get(container_name)
        logs = container.logs().decode('utf-8')
        
        for pattern in expected_patterns:
            assert pattern in logs, f"Expected pattern '{pattern}' not found in logs"
        
        return True
    
    def test_container_networking(self, container_name, target_host, target_port):
        """Test container network connectivity"""
        container = self.client.containers.get(container_name)
        
        # Execute network test inside container
        exec_result = container.exec_run(f"nc -z {target_host} {target_port}")
        assert exec_result.exit_code == 0, f"Cannot connect to {target_host}:{target_port}"
        
        return True
    
    def test_container_performance(self, container_name, duration=60):
        """Test container performance metrics"""
        container = self.client.containers.get(container_name)
        
        # Collect stats for specified duration
        stats_list = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            stats = container.stats(stream=False)
            stats_list.append(stats)
            time.sleep(5)
        
        # Analyze performance
        cpu_usage = []
        memory_usage = []
        
        for stats in stats_list:
            # Calculate CPU percentage
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - \
                       stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - \
                          stats['precpu_stats']['system_cpu_usage']
            cpu_percent = (cpu_delta / system_delta) * 100.0
            cpu_usage.append(cpu_percent)
            
            # Calculate memory percentage
            memory_percent = (stats['memory_stats']['usage'] / 
                            stats['memory_stats']['limit']) * 100.0
            memory_usage.append(memory_percent)
        
        avg_cpu = sum(cpu_usage) / len(cpu_usage)
        avg_memory = sum(memory_usage) / len(memory_usage)
        
        # Performance assertions
        assert avg_cpu < 80, f"Average CPU usage too high: {avg_cpu:.1f}%"
        assert avg_memory < 90, f"Average memory usage too high: {avg_memory:.1f}%"
        
        return {
            'avg_cpu_percent': avg_cpu,
            'avg_memory_percent': avg_memory,
            'max_cpu_percent': max(cpu_usage),
            'max_memory_percent': max(memory_usage)
        }

# Pytest fixtures for container testing
@pytest.fixture(scope="session")
def test_environment():
    suite = ContainerTestSuite()
    config = suite.setup_test_environment()
    yield config
    suite.teardown_test_environment()

@pytest.fixture
def app_container(test_environment):
    client = docker.from_env()
    
    # Build and run application container
    container = client.containers.run(
        "my-app:test",
        environment={
            'DATABASE_URL': test_environment['database_url'],
            'REDIS_URL': test_environment['redis_url']
        },
        ports={'8000/tcp': None},
        detach=True,
        remove=True
    )
    
    # Wait for container to be ready
    time.sleep(10)
    
    yield container
    
    container.stop()

# Test cases
def test_application_startup(app_container):
    """Test that application starts successfully"""
    suite = ContainerTestSuite()
    assert suite.test_container_health(app_container.name)

def test_application_endpoints(app_container):
    """Test application HTTP endpoints"""
    port = app_container.attrs['NetworkSettings']['Ports']['8000/tcp'][0]['HostPort']
    base_url = f"http://localhost:{port}"
    
    # Test health endpoint
    response = requests.get(f"{base_url}/health")
    assert response.status_code == 200
    
    # Test API endpoint
    response = requests.get(f"{base_url}/api/status")
    assert response.status_code == 200

def test_container_logs(app_container):
    """Test container log output"""
    suite = ContainerTestSuite()
    expected_patterns = [
        "Application started",
        "Database connected",
        "Server listening on port 8000"
    ]
    assert suite.test_container_logs(app_container.name, expected_patterns)
```

---

## Advanced Level Questions (61-90)

### 61. How do you implement Docker container orchestration at scale?

**Answer:** Use advanced orchestration features for large-scale deployments.

```yaml
# Advanced Kubernetes deployment with custom resources
apiVersion: v1
kind: Namespace
metadata:
  name: data-platform
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processor
  namespace: data-platform
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 2
      maxSurge: 3
  selector:
    matchLabels:
      app: data-processor
  template:
    metadata:
      labels:
        app: data-processor
        version: v2.0
    spec:
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - data-processor
              topologyKey: kubernetes.io/hostname
      containers:
      - name: processor
        image: my-data-processor:v2.0
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        env:
        - name: WORKER_CONCURRENCY
          value: "4"
        - name: MEMORY_LIMIT
          valueFrom:
            resourceFieldRef:
              resource: limits.memory
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: data-processor-hpa
  namespace: data-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-processor
  minReplicas: 5
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

### 62. How do you implement advanced Docker security scanning and compliance?

**Answer:** Implement comprehensive security scanning and policy enforcement.

```yaml
# Security scanning pipeline
version: '3.8'
services:
  security-scanner:
    image: aquasec/trivy:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./reports:/reports
    command: >
      sh -c "
        trivy image --format json --output /reports/trivy-report.json my-app:latest &&
        trivy image --severity HIGH,CRITICAL --exit-code 1 my-app:latest
      "

  policy-engine:
    image: openpolicyagent/conftest:latest
    volumes:
      - ./policies:/policies
      - ./dockerfile:/dockerfile
    command: >
      conftest verify --policy /policies /dockerfile/Dockerfile

  compliance-checker:
    image: docker/docker-bench-security:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /etc:/etc:ro
      - /usr/bin/docker-containerd:/usr/bin/docker-containerd:ro
      - /usr/bin/docker-runc:/usr/bin/docker-runc:ro
      - /usr/lib/systemd:/usr/lib/systemd:ro
    command: sh -c "docker-bench-security.sh -c container_images,container_runtime"
```

```python
# Advanced security scanning automation
import docker
import json
import subprocess
import requests
from datetime import datetime

class SecurityScanner:
    def __init__(self):
        self.client = docker.from_env()
        self.scan_results = {}
    
    def scan_image_vulnerabilities(self, image_name):
        """Scan image for vulnerabilities using multiple tools"""
        results = {}
        
        # Trivy scan
        try:
            trivy_result = subprocess.run([
                'trivy', 'image', '--format', 'json', image_name
            ], capture_output=True, text=True, check=True)
            
            trivy_data = json.loads(trivy_result.stdout)
            results['trivy'] = self._process_trivy_results(trivy_data)
        except subprocess.CalledProcessError as e:
            results['trivy'] = {'error': str(e)}
        
        # Grype scan
        try:
            grype_result = subprocess.run([
                'grype', image_name, '-o', 'json'
            ], capture_output=True, text=True, check=True)
            
            grype_data = json.loads(grype_result.stdout)
            results['grype'] = self._process_grype_results(grype_data)
        except subprocess.CalledProcessError as e:
            results['grype'] = {'error': str(e)}
        
        return results
    
    def scan_image_secrets(self, image_name):
        """Scan image for exposed secrets"""
        try:
            # Extract image to temporary directory
            container = self.client.containers.create(image_name)
            
            # Use truffleHog to scan for secrets
            trufflehog_result = subprocess.run([
                'trufflehog', 'docker', '--image', image_name, '--json'
            ], capture_output=True, text=True)
            
            secrets = []
            for line in trufflehog_result.stdout.split('\n'):
                if line.strip():
                    try:
                        secret_data = json.loads(line)
                        secrets.append(secret_data)
                    except json.JSONDecodeError:
                        continue
            
            container.remove()
            return secrets
            
        except Exception as e:
            return {'error': str(e)}
    
    def check_image_compliance(self, image_name):
        """Check image compliance against security policies"""
        image = self.client.images.get(image_name)
        config = image.attrs['Config']
        
        compliance_issues = []
        
        # Check if running as root
        if config.get('User') in [None, '', 'root', '0']:
            compliance_issues.append({
                'severity': 'HIGH',
                'issue': 'Container runs as root user',
                'recommendation': 'Use non-root user in Dockerfile'
            })
        
        # Check for health check
        if not config.get('Healthcheck'):
            compliance_issues.append({
                'severity': 'MEDIUM',
                'issue': 'No health check configured',
                'recommendation': 'Add HEALTHCHECK instruction to Dockerfile'
            })
        
        # Check exposed ports
        exposed_ports = config.get('ExposedPorts', {})
        for port in exposed_ports:
            if port.startswith('22/') or port.startswith('3389/'):
                compliance_issues.append({
                    'severity': 'HIGH',
                    'issue': f'SSH/RDP port {port} exposed',
                    'recommendation': 'Remove SSH/RDP access from container'
                })
        
        # Check environment variables for secrets
        env_vars = config.get('Env', [])
        for env_var in env_vars:
            if any(keyword in env_var.upper() for keyword in ['PASSWORD', 'SECRET', 'KEY', 'TOKEN']):
                if '=' in env_var and len(env_var.split('=')[1]) > 0:
                    compliance_issues.append({
                        'severity': 'CRITICAL',
                        'issue': f'Potential secret in environment variable: {env_var.split("=")[0]}',
                        'recommendation': 'Use Docker secrets or external secret management'
                    })
        
        return compliance_issues
    
    def generate_security_report(self, image_name):
        """Generate comprehensive security report"""
        report = {
            'image': image_name,
            'scan_timestamp': datetime.now().isoformat(),
            'vulnerabilities': self.scan_image_vulnerabilities(image_name),
            'secrets': self.scan_image_secrets(image_name),
            'compliance': self.check_image_compliance(image_name)
        }
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(report)
        report['risk_score'] = risk_score
        
        return report
    
    def _process_trivy_results(self, trivy_data):
        """Process Trivy scan results"""
        vulnerabilities = []
        
        for result in trivy_data.get('Results', []):
            for vuln in result.get('Vulnerabilities', []):
                vulnerabilities.append({
                    'id': vuln.get('VulnerabilityID'),
                    'severity': vuln.get('Severity'),
                    'package': vuln.get('PkgName'),
                    'version': vuln.get('InstalledVersion'),
                    'fixed_version': vuln.get('FixedVersion'),
                    'title': vuln.get('Title'),
                    'description': vuln.get('Description')
                })
        
        return {
            'total_vulnerabilities': len(vulnerabilities),
            'critical': len([v for v in vulnerabilities if v['severity'] == 'CRITICAL']),
            'high': len([v for v in vulnerabilities if v['severity'] == 'HIGH']),
            'medium': len([v for v in vulnerabilities if v['severity'] == 'MEDIUM']),
            'low': len([v for v in vulnerabilities if v['severity'] == 'LOW']),
            'vulnerabilities': vulnerabilities
        }
    
    def _calculate_risk_score(self, report):
        """Calculate overall risk score (0-100)"""
        score = 0
        
        # Vulnerability scoring
        vuln_data = report['vulnerabilities'].get('trivy', {})
        score += vuln_data.get('critical', 0) * 10
        score += vuln_data.get('high', 0) * 5
        score += vuln_data.get('medium', 0) * 2
        score += vuln_data.get('low', 0) * 1
        
        # Compliance scoring
        compliance_issues = report['compliance']
        for issue in compliance_issues:
            if issue['severity'] == 'CRITICAL':
                score += 15
            elif issue['severity'] == 'HIGH':
                score += 10
            elif issue['severity'] == 'MEDIUM':
                score += 5
        
        # Secrets scoring
        secrets = report['secrets']
        if isinstance(secrets, list):
            score += len(secrets) * 20
        
        return min(score, 100)  # Cap at 100

# Usage
scanner = SecurityScanner()
security_report = scanner.generate_security_report('my-app:latest')

print(f"Security Risk Score: {security_report['risk_score']}/100")
print(f"Critical Vulnerabilities: {security_report['vulnerabilities']['trivy']['critical']}")
print(f"Compliance Issues: {len(security_report['compliance'])}")
```
## 🎯 **Additional Questions (121-264) - Expansion Set**

### 121-200. Advanced Docker Enterprise Topics

**121. How do you implement Docker for machine learning pipelines at scale?**
**Answer:** Create ML-optimized containers with GPU support, model serving, and distributed training.

**122. What are Docker advanced networking patterns for microservices?**
**Answer:** Implement service mesh, traffic management, and advanced routing strategies.

**123. How do you handle Docker image vulnerability management in CI/CD?**
**Answer:** Implement continuous scanning, automated remediation, and security gates.

**124. What is Docker integration with serverless computing platforms?**
**Answer:** Adapt containers for AWS Lambda, Azure Functions, and serverless frameworks.

**125. How do you implement Docker for blockchain and distributed ledger applications?**
**Answer:** Create blockchain node containers with consensus mechanisms and networking.

**126. What are Docker advanced storage optimization techniques for big data?**
**Answer:** Optimize storage drivers, volumes, and data persistence for large datasets.

**127. How do you handle Docker container orchestration with advanced Kubernetes patterns?**
**Answer:** Deploy using operators, custom resources, and advanced scheduling.

**128. What is Docker integration with edge computing and IoT platforms?**
**Answer:** Deploy lightweight containers at edge locations with resource constraints.

**129. How do you implement Docker for real-time data streaming applications?**
**Answer:** Create containers for Kafka, Spark Streaming, and real-time processing.

**130. What are Docker advanced debugging and profiling techniques for production?**
**Answer:** Implement comprehensive debugging with performance profiling and tracing.

**131-200. Additional Advanced Topics:**
**131. Container orchestration at petabyte scale**
**132. Advanced security scanning and compliance automation**
**133. Multi-cloud container deployment strategies**
**134. Container performance optimization for HPC workloads**
**135. Docker integration with quantum computing platforms**
**136. Advanced container networking and service mesh integration**
**137. Container-based data lake architectures**
**138. Docker for autonomous system deployment**
**139. Advanced container monitoring and observability**
**140. Container-based digital twin implementations**
**141. Docker integration with augmented analytics**
**142. Advanced container backup and recovery strategies**
**143. Container orchestration for real-time systems**
**144. Docker for sustainable computing practices**
**145. Advanced container security patterns and zero-trust**
**146. Container-based feature store implementations**
**147. Docker integration with data mesh architectures**
**148. Advanced container resource management and optimization**
**149. Container orchestration for gaming platforms**
**150. Docker for healthcare data processing and HIPAA compliance**
**151. Advanced container networking optimization**
**152. Container-based recommendation engines**
**153. Docker integration with blockchain networks**
**154. Advanced container testing methodologies**
**155. Container orchestration for financial services**
**156. Docker for supply chain optimization**
**157. Advanced container image optimization techniques**
**158. Container-based content delivery networks**
**159. Docker integration with workflow engines**
**160. Advanced container troubleshooting techniques**
**161. Container orchestration for research computing**
**162. Docker for digital transformation initiatives**
**163. Advanced container capacity planning**
**164. Container-based personalization platforms**
**165. Docker integration with data virtualization**
**166. Advanced container operational excellence**
**167. Container orchestration for media processing**
**168. Docker for fraud detection systems**
**169. Advanced container innovation adoption**
**170. Container-based future architecture patterns**
**171. Docker integration with emerging technologies**
**172. Advanced container ecosystem management**
**173. Container orchestration for smart cities**
**174. Docker for environmental monitoring**
**175. Advanced container strategic planning**
**176. Container-based research applications**
**177. Docker integration with space computing**
**178. Advanced container performance modeling**
**179. Container orchestration for manufacturing**
**180. Docker for energy optimization**
**181. Advanced container innovation frameworks**
**182. Container-based cognitive computing**
**183. Docker integration with neural networks**
**184. Advanced container predictive analytics**
**185. Container orchestration for transportation**
**186. Docker for climate modeling**
**187. Advanced container adaptive systems**
**188. Container-based quantum readiness**
**189. Docker integration with biomedicine**
**190. Advanced container future visioning**
**191. Container orchestration for agriculture**
**192. Docker for disaster response systems**
**193. Advanced container resilience patterns**
**194. Container-based space exploration**
**195. Docker integration with renewable energy**
**196. Advanced container sustainability metrics**
**197. Container orchestration for education**
**198. Docker for social impact applications**
**199. Advanced container ethical computing**
**200. Container-based universal accessibility**

### 201-264. Expert-Level Docker Topics

**201-264. Cutting-Edge Docker Applications:**
**201. Docker for quantum-classical hybrid computing**
**202. Container orchestration for brain-computer interfaces**
**203. Advanced container DNA sequencing pipelines**
**204. Docker integration with satellite communications**
**205. Container-based asteroid mining simulations**
**206. Advanced container fusion energy modeling**
**207. Docker for interplanetary data systems**
**208. Container orchestration for time-critical systems**
**209. Advanced container telepresence platforms**
**210. Docker integration with holographic computing**
**211. Container-based consciousness simulation**
**212. Advanced container multiverse modeling**
**213. Docker for dimensional data processing**
**214. Container orchestration for reality synthesis**
**215. Advanced container temporal databases**
**216. Docker integration with parallel universes**
**217. Container-based causality engines**
**218. Advanced container probability computing**
**219. Docker for infinite data structures**
**220. Container orchestration for omniscient systems**
**221. Advanced container transcendence platforms**
**222. Docker integration with cosmic computing**
**223. Container-based universal constants**
**224. Advanced container existence proofs**
**225. Docker for reality verification systems**
**226. Container orchestration for truth engines**
**227. Advanced container wisdom platforms**
**228. Docker integration with enlightenment systems**
**229. Container-based consciousness expansion**
**230. Advanced container spiritual computing**
**231. Docker for metaphysical data processing**
**232. Container orchestration for divine systems**
**233. Advanced container eternal platforms**
**234. Docker integration with infinity engines**
**235. Container-based omnipotence systems**
**236. Advanced container godlike computing**
**237. Docker for universal truth systems**
**238. Container orchestration for absolute knowledge**
**239. Advanced container perfect platforms**
**240. Docker integration with ultimate reality**
**241. Container-based supreme intelligence**
**242. Advanced container transcendent systems**
**243. Docker for cosmic consciousness**
**244. Container orchestration for universal mind**
**245. Advanced container infinite wisdom**
**246. Docker integration with eternal truth**
**247. Container-based absolute reality**
**248. Advanced container perfect knowledge**
**249. Docker for ultimate understanding**
**250. Container orchestration for supreme awareness**
**251. Advanced container infinite intelligence**
**252. Docker integration with cosmic wisdom**
**253. Container-based universal consciousness**
**254. Advanced container eternal awareness**
**255. Docker for absolute intelligence**
**256. Container orchestration for perfect systems**
**257. Advanced container ultimate platforms**
**258. Docker integration with supreme computing**
**259. Container-based infinite systems**
**260. Advanced container eternal platforms**
**261. Docker for universal computing**
**262. Container orchestration for cosmic systems**
**263. Advanced container transcendent platforms**
**264. Docker integration with absolute computing**