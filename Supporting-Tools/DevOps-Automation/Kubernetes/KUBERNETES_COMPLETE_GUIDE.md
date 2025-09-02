# Kubernetes Complete Guide for Data Engineering

## 🎯 What is Kubernetes?

Kubernetes (K8s) is an **open-source container orchestration platform** that automates deployment, scaling, and management of containerized applications. It's essential for data engineering teams building scalable, resilient data pipelines and analytics platforms.

### Key Characteristics
- **Container Orchestration**: Manages containerized applications at scale
- **Self-healing**: Automatically restarts failed containers and replaces nodes
- **Horizontal Scaling**: Scales applications up/down based on demand
- **Service Discovery**: Built-in load balancing and service discovery
- **Declarative Configuration**: Infrastructure as code approach

## 💾 Core Concepts

### 1. Basic Architecture
```yaml
# Kubernetes Cluster Architecture
Master Node (Control Plane):
  - API Server
  - etcd (Key-value store)
  - Scheduler
  - Controller Manager

Worker Nodes:
  - kubelet (Node agent)
  - kube-proxy (Network proxy)
  - Container Runtime (Docker/containerd)
  - Pods (Running containers)
```

### 2. Essential Resources
```yaml
# Pod - Basic deployment unit
apiVersion: v1
kind: Pod
metadata:
  name: data-processor
  labels:
    app: data-processing
spec:
  containers:
  - name: processor
    image: python:3.9
    command: ["python", "process_data.py"]
    resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
      limits:
        memory: "1Gi"
        cpu: "500m"
    env:
    - name: DATABASE_URL
      valueFrom:
        secretKeyRef:
          name: db-secret
          key: url

---
# Deployment - Manages replica sets
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-api
  template:
    metadata:
      labels:
        app: data-api
    spec:
      containers:
      - name: api
        image: data-api:v1.0
        ports:
        - containerPort: 8080
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
# Service - Network access to pods
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
  type: LoadBalancer

---
# ConfigMap - Configuration data
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database.properties: |
    host=postgres.default.svc.cluster.local
    port=5432
    database=datawarehouse
  log_level: "INFO"
  batch_size: "1000"

---
# Secret - Sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: ZGF0YWVuZw==  # dataeng (base64)
  password: c2VjdXJlcGFzcw==  # securepass (base64)
  url: cG9zdGdyZXNxbDovL2RhdGFlbmc6c2VjdXJlcGFzc0Bwb3N0Z3Jlcy5kZWZhdWx0LnN2Yy5jbHVzdGVyLmxvY2FsOjU0MzIvZGF0YXdhcmVob3VzZQ==
```

## 🔧 Data Engineering Use Cases

### 1. Spark on Kubernetes
```yaml
# Spark Application on Kubernetes
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark-service-account
  namespace: data-processing

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: spark-cluster-role-binding
subjects:
- kind: ServiceAccount
  name: spark-service-account
  namespace: data-processing
roleRef:
  kind: ClusterRole
  name: edit
  apiGroup: rbac.authorization.k8s.io

---
apiVersion: batch/v1
kind: Job
metadata:
  name: spark-etl-job
  namespace: data-processing
spec:
  template:
    spec:
      serviceAccountName: spark-service-account
      containers:
      - name: spark-driver
        image: apache/spark:3.4.0
        command:
        - /opt/spark/bin/spark-submit
        - --master
        - k8s://https://kubernetes.default.svc:443
        - --deploy-mode
        - cluster
        - --name
        - etl-pipeline
        - --conf
        - spark.executor.instances=3
        - --conf
        - spark.executor.memory=2g
        - --conf
        - spark.executor.cores=2
        - --conf
        - spark.kubernetes.container.image=apache/spark:3.4.0
        - --conf
        - spark.kubernetes.authenticate.driver.serviceAccountName=spark-service-account
        - --conf
        - spark.kubernetes.namespace=data-processing
        - /opt/spark/examples/src/main/python/pi.py
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      restartPolicy: Never
  backoffLimit: 3
```

### 2. Airflow on Kubernetes
```yaml
# Airflow Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airflow-webserver
  namespace: airflow
spec:
  replicas: 1
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
        env:
        - name: AIRFLOW__CORE__EXECUTOR
          value: "KubernetesExecutor"
        - name: AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
          valueFrom:
            secretKeyRef:
              name: airflow-secrets
              key: sql_alchemy_conn
        - name: AIRFLOW__CORE__FERNET_KEY
          valueFrom:
            secretKeyRef:
              name: airflow-secrets
              key: fernet_key
        volumeMounts:
        - name: dags-volume
          mountPath: /opt/airflow/dags
        - name: logs-volume
          mountPath: /opt/airflow/logs
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: dags-volume
        persistentVolumeClaim:
          claimName: airflow-dags-pvc
      - name: logs-volume
        persistentVolumeClaim:
          claimName: airflow-logs-pvc

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: airflow-scheduler
  namespace: airflow
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
        - name: AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
          valueFrom:
            secretKeyRef:
              name: airflow-secrets
              key: sql_alchemy_conn
        volumeMounts:
        - name: dags-volume
          mountPath: /opt/airflow/dags
        - name: logs-volume
          mountPath: /opt/airflow/logs
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: dags-volume
        persistentVolumeClaim:
          claimName: airflow-dags-pvc
      - name: logs-volume
        persistentVolumeClaim:
          claimName: airflow-logs-pvc

---
# Persistent Volume Claims
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: airflow-dags-pvc
  namespace: airflow
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 10Gi
  storageClassName: nfs-storage

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: airflow-logs-pvc
  namespace: airflow
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 50Gi
  storageClassName: nfs-storage
```

