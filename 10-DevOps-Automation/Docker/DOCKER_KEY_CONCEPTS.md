# Docker Key Concepts for Data Engineering

## 1. Images and Containers
**What they are**: Images are blueprints, containers are running instances of those blueprints.

**Image Fundamentals**:
```bash
# Pull image from registry
docker pull python:3.9-slim
docker pull postgres:13
docker pull apache/airflow:2.5.0

# List local images
docker images
docker image ls

# Remove images
docker rmi python:3.8
docker image prune  # Remove unused images
```

**Container Lifecycle**:
```bash
# Run container (creates and starts)
docker run -d --name my-postgres \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:13

# Start/stop existing containers
docker start my-postgres
docker stop my-postgres
docker restart my-postgres

# List containers
docker ps          # Running containers
docker ps -a       # All containers

# Remove containers
docker rm my-postgres
docker container prune  # Remove stopped containers
```

**Container Interaction**:
```bash
# Execute commands in running container
docker exec -it my-postgres psql -U postgres

# Copy files to/from container
docker cp data.csv my-postgres:/tmp/
docker cp my-postgres:/tmp/output.csv ./

# View container logs
docker logs my-postgres
docker logs -f my-postgres  # Follow logs

# Inspect container details
docker inspect my-postgres
```

## 2. Dockerfile - Building Custom Images
**What it is**: Text file containing instructions to build a Docker image.

**Basic Dockerfile Structure**:
```dockerfile
# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app
USER app

# Expose port
EXPOSE 8000

# Define default command
CMD ["python", "app.py"]
```

**Data Engineering Dockerfile Example**:
```dockerfile
FROM apache/spark:3.3.0-scala2.12-java11-python3-ubuntu

# Switch to root to install packages
USER root

# Install additional Python packages for data engineering
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install additional system tools
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy data processing scripts
COPY scripts/ /opt/spark/scripts/
COPY data/ /opt/spark/data/

# Set permissions
RUN chmod +x /opt/spark/scripts/*.py

# Switch back to spark user
USER spark

# Set default working directory
WORKDIR /opt/spark

# Default command
CMD ["/opt/spark/bin/spark-submit", "/opt/spark/scripts/etl_job.py"]
```

**Build and Tag Images**:
```bash
# Build image from Dockerfile
docker build -t my-data-app:latest .
docker build -t my-data-app:v1.0 .

# Build with specific Dockerfile
docker build -f Dockerfile.prod -t my-data-app:prod .

# Build with build arguments
docker build --build-arg PYTHON_VERSION=3.9 -t my-app .
```

## 3. Docker Compose - Multi-Container Applications
**What it is**: Tool for defining and running multi-container Docker applications using YAML.

**Basic docker-compose.yml**:
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:13
    container_name: data-postgres
    environment:
      POSTGRES_DB: datawarehouse
      POSTGRES_USER: dataeng
      POSTGRES_PASSWORD: password123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    networks:
      - data-network

  # Redis for caching
  redis:
    image: redis:6-alpine
    container_name: data-redis
    ports:
      - "6379:6379"
    networks:
      - data-network

  # Data processing application
  data-app:
    build: .
    container_name: data-processor
    environment:
      DATABASE_URL: postgresql://dataeng:password123@postgres:5432/datawarehouse
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    networks:
      - data-network

volumes:
  postgres_data:

networks:
  data-network:
    driver: bridge
```

**Advanced Data Engineering Stack**:
```yaml
version: '3.8'

services:
  # Apache Airflow
  airflow-webserver:
    image: apache/airflow:2.5.0
    container_name: airflow-webserver
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
      AIRFLOW__CORE__FERNET_KEY: 'your-fernet-key-here'
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    depends_on:
      - postgres
    command: webserver

  airflow-scheduler:
    image: apache/airflow:2.5.0
    container_name: airflow-scheduler
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres:5432/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    depends_on:
      - postgres
    command: scheduler

  # Jupyter Notebook for data analysis
  jupyter:
    image: jupyter/datascience-notebook:latest
    container_name: data-jupyter
    ports:
      - "8888:8888"
    environment:
      JUPYTER_ENABLE_LAB: "yes"
    volumes:
      - ./notebooks:/home/jovyan/work
    networks:
      - data-network

  # MinIO for S3-compatible storage
  minio:
    image: minio/minio:latest
    container_name: data-minio
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123
    volumes:
      - minio_data:/data
    command: server /data --console-address ":9001"
    networks:
      - data-network

