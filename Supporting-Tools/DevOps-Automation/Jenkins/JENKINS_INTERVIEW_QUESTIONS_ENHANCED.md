# 🔧 Jenkins Interview Questions for Data Engineering (Enhanced)

## 📋 Table of Contents

1. [CI/CD Fundamentals (1-25)](#cicd-fundamentals-1-25)
2. [Data Pipeline Automation (26-50)](#data-pipeline-automation-26-50)
3. [Advanced Features (51-75)](#advanced-features-51-75)
4. [Production & Scaling (76-100)](#production--scaling-76-100)

---

## CI/CD Fundamentals (1-25)

### 1. What is Jenkins and why is it important for data engineering?
**Answer**: Jenkins is an open-source automation server for building CI/CD pipelines.

**Benefits for Data Engineering:**
- **Automated Testing**: Test data pipelines and transformations
- **Deployment Automation**: Deploy data applications consistently
- **Scheduled Jobs**: Run ETL processes on schedule
- **Integration**: Connect with data tools and platforms

```groovy
// Basic Jenkins pipeline for data processing
pipeline {
    agent any
    
    environment {
        PYTHON_PATH = '/usr/bin/python3'
        DATA_ENV = 'production'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/company/data-pipeline.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Data Quality Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    python -m pytest tests/data_quality/ -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Deploy Pipeline') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    source venv/bin/activate
                    python deploy_pipeline.py --env production
                '''
            }
        }
    }
    
    post {
        failure {
            emailext (
                subject: "Pipeline Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Build failed. Check console output at ${env.BUILD_URL}",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

### 2. How do you create Jenkins pipelines for data workflows?
**Answer**: Use declarative or scripted pipelines with data-specific stages.

```groovy
// Data ETL pipeline
pipeline {
    agent {
        docker {
            image 'python:3.9'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }
    
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'prod'],
            description: 'Target environment'
        )
        string(
            name: 'DATA_DATE',
            defaultValue: '',
            description: 'Processing date (YYYY-MM-DD), leave empty for today'
        )
    }
    
    stages {
        stage('Data Extraction') {
            steps {
                script {
                    def dataDate = params.DATA_DATE ?: new Date().format('yyyy-MM-dd')
                    sh """
                        python scripts/extract_data.py \\
                            --date ${dataDate} \\
                            --env ${params.ENVIRONMENT} \\
                            --output /tmp/raw_data/
                    """
                }
            }
        }
        
        stage('Data Transformation') {
            parallel {
                stage('Customer Data') {
                    steps {
                        sh 'python scripts/transform_customers.py --input /tmp/raw_data/ --output /tmp/processed/'
                    }
                }
                stage('Order Data') {
                    steps {
                        sh 'python scripts/transform_orders.py --input /tmp/raw_data/ --output /tmp/processed/'
                    }
                }
                stage('Product Data') {
                    steps {
                        sh 'python scripts/transform_products.py --input /tmp/raw_data/ --output /tmp/processed/'
                    }
                }
            }
        }
        
        stage('Data Validation') {
            steps {
                sh '''
                    python scripts/validate_data.py \\
                        --input /tmp/processed/ \\
                        --rules config/validation_rules.yaml \\
                        --report /tmp/validation_report.json
                '''
                
                script {
                    def report = readJSON file: '/tmp/validation_report.json'
                    if (report.failed_checks > 0) {
                        error("Data validation failed: ${report.failed_checks} checks failed")
                    }
                }
            }
        }
        
        stage('Data Loading') {
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'warehouse-db', usernameVariable: 'DB_USER', passwordVariable: 'DB_PASS')
                ]) {
                    sh '''
                        python scripts/load_data.py \\
                            --input /tmp/processed/ \\
                            --db-host warehouse.company.com \\
                            --db-user $DB_USER \\
                            --db-pass $DB_PASS \\
                            --env ${ENVIRONMENT}
                    '''
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'logs/*.log', allowEmptyArchive: true
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'data_quality_report.html',
                reportName: 'Data Quality Report'
            ])
        }
        success {
            slackSend(
                channel: '#data-engineering',
                color: 'good',
                message: "✅ Data pipeline completed successfully for ${params.DATA_DATE}"
            )
        }
        failure {
            slackSend(
                channel: '#data-engineering',
                color: 'danger',
                message: "❌ Data pipeline failed for ${params.DATA_DATE}. Check ${env.BUILD_URL}"
            )
        }
    }
}
```

## Data Pipeline Automation (26-50)

### 26. How do you implement automated testing for data pipelines?
**Answer**: Create comprehensive test suites for data quality, schema validation, and business logic.

```groovy
// Data testing pipeline
pipeline {
    agent any
    
    stages {
        stage('Unit Tests') {
            steps {
                sh '''
                    # Test individual transformation functions
                    python -m pytest tests/unit/ -v \\
                        --cov=src \\
                        --cov-report=xml \\
                        --cov-report=html
                '''
            }
        }
        
        stage('Integration Tests') {
            steps {
                sh '''
                    # Test end-to-end data flow with sample data
                    python -m pytest tests/integration/ -v \\
                        --tb=short
                '''
            }
        }
        
        stage('Data Quality Tests') {
            steps {
                script {
                    // Run Great Expectations data quality tests
                    sh '''
                        great_expectations checkpoint run daily_data_quality \\
                            --config config/great_expectations.yml
                    '''
                    
                    // Parse results
                    def results = readJSON file: 'great_expectations/uncommitted/validations/results.json'
                    if (!results.success) {
                        error("Data quality tests failed")
                    }
                }
            }
        }
        
        stage('Schema Validation') {
            steps {
                sh '''
                    # Validate schema compatibility
                    python scripts/validate_schema.py \\
                        --source-schema schemas/source.json \\
                        --target-schema schemas/target.json \\
                        --compatibility-check backward
                '''
            }
        }
        
        stage('Performance Tests') {
            steps {
                sh '''
                    # Test pipeline performance with larger datasets
                    python scripts/performance_test.py \\
                        --dataset-size 1000000 \\
                        --max-duration 300 \\
                        --memory-limit 2GB
                '''
            }
        }
    }
    
    post {
        always {
            publishCoverage adapters: [
                coberturaAdapter('coverage.xml')
            ], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
            
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
    }
}
```

### 27. How do you handle different environments in Jenkins?
**Answer**: Use environment-specific configurations and deployment strategies.

```groovy
// Multi-environment deployment pipeline
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t data-pipeline:${BUILD_NUMBER} .'
            }
        }
        
        stage('Deploy to Dev') {
            steps {
                deployToEnvironment('dev')
            }
        }
        
        stage('Integration Tests') {
            steps {
                runIntegrationTests('dev')
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                deployToEnvironment('staging')
            }
        }
        
        stage('Staging Validation') {
            when {
                branch 'main'
            }
            steps {
                runStagingValidation()
            }
        }
        
        stage('Deploy to Production') {
            when {
                allOf {
                    branch 'main'
                    expression { return currentBuild.result != 'FAILURE' }
                }
            }
            steps {
                script {
                    def userInput = input(
                        id: 'Proceed',
                        message: 'Deploy to production?',
                        parameters: [
                            choice(
                                choices: ['Deploy', 'Abort'],
                                description: 'Proceed with production deployment?',
                                name: 'DEPLOY_CHOICE'
                            )
                        ]
                    )
                    
                    if (userInput == 'Deploy') {
                        deployToEnvironment('prod')
                    } else {
                        error('Deployment aborted by user')
                    }
                }
            }
        }
    }
}

