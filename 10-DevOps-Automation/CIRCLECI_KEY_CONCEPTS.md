# CircleCI Key Concepts

## 1. Cloud-Based CI/CD Platform
**What it is**: Continuous integration and deployment platform that automates software development workflows with cloud-based and on-premises options.

**Core Features**:
- **Docker-First**: Native Docker support for consistent environments
- **Parallel Execution**: Run jobs simultaneously for faster builds
- **Orbs**: Reusable configuration packages
- **Workflows**: Orchestrate complex job dependencies
- **Insights**: Performance analytics and optimization

## 2. Configuration Structure
**Basic .circleci/config.yml**:
```yaml
version: 2.1

# Define executors
executors:
  python-executor:
    docker:
      - image: cimg/python:3.9
    working_directory: ~/project

# Define jobs
jobs:
  test:
    executor: python-executor
    steps:
      - checkout
      - restore_cache:
          keys:
            - deps-{{ checksum "requirements.txt" }}
      - run:
          name: Install dependencies
          command: |
            python -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt
      - save_cache:
          key: deps-{{ checksum "requirements.txt" }}
          paths:
            - venv
      - run:
          name: Run tests
          command: |
            . venv/bin/activate
            pytest tests/ --junitxml=test-results/junit.xml
      - store_test_results:
          path: test-results

  build:
    executor: python-executor
    steps:
      - checkout
      - setup_remote_docker:
          version: 20.10.14
      - run:
          name: Build Docker image
          command: |
            docker build -t myapp:${CIRCLE_SHA1} .
            docker tag myapp:${CIRCLE_SHA1} myapp:latest

# Define workflows
workflows:
  version: 2
  test-and-build:
    jobs:
      - test
      - build:
          requires:
            - test
```

## 3. Executors and Environments
**Docker Executor**:
```yaml
executors:
  node-executor:
    docker:
      - image: cimg/node:16.14
        environment:
          NODE_ENV: test
      - image: cimg/postgres:13.1
        environment:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: testdb
    working_directory: ~/app

jobs:
  integration-test:
    executor: node-executor
    steps:
      - checkout
      - run:
          name: Wait for database
          command: dockerize -wait tcp://localhost:5432 -timeout 1m
      - run:
          name: Run integration tests
          command: npm run test:integration
```

**Machine Executor**:
```yaml
jobs:
  docker-build:
    machine:
      image: ubuntu-2004:202201-02
    steps:
      - checkout
      - run:
          name: Build and test Docker image
          command: |
            docker build -t myapp .
            docker run --rm myapp npm test
```

**macOS Executor**:
```yaml
jobs:
  ios-build:
    macos:
      xcode: 13.4.1
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: |
            brew install node
            npm install
      - run:
          name: Build iOS app
          command: |
            xcodebuild -workspace MyApp.xcworkspace \
                       -scheme MyApp \
                       -destination 'platform=iOS Simulator,name=iPhone 13'
```

## 4. Orbs (Reusable Configuration)
**Using Orbs**:
```yaml
version: 2.1

orbs:
  python: circleci/python@2.0.3
  aws-cli: circleci/aws-cli@3.1.1
  slack: circleci/slack@4.10.1

jobs:
  test:
    executor: python/default
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
      - run:
          name: Run tests
          command: pytest
      - slack/notify:
          event: fail
          template: basic_fail_1

  deploy:
    executor: aws-cli/default
    steps:
      - checkout
      - aws-cli/setup
      - run:
          name: Deploy to S3
          command: |
            aws s3 sync ./dist s3://my-app-bucket --delete
      - slack/notify:
          event: pass
          template: success_tagged_deploy_1

workflows:
  test-and-deploy:
    jobs:
      - test
      - deploy:
          requires:
            - test
          filters:
            branches:
              only: main
```

**Custom Orb Development**:
```yaml
# .circleci/orb.yml
version: 2.1

description: Custom data pipeline orb

commands:
  run-data-quality-checks:
    description: Run data quality validation
    parameters:
      config-file:
        type: string
        default: "dq-config.yml"
    steps:
      - run:
          name: Data Quality Checks
          command: |
            python -m data_quality.validator \
              --config << parameters.config-file >> \
              --output-format junit \
              --output-file test-results/dq-results.xml

jobs:
  data-pipeline-test:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - run-data-quality-checks:
          config-file: "pipeline-dq-config.yml"
      - store_test_results:
          path: test-results
```