volumes:
  postgres_data:
  minio_data:

networks:
  data-network:
    driver: bridge
```

**Docker Compose Commands**:
```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d postgres

# View logs
docker-compose logs -f data-app

# Scale services
docker-compose up -d --scale data-app=3

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild services
docker-compose build
docker-compose up -d --build
```

## 4. Volumes and Data Persistence
**What they are**: Mechanisms to persist data beyond container lifecycle.

**Volume Types**:
```bash
# Named volumes (managed by Docker)
docker volume create data-volume
docker run -v data-volume:/app/data my-app

# Bind mounts (host directory)
docker run -v /host/path:/container/path my-app
docker run -v $(pwd)/data:/app/data my-app

# Anonymous volumes
docker run -v /app/data my-app
```

**Data Engineering Volume Examples**:
```yaml
services:
  spark-master:
    image: bitnami/spark:3.3.0
    volumes:
      # Bind mount for code
      - ./spark-jobs:/opt/spark-jobs
      # Bind mount for data
      - ./data:/opt/spark-data
      # Named volume for logs
      - spark-logs:/opt/spark/logs
    environment:
      - SPARK_MODE=master

  postgres:
    image: postgres:13
    volumes:
      # Named volume for database data
      - postgres-data:/var/lib/postgresql/data
      # Bind mount for initialization scripts
      - ./init-sql:/docker-entrypoint-initdb.d
    environment:
      POSTGRES_DB: warehouse

volumes:
  postgres-data:
  spark-logs:
```

**Volume Management**:
```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect postgres-data

# Remove unused volumes
docker volume prune

# Backup volume data
docker run --rm -v postgres-data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/postgres-backup.tar.gz -C /data .

# Restore volume data
docker run --rm -v postgres-data:/data -v $(pwd):/backup \
  ubuntu tar xzf /backup/postgres-backup.tar.gz -C /data
```

## 5. Networking
**What it is**: How containers communicate with each other and external systems.

**Network Types**:
```bash
# List networks
docker network ls

# Create custom network
docker network create data-network
docker network create --driver bridge data-bridge

# Run containers on custom network
docker run -d --name postgres --network data-network postgres:13
docker run -d --name app --network data-network my-data-app

# Connect existing container to network
docker network connect data-network existing-container
```

**Service Discovery**:
```yaml
# In docker-compose.yml, services can reach each other by service name
services:
  database:
    image: postgres:13
    # Accessible as 'database' from other containers
    
  app:
    image: my-app
    environment:
      # Use service name as hostname
      DB_HOST: database
      DB_PORT: 5432
```

**Port Mapping**:
```bash
# Map container port to host port
docker run -p 8080:80 nginx        # Host:Container
docker run -p 127.0.0.1:8080:80 nginx  # Bind to specific interface

# Multiple port mappings
docker run -p 8080:80 -p 8443:443 nginx

# Expose all ports randomly
docker run -P nginx
```

## 6. Environment Variables and Configuration
**What they are**: Ways to configure containers without rebuilding images.

**Setting Environment Variables**:
```bash
# Single environment variable
docker run -e DATABASE_URL=postgresql://localhost/db my-app

# Multiple environment variables
docker run \
  -e DATABASE_URL=postgresql://localhost/db \
  -e REDIS_URL=redis://localhost:6379 \
  -e DEBUG=true \
  my-app

# Environment file
docker run --env-file .env my-app
```

**Environment File (.env)**:
```bash
# .env file
DATABASE_URL=postgresql://user:pass@postgres:5432/db
REDIS_URL=redis://redis:6379
SPARK_MASTER_URL=spark://spark-master:7077
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
LOG_LEVEL=INFO
BATCH_SIZE=1000
```

**Docker Compose with Environment**:
```yaml
services:
  data-processor:
    build: .
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - LOG_LEVEL=${LOG_LEVEL:-INFO}
    env_file:
      - .env
      - .env.local  # Override with local settings
```

## 7. Multi-Stage Builds
**What they are**: Technique to create smaller, more secure production images.

**Multi-Stage Dockerfile**:
```dockerfile
# Build stage
FROM python:3.9 AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy and compile application
COPY . .
RUN python -m compileall .

# Production stage
FROM python:3.9-slim AS production

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Copy only necessary files from builder stage
COPY --from=builder /root/.local /home/app/.local
COPY --from=builder /app /home/app/app