def deployToEnvironment(env) {
    withCredentials([
        kubeconfigFile(credentialsId: "${env}-kubeconfig", variable: 'KUBECONFIG')
    ]) {
        sh """
            # Update Kubernetes deployment
            kubectl set image deployment/data-pipeline \\
                data-pipeline=data-pipeline:${BUILD_NUMBER} \\
                --namespace=${env}
            
            # Wait for rollout
            kubectl rollout status deployment/data-pipeline \\
                --namespace=${env} \\
                --timeout=300s
            
            # Update configuration
            kubectl apply -f k8s/${env}/configmap.yaml
        """
    }
}
```

## Advanced Features (51-75)

### 51. How do you implement Jenkins shared libraries for data pipelines?
**Answer**: Create reusable pipeline components for common data engineering tasks.

```groovy
// vars/dataETLPipeline.groovy (Shared Library)
def call(Map config) {
    pipeline {
        agent any
        
        environment {
            DATA_ENV = "${config.environment}"
            SOURCE_SYSTEM = "${config.sourceSystem}"
        }
        
        stages {
            stage('Validate Config') {
                steps {
                    script {
                        validateETLConfig(config)
                    }
                }
            }
            
            stage('Extract Data') {
                steps {
                    script {
                        extractData(config.sources)
                    }
                }
            }
            
            stage('Transform Data') {
                steps {
                    script {
                        transformData(config.transformations)
                    }
                }
            }
            
            stage('Load Data') {
                steps {
                    script {
                        loadData(config.targets)
                    }
                }
            }
            
            stage('Data Quality Checks') {
                steps {
                    script {
                        runDataQualityChecks(config.qualityRules)
                    }
                }
            }
        }
        
        post {
            always {
                script {
                    sendETLNotification(config.notifications, currentBuild.result)
                }
            }
        }
    }
}

