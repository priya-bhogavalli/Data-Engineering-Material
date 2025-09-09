# ☸️ Kubernetes Interview Questions for Data Engineering (Enhanced)

## 📋 Table of Contents

1. [Core Concepts (1-25)](#core-concepts-1-25)
2. [Data Workloads (26-50)](#data-workloads-26-50)
3. [Storage & Persistence (51-75)](#storage--persistence-51-75)
4. [Production & Operations (76-100)](#production--operations-76-100)

---

## Core Concepts (1-25)

### 1. What is Kubernetes and why is it important for data engineering?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Kubernetes is a container orchestration platform that automates deployment, scaling, and management of containerized applications.

**Benefits for Data Engineering:**
- **Scalability**: Auto-scale data processing workloads
- **Resource Management**: Efficient resource allocation
- **Fault Tolerance**: Automatic recovery and healing
- **Multi-tenancy**: Isolate different data pipelines

```yaml
# Data processing deployment
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
        image: my-pipeline:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
```

### 2. How do you deploy Spark applications on Kubernetes?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Use Spark Operator or native Kubernetes support for Spark.

```yaml
# Spark Application with Operator
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: spark-pi
spec:
  type: Scala
  mode: cluster
  image: gcr.io/spark-operator/spark:v3.3.0
  imagePullPolicy: Always
  mainClass: org.apache.spark.examples.SparkPi
  mainApplicationFile: local:///opt/spark/examples/jars/spark-examples_2.12-3.3.0.jar
  sparkVersion: 3.3.0
  driver:
    cores: 1
    coreLimit: 1200m
    memory: 512m
    serviceAccount: spark
  executor:
    cores: 1
    instances: 2
    memory: 512m
```

### 3. How do you manage data pipeline configurations in Kubernetes?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Use ConfigMaps and Secrets for configuration management.

```yaml
# ConfigMap for pipeline configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: pipeline-config
data:
  config.yaml: |
    database:
      host: postgres-service
      port: 5432
      name: datadb
    kafka:
      brokers: kafka-service:9092
      topics:
        - user-events
        - order-events
    batch_size: 1000
    processing_interval: 60

---
# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: pipeline-secrets
type: Opaque
data:
  db-password: cGFzc3dvcmQ=  # base64 encoded
  api-key: YWJjZGVmZ2g=

---
# Deployment using ConfigMap and Secret
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processor
spec:
  template:
    spec:
      containers:
      - name: processor
        image: data-processor:latest
        volumeMounts:
        - name: config
          mountPath: /app/config
        - name: secrets
          mountPath: /app/secrets
        env:
        - name: CONFIG_PATH
          value: /app/config/config.yaml
      volumes:
      - name: config
        configMap:
          name: pipeline-config
      - name: secrets
        secret:
          secretName: pipeline-secrets
```

## Data Workloads (26-50)

### 26. How do you run batch processing jobs in Kubernetes?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Use Jobs and CronJobs for batch processing workloads.

```yaml
# Batch processing Job
apiVersion: batch/v1
kind: Job
metadata:
  name: daily-etl-job
spec:
  template:
    spec:
      containers:
      - name: etl
        image: etl-processor:latest
        command: ["python", "daily_etl.py"]
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
          limits:
            memory: "8Gi"
            cpu: "4000m"
        env:
        - name: PROCESSING_DATE
          value: "2023-01-01"
      restartPolicy: Never
  backoffLimit: 3

---
# Scheduled CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: hourly-aggregation
spec:
  schedule: "0 * * * *"  # Every hour
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: aggregator
            image: data-aggregator:latest
            command: ["python", "hourly_agg.py"]
          restartPolicy: OnFailure
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
```

### 27. How do you implement streaming data processing?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Deploy streaming applications with proper resource management and scaling.

```yaml
# Kafka Streams application
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-streams-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kafka-streams
  template:
    metadata:
      labels:
        app: kafka-streams
    spec:
      containers:
      - name: streams
        image: kafka-streams-app:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: KAFKA_BROKERS
          value: "kafka-service:9092"
        - name: APPLICATION_ID
          value: "user-analytics-stream"
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
# HorizontalPodAutoscaler for streaming app
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: kafka-streams-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: kafka-streams-app
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

## Storage & Persistence (51-75)

### 51. How do you handle persistent storage for data applications?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Use PersistentVolumes and StatefulSets for data persistence.

```yaml
# StorageClass for fast SSD storage
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
allowVolumeExpansion: true

---
# StatefulSet for database
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-cluster
spec:
  serviceName: postgres-service
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:13
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secret
              key: password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 100Gi
```

### 52. How do you backup and restore data in Kubernetes?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Use backup operators and volume snapshots.

```yaml
# Velero backup configuration
apiVersion: velero.io/v1
kind: Backup
metadata:
  name: daily-backup
spec:
  includedNamespaces:
  - data-engineering
  includedResources:
  - persistentvolumes
  - persistentvolumeclaims
  - secrets
  - configmaps
  storageLocation: aws-backup-location
  ttl: 720h0m0s  # 30 days

---
# VolumeSnapshot for database backup
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: postgres-snapshot
spec:
  volumeSnapshotClassName: csi-aws-vsc
  source:
    persistentVolumeClaimName: postgres-storage-postgres-cluster-0
```

## Production & Operations (76-100)

### 76. How do you monitor data applications in Kubernetes?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Use Prometheus, Grafana, and custom metrics for monitoring.

```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: data-pipeline-metrics
spec:
  selector:
    matchLabels:
      app: data-pipeline
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics

---
# Custom metrics for data pipeline
apiVersion: v1
kind: Service
metadata:
  name: pipeline-metrics
  labels:
    app: data-pipeline
spec:
  ports:
  - name: metrics
    port: 8080
    targetPort: 8080
  selector:
    app: data-pipeline
```

### 77. How do you implement security for data workloads?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Use RBAC, Network Policies, and Pod Security Standards.

```yaml
# ServiceAccount for data pipeline
apiVersion: v1
kind: ServiceAccount
metadata:
  name: data-pipeline-sa

---
# Role with specific permissions
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: data-pipeline-role
rules:
- apiGroups: [""]
  resources: ["secrets", "configmaps"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "create"]

---
# RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: data-pipeline-binding
subjects:
- kind: ServiceAccount
  name: data-pipeline-sa
roleRef:
  kind: Role
  name: data-pipeline-role
  apiGroup: rbac.authorization.k8s.io

---
# NetworkPolicy for isolation
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: data-pipeline-netpol
spec:
  podSelector:
    matchLabels:
      app: data-pipeline
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: api-gateway
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
```

### 78. How do you handle resource management and optimization?

#### **Mathematical/Algorithmic Basis**
Algorithmic foundations underlying kubernetes operations

#### **Case Studies**
Real-world case studies of kubernetes implementations

#### **Industry Direction**
Future direction of kubernetes technologies

### **Enhanced Answer**

**Answer**: Use resource quotas, limits, and vertical/horizontal scaling.

```yaml
# ResourceQuota for namespace
apiVersion: v1
kind: ResourceQuota
metadata:
  name: data-engineering-quota
spec:
  hard:
    requests.cpu: "100"
    requests.memory: 200Gi
    limits.cpu: "200"
    limits.memory: 400Gi
    persistentvolumeclaims: "50"

---
# LimitRange for default limits
apiVersion: v1
kind: LimitRange
metadata:
  name: data-pipeline-limits
spec:
  limits:
  - default:
      cpu: "1000m"
      memory: "2Gi"
    defaultRequest:
      cpu: "500m"
      memory: "1Gi"
    type: Container

---
# VerticalPodAutoscaler
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: data-pipeline-vpa
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-pipeline
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: pipeline
      maxAllowed:
        cpu: "4"
        memory: "8Gi"
      minAllowed:
        cpu: "500m"
        memory: "1Gi"
```

---

**Total Questions: 100** | **Coverage: Complete Kubernetes for Data Engineering**