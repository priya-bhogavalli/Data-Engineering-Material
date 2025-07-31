# Docker Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is Docker and why is it used in data engineering?
**Answer**: Docker is a containerization platform that packages applications and their dependencies into lightweight, portable containers.

**Key Benefits for Data Engineering**:
- **Environment Consistency**: Same environment across dev, test, and production
- **Dependency Management**: Isolate different Python/Java versions and libraries
- **Scalability**: Easy horizontal scaling of data processing services
- **Deployment**: Simplified deployment of data pipelines and services

```dockerfile
# Example: Data processing container
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY config/ ./config/

# Set environment variables
ENV PYTHONPATH=/app
ENV DATA_PATH=/data

# Create data directory
RUN mkdir -p /data

# Run the application
CMD ["python", "src/main.py"]
```

### 2. Explain the difference between Docker Image and Container
**Answer**: 
- **Image**: Read-only template used to create containers (like a class)
- **Container**: Running instance of an image (like an object)

```bash
# Build image from Dockerfile
docker build -t my-data-app:v1.0 .

# List images
docker images

# Run container from image
docker run -d --name data-processor my-data-app:v1.0

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a
```

### 3. What is a Dockerfile and its key instructions?
**Answer**: Dockerfile is a text file containing instructions to build a Docker image.

```dockerfile
# Base image
FROM python:3.9-slim

# Metadata
LABEL maintainer="data-team@company.com"
LABEL version="1.0"

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Set environment variables
ENV ENVIRONMENT=production
ENV LOG_LEVEL=INFO

# Create non-root user
RUN useradd -m -u 1000 datauser
USER datauser

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["python", "app.py"]
```

**Key Instructions**:
- `FROM`: Base image
- `WORKDIR`: Set working directory
- `COPY/ADD`: Copy files from host to container
- `RUN`: Execute commands during build
- `CMD`: Default command when container starts
- `ENTRYPOINT`: Configure container as executable
- `ENV`: Set environment variables
- `EXPOSE`: Document port usage

### 4. How do you manage data persistence in Docker?
**Answer**: Use Docker volumes and bind mounts to persist data outside containers.

```bash
# Named volume
docker volume create data-volume
docker run -v data-volume:/data my-data-app

# Bind mount (host directory)
docker run -v /host/data:/container/data my-data-app

# Anonymous volume
docker run -v /data my-data-app

# List volumes
docker volume ls

# Inspect volume
docker volume inspect data-volume

# Remove unused volumes
docker volume prune
```

**Data Engineering Example**:
```bash
# Mount data directories for ETL pipeline
docker run -d \
  --name etl-pipeline \
  -v /data/input:/app/input:ro \
  -v /data/output:/app/output \
  -v /data/logs:/app/logs \
  etl-processor:latest
```

### 5. What is Docker Compose and when would you use it?
**Answer**: Docker Compose is a tool for defining and running multi-container applications using YAML files.

```yaml
# docker-compose.yml for data pipeline
version: '3.8'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_DB: datawarehouse
      POSTGRES_USER: datauser
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"

  data-processor:
    build: .
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://datauser:password@postgres:5432/datawarehouse
      REDIS_URL: redis://redis:6379
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs

  scheduler:
    image: apache/airflow:2.5.0
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql://datauser:password@postgres:5432/datawarehouse
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs

volumes:
  postgres_data:
```

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f data-processor

# Scale service
docker-compose up -d --scale data-processor=3

# Stop all services
docker-compose down

# Remove volumes
docker-compose down -v
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you optimize Docker images for data engineering workloads?
**Answer**: Use multi-stage builds, minimize layers, and optimize for caching.

```dockerfile
# Multi-stage build for Python data app
FROM python:3.9-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.9-slim

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application
WORKDIR /app
COPY src/ ./src/

# Non-root user
RUN useradd -m -u 1000 datauser
USER datauser

CMD ["python", "src/main.py"]
```

**Optimization Techniques**:
```dockerfile
# 1. Use specific tags, not 'latest'
FROM python:3.9.16-slim

# 2. Combine RUN commands to reduce layers
RUN apt-get update && \
    apt-get install -y curl wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 3. Use .dockerignore
# .dockerignore file:
# .git
# __pycache__
# *.pyc
# .pytest_cache
# .coverage

# 4. Order instructions by change frequency
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .  # This changes most frequently, so put it last
```

### 7. How do you handle secrets and configuration in Docker containers?
**Answer**: Use environment variables, Docker secrets, and external secret management systems.

```bash
# Environment variables
docker run -e DATABASE_PASSWORD=secret123 my-app

# Environment file
docker run --env-file .env my-app

# Docker secrets (Swarm mode)
echo "mysecretpassword" | docker secret create db_password -
docker service create --secret db_password my-app
```

**Secure Configuration Example**:
```dockerfile
# Use build args for non-sensitive config
ARG APP_VERSION=1.0
ENV APP_VERSION=$APP_VERSION

# Runtime secrets via environment
ENV DATABASE_PASSWORD_FILE=/run/secrets/db_password

# Application reads from file
COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

```bash
#!/bin/bash
# entrypoint.sh
if [ -f "$DATABASE_PASSWORD_FILE" ]; then
    export DATABASE_PASSWORD=$(cat "$DATABASE_PASSWORD_FILE")
fi

exec "$@"
```

**Docker Compose with Secrets**:
```yaml
version: '3.8'

services:
  app:
    build: .
    secrets:
      - db_password
    environment:
      DATABASE_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