// vars/extractData.groovy
def call(sources) {
    sources.each { source ->
        sh """
            python scripts/extractors/${source.type}_extractor.py \\
                --config ${source.config} \\
                --output /tmp/raw/${source.name}/
        """
    }
}

// vars/runDataQualityChecks.groovy
def call(qualityRules) {
    sh """
        python scripts/data_quality_checker.py \\
            --rules ${qualityRules} \\
            --data-path /tmp/processed/ \\
            --report-path /tmp/quality_report.json
    """
    
    def report = readJSON file: '/tmp/quality_report.json'
    if (report.failed_checks > 0) {
        error("Data quality checks failed: ${report.failed_checks} failures")
    }
}

// Usage in Jenkinsfile
@Library('data-engineering-shared-lib') _

dataETLPipeline([
    environment: 'production',
    sourceSystem: 'crm',
    sources: [
        [type: 'database', name: 'customers', config: 'config/db_customers.yaml'],
        [type: 'api', name: 'orders', config: 'config/api_orders.yaml']
    ],
    transformations: [
        'customer_cleansing',
        'order_enrichment',
        'data_aggregation'
    ],
    targets: [
        [type: 'warehouse', config: 'config/warehouse.yaml'],
        [type: 's3', config: 'config/s3_backup.yaml']
    ],
    qualityRules: 'config/quality_rules.yaml',
    notifications: [
        slack: '#data-engineering',
        email: 'data-team@company.com'
    ]
])
```

### 52. How do you implement blue-green deployments for data services?
**Answer**: Use Jenkins to orchestrate blue-green deployments with traffic switching.

```groovy
// Blue-Green deployment pipeline
pipeline {
    agent any
    
    environment {
        BLUE_ENV = 'data-service-blue'
        GREEN_ENV = 'data-service-green'
        CURRENT_ENV = sh(
            script: "kubectl get service data-service-active -o jsonpath='{.spec.selector.version}'",
            returnStdout: true
        ).trim()
    }
    
    stages {
        stage('Determine Target Environment') {
            steps {
                script {
                    env.TARGET_ENV = (env.CURRENT_ENV == 'blue') ? 'green' : 'blue'
                    env.TARGET_DEPLOYMENT = (env.TARGET_ENV == 'blue') ? env.BLUE_ENV : env.GREEN_ENV
                    
                    echo "Current environment: ${env.CURRENT_ENV}"
                    echo "Target environment: ${env.TARGET_ENV}"
                }
            }
        }
        
        stage('Deploy to Target Environment') {
            steps {
                sh """
                    # Update target environment
                    kubectl set image deployment/${TARGET_DEPLOYMENT} \\
                        data-service=data-service:${BUILD_NUMBER} \\
                        --namespace=production
                    
                    # Wait for deployment
                    kubectl rollout status deployment/${TARGET_DEPLOYMENT} \\
                        --namespace=production \\
                        --timeout=300s
                """
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    def healthCheckPassed = false
                    def maxRetries = 10
                    def retryCount = 0
                    
                    while (!healthCheckPassed && retryCount < maxRetries) {
                        try {
                            sh """
                                # Get target service endpoint
                                TARGET_IP=\$(kubectl get service ${TARGET_DEPLOYMENT} -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
                                
                                # Health check
                                curl -f http://\$TARGET_IP:8080/health
                                
                                # Data consistency check
                                python scripts/data_consistency_check.py --endpoint http://\$TARGET_IP:8080
                            """
                            healthCheckPassed = true
                        } catch (Exception e) {
                            retryCount++
                            sleep(30)
                        }
                    }
                    
                    if (!healthCheckPassed) {
                        error("Health check failed after ${maxRetries} attempts")
                    }
                }
            }
        }
        
        stage('Switch Traffic') {
            steps {
                script {
                    def userInput = input(
                        id: 'SwitchTraffic',
                        message: 'Switch traffic to new environment?',
                        parameters: [
                            choice(
                                choices: ['Switch', 'Rollback'],
                                description: 'Action to take',
                                name: 'ACTION'
                            )
                        ]
                    )
                    
                    if (userInput == 'Switch') {
                        sh """
                            # Update active service selector
                            kubectl patch service data-service-active \\
                                -p '{"spec":{"selector":{"version":"${TARGET_ENV}"}}}' \\
                                --namespace=production
                        """
                        
                        echo "Traffic switched to ${env.TARGET_ENV} environment"
                    } else {
                        error("Deployment rolled back by user")
                    }
                }
            }
        }
        
        stage('Cleanup Old Environment') {
            steps {
                script {
                    def oldDeployment = (env.TARGET_ENV == 'blue') ? env.GREEN_ENV : env.BLUE_ENV
                    
                    // Scale down old environment after successful switch
                    sh """
                        kubectl scale deployment ${oldDeployment} --replicas=0 --namespace=production
                    """
                }
            }
        }
    }
    
    post {
        failure {
            script {
                // Automatic rollback on failure
                sh """
                    kubectl patch service data-service-active \\
                        -p '{"spec":{"selector":{"version":"${CURRENT_ENV}"}}}' \\
                        --namespace=production
                """
                
                slackSend(
                    channel: '#data-engineering',
                    color: 'danger',
                    message: "🚨 Blue-Green deployment failed and rolled back to ${env.CURRENT_ENV}"
                )
            }
        }
    }
}
```

## Production & Scaling (76-100)

### 76. How do you scale Jenkins for large data engineering teams?
**Answer**: Implement Jenkins clustering, agent management, and resource optimization.

```groovy
// Jenkins agent configuration for data workloads
pipeline {
    agent {
        label 'data-processing-large'
    }
    
    options {
        // Limit concurrent builds
        disableConcurrentBuilds()
        
        // Build timeout
        timeout(time: 2, unit: 'HOURS')
        
        // Keep builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    stages {
        stage('Resource Allocation') {
            steps {
                script {
                    // Dynamic agent allocation based on workload
                    def requiredMemory = calculateMemoryRequirement()
                    def requiredCPU = calculateCPURequirement()
                    
                    if (requiredMemory > 16) {
                        // Use high-memory agents
                        env.AGENT_LABEL = 'data-processing-highmem'
                    } else if (requiredCPU > 8) {
                        // Use high-CPU agents
                        env.AGENT_LABEL = 'data-processing-highcpu'
                    }
                }
            }
        }
        
        stage('Parallel Processing') {
            parallel {
                stage('Dataset 1') {
                    agent { label 'data-worker' }
                    steps {
                        processDataset('dataset1')
                    }
                }
                stage('Dataset 2') {
                    agent { label 'data-worker' }
                    steps {
                        processDataset('dataset2')
                    }
                }
                stage('Dataset 3') {
                    agent { label 'data-worker' }
                    steps {
                        processDataset('dataset3')
                    }
                }
            }
        }
    }
}

