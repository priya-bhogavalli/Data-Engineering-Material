# Kubernetes Key Concepts

## 1. Kubernetes Architecture
**What is Kubernetes**: An open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.

**Cluster Components**:
```
┌─────────────────────────────────────────────────────────┐
│                   Control Plane                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │   API       │ │   etcd      │ │   Scheduler     │   │
│  │   Server    │ │  (Storage)  │ │                 │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Controller Manager                      │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────┐
│                    Worker Nodes                        │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────┐   │
│  │   kubelet   │ │ kube-proxy  │ │   Container     │   │
│  │             │ │             │ │   Runtime       │   │
│  └─────────────┘ └─────────────┘ └─────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  Pods                           │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Key Components**:
- **API Server**: Central management entity, REST API endpoint
- **etcd**: Distributed key-value store for cluster state
- **Scheduler**: Assigns pods to nodes
- **Controller Manager**: Runs controller processes
- **kubelet**: Node agent that manages pods
- **kube-proxy**: Network proxy for services

## 2. Pods
**What they are**: Smallest deployable units containing one or more containers.

**Pod Manifest**:
```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: data-processor
  labels:
    app: data-processing
    tier: worker
  annotations:
    description: "Data processing pod"
spec:
  containers:
  - name: processor
    image: python:3.9-slim
    command: ["python", "process_data.py"]
    env:
    - name: DATABASE_URL
      value: "postgresql://db:5432/datadb"
    - name: REDIS_URL
      valueFrom:
        secretKeyRef:
          name: redis-secret
          key: url
    resources:
      requests:
        memory: "256Mi"
        cpu: "250m"
      limits:
        memory: "512Mi"
        cpu: "500m"
    volumeMounts:
    - name: data-volume
      mountPath: /data
    - name: config-volume
      mountPath: /config
  volumes:
  - name: data-volume
    persistentVolumeClaim:
      claimName: data-pvc
  - name: config-volume
    configMap:
      name: app-config
  restartPolicy: Always
  nodeSelector:
    disktype: ssd
```

**Multi-Container Pod**:
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-app
spec:
  containers:
  # Main application container
  - name: app
    image: nginx:1.21
    ports:
    - containerPort: 80
    volumeMounts:
    - name: shared-data
      mountPath: /usr/share/nginx/html
  
  # Sidecar container for log processing
  - name: log-processor
    image: fluent/fluent-bit:1.8
    volumeMounts:
    - name: shared-data
      mountPath: /var/log
    - name: fluent-config
      mountPath: /fluent-bit/etc
  
  volumes:
  - name: shared-data
    emptyDir: {}
  - name: fluent-config
    configMap:
      name: fluent-config
```

## 3. Deployments
**What they are**: Manage replica sets and provide declarative updates for pods.

**Deployment Manifest**:
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-api
  labels:
    app: data-api
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
  selector:
    matchLabels:
      app: data-api
  template:
    metadata:
      labels:
        app: data-api
        version: v1.2.0
    spec:
      containers:
      - name: api
        image: myregistry/data-api:v1.2.0
        ports:
        - containerPort: 8080
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: log_level
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
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

**Deployment Operations**:
```bash
# Create deployment
kubectl apply -f deployment.yaml

# Scale deployment
kubectl scale deployment data-api --replicas=5

# Update image (rolling update)
kubectl set image deployment/data-api api=myregistry/data-api:v1.3.0

# Check rollout status
kubectl rollout status deployment/data-api

# Rollback deployment
kubectl rollout undo deployment/data-api

# View rollout history
kubectl rollout history deployment/data-api
```

## 4. Services
**What they are**: Stable network endpoints for accessing pods.

**Service Types**:

### ClusterIP (Internal)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: database-service
spec:
  type: ClusterIP
  selector:
    app: database
  ports:
  - port: 5432
    targetPort: 5432
    protocol: TCP
```

### NodePort (External Access)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-service
spec:
  type: NodePort
  selector:
    app: web-app
  ports:
  - port: 80
    targetPort: 8080
    nodePort: 30080
```

### LoadBalancer (Cloud Provider)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: LoadBalancer
  selector:
    app: data-api
  ports:
  - port: 443
    targetPort: 8080
    protocol: TCP
```

### Headless Service
```yaml
apiVersion: v1
kind: Service
metadata:
  name: database-headless
spec:
  clusterIP: None  # Headless service
  selector:
    app: database
  ports:
  - port: 5432
    targetPort: 5432
```

## 5. ConfigMaps and Secrets
**ConfigMaps**: Store non-sensitive configuration data.

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  # Key-value pairs
  log_level: "INFO"
  max_connections: "100"
  
  # File-like keys
  database.properties: |
    host=db.example.com
    port=5432
    database=myapp
    
  nginx.conf: |
    server {
        listen 80;
        server_name localhost;
        location / {
            proxy_pass http://backend:8080;
        }
    }
```

**Secrets**: Store sensitive data (base64 encoded).

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
type: Opaque
data:
  username: YWRtaW4=  # admin (base64)
  password: cGFzc3dvcmQ=  # password (base64)
  url: cG9zdGdyZXNxbDovL2FkbWluOnBhc3N3b3JkQGRiOjU0MzIvbXlkYg==

---
# TLS Secret
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: LS0tLS1CRUdJTi... # Certificate
  tls.key: LS0tLS1CRUdJTi... # Private key
