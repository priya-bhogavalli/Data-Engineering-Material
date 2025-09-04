# Jenkins Extended Interview Questions & Answers

## 📋 Table of Contents
1. [Advanced Pipeline Development](#advanced-pipeline-development)
2. [Security & Access Control](#security--access-control)
3. [Scalability & Performance](#scalability--performance)
4. [Integration & Ecosystem](#integration--ecosystem)
5. [Monitoring & Troubleshooting](#monitoring--troubleshooting)
6. [Best Practices & Governance](#best-practices--governance)

---

## Advanced Pipeline Development

### 1. How do you implement complex Jenkins pipelines with parallel execution and conditional logic?

**Answer:**
Advanced pipeline patterns for complex workflows:

**Parallel Execution:**
```groovy
pipeline {
    agent any
    
    stages {
        stage('Parallel Testing') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        sh 'mvn test'
                        publishTestResults testResultsPattern: 'target/surefire-reports/*.xml'
                    }
                }
                stage('Integration Tests') {
                    steps {
                        sh 'mvn integration-test'
                        publishTestResults testResultsPattern: 'target/failsafe-reports/*.xml'
                    }
                }
                stage('Security Scan') {
                    steps {
                        sh 'sonar-scanner'
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }
        
        stage('Conditional Deployment') {
            when {
                anyOf {
                    branch 'main'
                    branch 'release/*'
                }
            }
            parallel {
                stage('Deploy to Staging') {
                    when { branch 'main' }
                    steps {
                        deployToEnvironment('staging')
                    }
                }
                stage('Deploy to Production') {
                    when { 
                        allOf {
                            branch 'release/*'
                            expression { params.DEPLOY_TO_PROD == true }
                        }
                    }
                    steps {
                        input message: 'Deploy to production?', ok: 'Deploy'
                        deployToEnvironment('production')
                    }
                }
            }
        }
    }
}

def deployToEnvironment(environment) {
    script {
        def deploymentConfig = [
            staging: [
                namespace: 'staging',
                replicas: 2,
                resources: [cpu: '500m', memory: '1Gi']
            ],
            production: [
                namespace: 'production',
                replicas: 5,
                resources: [cpu: '1000m', memory: '2Gi']
            ]
        ]
        
        def config = deploymentConfig[environment]
        
        sh """
            helm upgrade --install myapp ./helm-chart \\
                --namespace ${config.namespace} \\
                --set replicaCount=${config.replicas} \\
                --set resources.requests.cpu=${config.resources.cpu} \\
                --set resources.requests.memory=${config.resources.memory}
        """
    }
}
```

### 2. How do you implement Jenkins shared libraries for code reuse?

**Answer:**
Shared libraries promote code reuse and standardization:

**Library Structure:**
```
jenkins-shared-library/
├── vars/
│   ├── buildAndDeploy.groovy
│   ├── notifySlack.groovy
│   └── runTests.groovy
├── src/
│   └── com/
│       └── company/
│           └── jenkins/
│               ├── Docker.groovy
│               └── Kubernetes.groovy
└── resources/
    ├── templates/
    │   └── deployment.yaml
    └── scripts/
        └── deploy.sh
```

**Shared Library Implementation:**
```groovy
// vars/buildAndDeploy.groovy
def call(Map config) {
    pipeline {
        agent any
        
        environment {
            DOCKER_REGISTRY = config.registry ?: 'docker.company.com'
            APP_NAME = config.appName
            NAMESPACE = config.namespace ?: 'default'
        }
        
        stages {
            stage('Build') {
                steps {
                    script {
                        def docker = new com.company.jenkins.Docker()
                        def image = docker.buildImage(APP_NAME, env.BUILD_NUMBER)
                        docker.pushImage(image, DOCKER_REGISTRY)
                    }
                }
            }
            
            stage('Test') {
                steps {
                    runTests(config.testConfig)
                }
            }
            
            stage('Deploy') {
                steps {
                    script {
                        def k8s = new com.company.jenkins.Kubernetes()
                        k8s.deploy(APP_NAME, NAMESPACE, env.BUILD_NUMBER)
                    }
                }
            }
        }
        
        post {
            always {
                notifySlack(
                    channel: config.slackChannel,
                    status: currentBuild.result
                )
            }
        }
    }
}

// src/com/company/jenkins/Docker.groovy
package com.company.jenkins

class Docker implements Serializable {
    def script
    
    Docker(script) {
        this.script = script
    }
    
    def buildImage(appName, buildNumber) {
        def imageName = "${appName}:${buildNumber}"
        script.sh "docker build -t ${imageName} ."
        return imageName
    }
    
    def pushImage(imageName, registry) {
        script.sh """
            docker tag ${imageName} ${registry}/${imageName}
            docker push ${registry}/${imageName}
        """
    }
    
    def scanImage(imageName) {
        script.sh "trivy image ${imageName}"
    }
}
```

**Using Shared Library:**
```groovy
@Library('jenkins-shared-library@main') _

buildAndDeploy([
    appName: 'my-microservice',
    registry: 'docker.company.com',
    namespace: 'production',
    slackChannel: '#deployments',
    testConfig: [
        unitTests: true,
        integrationTests: true,
        securityScan: true
    ]
])
```

### 3. How do you implement blue-green deployments with Jenkins?

**Answer:**
Blue-green deployment strategy for zero-downtime deployments:

**Blue-Green Pipeline:**
```groovy
pipeline {
    agent any
    
    parameters {
        choice(
            name: 'DEPLOYMENT_STRATEGY',
            choices: ['blue-green', 'rolling', 'canary'],
            description: 'Deployment strategy'
        )
        booleanParam(
            name: 'SKIP_TESTS',
            defaultValue: false,
            description: 'Skip test execution'
        )
    }
    
    environment {
        APP_NAME = 'my-app'
        CURRENT_COLOR = sh(
            script: "kubectl get service ${APP_NAME} -o jsonpath='{.spec.selector.version}'",
            returnStdout: true
        ).trim()
        NEW_COLOR = CURRENT_COLOR == 'blue' ? 'green' : 'blue'
    }
    
    stages {
        stage('Determine Deployment Color') {
            steps {
                script {
                    echo "Current color: ${CURRENT_COLOR}"
                    echo "New color: ${NEW_COLOR}"
                }
            }
        }
        
        stage('Deploy to New Environment') {
            steps {
                script {
                    sh """
                        helm upgrade --install ${APP_NAME}-${NEW_COLOR} ./helm-chart \\
                            --set image.tag=${BUILD_NUMBER} \\
                            --set color=${NEW_COLOR} \\
                            --set service.enabled=false \\
                            --namespace production
                    """
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    def healthCheckUrl = "http://${APP_NAME}-${NEW_COLOR}.production.svc.cluster.local:8080/health"
                    
                    timeout(time: 5, unit: 'MINUTES') {
                        waitUntil {
                            script {
                                def response = sh(
                                    script: "curl -s -o /dev/null -w '%{http_code}' ${healthCheckUrl}",
                                    returnStdout: true
                                ).trim()
                                return response == '200'
                            }
                        }
                    }
                }
            }
        }
        
        stage('Smoke Tests') {
            when { not { params.SKIP_TESTS } }
            steps {
                script {
                    sh """
                        newman run tests/smoke-tests.postman_collection.json \\
                            --env-var baseUrl=http://${APP_NAME}-${NEW_COLOR}.production.svc.cluster.local:8080
                    """
                }
            }
        }
        
        stage('Switch Traffic') {
            steps {
                input message: 'Switch traffic to new version?', ok: 'Switch'
                
                script {
                    sh """
                        kubectl patch service ${APP_NAME} \\
                            -p '{"spec":{"selector":{"version":"${NEW_COLOR}"}}}'
                    """
                }
            }
        }
        
        stage('Cleanup Old Environment') {
            steps {
                script {
                    sh "helm uninstall ${APP_NAME}-${CURRENT_COLOR} --namespace production"
                }
            }
        }
    }
    
    post {
        failure {
            script {
                // Rollback on failure
                sh """
                    kubectl patch service ${APP_NAME} \\
                        -p '{"spec":{"selector":{"version":"${CURRENT_COLOR}"}}}'
                    helm uninstall ${APP_NAME}-${NEW_COLOR} --namespace production
                """
            }
        }
    }
}
```

---

## Security & Access Control

### 4. How do you implement comprehensive Jenkins security?

**Answer:**
Multi-layered security approach:

**Authentication and Authorization:**
```groovy
// Security configuration (Jenkins Configuration as Code)
jenkins:
  securityRealm:
    ldap:
      configurations:
        - server: "ldap://ldap.company.com:389"
          rootDN: "dc=company,dc=com"
          userSearchBase: "ou=users"
          userSearch: "uid={0}"
          groupSearchBase: "ou=groups"
          groupSearchFilter: "member={0}"
          
  authorizationStrategy:
    roleBased:
      roles:
        global:
          - name: "admin"
            description: "Jenkins administrators"
            permissions:
              - "Overall/Administer"
            assignments:
              - "jenkins-admins"
          - name: "developer"
            description: "Developers"
            permissions:
              - "Overall/Read"
              - "Job/Build"
              - "Job/Cancel"
              - "Job/Read"
            assignments:
              - "developers"
        items:
          - name: "production-deployer"
            pattern: "production-.*"
            permissions:
              - "Job/Build"
              - "Job/Cancel"
              - "Job/Read"
            assignments:
              - "devops-team"
```

**Secrets Management:**
```groovy
pipeline {
    agent any
    
    environment {
        // Use Jenkins credentials
        DB_PASSWORD = credentials('database-password')
        API_KEY = credentials('external-api-key')
        
        // Use external secret management
        VAULT_ADDR = 'https://vault.company.com'
        VAULT_NAMESPACE = 'production'
    }
    
    stages {
        stage('Retrieve Secrets') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'vault-token', variable: 'VAULT_TOKEN')
                    ]) {
                        // Retrieve secrets from HashiCorp Vault
                        def secrets = sh(
                            script: """
                                vault kv get -format=json secret/myapp | jq -r '.data.data'
                            """,
                            returnStdout: true
                        ).trim()
                        
                        def secretsJson = readJSON text: secrets
                        env.DATABASE_URL = secretsJson.database_url
                        env.REDIS_PASSWORD = secretsJson.redis_password
                    }
                }
            }
        }
        
        stage('Deploy with Secrets') {
            steps {
                script {
                    sh """
                        kubectl create secret generic app-secrets \\
                            --from-literal=database-url="\${DATABASE_URL}" \\
                            --from-literal=redis-password="\${REDIS_PASSWORD}" \\
                            --dry-run=client -o yaml | kubectl apply -f -
                    """
                }
            }
        }
    }
}
```

### 5. How do you implement Jenkins pipeline security scanning?

**Answer:**
Integrated security scanning in CI/CD pipeline:

**Security Scanning Pipeline:**
```groovy
pipeline {
    agent any
    
    tools {
        maven 'Maven-3.8'
        jdk 'JDK-11'
    }
    
    stages {
        stage('Code Quality & Security') {
            parallel {
                stage('SAST - SonarQube') {
                    steps {
                        withSonarQubeEnv('SonarQube') {
                            sh 'mvn sonar:sonar'
                        }
                        
                        timeout(time: 10, unit: 'MINUTES') {
                            waitForQualityGate abortPipeline: true
                        }
                    }
                }
                
                stage('Dependency Check') {
                    steps {
                        sh 'mvn org.owasp:dependency-check-maven:check'
                        
                        publishHTML([
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: 'target',
                            reportFiles: 'dependency-check-report.html',
                            reportName: 'OWASP Dependency Check'
                        ])
                    }
                }
                
                stage('License Check') {
                    steps {
                        sh 'mvn license:check'
                    }
                }
            }
        }
        
        stage('Build & Package') {
            steps {
                sh 'mvn clean package -DskipTests'
                
                script {
                    def image = docker.build("${APP_NAME}:${BUILD_NUMBER}")
                    docker.withRegistry('https://registry.company.com', 'docker-registry-credentials') {
                        image.push()
                        image.push('latest')
                    }
                }
            }
        }
        
        stage('Container Security Scan') {
            steps {
                script {
                    // Trivy container scanning
                    sh """
                        trivy image --format json --output trivy-report.json \\
                            registry.company.com/${APP_NAME}:${BUILD_NUMBER}
                    """
                    
                    // Parse results and fail on high/critical vulnerabilities
                    def trivyReport = readJSON file: 'trivy-report.json'
                    def highVulns = trivyReport.Results?.findAll { 
                        it.Vulnerabilities?.any { vuln -> 
                            vuln.Severity in ['HIGH', 'CRITICAL'] 
                        }
                    }
                    
                    if (highVulns) {
                        error("High/Critical vulnerabilities found in container image")
                    }
                }
            }
        }
        
        stage('Infrastructure Security') {
            steps {
                script {
                    // Terraform security scanning with Checkov
                    sh 'checkov -d terraform/ --framework terraform --output json > checkov-report.json'
                    
                    // Kubernetes manifest scanning
                    sh 'kubesec scan k8s/*.yaml > kubesec-report.json'
                    
                    // Parse and evaluate results
                    def checkovReport = readJSON file: 'checkov-report.json'
                    if (checkovReport.summary.failed > 0) {
                        unstable("Infrastructure security issues found")
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Archive security reports
            archiveArtifacts artifacts: '*-report.json', fingerprint: true
            
            // Publish security metrics to monitoring system
            script {
                def metrics = [
                    sonarqube_issues: getSonarQubeIssues(),
                    dependency_vulnerabilities: getDependencyVulnerabilities(),
                    container_vulnerabilities: getContainerVulnerabilities()
                ]
                
                publishMetrics(metrics)
            }
        }
    }
}
```

---

## Scalability & Performance

### 6. How do you implement Jenkins at scale with master-agent architecture?

**Answer:**
Scalable Jenkins architecture for large organizations:

**Master Configuration:**
```groovy
// Jenkins Configuration as Code
jenkins:
  systemMessage: "Jenkins Master - Production Environment"
  numExecutors: 0  # Master should not run builds
  
  nodes:
    - permanent:
        name: "linux-agent-1"
        remoteFS: "/home/jenkins"
        launcher:
          ssh:
            host: "jenkins-agent-1.company.com"
            credentialsId: "jenkins-ssh-key"
            sshHostKeyVerificationStrategy: "nonVerifyingKeyVerificationStrategy"
        retentionStrategy: "always"
        nodeProperties:
          - envVars:
              env:
                - key: "AGENT_TYPE"
                  value: "linux"
                - key: "DOCKER_HOST"
                  value: "unix:///var/run/docker.sock"
        
    - permanent:
        name: "windows-agent-1"
        remoteFS: "C:\\Jenkins"
        launcher:
          command:
            command: "java -jar agent.jar"
        nodeProperties:
          - envVars:
              env:
                - key: "AGENT_TYPE"
                  value: "windows"

  clouds:
    - kubernetes:
        name: "kubernetes"
        serverUrl: "https://k8s-api.company.com"
        namespace: "jenkins"
        credentialsId: "k8s-service-account"
        templates:
          - name: "maven-build"
            label: "maven"
            containers:
              - name: "maven"
                image: "maven:3.8-openjdk-11"
                command: "sleep"
                args: "infinity"
                resourceRequestCpu: "500m"
                resourceRequestMemory: "1Gi"
                resourceLimitCpu: "2000m"
                resourceLimitMemory: "4Gi"
```

**Dynamic Agent Provisioning:**
```groovy
pipeline {
    agent {
        kubernetes {
            yaml """
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: maven
                    image: maven:3.8-openjdk-11
                    command:
                    - sleep
                    args:
                    - infinity
                    resources:
                      requests:
                        memory: "1Gi"
                        cpu: "500m"
                      limits:
                        memory: "4Gi"
                        cpu: "2000m"
                  - name: docker
                    image: docker:20.10-dind
                    securityContext:
                      privileged: true
                    env:
                    - name: DOCKER_TLS_CERTDIR
                      value: ""
            """
        }
    }
    
    stages {
        stage('Build') {
            steps {
                container('maven') {
                    sh 'mvn clean compile'
                }
            }
        }
        
        stage('Test') {
            steps {
                container('maven') {
                    sh 'mvn test'
                }
            }
        }
        
        stage('Package') {
            steps {
                container('docker') {
                    script {
                        def image = docker.build("${APP_NAME}:${BUILD_NUMBER}")
                        image.push()
                    }
                }
            }
        }
    }
}
```

### 7. How do you optimize Jenkins performance and resource usage?

**Answer:**
Performance optimization strategies:

**JVM Tuning:**
```bash
# Jenkins JVM options
JENKINS_JAVA_OPTIONS="-Xms4g -Xmx8g \
    -XX:+UseG1GC \
    -XX:MaxGCPauseMillis=100 \
    -XX:+UseStringDeduplication \
    -XX:+ParallelRefProcEnabled \
    -XX:+DisableExplicitGC \
    -Djava.awt.headless=true \
    -Djenkins.install.runSetupWizard=false"

# System properties for performance
-Dhudson.model.DirectoryBrowserSupport.CSP="default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
-Dhudson.slaves.NodeProvisioner.initialDelay=0
-Dhudson.slaves.NodeProvisioner.MARGIN=50
-Dhudson.slaves.NodeProvisioner.MARGIN0=0.85
```

**Pipeline Optimization:**
```groovy
pipeline {
    agent none
    
    options {
        // Optimize build retention
        buildDiscarder(logRotator(
            numToKeepStr: '10',
            daysToKeepStr: '30',
            artifactNumToKeepStr: '5'
        ))
        
        // Timeout for entire pipeline
        timeout(time: 1, unit: 'HOURS')
        
        // Skip default checkout
        skipDefaultCheckout()
        
        // Disable concurrent builds
        disableConcurrentBuilds()
    }
    
    stages {
        stage('Checkout') {
            agent { label 'lightweight' }
            steps {
                // Shallow clone for faster checkout
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    extensions: [
                        [$class: 'CloneOption', depth: 1, shallow: true],
                        [$class: 'CheckoutOption', timeout: 10]
                    ],
                    userRemoteConfigs: [[url: 'https://github.com/company/repo.git']]
                ])
                
                // Stash code for other stages
                stash includes: '**', name: 'source-code'
            }
        }
        
        stage('Parallel Processing') {
            parallel {
                stage('Build') {
                    agent { label 'build-agent' }
                    steps {
                        unstash 'source-code'
                        sh 'mvn clean compile -T 4'  // Parallel compilation
                        stash includes: 'target/**', name: 'build-artifacts'
                    }
                }
                
                stage('Static Analysis') {
                    agent { label 'analysis-agent' }
                    steps {
                        unstash 'source-code'
                        sh 'sonar-scanner'
                    }
                }
            }
        }
    }
}
```

---

## Integration & Ecosystem

### 8. How do you integrate Jenkins with monitoring and observability tools?

**Answer:**
Comprehensive monitoring integration:

**Metrics Collection:**
```groovy
// Pipeline with metrics collection
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    def startTime = System.currentTimeMillis()
                    
                    try {
                        sh 'mvn clean compile'
                        
                        // Record success metrics
                        def duration = System.currentTimeMillis() - startTime
                        publishMetric('build.duration', duration, 'ms')
                        publishMetric('build.success', 1, 'count')
                        
                    } catch (Exception e) {
                        publishMetric('build.failure', 1, 'count')
                        throw e
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                // Collect build metrics
                def buildMetrics = [
                    build_number: env.BUILD_NUMBER,
                    build_duration: currentBuild.duration,
                    build_result: currentBuild.result,
                    queue_time: currentBuild.timeInMillis - currentBuild.startTimeInMillis,
                    node_name: env.NODE_NAME,
                    job_name: env.JOB_NAME
                ]
                
                // Send to monitoring systems
                sendToDatadog(buildMetrics)
                sendToPrometheus(buildMetrics)
                sendToElasticsearch(buildMetrics)
            }
        }
    }
}

def publishMetric(name, value, unit) {
    // Send to multiple monitoring systems
    sh """
        curl -X POST 'http://prometheus-pushgateway:9091/metrics/job/jenkins/instance/${env.NODE_NAME}' \\
            --data-binary '${name}{job="${env.JOB_NAME}",build="${env.BUILD_NUMBER}"} ${value}'
    """
    
    // Send to Datadog
    sh """
        curl -X POST 'https://api.datadoghq.com/api/v1/series' \\
            -H 'Content-Type: application/json' \\
            -H 'DD-API-KEY: ${env.DATADOG_API_KEY}' \\
            -d '{
                "series": [{
                    "metric": "jenkins.${name}",
                    "points": [[$(date +%s), ${value}]],
                    "tags": ["job:${env.JOB_NAME}", "build:${env.BUILD_NUMBER}"]
                }]
            }'
    """
}
```

**Log Aggregation:**
```groovy
// Structured logging pipeline
pipeline {
    agent any
    
    environment {
        LOG_LEVEL = 'INFO'
        CORRELATION_ID = UUID.randomUUID().toString()
    }
    
    stages {
        stage('Setup Logging') {
            steps {
                script {
                    // Configure structured logging
                    sh """
                        cat > logback.xml << 'EOF'
                        <configuration>
                            <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
                                <encoder class="net.logstash.logback.encoder.LoggingEventCompositeJsonEncoder">
                                    <providers>
                                        <timestamp/>
                                        <logLevel/>
                                        <loggerName/>
                                        <message/>
                                        <mdc/>
                                        <pattern>
                                            <pattern>
                                                {
                                                    "job_name": "${env.JOB_NAME}",
                                                    "build_number": "${env.BUILD_NUMBER}",
                                                    "correlation_id": "${env.CORRELATION_ID}",
                                                    "node_name": "${env.NODE_NAME}"
                                                }
                                            </pattern>
                                        </pattern>
                                    </providers>
                                </encoder>
                            </appender>
                            <root level="${env.LOG_LEVEL}">
                                <appender-ref ref="STDOUT"/>
                            </root>
                        </configuration>
                        EOF
                    """
                }
            }
        }
        
        stage('Application Build') {
            steps {
                script {
                    // Build with structured logging
                    sh """
                        mvn clean package \\
                            -Dlogback.configurationFile=logback.xml \\
                            -Dcorrelation.id=${env.CORRELATION_ID}
                    """
                }
            }
        }
    }
    
    post {
        always {
            // Ship logs to ELK stack
            sh """
                curl -X POST 'http://logstash:5044' \\
                    -H 'Content-Type: application/json' \\
                    -d '{
                        "job_name": "${env.JOB_NAME}",
                        "build_number": "${env.BUILD_NUMBER}",
                        "correlation_id": "${env.CORRELATION_ID}",
                        "build_result": "${currentBuild.result}",
                        "build_duration": ${currentBuild.duration},
                        "timestamp": "$(date -Iseconds)",
                        "logs": "$(cat jenkins.log | base64 -w 0)"
                    }'
            """
        }
    }
}
```

---

## Best Practices & Governance

### 9. How do you implement Jenkins governance and compliance?

**Answer:**
Governance framework for enterprise Jenkins:

**Pipeline Standards:**
```groovy
// Shared library for enforcing standards
// vars/standardPipeline.groovy
def call(Map config) {
    // Validate required configuration
    validateConfig(config)
    
    pipeline {
        agent any
        
        options {
            // Enforce standard options
            buildDiscarder(logRotator(numToKeepStr: '10'))
            timeout(time: config.timeout ?: 60, unit: 'MINUTES')
            skipDefaultCheckout()
        }
        
        stages {
            stage('Compliance Checks') {
                steps {
                    script {
                        // Mandatory security scans
                        runSecurityScans()
                        
                        // License compliance
                        checkLicenseCompliance()
                        
                        // Code quality gates
                        enforceQualityGates(config.qualityGates)
                    }
                }
            }
            
            stage('Build') {
                steps {
                    script {
                        // Standardized build process
                        executeBuildSteps(config.buildSteps)
                    }
                }
            }
            
            stage('Deploy') {
                when {
                    anyOf {
                        branch 'main'
                        branch 'release/*'
                    }
                }
                steps {
                    script {
                        // Deployment approval process
                        if (config.requiresApproval) {
                            def approvers = getApprovers(config.environment)
                            input message: "Deploy to ${config.environment}?", 
                                  submitterParameter: 'APPROVER',
                                  submitter: approvers.join(',')
                        }
                        
                        // Standardized deployment
                        executeDeployment(config)
                    }
                }
            }
        }
        
        post {
            always {
                // Mandatory reporting
                generateComplianceReport()
                archiveArtifacts artifacts: 'compliance-report.json'
                
                // Audit logging
                auditPipelineExecution(config)
            }
        }
    }
}

def validateConfig(config) {
    def requiredFields = ['appName', 'environment', 'buildSteps']
    requiredFields.each { field ->
        if (!config.containsKey(field)) {
            error("Missing required configuration: ${field}")
        }
    }
}

def getApprovers(environment) {
    def approvers = [
        'development': ['dev-team'],
        'staging': ['dev-team', 'qa-team'],
        'production': ['devops-team', 'security-team']
    ]
    return approvers[environment] ?: ['admin']
}
```

**Configuration as Code:**
```yaml
# jenkins.yaml - Jenkins Configuration as Code
jenkins:
  systemMessage: "Managed by Configuration as Code"
  
  globalNodeProperties:
    - envVars:
        env:
          - key: "COMPANY_STANDARDS_VERSION"
            value: "2.1.0"
          - key: "COMPLIANCE_ENDPOINT"
            value: "https://compliance.company.com/api"

  securityRealm:
    saml:
      binding: "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
      displayNameAttributeName: "displayName"
      emailAttributeName: "email"
      groupsAttributeName: "groups"
      idpMetadataConfiguration:
        url: "https://sso.company.com/metadata"
      maximumAuthenticationLifetime: 86400
      usernameAttributeName: "username"

  authorizationStrategy:
    projectMatrix:
      permissions:
        - "Overall/Administer:admin"
        - "Overall/Read:authenticated"
        - "Job/Build:developers"
        - "Job/Cancel:developers"
        - "Job/Read:developers"

tool:
  maven:
    installations:
      - name: "Maven-3.8"
        properties:
          - installSource:
              installers:
                - maven:
                    id: "3.8.6"
  
  jdk:
    installations:
      - name: "JDK-11"
        properties:
          - installSource:
              installers:
                - adoptOpenJdkInstaller:
                    id: "jdk-11.0.16+8"

unclassified:
  sonarGlobalConfiguration:
    installations:
      - name: "SonarQube"
        serverUrl: "https://sonar.company.com"
        credentialsId: "sonar-token"
  
  globalLibraries:
    libraries:
      - name: "company-jenkins-library"
        defaultVersion: "main"
        retriever:
          modernSCM:
            scm:
              git:
                remote: "https://github.com/company/jenkins-shared-library.git"
                credentialsId: "github-token"
```

### 10. How do you implement disaster recovery for Jenkins?

**Answer:**
Comprehensive disaster recovery strategy:

**Backup Strategy:**
```bash
#!/bin/bash
# Jenkins backup script

JENKINS_HOME="/var/lib/jenkins"
BACKUP_DIR="/backup/jenkins"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="jenkins_backup_${DATE}.tar.gz"

# Create backup directory
mkdir -p ${BACKUP_DIR}

# Stop Jenkins service
systemctl stop jenkins

# Create backup excluding unnecessary files
tar -czf ${BACKUP_DIR}/${BACKUP_FILE} \
    --exclude='workspace/*' \
    --exclude='builds/*/archive' \
    --exclude='*.log' \
    --exclude='cache/*' \
    --exclude='war/*' \
    -C ${JENKINS_HOME} .

# Restart Jenkins service
systemctl start jenkins

# Upload to cloud storage
aws s3 cp ${BACKUP_DIR}/${BACKUP_FILE} s3://company-jenkins-backups/

# Cleanup old backups (keep last 30 days)
find ${BACKUP_DIR} -name "jenkins_backup_*.tar.gz" -mtime +30 -delete

# Verify backup integrity
tar -tzf ${BACKUP_DIR}/${BACKUP_FILE} > /dev/null
if [ $? -eq 0 ]; then
    echo "Backup completed successfully: ${BACKUP_FILE}"
else
    echo "Backup verification failed!"
    exit 1
fi
```

**Infrastructure as Code:**
```terraform
# Terraform configuration for Jenkins infrastructure
resource "aws_instance" "jenkins_master" {
  ami           = var.jenkins_ami
  instance_type = "t3.large"
  
  vpc_security_group_ids = [aws_security_group.jenkins.id]
  subnet_id              = aws_subnet.private.id
  
  user_data = templatefile("${path.module}/jenkins-init.sh", {
    backup_bucket = aws_s3_bucket.jenkins_backups.bucket
  })
  
  tags = {
    Name = "jenkins-master"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "jenkins_backups" {
  bucket = "company-jenkins-backups-${var.environment}"
  
  versioning {
    enabled = true
  }
  
  lifecycle_rule {
    enabled = true
    
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    
    expiration {
      days = 365
    }
  }
}

resource "aws_efs_file_system" "jenkins_home" {
  creation_token = "jenkins-home-${var.environment}"
  
  lifecycle_policy {
    transition_to_ia = "AFTER_30_DAYS"
  }
  
  tags = {
    Name = "jenkins-home"
  }
}
```

**Recovery Procedures:**
```bash
#!/bin/bash
# Jenkins disaster recovery script

BACKUP_BUCKET="s3://company-jenkins-backups"
JENKINS_HOME="/var/lib/jenkins"
RECOVERY_DIR="/tmp/jenkins-recovery"

# Download latest backup
echo "Downloading latest backup..."
aws s3 cp ${BACKUP_BUCKET}/ ${RECOVERY_DIR}/ --recursive
LATEST_BACKUP=$(ls -t ${RECOVERY_DIR}/jenkins_backup_*.tar.gz | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "No backup found!"
    exit 1
fi

# Stop Jenkins service
systemctl stop jenkins

# Backup current state (if any)
if [ -d "$JENKINS_HOME" ]; then
    mv $JENKINS_HOME ${JENKINS_HOME}.$(date +%Y%m%d_%H%M%S)
fi

# Create new Jenkins home
mkdir -p $JENKINS_HOME

# Restore from backup
echo "Restoring from backup: $LATEST_BACKUP"
tar -xzf $LATEST_BACKUP -C $JENKINS_HOME

# Set correct permissions
chown -R jenkins:jenkins $JENKINS_HOME
chmod -R 755 $JENKINS_HOME

# Start Jenkins service
systemctl start jenkins

# Wait for Jenkins to start
echo "Waiting for Jenkins to start..."
timeout 300 bash -c 'until curl -s http://localhost:8080 > /dev/null; do sleep 5; done'

if [ $? -eq 0 ]; then
    echo "Jenkins recovery completed successfully!"
else
    echo "Jenkins failed to start after recovery!"
    exit 1
fi

# Verify critical jobs
echo "Verifying critical jobs..."
curl -s "http://localhost:8080/api/json" | jq '.jobs[].name'
```

---

## 🎯 Key Takeaways

1. **Advanced Pipelines**: Implement complex workflows with parallel execution and conditional logic
2. **Shared Libraries**: Promote code reuse and standardization across teams
3. **Security**: Multi-layered security with secrets management and scanning
4. **Scalability**: Master-agent architecture with dynamic provisioning
5. **Monitoring**: Comprehensive observability and metrics collection
6. **Governance**: Enforce standards and compliance requirements
7. **Disaster Recovery**: Robust backup and recovery procedures

---

*This extended guide covers advanced Jenkins concepts for senior DevOps and data engineering roles. Focus on understanding enterprise-scale implementations, security best practices, and operational excellence.*