// Jenkins Configuration as Code (JCasC)
jenkins:
  systemMessage: "Data Engineering Jenkins Controller"
  numExecutors: 0  # Use agents only
  
  clouds:
    - kubernetes:
        name: "kubernetes"
        serverUrl: "https://kubernetes.default"
        namespace: "jenkins"
        templates:
          - name: "data-processing-large"
            label: "data-processing-large"
            containers:
              - name: "python"
                image: "python:3.9"
                resourceRequestMemory: "8Gi"
                resourceRequestCpu: "4000m"
                resourceLimitMemory: "16Gi"
                resourceLimitCpu: "8000m"
          - name: "spark-executor"
            label: "spark-executor"
            containers:
              - name: "spark"
                image: "bitnami/spark:3.3"
                resourceRequestMemory: "4Gi"
                resourceRequestCpu: "2000m"
                resourceLimitMemory: "8Gi"
                resourceLimitCpu: "4000m"

credentials:
  system:
    domainCredentials:
      - credentials:
          - usernamePassword:
              scope: GLOBAL
              id: "warehouse-db"
              username: "${WAREHOUSE_DB_USER}"
              password: "${WAREHOUSE_DB_PASS}"
          - string:
              scope: GLOBAL
              id: "slack-token"
              secret: "${SLACK_TOKEN}"
```

---

**Total Questions: 100** | **Coverage: Complete Jenkins for Data Engineering**