## 5. Workflows and Job Orchestration
**Complex Workflow**:
```yaml
workflows:
  version: 2
  data-pipeline:
    jobs:
      # Parallel testing
      - unit-tests
      - integration-tests
      - lint-and-security
      
      # Build after tests pass
      - build-image:
          requires:
            - unit-tests
            - integration-tests
            - lint-and-security
      
      # Deploy to staging
      - deploy-staging:
          requires:
            - build-image
          filters:
            branches:
              only: develop
      
      # Manual approval for production
      - hold-for-approval:
          type: approval
          requires:
            - deploy-staging
          filters:
            branches:
              only: main
      
      # Deploy to production
      - deploy-production:
          requires:
            - hold-for-approval
          filters:
            branches:
              only: main

  # Scheduled workflow
  nightly-data-refresh:
    triggers:
      - schedule:
          cron: "0 2 * * *"  # 2 AM daily
          filters:
            branches:
              only: main
    jobs:
      - refresh-data-warehouse
      - run-data-quality-checks:
          requires:
            - refresh-data-warehouse
```

**Conditional Workflows**:
```yaml
workflows:
  version: 2
  conditional-deploy:
    when:
      and:
        - equal: [ main, << pipeline.git.branch >> ]
        - not:
            matches:
              pattern: "^skip-deploy.*"
              value: << pipeline.git.tag >>
    jobs:
      - test
      - deploy:
          requires:
            - test
```

## 6. Caching and Optimization
**Dependency Caching**:
```yaml
jobs:
  test:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      
      # Restore cache
      - restore_cache:
          keys:
            - deps-v1-{{ checksum "requirements.txt" }}
            - deps-v1-  # Fallback cache
      
      - run:
          name: Install dependencies
          command: |
            python -m venv venv
            . venv/bin/activate
            pip install -r requirements.txt
      
      # Save cache
      - save_cache:
          key: deps-v1-{{ checksum "requirements.txt" }}
          paths:
            - venv
      
      - run:
          name: Run tests
          command: |
            . venv/bin/activate
            pytest tests/
```

**Docker Layer Caching**:
```yaml
jobs:
  build:
    machine:
      image: ubuntu-2004:202201-02
      docker_layer_caching: true  # Requires paid plan
    steps:
      - checkout
      - run:
          name: Build Docker image
          command: |
            # Docker layers will be cached automatically
            docker build -t myapp:${CIRCLE_SHA1} .
```

**Workspace Sharing**:
```yaml
jobs:
  build:
    docker:
      - image: cimg/node:16.14
    steps:
      - checkout
      - run: npm ci
      - run: npm run build
      - persist_to_workspace:
          root: .
          paths:
            - dist
            - node_modules

  test:
    docker:
      - image: cimg/node:16.14
    steps:
      - checkout
      - attach_workspace:
          at: .
      - run: npm test

  deploy:
    docker:
      - image: cimg/node:16.14
    steps:
      - checkout
      - attach_workspace:
          at: .
      - run: npm run deploy
```

## 7. Environment Variables and Secrets
**Environment Variables**:
```yaml
jobs:
  deploy:
    docker:
      - image: cimg/python:3.9
    environment:
      FLASK_ENV: production
      DATABASE_URL: postgresql://localhost/myapp
    steps:
      - checkout
      - run:
          name: Deploy application
          command: |
            echo "Deploying to $FLASK_ENV environment"
            echo "Database: $DATABASE_URL"
            python deploy.py
```

**Context Usage**:
```yaml
workflows:
  deploy-to-aws:
    jobs:
      - deploy:
          context:
            - aws-credentials
            - slack-notifications
          filters:
            branches:
              only: main

# Contexts are managed in CircleCI UI and contain:
# aws-credentials context:
#   - AWS_ACCESS_KEY_ID
#   - AWS_SECRET_ACCESS_KEY
#   - AWS_DEFAULT_REGION
# slack-notifications context:
#   - SLACK_WEBHOOK_URL
```

## 8. Testing and Quality Gates
**Parallel Testing**:
```yaml
jobs:
  test:
    docker:
      - image: cimg/python:3.9
    parallelism: 4
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: pip install -r requirements.txt
      - run:
          name: Run tests in parallel
          command: |
            # Split tests across parallel containers
            TESTFILES=$(circleci tests glob "tests/**/*.py" | circleci tests split --split-by=timings)
            pytest $TESTFILES --junitxml=test-results/junit.xml
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: test-results
```

**Code Coverage**:
```yaml
jobs:
  test-with-coverage:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - run:
          name: Install dependencies
          command: |
            pip install -r requirements.txt
            pip install pytest-cov codecov
      - run:
          name: Run tests with coverage
          command: |
            pytest --cov=src tests/ --cov-report=xml --cov-report=html
      - run:
          name: Upload coverage to Codecov
          command: codecov
      - store_artifacts:
          path: htmlcov
```

