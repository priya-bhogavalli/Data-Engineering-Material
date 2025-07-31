# Kubernetes Best Practices for Data Engineering

## Pod and Container Configuration

### Resource Management
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: spark-driver
spec:
  replicas: 1
  selector:
    matchLabels:
      app: spark-driver
  template:
    metadata:
      labels:
        app: spark-driver
    spec:
      containers:
      - name: spark-driver
        image: spark:3.4.0
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: SPARK_MODE
          value: "driver"
```

### Security Context
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-processor
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
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
    - name: tmp-volume
      mountPath: /tmp
  volumes:
  - name: tmp-volume
    emptyDir: {}
```

## Data Pipeline Deployments

### Spark on Kubernetes
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: spark-config
data:
  spark-defaults.conf: |
    spark.kubernetes.container.image=spark:3.4.0
    spark.kubernetes.authenticate.driver.serviceAccountName=spark
    spark.kubernetes.executor.deleteOnTermination=true
    spark.sql.adaptive.enabled=true
    spark.sql.adaptive.coalescePartitions.enabled=true

---
apiVersion: batch/v1
kind: Job
metadata:
  name: spark-etl-job
spec:
  template:
    spec:
      serviceAccountName: spark
      containers:
      - name: spark-submit
        image: spark:3.4.0
        command: ["/opt/spark/bin/spark-submit"]
        args:
        - "--master=k8s://https://kubernetes.default.svc:443"
        - "--deploy-mode=cluster"
        - "--conf=spark.kubernetes.executor.request.cores=1"
        - "--conf=spark.kubernetes.executor.limit.cores=2"
        - "s3a://data-scripts/etl-job.py"
        env:
        - name: AWS_ACCESS_KEY_ID
          valueFrom:
            secretKeyRef:
              name: aws-credentials
              key: access-key-id
      restartPolicy: Never
```

### Airflow on Kubernetes
```yaml
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
        ports:
        - containerPort: 8080
        env:
        - name: AIRFLOW__CORE__EXECUTOR
          value: "KubernetesExecutor"
        - name: AIRFLOW__DATABASE__SQL_ALCHEMY_CONN
          valueFrom:
            secretKeyRef:
              name: airflow-secrets
              key: database-url
        volumeMounts:
        - name: dags-volume
          mountPath: /opt/airflow/dags
      volumes:
      - name: dags-volume
        persistentVolumeClaim:
          claimName: airflow-dags-pvc
```

## Storage and Persistence

### Persistent Volumes
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-storage-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 100Gi
  storageClassName: fast-ssd

---
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
        volumeMounts:
        - name: kafka-storage
          mountPath: /var/lib/kafka/data
  volumeClaimTemplates:
  - metadata:
      name: kafka-storage
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 50Gi
```

### ConfigMaps and Secrets
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: database-credentials
type: Opaque
data:
  username: cG9zdGdyZXM=  # base64 encoded
  password: cGFzc3dvcmQ=  # base64 encoded

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  database.properties: |
    host=postgres-service
    port=5432
    database=datawarehouse
  logging.conf: |
    level=INFO
    format=json
```

## Networking and Services

### Service Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP

---
apiVersion: v1
kind: Service
metadata:
  name: airflow-webserver-service
spec:
  selector:
    app: airflow-webserver
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
```

### Network Policies
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: data-pipeline-network-policy
spec:
  podSelector:
    matchLabels:
      tier: data-processing
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: airflow
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

## Monitoring and Observability

### Prometheus Monitoring
```yaml
apiVersion: v1
kind: ServiceMonitor
metadata:
  name: spark-metrics
spec:
  selector:
    matchLabels:
      app: spark-driver
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics

---
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: data-pipeline-alerts
spec:
  groups:
  - name: spark.rules
    rules:
    - alert: SparkJobFailed
      expr: spark_job_failed_total > 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Spark job has failed"
```

### Logging Configuration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush         1
        Log_Level     info
        Daemon        off
        Parsers_File  parsers.conf

    [INPUT]
        Name              tail
        Path              /var/log/containers/*spark*.log
        Parser            docker
        Tag               spark.*
        Refresh_Interval  5

    [OUTPUT]
        Name  es
        Match spark.*
        Host  elasticsearch.logging.svc.cluster.local
        Port  9200
        Index spark-logs
```

## Scaling and Performance

### Horizontal Pod Autoscaler
```yaml
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

### Cluster Autoscaler
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cluster-autoscaler
  namespace: kube-system
spec:
  template:
    spec:
      containers:
      - image: k8s.gcr.io/autoscaling/cluster-autoscaler:v1.21.0
        name: cluster-autoscaler
        command:
        - ./cluster-autoscaler
        - --v=4
        - --stderrthreshold=info
        - --cloud-provider=aws
        - --skip-nodes-with-local-storage=false
        - --expander=least-waste
        - --node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/data-cluster
```

## Security Best Practices

### RBAC Configuration
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: spark-service-account
  namespace: data-processing

---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: spark-role
  namespace: data-processing
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["create", "get", "list", "delete"]
- apiGroups: [""]
  resources: ["services"]
  verbs: ["create", "get", "delete"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: spark-role-binding
  namespace: data-processing
subjects:
- kind: ServiceAccount
  name: spark-service-account
  namespace: data-processing
roleRef:
  kind: Role
  name: spark-role
  apiGroup: rbac.authorization.k8s.io
```

### Pod Security Standards
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: data-processing
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```