# Set up environment
USER app
WORKDIR /home/app/app
ENV PATH=/home/app/.local/bin:$PATH

# Run application
CMD ["python", "main.py"]
```

**Data Engineering Multi-Stage Example**:
```dockerfile
# Build stage - compile and prepare
FROM openjdk:11-jdk AS builder

# Install Maven
RUN apt-get update && apt-get install -y maven

WORKDIR /build

# Copy POM and download dependencies (for better caching)
COPY pom.xml .
RUN mvn dependency:go-offline

# Copy source and build
COPY src ./src
RUN mvn clean package -DskipTests

# Runtime stage - minimal image
FROM openjdk:11-jre-slim AS runtime

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd --create-home --shell /bin/bash spark

# Copy built JAR from builder stage
COPY --from=builder /build/target/data-processor-*.jar /app/data-processor.jar

USER spark
WORKDIR /app

EXPOSE 8080

CMD ["java", "-jar", "data-processor.jar"]
```

## 8. Health Checks and Monitoring
**What they are**: Mechanisms to monitor container health and status.

**Dockerfile Health Check**:
```dockerfile
FROM python:3.9-slim

# Install application
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "app.py"]
```

**Docker Compose Health Checks**:
```yaml
services:
  web-app:
    build: .
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    
  database:
    image: postgres:13
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    
  data-processor:
    build: .
    depends_on:
      database:
        condition: service_healthy  # Wait for database to be healthy
```

**Monitoring Commands**:
```bash
# Check container health
docker ps  # Shows health status
docker inspect container-name | grep Health

# View container stats
docker stats
docker stats container-name

# Monitor logs
docker logs -f --tail 100 container-name

# System-wide information
docker system df  # Disk usage
docker system events  # Real-time events
```

## 9. Security Best Practices
**What they are**: Techniques to secure Docker containers and images.

**Secure Dockerfile Practices**:
```dockerfile
# Use specific version tags, not 'latest'
FROM python:3.9.16-slim

# Run as non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Install security updates
RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Copy files with appropriate ownership
COPY --chown=appuser:appgroup . /app

# Use COPY instead of ADD
COPY requirements.txt /app/

# Don't store secrets in image
# Use environment variables or secrets management instead

# Switch to non-root user
USER appuser

# Use specific WORKDIR
WORKDIR /app

# Minimize attack surface - only expose necessary ports
EXPOSE 8000

# Use exec form for CMD/ENTRYPOINT
CMD ["python", "app.py"]
```

**Runtime Security**:
```bash
# Run with read-only filesystem
docker run --read-only -v /tmp:/tmp my-app

# Limit resources
docker run --memory=512m --cpus=1.0 my-app

# Drop capabilities
docker run --cap-drop=ALL --cap-add=NET_BIND_SERVICE my-app

# Use security profiles
docker run --security-opt seccomp=default.json my-app

# Scan images for vulnerabilities
docker scan my-app:latest
```

## 10. Docker in CI/CD Pipelines
**What it is**: Using Docker for consistent build and deployment processes.

**GitHub Actions Example**:
```yaml
name: Build and Deploy Data Pipeline

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t data-pipeline:${{ github.sha }} .
        docker tag data-pipeline:${{ github.sha }} data-pipeline:latest
    
    - name: Run tests
      run: |
        docker run --rm data-pipeline:${{ github.sha }} python -m pytest
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push data-pipeline:${{ github.sha }}
        docker push data-pipeline:latest
```

**Production Deployment**:
```bash
# Pull latest image
docker pull my-registry/data-pipeline:latest

# Stop old container
docker stop data-pipeline || true
docker rm data-pipeline || true

# Start new container
docker run -d \
  --name data-pipeline \
  --restart unless-stopped \
  -v /data:/app/data \
  -v /logs:/app/logs \
  --env-file /etc/data-pipeline/.env \
  my-registry/data-pipeline:latest

# Verify deployment
docker logs data-pipeline
docker exec data-pipeline python -c "import app; print('Health check passed')"
```

**Docker Registry Operations**:
```bash
# Tag for registry
docker tag my-app:latest registry.company.com/my-app:v1.0

# Push to registry
docker push registry.company.com/my-app:v1.0

# Pull from registry
docker pull registry.company.com/my-app:v1.0

# Login to private registry
docker login registry.company.com
```