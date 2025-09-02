# Kubernetes Comprehensive Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Core Concepts Questions (1-15)](#core-concepts-questions-1-15)
2. [Workload Management (16-30)](#workload-management-16-30)
3. [Networking & Services (31-45)](#networking--services-31-45)
4. [Storage & Persistence (46-60)](#storage--persistence-46-60)
5. [Security & RBAC (61-75)](#security--rbac-61-75)
6. [Monitoring & Operations (76-90)](#monitoring--operations-76-90)
7. [Data Engineering Integration (91-100)](#data-engineering-integration-91-100)

---

## 🎯 **Introduction**

Kubernetes is a container orchestration platform that automates deployment, scaling, and management of containerized applications. For data engineers, Kubernetes provides scalable infrastructure for data pipelines, streaming applications, and analytics workloads.

**Why Kubernetes is Critical for Data Engineers:**
- **Scalability**: Auto-scaling for variable data processing workloads
- **Resource Management**: Efficient resource allocation and isolation
- **High Availability**: Built-in fault tolerance and self-healing
- **Portability**: Consistent deployment across environments
- **Ecosystem**: Rich ecosystem for data tools and frameworks

---

## Core Concepts Questions (1-15)

### 1. Explain Kubernetes architecture and core components.
**Answer**: 
Kubernetes follows a master-worker architecture with several key components.

**Control Plane Components:**
- **API Server**: Central management entity, exposes Kubernetes API
- **etcd**: Distributed key-value store for cluster state
- **Controller Manager**: Runs controller processes
- **Scheduler**: Assigns pods to nodes based on resource requirements

**Node Components:**
- **kubelet**: Agent that runs on each node
- **kube-proxy**: Network proxy for service communication
- **Container Runtime**: Docker, containerd, or CRI-O

```yaml
# Example cluster information
apiVersion: v1
kind: ConfigMap
metadata:
  name: cluster-info
  namespace: kube-system
data:
  cluster-name: "data-engineering-cluster"
  cluster-region: "us-west-2"
  cluster-version: "1.28"
```

```bash
# Check cluster components
kubectl get componentstatuses
kubectl get nodes -o wide
kubectl cluster-info

# View cluster resources
kubectl top nodes
kubectl describe node <node-name>
```

### 2. What are Kubernetes objects and how do they relate to data engineering workloads?
**Answer**: 
Kubernetes objects are persistent entities that represent the desired state of your cluster.

**Core Objects for Data Engineering:**
```yaml
# Pod - Basic execution unit
apiVersion: v1
kind: Pod
metadata:
  name: spark-driver
  labels:
    app: spark
    component: driver
spec:
  containers:
  - name: spark-driver
    image: apache/spark:3.4.0
    resources:
      requests:
        memory: "2Gi"
        cpu: "1"
      limits:
        memory: "4Gi"
        cpu: "2"
    env:
    - name: SPARK_MODE
      value: "driver"

---
# Deployment - Manages replica sets
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-connect
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kafka-connect
  template:
    metadata:
      labels:
        app: kafka-connect
    spec:
      containers:
      - name: kafka-connect
        image: confluentinc/cp-kafka-connect:7.4.0
        ports:
        - containerPort: 8083
        env:
        - name: CONNECT_BOOTSTRAP_SERVERS
          value: "kafka:9092"
        - name: CONNECT_GROUP_ID
          value: "connect-cluster"

---
# Service - Network abstraction
apiVersion: v1
kind: Service
metadata:
  name: kafka-connect-service
spec:
  selector:
    app: kafka-connect
  ports:
  - port: 8083
    targetPort: 8083
  type: ClusterIP
```

### 3. How do you manage configuration and secrets in Kubernetes for data applications?
**Answer**: 
Kubernetes provides ConfigMaps and Secrets for configuration management.

**ConfigMap for Application Configuration:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: spark-config
data:
  spark-defaults.conf: |
    spark.sql.adaptive.enabled=true
    spark.sql.adaptive.coalescePartitions.enabled=true
    spark.serializer=org.apache.spark.serializer.KryoSerializer
    spark.sql.warehouse.dir=/opt/spark/warehouse
  log4j.properties: |
    log4j.rootLogger=INFO, console
    log4j.appender.console=org.apache.spark.util.logging.ConsoleAppender
    log4j.appender.console.layout=org.apache.log4j.PatternLayout

---
# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: database-credentials
type: Opaque
data:
  username: ZGF0YWVuZ2luZWVy  # base64 encoded
  password: c2VjdXJlcGFzcw==  # base64 encoded
  connection-string: cG9zdGdyZXNxbDovL2RhdGFlbmdpbmVlcjpzZWN1cmVwYXNzQHBvc3RncmVzOjU0MzIvZGF0YXdhcmVob3VzZQ==

---
# Using ConfigMap and Secret in Pod
apiVersion: v1
kind: Pod
metadata:
  name: data-processor
spec:
  containers:
  - name: processor
    image: python:3.9
    volumeMounts:
    - name: config-volume
      mountPath: /etc/config
    - name: secret-volume
      mountPath: /etc/secrets
      readOnly: true
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: database-credentials
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: database-credentials
          key: password
  volumes:
  - name: config-volume
    configMap:
      name: spark-config
  - name: secret-volume
    secret:
      secretName: database-credentials
```

## Workload Management (16-30)

### 4. How do you deploy and manage Spark applications on Kubernetes?
**Answer**: 
Spark on Kubernetes can be deployed using native Kubernetes support or operators.

**Native Spark on Kubernetes:**
```bash
# Submit Spark application to Kubernetes
spark-submit \
  --master k8s://https://kubernetes-api-server:6443 \
  --deploy-mode cluster \
  --name spark-pi \
  --class org.apache.spark.examples.SparkPi \
  --conf spark.executor.instances=3 \
  --conf spark.kubernetes.container.image=apache/spark:3.4.0 \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.kubernetes.namespace=data-engineering \
  --conf spark.executor.memory=2g \
  --conf spark.executor.cores=2 \
  --conf spark.driver.memory=1g \
  local:///opt/spark/examples/jars/spark-examples_2.12-3.4.0.jar 10
```

**Spark Operator Deployment:**
```yaml
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: data-processing-job
  namespace: data-engineering
spec:
  type: Python
  pythonVersion: "3"
  mode: cluster
  image: "apache/spark-py:3.4.0"
  imagePullPolicy: Always
  mainApplicationFile: local:///opt/spark/work-dir/data_processing.py
  sparkVersion: "3.4.0"
  restartPolicy:
    type: OnFailure
    onFailureRetries: 3
    onFailureRetryInterval: 10
    onSubmissionFailureRetries: 5
    onSubmissionFailureRetryInterval: 20
  driver:
    cores: 1
    coreLimit: "1200m"
    memory: "2g"
    labels:
      version: 3.4.0
    serviceAccount: spark
    volumeMounts:
      - name: data-volume
        mountPath: /data
  executor:
    cores: 2
    instances: 3
    memory: "4g"
    labels:
      version: 3.4.0
    volumeMounts:
      - name: data-volume
        mountPath: /data
  volumes:
    - name: data-volume
      persistentVolumeClaim:
        claimName: data-pvc
  monitoring:
    exposeDriverMetrics: true
    exposeExecutorMetrics: true
    prometheus:
      jmxExporterJar: "/prometheus/jmx_prometheus_javaagent-0.17.0.jar"
      port: 8090
```

### 5. How do you implement auto-scaling for data processing workloads?
**Answer**: 
Kubernetes provides multiple auto-scaling mechanisms for data workloads.

**Horizontal Pod Autoscaler (HPA):**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: kafka-consumer-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: kafka-consumer
  minReplicas: 2
  maxReplicas: 20
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
  - type: Pods
    pods:
      metric:
        name: kafka_consumer_lag
      target:
        type: AverageValue
        averageValue: "100"
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
```

**Vertical Pod Autoscaler (VPA):**
```yaml
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
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: processor
      minAllowed:
        cpu: 100m
        memory: 128Mi
      maxAllowed:
        cpu: 4
        memory: 8Gi
      controlledResources: ["cpu", "memory"]
```

### 6. How do you manage batch jobs and workflows in Kubernetes?
**Answer**: 
Kubernetes provides Job and CronJob resources for batch processing.

**Batch Job for Data Processing:**
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: etl-batch-job
spec:
  parallelism: 3
  completions: 10
  backoffLimit: 3
  activeDeadlineSeconds: 3600
  template:
    metadata:
      labels:
        app: etl-job
    spec:
      restartPolicy: Never
      containers:
      - name: etl-processor
        image: python:3.9
        command: ["python", "/app/etl_script.py"]
        env:
        - name: BATCH_SIZE
          value: "1000"
        - name: S3_BUCKET
          value: "data-lake-bucket"
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        volumeMounts:
        - name: data-volume
          mountPath: /data
      volumes:
      - name: data-volume
        persistentVolumeClaim:
          claimName: shared-data-pvc

---
# CronJob for scheduled data processing
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-data-sync
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: data-sync
            image: data-sync:latest
            command: ["python", "/app/sync_data.py"]
            env:
            - name: SYNC_DATE
              value: "$(date -d 'yesterday' +%Y-%m-%d)"
          restartPolicy: OnFailure
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
```

## Networking & Services (31-45)

### 7. How do you configure networking for data engineering applications?
**Answer**: 
Kubernetes networking enables communication between data services and external systems.

**Service Types and Configuration:**
```yaml
# ClusterIP for internal communication
apiVersion: v1
kind: Service
metadata:
  name: kafka-internal
spec:
  type: ClusterIP
  selector:
    app: kafka
  ports:
  - port: 9092
    targetPort: 9092
    name: kafka

---
# NodePort for external access
apiVersion: v1
kind: Service
metadata:
  name: jupyter-notebook
spec:
  type: NodePort
  selector:
    app: jupyter
  ports:
  - port: 8888
    targetPort: 8888
    nodePort: 30888

---
# LoadBalancer for production access
apiVersion: v1
kind: Service
metadata:
  name: api-gateway
spec:
  type: LoadBalancer
  selector:
    app: api-gateway
  ports:
  - port: 80
    targetPort: 8080
  loadBalancerSourceRanges:
  - "10.0.0.0/8"
  - "192.168.0.0/16"

---
# Headless service for StatefulSet
apiVersion: v1
kind: Service
metadata:
  name: elasticsearch-headless
spec:
  clusterIP: None
  selector:
    app: elasticsearch
  ports:
  - port: 9200
    name: http
  - port: 9300
    name: transport
```

**Network Policies for Security:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: data-tier-policy
spec:
  podSelector:
    matchLabels:
      tier: data
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          tier: application
    ports:
    - protocol: TCP
      port: 5432
  egress:
  - to:
    - podSelector:
        matchLabels:
          tier: monitoring
    ports:
    - protocol: TCP
      port: 9090
```

### 8. How do you implement service discovery for microservices architecture?
**Answer**: 
Kubernetes provides built-in service discovery through DNS and environment variables.

**Service Discovery Configuration:**
```yaml
# Service for discovery
apiVersion: v1
kind: Service
metadata:
  name: data-api
  labels:
    app: data-api
    version: v1
spec:
  selector:
    app: data-api
  ports:
  - port: 8080
    targetPort: 8080

---
# Consumer using service discovery
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-consumer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-consumer
  template:
    metadata:
      labels:
        app: data-consumer
    spec:
      containers:
      - name: consumer
        image: data-consumer:latest
        env:
        - name: DATA_API_URL
          value: "http://data-api:8080"  # DNS-based discovery
        - name: KAFKA_BROKERS
          value: "kafka-0.kafka-headless:9092,kafka-1.kafka-headless:9092"
```

## Storage & Persistence (46-60)

### 9. How do you manage persistent storage for data applications?
**Answer**: 
Kubernetes provides various storage options for data persistence.

**Persistent Volume and Claims:**
```yaml
# Storage Class
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
reclaimPolicy: Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer

---
# Persistent Volume Claim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-lake-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi

---
# StatefulSet with persistent storage
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: elasticsearch
spec:
  serviceName: elasticsearch-headless
  replicas: 3
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - name: elasticsearch
        image: elasticsearch:8.8.0
        ports:
        - containerPort: 9200
        - containerPort: 9300
        volumeMounts:
        - name: data
          mountPath: /usr/share/elasticsearch/data
        env:
        - name: cluster.name
          value: "data-cluster"
        - name: node.name
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 50Gi
```

### 10. How do you implement backup and disaster recovery for data workloads?
**Answer**: 
Kubernetes backup strategies involve volume snapshots and application-specific backups.

**Volume Snapshot Configuration:**
```yaml
# Volume Snapshot Class
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshotClass
metadata:
  name: csi-aws-vsc
driver: ebs.csi.aws.com
deletionPolicy: Retain

---
# Volume Snapshot
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: data-backup-snapshot
spec:
  volumeSnapshotClassName: csi-aws-vsc
  source:
    persistentVolumeClaimName: data-lake-pvc

---
# Backup CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
spec:
  schedule: "0 2 * * *"
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
              pg_dump -h postgres-service -U $POSTGRES_USER $POSTGRES_DB | \
              gzip > /backup/backup-$(date +%Y%m%d-%H%M%S).sql.gz
              
              # Upload to S3
              aws s3 cp /backup/backup-$(date +%Y%m%d-%H%M%S).sql.gz \
                s3://backup-bucket/postgres/
            env:
            - name: POSTGRES_USER
              valueFrom:
                secretKeyRef:
                  name: postgres-secret
                  key: username
            - name: POSTGRES_DB
              value: "datawarehouse"
            volumeMounts:
            - name: backup-volume
              mountPath: /backup
          volumes:
          - name: backup-volume
            emptyDir: {}
          restartPolicy: OnFailure
```

## Security & RBAC (61-75)

### 11. How do you implement security and access control for data applications?
**Answer**: 
Kubernetes security involves RBAC, network policies, and pod security standards.

**RBAC Configuration:**
```yaml
# Service Account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: data-engineer
  namespace: data-engineering

---
# Role for data engineering operations
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: data-engineering
  name: data-engineer-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: ["batch"]
  resources: ["jobs", "cronjobs"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

---
# Role Binding
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: data-engineer-binding
  namespace: data-engineering
subjects:
- kind: ServiceAccount
  name: data-engineer
  namespace: data-engineering
roleRef:
  kind: Role
  name: data-engineer-role
  apiGroup: rbac.authorization.k8s.io

---
# Cluster Role for cross-namespace access
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: spark-operator
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps"]
  verbs: ["*"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["*"]
- apiGroups: ["sparkoperator.k8s.io"]
  resources: ["sparkapplications", "scheduledsparkapplications"]
  verbs: ["*"]
```

**Pod Security Standards:**
```yaml
# Pod Security Policy (deprecated, use Pod Security Standards)
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: data-processing-psp
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'

---
# Security Context in Pod
apiVersion: v1
kind: Pod
metadata:
  name: secure-data-processor
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: processor
    image: data-processor:latest
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: tmp
      mountPath: /tmp
    - name: var-run
      mountPath: /var/run
  volumes:
  - name: tmp
    emptyDir: {}
  - name: var-run
    emptyDir: {}
```

## Monitoring & Operations (76-90)

### 12. How do you implement monitoring and observability for Kubernetes data workloads?
**Answer**: 
Comprehensive monitoring involves metrics, logs, and traces collection.

**Prometheus Monitoring Setup:**
```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: spark-metrics
  labels:
    app: spark
spec:
  selector:
    matchLabels:
      app: spark
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics

---
# Grafana Dashboard ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: spark-dashboard
  labels:
    grafana_dashboard: "1"
data:
  spark-dashboard.json: |
    {
      "dashboard": {
        "title": "Spark Applications",
        "panels": [
          {
            "title": "Active Executors",
            "type": "stat",
            "targets": [
              {
                "expr": "spark_executor_count",
                "legendFormat": "Executors"
              }
            ]
          }
        ]
      }
    }

---
# Custom metrics for data processing
apiVersion: v1
kind: Service
metadata:
  name: data-processor-metrics
  labels:
    app: data-processor
spec:
  ports:
  - port: 8080
    name: metrics
  selector:
    app: data-processor
```

**Logging Configuration:**
```yaml
# Fluentd DaemonSet for log collection
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd
  namespace: kube-system
spec:
  selector:
    matchLabels:
      name: fluentd
  template:
    metadata:
      labels:
        name: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd-kubernetes-daemonset:v1-debian-elasticsearch
        env:
        - name: FLUENT_ELASTICSEARCH_HOST
          value: "elasticsearch.logging.svc.cluster.local"
        - name: FLUENT_ELASTICSEARCH_PORT
          value: "9200"
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
        - name: config-volume
          mountPath: /fluentd/etc
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
      - name: config-volume
        configMap:
          name: fluentd-config
```

### 13. How do you implement health checks and self-healing for data applications?
**Answer**: 
Kubernetes provides liveness, readiness, and startup probes for application health.

**Health Check Configuration:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-consumer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kafka-consumer
  template:
    metadata:
      labels:
        app: kafka-consumer
    spec:
      containers:
      - name: consumer
        image: kafka-consumer:latest
        ports:
        - containerPort: 8080
        
        # Startup probe - initial health check
        startupProbe:
          httpGet:
            path: /health/startup
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 30
        
        # Liveness probe - restart if unhealthy
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        
        # Readiness probe - remove from service if not ready
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        # Resource limits for stability
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1"
        
        # Graceful shutdown
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 15"]
        
        env:
        - name: KAFKA_BROKERS
          value: "kafka:9092"
        - name: CONSUMER_GROUP
          value: "data-processing-group"
```

## Data Engineering Integration (91-100)

### 14. How do you deploy and manage Apache Airflow on Kubernetes?
**Answer**: 
Airflow on Kubernetes provides scalable workflow orchestration.

**Airflow Kubernetes Deployment:**
```yaml
# Airflow Scheduler
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airflow-scheduler
spec:
  replicas: 1
  selector:
    matchLabels:
      app: airflow-scheduler
  template:
    metadata:
      labels:
        app: airflow-scheduler
    spec:
      containers:
      - name: scheduler
        image: apache/airflow:2.7.0
        command: ["airflow", "scheduler"]
        env:
        - name: AIRFLOW__CORE__EXECUTOR
          value: "KubernetesExecutor"
        - name: AIRFLOW__KUBERNETES__NAMESPACE
          value: "airflow"
        - name: AIRFLOW__KUBERNETES__WORKER_CONTAINER_REPOSITORY
          value: "apache/airflow"
        - name: AIRFLOW__KUBERNETES__WORKER_CONTAINER_TAG
          value: "2.7.0"
        volumeMounts:
        - name: dags
          mountPath: /opt/airflow/dags
        - name: logs
          mountPath: /opt/airflow/logs
      volumes:
      - name: dags
        persistentVolumeClaim:
          claimName: airflow-dags-pvc
      - name: logs
        persistentVolumeClaim:
          claimName: airflow-logs-pvc

---
# Airflow Webserver
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airflow-webserver
spec:
  replicas: 2
  selector:
    matchLabels:
      app: airflow-webserver
  template:
    metadata:
      labels:
        app: airflow-webserver
    spec:
      containers:
      - name: webserver
        image: apache/airflow:2.7.0
        command: ["airflow", "webserver"]
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10

---
# Service for Airflow Webserver
apiVersion: v1
kind: Service
metadata:
  name: airflow-webserver
spec:
  selector:
    app: airflow-webserver
  ports:
  - port: 8080
    targetPort: 8080
  type: LoadBalancer
```

### 15. How do you implement a complete data pipeline architecture on Kubernetes?
**Answer**: 
A complete data pipeline involves ingestion, processing, storage, and monitoring components.

**Complete Data Pipeline Architecture:**
```yaml
# Kafka for data ingestion
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: kafka
spec:
  serviceName: kafka-headless
  replicas: 3
  selector:
    matchLabels:
      app: kafka
  template:
    metadata:
      labels:
        app: kafka
    spec:
      containers:
      - name: kafka
        image: confluentinc/cp-kafka:7.4.0
        ports:
        - containerPort: 9092
        env:
        - name: KAFKA_BROKER_ID
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: KAFKA_ZOOKEEPER_CONNECT
          value: "zookeeper:2181"
        - name: KAFKA_ADVERTISED_LISTENERS
          value: "PLAINTEXT://$(POD_NAME).kafka-headless:9092"
        volumeMounts:
        - name: kafka-data
          mountPath: /var/lib/kafka/data
  volumeClaimTemplates:
  - metadata:
      name: kafka-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 100Gi

---
# Spark for data processing
apiVersion: sparkoperator.k8s.io/v1beta2
kind: SparkApplication
metadata:
  name: streaming-etl
spec:
  type: Scala
  mode: cluster
  image: "apache/spark:3.4.0"
  mainClass: "com.company.StreamingETL"
  mainApplicationFile: "local:///opt/spark/work-dir/streaming-etl.jar"
  sparkVersion: "3.4.0"
  driver:
    cores: 2
    memory: "4g"
    serviceAccount: spark
  executor:
    cores: 2
    instances: 5
    memory: "4g"
  deps:
    packages:
      - "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0"
  sparkConf:
    "spark.sql.streaming.checkpointLocation": "/tmp/checkpoint"
    "spark.sql.adaptive.enabled": "true"

---
# PostgreSQL for data warehouse
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
spec:
  serviceName: postgres-headless
  replicas: 1
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
        - name: POSTGRES_DB
          value: "datawarehouse"
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
        volumeMounts:
        - name: postgres-data
          mountPath: /var/lib/postgresql/data
  volumeClaimTemplates:
  - metadata:
      name: postgres-data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 200Gi

---
# Redis for caching
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1"

---
# Monitoring with Prometheus
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
        - name: data
          mountPath: /prometheus
      volumes:
      - name: config
        configMap:
          name: prometheus-config
      - name: data
        persistentVolumeClaim:
          claimName: prometheus-data-pvc
```

**Pipeline Orchestration with Argo Workflows:**
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  name: data-pipeline
spec:
  entrypoint: data-pipeline
  templates:
  - name: data-pipeline
    dag:
      tasks:
      - name: extract-data
        template: extract
      - name: transform-data
        template: transform
        dependencies: [extract-data]
      - name: load-data
        template: load
        dependencies: [transform-data]
      - name: validate-data
        template: validate
        dependencies: [load-data]
  
  - name: extract
    container:
      image: data-extractor:latest
      command: [python, /app/extract.py]
      env:
      - name: SOURCE_DB
        value: "postgresql://source:5432/production"
  
  - name: transform
    container:
      image: apache/spark:3.4.0
      command: [spark-submit, /app/transform.py]
      resources:
        requests:
          memory: 4Gi
          cpu: 2
  
  - name: load
    container:
      image: data-loader:latest
      command: [python, /app/load.py]
      env:
      - name: TARGET_DB
        value: "postgresql://warehouse:5432/datawarehouse"
  
  - name: validate
    container:
      image: data-validator:latest
      command: [python, /app/validate.py]
```

---

## 🎯 **Summary**

This comprehensive guide covers Kubernetes essential concepts for data engineering interviews. Key areas include:

- **Container orchestration** for scalable data applications
- **Workload management** with deployments, jobs, and auto-scaling
- **Storage and persistence** for data applications
- **Security and RBAC** for production environments
- **Monitoring and observability** for operational excellence
- **Data pipeline integration** with Spark, Kafka, and Airflow

**Interview Preparation Tips:**
1. **Master core concepts** - Understand pods, services, and deployments
2. **Know storage patterns** - Persistent volumes and StatefulSets
3. **Practice YAML configuration** - Be comfortable writing manifests
4. **Understand scaling strategies** - HPA, VPA, and cluster autoscaling
5. **Study data tool integration** - How Spark, Kafka, and Airflow run on K8s