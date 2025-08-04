# DevOps Automation Quick Reference

## Docker Commands

### Basic Operations
```bash
# Build image
docker build -t myapp:latest .
docker build -t myapp:v1.0 --build-arg ENV=prod .

# Run container
docker run -d --name myapp -p 8080:8080 myapp:latest
docker run -it --rm myapp:latest /bin/bash

# Container management
docker ps                    # List running containers
docker ps -a                 # List all containers
docker stop container_name   # Stop container
docker start container_name  # Start container
docker restart container_name # Restart container
docker rm container_name     # Remove container

# Image management
docker images               # List images
docker rmi image_name       # Remove image
docker pull image_name      # Pull image
docker push image_name      # Push image
docker tag source target    # Tag image
```

### Docker Compose
```bash
# Start services
docker-compose up -d
docker-compose up --build

# Stop services
docker-compose down
docker-compose down -v  # Remove volumes

# View logs
docker-compose logs
docker-compose logs service_name

# Scale services
docker-compose up -d --scale web=3

# Execute commands
docker-compose exec service_name bash
docker-compose run --rm service_name command
```

## Kubernetes Commands

### Cluster Management
```bash
# Cluster info
kubectl cluster-info
kubectl get nodes
kubectl describe node node_name

# Contexts
kubectl config get-contexts
kubectl config use-context context_name
kubectl config set-context --current --namespace=namespace_name
```

### Resource Management
```bash
# Deployments
kubectl create deployment app --image=nginx
kubectl get deployments
kubectl describe deployment app
kubectl scale deployment app --replicas=3
kubectl rollout status deployment/app
kubectl rollout history deployment/app
kubectl rollout undo deployment/app

# Pods
kubectl get pods
kubectl get pods -o wide
kubectl describe pod pod_name
kubectl logs pod_name
kubectl logs -f pod_name  # Follow logs
kubectl exec -it pod_name -- /bin/bash

# Services
kubectl get services
kubectl expose deployment app --port=80 --type=LoadBalancer
kubectl port-forward service/app 8080:80

# ConfigMaps and Secrets
kubectl create configmap app-config --from-file=config.yaml
kubectl create secret generic app-secret --from-literal=password=secret
kubectl get configmaps
kubectl get secrets
```

### YAML Operations
```bash
# Apply configurations
kubectl apply -f deployment.yaml
kubectl apply -f .  # Apply all YAML files in directory
kubectl apply -k .  # Apply Kustomize

# Delete resources
kubectl delete -f deployment.yaml
kubectl delete deployment app
kubectl delete pod pod_name --force --grace-period=0
```

## Terraform Commands

### Basic Operations
```bash
# Initialize
terraform init
terraform init -upgrade

# Plan and apply
terraform plan
terraform plan -var-file="prod.tfvars"
terraform apply
terraform apply -auto-approve
terraform apply -target=resource.name

# Destroy
terraform destroy
terraform destroy -target=resource.name

# State management
terraform state list
terraform state show resource.name
terraform state mv old_name new_name
terraform state rm resource.name
```

### Workspace Management
```bash
# Workspaces
terraform workspace list
terraform workspace new dev
terraform workspace select dev
terraform workspace delete dev
```

### Import and Output
```bash
# Import existing resources
terraform import aws_instance.example i-1234567890abcdef0

# Outputs
terraform output
terraform output -json
terraform output variable_name
```

## Ansible Commands

### Basic Operations
```bash
# Run playbook
ansible-playbook playbook.yml
ansible-playbook -i inventory playbook.yml
ansible-playbook playbook.yml --limit webservers
ansible-playbook playbook.yml --tags "install,configure"

# Ad-hoc commands
ansible all -m ping
ansible webservers -m shell -a "uptime"
ansible all -m copy -a "src=/etc/hosts dest=/tmp/hosts"
ansible all -m yum -a "name=httpd state=present" --become

# Inventory
ansible-inventory --list
ansible-inventory --host hostname
```

### Vault Operations
```bash
# Encrypt/decrypt
ansible-vault encrypt secrets.yml
ansible-vault decrypt secrets.yml
ansible-vault edit secrets.yml
ansible-vault view secrets.yml

# Run with vault
ansible-playbook playbook.yml --ask-vault-pass
ansible-playbook playbook.yml --vault-password-file vault_pass.txt
```

## CI/CD Pipeline Patterns

### GitHub Actions
```yaml
# Basic workflow
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Run tests
      run: |
        npm install
        npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy
      run: echo "Deploying..."
```

### GitLab CI
```yaml
# .gitlab-ci.yml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  script:
    - npm install
    - npm test

build:
  stage: build
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy:
  stage: deploy
  script:
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
```

## Monitoring Commands

### Prometheus Queries
```promql
# CPU usage
rate(cpu_usage_seconds_total[5m])

# Memory usage
(container_memory_usage_bytes / container_spec_memory_limit_bytes) * 100

# HTTP request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# 95th percentile response time
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Grafana Dashboard Queries
```json
{
  "targets": [
    {
      "expr": "rate(data_pipeline_executions_total[5m])",
      "legendFormat": "{{pipeline_name}}"
    }
  ],
  "title": "Pipeline Execution Rate"
}
```

## Security Commands

### Container Security
```bash
# Scan image for vulnerabilities
trivy image nginx:latest
docker scan nginx:latest

# Run security benchmark
docker-bench-security

# Check container runtime security
falco
```

### Kubernetes Security
```bash
# Security scanning
kube-bench  # CIS Kubernetes Benchmark
kube-hunter # Penetration testing

# RBAC
kubectl auth can-i create pods --as=user
kubectl auth can-i "*" "*" --as=system:serviceaccount:default:my-sa

# Network policies
kubectl get networkpolicies
kubectl describe networkpolicy policy-name
```

## Troubleshooting Commands

### Docker Troubleshooting
```bash
# Container inspection
docker inspect container_name
docker stats container_name
docker top container_name

# Debugging
docker exec -it container_name /bin/bash
docker logs --tail 50 container_name
docker events --filter container=container_name

# System info
docker system info
docker system df
docker system prune  # Clean up
```

### Kubernetes Troubleshooting
```bash
# Pod debugging
kubectl describe pod pod_name
kubectl logs pod_name --previous
kubectl get events --sort-by=.metadata.creationTimestamp

# Resource usage
kubectl top nodes
kubectl top pods
kubectl top pods --containers

# Network debugging
kubectl exec -it pod_name -- nslookup service_name
kubectl exec -it pod_name -- wget -qO- http://service_name

# Debug utilities
kubectl run debug --image=busybox -it --rm -- /bin/sh
kubectl debug pod_name -it --image=ubuntu
```

## Configuration Files

### Docker Compose Example
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - db_data:/var/lib/postgresql/data
volumes:
  db_data:
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Terraform Resource
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1d0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
    Environment = var.environment
  }
}

output "instance_ip" {
  value = aws_instance.web.public_ip
}
```

## Environment Variables

### Common Environment Variables
```bash
# Docker
export DOCKER_HOST=tcp://localhost:2376
export DOCKER_TLS_VERIFY=1

# Kubernetes
export KUBECONFIG=~/.kube/config
export KUBE_NAMESPACE=default

# Terraform
export TF_VAR_region=us-west-2
export TF_LOG=DEBUG

# AWS
export AWS_PROFILE=default
export AWS_REGION=us-west-2

# Ansible
export ANSIBLE_HOST_KEY_CHECKING=False
export ANSIBLE_INVENTORY=inventory.ini
```

This quick reference provides essential commands and patterns for daily DevOps automation tasks in data engineering environments.