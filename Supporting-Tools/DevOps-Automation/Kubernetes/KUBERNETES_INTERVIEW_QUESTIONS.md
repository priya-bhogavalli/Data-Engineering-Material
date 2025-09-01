# Kubernetes Interview Questions for Data Engineering

## 📋 Quick Navigation

### 🎯 **By Difficulty Level**
- **🟢 Fundamentals**: [K8s Basics](#fundamentals) | [Pods & Services](#pods-services) | [Configuration](#configuration)
- **🟡 Intermediate**: [Storage & Scaling](#intermediate) | [Jobs & Workloads](#jobs-workloads) | [Networking](#networking)
- **🔴 Advanced**: [Security & RBAC](#advanced) | [Monitoring](#monitoring) | [Production](#production)

### 📚 **By Topic Category**
- **Core Concepts**: [Architecture](#architecture) | [Workloads](#workloads) | [Networking](#networking)
- **Data Management**: [Storage](#storage) | [ConfigMaps & Secrets](#configuration) | [Persistence](#persistence)
- **Operations**: [Scaling](#scaling) | [Monitoring](#monitoring) | [Security](#security)

---

## 🎯 Essential Kubernetes Concepts for Data Engineering

### 🔑 **Must-Know for Data Engineering Interviews**
- **Container Orchestration**: Automated deployment, scaling, and management of containerized applications
- **Resource Management**: Efficient allocation and utilization of CPU, memory, and storage resources
- **Service Discovery**: Automatic discovery and communication between microservices
- **Auto-scaling**: Horizontal and vertical scaling based on metrics and demand
- **High Availability**: Self-healing, fault tolerance, and zero-downtime deployments
- **Data Persistence**: Persistent volumes and stateful workloads for databases and data processing

### 📊 **Interview Success Metrics**
- **Architecture Understanding**: 90%+ accuracy on K8s components and their interactions
- **Practical Skills**: Ability to write YAML manifests and troubleshoot deployments
- **Production Awareness**: Understanding of security, monitoring, and scaling strategies
- **Data Engineering Focus**: Knowledge of stateful workloads and data pipeline orchestration

---

## 🟢 Fundamentals

### 1. What is Kubernetes and why is it used in data engineering?

**Answer:**
Kubernetes (K8s) is an open-source container orchestration platform that automates the deployment, scaling, and management of containerized applications. Originally developed by Google, it has become the de facto standard for container orchestration in production environments.

**Core Kubernetes Concepts:**
- **Orchestration**: Automated management of containerized applications across clusters
- **Declarative Configuration**: Describe desired state, K8s maintains it automatically
- **Self-Healing**: Automatically replaces failed containers and reschedules workloads
- **Service Discovery**: Built-in DNS and service mesh capabilities
- **Load Balancing**: Automatic traffic distribution across healthy pods

**Why Kubernetes is Critical for Data Engineering:**

**1. Scalable Data Processing**
- **Auto-scaling**: Automatically scale data processing workloads based on queue length, CPU, or custom metrics
- **Resource Efficiency**: Optimal resource utilization across cluster nodes
- **Batch Processing**: Efficient handling of large-scale batch jobs with parallel execution
- **Stream Processing**: Deploy and scale real-time data processing applications

**2. High Availability and Fault Tolerance**
- **Self-Healing**: Automatically restart failed data processing pods
- **Multi-Zone Deployment**: Distribute workloads across availability zones
- **Rolling Updates**: Zero-downtime deployments of data pipeline updates
- **Backup and Recovery**: Automated backup strategies for stateful data services

**3. Microservices Architecture for Data Pipelines**
- **Service Decomposition**: Break monolithic ETL processes into manageable microservices
- **Independent Scaling**: Scale different pipeline components based on their specific needs
- **Technology Diversity**: Run different data tools (Spark, Kafka, Airflow) in the same cluster
- **Fault Isolation**: Failures in one service don't affect the entire pipeline

**4. Resource Management and Cost Optimization**
- **Resource Quotas**: Prevent resource contention between different data teams
- **Node Affinity**: Schedule data-intensive workloads on appropriate hardware
- **Spot Instance Integration**: Use cheaper compute resources for fault-tolerant batch jobs
- **Multi-Tenancy**: Share cluster resources across multiple data engineering teams

**Real-World Data Engineering Use Cases:**
- **ETL Pipeline Orchestration**: Deploy and manage complex data transformation workflows
- **Real-Time Analytics**: Scale streaming data processing applications (Kafka, Flink, Storm)
- **Machine Learning Workflows**: Orchestrate model training, validation, and serving pipelines
- **Data Lake Management**: Deploy and scale data ingestion and processing services
- **Database Operations**: Manage stateful databases with persistent storage and backups

```yaml
# Example: Scalable data processing deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processor
  labels:
    app: data-processor
    tier: processing
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-processor
  template:
    metadata:
      labels:
        app: data-processor
    spec:
      containers:
      - name: processor
        image: my-registry/data-processor:v1.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: BATCH_SIZE
          valueFrom:
            configMapKeyRef:
              name: processing-config
              key: batch.size
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
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
```

### 2. Explain the main Kubernetes components and architecture

**Answer:**
Kubernetes follows a master-worker architecture with distinct control plane and data plane components that work together to manage the cluster.

**Control Plane Components (Master Nodes):**

**1. API Server (kube-apiserver)**
- **Function**: Central management component that exposes the Kubernetes API
- **Responsibilities**: Authentication, authorization, admission control, and API validation
- **Data Engineering Impact**: All kubectl commands and CI/CD pipelines interact through the API server
- **Scalability**: Can be horizontally scaled for high-availability clusters

**2. etcd**
- **Function**: Distributed key-value store that serves as Kubernetes' backing store
- **Responsibilities**: Stores all cluster data, configuration, and state information
- **Data Engineering Impact**: Critical for maintaining state of data processing jobs and configurations
- **Backup Strategy**: Regular etcd backups are essential for disaster recovery

**3. Scheduler (kube-scheduler)**
- **Function**: Assigns pods to nodes based on resource requirements and constraints
- **Responsibilities**: Resource allocation, node affinity, anti-affinity rules
- **Data Engineering Impact**: Ensures data-intensive workloads are scheduled on appropriate nodes
- **Custom Scheduling**: Can be extended with custom schedulers for specialized workloads

**4. Controller Manager (kube-controller-manager)**
- **Function**: Runs controller processes that regulate the state of the cluster
- **Key Controllers**: Deployment, ReplicaSet, Job, CronJob, Service controllers
- **Data Engineering Impact**: Manages lifecycle of data processing jobs and services
- **Custom Controllers**: Can implement custom controllers for data pipeline management

**Node Components (Worker Nodes):**

**1. kubelet**
- **Function**: Primary node agent that communicates with the control plane
- **Responsibilities**: Pod lifecycle management, container health monitoring, resource reporting
- **Data Engineering Impact**: Manages data processing containers and their resource usage
- **Monitoring**: Provides metrics about node and pod resource consumption

**2. kube-proxy**
- **Function**: Network proxy that maintains network rules for service communication
- **Responsibilities**: Load balancing, service discovery, network routing
- **Data Engineering Impact**: Enables communication between data pipeline components
- **Network Modes**: iptables, IPVS, or userspace proxy modes

**3. Container Runtime**
- **Function**: Software responsible for running containers
- **Options**: Docker, containerd, CRI-O, or other CRI-compatible runtimes
- **Data Engineering Impact**: Executes data processing containers with proper isolation
- **Performance**: Choice of runtime can impact data processing performance

**Architecture Flow:**
```
┌─────────────────────────────────────────────────────────────┐
│                    Control Plane                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────┐ │
│  │ API Server  │ │   Scheduler │ │ Controller  │ │  etcd  │ │
│  │             │ │             │ │   Manager   │ │        │ │
│  └─────────────┘ └─────────────┘ └─────────────┘ └────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ API Calls
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Worker Nodes                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │   kubelet   │ │ kube-proxy  │ │   Container Runtime     │ │
│  │             │ │             │ │                         │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                    Pods                                 │ │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │ │
│  │  │ Data Proc 1 │ │ Data Proc 2 │ │     Database        │ │ │
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘ │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

```bash
# Check cluster components health
kubectl get componentstatuses

# View cluster information
kubectl cluster-info

# Get detailed node information
kubectl get nodes -o wide

# Describe specific node
kubectl describe node <node-name>

# Check control plane pods
kubectl get pods -n kube-system
```

### 3. What are Pods and how do they work in data engineering contexts?

**Answer:**
A Pod is the smallest deployable unit in Kubernetes, representing one or more tightly coupled containers that share storage, network, and lifecycle. Understanding Pods is crucial for designing effective data processing architectures.

**Pod Characteristics:**
- **Shared Network**: All containers in a pod share the same IP address and port space
- **Shared Storage**: Containers can share volumes for data exchange
- **Atomic Unit**: Pods are created, scheduled, and destroyed as a single unit
- **Ephemeral**: Pods are mortal and can be replaced at any time
- **Single Node**: All containers in a pod run on the same node

**Data Engineering Pod Patterns:**

**1. Single Container Pod (Most Common)**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-processor
  labels:
    app: data-processor
    component: etl
spec:
  containers:
  - name: processor
    image: my-registry/spark-processor:v2.0
    env:
    - name: SPARK_MASTER_URL
      value: "spark://spark-master:7077"
    - name: INPUT_PATH
      value: "/data/input"
    - name: OUTPUT_PATH
      value: "/data/output"
    resources:
      requests:
        memory: "4Gi"
        cpu: "2"
      limits:
        memory: "8Gi"
        cpu: "4"
    volumeMounts:
    - name: data-volume
      mountPath: /data
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: processing-data-pvc
  restartPolicy: OnFailure
```

**2. Multi-Container Pod (Sidecar Pattern)**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-processor-with-monitoring
spec:
  containers:
  # Main application container
  - name: data-processor
    image: my-registry/data-processor:v1.0
    ports:
    - containerPort: 8080
    volumeMounts:
    - name: shared-logs
      mountPath: /app/logs
    - name: shared-data
      mountPath: /app/data
  
  # Sidecar: Log shipping container
  - name: log-shipper
    image: fluent/fluent-bit:latest
    volumeMounts:
    - name: shared-logs
      mountPath: /logs
      readOnly: true
    - name: fluent-config
      mountPath: /fluent-bit/etc
  
  # Sidecar: Metrics exporter
  - name: metrics-exporter
    image: prom/node-exporter:latest
    ports:
    - containerPort: 9100
    volumeMounts:
    - name: shared-data
      mountPath: /data
      readOnly: true
  
  volumes:
  - name: shared-logs
    emptyDir: {}
  - name: shared-data
    emptyDir: {}
  - name: fluent-config
    configMap:
      name: fluent-config
```

**3. Init Container Pattern**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-processor-with-init
spec:
  # Init containers run before main containers
  initContainers:
  - name: data-validator
    image: my-registry/data-validator:v1.0
    command: ['sh', '-c']
    args:
    - |
      echo "Validating input data..."
      python /app/validate_data.py --input-path /data/input
      echo "Data validation completed"
    volumeMounts:
    - name: input-data
      mountPath: /data/input
  
  - name: schema-migrator
    image: my-registry/schema-migrator:v1.0
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: url
    command: ['python', '/app/migrate_schema.py']
  
  # Main container starts after all init containers complete
  containers:
  - name: data-processor
    image: my-registry/data-processor:v1.0
    volumeMounts:
    - name: input-data
      mountPath: /data/input
    - name: output-data
      mountPath: /data/output
  
  volumes:
  - name: input-data
    persistentVolumeClaim:
      claimName: input-data-pvc
  - name: output-data
    persistentVolumeClaim:
      claimName: output-data-pvc
```

**Pod Lifecycle and States:**
- **Pending**: Pod accepted but containers not yet created
- **Running**: At least one container is running
- **Succeeded**: All containers terminated successfully
- **Failed**: At least one container failed
- **Unknown**: Pod state cannot be determined

**Data Engineering Best Practices:**
- **Resource Limits**: Always set resource requests and limits for predictable scheduling
- **Health Checks**: Implement liveness and readiness probes for reliable operations
- **Data Persistence**: Use persistent volumes for data that must survive pod restarts
- **Security Context**: Run containers as non-root users when possible
- **Graceful Shutdown**: Handle SIGTERM signals for clean data processing shutdown

```bash
# Pod management commands
kubectl apply -f pod.yaml
kubectl get pods -o wide
kubectl describe pod data-processor
kubectl logs data-processor -c processor
kubectl exec -it data-processor -c processor -- bash
kubectl delete pod data-processor

# Debug pod issues
kubectl get events --sort-by=.metadata.creationTimestamp
kubectl logs data-processor --previous  # Previous container logs
kubectl port-forward pod/data-processor 8080:8080  # Local access
```

---

## 🟡 Intermediate

### 4. How do you manage persistent storage for data engineering workloads?

**Answer:**
Persistent storage in Kubernetes is managed through Persistent Volumes (PV), Persistent Volume Claims (PVC), and Storage Classes, enabling data to survive pod restarts and rescheduling.

**Storage Architecture Components:**

**1. Storage Classes**
- **Purpose**: Define different types of storage with specific characteristics
- **Dynamic Provisioning**: Automatically create PVs when PVCs are requested
- **Parameters**: Configure storage type, performance, replication, etc.

**2. Persistent Volumes (PV)**
- **Purpose**: Cluster-wide storage resources provisioned by administrators
- **Lifecycle**: Independent of pod lifecycle
- **Access Modes**: ReadWriteOnce, ReadOnlyMany, ReadWriteMany

**3. Persistent Volume Claims (PVC)**
- **Purpose**: User requests for storage resources
- **Binding**: Automatically bound to suitable PVs
- **Namespace Scoped**: PVCs exist within specific namespaces

```yaml
# High-performance storage class for data processing
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd-data
  annotations:
    storageclass.kubernetes.io/is-default-class: "false"
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "16000"
  throughput: "1000"
  encrypted: "true"
allowVolumeExpansion: true
reclaimPolicy: Delete
volumeBindingMode: WaitForFirstConsumer

---
# Standard storage for logs and temporary data
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard-storage
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp2
  encrypted: "true"
allowVolumeExpansion: true
reclaimPolicy: Retain
volumeBindingMode: Immediate

---
# Shared storage for multi-pod access
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: shared-nfs
provisioner: example.com/nfs
parameters:
  server: nfs-server.example.com
  path: /shared/data
  readOnly: "false"
reclaimPolicy: Retain
volumeBindingMode: Immediate
```

**Data Engineering Storage Patterns:**

**1. Database Storage with StatefulSets**
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgresql-cluster
spec:
  serviceName: postgresql-service
  replicas: 3
  selector:
    matchLabels:
      app: postgresql
  template:
    metadata:
      labels:
        app: postgresql
    spec:
      containers:
      - name: postgresql
        image: postgres:13
        env:
        - name: POSTGRES_DB
          value: datawarehouse
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        - name: postgres-config
          mountPath: /etc/postgresql/postgresql.conf
          subPath: postgresql.conf
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
      volumes:
      - name: postgres-config
        configMap:
          name: postgres-config
  # Dynamic volume provisioning
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd-data
      resources:
        requests:
          storage: 100Gi
```

**2. Shared Data Processing Storage**
```yaml
# Shared PVC for input data
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-input-data
spec:
  accessModes:
    - ReadOnlyMany
  storageClassName: shared-nfs
  resources:
    requests:
      storage: 1Ti

---
# Individual PVC for each processing pod
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: processing-workspace-template
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd-data
  resources:
    requests:
      storage: 50Gi

---
# Deployment using shared and individual storage
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processors
spec:
  replicas: 5
  selector:
    matchLabels:
      app: data-processor
  template:
    metadata:
      labels:
        app: data-processor
    spec:
      containers:
      - name: processor
        image: my-registry/data-processor:v1.0
        volumeMounts:
        # Shared read-only input data
        - name: input-data
          mountPath: /data/input
          readOnly: true
        # Individual workspace for processing
        - name: workspace
          mountPath: /workspace
        # Shared output location
        - name: output-data
          mountPath: /data/output
        # Temporary high-speed storage
        - name: temp-storage
          mountPath: /tmp/processing
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        resources:
          requests:
            memory: "8Gi"
            cpu: "4"
          limits:
            memory: "16Gi"
            cpu: "8"
      volumes:
      - name: input-data
        persistentVolumeClaim:
          claimName: shared-input-data
      - name: workspace
        persistentVolumeClaim:
          claimName: processing-workspace-template
      - name: output-data
        persistentVolumeClaim:
          claimName: shared-output-data
      - name: temp-storage
        emptyDir:
          sizeLimit: 20Gi
          medium: Memory  # Use RAM for temporary storage
```

**3. Backup and Disaster Recovery**
```yaml
# Backup CronJob for database
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:13
            command:
            - /bin/bash
            - -c
            - |
              BACKUP_FILE="/backup/postgres-$(date +%Y%m%d-%H%M%S).sql"
              pg_dump -h postgresql-service -U $POSTGRES_USER -d datawarehouse > $BACKUP_FILE
              echo "Backup completed: $BACKUP_FILE"
              # Upload to cloud storage
              aws s3 cp $BACKUP_FILE s3://data-backups/postgres/
            env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: username
            - name: PGPASSWORD
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: password
            volumeMounts:
            - name: backup-storage
              mountPath: /backup
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-storage-pvc
          restartPolicy: OnFailure
```

**Storage Management Commands:**
```bash
# Storage class operations
kubectl get storageclass
kubectl describe storageclass fast-ssd-data

# PVC operations
kubectl get pvc
kubectl describe pvc postgres-storage-postgresql-cluster-0
kubectl get pv

# Volume expansion (if supported)
kubectl patch pvc postgres-storage-postgresql-cluster-0 -p '{"spec":{"resources":{"requests":{"storage":"200Gi"}}}}'

# Check volume usage
kubectl exec -it postgresql-cluster-0 -- df -h /var/lib/postgresql/data
```

### 5. How do you implement auto-scaling for data processing workloads?

**Answer:**
Kubernetes provides multiple auto-scaling mechanisms to handle varying data processing loads efficiently: Horizontal Pod Autoscaler (HPA), Vertical Pod Autoscaler (VPA), and Cluster Autoscaler.

**Auto-scaling Components:**

**1. Horizontal Pod Autoscaler (HPA)**
- **Purpose**: Scales the number of pod replicas based on metrics
- **Metrics**: CPU, memory, custom metrics (queue length, processing rate)
- **Algorithm**: Target utilization percentage with stabilization windows

**2. Vertical Pod Autoscaler (VPA)**
- **Purpose**: Adjusts CPU and memory requests/limits for containers
- **Modes**: Off, Initial, Auto (with pod restart)
- **Use Case**: Right-sizing containers for optimal resource usage

**3. Cluster Autoscaler**
- **Purpose**: Scales the number of nodes in the cluster
- **Integration**: Works with cloud provider auto-scaling groups
- **Efficiency**: Adds/removes nodes based on pod scheduling needs

```yaml
# Comprehensive HPA for data processing
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: data-processor-hpa
  namespace: data-processing
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-processor
  minReplicas: 2
  maxReplicas: 50
  metrics:
  # CPU-based scaling
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  
  # Memory-based scaling
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  
  # Custom metric: Queue length
  - type: Pods
    pods:
      metric:
        name: queue_messages_per_pod
      target:
        type: AverageValue
        averageValue: "10"
  
  # External metric: Processing rate
  - type: External
    external:
      metric:
        name: processing_rate_per_second
        selector:
          matchLabels:
            service: data-processor
      target:
        type: Value
        value: "100"
  
  # Scaling behavior configuration
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300  # 5 minutes
      policies:
      - type: Percent
        value: 10  # Scale down by 10% of current replicas
        periodSeconds: 60
      - type: Pods
        value: 2   # Or scale down by 2 pods
        periodSeconds: 60
      selectPolicy: Min  # Use the policy that results in fewer pods removed
    
    scaleUp:
      stabilizationWindowSeconds: 60   # 1 minute
      policies:
      - type: Percent
        value: 50  # Scale up by 50% of current replicas
        periodSeconds: 60
      - type: Pods
        value: 5   # Or scale up by 5 pods
        periodSeconds: 60
      selectPolicy: Max  # Use the policy that results in more pods added

---
# VPA for automatic resource optimization
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: data-processor-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-processor
  updatePolicy:
    updateMode: "Auto"  # Auto, Initial, Off
  resourcePolicy:
    containerPolicies:
    - containerName: processor
      maxAllowed:
        cpu: 8
        memory: 32Gi
      minAllowed:
        cpu: 100m
        memory: 128Mi
      controlledResources: ["cpu", "memory"]
      controlledValues: RequestsAndLimits
```

**Custom Metrics for Data Engineering:**
```yaml
# ServiceMonitor for Prometheus metrics collection
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: data-processor-metrics
spec:
  selector:
    matchLabels:
      app: data-processor
  endpoints:
  - port: metrics
    path: /metrics
    interval: 30s

---
# Custom metrics application deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-processor
  template:
    metadata:
      labels:
        app: data-processor
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: processor
        image: my-registry/data-processor:v1.0
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 9090
          name: metrics
        env:
        - name: METRICS_ENABLED
          value: "true"
        - name: QUEUE_URL
          valueFrom:
            configMapKeyRef:
              name: processing-config
              key: queue.url
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        # Application exposes custom metrics:
        # - queue_messages_total
        # - processing_rate_per_second
        # - data_processing_duration_seconds
        # - active_connections_total
```

**KEDA (Kubernetes Event-Driven Autoscaling):**
```yaml
# KEDA ScaledObject for event-driven scaling
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: kafka-processor-scaler
spec:
  scaleTargetRef:
    name: kafka-data-processor
  minReplicaCount: 1
  maxReplicaCount: 30
  triggers:
  # Kafka topic lag-based scaling
  - type: kafka
    metadata:
      bootstrapServers: kafka-cluster:9092
      consumerGroup: data-processor-group
      topic: data-events
      lagThreshold: "100"
  
  # Redis queue length scaling
  - type: redis
    metadata:
      address: redis-cluster:6379
      listName: processing-queue
      listLength: "10"
  
  # Prometheus query scaling
  - type: prometheus
    metadata:
      serverAddress: http://prometheus:9090
      metricName: pending_jobs_count
      threshold: "5"
      query: sum(pending_jobs{service="data-processor"})

---
# Advanced scaling with multiple triggers
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: multi-trigger-scaler
spec:
  scaleTargetRef:
    name: data-processor
  minReplicaCount: 2
  maxReplicaCount: 100
  triggers:
  # Scale based on CPU (similar to HPA)
  - type: cpu
    metadata:
      type: Utilization
      value: "70"
  
  # Scale based on memory
  - type: memory
    metadata:
      type: Utilization
      value: "80"
  
  # Scale based on external queue
  - type: external-push
    metadata:
      scalerAddress: queue-scaler-service:8080
```

**Monitoring and Troubleshooting Auto-scaling:**
```bash
# Check HPA status
kubectl get hpa
kubectl describe hpa data-processor-hpa

# View HPA events and decisions
kubectl get events --field-selector involvedObject.name=data-processor-hpa

# Check VPA recommendations
kubectl get vpa data-processor-vpa -o yaml
kubectl describe vpa data-processor-vpa

# Monitor cluster autoscaler
kubectl logs -n kube-system deployment/cluster-autoscaler

# Check node resource usage
kubectl top nodes
kubectl top pods

# Custom metrics debugging
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1" | jq .
kubectl get --raw "/apis/external.metrics.k8s.io/v1beta1" | jq .
```

---

## Interview Preparation Checklist

### 📋 **Before the Interview**
- [ ] Understand Kubernetes architecture and core components
- [ ] Practice writing YAML manifests for different workload types
- [ ] Know storage concepts: PV, PVC, StorageClass
- [ ] Understand networking: Services, Ingress, NetworkPolicies
- [ ] Learn security concepts: RBAC, Pod Security Standards
- [ ] Practice troubleshooting common issues

### 🎯 **During the Interview**
- [ ] Explain concepts with real-world data engineering examples
- [ ] Demonstrate understanding of production considerations
- [ ] Discuss scaling strategies and resource management
- [ ] Show knowledge of monitoring and observability
- [ ] Address security and compliance requirements

### 📈 **Key Success Factors**
- **Practical Experience**: Hands-on experience with K8s in data projects
- **Production Awareness**: Understanding of reliability, security, and performance
- **Problem Solving**: Ability to troubleshoot and optimize deployments
- **Best Practices**: Knowledge of industry standards and patterns

---

**Remember**: Kubernetes mastery comes from practical experience. Deploy real data engineering workloads to understand the nuances of container orchestration in production environments.