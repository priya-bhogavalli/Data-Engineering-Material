
### Q1: What is Apache Oozie and what problems does it solve?
**Answer:**
Apache Oozie is a workflow scheduler system to manage Apache Hadoop jobs, providing a way to combine multiple jobs sequentially into one logical unit of work.

**Key Problems Solved:**
- **Workflow Orchestration**: Coordinate complex multi-step data processing
- **Job Dependencies**: Manage dependencies between different Hadoop jobs
- **Scheduling**: Time-based and data-based job scheduling
- **Error Handling**: Built-in retry and error recovery mechanisms
- **Monitoring**: Centralized monitoring and management of workflows

**Core Features:**
- XML-based workflow definition
- Support for MapReduce, Pig, Hive, Sqoop, and other actions
- Time and data-based triggers
- Web-based monitoring interface
- Integration with Hadoop security

### Q2: Explain Oozie architecture and components
**Answer:**
**Oozie Architecture:**

```
Client → Oozie Server → Hadoop Cluster
   ↓         ↓              ↓
Web UI ← Database ← → HDFS/JobTracker
```

**Key Components:**

1. **Oozie Server**
   - Web application running on servlet container
   - Processes workflow definitions
   - Manages job execution and state
   - Provides REST API and web UI

2. **Oozie Client**
   - Command-line tool for job submission
   - REST API client libraries
   - Web UI for monitoring

3. **Database**
   - Stores workflow definitions and execution state
   - Supports MySQL, PostgreSQL, Oracle, etc.
   - Maintains job history and metadata

4. **HDFS Integration**
   - Workflow definitions stored in HDFS
   - Application JARs and configuration files
   - Job logs and output data

### Q3: What are the different types of Oozie jobs?
**Answer:**
**Oozie Job Types:**

**1. Workflow Jobs**
- Directed Acyclic Graph (DAG) of actions
- Single execution instance
- Immediate or scheduled execution

**2. Coordinator Jobs**
- Schedules workflow jobs based on time and data availability
- Manages multiple workflow instances
- Handles data dependencies

**3. Bundle Jobs**
- Groups multiple coordinator jobs
- Manages related workflows as a unit
- Provides higher-level orchestration

**Job Hierarchy:**
```
Bundle Job
├── Coordinator Job 1 → Workflow Job 1.1, 1.2, 1.3...
├── Coordinator Job 2 → Workflow Job 2.1, 2.2, 2.3...
└── Coordinator Job 3 → Workflow Job 3.1, 3.2, 3.3...
```

---

## 🔄 Workflow Development

### Q4: How do you create a basic Oozie workflow?
**Answer:**
**Basic Oozie Workflow Structure:**

**1. Workflow Definition (workflow.xml):**
```xml
<workflow-app xmlns="uri:oozie:workflow:0.5" name="sample-workflow">
    <start to="first-action"/>
    
    <action name="first-action">
        <map-reduce>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <configuration>
                <property>
                    <name>mapred.mapper.class</name>
                    <value>org.example.MyMapper</value>
                </property>
                <property>
                    <name>mapred.reducer.class</name>
                    <value>org.example.MyReducer</value>
                </property>
                <property>
                    <name>mapred.input.dir</name>
                    <value>${inputDir}</value>
                </property>
                <property>
                    <name>mapred.output.dir</name>
                    <value>${outputDir}</value>
                </property>
            </configuration>
        </map-reduce>
        <ok to="second-action"/>
        <error to="fail"/>
    </action>
    
    <action name="second-action">
        <pig>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>process-data.pig</script>
            <param>INPUT=${outputDir}</param>
            <param>OUTPUT=${finalOutput}</param>
        </pig>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Workflow failed, error message[${wf:errorMessage(wf:lastErrorNode())}]</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**2. Job Properties (job.properties):**
```properties
nameNode=hdfs://namenode:8020
jobTracker=resourcemanager:8032
queueName=default

oozie.wf.application.path=${nameNode}/user/oozie/workflows/sample-workflow
inputDir=${nameNode}/user/data/input
outputDir=${nameNode}/user/data/output
finalOutput=${nameNode}/user/data/final
```

**3. Workflow Submission:**
```bash
# Submit workflow
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -submit

# Run workflow
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -run

# Check status
oozie job -oozie http://oozie-server:11000/oozie -info job-id
```

### Q5: Explain Oozie workflow control nodes
**Answer:**
**Oozie Control Nodes:**

**1. Start Node:**
```xml
<start to="first-action"/>
```

**2. End Node:**
```xml
<end name="end"/>
```

**3. Kill Node:**
```xml
<kill name="fail">
    <message>Workflow failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
</kill>
```

**4. Decision Node:**
```xml
<decision name="check-data">
    <switch>
        <case to="process-large-data">
            ${fs:fileSize(wf:conf('inputDir')) gt 1000000}
        </case>
        <case to="process-small-data">
            ${fs:fileSize(wf:conf('inputDir')) le 1000000}
        </case>
        <default to="fail"/>
    </switch>