```

**Using ConfigMaps and Secrets**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        
        # Environment variables from ConfigMap
        envFrom:
        - configMapRef:
            name: app-config
        
        # Specific environment variables
        env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: password
        
        # Mount as volumes
        volumeMounts:
        - name: config-volume
          mountPath: /etc/config
        - name: secret-volume
          mountPath: /etc/secrets
          readOnly: true
      
      volumes:
      - name: config-volume
        configMap:
          name: app-config
      - name: secret-volume
        secret:
          secretName: db-secret
```

## 6. Persistent Volumes
**Storage Classes**:
```yaml
# storageclass.yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
reclaimPolicy: Delete
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer
```

**Persistent Volume Claim**:
```yaml
# pvc.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data-pvc
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd
  resources:
    requests:
      storage: 100Gi
```

**StatefulSet with Persistent Storage**:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
spec:
  serviceName: database-headless
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
          value: mydb
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
        - name: data
          mountPath: /var/lib/postgresql/data
        ports:
        - containerPort: 5432
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

## 7. Ingress
**What it is**: Manages external access to services, typically HTTP/HTTPS.

**Ingress Controller** (NGINX):
```yaml
# Install NGINX Ingress Controller
apiVersion: v1
kind: Namespace
metadata:
  name: ingress-nginx

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-ingress-controller
  namespace: ingress-nginx
spec:
  replicas: 2
  selector:
    matchLabels:
      app: nginx-ingress
  template:
    metadata:
      labels:
        app: nginx-ingress
    spec:
      containers:
      - name: nginx-ingress-controller
        image: k8s.gcr.io/ingress-nginx/controller:v1.8.1
        args:
        - /nginx-ingress-controller
        - --configmap=$(POD_NAMESPACE)/nginx-configuration
```

**Ingress Resource**:
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: data-platform-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.dataplatform.com
    - dashboard.dataplatform.com
    secretName: tls-secret
  rules:
  - host: api.dataplatform.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: data-api-service
            port:
              number: 80
  - host: dashboard.dataplatform.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: dashboard-service
            port:
              number: 80
```

## 8. Jobs and CronJobs
**Job**: Run pods to completion.

```yaml
# job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: data-migration
spec:
  completions: 1
  parallelism: 1
  backoffLimit: 3
  template:
    spec:
      containers:
      - name: migrator
        image: myregistry/data-migrator:v1.0
        command: ["python", "migrate.py"]
        env:
        - name: SOURCE_DB
          valueFrom:
            secretKeyRef:
              name: source-db-secret
              key: url
        - name: TARGET_DB
          valueFrom:
            secretKeyRef:
              name: target-db-secret
              key: url
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      restartPolicy: Never
```

**CronJob**: Scheduled jobs.

```yaml
# cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-etl
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: etl-processor
            image: myregistry/etl-processor:v2.1
            command: ["python", "daily_etl.py"]
            env:
            - name: ETL_DATE
              value: "{{ .Values.etl_date }}"
            - name: S3_BUCKET
              value: "data-lake-bucket"
            volumeMounts:
            - name: etl-config
              mountPath: /config
          volumes:
          - name: etl-config
            configMap:
              name: etl-config
          restartPolicy: OnFailure
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
```

## 9. Namespaces and RBAC
**Namespaces**: Virtual clusters for resource isolation.

```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: data-engineering
  labels:
    team: data-engineering
    environment: production

---
apiVersion: v1
kind: Namespace
metadata:
  name: data-science
  labels:
    team: data-science
    environment: production
```

**Role-Based Access Control (RBAC)**:

```yaml
# rbac.yaml
# Service Account
apiVersion: v1
kind: ServiceAccount
metadata:
  name: data-engineer
  namespace: data-engineering

---
# Role (namespace-scoped)
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: data-engineering
  name: pod-manager
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "list", "create", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "create", "update", "patch"]

---
# RoleBinding
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
  name: pod-manager
  apiGroup: rbac.authorization.k8s.io

---
# ClusterRole (cluster-wide)
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: node-reader
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "list"]

---
# ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: node-reader-binding
subjects:
- kind: ServiceAccount
  name: data-engineer
  namespace: data-engineering
roleRef:
  kind: ClusterRole
  name: node-reader
  apiGroup: rbac.authorization.k8s.io
```

## 10. Monitoring and Observability
**Resource Quotas**:
```yaml
# resourcequota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: data-engineering-quota
  namespace: data-engineering
spec:
  hard:
    requests.cpu: "10"
    requests.memory: 20Gi
    limits.cpu: "20"
    limits.memory: 40Gi
    persistentvolumeclaims: "10"
    pods: "20"
    services: "10"
```

**Horizontal Pod Autoscaler**:
```yaml
# hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: data-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: data-api
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

**Monitoring with Prometheus**:
```yaml
# servicemonitor.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: data-api-monitor
spec:
  selector:
    matchLabels:
      app: data-api
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

**Common kubectl Commands**:
```bash
# Cluster info
kubectl cluster-info
kubectl get nodes

# Pods
kubectl get pods -A
kubectl describe pod <pod-name>
kubectl logs <pod-name> -f
kubectl exec -it <pod-name> -- /bin/bash

# Deployments
kubectl get deployments
kubectl describe deployment <deployment-name>
kubectl scale deployment <deployment-name> --replicas=5

# Services
kubectl get services
kubectl port-forward service/<service-name> 8080:80

# Debug
kubectl top nodes
kubectl top pods
kubectl get events --sort-by=.metadata.creationTimestamp
```