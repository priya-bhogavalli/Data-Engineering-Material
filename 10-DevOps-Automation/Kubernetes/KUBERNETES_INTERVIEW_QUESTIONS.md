# Kubernetes Interview Questions

## Basic Level Questions (1-3 years experience)

### 1. What is Kubernetes and why is it used in data engineering?
**Answer**: Kubernetes is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications.

**Key Benefits for Data Engineering**:
- **Auto-scaling**: Scale data processing workloads based on demand
- **Resource Management**: Efficient allocation of CPU, memory, and storage
- **High Availability**: Automatic failover and self-healing
- **Service Discovery**: Easy communication between data services
- **Rolling Updates**: Zero-downtime deployments of data pipelines

```yaml
# Example: Data processing deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-processor
  labels:
    app: data-processor
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
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

### 2. Explain the main Kubernetes components
**Answer**: Kubernetes has control plane components and node components that work together to manage the cluster.

**Control Plane Components**:
- **API Server**: Central management entity, exposes Kubernetes API
- **etcd**: Distributed key-value store for cluster data
- **Scheduler**: Assigns pods to nodes based on resource requirements
- **Controller Manager**: Runs controller processes

**Node Components**:
- **kubelet**: Agent that runs on each node, manages pods
- **kube-proxy**: Network proxy, handles service networking
- **Container Runtime**: Runs containers (Docker, containerd, etc.)

```bash
# Check cluster components
kubectl get componentstatuses

# View cluster info
kubectl cluster-info

# Get node information
kubectl get nodes -o wide

# Describe a node
kubectl describe node <node-name>
```

### 3. What are Pods and how do they work?
**Answer**: A Pod is the smallest deployable unit in Kubernetes, containing one or more containers that share storage and network.

```yaml
# Simple pod definition
apiVersion: v1
kind: Pod
metadata:
  name: data-processor-pod
  labels:
    app: data-processor
spec:
  containers:
  - name: processor
    image: python:3.9
    command: ["python"]
    args: ["-c", "import time; time.sleep(3600)"]
    env:
    - name: ENVIRONMENT
      value: "production"
    volumeMounts:
    - name: data-volume
      mountPath: /data
  - name: sidecar-logger
    image: busybox
    command: ["sh"]
    args: ["-c", "tail -f /shared/logs/app.log"]
    volumeMounts:
    - name: shared-logs
      mountPath: /shared/logs
  volumes:
  - name: data-volume
    emptyDir: {}
  - name: shared-logs
    emptyDir: {}
  restartPolicy: Always
```

```bash
# Create pod
kubectl apply -f pod.yaml

# List pods
kubectl get pods

# Describe pod
kubectl describe pod data-processor-pod

# Get pod logs
kubectl logs data-processor-pod -c processor

# Execute command in pod
kubectl exec -it data-processor-pod -c processor -- bash

# Delete pod
kubectl delete pod data-processor-pod
```

### 4. What are Services and how do they enable communication?
**Answer**: Services provide stable network endpoints for accessing pods, enabling service discovery and load balancing.

```yaml
# ClusterIP Service (internal communication)
apiVersion: v1
kind: Service
metadata:
  name: data-processor-service
spec:
  selector:
    app: data-processor
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: ClusterIP

---
# NodePort Service (external access)
apiVersion: v1
kind: Service
metadata:
  name: data-api-service
spec:
  selector:
    app: data-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
    nodePort: 30080
  type: NodePort

---
# LoadBalancer Service (cloud provider)
apiVersion: v1
kind: Service
metadata:
  name: data-web-service
spec:
  selector:
    app: data-web
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

**Service Discovery Example**:
```yaml
# Consumer pod accessing service
apiVersion: v1
kind: Pod
metadata:
  name: data-consumer
spec:
  containers:
  - name: consumer
    image: my-registry/data-consumer:v1.0
    env:
    - name: DATA_PROCESSOR_URL
      value: "http://data-processor-service:80"
    # Kubernetes DNS automatically resolves service names
```

### 5. What are ConfigMaps and Secrets?
**Answer**: ConfigMaps store non-sensitive configuration data, while Secrets store sensitive information like passwords and API keys.