</decision>
```

**5. Fork and Join Nodes:**
```xml
<fork name="parallel-processing">
    <path start="process-data-1"/>
    <path start="process-data-2"/>
    <path start="process-data-3"/>
</fork>

<action name="process-data-1">
    <!-- Action definition -->
    <ok to="join-node"/>
    <error to="fail"/>
</action>

<action name="process-data-2">
    <!-- Action definition -->
    <ok to="join-node"/>
    <error to="fail"/>
</action>

<action name="process-data-3">
    <!-- Action definition -->
    <ok to="join-node"/>
    <error to="fail"/>
</action>

<join name="join-node" to="final-action"/>
```

### Q6: How do you handle error handling and retries in Oozie?
**Answer:**
**Oozie Error Handling:**

**1. Action-level Error Handling:**
```xml
<action name="risky-action" retry-max="3" retry-interval="10">
    <map-reduce>
        <!-- MapReduce configuration -->
    </map-reduce>
    <ok to="next-action"/>
    <error to="error-handler"/>
</action>

<action name="error-handler">
    <email>
        <to>admin@company.com</to>
        <subject>Workflow Failed: ${wf:name()}</subject>
        <body>Error in action: ${wf:lastErrorNode()}</body>
    </email>
    <ok to="cleanup"/>
    <error to="fail"/>
</action>
```

**2. Global Error Handling:**
```xml
<global>
    <job-tracker>${jobTracker}</job-tracker>
    <name-node>${nameNode}</name-node>
    <configuration>
        <property>
            <name>mapred.job.queue.name</name>
            <value>${queueName}</value>
        </property>
    </configuration>
</global>
```

**3. Conditional Error Handling:**
```xml
<decision name="check-error-type">
    <switch>
        <case to="retry-action">
            ${wf:errorCode(wf:lastErrorNode()) eq 'TRANSIENT_ERROR'}
        </case>
        <case to="skip-action">
            ${wf:errorCode(wf:lastErrorNode()) eq 'DATA_NOT_AVAILABLE'}
        </case>
        <default to="fail"/>
    </switch>
</decision>
```

**4. Cleanup Actions:**
```xml
<action name="cleanup">
    <fs>
        <delete path="${tempDir}"/>
        <delete path="${errorDir}"/>
    </fs>
    <ok to="end"/>
    <error to="end"/>