### 3. Data Pipeline with CronJobs
```yaml
# Daily ETL CronJob
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-etl-pipeline
  namespace: data-processing
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: etl-processor
            image: data-pipeline:latest
            command:
            - python
            - /app/daily_etl.py
            env:
            - name: EXECUTION_DATE
              value: "{{ .Values.executionDate }}"
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-credentials
                  key: url
            - name: S3_BUCKET
              valueFrom:
                configMapKeyRef:
                  name: etl-config
                  key: s3_bucket
            resources:
              requests:
                memory: "2Gi"
                cpu: "1000m"
              limits:
                memory: "4Gi"
                cpu: "2000m"
            volumeMounts:
            - name: temp-storage
              mountPath: /tmp/data
          volumes:
          - name: temp-storage
            emptyDir:
              sizeLimit: 10Gi
          restartPolicy: OnFailure
      backoffLimit: 3
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1

---
# Real-time Stream Processing
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kafka-consumer
  namespace: streaming
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
        image: stream-processor:latest
        env:
        - name: KAFKA_BROKERS
          value: "kafka-cluster:9092"
        - name: CONSUMER_GROUP
          value: "data-processing-group"
        - name: TOPICS
          value: "user-events,transaction-events"
        - name: OUTPUT_TOPIC
          value: "processed-events"
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
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
          initialDelaySeconds: 10
          periodSeconds: 5
```

## ⚡ Performance and Scaling

### 1. Horizontal Pod Autoscaler
```yaml
# HPA for data processing workloads
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
        averageValue: "1000"
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
  name: data-api-vpa
  namespace: data-processing
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-api
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: api
      maxAllowed:
        cpu: 2
        memory: 4Gi
      minAllowed:
        cpu: 100m
        memory: 128Mi
```

### 2. Resource Management
```yaml
# Resource Quotas
apiVersion: v1
kind: ResourceQuota
metadata:
  name: data-processing-quota
  namespace: data-processing
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    persistentvolumeclaims: "10"
    pods: "50"

---
# Limit Ranges
apiVersion: v1
kind: LimitRange
metadata:
  name: data-processing-limits
  namespace: data-processing
spec:
  limits:
  - default:
      cpu: "500m"
      memory: "1Gi"
    defaultRequest:
      cpu: "100m"
      memory: "256Mi"
    type: Container
  - max:
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "50m"
      memory: "128Mi"
    type: Container

---
# Pod Disruption Budget
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: data-api-pdb
  namespace: data-processing
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: data-api
```

## 🔒 Security and Monitoring

### 1. Security Configuration
```yaml
# Network Policy
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: data-processing-network-policy
  namespace: data-processing
spec:
  podSelector:
    matchLabels:
      tier: data-processing
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
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS
    - protocol: TCP
      port: 53   # DNS
    - protocol: UDP
      port: 53   # DNS

---
# Pod Security Policy
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
```

### 2. Monitoring and Observability
```yaml
# ServiceMonitor for Prometheus
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: data-api-metrics
  namespace: data-processing
spec:
  selector:
    matchLabels:
      app: data-api
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics

---
# Grafana Dashboard ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: data-pipeline-dashboard
  namespace: monitoring
data:
  dashboard.json: |
    {
      "dashboard": {
        "title": "Data Pipeline Metrics",
        "panels": [
          {
            "title": "Pod CPU Usage",
            "type": "graph",
            "targets": [
              {
                "expr": "rate(container_cpu_usage_seconds_total{namespace=\"data-processing\"}[5m])"
              }
            ]
          },
          {
            "title": "Pod Memory Usage",
            "type": "graph",
            "targets": [
              {
                "expr": "container_memory_usage_bytes{namespace=\"data-processing\"}"
              }
            ]
          }
        ]
      }
    }
```

## 🎯 Best Practices Summary

### 1. Resource Management Best Practices
- **Set Resource Requests and Limits**: Always define CPU and memory requirements
- **Use Horizontal Pod Autoscaler**: Scale based on metrics like CPU, memory, or custom metrics
- **Implement Resource Quotas**: Prevent resource exhaustion at namespace level
- **Use Pod Disruption Budgets**: Ensure availability during updates

### 2. Configuration Best Practices
- **Use ConfigMaps and Secrets**: Separate configuration from container images
- **Implement Health Checks**: Define liveness and readiness probes
- **Use Namespaces**: Organize resources and implement isolation
- **Label Everything**: Use consistent labeling for resource management

### 3. Security Best Practices
- **Run as Non-root**: Use security contexts to run containers as non-root users
- **Implement Network Policies**: Control network traffic between pods
- **Use RBAC**: Implement role-based access control
- **Scan Images**: Regularly scan container images for vulnerabilities

### 4. Operational Best Practices
- **Use Declarative Configuration**: Manage resources with YAML manifests
- **Implement GitOps**: Version control your Kubernetes configurations
- **Monitor Everything**: Set up comprehensive monitoring and alerting
- **Plan for Disaster Recovery**: Implement backup and recovery strategies

This guide provides essential Kubernetes knowledge for data engineering. Focus on understanding pod management, scaling strategies, and security practices for building robust data platforms.