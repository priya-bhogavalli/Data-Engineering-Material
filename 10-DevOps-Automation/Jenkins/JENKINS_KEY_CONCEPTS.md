# Jenkins Key Concepts

## 1. Jenkins Fundamentals
**What is Jenkins**: Open-source automation server for CI/CD pipelines.

**Core Components**:
- **Master/Controller**: Orchestrates builds and manages agents
- **Agents/Nodes**: Execute build jobs
- **Jobs/Projects**: Individual build configurations
- **Builds**: Execution instances of jobs
- **Plugins**: Extend functionality

## 2. Pipeline as Code
```groovy
// Jenkinsfile - Declarative Pipeline
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'my-registry.com'
        APP_NAME = 'data-processor'
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/company/data-pipeline.git'
            }
        }
        
        stage('Test') {
            steps {
                sh 'python -m pytest tests/'
                sh 'flake8 src/'
            }
        }
        
        stage('Build') {
            steps {
                sh 'docker build -t ${APP_NAME}:${BUILD_NUMBER} .'
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker push ${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}'
                sh 'kubectl set image deployment/${APP_NAME} ${APP_NAME}=${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        failure {
            emailext to: 'team@company.com',
                     subject: 'Build Failed: ${JOB_NAME} - ${BUILD_NUMBER}',
                     body: 'Build failed. Check console output.'
        }
    }
}
```

## 3. Job Types and Configuration
```groovy
// Freestyle Job equivalent in Pipeline
node {
    stage('Build') {
        checkout scm
        sh 'make build'
    }
    
    stage('Test') {
        sh 'make test'
        publishTestResults testResultsPattern: 'test-results.xml'
    }
    
    stage('Archive') {
        archiveArtifacts artifacts: 'dist/*.jar', fingerprint: true
    }
}

// Multi-branch Pipeline
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo "Building branch: ${env.BRANCH_NAME}"
                sh 'make build'
            }
        }
    }
}
```

## 4. Build Triggers
```groovy
pipeline {
    agent any
    
    triggers {
        // Poll SCM every 5 minutes
        pollSCM('H/5 * * * *')
        
        // Cron schedule
        cron('H 2 * * *')  // Daily at 2 AM
        
        // Upstream projects
        upstream(upstreamProjects: 'data-ingestion', threshold: hudson.model.Result.SUCCESS)
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
    }
}

// Webhook trigger (configured in SCM)
// GitHub webhook: http://jenkins-server/github-webhook/
```

## 5. Parallel Execution
```groovy
pipeline {
    agent none
    
    stages {
        stage('Parallel Tests') {
            parallel {
                stage('Unit Tests') {
                    agent { label 'linux' }
                    steps {
                        sh 'python -m pytest unit_tests/'
                    }
                }
                
                stage('Integration Tests') {
                    agent { label 'docker' }
                    steps {
                        sh 'docker-compose up -d'
                        sh 'python -m pytest integration_tests/'
                        sh 'docker-compose down'
                    }
                }
                
                stage('Security Scan') {
                    agent any
                    steps {
                        sh 'bandit -r src/'
                    }
                }
            }
        }
    }
}
```

## 6. Environment Management
```groovy
pipeline {
    agent any
    
    environment {
        // Global environment variables
        DATABASE_URL = credentials('database-url')
        API_KEY = credentials('api-key')
        ENVIRONMENT = "${env.BRANCH_NAME == 'main' ? 'prod' : 'dev'}"
    }
    
    stages {
        stage('Deploy') {
            environment {
                // Stage-specific variables
                DEPLOY_TARGET = "${ENVIRONMENT}-cluster"
            }
            steps {
                script {
                    if (env.ENVIRONMENT == 'prod') {
                        input message: 'Deploy to production?', ok: 'Deploy'
                    }
                }
                sh 'kubectl config use-context ${DEPLOY_TARGET}'
                sh 'helm upgrade --install myapp ./chart'
            }
        }
    }
}
```

## 7. Error Handling and Notifications
```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                script {
                    try {
                        sh 'make build'
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error "Build failed: ${e.getMessage()}"
                    }
                }
            }
        }
    }
    
    post {
        success {
            slackSend channel: '#deployments',
                     color: 'good',
                     message: "✅ Build succeeded: ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
        }
        
        failure {
            emailext to: '${DEFAULT_RECIPIENTS}',
                     subject: '❌ Build Failed: ${JOB_NAME} - ${BUILD_NUMBER}',
                     body: '''Build failed. 
                             Check console output: ${BUILD_URL}console
                             Changes: ${CHANGES}'''
        }
        
        unstable {
            emailext to: '${DEFAULT_RECIPIENTS}',
                     subject: '⚠️ Build Unstable: ${JOB_NAME} - ${BUILD_NUMBER}',
                     body: 'Build completed with warnings.'
        }
    }
}
```

## 8. Shared Libraries
```groovy
// vars/deployToK8s.groovy (in shared library)
def call(Map config) {
    sh "kubectl config use-context ${config.cluster}"
    sh "helm upgrade --install ${config.app} ${config.chart} --set image.tag=${config.tag}"
}

// Using shared library in Jenkinsfile
@Library('my-shared-library') _

pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                deployToK8s([
                    cluster: 'prod-cluster',
                    app: 'data-processor',
                    chart: './helm-chart',
                    tag: env.BUILD_NUMBER
                ])
            }
        }
    }
}
```

## 9. Agent Management
```groovy
pipeline {
    agent none
    
    stages {
        stage('Build on Linux') {
            agent {
                label 'linux && docker'
            }
            steps {
                sh 'docker build -t myapp .'
            }
        }
        
        stage('Test on Windows') {
            agent {
                label 'windows'
            }
            steps {
                bat 'pytest tests/'
            }
        }
        
        stage('Deploy with Docker') {
            agent {
                docker {
                    image 'kubectl:latest'
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                sh 'kubectl apply -f deployment.yaml'
            }
        }
    }
}
```

## 10. Monitoring and Maintenance
```groovy
// Build metrics and monitoring
pipeline {
    agent any
    
    stages {
        stage('Metrics') {
            steps {
                script {
                    // Custom metrics
                    def buildTime = currentBuild.duration
                    def testResults = readFile('test-results.json')
                    
                    // Send to monitoring system
                    httpRequest(
                        httpMode: 'POST',
                        url: 'http://metrics-server/api/metrics',
                        requestBody: """
                        {
                            "job": "${env.JOB_NAME}",
                            "build": "${env.BUILD_NUMBER}",
                            "duration": ${buildTime},
                            "result": "${currentBuild.result}"
                        }
                        """
                    )
                }
            }
        }
    }
}

// Cleanup old builds
properties([
    buildDiscarder(logRotator(
        numToKeepStr: '10',
        daysToKeepStr: '30',
        artifactNumToKeepStr: '5'
    ))
])
```