</action>
```

---

## 📅 Coordinator & Bundle

### Q7: How do you create and configure Oozie coordinators?
**Answer:**
**Oozie Coordinator Configuration:**

**1. Coordinator Definition (coordinator.xml):**
```xml
<coordinator-app name="daily-data-processing" 
                 frequency="${coord:days(1)}" 
                 start="${startTime}" 
                 end="${endTime}" 
                 timezone="UTC"
                 xmlns="uri:oozie:coordinator:0.4">
    
    <parameters>
        <property>
            <name>workflowPath</name>
            <value>${workflowPath}</value>
        </property>
    </parameters>
    
    <datasets>
        <dataset name="input-data" frequency="${coord:days(1)}" 
                 initial-instance="${startTime}" timezone="UTC">
            <uri-template>${nameNode}/data/input/${YEAR}/${MONTH}/${DAY}</uri-template>
            <done-flag>_SUCCESS</done-flag>
        </dataset>
        
        <dataset name="output-data" frequency="${coord:days(1)}" 
                 initial-instance="${startTime}" timezone="UTC">
            <uri-template>${nameNode}/data/output/${YEAR}/${MONTH}/${DAY}</uri-template>
        </dataset>
    </datasets>
    
    <input-events>
        <data-in name="input" dataset="input-data">
            <instance>${coord:current(0)}</instance>
        </data-in>
    </input-events>
    
    <output-events>
        <data-out name="output" dataset="output-data">
            <instance>${coord:current(0)}</instance>
        </data-out>
    </output-events>
    
    <action>
        <workflow>
            <app-path>${workflowPath}</app-path>
            <configuration>
                <property>
                    <name>inputDir</name>
                    <value>${coord:dataIn('input')}</value>
                </property>
                <property>
                    <name>outputDir</name>
                    <value>${coord:dataOut('output')}</value>
                </property>
                <property>
                    <name>processDate</name>
                    <value>${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd')}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

**2. Coordinator Properties:**
```properties
nameNode=hdfs://namenode:8020
jobTracker=resourcemanager:8032
queueName=default

oozie.coord.application.path=${nameNode}/user/oozie/coordinators/daily-processing
workflowPath=${nameNode}/user/oozie/workflows/data-processing

startTime=2023-01-01T00:00Z
endTime=2024-01-01T00:00Z

oozie.use.system.libpath=true
```

**3. Advanced Coordinator Features:**
```xml
<!-- SLA monitoring -->
<action>
    <workflow>
        <app-path>${workflowPath}</app-path>
        <configuration>
            <!-- Workflow properties -->
        </configuration>
    </workflow>
    <sla:info>
        <sla:nominal-time>${coord:nominalTime()}</sla:nominal-time>
        <sla:should-start>${10 * MINUTES}</sla:should-start>
        <sla:should-end>${6 * HOURS}</sla:should-end>
        <sla:max-duration>${8 * HOURS}</sla:max-duration>
        <sla:alert-events>start_miss,end_miss,duration_miss</sla:alert-events>
        <sla:alert-contact>admin@company.com</sla:alert-contact>
    </sla:info>
</action>
```

### Q8: How do you create Oozie bundles?
**Answer:**
**Oozie Bundle Configuration:**

**1. Bundle Definition (bundle.xml):**
```xml
<bundle-app name="data-pipeline-bundle" xmlns="uri:oozie:bundle:0.2">
    
    <parameters>
        <property>
            <name>startTime</name>
            <value>${startTime}</value>
        </property>
        <property>
            <name>endTime</name>
            <value>${endTime}</value>
        </property>
    </parameters>
    
    <coordinator name="raw-data-ingestion">
        <app-path>${nameNode}/user/oozie/coordinators/raw-data-ingestion</app-path>
        <configuration>
            <property>
                <name>startTime</name>
                <value>${startTime}</value>
            </property>
            <property>
                <name>endTime</name>
                <value>${endTime}</value>
            </property>
            <property>
                <name>inputPath</name>
                <value>/data/raw</value>
            </property>
        </configuration>
    </coordinator>
    
    <coordinator name="data-processing">
        <app-path>${nameNode}/user/oozie/coordinators/data-processing</app-path>
        <configuration>
            <property>
                <name>startTime</name>
                <value>${startTime}</value>
            </property>
            <property>
                <name>endTime</name>
                <value>${endTime}</value>
            </property>
            <property>
                <name>dependsOn</name>
                <value>raw-data-ingestion</value>
            </property>
        </configuration>
    </coordinator>
    
    <coordinator name="data-export">
        <app-path>${nameNode}/user/oozie/coordinators/data-export</app-path>
        <configuration>
            <property>
                <name>startTime</name>
                <value>${startTime}</value>
            </property>
            <property>
                <name>endTime</name>
                <value>${endTime}</value>
            </property>
        </configuration>
    </coordinator>
    
</bundle-app>
```

**2. Bundle Submission:**
```bash
# Submit bundle
oozie job -oozie http://oozie-server:11000/oozie -config bundle.properties -submit

# Start bundle
oozie job -oozie http://oozie-server:11000/oozie -start bundle-job-id

# Monitor bundle
oozie job -oozie http://oozie-server:11000/oozie -info bundle-job-id
```

---

## ⚙️ Action Types

### Q9: Explain different Oozie action types and their usage
**Answer:**
**Oozie Action Types:**

**1. MapReduce Action:**
```xml
<action name="mapreduce-action">
    <map-reduce>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <prepare>
            <delete path="${outputDir}"/>
        </prepare>
        <configuration>
            <property>
                <name>mapred.job.queue.name</name>
                <value>${queueName}</value>
            </property>
            <property>
                <name>mapred.mapper.class</name>
                <value>org.example.MyMapper</value>
            </property>
            <property>
                <name>mapred.reducer.class</name>
                <value>org.example.MyReducer</value>
            </property>
            <property>
                <name>mapred.input.dir</name>
                <value>${inputDir}</value>
            </property>
            <property>
                <name>mapred.output.dir</name>
                <value>${outputDir}</value>
            </property>
        </configuration>
    </map-reduce>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

**2. Pig Action:**
```xml
<action name="pig-action">
    <pig>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <prepare>
            <delete path="${outputDir}"/>
        </prepare>
        <configuration>
            <property>
                <name>mapred.job.queue.name</name>
                <value>${queueName}</value>
            </property>
        </configuration>
        <script>process-data.pig</script>
        <param>INPUT=${inputDir}</param>
        <param>OUTPUT=${outputDir}</param>
        <param>DATE=${processDate}</param>
        <file>lookup-data.txt</file>
    </pig>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

**3. Hive Action:**
```xml
<action name="hive-action">
    <hive xmlns="uri:oozie:hive-action:0.5">
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <configuration>
            <property>
                <name>mapred.job.queue.name</name>
                <value>${queueName}</value>
            </property>
        </configuration>
        <script>process-data.hql</script>
        <param>INPUT_TABLE=${inputTable}</param>
        <param>OUTPUT_TABLE=${outputTable}</param>
        <param>PROCESS_DATE=${processDate}</param>
    </hive>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

**4. Sqoop Action:**
```xml
<action name="sqoop-action">
    <sqoop xmlns="uri:oozie:sqoop-action:0.4">
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <configuration>
            <property>
                <name>mapred.job.queue.name</name>
                <value>${queueName}</value>
            </property>
        </configuration>
        <command>import --connect jdbc:mysql://db-server:3306/mydb --username sqoop --password-file ${passwordFile} --table users --target-dir ${outputDir} --num-mappers 4</command>
    </sqoop>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

**5. Shell Action:**
```xml
<action name="shell-action">
    <shell xmlns="uri:oozie:shell-action:0.3">
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <exec>process-data.sh</exec>
        <argument>${inputDir}</argument>
        <argument>${outputDir}</argument>
        <argument>${processDate}</argument>
        <file>process-data.sh</file>
        <capture-output/>
    </shell>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

**6. Java Action:**
```xml
<action name="java-action">
    <java>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <configuration>
            <property>
                <name>mapred.job.queue.name</name>
                <value>${queueName}</value>
            </property>
        </configuration>
        <main-class>org.example.DataProcessor</main-class>
        <java-opts>-Xmx2048m</java-opts>
        <arg>${inputDir}</arg>
        <arg>${outputDir}</arg>
        <arg>${processDate}</arg>
        <file>data-processor.jar</file>
    </java>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

### Q10: How do you use Oozie EL functions?
**Answer:**
**Oozie Expression Language (EL) Functions:**

**1. Workflow Functions:**
```xml
<!-- Get workflow configuration -->
<value>${wf:conf('inputDir')}</value>

<!-- Get workflow ID and name -->
<value>${wf:id()}</value>
<value>${wf:name()}</value>

<!-- Get workflow run number -->
<value>${wf:run()}</value>

<!-- Error handling functions -->
<value>${wf:lastErrorNode()}</value>
<value>${wf:errorMessage(wf:lastErrorNode())}</value>
<value>${wf:errorCode(wf:lastErrorNode())}</value>

<!-- Action data functions -->
<value>${wf:actionData('previous-action')['key']}</value>
<value>${wf:actionExternalId('mapreduce-action')}</value>
```

**2. Coordinator Functions:**
```xml
<!-- Time functions -->
<value>${coord:current(0)}</value>  <!-- Current instance -->
<value>${coord:current(-1)}</value> <!-- Previous instance -->
<value>${coord:current(1)}</value>  <!-- Next instance -->

<!-- Nominal time -->
<value>${coord:nominalTime()}</value>
<value>${coord:actualTime()}</value>

<!-- Date formatting -->
<value>${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd')}</value>
<value>${coord:formatTime(coord:nominalTime(), 'yyyy/MM/dd/HH')}</value>

<!-- Data functions -->
<value>${coord:dataIn('input-dataset')}</value>
<value>${coord:dataOut('output-dataset')}</value>

<!-- Range functions -->
<value>${coord:latest(0)}</value>
<value>${coord:future(0, 1)}</value>
```

**3. File System Functions:**
```xml
<!-- File existence and size -->
<case to="process-large-file">
    ${fs:exists(wf:conf('inputFile')) and fs:fileSize(wf:conf('inputFile')) gt 1000000}
</case>

<!-- Directory operations -->
<case to="process-directory">
    ${fs:isDir(wf:conf('inputPath'))}
</case>

<!-- Directory listing -->
<value>${fs:dirSize(wf:conf('inputDir'))}</value>
```

**4. Utility Functions:**
```xml
<!-- String functions -->
<value>${replaceAll(wf:conf('inputPath'), '/input/', '/output/')}</value>
<value>${concat(wf:conf('basePath'), '/', coord:formatTime(coord:nominalTime(), 'yyyy/MM/dd'))}</value>

<!-- URL encoding -->
<value>${urlEncode(wf:conf('queryString'))}</value>

<!-- Math functions -->
<value>${firstNotNull(wf:conf('customValue'), 'defaultValue')}</value>
```

---

## 🔧 Configuration & Deployment

### Q11: How do you configure and deploy Oozie workflows?
**Answer:**
**Oozie Deployment Process:**

**1. Directory Structure:**
```
/user/oozie/workflows/my-workflow/
├── workflow.xml
├── job.properties
├── lib/
│   ├── my-workflow.jar
│   └── dependencies.jar
├── scripts/
│   ├── process-data.pig
│   └── process-data.hql
└── conf/
    └── hive-site.xml
```

**2. Workflow Packaging:**
```bash
#!/bin/bash
# deploy-workflow.sh

WORKFLOW_NAME="my-workflow"
HDFS_PATH="/user/oozie/workflows/${WORKFLOW_NAME}"

# Create HDFS directory
hdfs dfs -mkdir -p ${HDFS_PATH}
hdfs dfs -mkdir -p ${HDFS_PATH}/lib
hdfs dfs -mkdir -p ${HDFS_PATH}/scripts
hdfs dfs -mkdir -p ${HDFS_PATH}/conf

# Upload workflow files
hdfs dfs -put workflow.xml ${HDFS_PATH}/
hdfs dfs -put lib/*.jar ${HDFS_PATH}/lib/
hdfs dfs -put scripts/* ${HDFS_PATH}/scripts/
hdfs dfs -put conf/* ${HDFS_PATH}/conf/

# Set permissions
hdfs dfs -chmod -R 755 ${HDFS_PATH}
```

**3. Environment Configuration:**
```properties
# job.properties
nameNode=hdfs://namenode:8020
jobTracker=resourcemanager:8032
queueName=default

# Workflow path
oozie.wf.application.path=${nameNode}/user/oozie/workflows/my-workflow

# Input/Output paths
inputDir=${nameNode}/data/input/${year}/${month}/${day}
outputDir=${nameNode}/data/output/${year}/${month}/${day}
tempDir=${nameNode}/tmp/workflow/${wf:id()}

# Processing parameters
processDate=${year}-${month}-${day}
numReducers=10

# System properties
oozie.use.system.libpath=true
oozie.action.sharelib.for.pig=pig,hcatalog
```

**4. Workflow Validation:**
```bash
# Validate workflow XML
oozie validate -oozie http://oozie-server:11000/oozie /user/oozie/workflows/my-workflow/workflow.xml

# Dry run
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -dryrun

# Submit and run
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -run
```

### Q12: How do you manage Oozie workflow versions and environments?
**Answer:**
**Oozie Version Management:**

**1. Version Control Structure:**
```
workflows/
├── my-workflow/
│   ├── v1.0/
│   │   ├── workflow.xml
│   │   └── lib/
│   ├── v1.1/
│   │   ├── workflow.xml
│   │   └── lib/
│   └── current -> v1.1/
```

**2. Environment-specific Configuration:**
```bash
# Environment properties
# dev.properties
nameNode=hdfs://dev-namenode:8020
jobTracker=dev-resourcemanager:8032
queueName=dev-queue
inputDir=/dev/data/input
outputDir=/dev/data/output

# prod.properties
nameNode=hdfs://prod-namenode:8020
jobTracker=prod-resourcemanager:8032
queueName=prod-queue
inputDir=/prod/data/input
outputDir=/prod/data/output
```

**3. Deployment Script:**
```bash
#!/bin/bash
# deploy.sh

ENVIRONMENT=$1
VERSION=$2
WORKFLOW_NAME=$3

if [ -z "$ENVIRONMENT" ] || [ -z "$VERSION" ] || [ -z "$WORKFLOW_NAME" ]; then
    echo "Usage: $0 <environment> <version> <workflow-name>"
    exit 1
fi

# Load environment configuration
source ${ENVIRONMENT}.properties

# Deploy workflow
HDFS_PATH="/user/oozie/workflows/${WORKFLOW_NAME}/${VERSION}"
hdfs dfs -mkdir -p ${HDFS_PATH}
hdfs dfs -put workflows/${WORKFLOW_NAME}/${VERSION}/* ${HDFS_PATH}/

# Update current symlink
hdfs dfs -rm /user/oozie/workflows/${WORKFLOW_NAME}/current
hdfs dfs -ln -s ${HDFS_PATH} /user/oozie/workflows/${WORKFLOW_NAME}/current

echo "Deployed ${WORKFLOW_NAME} version ${VERSION} to ${ENVIRONMENT}"
```

**4. Configuration Templates:**
```xml
<!-- workflow-template.xml -->
<workflow-app xmlns="uri:oozie:workflow:0.5" name="${workflow.name}">
    <start to="first-action"/>
    
    <action name="first-action">
        <map-reduce>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <configuration>
                <property>
                    <name>mapred.job.queue.name</name>
                    <value>${queueName}</value>
                </property>
                <property>
                    <name>mapred.input.dir</name>
                    <value>${inputDir}</value>
                </property>
                <property>
                    <name>mapred.output.dir</name>
                    <value>${outputDir}</value>
                </property>
            </configuration>
        </map-reduce>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Workflow failed</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

---

## 📊 Monitoring & Management

### Q13: How do you monitor Oozie jobs and workflows?
**Answer:**
**Oozie Monitoring Strategies:**

**1. Web UI Monitoring:**
```bash
# Access Oozie Web UI
http://oozie-server:11000/oozie

# Key monitoring views:
# - Job list with status and progress
# - Workflow DAG visualization
# - Action logs and error messages
# - Coordinator job instances
# - Bundle job status
```

**2. Command Line Monitoring:**
```bash
# List jobs
oozie jobs -oozie http://oozie-server:11000/oozie -jobtype workflow -filter status=RUNNING

# Job details
oozie job -oozie http://oozie-server:11000/oozie -info job-id

# Job logs
oozie job -oozie http://oozie-server:11000/oozie -log job-id

# Coordinator job info
oozie job -oozie http://oozie-server:11000/oozie -info coord-job-id -len 10

# Kill job
oozie job -oozie http://oozie-server:11000/oozie -kill job-id
```

**3. REST API Monitoring:**
```bash
# Get job status via REST API
curl -X GET "http://oozie-server:11000/oozie/v1/job/job-id?show=info"

# Get job log
curl -X GET "http://oozie-server:11000/oozie/v1/job/job-id?show=log"

# Get workflow definition
curl -X GET "http://oozie-server:11000/oozie/v1/job/job-id?show=definition"
```

**4. Custom Monitoring Script:**
```bash
#!/bin/bash
# monitor-oozie.sh

OOZIE_URL="http://oozie-server:11000/oozie"
ALERT_EMAIL="admin@company.com"

# Check for failed workflows
FAILED_JOBS=$(oozie jobs -oozie $OOZIE_URL -jobtype workflow -filter status=KILLED -len 10 | grep -c KILLED)

if [ $FAILED_JOBS -gt 0 ]; then
    echo "ALERT: $FAILED_JOBS failed workflows found" | mail -s "Oozie Alert" $ALERT_EMAIL
fi

# Check for long-running jobs
LONG_RUNNING=$(oozie jobs -oozie $OOZIE_URL -jobtype workflow -filter status=RUNNING | \
               awk '{print $1, $6}' | while read job_id start_time; do
    # Calculate runtime and alert if > 4 hours
    # Implementation depends on date format
done)

# Check coordinator lag
COORD_JOBS=$(oozie jobs -oozie $OOZIE_URL -jobtype coordinator -filter status=RUNNING)
echo "$COORD_JOBS" | while read line; do
    # Check for coordinator lag
    # Implementation specific to requirements
done
```

### Q14: How do you handle Oozie job failures and recovery?
**Answer:**
**Oozie Failure Handling and Recovery:**

**1. Automatic Retry Configuration:**
```xml
<action name="retry-action" retry-max="3" retry-interval="10">
    <map-reduce>
        <!-- Action configuration -->
    </map-reduce>
    <ok to="next-action"/>
    <error to="error-handler"/>
</action>
```

**2. Manual Job Recovery:**
```bash
# Rerun failed workflow from specific action
oozie job -oozie http://oozie-server:11000/oozie -rerun job-id -Doozie.wf.rerun.skip.nodes=failed-action

# Rerun coordinator job
oozie job -oozie http://oozie-server:11000/oozie -coord-rerun coord-job-id -action 1-5

# Resume suspended job
oozie job -oozie http://oozie-server:11000/oozie -resume job-id
```

**3. Error Notification Workflow:**
```xml
<action name="error-notification">
    <email xmlns="uri:oozie:email-action:0.2">
        <to>admin@company.com,team@company.com</to>
        <cc>manager@company.com</cc>
        <subject>Workflow Failed: ${wf:name()}</subject>
        <body>
Workflow: ${wf:name()}
Job ID: ${wf:id()}
Failed Action: ${wf:lastErrorNode()}
Error Message: ${wf:errorMessage(wf:lastErrorNode())}
Error Code: ${wf:errorCode(wf:lastErrorNode())}

Please investigate and take appropriate action.
        </body>
    </email>
    <ok to="cleanup"/>
    <error to="fail"/>
</action>
```

**4. Recovery Workflow Pattern:**
```xml
<workflow-app name="recovery-workflow" xmlns="uri:oozie:workflow:0.5">
    <start to="check-previous-run"/>
    
    <decision name="check-previous-run">
        <switch>
            <case to="cleanup-previous">
                ${fs:exists(concat(wf:conf('outputDir'), '/_RUNNING'))}
            </case>
            <default to="main-processing"/>
        </switch>
    </decision>
    
    <action name="cleanup-previous">
        <fs>
            <delete path="${outputDir}"/>
            <delete path="${tempDir}"/>
        </fs>
        <ok to="main-processing"/>
        <error to="fail"/>
    </action>
    
    <action name="main-processing">
        <fs>
            <touchz path="${concat(outputDir, '/_RUNNING')}"/>
        </fs>
        <ok to="process-data"/>
        <error to="fail"/>
    </action>
    
    <action name="process-data">
        <!-- Main processing logic -->
        <ok to="mark-complete"/>
        <error to="cleanup-on-error"/>
    </action>
    
    <action name="mark-complete">
        <fs>
            <delete path="${concat(outputDir, '/_RUNNING')}"/>
            <touchz path="${concat(outputDir, '/_SUCCESS')}"/>
        </fs>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <action name="cleanup-on-error">
        <fs>
            <delete path="${outputDir}"/>
            <delete path="${tempDir}"/>
        </fs>
        <ok to="fail"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Workflow failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

---

## 🔗 Integration & Use Cases

### Q15: How do you integrate Oozie with other Hadoop ecosystem tools?
**Answer:**
**Oozie Integration Examples:**

**1. Spark Integration:**
```xml
<action name="spark-action">
    <spark xmlns="uri:oozie:spark-action:0.2">
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <master>yarn</master>
        <mode>cluster</mode>
        <name>SparkDataProcessing</name>
        <class>com.example.SparkProcessor</class>
        <jar>${nameNode}/user/oozie/lib/spark-processor.jar</jar>
        <spark-opts>--executor-memory 2g --num-executors 10</spark-opts>
        <arg>${inputDir}</arg>
        <arg>${outputDir}</arg>
        <arg>${processDate}</arg>
    </spark>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

**2. Kafka Integration:**
```xml
<action name="kafka-producer">
    <java>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <main-class>com.example.KafkaProducer</main-class>
        <java-opts>-Xmx1024m</java-opts>
        <arg>--bootstrap-servers</arg>
        <arg>${kafkaBootstrapServers}</arg>
        <arg>--topic</arg>
        <arg>${kafkaTopic}</arg>
        <arg>--input-path</arg>
        <arg>${inputDir}</arg>
        <file>kafka-producer.jar</file>
    </java>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

**3. HBase Integration:**
```xml
<action name="hbase-bulk-load">
    <java>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <main-class>org.apache.hadoop.hbase.mapreduce.LoadIncrementalHFiles</main-class>
        <arg>${hfileOutputDir}</arg>
        <arg>${hbaseTableName}</arg>
        <file>hbase-server.jar</file>
    </java>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

**4. External System Integration:**
```xml
<action name="rest-api-call">
    <shell xmlns="uri:oozie:shell-action:0.3">
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <exec>curl</exec>
        <argument>-X</argument>
        <argument>POST</argument>
        <argument>-H</argument>
        <argument>Content-Type: application/json</argument>
        <argument>-d</argument>
        <argument>{"status": "completed", "job_id": "${wf:id()}"}</argument>
        <argument>${externalApiUrl}</argument>
        <capture-output/>
    </shell>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

---

## 🌟 Real-world Scenarios

### Q16: Design a complete ETL pipeline using Oozie
**Answer:**
**Complete ETL Pipeline Design:**

**1. Pipeline Architecture:**
```
Data Sources → Ingestion → Processing → Quality Checks → Loading → Notification
```

**2. Main Workflow (etl-pipeline.xml):**
```xml
<workflow-app name="etl-pipeline" xmlns="uri:oozie:workflow:0.5">
    <start to="data-ingestion"/>
    
    <!-- Data Ingestion Phase -->
    <action name="data-ingestion">
        <sqoop xmlns="uri:oozie:sqoop-action:0.4">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <command>import --connect ${dbUrl} --username ${dbUser} --password-file ${passwordFile} --table ${sourceTable} --target-dir ${rawDataDir} --incremental append --check-column ${incrementalColumn} --last-value ${lastValue}</command>
        </sqoop>
        <ok to="data-validation"/>
        <error to="ingestion-failure"/>
    </action>
    
    <!-- Data Validation -->
    <action name="data-validation">
        <pig>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>validate-data.pig</script>
            <param>INPUT=${rawDataDir}</param>
            <param>OUTPUT=${validatedDataDir}</param>
            <param>ERROR_OUTPUT=${errorDataDir}</param>
            <param>PROCESS_DATE=${processDate}</param>
        </pig>
        <ok to="check-validation-results"/>
        <error to="validation-failure"/>
    </action>
    
    <!-- Check Validation Results -->
    <decision name="check-validation-results">
        <switch>
            <case to="data-transformation">
                ${fs:fileSize(concat(errorDataDir, '/part-r-00000')) lt 1000}
            </case>
            <default to="validation-failure"/>
        </switch>
    </decision>
    
    <!-- Data Transformation -->
    <fork name="parallel-transformation">
        <path start="customer-transformation"/>
        <path start="order-transformation"/>
        <path start="product-transformation"/>
    </fork>
    
    <action name="customer-transformation">
        <hive xmlns="uri:oozie:hive-action:0.5">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>transform-customers.hql</script>
            <param>INPUT_TABLE=${rawCustomerTable}</param>
            <param>OUTPUT_TABLE=${transformedCustomerTable}</param>
            <param>PROCESS_DATE=${processDate}</param>
        </hive>
        <ok to="join-transformations"/>
        <error to="transformation-failure"/>
    </action>
    
    <action name="order-transformation">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>OrderTransformation</name>
            <class>com.example.OrderTransformer</class>
            <jar>order-transformer.jar</jar>
            <arg>${rawOrderDir}</arg>
            <arg>${transformedOrderDir}</arg>
            <arg>${processDate}</arg>
        </spark>
        <ok to="join-transformations"/>
        <error to="transformation-failure"/>
    </action>
    
    <action name="product-transformation">
        <map-reduce>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <configuration>
                <property>
                    <name>mapred.mapper.class</name>
                    <value>com.example.ProductMapper</value>
                </property>
                <property>
                    <name>mapred.reducer.class</name>
                    <value>com.example.ProductReducer</value>
                </property>
                <property>
                    <name>mapred.input.dir</name>
                    <value>${rawProductDir}</value>
                </property>
                <property>
                    <name>mapred.output.dir</name>
                    <value>${transformedProductDir}</value>
                </property>
            </configuration>
        </map-reduce>
        <ok to="join-transformations"/>
        <error to="transformation-failure"/>
    </action>
    
    <join name="join-transformations" to="data-quality-checks"/>
    
    <!-- Data Quality Checks -->
    <action name="data-quality-checks">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.example.DataQualityChecker</main-class>
            <arg>${transformedCustomerTable}</arg>
            <arg>${transformedOrderDir}</arg>
            <arg>${transformedProductDir}</arg>
            <arg>${qualityReportDir}</arg>
            <file>data-quality-checker.jar</file>
        </java>
        <ok to="check-quality-results"/>
        <error to="quality-check-failure"/>
    </action>
    
    <!-- Check Quality Results -->
    <decision name="check-quality-results">
        <switch>
            <case to="data-loading">
                ${wf:actionData('data-quality-checks')['quality_score'] gt 0.95}
            </case>
            <default to="quality-failure"/>
        </switch>
    </decision>
    
    <!-- Data Loading -->
    <action name="data-loading">
        <sqoop xmlns="uri:oozie:sqoop-action:0.4">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <command>export --connect ${warehouseDbUrl} --username ${warehouseUser} --password-file ${warehousePasswordFile} --table ${targetTable} --export-dir ${transformedDataDir} --update-mode allowinsert --update-key id</command>
        </sqoop>
        <ok to="success-notification"/>
        <error to="loading-failure"/>
    </action>
    
    <!-- Success Notification -->
    <action name="success-notification">
        <email xmlns="uri:oozie:email-action:0.2">
            <to>team@company.com</to>
            <subject>ETL Pipeline Completed Successfully - ${processDate}</subject>
            <body>
ETL Pipeline: ${wf:name()}
Process Date: ${processDate}
Job ID: ${wf:id()}
Status: SUCCESS

Records Processed:
- Customers: ${wf:actionData('customer-transformation')['record_count']}
- Orders: ${wf:actionData('order-transformation')['record_count']}
- Products: ${wf:actionData('product-transformation')['record_count']}

Quality Score: ${wf:actionData('data-quality-checks')['quality_score']}

Pipeline completed successfully.
            </body>
        </email>
        <ok to="cleanup"/>
        <error to="end"/>
    </action>
    
    <!-- Cleanup -->
    <action name="cleanup">
        <fs>
            <delete path="${tempDir}"/>
            <delete path="${errorDataDir}"/>
        </fs>
        <ok to="end"/>
        <error to="end"/>
    </action>
    
    <!-- Error Handlers -->
    <action name="ingestion-failure">
        <email xmlns="uri:oozie:email-action:0.2">
            <to>admin@company.com</to>
            <subject>ETL Pipeline Failed - Data Ingestion</subject>
            <body>Data ingestion failed for ${processDate}. Error: ${wf:errorMessage(wf:lastErrorNode())}</body>
        </email>
        <ok to="fail"/>
        <error to="fail"/>
    </action>
    
    <action name="validation-failure">
        <email xmlns="uri:oozie:email-action:0.2">
            <to>admin@company.com</to>
            <subject>ETL Pipeline Failed - Data Validation</subject>
            <body>Data validation failed for ${processDate}. Check error data at ${errorDataDir}</body>
        </email>
        <ok to="fail"/>
        <error to="fail"/>
    </action>
    
    <action name="transformation-failure">
        <email xmlns="uri:oozie:email-action:0.2">
            <to>admin@company.com</to>
            <subject>ETL Pipeline Failed - Data Transformation</subject>
            <body>Data transformation failed for ${processDate}. Error: ${wf:errorMessage(wf:lastErrorNode())}</body>
        </email>
        <ok to="fail"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>ETL Pipeline failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**3. Coordinator Configuration:**
```xml
<coordinator-app name="daily-etl-coordinator" 
                 frequency="${coord:days(1)}" 
                 start="${startTime}" 
                 end="${endTime}" 
                 timezone="UTC"
                 xmlns="uri:oozie:coordinator:0.4">
    
    <datasets>
        <dataset name="source-data" frequency="${coord:days(1)}" 
                 initial-instance="${startTime}" timezone="UTC">
            <uri-template>/data/source/${YEAR}/${MONTH}/${DAY}</uri-template>
            <done-flag>_SUCCESS</done-flag>
        </dataset>
    </datasets>
    
    <input-events>
        <data-in name="input" dataset="source-data">
            <instance>${coord:current(0)}</instance>
        </data-in>
    </input-events>
    
    <action>
        <workflow>
            <app-path>/user/oozie/workflows/etl-pipeline</app-path>
            <configuration>
                <property>
                    <name>processDate</name>
                    <value>${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd')}</value>
                </property>
                <property>
                    <name>rawDataDir</name>
                    <value>/data/raw/${coord:formatTime(coord:nominalTime(), 'yyyy/MM/dd')}</value>
                </property>
                <property>
                    <name>transformedDataDir</name>
                    <value>/data/transformed/${coord:formatTime(coord:nominalTime(), 'yyyy/MM/dd')}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

---

## 📚 Additional Resources

### Best Practices Summary
1. **Workflow Design**: Keep workflows modular and reusable
2. **Error Handling**: Implement comprehensive error handling and notifications
3. **Resource Management**: Use appropriate queue configurations and resource limits
4. **Monitoring**: Set up proactive monitoring and alerting
5. **Version Control**: Maintain proper version control and deployment processes

### Recommended Reading
- Apache Oozie Official Documentation
- "Hadoop: The Definitive Guide" - Oozie chapter
- Oozie best practices guides

### Hands-on Practice
- Local Oozie setup with Hadoop
- Complex workflow development
- Coordinator and bundle configuration
- Integration with various Hadoop tools

---

*This comprehensive guide covers essential Apache Oozie concepts for workflow orchestration and data engineering roles. Practice with complex multi-step workflows to master Oozie development and deployment.*