# Comprehensive Apache Airflow Installation Guide

Complete installation guide for Apache Airflow 3.0.2 covering all major installation methods.

## Table of Contents
1. [Windows Installation (WSL)](#windows-installation-wsl)
2. [Pip Installation (Recommended)](#pip-installation-recommended)
3. [Docker Installation](#docker-installation)
4. [Kubernetes Installation (Helm)](#kubernetes-installation-helm)
5. [Conda Installation](#conda-installation)
6. [Native Linux Installation](#native-linux-installation)
7. [macOS Installation](#macos-installation)
8. [Cloud Installations](#cloud-installations)
9. [Development Setup](#development-setup)
10. [Post-Installation Setup](#post-installation-setup)
11. [Troubleshooting](#troubleshooting)

---

## Windows Installation (WSL)

This guide walks you through installing Apache Airflow 3.0.2 on a Windows machine using WSL (Windows Subsystem for Linux).

### Step 1: Install WSL
Open PowerShell as Administrator and run:
```powershell
wsl --install
```

### Step 2: Set Up Python Environment
Once WSL is installed and Ubuntu is running:
```bash
sudo apt update && sudo apt install python3.12 python3.12-venv python3-pip -y
```

Create and activate a virtual environment:
```bash
python3.12 -m venv airflow_venv
source airflow_venv/bin/activate
```

### Step 3: Install Apache Airflow
Install Airflow with version-specific constraints:
```bash
pip install "apache-airflow==3.0.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.12.txt"
```

Upgrade essential packages:
```bash
pip install --upgrade pip setuptools wheel
```

### Step 4: Start Airflow Standalone
Run the following command to initialize Airflow:
```bash
airflow standalone
```

### Step 5: Access the Airflow UI
Once started, open your browser and go to:
```
http://localhost:8080
```

### Step 6: Open Airflow in VS Code (Optional)
To open your Airflow project in VS Code using WSL:
1. Install the 'Remote - WSL' extension in VS Code
2. Open VS Code and select 'WSL: Ubuntu' from the Command Palette
3. Navigate to your Airflow project folder

---

## Pip Installation (Recommended)

### Quick Start (Any Platform)
```bash
# Create virtual environment
python3 -m venv airflow_venv
source airflow_venv/bin/activate  # Linux/macOS
# airflow_venv\Scripts\activate  # Windows

# Set Airflow home
export AIRFLOW_HOME=~/airflow

# Install Airflow
pip install "apache-airflow==3.0.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.12.txt"

# Initialize and start
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
airflow standalone
```

### With Specific Providers
```bash
# Install with common providers
pip install "apache-airflow[postgres,redis,celery,crypto,ssh]==3.0.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.12.txt"

# Install additional providers
pip install apache-airflow-providers-amazon
pip install apache-airflow-providers-google
pip install apache-airflow-providers-microsoft-azure
```

---

## Docker Installation

### Method 1: Official Docker Compose
```bash
# Download official compose file
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.2/docker-compose.yaml'

# Create directories
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialize and start
docker compose up airflow-init
docker compose up -d
```

### Method 2: Custom Dockerfile
```dockerfile
FROM apache/airflow:3.0.2
USER root
RUN apt-get update && apt-get install -y git
USER airflow
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
```

### Method 3: Single Container (Development)
```bash
docker run -d \
  --name airflow \
  -p 8080:8080 \
  -v $(pwd)/dags:/opt/airflow/dags \
  apache/airflow:3.0.2 \
  standalone
```

---

## Kubernetes Installation (Helm)

### Prerequisites
- Kubernetes cluster (1.23+)
- Helm 3.6+
- kubectl configured

### Step 1: Add Airflow Helm Repository
```bash
helm repo add apache-airflow https://airflow.apache.org
helm repo update
```

### Step 2: Create Namespace
```bash
kubectl create namespace airflow
```

### Step 3: Install Airflow
```bash
# Basic installation
helm install airflow apache-airflow/airflow --namespace airflow

# With custom values
helm install airflow apache-airflow/airflow \
  --namespace airflow \
  --set webserver.service.type=LoadBalancer \
  --set postgresql.enabled=true \
  --set redis.enabled=true
```

### Step 4: Access Airflow
```bash
# Get webserver URL
kubectl get svc -n airflow

# Port forward (if using ClusterIP)
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
```

### Custom Values File (values.yaml)
```yaml
webserver:
  service:
    type: LoadBalancer
  replicas: 2

scheduler:
  replicas: 2

workers:
  replicas: 3

postgresql:
  enabled: true
  auth:
    postgresPassword: "airflow"

redis:
  enabled: true

executor: "CeleryExecutor"

dags:
  gitSync:
    enabled: true
    repo: https://github.com/your-org/airflow-dags
    branch: main
```

---

## Docker Installation

### Method 1: Official Docker Compose
```bash
# Download official compose file
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.2/docker-compose.yaml'

# Create directories
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialize and start
docker compose up airflow-init
docker compose up -d
```

### Method 2: Custom Dockerfile
```dockerfile
FROM apache/airflow:3.0.2
USER root
RUN apt-get update && apt-get install -y git
USER airflow
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
```

### Method 3: Single Container (Development)
```bash
docker run -d \
  --name airflow \
  -p 8080:8080 \
  -v $(pwd)/dags:/opt/airflow/dags \
  apache/airflow:3.0.2 \
  standalone
```

---

## Conda Installation

### Method 1: Using conda-forge
```bash
# Create conda environment
conda create -n airflow python=3.12
conda activate airflow

# Install from conda-forge
conda install -c conda-forge apache-airflow

# Or install specific version
conda install -c conda-forge apache-airflow=3.0.2
```

### Method 2: Mixed conda/pip
```bash
# Create environment with dependencies
conda create -n airflow python=3.12 postgresql redis
conda activate airflow

# Install Airflow with pip
pip install "apache-airflow==3.0.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.12.txt"
```



---

## Native Linux Installation

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip \
    build-essential libssl-dev libffi-dev python3-dev \
    postgresql postgresql-contrib redis-server -y

python3.12 -m venv airflow_venv
source airflow_venv/bin/activate
export AIRFLOW_HOME=~/airflow

pip install "apache-airflow==3.0.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.12.txt"
```

### CentOS/RHEL
```bash
sudo dnf install python3.12 python3-pip gcc openssl-devel \
    libffi-devel python3-devel postgresql postgresql-server \
    redis -y

python3.12 -m venv airflow_venv
source airflow_venv/bin/activate
export AIRFLOW_HOME=~/airflow

pip install "apache-airflow==3.0.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.12.txt"
```

---

## macOS Installation

### Using Homebrew
```bash
brew install python@3.12 postgresql redis
python3.12 -m venv airflow_venv
source airflow_venv/bin/activate
export AIRFLOW_HOME=~/airflow

pip install "apache-airflow==3.0.2" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.0.2/constraints-3.12.txt"

brew services start postgresql
brew services start redis
airflow standalone
```

---

## Cloud Installations

### AWS (Amazon MWAA)
```bash
# Install AWS CLI
pip install awscli

# Create MWAA environment
aws mwaa create-environment \
  --name my-airflow-env \
  --airflow-version 2.8.1 \
  --source-bucket-arn arn:aws:s3:::my-airflow-bucket \
  --dag-s3-path dags/ \
  --execution-role-arn arn:aws:iam::123456789012:role/AirflowExecutionRole
```

### Google Cloud Composer
```bash
# Install gcloud CLI
curl https://sdk.cloud.google.com | bash

# Create Composer environment
gcloud composer environments create my-airflow-env \
  --location us-central1 \
  --python-version 3 \
  --airflow-version 2.8.1
```

### Azure Data Factory
```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Create managed Airflow
az datafactory create \
  --resource-group myResourceGroup \
  --factory-name myDataFactory \
  --location "East US"
```

---

## Development Setup

### VS Code Integration
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./airflow_venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "airflow.dags.path": "./dags",
  "airflow.connections.path": "./connections"
}
```

### Testing Setup
```bash
# Install testing dependencies
pip install pytest pytest-airflow pytest-cov

# Create test structure
mkdir -p tests/dags tests/operators
touch tests/__init__.py tests/conftest.py

# Sample conftest.py
cat > tests/conftest.py << EOF
import pytest
from airflow.models import DagBag

@pytest.fixture
def dagbag():
    return DagBag(dag_folder="dags/", include_examples=False)
EOF
```

---

## Post-Installation Setup

### Environment Variables
```bash
# Add to ~/.bashrc or ~/.zshrc
export AIRFLOW_HOME=~/airflow
export PATH=$PATH:~/airflow_venv/bin
```

### Configuration
```ini
# Edit $AIRFLOW_HOME/airflow.cfg
[core]
dags_are_paused_at_creation = False
load_examples = False
max_active_runs_per_dag = 1

[webserver]
expose_config = True
web_server_port = 8080

[scheduler]
catchup_by_default = False
```

### Additional Providers
```bash
pip install apache-airflow-providers-postgres
pip install apache-airflow-providers-http
pip install apache-airflow-providers-email
pip install apache-airflow-providers-slack
```

---

## Troubleshooting

### Common Issues

**Import Errors**
```bash
airflow dags list-import-errors
```

**Port Conflicts**
```bash
lsof -i :8080
kill -9 <PID>
```

**Database Issues**
```bash
airflow db reset
airflow db upgrade
```

**Permission Issues**
```bash
sudo chown -R $USER:$USER $AIRFLOW_HOME
chmod -R 755 $AIRFLOW_HOME
```

### Useful Commands
```bash
# Check version
airflow version

# List DAGs
airflow dags list

# Test task
airflow tasks test <dag_id> <task_id> <execution_date>

# Trigger DAG
airflow dags trigger <dag_id>

# Check configuration
airflow config list
```

### Performance Tuning

**Development**
```ini
[core]
parallelism = 4
max_active_runs_per_dag = 1
max_active_tasks_per_dag = 2

[celery]
worker_concurrency = 2
```

**Production**
```ini
[core]
parallelism = 32
max_active_runs_per_dag = 16
max_active_tasks_per_dag = 16

[celery]
worker_concurrency = 16
```

---

## Quick Reference

### Start Commands
```bash
# Standalone (development)
airflow standalone

# Separate processes (production)
airflow webserver --port 8080 &
airflow scheduler &

# With Celery
airflow celery worker &
airflow celery flower &
```

### Stop Commands
```bash
pkill -f "airflow webserver"
pkill -f "airflow scheduler"
pkill -f "airflow celery"
```

### Access Points
- **Web UI**: http://localhost:8080 (admin/admin)
- **Flower**: http://localhost:5555 (if Celery enabled)
- **API**: http://localhost:8080/api/v1/

---

**Installation Complete!** 🎉

Choose the installation method that best fits your environment and requirements.