```yaml
# ConfigMap for application configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database.host: "postgres.default.svc.cluster.local"
  database.port: "5432"
  database.name: "datawarehouse"
  batch.size: "1000"
  log.level: "INFO"
  config.yaml: |
    processing:
      batch_size: 1000
      timeout: 30
    features:
      enable_caching: true
      enable_monitoring: true

---
# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: ZGF0YXVzZXI=  # base64 encoded 'datauser'
  password: cGFzc3dvcmQ=  # base64 encoded 'password'
  api-key: YWJjZGVmZ2hpams=  # base64 encoded API key
```

**Using ConfigMaps and Secrets in Pods**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-app
spec:
  containers:
  - name: app
    image: my-registry/data-app:v1.0
    # Environment variables from ConfigMap
    envFrom:
    - configMapRef:
        name: app-config
    # Specific environment variables from Secret
    env:
    - name: DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: username
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: password
    # Mount ConfigMap as volume
    volumeMounts:
    - name: config-volume
      mountPath: /app/config
    - name: secret-volume
      mountPath: /app/secrets
      readOnly: true
  volumes:
  - name: config-volume
    configMap:
      name: app-config
  - name: secret-volume
    secret:
      secretName: db-secret
```

```bash
# Create ConfigMap from literal values
kubectl create configmap app-config \
  --from-literal=database.host=postgres \
  --from-literal=batch.size=1000

# Create ConfigMap from file
kubectl create configmap app-config --from-file=config.yaml

# Create Secret
kubectl create secret generic db-secret \
  --from-literal=username=datauser \
  --from-literal=password=secretpassword

# View ConfigMap
kubectl get configmap app-config -o yaml

# View Secret (base64 encoded)
kubectl get secret db-secret -o yaml
```

## Intermediate Level Questions (3-5 years experience)

### 6. How do you manage persistent storage in Kubernetes?
**Answer**: Use Persistent Volumes (PV), Persistent Volume Claims (PVC), and Storage Classes for managing persistent storage.

```yaml
# Storage Class for dynamic provisioning
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
reclaimPolicy: Delete

---
# Persistent Volume Claim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-storage-claim
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi

---
# StatefulSet using persistent storage
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
spec:
  serviceName: database-service
  replicas: 3
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
    spec:
      containers:
      - name: postgres
        image: postgres:13
        env:
        - name: POSTGRES_DB
          value: datawarehouse
        - name: POSTGRES_USER
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: username
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        ports:
        - containerPort: 5432
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      storageClassName: fast-ssd
      resources:
        requests:
          storage: 50Gi
```

**Data Processing with Persistent Storage**:
```yaml
# Deployment with shared storage for data processing
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
    spec:
      containers:
      - name: processor
        image: my-registry/data-processor:v1.0
        volumeMounts:
        - name: input-data
          mountPath: /data/input
          readOnly: true
        - name: output-data
          mountPath: /data/output
        - name: temp-storage
          mountPath: /tmp/processing
      volumes:
      - name: input-data
        persistentVolumeClaim:
          claimName: input-data-claim
      - name: output-data
        persistentVolumeClaim:
          claimName: output-data-claim
      - name: temp-storage
        emptyDir:
          sizeLimit: 10Gi
```

### 7. How do you implement auto-scaling in Kubernetes?
**Answer**: Use Horizontal Pod Autoscaler (HPA) and Vertical Pod Autoscaler (VPA) for automatic scaling based on metrics.

```yaml
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: data-processor-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-processor
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
        name: queue_length
      target:
        type: AverageValue
        averageValue: "10"
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

---
# Vertical Pod Autoscaler
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
        cpu: 2
        memory: 4Gi
      minAllowed:
        cpu: 100m
        memory: 128Mi
```

**Custom Metrics for Scaling**:
```yaml
# Custom metrics using Prometheus adapter
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

---
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: data-processor-monitor
spec:
  selector:
    matchLabels:
      app: data-processor
  endpoints:
  - port: metrics
    path: /metrics
```

### 8. How do you handle Jobs and CronJobs for batch processing?
**Answer**: Use Jobs for one-time tasks and CronJobs for scheduled batch processing workloads.

```yaml
# Job for one-time data processing
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration-job
spec:
  parallelism: 3  # Run 3 pods in parallel
  completions: 10  # Complete 10 successful runs
  backoffLimit: 3  # Retry failed pods 3 times
  activeDeadlineSeconds: 3600  # Timeout after 1 hour
  template:
    metadata:
      labels:
        app: data-migration
    spec:
      restartPolicy: Never
      containers:
      - name: migrator
        image: my-registry/data-migrator:v1.0
        env:
        - name: BATCH_SIZE
          value: "1000"
        - name: SOURCE_DB
          valueFrom:
            configMapKeyRef:
              name: migration-config
              key: source.db
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        volumeMounts:
        - name: migration-data
          mountPath: /data
      volumes:
      - name: migration-data
        persistentVolumeClaim:
          claimName: migration-data-claim