### 8. How do you implement health checks and monitoring?
**Answer**: Use Docker health checks, logging, and monitoring tools.

```dockerfile
# Health check in Dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Alternative health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python /app/health_check.py || exit 1
```

```python
# health_check.py
import sys
import requests
import psycopg2

def check_database():
    try:
        conn = psycopg2.connect(
            host="postgres",
            database="datawarehouse",
            user="datauser",
            password="password"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return True
    except:
        return False

def check_api():
    try:
        response = requests.get("http://localhost:8080/api/status", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    if check_database() and check_api():
        sys.exit(0)
    else:
        sys.exit(1)
```

**Monitoring with Docker Compose**:
```yaml
version: '3.8'

services:
  app:
    build: .
    healthcheck:
      test: ["CMD", "python", "/app/health_check.py"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

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
```

### 9. How do you handle networking in Docker for data pipelines?
**Answer**: Use Docker networks to enable secure communication between containers.

```bash
# Create custom network
docker network create data-pipeline-network

# Run containers on custom network
docker run -d --name postgres --network data-pipeline-network postgres:13
docker run -d --name redis --network data-pipeline-network redis:6-alpine
docker run -d --name app --network data-pipeline-network my-data-app

# List networks
docker network ls

# Inspect network
docker network inspect data-pipeline-network
```

**Docker Compose Networking**:
```yaml
version: '3.8'

services:
  # Database tier
  postgres:
    image: postgres:13
    networks:
      - db-tier
    environment:
      POSTGRES_DB: datawarehouse

  # Application tier
  data-processor:
    build: .
    networks:
      - app-tier
      - db-tier
    depends_on:
      - postgres

  # Web tier
  api:
    build: ./api
    networks:
      - app-tier
      - web-tier
    ports:
      - "8080:8080"

  # Load balancer
  nginx:
    image: nginx:alpine
    networks:
      - web-tier
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf

networks:
  db-tier:
    driver: bridge
  app-tier:
    driver: bridge
  web-tier:
    driver: bridge
```

### 10. How do you debug Docker containers?
**Answer**: Use various debugging techniques and tools.

```bash
# Execute commands in running container
docker exec -it container_name bash
docker exec -it container_name python -c "import sys; print(sys.path)"

# View logs
docker logs container_name
docker logs -f --tail 100 container_name

# Inspect container
docker inspect container_name

# Check resource usage
docker stats container_name

# Copy files from container
docker cp container_name:/app/logs/error.log ./error.log

# Run container with debugging
docker run -it --rm my-app bash

# Override entrypoint for debugging
docker run -it --entrypoint bash my-app
```

**Debugging Dockerfile Build**:
```bash
# Build with no cache
docker build --no-cache -t my-app .

# Build specific stage in multi-stage
docker build --target builder -t my-app-debug .

# Run intermediate stage
docker run -it my-app-debug bash
```

**Debug Docker Compose**:
```bash
# Check configuration
docker-compose config

# View service logs
docker-compose logs service_name

# Execute in service container
docker-compose exec service_name bash

# Override command for debugging
docker-compose run --rm service_name bash
```

## Advanced Level Questions (5+ years experience)

### 11. How do you implement CI/CD pipelines with Docker?
**Answer**: Integrate Docker builds into CI/CD workflows with proper testing and deployment strategies.

```yaml
# .github/workflows/docker-ci.yml
name: Docker CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build test image
        run: |
          docker build -t data-app:test --target test .
      
      - name: Run tests
        run: |
          docker run --rm data-app:test pytest tests/
      
      - name: Run security scan
        run: |
          docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
            aquasec/trivy image data-app:test

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to registry
        uses: docker/login-action@v2
        with:
          registry: ${{ secrets.REGISTRY_URL }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}
      
      - name: Build and push
        uses: docker/build-push-action@v3
        with:
          context: .
          push: true
          tags: |
            ${{ secrets.REGISTRY_URL }}/data-app:latest
            ${{ secrets.REGISTRY_URL }}/data-app:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          # Deploy using docker-compose or Kubernetes
          echo "Deploying to staging environment"
```

**Multi-stage Dockerfile for CI/CD**:
```dockerfile
# Test stage
FROM python:3.9-slim as test
WORKDIR /app
COPY requirements-test.txt .
RUN pip install -r requirements-test.txt
COPY . .
RUN pytest tests/

# Build stage
FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Production stage
FROM python:3.9-slim as production
WORKDIR /app
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY src/ ./src/
USER 1000
CMD ["python", "src/main.py"]
```

### 12. How do you implement container orchestration for data pipelines?
**Answer**: Use Docker Swarm or Kubernetes for orchestrating containerized data pipelines.

**Docker Swarm Example**:
```yaml
# docker-stack.yml
version: '3.8'

services:
  data-processor:
    image: my-registry/data-processor:latest
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    networks:
      - data-network
    volumes:
      - data-volume:/data
    secrets:
      - db_password

  scheduler:
    image: my-registry/scheduler:latest
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager
    networks:
      - data-network

networks:
  data-network:
    driver: overlay
    attachable: true

volumes:
  data-volume:
    driver: local

secrets:
  db_password:
    external: true
```

```bash
# Deploy stack
docker stack deploy -c docker-stack.yml data-pipeline

# Scale service
docker service scale data-pipeline_data-processor=5

# Update service
docker service update --image my-registry/data-processor:v2 data-pipeline_data-processor
```

This comprehensive set covers Docker fundamentals through advanced orchestration concepts with practical data engineering examples.