## 9. Deployment Strategies
**Blue-Green Deployment**:
```yaml
jobs:
  deploy-blue-green:
    docker:
      - image: cimg/aws:2022.06
    steps:
      - checkout
      - run:
          name: Deploy to blue environment
          command: |
            # Deploy new version to blue environment
            aws ecs update-service \
              --cluster production \
              --service myapp-blue \
              --task-definition myapp:${CIRCLE_BUILD_NUM}
            
            # Wait for deployment to complete
            aws ecs wait services-stable \
              --cluster production \
              --services myapp-blue
      
      - run:
          name: Run health checks
          command: |
            # Health check blue environment
            for i in {1..30}; do
              if curl -f http://blue.myapp.com/health; then
                echo "Health check passed"
                break
              fi
              sleep 10
            done
      
      - run:
          name: Switch traffic to blue
          command: |
            # Update load balancer to point to blue
            aws elbv2 modify-target-group \
              --target-group-arn $BLUE_TARGET_GROUP_ARN \
              --health-check-path /health
```

**Canary Deployment**:
```yaml
jobs:
  canary-deploy:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - run:
          name: Deploy canary (10% traffic)
          command: |
            # Deploy to canary environment with 10% traffic
            kubectl patch service myapp-service -p \
              '{"spec":{"selector":{"version":"canary"}}}'
            
            # Update canary deployment
            kubectl set image deployment/myapp-canary \
              myapp=myapp:${CIRCLE_SHA1}
      
      - run:
          name: Monitor canary metrics
          command: |
            # Monitor for 10 minutes
            python scripts/monitor_canary.py \
              --duration 600 \
              --error-threshold 0.01 \
              --latency-threshold 500
      
      - run:
          name: Promote or rollback
          command: |
            if [ "$CANARY_SUCCESS" = "true" ]; then
              # Promote canary to full deployment
              kubectl patch service myapp-service -p \
                '{"spec":{"selector":{"version":"canary"}}}'
            else
              # Rollback canary
              kubectl rollout undo deployment/myapp-canary
            fi
```

## 10. Monitoring and Notifications
**Slack Integration**:
```yaml
version: 2.1

orbs:
  slack: circleci/slack@4.10.1

jobs:
  test:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - run: pytest tests/
      - slack/notify:
          event: fail
          mentions: '@data-team'
          template: basic_fail_1
      - slack/notify:
          event: pass
          template: success_tagged_deploy_1

  deploy:
    docker:
      - image: cimg/aws:2022.06
    steps:
      - checkout
      - run:
          name: Deploy to production
          command: ./deploy.sh
      - slack/notify:
          event: always
          custom: |
            {
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "🚀 Deployment completed!\n*Project:* $CIRCLE_PROJECT_REPONAME\n*Branch:* $CIRCLE_BRANCH\n*Commit:* $CIRCLE_SHA1"
                  }
                }
              ]
            }
```

**Custom Monitoring**:
```python
# scripts/monitor_deployment.py
import requests
import time
import sys
from datetime import datetime

def monitor_deployment(endpoint, duration_minutes=10, check_interval=30):
    """Monitor deployment health"""
    
    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)
    
    success_count = 0
    total_checks = 0
    
    while time.time() < end_time:
        try:
            response = requests.get(f"{endpoint}/health", timeout=10)
            
            if response.status_code == 200:
                success_count += 1
                print(f"✓ Health check passed ({datetime.now()})")
            else:
                print(f"✗ Health check failed: {response.status_code}")
            
            total_checks += 1
            
        except Exception as e:
            print(f"✗ Health check error: {e}")
            total_checks += 1
        
        time.sleep(check_interval)
    
    success_rate = success_count / total_checks if total_checks > 0 else 0
    
    print(f"\nMonitoring complete:")
    print(f"Success rate: {success_rate:.2%} ({success_count}/{total_checks})")
    
    # Exit with error if success rate is below threshold
    if success_rate < 0.95:
        print("❌ Deployment failed health checks")
        sys.exit(1)
    else:
        print("✅ Deployment passed health checks")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--duration", type=int, default=10)
    parser.add_argument("--interval", type=int, default=30)
    
    args = parser.parse_args()
    
    monitor_deployment(args.endpoint, args.duration, args.interval)
```

**Performance Insights**:
```yaml
jobs:
  performance-test:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - run:
          name: Install performance testing tools
          command: |
            pip install locust
      - run:
          name: Run load tests
          command: |
            locust --headless \
                   --users 100 \
                   --spawn-rate 10 \
                   --run-time 5m \
                   --host https://staging.myapp.com \
                   --html performance-report.html
      - store_artifacts:
          path: performance-report.html
      - run:
          name: Check performance thresholds
          command: |
            python scripts/check_performance.py \
              --report performance-report.html \
              --max-response-time 500 \
              --min-rps 50
```