---
# CronJob for scheduled ETL
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-etl-job
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  timeZone: "America/New_York"
  concurrencyPolicy: Forbid  # Don't run concurrent jobs
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  startingDeadlineSeconds: 300  # Start within 5 minutes
  jobTemplate:
    spec:
      backoffLimit: 2
      template:
        metadata:
          labels:
            app: daily-etl
        spec:
          restartPolicy: OnFailure
          containers:
          - name: etl-processor
            image: my-registry/etl-processor:v1.0
            env:
            - name: ETL_DATE
              value: "{{ .Values.etlDate | default \"today\" }}"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
            command:
            - /bin/bash
            - -c
            - |
              echo "Starting ETL for date: $ETL_DATE"
              python /app/etl_main.py --date $ETL_DATE
              echo "ETL completed successfully"
            resources:
              requests:
                memory: "4Gi"
                cpu: "2"
              limits:
                memory: "8Gi"
                cpu: "4"
```

**Managing Jobs**:
```bash
# Create job
kubectl apply -f job.yaml

# Monitor job progress
kubectl get jobs
kubectl describe job data-migration-job

# View job pods
kubectl get pods -l job-name=data-migration-job

# Get job logs
kubectl logs -l job-name=data-migration-job

# Delete completed jobs
kubectl delete job data-migration-job

# Manage CronJobs
kubectl get cronjobs
kubectl describe cronjob daily-etl-job

# Manually trigger CronJob
kubectl create job --from=cronjob/daily-etl-job manual-etl-run
```

### 9. How do you implement monitoring and logging?
**Answer**: Use Prometheus for metrics, Grafana for visualization, and centralized logging with ELK stack or similar.

```yaml
# Prometheus monitoring setup
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'kubernetes-pods'
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)

---
# Application with monitoring
apiVersion: apps/v1
kind: Deployment
metadata:
  name: monitored-data-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: monitored-data-app
  template:
    metadata:
      labels:
        app: monitored-data-app
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: app
        image: my-registry/data-app:v1.0
        ports:
        - containerPort: 8080
          name: http
        - containerPort: 9090
          name: metrics
        env:
        - name: METRICS_ENABLED
          value: "true"
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
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
```

**Centralized Logging**:
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
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

### 10. How do you manage security in Kubernetes?
**Answer**: Implement RBAC, Pod Security Standards, Network Policies, and secure container practices.

```yaml
# RBAC - Role-Based Access Control
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: data-engineering
  name: data-engineer-role
rules:
- apiGroups: [""]
  resources: ["pods", "services", "configmaps", "secrets"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments", "replicasets"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]
- apiGroups: ["batch"]
  resources: ["jobs", "cronjobs"]
  verbs: ["get", "list", "create", "update", "patch", "delete"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: data-engineer-binding
  namespace: data-engineering
subjects:
- kind: User
  name: data-engineer@company.com
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: data-engineer-role
  apiGroup: rbac.authorization.k8s.io

---
# Service Account for applications
apiVersion: v1
kind: ServiceAccount
metadata:
  name: data-processor-sa
  namespace: data-engineering

---
# Pod Security Standards
apiVersion: v1
kind: Pod
metadata:
  name: secure-data-processor
spec:
  serviceAccountName: data-processor-sa
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault
  containers:
  - name: processor
    image: my-registry/data-processor:v1.0
    securityContext:
      allowPrivilegeEscalation: false
      readOnlyRootFilesystem: true
      capabilities:
        drop:
        - ALL
    volumeMounts:
    - name: tmp-volume
      mountPath: /tmp
    - name: cache-volume
      mountPath: /app/cache
  volumes:
  - name: tmp-volume
    emptyDir: {}
  - name: cache-volume
    emptyDir: {}

---
# Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: data-processor-netpol
  namespace: data-engineering
spec:
  podSelector:
    matchLabels:
      app: data-processor
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: api-gateway
    - podSelector:
        matchLabels:
          app: data-api
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to: []  # Allow DNS
    ports:
    - protocol: UDP
      port: 53
```

This comprehensive set covers Kubernetes fundamentals through advanced security and monitoring concepts with practical data engineering examples.