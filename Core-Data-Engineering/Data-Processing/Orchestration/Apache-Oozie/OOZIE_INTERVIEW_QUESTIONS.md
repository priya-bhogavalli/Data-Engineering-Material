# Apache Oozie Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Basic Level Questions](#-basic-level-questions)
2. [Intermediate Level Questions](#-intermediate-level-questions)
3. [Advanced Level Questions](#-advanced-level-questions)
4. [Architecture & Performance](#-architecture--performance)
5. [Streaming & Real-time Processing](#-streaming--real-time-processing)
6. [Production & Operations](#-production--operations)
7. [Scenario-Based Questions](#-scenario-based-questions)

---

## 🟢 Basic Level Questions

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

### Q2: Explain the different types of Oozie jobs
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

### Q3: What are the core components of Oozie architecture?
**Answer:**
**Oozie Architecture Components:**

**1. Oozie Server**
- Web application running on servlet container
- Processes workflow definitions
- Manages job execution and state
- Provides REST API and web UI

**2. Oozie Client**
- Command-line tool for job submission
- REST API client libraries
- Web UI for monitoring

**3. Database**
- Stores workflow definitions and execution state
- Supports MySQL, PostgreSQL, Oracle, etc.
- Maintains job history and metadata

**4. HDFS Integration**
- Workflow definitions stored in HDFS
- Application JARs and configuration files
- Job logs and output data

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
        <message>Workflow failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**2. Job Properties (job.properties):**
```properties
nameNode=hdfs://namenode:8020
jobTracker=resourcemanager:8032
oozie.wf.application.path=${nameNode}/user/oozie/workflows/sample-workflow
inputDir=${nameNode}/user/data/input
outputDir=${nameNode}/user/data/output
```

### Q5: What are Oozie workflow control nodes?
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
</fork>

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

### Q7: What are the different action types supported by Oozie?
**Answer:**
**Oozie Action Types:**

**1. Hadoop Ecosystem Actions:**
- **MapReduce**: Execute MapReduce jobs
- **Pig**: Run Pig scripts
- **Hive**: Execute HiveQL queries
- **Sqoop**: Data import/export operations
- **Spark**: Execute Spark applications

**2. System Actions:**
- **Shell**: Run shell scripts
- **Java**: Execute Java applications
- **SSH**: Remote command execution
- **FS**: File system operations

**3. Notification Actions:**
- **Email**: Send email notifications
- **JMS**: Java Message Service integration

**Example Action:**
```xml
<action name="pig-processing">
    <pig>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <script>process-data.pig</script>
        <param>INPUT=${inputDir}</param>
        <param>OUTPUT=${outputDir}</param>
    </pig>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

### Q8: How do you submit and monitor Oozie jobs?
**Answer:**
**Job Submission:**

**1. Command Line Submission:**
```bash
# Submit workflow
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -submit

# Run workflow
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -run

# Submit and run in one command
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -run
```

**2. Job Monitoring:**
```bash
# Check job status
oozie job -oozie http://oozie-server:11000/oozie -info job-id

# Check job logs
oozie job -oozie http://oozie-server:11000/oozie -log job-id

# List all jobs
oozie jobs -oozie http://oozie-server:11000/oozie -jobtype workflow
```

**3. Web UI Monitoring:**
- Access Oozie Web Console at `http://oozie-server:11000/oozie`
- View job status, workflow graph, and logs
- Monitor coordinator and bundle jobs

### Q9: What is the difference between workflow, coordinator, and bundle jobs?
**Answer:**
**Job Type Comparison:**

| **Aspect** | **Workflow** | **Coordinator** | **Bundle** |
|------------|--------------|-----------------|------------|
| **Purpose** | Single workflow execution | Schedule multiple workflows | Group multiple coordinators |
| **Execution** | One-time or triggered | Recurring based on schedule | Manages coordinator lifecycle |
| **Dependencies** | Action dependencies | Time and data dependencies | Coordinator dependencies |
| **Scheduling** | Immediate or external | Built-in time/data scheduling | Coordinator-level scheduling |
| **Scope** | Single DAG | Multiple workflow instances | Multiple coordinator jobs |
| **Use Case** | ETL pipeline | Daily/hourly batch jobs | Complete data platform |

**Example Hierarchy:**
```
Bundle: "Data Platform"
├── Coordinator: "Daily Ingestion" → Workflows: ingest-2024-01-01, ingest-2024-01-02...
├── Coordinator: "Hourly Processing" → Workflows: process-01:00, process-02:00...
└── Coordinator: "Weekly Reports" → Workflows: report-week-1, report-week-2...
```

### Q10: How do you configure Oozie coordinators for scheduling?
**Answer:**
**Coordinator Configuration:**

**1. Basic Time-based Scheduling:**
```xml
<coordinator-app name="daily-etl" 
                 frequency="${coord:days(1)}" 
                 start="2024-01-01T02:00Z" 
                 end="2024-12-31T02:00Z" 
                 timezone="UTC">
    
    <action>
        <workflow>
            <app-path>${workflowPath}</app-path>
            <configuration>
                <property>
                    <name>inputDir</name>
                    <value>/data/input/${coord:formatTime(coord:nominalTime(), 'yyyy/MM/dd')}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

**2. Data Dependency Configuration:**
```xml
<datasets>
    <dataset name="input-data" frequency="${coord:days(1)}" 
             initial-instance="2024-01-01T00:00Z" timezone="UTC">
        <uri-template>/data/input/${YEAR}/${MONTH}/${DAY}</uri-template>
        <done-flag>_SUCCESS</done-flag>
    </dataset>
</datasets>

<input-events>
    <data-in name="input" dataset="input-data">
        <instance>${coord:current(0)}</instance>
    </data-in>
</input-events>
```

**3. Frequency Options:**
- `${coord:minutes(30)}` - Every 30 minutes
- `${coord:hours(2)}` - Every 2 hours
- `${coord:days(1)}` - Daily
- `${coord:months(1)}` - Monthly

---

*[Continuing with more questions in the next batch...]*
# Apache Oozie Interview Questions for Data Engineering

## 📋 Table of Contents

1. [Basic Level Questions](#-basic-level-questions)
2. [Intermediate Level Questions](#-intermediate-level-questions)
3. [Advanced Level Questions](#-advanced-level-questions)
4. [Architecture & Performance](#-architecture--performance)
5. [Streaming & Real-time Processing](#-streaming--real-time-processing)
6. [Production & Operations](#-production--operations)
7. [Scenario-Based Questions](#-scenario-based-questions)

---

## 🟢 Basic Level Questions

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

### Q2: Explain the different types of Oozie jobs
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

### Q3: What are the core components of Oozie architecture?
**Answer:**
**Oozie Architecture Components:**

**1. Oozie Server**
- Web application running on servlet container
- Processes workflow definitions
- Manages job execution and state
- Provides REST API and web UI

**2. Oozie Client**
- Command-line tool for job submission
- REST API client libraries
- Web UI for monitoring

**3. Database**
- Stores workflow definitions and execution state
- Supports MySQL, PostgreSQL, Oracle, etc.
- Maintains job history and metadata

**4. HDFS Integration**
- Workflow definitions stored in HDFS
- Application JARs and configuration files
- Job logs and output data

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
        <message>Workflow failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**2. Job Properties (job.properties):**
```properties
nameNode=hdfs://namenode:8020
jobTracker=resourcemanager:8032
oozie.wf.application.path=${nameNode}/user/oozie/workflows/sample-workflow
inputDir=${nameNode}/user/data/input
outputDir=${nameNode}/user/data/output
```

### Q5: What are Oozie workflow control nodes?
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
</fork>

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

### Q7: What are the different action types supported by Oozie?
**Answer:**
**Oozie Action Types:**

**1. Hadoop Ecosystem Actions:**
- **MapReduce**: Execute MapReduce jobs
- **Pig**: Run Pig scripts
- **Hive**: Execute HiveQL queries
- **Sqoop**: Data import/export operations
- **Spark**: Execute Spark applications

**2. System Actions:**
- **Shell**: Run shell scripts
- **Java**: Execute Java applications
- **SSH**: Remote command execution
- **FS**: File system operations

**3. Notification Actions:**
- **Email**: Send email notifications
- **JMS**: Java Message Service integration

**Example Action:**
```xml
<action name="pig-processing">
    <pig>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <script>process-data.pig</script>
        <param>INPUT=${inputDir}</param>
        <param>OUTPUT=${outputDir}</param>
    </pig>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

### Q8: How do you submit and monitor Oozie jobs?
**Answer:**
**Job Submission:**

**1. Command Line Submission:**
```bash
# Submit workflow
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -submit

# Run workflow
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -run

# Submit and run in one command
oozie job -oozie http://oozie-server:11000/oozie -config job.properties -run
```

**2. Job Monitoring:**
```bash
# Check job status
oozie job -oozie http://oozie-server:11000/oozie -info job-id

# Check job logs
oozie job -oozie http://oozie-server:11000/oozie -log job-id

# List all jobs
oozie jobs -oozie http://oozie-server:11000/oozie -jobtype workflow
```

**3. Web UI Monitoring:**
- Access Oozie Web Console at `http://oozie-server:11000/oozie`
- View job status, workflow graph, and logs
- Monitor coordinator and bundle jobs

### Q9: What is the difference between workflow, coordinator, and bundle jobs?
**Answer:**
**Job Type Comparison:**

| **Aspect** | **Workflow** | **Coordinator** | **Bundle** |
|------------|--------------|-----------------|------------|
| **Purpose** | Single workflow execution | Schedule multiple workflows | Group multiple coordinators |
| **Execution** | One-time or triggered | Recurring based on schedule | Manages coordinator lifecycle |
| **Dependencies** | Action dependencies | Time and data dependencies | Coordinator dependencies |
| **Scheduling** | Immediate or external | Built-in time/data scheduling | Coordinator-level scheduling |
| **Scope** | Single DAG | Multiple workflow instances | Multiple coordinator jobs |
| **Use Case** | ETL pipeline | Daily/hourly batch jobs | Complete data platform |

**Example Hierarchy:**
```
Bundle: "Data Platform"
├── Coordinator: "Daily Ingestion" → Workflows: ingest-2024-01-01, ingest-2024-01-02...
├── Coordinator: "Hourly Processing" → Workflows: process-01:00, process-02:00...
└── Coordinator: "Weekly Reports" → Workflows: report-week-1, report-week-2...
```

### Q10: How do you configure Oozie coordinators for scheduling?
**Answer:**
**Coordinator Configuration:**

**1. Basic Time-based Scheduling:**
```xml
<coordinator-app name="daily-etl" 
                 frequency="${coord:days(1)}" 
                 start="2024-01-01T02:00Z" 
                 end="2024-12-31T02:00Z" 
                 timezone="UTC">
    
    <action>
        <workflow>
            <app-path>${workflowPath}</app-path>
            <configuration>
                <property>
                    <name>inputDir</name>
                    <value>/data/input/${coord:formatTime(coord:nominalTime(), 'yyyy/MM/dd')}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

**2. Data Dependency Configuration:**
```xml
<datasets>
    <dataset name="input-data" frequency="${coord:days(1)}" 
             initial-instance="2024-01-01T00:00Z" timezone="UTC">
        <uri-template>/data/input/${YEAR}/${MONTH}/${DAY}</uri-template>
        <done-flag>_SUCCESS</done-flag>
    </dataset>
</datasets>

<input-events>
    <data-in name="input" dataset="input-data">
        <instance>${coord:current(0)}</instance>
    </data-in>
</input-events>
```

**3. Frequency Options:**
- `${coord:minutes(30)}` - Every 30 minutes
- `${coord:hours(2)}` - Every 2 hours
- `${coord:days(1)}` - Daily
- `${coord:months(1)}` - Monthly

---

## 🟡 Intermediate Level Questions

### Q11: How do you implement complex data dependencies in Oozie coordinators?
**Answer:**
**Complex Data Dependencies:**

**1. Multiple Dataset Dependencies:**
```xml
<datasets>
    <dataset name="raw-logs" frequency="${coord:days(1)}" 
             initial-instance="2024-01-01T00:00Z" timezone="UTC">
        <uri-template>/data/raw/logs/${YEAR}/${MONTH}/${DAY}</uri-template>
        <done-flag>_SUCCESS</done-flag>
    </dataset>
    
    <dataset name="reference-data" frequency="${coord:days(7)}" 
             initial-instance="2024-01-01T00:00Z" timezone="UTC">
        <uri-template>/data/reference/${YEAR}/${MONTH}/${DAY}</uri-template>
        <done-flag>_READY</done-flag>
    </dataset>
    
    <dataset name="config-data" frequency="${coord:months(1)}" 
             initial-instance="2024-01-01T00:00Z" timezone="UTC">
        <uri-template>/data/config/${YEAR}/${MONTH}</uri-template>
        <done-flag>_COMPLETE</done-flag>
    </dataset>
</datasets>

<input-events>
    <!-- Wait for current day's logs -->
    <data-in name="daily-logs" dataset="raw-logs">
        <instance>${coord:current(0)}</instance>
    </data-in>
    
    <!-- Wait for latest weekly reference data -->
    <data-in name="weekly-ref" dataset="reference-data">
        <instance>${coord:latest(0)}</instance>
    </data-in>
    
    <!-- Wait for current month's config -->
    <data-in name="monthly-config" dataset="config-data">
        <instance>${coord:current(0)}</instance>
    </data-in>
</input-events>
```

**2. Range-based Dependencies:**
```xml
<input-events>
    <!-- Wait for last 7 days of data -->
    <data-in name="weekly-data" dataset="daily-sales">
        <start-instance>${coord:current(-6)}</start-instance>
        <end-instance>${coord:current(0)}</end-instance>
    </data-in>
</input-events>
```

**3. Conditional Dependencies:**
```xml
<action>
    <workflow>
        <app-path>${workflowPath}</app-path>
        <configuration>
            <property>
                <name>hasReferenceData</name>
                <value>${coord:dataIn('weekly-ref') != ""}</value>
            </property>
            <property>
                <name>inputPaths</name>
                <value>${coord:dataIn('daily-logs')},${coord:dataIn('weekly-ref')}</value>
            </property>
        </configuration>
    </workflow>
</action>
```

### Q12: Explain Oozie EL (Expression Language) functions and their usage
**Answer:**
**Oozie Expression Language Functions:**

**1. Workflow Functions (wf:):**
```xml
<!-- Get workflow configuration -->
${wf:conf('inputDir')}

<!-- Get workflow ID -->
${wf:id()}

<!-- Get workflow name -->
${wf:name()}

<!-- Get error information -->
${wf:errorMessage(wf:lastErrorNode())}
${wf:errorCode(wf:lastErrorNode())}

<!-- Get action data -->
${wf:actionData('action-name')['key']}

<!-- Get workflow run number -->
${wf:run()}
```

**2. Coordinator Functions (coord:):**
```xml
<!-- Time functions -->
${coord:current(0)}          <!-- Current instance -->
${coord:current(-1)}         <!-- Previous instance -->
${coord:latest(0)}           <!-- Latest available data -->

<!-- Date formatting -->
${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd')}
${coord:formatTime(coord:actualTime(), 'yyyy/MM/dd/HH')}

<!-- Data functions -->
${coord:dataIn('dataset-name')}
${coord:dataOut('dataset-name')}

<!-- Frequency functions -->
${coord:days(1)}
${coord:hours(6)}
${coord:minutes(30)}
```

**3. File System Functions (fs:):**
```xml
<!-- Check file existence -->
${fs:exists('/data/input/file.txt')}

<!-- Get file size -->
${fs:fileSize('/data/input/file.txt')}

<!-- Check directory -->
${fs:isDir('/data/input')}

<!-- Get directory size -->
${fs:dirSize('/data/input')}
```

**4. Hadoop Functions (hadoop:):**
```xml
<!-- Get Hadoop counters -->
${hadoop:counters('action-name')['GROUP']['COUNTER']}
```

### Q13: How do you implement parallel processing in Oozie workflows?
**Answer:**
**Parallel Processing Implementation:**

**1. Fork-Join Pattern:**
```xml
<workflow-app name="parallel-processing" xmlns="uri:oozie:workflow:0.5">
    <start to="prepare-data"/>
    
    <action name="prepare-data">
        <fs>
            <mkdir path="${outputDir}/region1"/>
            <mkdir path="${outputDir}/region2"/>
            <mkdir path="${outputDir}/region3"/>
        </fs>
        <ok to="parallel-fork"/>
        <error to="fail"/>
    </action>
    
    <fork name="parallel-fork">
        <path start="process-region1"/>
        <path start="process-region2"/>
        <path start="process-region3"/>
    </fork>
    
    <action name="process-region1">
        <map-reduce>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <configuration>
                <property>
                    <name>mapred.input.dir</name>
                    <value>${inputDir}/region1</value>
                </property>
                <property>
                    <name>mapred.output.dir</name>
                    <value>${outputDir}/region1</value>
                </property>
            </configuration>
        </map-reduce>
        <ok to="parallel-join"/>
        <error to="fail"/>
    </action>
    
    <action name="process-region2">
        <pig>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>process-region2.pig</script>
            <param>INPUT=${inputDir}/region2</param>
            <param>OUTPUT=${outputDir}/region2</param>
        </pig>
        <ok to="parallel-join"/>
        <error to="fail"/>
    </action>
    
    <action name="process-region3">
        <hive xmlns="uri:oozie:hive-action:0.5">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>process-region3.hql</script>
            <param>INPUT=${inputDir}/region3</param>
            <param>OUTPUT=${outputDir}/region3</param>
        </hive>
        <ok to="parallel-join"/>
        <error to="fail"/>
    </action>
    
    <join name="parallel-join" to="aggregate-results"/>
    
    <action name="aggregate-results">
        <map-reduce>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <configuration>
                <property>
                    <name>mapred.input.dir</name>
                    <value>${outputDir}/region1,${outputDir}/region2,${outputDir}/region3</value>
                </property>
                <property>
                    <name>mapred.output.dir</name>
                    <value>${outputDir}/final</value>
                </property>
            </configuration>
        </map-reduce>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Parallel processing failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**2. Nested Fork-Join:**
```xml
<fork name="main-fork">
    <path start="data-ingestion-fork"/>
    <path start="data-validation"/>
</fork>

<fork name="data-ingestion-fork">
    <path start="ingest-source1"/>
    <path start="ingest-source2"/>
</fork>

<action name="ingest-source1">
    <!-- Ingestion logic -->
    <ok to="ingestion-join"/>
    <error to="fail"/>
</action>

<action name="ingest-source2">
    <!-- Ingestion logic -->
    <ok to="ingestion-join"/>
    <error to="fail"/>
</action>

<join name="ingestion-join" to="main-join"/>
<join name="main-join" to="final-processing"/>
```

### Q14: How do you configure SLA monitoring in Oozie?
**Answer:**
**SLA (Service Level Agreement) Configuration:**

**1. Workflow SLA:**
```xml
<workflow-app name="sla-workflow" xmlns="uri:oozie:workflow:0.5" 
               xmlns:sla="uri:oozie:sla:0.2">
    
    <start to="data-processing"/>
    
    <action name="data-processing">
        <map-reduce>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <!-- MapReduce configuration -->
        </map-reduce>
        <ok to="end"/>
        <error to="fail"/>
        
        <sla:info>
            <sla:nominal-time>${nominalTime}</sla:nominal-time>
            <sla:should-start>15</sla:should-start>
            <sla:should-end>60</sla:should-end>
            <sla:max-duration>120</sla:max-duration>
            <sla:alert-events>start_miss,end_miss,duration_miss</sla:alert-events>
            <sla:alert-contact>team@company.com</sla:alert-contact>
            <sla:notification-msg>Data processing SLA violation</sla:notification-msg>
        </sla:info>
    </action>
    
    <kill name="fail">
        <message>Workflow failed</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**2. Coordinator SLA:**
```xml
<coordinator-app name="sla-coordinator" xmlns="uri:oozie:coordinator:0.4"
                 xmlns:sla="uri:oozie:sla:0.2">
    
    <action>
        <workflow>
            <app-path>${workflowPath}</app-path>
        </workflow>
        
        <sla:info>
            <sla:nominal-time>${coord:nominalTime()}</sla:nominal-time>
            <sla:should-start>30</sla:should-start>
            <sla:should-end>180</sla:should-end>
            <sla:max-duration>240</sla:max-duration>
            <sla:alert-events>start_miss,end_miss,duration_miss</sla:alert-events>
            <sla:alert-contact>ops-team@company.com,manager@company.com</sla:alert-contact>
            <sla:notification-msg>Daily ETL SLA breach for ${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd')}</sla:notification-msg>
        </sla:info>
    </action>
</coordinator-app>
```

**3. SLA Parameters:**
- **nominal-time**: Expected execution time
- **should-start**: Minutes after nominal time when job should start
- **should-end**: Minutes after nominal time when job should complete
- **max-duration**: Maximum allowed duration in minutes
- **alert-events**: Types of SLA violations to monitor
- **alert-contact**: Email addresses for notifications

### Q15: How do you handle dynamic parameter passing in Oozie workflows?
**Answer:**
**Dynamic Parameter Handling:**

**1. Coordinator to Workflow Parameter Passing:**
```xml
<!-- Coordinator -->
<coordinator-app name="dynamic-params">
    <action>
        <workflow>
            <app-path>${workflowPath}</app-path>
            <configuration>
                <property>
                    <name>processDate</name>
                    <value>${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd')}</value>
                </property>
                <property>
                    <name>inputPath</name>
                    <value>/data/input/${coord:formatTime(coord:nominalTime(), 'yyyy/MM/dd')}</value>
                </property>
                <property>
                    <name>outputPath</name>
                    <value>/data/output/${coord:formatTime(coord:nominalTime(), 'yyyy/MM/dd')}</value>
                </property>
                <property>
                    <name>runId</name>
                    <value>${coord:formatTime(coord:actualTime(), 'yyyyMMdd-HHmmss')}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

**2. Workflow Parameter Usage:**
```xml
<!-- Workflow -->
<workflow-app name="parameterized-workflow">
    <parameters>
        <property>
            <name>processDate</name>
            <description>Date to process in yyyy-MM-dd format</description>
        </property>
        <property>
            <name>inputPath</name>
            <description>Input data path</description>
        </property>
        <property>
            <name>outputPath</name>
            <description>Output data path</description>
        </property>
    </parameters>
    
    <start to="validate-params"/>
    
    <decision name="validate-params">
        <switch>
            <case to="process-data">
                ${fs:exists(wf:conf('inputPath'))}
            </case>
            <default to="create-empty-output"/>
        </switch>
    </decision>
    
    <action name="process-data">
        <pig>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>process-data.pig</script>
            <param>PROCESS_DATE=${processDate}</param>
            <param>INPUT_PATH=${inputPath}</param>
            <param>OUTPUT_PATH=${outputPath}</param>
            <param>RUN_ID=${runId}</param>
        </pig>
        <ok to="end"/>
        <error to="fail"/>
    </action>
</workflow-app>
```

**3. Action Data Sharing:**
```xml
<action name="count-records">
    <java>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <main-class>com.company.RecordCounter</main-class>
        <arg>${inputPath}</arg>
        <capture-output/>
    </java>
    <ok to="process-based-on-count"/>
    <error to="fail"/>
</action>

<decision name="process-based-on-count">
    <switch>
        <case to="large-dataset-processing">
            ${wf:actionData('count-records')['recordCount'] gt 1000000}
        </case>
        <case to="small-dataset-processing">
            ${wf:actionData('count-records')['recordCount'] le 1000000}
        </case>
        <default to="fail"/>
    </switch>
</decision>
```

### Q16: How do you implement email notifications in Oozie workflows?
**Answer:**
**Email Notification Implementation:**

**1. Basic Email Action:**
```xml
<action name="send-success-notification">
    <email xmlns="uri:oozie:email-action:0.2">
        <to>team@company.com</to>
        <cc>manager@company.com</cc>
        <bcc>audit@company.com</bcc>
        <subject>ETL Job Completed Successfully - ${wf:conf('processDate')}</subject>
        <body>
            Dear Team,
            
            The daily ETL job has completed successfully.
            
            Details:
            - Job ID: ${wf:id()}
            - Process Date: ${wf:conf('processDate')}
            - Start Time: ${wf:conf('startTime')}
            - Input Path: ${wf:conf('inputPath')}
            - Output Path: ${wf:conf('outputPath')}
            - Records Processed: ${wf:actionData('count-records')['totalRecords']}
            
            Best regards,
            Oozie Workflow System
        </body>
        <content_type>text/plain</content_type>
    </email>
    <ok to="end"/>
    <error to="fail"/>
</action>
```

**2. HTML Email with Attachments:**
```xml
<action name="send-report-email">
    <email xmlns="uri:oozie:email-action:0.2">
        <to>executives@company.com</to>
        <subject>Daily Business Report - ${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd')}</subject>
        <body>
            <![CDATA[
            <html>
            <body>
                <h2>Daily Business Report</h2>
                <p>Please find the daily business report attached.</p>
                
                <table border="1">
                    <tr><th>Metric</th><th>Value</th></tr>
                    <tr><td>Total Sales</td><td>${wf:actionData('calculate-sales')['totalSales']}</td></tr>
                    <tr><td>New Customers</td><td>${wf:actionData('count-customers')['newCustomers']}</td></tr>
                    <tr><td>Processing Time</td><td>${wf:actionData('process-data')['duration']} minutes</td></tr>
                </table>
                
                <p>Report generated at: ${wf:conf('reportTime')}</p>
            </body>
            </html>
            ]]>
        </body>
        <content_type>text/html</content_type>
        <attachment>/reports/daily-report-${wf:conf('processDate')}.pdf</attachment>
        <attachment>/reports/sales-summary-${wf:conf('processDate')}.csv</attachment>
    </email>
    <ok to="end"/>
    <error to="fail"/>
</action>
```

**3. Conditional Email Notifications:**
```xml
<decision name="check-error-severity">
    <switch>
        <case to="send-critical-alert">
            ${wf:actionData('validate-data')['errorCount'] gt 1000}
        </case>
        <case to="send-warning-email">
            ${wf:actionData('validate-data')['errorCount'] gt 100}
        </case>
        <default to="send-success-notification"/>
    </switch>
</decision>

<action name="send-critical-alert">
    <email xmlns="uri:oozie:email-action:0.2">
        <to>oncall@company.com</to>
        <cc>manager@company.com</cc>
        <subject>CRITICAL: High Error Count in ETL Job - ${wf:conf('processDate')}</subject>
        <body>
            CRITICAL ALERT: ETL job has encountered ${wf:actionData('validate-data')['errorCount']} errors.
            
            Immediate action required.
            
            Job Details:
            - Job ID: ${wf:id()}
            - Error Count: ${wf:actionData('validate-data')['errorCount']}
            - Error Rate: ${wf:actionData('validate-data')['errorRate']}%
        </body>
    </email>
    <ok to="end"/>
    <error to="fail"/>
</action>
```

### Q17: How do you configure Oozie for high availability?
**Answer:**
**High Availability Configuration:**

**1. Database High Availability:**
```xml
<!-- oozie-site.xml -->
<configuration>
    <!-- Primary database connection -->
    <property>
        <name>oozie.service.JPAService.jdbc.url</name>
        <value>jdbc:mysql://db-primary:3306,db-secondary:3306/oozie?failOverReadOnly=false&amp;autoReconnect=true</value>
    </property>
    
    <!-- Connection pool settings -->
    <property>
        <name>oozie.service.JPAService.pool.max.active.conn</name>
        <value>50</value>
    </property>
    
    <!-- Enable connection validation -->
    <property>
        <name>oozie.service.JPAService.validate.db.connection</name>
        <value>true</value>
    </property>
</configuration>
```

**2. Load Balancer Configuration:**
```bash
# HAProxy configuration for Oozie servers
backend oozie_servers
    balance roundrobin
    option httpchk GET /oozie/v1/admin/status
    server oozie1 oozie-server1:11000 check
    server oozie2 oozie-server2:11000 check
    server oozie3 oozie-server3:11000 check

frontend oozie_frontend
    bind *:11000
    default_backend oozie_servers
```

**3. Shared Storage Configuration:**
```xml
<!-- Ensure HDFS is configured for HA -->
<property>
    <name>oozie.service.HadoopAccessorService.hadoop.configurations</name>
    <value>*=/etc/hadoop/conf</value>
</property>

<!-- Configure shared lib directory -->
<property>
    <name>oozie.service.WorkflowAppService.system.libpath</name>
    <value>/user/oozie/share/lib</value>
</property>
```

**4. Health Check and Monitoring:**
```bash
#!/bin/bash
# Health check script
OOZIE_URL="http://localhost:11000/oozie"

# Check server status
STATUS=$(curl -s "${OOZIE_URL}/v1/admin/status" | grep -o '"systemMode":"[^"]*"' | cut -d'"' -f4)

if [ "$STATUS" = "NORMAL" ]; then
    echo "Oozie server is healthy"
    exit 0
else
    echo "Oozie server is unhealthy: $STATUS"
    exit 1
fi
```

### Q18: How do you implement custom actions in Oozie?
**Answer:**
**Custom Action Implementation:**

**1. Java Action Example:**
```java
// Custom Java action
public class DataValidationAction {
    public static void main(String[] args) throws Exception {
        String inputPath = args[0];
        String outputPath = args[1];
        String threshold = args[2];
        
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        
        // Validation logic
        long recordCount = validateData(inputPath, fs);
        double errorRate = calculateErrorRate(inputPath, fs);
        
        // Write results for workflow to use
        Properties props = new Properties();
        props.setProperty("recordCount", String.valueOf(recordCount));
        props.setProperty("errorRate", String.valueOf(errorRate));
        props.setProperty("validationStatus", errorRate < Double.parseDouble(threshold) ? "PASS" : "FAIL");
        
        // Write to output file for Oozie to capture
        FileOutputStream fos = new FileOutputStream(System.getProperty("oozie.action.output.properties"));
        props.store(fos, "Data Validation Results");
        fos.close();
    }
    
    private static long validateData(String inputPath, FileSystem fs) {
        // Implementation
        return 0;
    }
    
    private static double calculateErrorRate(String inputPath, FileSystem fs) {
        // Implementation
        return 0.0;
    }
}
```

**2. Workflow Integration:**
```xml
<action name="custom-validation">
    <java>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <main-class>com.company.DataValidationAction</main-class>
        <java-opts>-Xmx2048m</java-opts>
        <arg>${inputPath}</arg>
        <arg>${outputPath}</arg>
        <arg>${errorThreshold}</arg>
        <file>/user/oozie/lib/data-validation.jar</file>
        <capture-output/>
    </java>
    <ok to="check-validation-results"/>
    <error to="fail"/>
</action>

<decision name="check-validation-results">
    <switch>
        <case to="process-data">
            ${wf:actionData('custom-validation')['validationStatus'] eq 'PASS'}
        </case>
        <default to="send-validation-failure-alert"/>
    </switch>
</decision>
```

**3. Shell Action for Custom Scripts:**
```xml
<action name="custom-shell-processing">
    <shell xmlns="uri:oozie:shell-action:0.3">
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <exec>custom-processor.sh</exec>
        <argument>${inputDir}</argument>
        <argument>${outputDir}</argument>
        <argument>${processingDate}</argument>
        <file>/user/oozie/scripts/custom-processor.sh#custom-processor.sh</file>
        <file>/user/oozie/scripts/utils.sh#utils.sh</file>
        <env-var>JAVA_HOME=/usr/lib/jvm/java-8-openjdk</env-var>
        <env-var>HADOOP_CONF_DIR=/etc/hadoop/conf</env-var>
        <capture-output/>
    </shell>
    <ok to="next-action"/>
    <error to="fail"/>
</action>
```

### Q19: How do you handle large-scale workflow orchestration with Oozie bundles?
**Answer:**
**Large-scale Bundle Orchestration:**

**1. Comprehensive Bundle Structure:**
```xml
<bundle-app name="enterprise-data-platform" xmlns="uri:oozie:bundle:0.2">
    <parameters>
        <property>
            <name>startTime</name>
            <value>2024-01-01T00:00Z</value>
        </property>
        <property>
            <name>endTime</name>
            <value>2024-12-31T23:59Z</value>
        </property>
        <property>
            <name>dataCenter</name>
            <value>us-east-1</value>
        </property>
    </parameters>
    
    <!-- Data Ingestion Layer -->
    <coordinator name="raw-data-ingestion">
        <app-path>/user/oozie/coordinators/ingestion/raw-data-coord</app-path>
        <configuration>
            <property>
                <name>frequency</name>
                <value>${coord:hours(1)}</value>
            </property>
            <property>
                <name>inputSources</name>
                <value>api,files,database</value>
            </property>
        </configuration>
    </coordinator>
    
    <coordinator name="reference-data-sync">
        <app-path>/user/oozie/coordinators/ingestion/reference-sync-coord</app-path>
        <configuration>
            <property>
                <name>frequency</name>
                <value>${coord:days(1)}</value>
            </property>
        </configuration>
    </coordinator>
    
    <!-- Data Processing Layer -->
    <coordinator name="data-cleansing">
        <app-path>/user/oozie/coordinators/processing/cleansing-coord</app-path>
        <configuration>
            <property>
                <name>frequency</name>
                <value>${coord:hours(2)}</value>
            </property>
            <property>
                <name>dependsOn</name>
                <value>raw-data-ingestion</value>
            </property>
        </configuration>
    </coordinator>
    
    <coordinator name="data-enrichment">
        <app-path>/user/oozie/coordinators/processing/enrichment-coord</app-path>
        <configuration>
            <property>
                <name>frequency</name>
                <value>${coord:hours(4)}</value>
            </property>
        </configuration>
    </coordinator>
    
    <coordinator name="aggregation-processing">
        <app-path>/user/oozie/coordinators/processing/aggregation-coord</app-path>
        <configuration>
            <property>
                <name>frequency</name>
                <value>${coord:days(1)}</value>
            </property>
        </configuration>
    </coordinator>
    
    <!-- Data Export Layer -->
    <coordinator name="warehouse-export">
        <app-path>/user/oozie/coordinators/export/warehouse-coord</app-path>
        <configuration>
            <property>
                <name>frequency</name>
                <value>${coord:days(1)}</value>
            </property>
        </configuration>
    </coordinator>
    
    <coordinator name="api-data-export">
        <app-path>/user/oozie/coordinators/export/api-coord</app-path>
        <configuration>
            <property>
                <name>frequency</name>
                <value>${coord:hours(6)}</value>
            </property>
        </configuration>
    </coordinator>
    
    <!-- Monitoring and Maintenance -->
    <coordinator name="data-quality-monitoring">
        <app-path>/user/oozie/coordinators/monitoring/quality-coord</app-path>
        <configuration>
            <property>
                <name>frequency</name>
                <value>${coord:hours(1)}</value>
            </property>
        </configuration>
    </coordinator>
    
    <coordinator name="system-maintenance">
        <app-path>/user/oozie/coordinators/maintenance/cleanup-coord</app-path>
        <configuration>
            <property>
                <name>frequency</name>
                <value>${coord:days(7)}</value>
            </property>
        </configuration>
    </coordinator>
</bundle-app>
```

**2. Bundle Management Commands:**
```bash
# Submit bundle
oozie job -oozie http://oozie-server:11000/oozie -config bundle.properties -submit

# Start bundle
oozie job -oozie http://oozie-server:11000/oozie -start bundle-job-id

# Monitor bundle status
oozie job -oozie http://oozie-server:11000/oozie -info bundle-job-id

# Suspend specific coordinator in bundle
oozie job -oozie http://oozie-server:11000/oozie -suspend coordinator-job-id

# Resume bundle
oozie job -oozie http://oozie-server:11000/oozie -resume bundle-job-id

# Kill bundle (stops all coordinators)
oozie job -oozie http://oozie-server:11000/oozie -kill bundle-job-id
```

**3. Bundle Monitoring and Alerting:**
```python
import requests
import json
from datetime import datetime, timedelta

class BundleMonitor:
    def __init__(self, oozie_url):
        self.oozie_url = oozie_url
        
    def monitor_bundle_health(self, bundle_id):
        """Monitor bundle and coordinator health"""
        bundle_info = self.get_bundle_info(bundle_id)
        
        health_report = {
            'bundle_id': bundle_id,
            'bundle_status': bundle_info['status'],
            'coordinators': [],
            'alerts': []
        }
        
        for coord in bundle_info['coordinators']:
            coord_health = self.check_coordinator_health(coord['coordJobId'])
            health_report['coordinators'].append(coord_health)
            
            # Check for alerts
            if coord_health['status'] == 'KILLED':
                health_report['alerts'].append(f"Coordinator {coord['coordJobName']} is KILLED")
            elif coord_health['behind_schedule'] > 2:
                health_report['alerts'].append(f"Coordinator {coord['coordJobName']} is {coord_health['behind_schedule']} hours behind")
                
        return health_report
    
    def get_bundle_info(self, bundle_id):
        """Get bundle information"""
        response = requests.get(f"{self.oozie_url}/v1/job/{bundle_id}")
        return response.json()
    
    def check_coordinator_health(self, coord_id):
        """Check individual coordinator health"""
        response = requests.get(f"{self.oozie_url}/v1/job/{coord_id}")
        coord_info = response.json()
        
        # Calculate how far behind schedule
        last_action_time = datetime.fromisoformat(coord_info.get('lastActionTime', '').replace('Z', '+00:00'))
        current_time = datetime.now()
        behind_hours = (current_time - last_action_time).total_seconds() / 3600
        
        return {
            'coord_id': coord_id,
            'coord_name': coord_info['coordJobName'],
            'status': coord_info['status'],
            'last_action_time': coord_info.get('lastActionTime'),
            'behind_schedule': behind_hours,
            'next_materialized_time': coord_info.get('nextMaterializedTime')
        }

# Usage
monitor = BundleMonitor("http://oozie-server:11000/oozie")
health_report = monitor.monitor_bundle_health("0000001-240101000000000-oozie-B")
print(json.dumps(health_report, indent=2))
```

### Q20: How do you implement data lineage tracking in Oozie workflows?
**Answer:**
**Data Lineage Tracking Implementation:**

**1. Workflow-level Lineage Tracking:**
```xml
<workflow-app name="lineage-tracking-workflow" xmlns="uri:oozie:workflow:0.5">
    <parameters>
        <property>
            <name>lineageTrackingEnabled</name>
            <value>true</value>
        </property>
    </parameters>
    
    <start to="initialize-lineage"/>
    
    <action name="initialize-lineage">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.lineage.LineageInitializer</main-class>
            <arg>${wf:id()}</arg>
            <arg>${wf:name()}</arg>
            <arg>${wf:conf('processDate')}</arg>
            <capture-output/>
        </java>
        <ok to="extract-data"/>
        <error to="fail"/>
    </action>
    
    <action name="extract-data">
        <sqoop xmlns="uri:oozie:sqoop-action:0.4">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <command>import --connect jdbc:mysql://source-db:3306/sales --table orders --target-dir /data/raw/orders/${processDate}</command>
        </sqoop>
        <ok to="track-extraction-lineage"/>
        <error to="fail"/>
    </action>
    
    <action name="track-extraction-lineage">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.lineage.LineageTracker</main-class>
            <arg>EXTRACT</arg>
            <arg>source-db.sales.orders</arg>
            <arg>/data/raw/orders/${processDate}</arg>
            <arg>${wf:id()}</arg>
            <arg>extract-data</arg>
        </java>
        <ok to="transform-data"/>
        <error to="fail"/>
    </action>
    
    <action name="transform-data">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>DataTransformation</name>
            <class>com.company.spark.OrderTransformation</class>
            <jar>/user/oozie/lib/data-transformation.jar</jar>
            <arg>/data/raw/orders/${processDate}</arg>
            <arg>/data/processed/orders/${processDate}</arg>
            <arg>${wf:id()}</arg>
        </spark>
        <ok to="track-transformation-lineage"/>
        <error to="fail"/>
    </action>
    
    <action name="track-transformation-lineage">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.lineage.LineageTracker</main-class>
            <arg>TRANSFORM</arg>
            <arg>/data/raw/orders/${processDate}</arg>
            <arg>/data/processed/orders/${processDate}</arg>
            <arg>${wf:id()}</arg>
            <arg>transform-data</arg>
            <arg>${wf:actionData('transform-data')['transformationRules']}</arg>
        </java>
        <ok to="load-data"/>
        <error to="fail"/>
    </action>
    
    <action name="load-data">
        <hive xmlns="uri:oozie:hive-action:0.5">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>load-orders.hql</script>
            <param>INPUT_PATH=/data/processed/orders/${processDate}</param>
            <param>TARGET_TABLE=warehouse.orders</param>
            <param>PROCESS_DATE=${processDate}</param>
        </hive>
        <ok to="track-load-lineage"/>
        <error to="fail"/>
    </action>
    
    <action name="track-load-lineage">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.lineage.LineageTracker</main-class>
            <arg>LOAD</arg>
            <arg>/data/processed/orders/${processDate}</arg>
            <arg>warehouse.orders</arg>
            <arg>${wf:id()}</arg>
            <arg>load-data</arg>
        </java>
        <ok to="finalize-lineage"/>
        <error to="fail"/>
    </action>
    
    <action name="finalize-lineage">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.lineage.LineageFinalizer</main-class>
            <arg>${wf:id()}</arg>
            <arg>SUCCESS</arg>
        </java>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Workflow failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**2. Lineage Tracking Java Implementation:**
```java
public class LineageTracker {
    public static void main(String[] args) throws Exception {
        String operation = args[0];  // EXTRACT, TRANSFORM, LOAD
        String sourceEntity = args[1];
        String targetEntity = args[2];
        String workflowId = args[3];
        String actionName = args[4];
        String metadata = args.length > 5 ? args[5] : "";
        
        LineageRecord lineage = new LineageRecord();
        lineage.setWorkflowId(workflowId);
        lineage.setActionName(actionName);
        lineage.setOperation(operation);
        lineage.setSourceEntity(sourceEntity);
        lineage.setTargetEntity(targetEntity);
        lineage.setTimestamp(System.currentTimeMillis());
        lineage.setMetadata(metadata);
        
        // Store lineage information
        LineageStore store = new LineageStore();
        store.recordLineage(lineage);
        
        // Also store in HDFS for audit trail
        storeLineageInHDFS(lineage);
    }
    
    private static void storeLineageInHDFS(LineageRecord lineage) throws Exception {
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        
        String lineagePath = "/lineage/" + lineage.getWorkflowId() + "/" + lineage.getActionName() + ".json";
        FSDataOutputStream out = fs.create(new Path(lineagePath));
        
        ObjectMapper mapper = new ObjectMapper();
        out.writeBytes(mapper.writeValueAsString(lineage));
        out.close();
    }
}
```

**3. Lineage Query and Visualization:**
```python
class LineageAnalyzer:
    def __init__(self, lineage_store):
        self.lineage_store = lineage_store
    
    def get_data_lineage(self, entity_name):
        """Get complete lineage for a data entity"""
        lineage_graph = {
            'entity': entity_name,
            'upstream': [],
            'downstream': [],
            'transformations': []
        }
        
        # Get upstream dependencies
        upstream_records = self.lineage_store.get_upstream_lineage(entity_name)
        for record in upstream_records:
            lineage_graph['upstream'].append({
                'source': record['source_entity'],
                'workflow': record['workflow_id'],
                'operation': record['operation'],
                'timestamp': record['timestamp']
            })
        
        # Get downstream dependencies
        downstream_records = self.lineage_store.get_downstream_lineage(entity_name)
        for record in downstream_records:
            lineage_graph['downstream'].append({
                'target': record['target_entity'],
                'workflow': record['workflow_id'],
                'operation': record['operation'],
                'timestamp': record['timestamp']
            })
        
        return lineage_graph
    
    def generate_lineage_report(self, workflow_id):
        """Generate lineage report for a specific workflow"""
        workflow_lineage = self.lineage_store.get_workflow_lineage(workflow_id)
        
        report = {
            'workflow_id': workflow_id,
            'data_flow': [],
            'impact_analysis': {}
        }
        
        for record in workflow_lineage:
            report['data_flow'].append({
                'step': record['action_name'],
                'operation': record['operation'],
                'source': record['source_entity'],
                'target': record['target_entity'],
                'timestamp': record['timestamp']
            })
        
        return report

# Usage
analyzer = LineageAnalyzer(lineage_store)
lineage = analyzer.get_data_lineage('warehouse.orders')
print(json.dumps(lineage, indent=2))
```

---

*[Continuing with more questions in the next batch...]*
## 🔴 Advanced Level Questions

### Q21: How do you implement complex workflow patterns like sub-workflows and workflow reuse?
**Answer:**
**Sub-workflow Implementation:**

**1. Main Workflow with Sub-workflows:**
```xml
<workflow-app name="main-etl-workflow" xmlns="uri:oozie:workflow:0.5">
    <start to="validate-inputs"/>
    
    <action name="validate-inputs">
        <sub-workflow>
            <app-path>/user/oozie/workflows/validation-subworkflow</app-path>
            <configuration>
                <property>
                    <name>inputPath</name>
                    <value>${inputPath}</value>
                </property>
                <property>
                    <name>validationRules</name>
                    <value>${validationRules}</value>
                </property>
                <property>
                    <name>parentWorkflowId</name>
                    <value>${wf:id()}</value>
                </property>
            </configuration>
        </sub-workflow>
        <ok to="parallel-processing"/>
        <error to="fail"/>
    </action>
    
    <fork name="parallel-processing">
        <path start="process-customer-data"/>
        <path start="process-order-data"/>
        <path start="process-product-data"/>
    </fork>
    
    <action name="process-customer-data">
        <sub-workflow>
            <app-path>/user/oozie/workflows/customer-processing-subworkflow</app-path>
            <configuration>
                <property>
                    <name>inputPath</name>
                    <value>${inputPath}/customers</value>
                </property>
                <property>
                    <name>outputPath</name>
                    <value>${outputPath}/customers</value>
                </property>
                <property>
                    <name>processDate</name>
                    <value>${processDate}</value>
                </property>
            </configuration>
        </sub-workflow>
        <ok to="join-processing"/>
        <error to="fail"/>
    </action>
    
    <action name="process-order-data">
        <sub-workflow>
            <app-path>/user/oozie/workflows/order-processing-subworkflow</app-path>
            <configuration>
                <property>
                    <name>inputPath</name>
                    <value>${inputPath}/orders</value>
                </property>
                <property>
                    <name>outputPath</name>
                    <value>${outputPath}/orders</value>
                </property>
                <property>
                    <name>processDate</name>
                    <value>${processDate}</value>
                </property>
            </configuration>
        </sub-workflow>
        <ok to="join-processing"/>
        <error to="fail"/>
    </action>
    
    <action name="process-product-data">
        <sub-workflow>
            <app-path>/user/oozie/workflows/product-processing-subworkflow</app-path>
            <configuration>
                <property>
                    <name>inputPath</name>
                    <value>${inputPath}/products</value>
                </property>
                <property>
                    <name>outputPath</name>
                    <value>${outputPath}/products</value>
                </property>
                <property>
                    <name>processDate</name>
                    <value>${processDate}</value>
                </property>
            </configuration>
        </sub-workflow>
        <ok to="join-processing"/>
        <error to="fail"/>
    </action>
    
    <join name="join-processing" to="aggregate-results"/>
    
    <action name="aggregate-results">
        <sub-workflow>
            <app-path>/user/oozie/workflows/aggregation-subworkflow</app-path>
            <configuration>
                <property>
                    <name>customerData</name>
                    <value>${outputPath}/customers</value>
                </property>
                <property>
                    <name>orderData</name>
                    <value>${outputPath}/orders</value>
                </property>
                <property>
                    <name>productData</name>
                    <value>${outputPath}/products</value>
                </property>
                <property>
                    <name>finalOutput</name>
                    <value>${outputPath}/aggregated</value>
                </property>
            </configuration>
        </sub-workflow>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Main workflow failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**2. Reusable Sub-workflow Template:**
```xml
<!-- Generic Data Processing Sub-workflow -->
<workflow-app name="generic-data-processing" xmlns="uri:oozie:workflow:0.5">
    <parameters>
        <property>
            <name>inputPath</name>
            <description>Input data path</description>
        </property>
        <property>
            <name>outputPath</name>
            <description>Output data path</description>
        </property>
        <property>
            <name>processingType</name>
            <description>Type of processing: customer, order, product</description>
        </property>
        <property>
            <name>configFile</name>
            <description>Configuration file for processing rules</description>
        </property>
    </parameters>
    
    <start to="setup-processing"/>
    
    <action name="setup-processing">
        <fs>
            <mkdir path="${outputPath}"/>
            <mkdir path="${outputPath}/temp"/>
        </fs>
        <ok to="determine-processing-type"/>
        <error to="fail"/>
    </action>
    
    <decision name="determine-processing-type">
        <switch>
            <case to="customer-specific-processing">
                ${wf:conf('processingType') eq 'customer'}
            </case>
            <case to="order-specific-processing">
                ${wf:conf('processingType') eq 'order'}
            </case>
            <case to="product-specific-processing">
                ${wf:conf('processingType') eq 'product'}
            </case>
            <default to="generic-processing"/>
        </switch>
    </decision>
    
    <action name="customer-specific-processing">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>CustomerProcessing</name>
            <class>com.company.processing.CustomerProcessor</class>
            <jar>/user/oozie/lib/data-processors.jar</jar>
            <arg>${inputPath}</arg>
            <arg>${outputPath}</arg>
            <arg>${configFile}</arg>
        </spark>
        <ok to="cleanup"/>
        <error to="fail"/>
    </action>
    
    <action name="order-specific-processing">
        <pig>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>order-processing.pig</script>
            <param>INPUT=${inputPath}</param>
            <param>OUTPUT=${outputPath}</param>
            <param>CONFIG=${configFile}</param>
        </pig>
        <ok to="cleanup"/>
        <error to="fail"/>
    </action>
    
    <action name="product-specific-processing">
        <hive xmlns="uri:oozie:hive-action:0.5">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>product-processing.hql</script>
            <param>INPUT=${inputPath}</param>
            <param>OUTPUT=${outputPath}</param>
            <param>CONFIG=${configFile}</param>
        </hive>
        <ok to="cleanup"/>
        <error to="fail"/>
    </action>
    
    <action name="generic-processing">
        <map-reduce>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <configuration>
                <property>
                    <name>mapred.mapper.class</name>
                    <value>com.company.processing.GenericMapper</value>
                </property>
                <property>
                    <name>mapred.reducer.class</name>
                    <value>com.company.processing.GenericReducer</value>
                </property>
                <property>
                    <name>mapred.input.dir</name>
                    <value>${inputPath}</value>
                </property>
                <property>
                    <name>mapred.output.dir</name>
                    <value>${outputPath}</value>
                </property>
            </configuration>
        </map-reduce>
        <ok to="cleanup"/>
        <error to="fail"/>
    </action>
    
    <action name="cleanup">
        <fs>
            <delete path="${outputPath}/temp"/>
        </fs>
        <ok to="end"/>
        <error to="end"/>
    </action>
    
    <kill name="fail">
        <message>Sub-workflow failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**3. Workflow Library Management:**
```bash
# Directory structure for reusable workflows
/user/oozie/workflows/
├── library/
│   ├── validation-subworkflow/
│   │   ├── workflow.xml
│   │   └── lib/
│   ├── processing-subworkflow/
│   │   ├── workflow.xml
│   │   └── lib/
│   └── aggregation-subworkflow/
│       ├── workflow.xml
│       └── lib/
├── main-workflows/
│   ├── daily-etl/
│   ├── hourly-processing/
│   └── weekly-reports/
└── shared/
    ├── lib/
    ├── scripts/
    └── config/
```

### Q22: How do you implement advanced error handling and recovery strategies?
**Answer:**
**Advanced Error Handling Strategies:**

**1. Multi-level Error Handling:**
```xml
<workflow-app name="robust-error-handling" xmlns="uri:oozie:workflow:0.5">
    <global>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <configuration>
            <property>
                <name>oozie.action.retry.max</name>
                <value>3</value>
            </property>
            <property>
                <name>oozie.action.retry.interval</name>
                <value>10</value>
            </property>
        </configuration>
    </global>
    
    <start to="initialize-error-tracking"/>
    
    <action name="initialize-error-tracking">
        <java>
            <main-class>com.company.error.ErrorTracker</main-class>
            <arg>INITIALIZE</arg>
            <arg>${wf:id()}</arg>
            <capture-output/>
        </java>
        <ok to="critical-data-processing"/>
        <error to="initialization-failed"/>
    </action>
    
    <action name="critical-data-processing" retry-max="5" retry-interval="30">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>CriticalProcessing</name>
            <class>com.company.processing.CriticalProcessor</class>
            <jar>/user/oozie/lib/critical-processor.jar</jar>
            <spark-opts>--conf spark.sql.adaptive.enabled=true --conf spark.sql.adaptive.coalescePartitions.enabled=true</spark-opts>
            <arg>${inputPath}</arg>
            <arg>${outputPath}</arg>
        </spark>
        <ok to="validate-critical-output"/>
        <error to="handle-critical-failure"/>
    </action>
    
    <action name="validate-critical-output">
        <java>
            <main-class>com.company.validation.OutputValidator</main-class>
            <arg>${outputPath}</arg>
            <arg>CRITICAL</arg>
            <capture-output/>
        </java>
        <ok to="check-validation-results"/>
        <error to="validation-failed"/>
    </action>
    
    <decision name="check-validation-results">
        <switch>
            <case to="secondary-processing">
                ${wf:actionData('validate-critical-output')['validationStatus'] eq 'PASS'}
            </case>
            <case to="handle-validation-failure">
                ${wf:actionData('validate-critical-output')['validationStatus'] eq 'FAIL'}
            </case>
            <default to="handle-validation-error"/>
        </switch>
    </decision>
    
    <action name="secondary-processing" retry-max="3" retry-interval="15">
        <pig>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>secondary-processing.pig</script>
            <param>INPUT=${outputPath}</param>
            <param>OUTPUT=${secondaryOutput}</param>
        </pig>
        <ok to="final-validation"/>
        <error to="handle-secondary-failure"/>
    </action>
    
    <!-- Error Handling Actions -->
    <action name="handle-critical-failure">
        <java>
            <main-class>com.company.error.CriticalErrorHandler</main-class>
            <arg>${wf:id()}</arg>
            <arg>${wf:lastErrorNode()}</arg>
            <arg>${wf:errorMessage(wf:lastErrorNode())}</arg>
            <arg>${wf:errorCode(wf:lastErrorNode())}</arg>
            <capture-output/>
        </java>
        <ok to="decide-recovery-strategy"/>
        <error to="escalate-critical-error"/>
    </action>
    
    <decision name="decide-recovery-strategy">
        <switch>
            <case to="attempt-alternative-processing">
                ${wf:actionData('handle-critical-failure')['recoveryStrategy'] eq 'ALTERNATIVE'}
            </case>
            <case to="attempt-partial-processing">
                ${wf:actionData('handle-critical-failure')['recoveryStrategy'] eq 'PARTIAL'}
            </case>
            <case to="skip-and-continue">
                ${wf:actionData('handle-critical-failure')['recoveryStrategy'] eq 'SKIP'}
            </case>
            <default to="escalate-critical-error"/>
        </switch>
    </decision>
    
    <action name="attempt-alternative-processing">
        <map-reduce>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <configuration>
                <property>
                    <name>mapred.mapper.class</name>
                    <value>com.company.processing.AlternativeMapper</value>
                </property>
                <property>
                    <name>mapred.reducer.class</name>
                    <value>com.company.processing.AlternativeReducer</value>
                </property>
                <property>
                    <name>mapred.input.dir</name>
                    <value>${inputPath}</value>
                </property>
                <property>
                    <name>mapred.output.dir</name>
                    <value>${outputPath}</value>
                </property>
            </configuration>
        </map-reduce>
        <ok to="validate-alternative-output"/>
        <error to="escalate-critical-error"/>
    </action>
    
    <action name="handle-validation-failure">
        <java>
            <main-class>com.company.error.ValidationErrorHandler</main-class>
            <arg>${wf:actionData('validate-critical-output')['errorDetails']}</arg>
            <arg>${outputPath}</arg>
            <capture-output/>
        </java>
        <ok to="decide-validation-recovery"/>
        <error to="escalate-validation-error"/>
    </action>
    
    <decision name="decide-validation-recovery">
        <switch>
            <case to="repair-and-retry">
                ${wf:actionData('handle-validation-failure')['canRepair'] eq 'true'}
            </case>
            <case to="generate-partial-output">
                ${wf:actionData('handle-validation-failure')['canPartial'] eq 'true'}
            </case>
            <default to="escalate-validation-error"/>
        </switch>
    </decision>
    
    <!-- Escalation Actions -->
    <action name="escalate-critical-error">
        <email xmlns="uri:oozie:email-action:0.2">
            <to>critical-alerts@company.com</to>
            <cc>manager@company.com</cc>
            <subject>CRITICAL: Workflow ${wf:name()} Failed - Immediate Action Required</subject>
            <body>
                CRITICAL ERROR in workflow ${wf:name()} (${wf:id()})
                
                Failed Action: ${wf:lastErrorNode()}
                Error Message: ${wf:errorMessage(wf:lastErrorNode())}
                Error Code: ${wf:errorCode(wf:lastErrorNode())}
                
                All recovery attempts have failed. Manual intervention required.
                
                Workflow Details:
                - Start Time: ${wf:conf('startTime')}
                - Input Path: ${inputPath}
                - Expected Output: ${outputPath}
            </body>
        </email>
        <ok to="mark-critical-failure"/>
        <error to="fail"/>
    </action>
    
    <action name="mark-critical-failure">
        <java>
            <main-class>com.company.error.ErrorTracker</main-class>
            <arg>CRITICAL_FAILURE</arg>
            <arg>${wf:id()}</arg>
            <arg>${wf:lastErrorNode()}</arg>
        </java>
        <ok to="fail"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Workflow failed after all recovery attempts: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**2. Error Recovery Java Implementation:**
```java
public class CriticalErrorHandler {
    public static void main(String[] args) throws Exception {
        String workflowId = args[0];
        String failedAction = args[1];
        String errorMessage = args[2];
        String errorCode = args[3];
        
        ErrorAnalyzer analyzer = new ErrorAnalyzer();
        ErrorContext context = analyzer.analyzeError(failedAction, errorMessage, errorCode);
        
        RecoveryStrategy strategy = determineRecoveryStrategy(context);
        
        Properties output = new Properties();
        output.setProperty("recoveryStrategy", strategy.name());
        output.setProperty("errorSeverity", context.getSeverity().name());
        output.setProperty("canRecover", String.valueOf(strategy != RecoveryStrategy.ESCALATE));
        
        // Log error details
        ErrorLogger.logError(workflowId, failedAction, context, strategy);
        
        // Write output for workflow
        FileOutputStream fos = new FileOutputStream(System.getProperty("oozie.action.output.properties"));
        output.store(fos, "Error Recovery Analysis");
        fos.close();
    }
    
    private static RecoveryStrategy determineRecoveryStrategy(ErrorContext context) {
        switch (context.getErrorType()) {
            case RESOURCE_UNAVAILABLE:
                return RecoveryStrategy.ALTERNATIVE;
            case DATA_QUALITY_ISSUE:
                return RecoveryStrategy.PARTIAL;
            case TRANSIENT_FAILURE:
                return RecoveryStrategy.RETRY;
            case CONFIGURATION_ERROR:
                return RecoveryStrategy.SKIP;
            default:
                return RecoveryStrategy.ESCALATE;
        }
    }
}
```

### Q23: How do you implement complex coordinator patterns with multiple data dependencies?
**Answer:**
**Complex Coordinator Patterns:**

**1. Multi-frequency Coordinator with Complex Dependencies:**
```xml
<coordinator-app name="complex-multi-dependency-coordinator" 
                 frequency="${coord:hours(4)}" 
                 start="2024-01-01T00:00Z" 
                 end="2024-12-31T23:59Z" 
                 timezone="UTC"
                 xmlns="uri:oozie:coordinator:0.4">
    
    <parameters>
        <property>
            <name>lookbackHours</name>
            <value>24</value>
        </property>
        <property>
            <name>maxWaitTime</name>
            <value>120</value>
        </property>
    </parameters>
    
    <datasets>
        <!-- High-frequency streaming data -->
        <dataset name="streaming-data" frequency="${coord:minutes(15)}" 
                 initial-instance="2024-01-01T00:00Z" timezone="UTC">
            <uri-template>/data/streaming/${YEAR}/${MONTH}/${DAY}/${HOUR}/${MINUTE}</uri-template>
            <done-flag>_COMPLETE</done-flag>
        </dataset>
        
        <!-- Hourly batch data -->
        <dataset name="batch-data" frequency="${coord:hours(1)}" 
                 initial-instance="2024-01-01T00:00Z" timezone="UTC">
            <uri-template>/data/batch/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_SUCCESS</done-flag>
        </dataset>
        
        <!-- Daily reference data -->
        <dataset name="reference-data" frequency="${coord:days(1)}" 
                 initial-instance="2024-01-01T00:00Z" timezone="UTC">
            <uri-template>/data/reference/${YEAR}/${MONTH}/${DAY}</uri-template>
            <done-flag>_READY</done-flag>
        </dataset>
        
        <!-- Weekly configuration data -->
        <dataset name="config-data" frequency="${coord:days(7)}" 
                 initial-instance="2024-01-01T00:00Z" timezone="UTC">
            <uri-template>/data/config/${YEAR}/${MONTH}/${DAY}</uri-template>
            <done-flag>_UPDATED</done-flag>
        </dataset>
        
        <!-- External system data (irregular frequency) -->
        <dataset name="external-data" frequency="${coord:hours(6)}" 
                 initial-instance="2024-01-01T00:00Z" timezone="UTC">
            <uri-template>/data/external/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_AVAILABLE</done-flag>
        </dataset>
    </datasets>
    
    <input-events>
        <!-- Wait for last 4 hours of streaming data (16 instances) -->
        <data-in name="recent-streaming" dataset="streaming-data">
            <start-instance>${coord:current(-15)}</start-instance>
            <end-instance>${coord:current(0)}</end-instance>
        </data-in>
        
        <!-- Wait for last 4 hours of batch data -->
        <data-in name="recent-batch" dataset="batch-data">
            <start-instance>${coord:current(-3)}</start-instance>
            <end-instance>${coord:current(0)}</end-instance>
        </data-in>
        
        <!-- Wait for latest reference data (within last 24 hours) -->
        <data-in name="latest-reference" dataset="reference-data">
            <instance>${coord:latest(0)}</instance>
        </data-in>
        
        <!-- Wait for latest config data (within last week) -->
        <data-in name="latest-config" dataset="config-data">
            <instance>${coord:latest(0)}</instance>
        </data-in>
        
        <!-- Optional external data (best effort) -->
        <data-in name="external-feed" dataset="external-data">
            <instance>${coord:latest(-1)}</instance>
        </data-in>
    </input-events>
    
    <output-events>
        <data-out name="processed-output" dataset="processed-data">
            <instance>${coord:current(0)}</instance>
        </data-out>
    </output-events>
    
    <action>
        <workflow>
            <app-path>/user/oozie/workflows/complex-processing-workflow</app-path>
            <configuration>
                <property>
                    <name>streamingDataPaths</name>
                    <value>${coord:dataIn('recent-streaming')}</value>
                </property>
                <property>
                    <name>batchDataPaths</name>
                    <value>${coord:dataIn('recent-batch')}</value>
                </property>
                <property>
                    <name>referenceDataPath</name>
                    <value>${coord:dataIn('latest-reference')}</value>
                </property>
                <property>
                    <name>configDataPath</name>
                    <value>${coord:dataIn('latest-config')}</value>
                </property>
                <property>
                    <name>externalDataPath</name>
                    <value>${coord:dataIn('external-feed')}</value>
                </property>
                <property>
                    <name>hasExternalData</name>
                    <value>${coord:dataIn('external-feed') != ""}</value>
                </property>
                <property>
                    <name>outputPath</name>
                    <value>${coord:dataOut('processed-output')}</value>
                </property>
                <property>
                    <name>nominalTime</name>
                    <value>${coord:nominalTime()}</value>
                </property>
                <property>
                    <name>actualTime</name>
                    <value>${coord:actualTime()}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

**2. Conditional Data Dependencies:**
```xml
<coordinator-app name="conditional-dependency-coordinator">
    <datasets>
        <dataset name="primary-data" frequency="${coord:hours(1)}">
            <uri-template>/data/primary/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_SUCCESS</done-flag>
        </dataset>
        
        <dataset name="secondary-data" frequency="${coord:hours(2)}">
            <uri-template>/data/secondary/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_SUCCESS</done-flag>
        </dataset>
        
        <dataset name="fallback-data" frequency="${coord:hours(4)}">
            <uri-template>/data/fallback/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_SUCCESS</done-flag>
        </dataset>
    </datasets>
    
    <input-events>
        <!-- Primary data dependency -->
        <data-in name="primary" dataset="primary-data">
            <instance>${coord:current(0)}</instance>
        </data-in>
        
        <!-- Secondary data (optional, use latest available) -->
        <data-in name="secondary" dataset="secondary-data">
            <instance>${coord:latest(-1)}</instance>
        </data-in>
        
        <!-- Fallback data (use if secondary not available) -->
        <data-in name="fallback" dataset="fallback-data">
            <instance>${coord:latest(-2)}</instance>
        </data-in>
    </input-events>
    
    <action>
        <workflow>
            <app-path>/user/oozie/workflows/conditional-processing</app-path>
            <configuration>
                <property>
                    <name>primaryDataPath</name>
                    <value>${coord:dataIn('primary')}</value>
                </property>
                <property>
                    <name>secondaryDataPath</name>
                    <value>${coord:dataIn('secondary')}</value>
                </property>
                <property>
                    <name>fallbackDataPath</name>
                    <value>${coord:dataIn('fallback')}</value>
                </property>
                <property>
                    <name>useSecondary</name>
                    <value>${coord:dataIn('secondary') != ""}</value>
                </property>
                <property>
                    <name>useFallback</name>
                    <value>${coord:dataIn('secondary') == "" and coord:dataIn('fallback') != ""}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

**3. Cross-timezone Coordination:**
```xml
<coordinator-app name="global-coordination" 
                 frequency="${coord:hours(6)}" 
                 start="2024-01-01T00:00Z" 
                 end="2024-12-31T23:59Z" 
                 timezone="UTC">
    
    <datasets>
        <!-- US East Coast data -->
        <dataset name="us-east-data" frequency="${coord:hours(1)}" 
                 initial-instance="2024-01-01T05:00Z" timezone="America/New_York">
            <uri-template>/data/regions/us-east/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_COMPLETE</done-flag>
        </dataset>
        
        <!-- US West Coast data -->
        <dataset name="us-west-data" frequency="${coord:hours(1)}" 
                 initial-instance="2024-01-01T08:00Z" timezone="America/Los_Angeles">
            <uri-template>/data/regions/us-west/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_COMPLETE</done-flag>
        </dataset>
        
        <!-- European data -->
        <dataset name="europe-data" frequency="${coord:hours(1)}" 
                 initial-instance="2024-01-01T01:00Z" timezone="Europe/London">
            <uri-template>/data/regions/europe/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_COMPLETE</done-flag>
        </dataset>
        
        <!-- Asian data -->
        <dataset name="asia-data" frequency="${coord:hours(1)}" 
                 initial-instance="2024-01-01T09:00Z" timezone="Asia/Tokyo">
            <uri-template>/data/regions/asia/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_COMPLETE</done-flag>
        </dataset>
    </datasets>
    
    <input-events>
        <!-- Wait for business hours data from each region -->
        <data-in name="us-east-business-hours" dataset="us-east-data">
            <start-instance>${coord:offset(-5, 'HOUR')}</start-instance>
            <end-instance>${coord:offset(0, 'HOUR')}</end-instance>
        </data-in>
        
        <data-in name="us-west-business-hours" dataset="us-west-data">
            <start-instance>${coord:offset(-5, 'HOUR')}</start-instance>
            <end-instance>${coord:offset(0, 'HOUR')}</end-instance>
        </data-in>
        
        <data-in name="europe-business-hours" dataset="europe-data">
            <start-instance>${coord:offset(-8, 'HOUR')}</start-instance>
            <end-instance>${coord:offset(-1, 'HOUR')}</end-instance>
        </data-in>
        
        <data-in name="asia-business-hours" dataset="asia-data">
            <start-instance>${coord:offset(-8, 'HOUR')}</start-instance>
            <end-instance>${coord:offset(-1, 'HOUR')}</end-instance>
        </data-in>
    </input-events>
    
    <action>
        <workflow>
            <app-path>/user/oozie/workflows/global-aggregation</app-path>
            <configuration>
                <property>
                    <name>usEastData</name>
                    <value>${coord:dataIn('us-east-business-hours')}</value>
                </property>
                <property>
                    <name>usWestData</name>
                    <value>${coord:dataIn('us-west-business-hours')}</value>
                </property>
                <property>
                    <name>europeData</name>
                    <value>${coord:dataIn('europe-business-hours')}</value>
                </property>
                <property>
                    <name>asiaData</name>
                    <value>${coord:dataIn('asia-business-hours')}</value>
                </property>
                <property>
                    <name>globalReportTime</name>
                    <value>${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd HH:mm:ss')}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

### Q24: How do you implement Oozie workflow versioning and deployment strategies?
**Answer:**
**Workflow Versioning and Deployment:**

**1. Version Management Structure:**
```bash
# Directory structure for versioned workflows
/user/oozie/workflows/
├── production/
│   ├── v1.0/
│   │   ├── daily-etl/
│   │   │   ├── workflow.xml
│   │   │   ├── lib/
│   │   │   └── config/
│   │   └── hourly-processing/
│   └── v1.1/
│       ├── daily-etl/
│       └── hourly-processing/
├── staging/
│   ├── v1.2-rc1/
│   └── v1.2-rc2/
└── development/
    ├── feature-branch-1/
    └── feature-branch-2/
```

**2. Versioned Workflow Template:**
```xml
<workflow-app name="versioned-etl-workflow" xmlns="uri:oozie:workflow:0.5">
    <parameters>
        <property>
            <name>workflowVersion</name>
            <value>1.2.0</value>
            <description>Workflow version for tracking and compatibility</description>
        </property>
        <property>
            <name>deploymentEnvironment</name>
            <value>production</value>
            <description>Deployment environment: development, staging, production</description>
        </property>
        <property>
            <name>compatibilityVersion</name>
            <value>1.0</value>
            <description>Minimum compatible version for data formats</description>
        </property>
    </parameters>
    
    <start to="version-check"/>
    
    <action name="version-check">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.version.VersionChecker</main-class>
            <arg>${workflowVersion}</arg>
            <arg>${compatibilityVersion}</arg>
            <arg>${deploymentEnvironment}</arg>
            <capture-output/>
        </java>
        <ok to="check-version-compatibility"/>
        <error to="version-check-failed"/>
    </action>
    
    <decision name="check-version-compatibility">
        <switch>
            <case to="load-version-specific-config">
                ${wf:actionData('version-check')['compatible'] eq 'true'}
            </case>
            <default to="version-incompatible"/>
        </switch>
    </decision>
    
    <action name="load-version-specific-config">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.config.VersionedConfigLoader</main-class>
            <arg>${workflowVersion}</arg>
            <arg>${deploymentEnvironment}</arg>
            <capture-output/>
        </java>
        <ok to="execute-versioned-processing"/>
        <error to="config-load-failed"/>
    </action>
    
    <action name="execute-versioned-processing">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>VersionedETLProcessing-${workflowVersion}</name>
            <class>com.company.etl.VersionedETLProcessor</class>
            <jar>/user/oozie/lib/${workflowVersion}/etl-processor.jar</jar>
            <arg>${inputPath}</arg>
            <arg>${outputPath}</arg>
            <arg>${workflowVersion}</arg>
            <arg>${wf:actionData('load-version-specific-config')['configPath']}</arg>
        </spark>
        <ok to="version-metadata-update"/>
        <error to="processing-failed"/>
    </action>
    
    <action name="version-metadata-update">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.metadata.VersionMetadataUpdater</main-class>
            <arg>${outputPath}</arg>
            <arg>${workflowVersion}</arg>
            <arg>${wf:id()}</arg>
            <arg>${wf:conf('processDate')}</arg>
        </java>
        <ok to="end"/>
        <error to="metadata-update-failed"/>
    </action>
    
    <!-- Error handling for version-related issues -->
    <action name="version-incompatible">
        <email xmlns="uri:oozie:email-action:0.2">
            <to>devops@company.com</to>
            <subject>Version Incompatibility: ${wf:name()} v${workflowVersion}</subject>
            <body>
                Version incompatibility detected in workflow ${wf:name()}
                
                Current Version: ${workflowVersion}
                Required Compatibility: ${compatibilityVersion}
                Environment: ${deploymentEnvironment}
                
                Please check version compatibility matrix and update accordingly.
            </body>
        </email>
        <ok to="fail"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Workflow failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**3. Deployment Automation Script:**
```bash
#!/bin/bash
# Oozie Workflow Deployment Script

set -e

# Configuration
OOZIE_URL="http://oozie-server:11000/oozie"
HDFS_BASE="/user/oozie/workflows"
VERSION=""
ENVIRONMENT=""
WORKFLOW_NAME=""
DRY_RUN=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--version)
            VERSION="$2"
            shift 2
            ;;
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -w|--workflow)
            WORKFLOW_NAME="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

# Validate inputs
if [[ -z "$VERSION" || -z "$ENVIRONMENT" || -z "$WORKFLOW_NAME" ]]; then
    echo "Usage: $0 -v VERSION -e ENVIRONMENT -w WORKFLOW_NAME [--dry-run]"
    exit 1
fi

echo "Deploying workflow: $WORKFLOW_NAME"
echo "Version: $VERSION"
echo "Environment: $ENVIRONMENT"
echo "Dry run: $DRY_RUN"

# Define paths
SOURCE_PATH="./workflows/$WORKFLOW_NAME"
TARGET_PATH="$HDFS_BASE/$ENVIRONMENT/$VERSION/$WORKFLOW_NAME"
BACKUP_PATH="$HDFS_BASE/$ENVIRONMENT/backup/$(date +%Y%m%d_%H%M%S)/$WORKFLOW_NAME"

# Pre-deployment validation
echo "Validating workflow definition..."
if ! xmllint --noout "$SOURCE_PATH/workflow.xml"; then
    echo "ERROR: Invalid workflow XML"
    exit 1
fi

# Check if coordinator exists
if [[ -f "$SOURCE_PATH/coordinator.xml" ]]; then
    if ! xmllint --noout "$SOURCE_PATH/coordinator.xml"; then
        echo "ERROR: Invalid coordinator XML"
        exit 1
    fi
fi

# Backup existing version if it exists
if hdfs dfs -test -d "$TARGET_PATH" 2>/dev/null; then
    echo "Backing up existing version..."
    if [[ "$DRY_RUN" == "false" ]]; then
        hdfs dfs -mkdir -p "$(dirname "$BACKUP_PATH")"
        hdfs dfs -cp "$TARGET_PATH" "$BACKUP_PATH"
    fi
fi

# Deploy new version
echo "Deploying new version..."
if [[ "$DRY_RUN" == "false" ]]; then
    # Create target directory
    hdfs dfs -mkdir -p "$TARGET_PATH"
    
    # Copy workflow files
    hdfs dfs -put -f "$SOURCE_PATH"/* "$TARGET_PATH/"
    
    # Set appropriate permissions
    hdfs dfs -chmod -R 755 "$TARGET_PATH"
    
    # Update Oozie shared lib if needed
    if [[ -d "$SOURCE_PATH/lib" ]]; then
        hdfs dfs -put -f "$SOURCE_PATH/lib"/* "/user/oozie/share/lib/lib_$(date +%Y%m%d_%H%M%S)/"
        oozie admin -oozie "$OOZIE_URL" -sharelibupdate
    fi
fi

# Validate deployment
echo "Validating deployment..."
if [[ "$DRY_RUN" == "false" ]]; then
    if hdfs dfs -test -f "$TARGET_PATH/workflow.xml"; then
        echo "✓ Workflow deployed successfully"
    else
        echo "✗ Deployment failed"
        exit 1
    fi
fi

# Create deployment metadata
METADATA_FILE="/tmp/deployment_metadata_$$.json"
cat > "$METADATA_FILE" << EOF
{
    "workflow_name": "$WORKFLOW_NAME",
    "version": "$VERSION",
    "environment": "$ENVIRONMENT",
    "deployment_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "deployed_by": "$(whoami)",
    "target_path": "$TARGET_PATH",
    "backup_path": "$BACKUP_PATH"
}
EOF

if [[ "$DRY_RUN" == "false" ]]; then
    hdfs dfs -put "$METADATA_FILE" "$TARGET_PATH/deployment_metadata.json"
fi

rm -f "$METADATA_FILE"

echo "Deployment completed successfully!"
echo "Target path: $TARGET_PATH"

# Optional: Submit test job
if [[ "$ENVIRONMENT" == "staging" && "$DRY_RUN" == "false" ]]; then
    echo "Submitting test job..."
    # Create test properties file
    TEST_PROPS="/tmp/test_${WORKFLOW_NAME}_$$.properties"
    cat > "$TEST_PROPS" << EOF
nameNode=hdfs://namenode:8020
jobTracker=resourcemanager:8032
oozie.wf.application.path=$TARGET_PATH
workflowVersion=$VERSION
deploymentEnvironment=$ENVIRONMENT
inputPath=/data/test/input
outputPath=/data/test/output/$VERSION
EOF
    
    # Submit test job
    TEST_JOB_ID=$(oozie job -oozie "$OOZIE_URL" -config "$TEST_PROPS" -run | grep -o '[0-9]\{7\}-[0-9]\{12\}-oozie-[WC]')
    echo "Test job submitted: $TEST_JOB_ID"
    
    rm -f "$TEST_PROPS"
fi
```

**4. Blue-Green Deployment Strategy:**
```bash
#!/bin/bash
# Blue-Green Deployment for Oozie Workflows

BLUE_PATH="/user/oozie/workflows/production/blue"
GREEN_PATH="/user/oozie/workflows/production/green"
ACTIVE_LINK="/user/oozie/workflows/production/active"

# Determine current active environment
if hdfs dfs -test -L "$ACTIVE_LINK"; then
    CURRENT_TARGET=$(hdfs dfs -ls "$ACTIVE_LINK" | awk '{print $NF}')
    if [[ "$CURRENT_TARGET" == *"blue"* ]]; then
        CURRENT_ENV="blue"
        DEPLOY_ENV="green"
        DEPLOY_PATH="$GREEN_PATH"
    else
        CURRENT_ENV="green"
        DEPLOY_ENV="blue"
        DEPLOY_PATH="$BLUE_PATH"
    fi
else
    CURRENT_ENV="none"
    DEPLOY_ENV="blue"
    DEPLOY_PATH="$BLUE_PATH"
fi

echo "Current active environment: $CURRENT_ENV"
echo "Deploying to: $DEPLOY_ENV"

# Deploy to inactive environment
deploy_workflow() {
    local target_path=$1
    local version=$2
    
    echo "Deploying version $version to $target_path"
    
    # Copy new version
    hdfs dfs -rm -r -f "$target_path"
    hdfs dfs -mkdir -p "$target_path"
    hdfs dfs -put -f "./workflows/$version"/* "$target_path/"
    
    # Run smoke tests
    run_smoke_tests "$target_path"
    
    if [[ $? -eq 0 ]]; then
        echo "Smoke tests passed"
        return 0
    else
        echo "Smoke tests failed"
        return 1
    fi
}

# Switch active environment
switch_active() {
    local new_active_path=$1
    
    echo "Switching active environment to $new_active_path"
    
    # Update symbolic link
    hdfs dfs -rm -f "$ACTIVE_LINK"
    hdfs dfs -ln -s "$new_active_path" "$ACTIVE_LINK"
    
    # Verify switch
    NEW_TARGET=$(hdfs dfs -ls "$ACTIVE_LINK" | awk '{print $NF}')
    if [[ "$NEW_TARGET" == "$new_active_path" ]]; then
        echo "Successfully switched to $new_active_path"
        return 0
    else
        echo "Failed to switch active environment"
        return 1
    fi
}

# Rollback function
rollback() {
    local rollback_path=$1
    
    echo "Rolling back to $rollback_path"
    switch_active "$rollback_path"
}

# Main deployment process
if deploy_workflow "$DEPLOY_PATH" "$VERSION"; then
    if switch_active "$DEPLOY_PATH"; then
        echo "Deployment successful!"
        
        # Optional: Clean up old environment after successful deployment
        # sleep 300  # Wait 5 minutes
        # hdfs dfs -rm -r -f "$OLD_PATH"
    else
        echo "Failed to switch active environment"
        exit 1
    fi
else
    echo "Deployment failed"
    exit 1
fi
```

### Q25: How do you implement custom Oozie extensions and plugins?
**Answer:**
**Custom Oozie Extensions:**

**1. Custom Action Extension:**
```java
// Custom Action Executor
public class CustomDataValidationActionExecutor extends ActionExecutor {
    
    public static final String ACTION_TYPE = "custom-data-validation";
    
    public CustomDataValidationActionExecutor() {
        super(ACTION_TYPE);
    }
    
    @Override
    public void initActionType() {
        super.initActionType();
        registerError(CustomDataValidationActionExecutor.class.getName(), 
                     ErrorType.ERROR, "CUSTOM_VALIDATION_ERROR");
    }
    
    @Override
    public void start(Context context, WorkflowAction action) throws ActionExecutorException {
        try {
            Element actionXml = XmlUtils.parseXml(action.getConf());
            String inputPath = actionXml.getChildTextTrim("input-path");
            String validationRules = actionXml.getChildTextTrim("validation-rules");
            String outputPath = actionXml.getChildTextTrim("output-path");
            
            // Create validation job configuration
            Configuration jobConf = createBaseHadoopConf(context, actionXml);
            jobConf.set("validation.input.path", inputPath);
            jobConf.set("validation.rules", validationRules);
            jobConf.set("validation.output.path", outputPath);
            
            // Submit validation job
            JobClient jobClient = createJobClient(context, jobConf);
            RunningJob runningJob = jobClient.submitJob(new JobConf(jobConf));
            
            String jobId = runningJob.getID().toString();
            context.setStartData(jobId, "", "");
            
        } catch (Exception e) {
            throw convertException(e);
        }
    }
    
    @Override
    public void end(Context context, WorkflowAction action) throws ActionExecutorException {
        try {
            String jobId = action.getExternalId();
            JobClient jobClient = createJobClient(context, null);
            RunningJob runningJob = jobClient.getJob(JobID.forName(jobId));
            
            if (runningJob.isComplete()) {
                if (runningJob.isSuccessful()) {
                    // Read validation results
                    String outputPath = getOutputPath(action);
                    Properties validationResults = readValidationResults(outputPath);
                    
                    context.setExecutionData(validationResults, null);
                    context.setEndData(WorkflowAction.Status.OK, "");
                } else {
                    context.setEndData(WorkflowAction.Status.ERROR, "Validation job failed");
                }
            } else {
                context.setEndData(WorkflowAction.Status.RUNNING, "");
            }
            
        } catch (Exception e) {
            throw convertException(e);
        }
    }
    
    @Override
    public void check(Context context, WorkflowAction action) throws ActionExecutorException {
        end(context, action);
    }
    
    @Override
    public void kill(Context context, WorkflowAction action) throws ActionExecutorException {
        try {
            String jobId = action.getExternalId();
            if (jobId != null) {
                JobClient jobClient = createJobClient(context, null);
                RunningJob runningJob = jobClient.getJob(JobID.forName(jobId));
                if (runningJob != null) {
                    runningJob.killJob();
                }
            }
            context.setEndData(WorkflowAction.Status.KILLED, "");
        } catch (Exception e) {
            throw convertException(e);
        }
    }
    
    private Properties readValidationResults(String outputPath) throws IOException {
        Properties results = new Properties();
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        
        Path resultFile = new Path(outputPath, "validation-results.properties");
        if (fs.exists(resultFile)) {
            FSDataInputStream in = fs.open(resultFile);
            results.load(in);
            in.close();
        }
        
        return results;
    }
}
```

**2. Custom Action XML Schema:**
```xml
<!-- Custom action usage in workflow -->
<action name="validate-customer-data">
    <custom-data-validation xmlns="uri:oozie:custom-data-validation-action:1.0">
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <input-path>${inputPath}/customers</input-path>
        <validation-rules>/user/oozie/config/customer-validation-rules.json</validation-rules>
        <output-path>${outputPath}/validation-results</output-path>
        <configuration>
            <property>
                <name>validation.threshold.error-rate</name>
                <value>0.05</value>
            </property>
            <property>
                <name>validation.threshold.completeness</name>
                <value>0.95</value>
            </property>
        </configuration>
    </custom-data-validation>
    <ok to="check-validation-results"/>
    <error to="validation-failed"/>
</action>

<decision name="check-validation-results">
    <switch>
        <case to="process-data">
            ${wf:actionData('validate-customer-data')['validation.status'] eq 'PASS'}
        </case>
        <case to="data-quality-alert">
            ${wf:actionData('validate-customer-data')['validation.status'] eq 'WARNING'}
        </case>
        <default to="validation-failed"/>
    </switch>
</decision>
```

**3. Custom Coordinator Extension:**
```java
// Custom Coordinator Command
public class CustomDataAvailabilityCommand extends CoordinatorCommand<Void> {
    
    private String coordJobId;
    private String datasetName;
    private String customCheckLogic;
    
    public CustomDataAvailabilityCommand(String coordJobId, String datasetName, String customCheckLogic) {
        super("CustomDataAvailabilityCommand", "CustomDataAvailabilityCommand", 1);
        this.coordJobId = coordJobId;
        this.datasetName = datasetName;
        this.customCheckLogic = customCheckLogic;
    }
    
    @Override
    protected Void execute() throws CommandException {
        try {
            CoordinatorJobBean coordJob = CoordJobQueryExecutor.getInstance()
                .get(CoordJobQuery.GET_COORD_JOB, coordJobId);
            
            if (coordJob == null) {
                throw new CommandException(ErrorCode.E0604, coordJobId);
            }
            
            // Custom data availability check logic
            boolean dataAvailable = performCustomDataCheck(coordJob, datasetName, customCheckLogic);
            
            if (dataAvailable) {
                // Trigger workflow instance
                triggerWorkflowInstance(coordJob);
            } else {
                // Schedule next check
                scheduleNextCheck(coordJob);
            }
            
        } catch (Exception e) {
            throw new CommandException(ErrorCode.E1021, e.getMessage(), e);
        }
        
        return null;
    }
    
    private boolean performCustomDataCheck(CoordinatorJobBean coordJob, String datasetName, String checkLogic) {
        // Implement custom data availability logic
        // This could include:
        // - Complex file pattern matching
        // - Database query validation
        // - External API calls
        // - Custom business logic
        
        try {
            // Example: Custom file pattern check
            if ("COMPLEX_PATTERN".equals(checkLogic)) {
                return checkComplexFilePattern(coordJob, datasetName);
            }
            // Example: Database validation
            else if ("DATABASE_CHECK".equals(checkLogic)) {
                return checkDatabaseAvailability(coordJob, datasetName);
            }
            // Example: External API validation
            else if ("API_CHECK".equals(checkLogic)) {
                return checkExternalAPIData(coordJob, datasetName);
            }
            
            return false;
        } catch (Exception e) {
            LOG.error("Custom data check failed", e);
            return false;
        }
    }
    
    private boolean checkComplexFilePattern(CoordinatorJobBean coordJob, String datasetName) {
        // Custom file pattern matching logic
        Configuration conf = new Configuration();
        try {
            FileSystem fs = FileSystem.get(conf);
            String basePath = getDatasetPath(coordJob, datasetName);
            
            // Check for multiple file patterns
            String[] patterns = {"*.parquet", "*.avro", "*_SUCCESS"};
            for (String pattern : patterns) {
                FileStatus[] files = fs.globStatus(new Path(basePath, pattern));
                if (files == null || files.length == 0) {
                    return false;
                }
            }
            
            return true;
        } catch (IOException e) {
            LOG.error("File system check failed", e);
            return false;
        }
    }
    
    private boolean checkDatabaseAvailability(CoordinatorJobBean coordJob, String datasetName) {
        // Custom database availability check
        try {
            String jdbcUrl = getDatasetProperty(coordJob, datasetName, "jdbc.url");
            String query = getDatasetProperty(coordJob, datasetName, "availability.query");
            
            Connection conn = DriverManager.getConnection(jdbcUrl);
            PreparedStatement stmt = conn.prepareStatement(query);
            ResultSet rs = stmt.executeQuery();
            
            boolean hasData = rs.next() && rs.getInt(1) > 0;
            
            rs.close();
            stmt.close();
            conn.close();
            
            return hasData;
        } catch (SQLException e) {
            LOG.error("Database check failed", e);
            return false;
        }
    }
    
    private boolean checkExternalAPIData(CoordinatorJobBean coordJob, String datasetName) {
        // Custom external API data availability check
        try {
            String apiUrl = getDatasetProperty(coordJob, datasetName, "api.url");
            String apiKey = getDatasetProperty(coordJob, datasetName, "api.key");
            
            HttpClient client = HttpClients.createDefault();
            HttpGet request = new HttpGet(apiUrl);
            request.addHeader("Authorization", "Bearer " + apiKey);
            
            HttpResponse response = client.execute(request);
            int statusCode = response.getStatusLine().getStatusCode();
            
            if (statusCode == 200) {
                // Parse response to check data availability
                String responseBody = EntityUtils.toString(response.getEntity());
                return parseAPIResponse(responseBody);
            }
            
            return false;
        } catch (Exception e) {
            LOG.error("API check failed", e);
            return false;
        }
    }
}
```

**4. Plugin Configuration:**
```xml
<!-- oozie-site.xml configuration for custom extensions -->
<configuration>
    <!-- Register custom action executor -->
    <property>
        <name>oozie.service.ActionService.executor.ext.classes</name>
        <value>
            com.company.oozie.CustomDataValidationActionExecutor,
            com.company.oozie.CustomNotificationActionExecutor
        </value>
    </property>
    
    <!-- Register custom coordinator commands -->
    <property>
        <name>oozie.service.CallableQueueService.callable.classes</name>
        <value>
            com.company.oozie.CustomDataAvailabilityCommand,
            com.company.oozie.CustomSLACommand
        </value>
    </property>
    
    <!-- Custom extension configuration -->
    <property>
        <name>oozie.custom.validation.enabled</name>
        <value>true</value>
    </property>
    
    <property>
        <name>oozie.custom.validation.timeout</name>
        <value>300</value>
    </property>
</configuration>
```

**5. Custom Extension Deployment:**
```bash
#!/bin/bash
# Deploy custom Oozie extensions

OOZIE_HOME="/opt/oozie"
CUSTOM_LIB_DIR="$OOZIE_HOME/libext-custom"
EXTENSION_JAR="oozie-custom-extensions-1.0.jar"

echo "Deploying custom Oozie extensions..."

# Create custom lib directory
mkdir -p "$CUSTOM_LIB_DIR"

# Copy custom extension JAR
cp "$EXTENSION_JAR" "$CUSTOM_LIB_DIR/"

# Update Oozie configuration
cp oozie-site-custom.xml "$OOZIE_HOME/conf/oozie-site.xml"

# Restart Oozie server
echo "Restarting Oozie server..."
$OOZIE_HOME/bin/oozied.sh stop
sleep 10
$OOZIE_HOME/bin/oozied.sh start

# Verify extensions are loaded
sleep 30
curl -s "http://localhost:11000/oozie/v1/admin/status" | grep -q "NORMAL"
if [ $? -eq 0 ]; then
    echo "Oozie server started successfully with custom extensions"
else
    echo "Failed to start Oozie server"
    exit 1
fi

# Test custom action
echo "Testing custom action..."
oozie job -oozie http://localhost:11000/oozie -config test-custom-action.properties -run

echo "Custom extension deployment completed"
```

---

*[Continuing with more questions in the next batch...]*
## 🏗️ Architecture & Performance

### Q26: How do you optimize Oozie performance for large-scale workflows?
**Answer:**
**Performance Optimization Strategies:**

**1. Database Optimization:**
```xml
<!-- oozie-site.xml database tuning -->
<configuration>
    <!-- Connection pool optimization -->
    <property>
        <name>oozie.service.JPAService.pool.max.active.conn</name>
        <value>50</value>
    </property>
    
    <property>
        <name>oozie.service.JPAService.pool.max.idle.conn</name>
        <value>20</value>
    </property>
    
    <!-- Query optimization -->
    <property>
        <name>oozie.service.JPAService.jdbc.fetch.size</name>
        <value>1000</value>
    </property>
    
    <!-- Batch processing -->
    <property>
        <name>oozie.service.JPAService.jdbc.batch.size</name>
        <value>100</value>
    </property>
    
    <!-- Connection validation -->
    <property>
        <name>oozie.service.JPAService.validate.db.connection</name>
        <value>true</value>
    </property>
    
    <property>
        <name>oozie.service.JPAService.validate.db.connection.eviction.interval</name>
        <value>300000</value>
    </property>
</configuration>
```

**2. Callable Queue Service Tuning:**
```xml
<configuration>
    <!-- Increase thread pool size -->
    <property>
        <name>oozie.service.CallableQueueService.threads</name>
        <value>50</value>
    </property>
    
    <!-- Optimize queue size -->
    <property>
        <name>oozie.service.CallableQueueService.queue.size</name>
        <value>10000</value>
    </property>
    
    <!-- Callable concurrency -->
    <property>
        <name>oozie.service.CallableQueueService.callable.concurrency</name>
        <value>20</value>
    </property>
    
    <!-- Interrupt timeout -->
    <property>
        <name>oozie.service.CallableQueueService.callable.interrupt.timeout</name>
        <value>180</value>
    </property>
</configuration>
```

**3. Memory Management:**
```bash
# JVM tuning for Oozie server
export OOZIE_OPTS="-Xmx8g -Xms4g -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:+UseStringDeduplication"

# Heap dump on OOM
export OOZIE_OPTS="$OOZIE_OPTS -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/log/oozie/"

# GC logging
export OOZIE_OPTS="$OOZIE_OPTS -Xloggc:/var/log/oozie/gc.log -XX:+PrintGCDetails -XX:+PrintGCTimeStamps"
```

**4. Workflow Optimization:**
```xml
<!-- Optimized workflow structure -->
<workflow-app name="optimized-workflow" xmlns="uri:oozie:workflow:0.5">
    <!-- Use global configuration to reduce repetition -->
    <global>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <configuration>
            <property>
                <name>mapred.job.queue.name</name>
                <value>${queueName}</value>
            </property>
            <property>
                <name>mapred.compress.map.output</name>
                <value>true</value>
            </property>
            <property>
                <name>mapred.output.compress</name>
                <value>true</value>
            </property>
        </configuration>
    </global>
    
    <start to="parallel-processing"/>
    
    <!-- Maximize parallelism -->
    <fork name="parallel-processing">
        <path start="process-partition-1"/>
        <path start="process-partition-2"/>
        <path start="process-partition-3"/>
        <path start="process-partition-4"/>
    </fork>
    
    <!-- Optimized action configuration -->
    <action name="process-partition-1">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <master>yarn</master>
            <mode>cluster</mode>
            <name>OptimizedProcessing-P1</name>
            <class>com.company.OptimizedProcessor</class>
            <jar>/user/oozie/lib/optimized-processor.jar</jar>
            <spark-opts>
                --executor-memory 4g
                --executor-cores 4
                --num-executors 10
                --conf spark.sql.adaptive.enabled=true
                --conf spark.sql.adaptive.coalescePartitions.enabled=true
                --conf spark.serializer=org.apache.spark.serializer.KryoSerializer
            </spark-opts>
            <arg>${inputPath}/partition1</arg>
            <arg>${outputPath}/partition1</arg>
        </spark>
        <ok to="join-processing"/>
        <error to="fail"/>
    </action>
    
    <join name="join-processing" to="end"/>
    
    <kill name="fail">
        <message>Workflow failed: ${wf:errorMessage(wf:lastErrorNode())}</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

### Q27: How do you implement Oozie clustering and high availability?
**Answer:**
**High Availability Implementation:**

**1. Database High Availability:**
```xml
<!-- MySQL Master-Slave configuration -->
<property>
    <name>oozie.service.JPAService.jdbc.url</name>
    <value>jdbc:mysql://db-master:3306,db-slave:3306/oozie?failOverReadOnly=false&amp;autoReconnect=true&amp;maxReconnects=10</value>
</property>

<!-- Connection pool for HA -->
<property>
    <name>oozie.service.JPAService.pool.max.active.conn</name>
    <value>100</value>
</property>

<property>
    <name>oozie.service.JPAService.connection.timeout</name>
    <value>30000</value>
</property>
```

**2. Load Balancer Configuration:**
```nginx
# Nginx load balancer for Oozie servers
upstream oozie_backend {
    least_conn;
    server oozie-server1:11000 max_fails=3 fail_timeout=30s;
    server oozie-server2:11000 max_fails=3 fail_timeout=30s;
    server oozie-server3:11000 max_fails=3 fail_timeout=30s;
}

server {
    listen 11000;
    
    location / {
        proxy_pass http://oozie_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        
        # Health check
        proxy_connect_timeout 5s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /oozie/v1/admin/status {
        proxy_pass http://oozie_backend;
        access_log off;
    }
}
```

**3. Shared Storage Configuration:**
```xml
<!-- HDFS HA configuration -->
<property>
    <name>oozie.service.HadoopAccessorService.hadoop.configurations</name>
    <value>*=/etc/hadoop/conf</value>
</property>

<!-- Shared lib path -->
<property>
    <name>oozie.service.WorkflowAppService.system.libpath</name>
    <value>/user/oozie/share/lib</value>
</property>

<!-- Shared workflow storage -->
<property>
    <name>oozie.service.WorkflowStoreService.workflow.store.path</name>
    <value>/user/oozie/workflows</value>
</property>
```

**4. Health Check and Monitoring:**
```bash
#!/bin/bash
# Oozie cluster health check script

OOZIE_SERVERS=("oozie-server1:11000" "oozie-server2:11000" "oozie-server3:11000")
LOAD_BALANCER="oozie-lb:11000"

check_oozie_server() {
    local server=$1
    local status_url="http://$server/oozie/v1/admin/status"
    
    response=$(curl -s -w "%{http_code}" -o /tmp/oozie_status_$$ "$status_url")
    http_code=$(tail -n1 <<< "$response")
    
    if [[ "$http_code" == "200" ]]; then
        status=$(grep -o '"systemMode":"[^"]*"' /tmp/oozie_status_$$ | cut -d'"' -f4)
        if [[ "$status" == "NORMAL" ]]; then
            echo "✓ $server: HEALTHY"
            return 0
        else
            echo "✗ $server: UNHEALTHY (Status: $status)"
            return 1
        fi
    else
        echo "✗ $server: UNREACHABLE (HTTP: $http_code)"
        return 1
    fi
}

check_database_connectivity() {
    local server=$1
    local db_url="http://$server/oozie/v1/admin/instrumentation"
    
    response=$(curl -s "$db_url" | grep -o '"db-connections-active":[0-9]*' | cut -d':' -f2)
    
    if [[ -n "$response" && "$response" -gt 0 ]]; then
        echo "✓ $server: Database connectivity OK (Active connections: $response)"
        return 0
    else
        echo "✗ $server: Database connectivity issues"
        return 1
    fi
}

# Check individual servers
healthy_servers=0
for server in "${OOZIE_SERVERS[@]}"; do
    if check_oozie_server "$server"; then
        check_database_connectivity "$server"
        ((healthy_servers++))
    fi
done

# Check load balancer
echo "Checking load balancer..."
if check_oozie_server "$LOAD_BALANCER"; then
    echo "✓ Load balancer: HEALTHY"
else
    echo "✗ Load balancer: UNHEALTHY"
fi

# Overall health assessment
total_servers=${#OOZIE_SERVERS[@]}
if [[ $healthy_servers -eq $total_servers ]]; then
    echo "✓ Cluster Status: ALL SERVERS HEALTHY"
    exit 0
elif [[ $healthy_servers -gt 0 ]]; then
    echo "⚠ Cluster Status: PARTIAL OUTAGE ($healthy_servers/$total_servers healthy)"
    exit 1
else
    echo "✗ Cluster Status: COMPLETE OUTAGE"
    exit 2
fi

rm -f /tmp/oozie_status_$$
```

### Q28: How do you monitor and troubleshoot Oozie performance issues?
**Answer:**
**Performance Monitoring and Troubleshooting:**

**1. JMX Monitoring Configuration:**
```xml
<!-- Enable JMX monitoring -->
<property>
    <name>oozie.service.InstrumentationService.jmx.enabled</name>
    <value>true</value>
</property>

<property>
    <name>oozie.service.InstrumentationService.jmx.port</name>
    <value>9999</value>
</property>
```

**2. Performance Monitoring Script:**
```python
import requests
import json
import time
from datetime import datetime

class OoziePerformanceMonitor:
    def __init__(self, oozie_url):
        self.oozie_url = oozie_url
        self.base_url = f"{oozie_url}/v1"
        
    def get_server_metrics(self):
        """Get server performance metrics"""
        try:
            response = requests.get(f"{self.base_url}/admin/instrumentation")
            data = response.json()
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'server_status': self.get_server_status(),
                'database_metrics': self.extract_database_metrics(data),
                'queue_metrics': self.extract_queue_metrics(data),
                'memory_metrics': self.extract_memory_metrics(data),
                'job_metrics': self.get_job_metrics()
            }
            
            return metrics
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            return None
    
    def get_server_status(self):
        """Get server status"""
        try:
            response = requests.get(f"{self.base_url}/admin/status")
            return response.json()
        except:
            return {"systemMode": "UNKNOWN"}
    
    def extract_database_metrics(self, data):
        """Extract database performance metrics"""
        db_metrics = {}
        
        # Database connection pool metrics
        for key, value in data.get('instrumentation', {}).items():
            if 'db-connections' in key:
                db_metrics[key] = value
        
        return db_metrics
    
    def extract_queue_metrics(self, data):
        """Extract callable queue metrics"""
        queue_metrics = {}
        
        for key, value in data.get('instrumentation', {}).items():
            if 'callablequeue' in key.lower():
                queue_metrics[key] = value
        
        return queue_metrics
    
    def extract_memory_metrics(self, data):
        """Extract JVM memory metrics"""
        memory_metrics = {}
        
        for key, value in data.get('instrumentation', {}).items():
            if any(mem_key in key.lower() for mem_key in ['memory', 'heap', 'gc']):
                memory_metrics[key] = value
        
        return memory_metrics
    
    def get_job_metrics(self):
        """Get job execution metrics"""
        try:
            # Get recent jobs
            response = requests.get(f"{self.base_url}/jobs?jobtype=wf&len=100")
            jobs_data = response.json()
            
            job_metrics = {
                'total_jobs': len(jobs_data.get('workflows', [])),
                'running_jobs': 0,
                'succeeded_jobs': 0,
                'failed_jobs': 0,
                'killed_jobs': 0,
                'avg_duration': 0
            }
            
            durations = []
            for job in jobs_data.get('workflows', []):
                status = job.get('status')
                if status == 'RUNNING':
                    job_metrics['running_jobs'] += 1
                elif status == 'SUCCEEDED':
                    job_metrics['succeeded_jobs'] += 1
                elif status == 'FAILED':
                    job_metrics['failed_jobs'] += 1
                elif status == 'KILLED':
                    job_metrics['killed_jobs'] += 1
                
                # Calculate duration for completed jobs
                if status in ['SUCCEEDED', 'FAILED', 'KILLED']:
                    start_time = job.get('startTime')
                    end_time = job.get('endTime')
                    if start_time and end_time:
                        duration = (datetime.fromisoformat(end_time.replace('Z', '+00:00')) - 
                                  datetime.fromisoformat(start_time.replace('Z', '+00:00'))).total_seconds()
                        durations.append(duration)
            
            if durations:
                job_metrics['avg_duration'] = sum(durations) / len(durations)
            
            return job_metrics
        except Exception as e:
            print(f"Error getting job metrics: {e}")
            return {}
    
    def analyze_performance_issues(self, metrics):
        """Analyze metrics for performance issues"""
        issues = []
        
        # Check database connection pool
        db_metrics = metrics.get('database_metrics', {})
        active_connections = db_metrics.get('db-connections-active', 0)
        max_connections = db_metrics.get('db-connections-max', 100)
        
        if active_connections > max_connections * 0.8:
            issues.append({
                'type': 'DATABASE_POOL_HIGH',
                'severity': 'WARNING',
                'message': f"Database connection pool usage high: {active_connections}/{max_connections}"
            })
        
        # Check queue metrics
        queue_metrics = metrics.get('queue_metrics', {})
        queue_size = queue_metrics.get('callablequeue-size', 0)
        
        if queue_size > 1000:
            issues.append({
                'type': 'QUEUE_SIZE_HIGH',
                'severity': 'WARNING',
                'message': f"Callable queue size high: {queue_size}"
            })
        
        # Check job failure rate
        job_metrics = metrics.get('job_metrics', {})
        total_jobs = job_metrics.get('total_jobs', 0)
        failed_jobs = job_metrics.get('failed_jobs', 0)
        
        if total_jobs > 0:
            failure_rate = failed_jobs / total_jobs
            if failure_rate > 0.1:
                issues.append({
                    'type': 'HIGH_FAILURE_RATE',
                    'severity': 'CRITICAL',
                    'message': f"High job failure rate: {failure_rate:.2%}"
                })
        
        # Check average job duration
        avg_duration = job_metrics.get('avg_duration', 0)
        if avg_duration > 3600:  # 1 hour
            issues.append({
                'type': 'LONG_JOB_DURATION',
                'severity': 'WARNING',
                'message': f"Average job duration high: {avg_duration/60:.1f} minutes"
            })
        
        return issues
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        metrics = self.get_server_metrics()
        if not metrics:
            return None
        
        issues = self.analyze_performance_issues(metrics)
        
        report = {
            'timestamp': metrics['timestamp'],
            'server_status': metrics['server_status']['systemMode'],
            'summary': {
                'total_jobs': metrics['job_metrics'].get('total_jobs', 0),
                'running_jobs': metrics['job_metrics'].get('running_jobs', 0),
                'success_rate': self.calculate_success_rate(metrics['job_metrics']),
                'avg_duration_minutes': metrics['job_metrics'].get('avg_duration', 0) / 60
            },
            'performance_issues': issues,
            'recommendations': self.generate_recommendations(issues)
        }
        
        return report
    
    def calculate_success_rate(self, job_metrics):
        """Calculate job success rate"""
        total = job_metrics.get('total_jobs', 0)
        succeeded = job_metrics.get('succeeded_jobs', 0)
        
        if total > 0:
            return succeeded / total
        return 0
    
    def generate_recommendations(self, issues):
        """Generate performance improvement recommendations"""
        recommendations = []
        
        for issue in issues:
            if issue['type'] == 'DATABASE_POOL_HIGH':
                recommendations.append("Increase database connection pool size or optimize database queries")
            elif issue['type'] == 'QUEUE_SIZE_HIGH':
                recommendations.append("Increase callable queue threads or optimize workflow complexity")
            elif issue['type'] == 'HIGH_FAILURE_RATE':
                recommendations.append("Review failed jobs and improve error handling")
            elif issue['type'] == 'LONG_JOB_DURATION':
                recommendations.append("Optimize workflow actions and increase parallelism")
        
        return recommendations

# Usage
monitor = OoziePerformanceMonitor("http://oozie-server:11000/oozie")
report = monitor.generate_performance_report()
print(json.dumps(report, indent=2))
```

**3. Database Performance Tuning:**
```sql
-- MySQL optimization for Oozie
-- Increase buffer pool size
SET GLOBAL innodb_buffer_pool_size = 2147483648; -- 2GB

-- Optimize query cache
SET GLOBAL query_cache_size = 268435456; -- 256MB
SET GLOBAL query_cache_type = ON;

-- Connection optimization
SET GLOBAL max_connections = 200;
SET GLOBAL wait_timeout = 28800;
SET GLOBAL interactive_timeout = 28800;

-- Index optimization for Oozie tables
CREATE INDEX idx_wf_jobs_status_created ON WF_JOBS(status, created_time);
CREATE INDEX idx_coord_jobs_status_created ON COORD_JOBS(status, created_time);
CREATE INDEX idx_wf_actions_wf_id_status ON WF_ACTIONS(wf_id, status);

-- Analyze table statistics
ANALYZE TABLE WF_JOBS;
ANALYZE TABLE COORD_JOBS;
ANALYZE TABLE WF_ACTIONS;
ANALYZE TABLE COORD_ACTIONS;
```

### Q29: How do you implement Oozie security and access control?
**Answer:**
**Security Implementation:**

**1. Kerberos Authentication:**
```xml
<!-- oozie-site.xml Kerberos configuration -->
<configuration>
    <!-- Enable Kerberos authentication -->
    <property>
        <name>oozie.authentication.type</name>
        <value>kerberos</value>
    </property>
    
    <property>
        <name>oozie.authentication.kerberos.principal</name>
        <value>oozie/_HOST@REALM.COM</value>
    </property>
    
    <property>
        <name>oozie.authentication.kerberos.keytab</name>
        <value>/etc/security/keytabs/oozie.service.keytab</value>
    </property>
    
    <!-- Hadoop security -->
    <property>
        <name>oozie.service.HadoopAccessorService.kerberos.enabled</name>
        <value>true</value>
    </property>
    
    <property>
        <name>local.realm</name>
        <value>REALM.COM</value>
    </property>
    
    <property>
        <name>oozie.service.HadoopAccessorService.keytab.file</name>
        <value>/etc/security/keytabs/oozie.service.keytab</value>
    </property>
    
    <property>
        <name>oozie.service.HadoopAccessorService.kerberos.principal</name>
        <value>oozie/_HOST@REALM.COM</value>
    </property>
</configuration>
```

**2. Authorization Configuration:**
```xml
<!-- Authorization service configuration -->
<property>
    <name>oozie.service.AuthorizationService.security.enabled</name>
    <value>true</value>
</property>

<property>
    <name>oozie.service.AuthorizationService.default.group.as.acl</name>
    <value>false</value>
</property>

<!-- Admin users -->
<property>
    <name>oozie.service.AuthorizationService.admin.users</name>
    <value>oozie,admin,hdfs</value>
</property>

<!-- Admin groups -->
<property>
    <name>oozie.service.AuthorizationService.admin.groups</name>
    <value>admin,supergroup</value>
</property>
```

**3. Workflow-level Security:**
```xml
<!-- Secure workflow with credentials -->
<workflow-app name="secure-workflow" xmlns="uri:oozie:workflow:0.5">
    <credentials>
        <credential name="hive-creds" type="hive">
            <property>
                <name>hive.metastore.kerberos.principal</name>
                <value>hive/_HOST@REALM.COM</value>
            </property>
            <property>
                <name>hive.metastore.sasl.enabled</name>
                <value>true</value>
            </property>
        </credential>
        
        <credential name="hbase-creds" type="hbase">
            <property>
                <name>hbase.security.authentication</name>
                <value>kerberos</value>
            </property>
        </credential>
    </credentials>
    
    <start to="secure-hive-action"/>
    
    <action name="secure-hive-action" cred="hive-creds">
        <hive xmlns="uri:oozie:hive-action:0.5">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <script>secure-query.hql</script>
            <param>INPUT_TABLE=${inputTable}</param>
            <param>OUTPUT_TABLE=${outputTable}</param>
        </hive>
        <ok to="secure-hbase-action"/>
        <error to="fail"/>
    </action>
    
    <action name="secure-hbase-action" cred="hbase-creds">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.hbase.SecureHBaseProcessor</main-class>
            <arg>${inputPath}</arg>
            <arg>${outputPath}</arg>
        </java>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Secure workflow failed</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**4. SSL/TLS Configuration:**
```xml
<!-- SSL configuration -->
<property>
    <name>oozie.https.enabled</name>
    <value>true</value>
</property>

<property>
    <name>oozie.https.port</name>
    <value>11443</value>
</property>

<property>
    <name>oozie.https.keystore.file</name>
    <value>/etc/security/keystores/oozie-keystore.jks</value>
</property>

<property>
    <name>oozie.https.keystore.pass</name>
    <value>keystore_password</value>
</property>

<property>
    <name>oozie.https.truststore.file</name>
    <value>/etc/security/keystores/oozie-truststore.jks</value>
</property>

<property>
    <name>oozie.https.truststore.pass</name>
    <value>truststore_password</value>
</property>
```

**5. Access Control Implementation:**
```java
// Custom authorization provider
public class CustomAuthorizationProvider implements AuthorizationProvider {
    
    @Override
    public void init() throws AuthorizationException {
        // Initialize authorization provider
    }
    
    @Override
    public void authorize(String user, String group, String operation, String resource) 
            throws AuthorizationException {
        
        // Custom authorization logic
        if (!isAuthorized(user, group, operation, resource)) {
            throw new AuthorizationException(
                String.format("User %s is not authorized to perform %s on %s", 
                             user, operation, resource));
        }
    }
    
    private boolean isAuthorized(String user, String group, String operation, String resource) {
        // Implement custom authorization logic
        
        // Check admin users
        if (isAdminUser(user)) {
            return true;
        }
        
        // Check resource-specific permissions
        if (resource.startsWith("/workflows/")) {
            return checkWorkflowPermissions(user, group, operation, resource);
        } else if (resource.startsWith("/coordinators/")) {
            return checkCoordinatorPermissions(user, group, operation, resource);
        }
        
        // Default deny
        return false;
    }
    
    private boolean checkWorkflowPermissions(String user, String group, String operation, String resource) {
        // Check workflow-specific permissions
        String workflowPath = extractWorkflowPath(resource);
        
        // Check if user owns the workflow
        if (isWorkflowOwner(user, workflowPath)) {
            return true;
        }
        
        // Check group permissions
        if (hasGroupPermission(group, operation, workflowPath)) {
            return true;
        }
        
        // Check read-only access for monitoring
        if ("READ".equals(operation) && hasMonitoringAccess(user, group)) {
            return true;
        }
        
        return false;
    }
    
    private boolean isAdminUser(String user) {
        String adminUsers = ConfigurationService.get("oozie.service.AuthorizationService.admin.users");
        return Arrays.asList(adminUsers.split(",")).contains(user);
    }
    
    private boolean isWorkflowOwner(String user, String workflowPath) {
        // Check HDFS ownership
        try {
            Configuration conf = new Configuration();
            FileSystem fs = FileSystem.get(conf);
            FileStatus status = fs.getFileStatus(new Path(workflowPath));
            return user.equals(status.getOwner());
        } catch (IOException e) {
            return false;
        }
    }
}
```

### Q30: How do you implement disaster recovery for Oozie?
**Answer:**
**Disaster Recovery Implementation:**

**1. Database Backup and Recovery:**
```bash
#!/bin/bash
# Oozie database backup script

DB_HOST="oozie-db-primary"
DB_NAME="oozie"
DB_USER="oozie"
DB_PASS="password"
BACKUP_DIR="/backup/oozie"
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate backup filename
BACKUP_FILE="oozie_backup_$(date +%Y%m%d_%H%M%S).sql"
BACKUP_PATH="$BACKUP_DIR/$BACKUP_FILE"

echo "Starting Oozie database backup..."

# Create database backup
mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    --hex-blob \
    "$DB_NAME" > "$BACKUP_PATH"

if [ $? -eq 0 ]; then
    echo "Database backup completed: $BACKUP_PATH"
    
    # Compress backup
    gzip "$BACKUP_PATH"
    echo "Backup compressed: ${BACKUP_PATH}.gz"
    
    # Copy to remote location
    rsync -av "${BACKUP_PATH}.gz" backup-server:/backup/oozie/
    
    # Clean up old backups
    find "$BACKUP_DIR" -name "oozie_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    
else
    echo "Database backup failed!"
    exit 1
fi
```

**2. HDFS Data Backup:**
```bash
#!/bin/bash
# HDFS workflow and data backup

HDFS_BACKUP_PATHS=(
    "/user/oozie/workflows"
    "/user/oozie/coordinators"
    "/user/oozie/bundles"
    "/user/oozie/share/lib"
)

BACKUP_CLUSTER="backup-cluster"
BACKUP_BASE_PATH="/backup/oozie"

for path in "${HDFS_BACKUP_PATHS[@]}"; do
    echo "Backing up $path..."
    
    # Use DistCp for efficient backup
    hadoop distcp \
        -update \
        -delete \
        -skipcrccheck \
        "$path" \
        "hdfs://$BACKUP_CLUSTER$BACKUP_BASE_PATH$path"
    
    if [ $? -eq 0 ]; then
        echo "✓ Backup completed for $path"
    else
        echo "✗ Backup failed for $path"
    fi
done

# Backup metadata
hdfs dfsadmin -metasave /tmp/oozie_metadata_$(date +%Y%m%d).txt
hadoop fs -put /tmp/oozie_metadata_$(date +%Y%m%d).txt "$BACKUP_BASE_PATH/metadata/"
```

**3. Configuration Backup:**
```bash
#!/bin/bash
# Oozie configuration backup

OOZIE_HOME="/opt/oozie"
CONFIG_BACKUP_DIR="/backup/oozie/config"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p "$CONFIG_BACKUP_DIR/$TIMESTAMP"

# Backup configuration files
cp -r "$OOZIE_HOME/conf" "$CONFIG_BACKUP_DIR/$TIMESTAMP/"

# Backup custom libraries
if [ -d "$OOZIE_HOME/libext" ]; then
    cp -r "$OOZIE_HOME/libext" "$CONFIG_BACKUP_DIR/$TIMESTAMP/"
fi

# Backup custom extensions
if [ -d "$OOZIE_HOME/libext-custom" ]; then
    cp -r "$OOZIE_HOME/libext-custom" "$CONFIG_BACKUP_DIR/$TIMESTAMP/"
fi

# Create archive
tar -czf "$CONFIG_BACKUP_DIR/oozie_config_$TIMESTAMP.tar.gz" \
    -C "$CONFIG_BACKUP_DIR" "$TIMESTAMP"

# Clean up temporary directory
rm -rf "$CONFIG_BACKUP_DIR/$TIMESTAMP"

echo "Configuration backup completed: oozie_config_$TIMESTAMP.tar.gz"
```

**4. Disaster Recovery Procedure:**
```bash
#!/bin/bash
# Oozie disaster recovery script

set -e

DR_MODE="$1"  # full, database, hdfs, config
BACKUP_DATE="$2"

if [[ -z "$DR_MODE" || -z "$BACKUP_DATE" ]]; then
    echo "Usage: $0 <full|database|hdfs|config> <backup_date>"
    echo "Example: $0 full 20240115"
    exit 1
fi

echo "Starting Oozie disaster recovery..."
echo "Mode: $DR_MODE"
echo "Backup Date: $BACKUP_DATE"

# Stop Oozie services
stop_oozie_services() {
    echo "Stopping Oozie services..."
    systemctl stop oozie
    sleep 10
}

# Restore database
restore_database() {
    echo "Restoring database..."
    
    BACKUP_FILE="/backup/oozie/oozie_backup_${BACKUP_DATE}_*.sql.gz"
    LATEST_BACKUP=$(ls -t $BACKUP_FILE 2>/dev/null | head -n1)
    
    if [[ -z "$LATEST_BACKUP" ]]; then
        echo "No database backup found for $BACKUP_DATE"
        exit 1
    fi
    
    echo "Restoring from: $LATEST_BACKUP"
    
    # Drop and recreate database
    mysql -u root -p -e "DROP DATABASE IF EXISTS oozie; CREATE DATABASE oozie;"
    
    # Restore from backup
    zcat "$LATEST_BACKUP" | mysql -u root -p oozie
    
    echo "Database restoration completed"
}

# Restore HDFS data
restore_hdfs() {
    echo "Restoring HDFS data..."
    
    BACKUP_CLUSTER="backup-cluster"
    BACKUP_BASE_PATH="/backup/oozie"
    
    HDFS_RESTORE_PATHS=(
        "/user/oozie/workflows"
        "/user/oozie/coordinators"
        "/user/oozie/bundles"
        "/user/oozie/share/lib"
    )
    
    for path in "${HDFS_RESTORE_PATHS[@]}"; do
        echo "Restoring $path..."
        
        # Remove existing data
        hadoop fs -rm -r -f "$path"
        
        # Restore from backup
        hadoop distcp \
            "hdfs://$BACKUP_CLUSTER$BACKUP_BASE_PATH$path" \
            "$path"
        
        echo "✓ Restored $path"
    done
}

# Restore configuration
restore_config() {
    echo "Restoring configuration..."
    
    CONFIG_BACKUP="/backup/oozie/config/oozie_config_${BACKUP_DATE}_*.tar.gz"
    LATEST_CONFIG=$(ls -t $CONFIG_BACKUP 2>/dev/null | head -n1)
    
    if [[ -z "$LATEST_CONFIG" ]]; then
        echo "No configuration backup found for $BACKUP_DATE"
        exit 1
    fi
    
    echo "Restoring from: $LATEST_CONFIG"
    
    # Backup current config
    cp -r /opt/oozie/conf /opt/oozie/conf.backup.$(date +%Y%m%d_%H%M%S)
    
    # Extract and restore
    tar -xzf "$LATEST_CONFIG" -C /tmp/
    EXTRACTED_DIR=$(tar -tzf "$LATEST_CONFIG" | head -1 | cut -f1 -d"/")
    
    cp -r "/tmp/$EXTRACTED_DIR/conf"/* /opt/oozie/conf/
    
    if [[ -d "/tmp/$EXTRACTED_DIR/libext" ]]; then
        cp -r "/tmp/$EXTRACTED_DIR/libext"/* /opt/oozie/libext/
    fi
    
    # Clean up
    rm -rf "/tmp/$EXTRACTED_DIR"
    
    echo "Configuration restoration completed"
}

# Start Oozie services
start_oozie_services() {
    echo "Starting Oozie services..."
    systemctl start oozie
    
    # Wait for service to be ready
    sleep 30
    
    # Verify service
    if curl -s "http://localhost:11000/oozie/v1/admin/status" | grep -q "NORMAL"; then
        echo "✓ Oozie service started successfully"
    else
        echo "✗ Oozie service failed to start properly"
        exit 1
    fi
}

# Execute recovery based on mode
case "$DR_MODE" in
    "full")
        stop_oozie_services
        restore_database
        restore_hdfs
        restore_config
        start_oozie_services
        ;;
    "database")
        stop_oozie_services
        restore_database
        start_oozie_services
        ;;
    "hdfs")
        restore_hdfs
        ;;
    "config")
        stop_oozie_services
        restore_config
        start_oozie_services
        ;;
    *)
        echo "Invalid recovery mode: $DR_MODE"
        exit 1
        ;;
esac

echo "Disaster recovery completed successfully!"

# Verify recovery
echo "Verifying recovery..."
oozie admin -oozie http://localhost:11000/oozie -status
oozie jobs -oozie http://localhost:11000/oozie -jobtype workflow -len 5
```

---

*[Continuing with more questions in the next batch...]*
## 🌊 Streaming & Real-time Processing

### Q31: How does Oozie handle near real-time data processing workflows?
**Answer:**
**Near Real-time Processing with Oozie:**

**1. High-frequency Coordinator:**
```xml
<coordinator-app name="near-realtime-processing" 
                 frequency="${coord:minutes(5)}" 
                 start="2024-01-01T00:00Z" 
                 end="2024-12-31T23:59Z" 
                 timezone="UTC">
    
    <datasets>
        <dataset name="streaming-data" frequency="${coord:minutes(5)}" 
                 initial-instance="2024-01-01T00:00Z" timezone="UTC">
            <uri-template>/data/streaming/${YEAR}/${MONTH}/${DAY}/${HOUR}/${MINUTE}</uri-template>
            <done-flag>_READY</done-flag>
        </dataset>
    </datasets>
    
    <input-events>
        <data-in name="current-batch" dataset="streaming-data">
            <instance>${coord:current(0)}</instance>
        </data-in>
    </input-events>
    
    <action>
        <workflow>
            <app-path>/user/oozie/workflows/streaming-processor</app-path>
            <configuration>
                <property>
                    <name>inputPath</name>
                    <value>${coord:dataIn('current-batch')}</value>
                </property>
                <property>
                    <name>processingTime</name>
                    <value>${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd-HH-mm')}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

**2. Streaming Integration Workflow:**
```xml
<workflow-app name="streaming-integration" xmlns="uri:oozie:workflow:0.5">
    <start to="check-kafka-lag"/>
    
    <action name="check-kafka-lag">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.kafka.LagChecker</main-class>
            <arg>${kafkaTopic}</arg>
            <arg>${consumerGroup}</arg>
            <capture-output/>
        </java>
        <ok to="decide-processing-mode"/>
        <error to="fail"/>
    </action>
    
    <decision name="decide-processing-mode">
        <switch>
            <case to="batch-processing">
                ${wf:actionData('check-kafka-lag')['lagMinutes'] gt 10}
            </case>
            <default to="streaming-processing"/>
        </switch>
    </decision>
    
    <action name="streaming-processing">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>StreamingProcessor</name>
            <class>com.company.streaming.SparkStreamingProcessor</class>
            <jar>/user/oozie/lib/streaming-processor.jar</jar>
            <spark-opts>--conf spark.streaming.backpressure.enabled=true</spark-opts>
            <arg>${kafkaBrokers}</arg>
            <arg>${kafkaTopic}</arg>
            <arg>${outputPath}</arg>
        </spark>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Streaming workflow failed</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

### Q32: How do you integrate Oozie with Apache Kafka for stream processing?
**Answer:**
**Kafka Integration Patterns:**

**1. Kafka Consumer Workflow:**
```xml
<action name="kafka-consumer">
    <spark xmlns="uri:oozie:spark-action:0.2">
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-name>
        <master>yarn</master>
        <mode>cluster</mode>
        <name>KafkaConsumer</name>
        <class>com.company.kafka.KafkaSparkConsumer</class>
        <jar>/user/oozie/lib/kafka-consumer.jar</jar>
        <spark-opts>
            --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0
            --conf spark.streaming.kafka.maxRatePerPartition=1000
        </spark-opts>
        <arg>${kafkaBrokers}</arg>
        <arg>${kafkaTopic}</arg>
        <arg>${checkpointLocation}</arg>
        <arg>${outputPath}</arg>
    </spark>
    <ok to="validate-output"/>
    <error to="handle-kafka-error"/>
</action>
```

**2. Kafka Producer Integration:**
```java
// Kafka producer in custom action
public class KafkaProducerAction {
    public static void main(String[] args) throws Exception {
        String brokers = args[0];
        String topic = args[1];
        String dataPath = args[2];
        
        Properties props = new Properties();
        props.put("bootstrap.servers", brokers);
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("acks", "all");
        props.put("retries", 3);
        
        KafkaProducer<String, String> producer = new KafkaProducer<>(props);
        
        // Read processed data and send to Kafka
        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(conf);
        
        FileStatus[] files = fs.listStatus(new Path(dataPath));
        int messageCount = 0;
        
        for (FileStatus file : files) {
            if (file.isFile() && !file.getPath().getName().startsWith("_")) {
                BufferedReader reader = new BufferedReader(
                    new InputStreamReader(fs.open(file.getPath())));
                
                String line;
                while ((line = reader.readLine()) != null) {
                    ProducerRecord<String, String> record = 
                        new ProducerRecord<>(topic, UUID.randomUUID().toString(), line);
                    producer.send(record);
                    messageCount++;
                }
                reader.close();
            }
        }
        
        producer.flush();
        producer.close();
        
        // Output results for Oozie
        Properties output = new Properties();
        output.setProperty("messagesSent", String.valueOf(messageCount));
        output.setProperty("topic", topic);
        
        FileOutputStream fos = new FileOutputStream(System.getProperty("oozie.action.output.properties"));
        output.store(fos, "Kafka Producer Results");
        fos.close();
    }
}
```

### Q33: How do you handle backpressure and flow control in Oozie workflows?
**Answer:**
**Backpressure Management:**

**1. Dynamic Frequency Adjustment:**
```xml
<coordinator-app name="adaptive-frequency-coordinator">
    <action>
        <workflow>
            <app-path>/user/oozie/workflows/adaptive-processing</app-path>
        </workflow>
    </action>
</coordinator-app>
```

**2. Queue Monitoring and Throttling:**
```java
public class BackpressureController {
    public static void main(String[] args) throws Exception {
        String queueName = args[0];
        String maxQueueSize = args[1];
        String throttleThreshold = args[2];
        
        // Check queue depth
        YarnClient yarnClient = YarnClient.createYarnClient();
        yarnClient.init(new Configuration());
        yarnClient.start();
        
        QueueInfo queueInfo = yarnClient.getQueueInfo(queueName);
        int currentJobs = getCurrentRunningJobs(queueName);
        
        Properties output = new Properties();
        
        if (currentJobs > Integer.parseInt(throttleThreshold)) {
            output.setProperty("shouldThrottle", "true");
            output.setProperty("recommendedDelay", "300"); // 5 minutes
            output.setProperty("currentLoad", String.valueOf(currentJobs));
        } else {
            output.setProperty("shouldThrottle", "false");
            output.setProperty("recommendedDelay", "0");
        }
        
        FileOutputStream fos = new FileOutputStream(System.getProperty("oozie.action.output.properties"));
        output.store(fos, "Backpressure Control Results");
        fos.close();
    }
    
    private static int getCurrentRunningJobs(String queueName) {
        // Implementation to count running jobs in queue
        return 0;
    }
}
```

**3. Adaptive Workflow:**
```xml
<workflow-app name="backpressure-aware-workflow">
    <start to="check-system-load"/>
    
    <action name="check-system-load">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.BackpressureController</main-class>
            <arg>${queueName}</arg>
            <arg>${maxQueueSize}</arg>
            <arg>${throttleThreshold}</arg>
            <capture-output/>
        </java>
        <ok to="decide-processing-strategy"/>
        <error to="fail"/>
    </action>
    
    <decision name="decide-processing-strategy">
        <switch>
            <case to="throttled-processing">
                ${wf:actionData('check-system-load')['shouldThrottle'] eq 'true'}
            </case>
            <default to="normal-processing"/>
        </switch>
    </decision>
    
    <action name="throttled-processing">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.ThrottledProcessor</main-class>
            <arg>${inputPath}</arg>
            <arg>${outputPath}</arg>
            <arg>${wf:actionData('check-system-load')['recommendedDelay']}</arg>
        </java>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <action name="normal-processing">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>NormalProcessing</name>
            <class>com.company.NormalProcessor</class>
            <jar>/user/oozie/lib/processor.jar</jar>
            <arg>${inputPath}</arg>
            <arg>${outputPath}</arg>
        </spark>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Backpressure workflow failed</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

---

## 🚀 Production & Operations

### Q34: How do you implement comprehensive logging and monitoring for Oozie workflows?
**Answer:**
**Comprehensive Logging Strategy:**

**1. Structured Logging Configuration:**
```xml
<!-- log4j.properties for Oozie -->
# Root logger
log4j.rootLogger=INFO, oozie

# Oozie appender
log4j.appender.oozie=org.apache.log4j.DailyRollingFileAppender
log4j.appender.oozie.file=${oozie.log.dir}/oozie.log
log4j.appender.oozie.datePattern='.'yyyy-MM-dd
log4j.appender.oozie.layout=org.apache.log4j.PatternLayout
log4j.appender.oozie.layout.conversionPattern=%d{ISO8601} %5p %c{1}:%L - %m%n

# Audit logging
log4j.logger.oozieaudit=INFO, oozieaudit
log4j.appender.oozieaudit=org.apache.log4j.DailyRollingFileAppender
log4j.appender.oozieaudit.file=${oozie.log.dir}/oozie-audit.log
log4j.appender.oozieaudit.datePattern='.'yyyy-MM-dd
log4j.appender.oozieaudit.layout=org.apache.log4j.PatternLayout
log4j.appender.oozieaudit.layout.conversionPattern=%d{ISO8601} %5p %c{1}:%L - %m%n

# Instrumentation logging
log4j.logger.oozieops=INFO, oozieops
log4j.appender.oozieops=org.apache.log4j.DailyRollingFileAppender
log4j.appender.oozieops.file=${oozie.log.dir}/oozie-ops.log
log4j.appender.oozieops.datePattern='.'yyyy-MM-dd
log4j.appender.oozieops.layout=org.apache.log4j.PatternLayout
log4j.appender.oozieops.layout.conversionPattern=%d{ISO8601} %5p %c{1}:%L - %m%n
```

**2. Custom Logging Action:**
```java
public class WorkflowLogger {
    public static void main(String[] args) throws Exception {
        String workflowId = args[0];
        String actionName = args[1];
        String logLevel = args[2];
        String message = args[3];
        
        // Create structured log entry
        Map<String, Object> logEntry = new HashMap<>();
        logEntry.put("timestamp", Instant.now().toString());
        logEntry.put("workflowId", workflowId);
        logEntry.put("actionName", actionName);
        logEntry.put("logLevel", logLevel);
        logEntry.put("message", message);
        logEntry.put("hostname", InetAddress.getLocalHost().getHostName());
        
        // Add system metrics
        MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();
        logEntry.put("heapUsed", memoryBean.getHeapMemoryUsage().getUsed());
        logEntry.put("heapMax", memoryBean.getHeapMemoryUsage().getMax());
        
        // Convert to JSON
        ObjectMapper mapper = new ObjectMapper();
        String jsonLog = mapper.writeValueAsString(logEntry);
        
        // Write to structured log file
        String logFile = "/var/log/oozie/workflow-structured.log";
        try (FileWriter writer = new FileWriter(logFile, true)) {
            writer.write(jsonLog + "\n");
        }
        
        // Also send to external logging system (e.g., ELK stack)
        sendToElasticsearch(jsonLog);
        
        System.out.println("Log entry created: " + jsonLog);
    }
    
    private static void sendToElasticsearch(String jsonLog) {
        // Implementation to send logs to Elasticsearch
        try {
            HttpClient client = HttpClients.createDefault();
            HttpPost post = new HttpPost("http://elasticsearch:9200/oozie-logs/_doc");
            post.setEntity(new StringEntity(jsonLog, ContentType.APPLICATION_JSON));
            
            HttpResponse response = client.execute(post);
            // Handle response
        } catch (Exception e) {
            System.err.println("Failed to send log to Elasticsearch: " + e.getMessage());
        }
    }
}
```

**3. Monitoring Integration:**
```python
import requests
import json
import time
from datetime import datetime, timedelta

class OozieMonitor:
    def __init__(self, oozie_url, alert_webhook=None):
        self.oozie_url = oozie_url
        self.alert_webhook = alert_webhook
        self.base_url = f"{oozie_url}/v1"
    
    def monitor_workflows(self):
        """Monitor workflow health and performance"""
        try:
            # Get recent workflows
            response = requests.get(f"{self.base_url}/jobs?jobtype=wf&len=50")
            workflows = response.json().get('workflows', [])
            
            alerts = []
            
            for workflow in workflows:
                # Check for long-running workflows
                if workflow['status'] == 'RUNNING':
                    start_time = datetime.fromisoformat(workflow['startTime'].replace('Z', '+00:00'))
                    duration = datetime.now(start_time.tzinfo) - start_time
                    
                    if duration > timedelta(hours=2):
                        alerts.append({
                            'type': 'LONG_RUNNING_WORKFLOW',
                            'workflow_id': workflow['id'],
                            'workflow_name': workflow['appName'],
                            'duration_hours': duration.total_seconds() / 3600,
                            'severity': 'WARNING'
                        })
                
                # Check for failed workflows
                elif workflow['status'] == 'FAILED':
                    alerts.append({
                        'type': 'WORKFLOW_FAILED',
                        'workflow_id': workflow['id'],
                        'workflow_name': workflow['appName'],
                        'end_time': workflow.get('endTime'),
                        'severity': 'CRITICAL'
                    })
            
            # Send alerts
            for alert in alerts:
                self.send_alert(alert)
            
            return alerts
            
        except Exception as e:
            print(f"Error monitoring workflows: {e}")
            return []
    
    def monitor_coordinators(self):
        """Monitor coordinator job health"""
        try:
            response = requests.get(f"{self.base_url}/jobs?jobtype=coord&len=20")
            coordinators = response.json().get('coordinatorjobs', [])
            
            alerts = []
            
            for coord in coordinators:
                # Check for coordinators behind schedule
                if coord['status'] == 'RUNNING':
                    next_materialized = coord.get('nextMaterializedTime')
                    if next_materialized:
                        next_time = datetime.fromisoformat(next_materialized.replace('Z', '+00:00'))
                        if datetime.now(next_time.tzinfo) > next_time + timedelta(hours=1):
                            alerts.append({
                                'type': 'COORDINATOR_BEHIND_SCHEDULE',
                                'coordinator_id': coord['coordJobId'],
                                'coordinator_name': coord['coordJobName'],
                                'behind_hours': (datetime.now(next_time.tzinfo) - next_time).total_seconds() / 3600,
                                'severity': 'WARNING'
                            })
            
            return alerts
            
        except Exception as e:
            print(f"Error monitoring coordinators: {e}")
            return []
    
    def send_alert(self, alert):
        """Send alert to external system"""
        if self.alert_webhook:
            try:
                payload = {
                    'timestamp': datetime.now().isoformat(),
                    'source': 'oozie_monitor',
                    'alert': alert
                }
                
                response = requests.post(self.alert_webhook, json=payload)
                print(f"Alert sent: {alert['type']} - {response.status_code}")
                
            except Exception as e:
                print(f"Failed to send alert: {e}")

# Usage
monitor = OozieMonitor(
    oozie_url="http://oozie-server:11000/oozie",
    alert_webhook="http://alertmanager:9093/api/v1/alerts"
)

# Run monitoring
workflow_alerts = monitor.monitor_workflows()
coordinator_alerts = monitor.monitor_coordinators()
```

### Q35: How do you implement automated testing for Oozie workflows?
**Answer:**
**Automated Testing Framework:**

**1. Unit Testing for Workflow Components:**
```python
import unittest
import tempfile
import shutil
from xml.etree import ElementTree as ET

class OozieWorkflowTester(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.workflow_xml = """
        <workflow-app xmlns="uri:oozie:workflow:0.5" name="test-workflow">
            <start to="validate-data"/>
            <action name="validate-data">
                <java>
                    <job-tracker>${jobTracker}</job-tracker>
                    <name-node>${nameNode}</name-node>
                    <main-class>com.company.DataValidator</main-class>
                    <arg>${inputPath}</arg>
                </java>
                <ok to="process-data"/>
                <error to="fail"/>
            </action>
            <action name="process-data">
                <spark xmlns="uri:oozie:spark-action:0.2">
                    <job-tracker>${jobTracker}</job-tracker>
                    <name-node>${nameNode}</name-name>
                    <master>yarn</master>
                    <mode>cluster</mode>
                    <name>DataProcessor</name>
                    <class>com.company.DataProcessor</class>
                    <jar>/user/oozie/lib/processor.jar</jar>
                    <arg>${inputPath}</arg>
                    <arg>${outputPath}</arg>
                </spark>
                <ok to="end"/>
                <error to="fail"/>
            </action>
            <kill name="fail">
                <message>Workflow failed</message>
            </kill>
            <end name="end"/>
        </workflow-app>
        """
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def test_workflow_xml_validity(self):
        """Test that workflow XML is valid"""
        try:
            root = ET.fromstring(self.workflow_xml)
            self.assertEqual(root.tag, 'workflow-app')
            self.assertEqual(root.get('name'), 'test-workflow')
        except ET.ParseError as e:
            self.fail(f"Invalid XML: {e}")
    
    def test_workflow_structure(self):
        """Test workflow has required elements"""
        root = ET.fromstring(self.workflow_xml)
        
        # Check for start node
        start_nodes = root.findall('start')
        self.assertEqual(len(start_nodes), 1)
        
        # Check for end node
        end_nodes = root.findall('end')
        self.assertEqual(len(end_nodes), 1)
        
        # Check for kill node
        kill_nodes = root.findall('kill')
        self.assertEqual(len(kill_nodes), 1)
        
        # Check actions have ok/error transitions
        actions = root.findall('action')
        for action in actions:
            ok_nodes = action.findall('ok')
            error_nodes = action.findall('error')
            self.assertEqual(len(ok_nodes), 1)
            self.assertEqual(len(error_nodes), 1)
    
    def test_workflow_connectivity(self):
        """Test that all workflow nodes are connected"""
        root = ET.fromstring(self.workflow_xml)
        
        # Get all node names
        node_names = set()
        transitions = set()
        
        # Start node
        start = root.find('start')
        start_to = start.get('to')
        transitions.add(start_to)
        
        # Actions
        actions = root.findall('action')
        for action in actions:
            name = action.get('name')
            node_names.add(name)
            
            ok = action.find('ok')
            error = action.find('error')
            transitions.add(ok.get('to'))
            transitions.add(error.get('to'))
        
        # End and kill nodes
        end = root.find('end')
        kill = root.find('kill')
        node_names.add(end.get('name'))
        node_names.add(kill.get('name'))
        
        # Check all transitions point to valid nodes
        for transition in transitions:
            self.assertIn(transition, node_names, f"Transition to '{transition}' points to non-existent node")

class OozieIntegrationTest(unittest.TestCase):
    
    def setUp(self):
        self.oozie_url = "http://localhost:11000/oozie"
        self.test_properties = {
            'nameNode': 'hdfs://localhost:8020',
            'jobTracker': 'localhost:8032',
            'oozie.wf.application.path': 'hdfs://localhost:8020/user/test/workflow',
            'inputPath': '/user/test/input',
            'outputPath': '/user/test/output'
        }
    
    def test_workflow_submission(self):
        """Test workflow can be submitted successfully"""
        import requests
        
        # Create properties string
        props_str = '\n'.join([f"{k}={v}" for k, v in self.test_properties.items()])
        
        try:
            response = requests.post(
                f"{self.oozie_url}/v1/jobs",
                data=props_str,
                headers={'Content-Type': 'application/xml'}
            )
            
            self.assertEqual(response.status_code, 201)
            job_id = response.json().get('id')
            self.assertIsNotNone(job_id)
            
            # Clean up - kill the test job
            requests.put(f"{self.oozie_url}/v1/job/{job_id}?action=kill")
            
        except requests.exceptions.ConnectionError:
            self.skipTest("Oozie server not available for integration testing")
    
    def test_workflow_execution(self):
        """Test complete workflow execution"""
        # This would require a full test environment
        # Implementation depends on your testing infrastructure
        pass

# Test runner
if __name__ == '__main__':
    # Run unit tests
    unittest.main(verbosity=2)
```

**2. End-to-End Testing Framework:**
```bash
#!/bin/bash
# Oozie E2E Testing Script

set -e

TEST_DIR="/tmp/oozie_e2e_test_$$"
OOZIE_URL="http://oozie-server:11000/oozie"
HDFS_BASE="/user/test"

# Setup test environment
setup_test_env() {
    echo "Setting up test environment..."
    
    # Create test directories
    mkdir -p "$TEST_DIR"
    
    # Create test data
    cat > "$TEST_DIR/test_data.csv" << EOF
id,name,age,email
1,John Doe,30,john@example.com
2,Jane Smith,25,jane@example.com
3,Bob Johnson,35,bob@example.com
EOF
    
    # Upload test data to HDFS
    hdfs dfs -mkdir -p "$HDFS_BASE/input"
    hdfs dfs -put "$TEST_DIR/test_data.csv" "$HDFS_BASE/input/"
    
    # Upload workflow to HDFS
    hdfs dfs -mkdir -p "$HDFS_BASE/workflow"
    hdfs dfs -put workflow.xml "$HDFS_BASE/workflow/"
    hdfs dfs -put lib/ "$HDFS_BASE/workflow/"
}

# Run workflow test
run_workflow_test() {
    echo "Running workflow test..."
    
    # Create job properties
    cat > "$TEST_DIR/job.properties" << EOF
nameNode=hdfs://namenode:8020
jobTracker=resourcemanager:8032
oozie.wf.application.path=$HDFS_BASE/workflow
inputPath=$HDFS_BASE/input
outputPath=$HDFS_BASE/output
queueName=default
EOF
    
    # Submit and run workflow
    JOB_ID=$(oozie job -oozie "$OOZIE_URL" -config "$TEST_DIR/job.properties" -run | grep -o '[0-9]\{7\}-[0-9]\{12\}-oozie-W')
    
    echo "Submitted job: $JOB_ID"
    
    # Wait for completion
    wait_for_completion "$JOB_ID"
    
    # Check results
    validate_results "$JOB_ID"
}

# Wait for job completion
wait_for_completion() {
    local job_id=$1
    local max_wait=600  # 10 minutes
    local wait_time=0
    
    while [ $wait_time -lt $max_wait ]; do
        status=$(oozie job -oozie "$OOZIE_URL" -info "$job_id" | grep "Status" | awk '{print $3}')
        
        case "$status" in
            "SUCCEEDED")
                echo "✓ Job completed successfully"
                return 0
                ;;
            "FAILED"|"KILLED")
                echo "✗ Job failed with status: $status"
                oozie job -oozie "$OOZIE_URL" -log "$job_id"
                return 1
                ;;
            "RUNNING"|"PREP")
                echo "Job status: $status (waiting...)"
                sleep 30
                wait_time=$((wait_time + 30))
                ;;
            *)
                echo "Unknown status: $status"
                sleep 30
                wait_time=$((wait_time + 30))
                ;;
        esac
    done
    
    echo "✗ Job timed out after $max_wait seconds"
    return 1
}

# Validate test results
validate_results() {
    local job_id=$1
    
    echo "Validating results..."
    
    # Check output exists
    if hdfs dfs -test -d "$HDFS_BASE/output"; then
        echo "✓ Output directory exists"
    else
        echo "✗ Output directory missing"
        return 1
    fi
    
    # Check output files
    output_files=$(hdfs dfs -ls "$HDFS_BASE/output" | grep -v "^d" | wc -l)
    if [ "$output_files" -gt 0 ]; then
        echo "✓ Output files created ($output_files files)"
    else
        echo "✗ No output files found"
        return 1
    fi
    
    # Validate data content
    hdfs dfs -cat "$HDFS_BASE/output/part-*" > "$TEST_DIR/output_data.txt"
    if [ -s "$TEST_DIR/output_data.txt" ]; then
        echo "✓ Output data validation passed"
    else
        echo "✗ Output data validation failed"
        return 1
    fi
}

# Cleanup test environment
cleanup_test_env() {
    echo "Cleaning up test environment..."
    
    # Remove HDFS test data
    hdfs dfs -rm -r -f "$HDFS_BASE"
    
    # Remove local test directory
    rm -rf "$TEST_DIR"
}

# Main test execution
main() {
    echo "Starting Oozie E2E Tests..."
    
    # Trap cleanup on exit
    trap cleanup_test_env EXIT
    
    # Run tests
    setup_test_env
    run_workflow_test
    
    echo "✓ All tests passed!"
}

# Run main function
main "$@"
```

---

*[Continuing with more questions in the next batch...]*
## 🎯 Scenario-Based Questions

### Q36: Design an Oozie workflow for a complex ETL pipeline with multiple data sources
**Answer:**
**Complex ETL Pipeline Design:**

**1. Multi-source ETL Workflow:**
```xml
<workflow-app name="complex-etl-pipeline" xmlns="uri:oozie:workflow:0.5">
    <parameters>
        <property>
            <name>processDate</name>
            <description>Processing date in YYYY-MM-DD format</description>
        </property>
    </parameters>
    
    <start to="initialize-pipeline"/>
    
    <action name="initialize-pipeline">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.etl.PipelineInitializer</main-class>
            <arg>${processDate}</arg>
            <arg>${workflowId}</arg>
            <capture-output/>
        </java>
        <ok to="parallel-extraction"/>
        <error to="fail"/>
    </action>
    
    <!-- Parallel data extraction from multiple sources -->
    <fork name="parallel-extraction">
        <path start="extract-database-data"/>
        <path start="extract-api-data"/>
        <path start="extract-file-data"/>
        <path start="extract-streaming-data"/>
    </fork>
    
    <!-- Database extraction -->
    <action name="extract-database-data">
        <sqoop xmlns="uri:oozie:sqoop-action:0.4">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <command>import --connect jdbc:mysql://db-server:3306/sales --table orders --where "order_date='${processDate}'" --target-dir /data/raw/database/${processDate}</command>
        </sqoop>
        <ok to="validate-database-extraction"/>
        <error to="handle-database-error"/>
    </action>
    
    <action name="validate-database-extraction">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.validation.DataValidator</main-class>
            <arg>/data/raw/database/${processDate}</arg>
            <arg>database</arg>
            <capture-output/>
        </java>
        <ok to="join-extraction"/>
        <error to="handle-validation-error"/>
    </action>
    
    <!-- API data extraction -->
    <action name="extract-api-data">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.extractors.APIExtractor</main-class>
            <arg>${apiEndpoint}</arg>
            <arg>${processDate}</arg>
            <arg>/data/raw/api/${processDate}</arg>
            <capture-output/>
        </java>
        <ok to="validate-api-extraction"/>
        <error to="handle-api-error"/>
    </action>
    
    <action name="validate-api-extraction">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.validation.DataValidator</main-class>
            <arg>/data/raw/api/${processDate}</arg>
            <arg>api</arg>
            <capture-output/>
        </java>
        <ok to="join-extraction"/>
        <error to="handle-validation-error"/>
    </action>
    
    <!-- File data extraction -->
    <action name="extract-file-data">
        <fs>
            <move source="/data/incoming/${processDate}" target="/data/raw/files/${processDate}"/>
        </fs>
        <ok to="validate-file-extraction"/>
        <error to="handle-file-error"/>
    </action>
    
    <action name="validate-file-extraction">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.validation.DataValidator</main-class>
            <arg>/data/raw/files/${processDate}</arg>
            <arg>files</arg>
            <capture-output/>
        </java>
        <ok to="join-extraction"/>
        <error to="handle-validation-error"/>
    </action>
    
    <!-- Streaming data extraction -->
    <action name="extract-streaming-data">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>StreamingExtractor</name>
            <class>com.company.extractors.StreamingExtractor</class>
            <jar>/user/oozie/lib/streaming-extractor.jar</jar>
            <arg>${kafkaBrokers}</arg>
            <arg>${kafkaTopic}</arg>
            <arg>/data/raw/streaming/${processDate}</arg>
            <arg>${processDate}</arg>
        </spark>
        <ok to="validate-streaming-extraction"/>
        <error to="handle-streaming-error"/>
    </action>
    
    <action name="validate-streaming-extraction">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.validation.DataValidator</main-class>
            <arg>/data/raw/streaming/${processDate}</arg>
            <arg>streaming</arg>
            <capture-output/>
        </java>
        <ok to="join-extraction"/>
        <error to="handle-validation-error"/>
    </action>
    
    <!-- Join extraction results -->
    <join name="join-extraction" to="data-quality-check"/>
    
    <!-- Data quality assessment -->
    <action name="data-quality-check">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-name>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>DataQualityChecker</name>
            <class>com.company.quality.DataQualityChecker</class>
            <jar>/user/oozie/lib/data-quality.jar</jar>
            <arg>/data/raw/database/${processDate}</arg>
            <arg>/data/raw/api/${processDate}</arg>
            <arg>/data/raw/files/${processDate}</arg>
            <arg>/data/raw/streaming/${processDate}</arg>
            <arg>/data/quality-report/${processDate}</arg>
        </spark>
        <ok to="decide-processing-strategy"/>
        <error to="fail"/>
    </action>
    
    <!-- Decide processing strategy based on data quality -->
    <decision name="decide-processing-strategy">
        <switch>
            <case to="full-processing">
                ${wf:actionData('data-quality-check')['overallQuality'] ge 0.95}
            </case>
            <case to="partial-processing">
                ${wf:actionData('data-quality-check')['overallQuality'] ge 0.80}
            </case>
            <default to="quality-remediation"/>
        </switch>
    </decision>
    
    <!-- Full processing path -->
    <action name="full-processing">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-name>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>FullETLProcessor</name>
            <class>com.company.etl.FullETLProcessor</class>
            <jar>/user/oozie/lib/etl-processor.jar</jar>
            <arg>/data/raw/database/${processDate}</arg>
            <arg>/data/raw/api/${processDate}</arg>
            <arg>/data/raw/files/${processDate}</arg>
            <arg>/data/raw/streaming/${processDate}</arg>
            <arg>/data/processed/${processDate}</arg>
        </spark>
        <ok to="data-validation"/>
        <error to="fail"/>
    </action>
    
    <!-- Error handling actions -->
    <action name="handle-database-error">
        <email xmlns="uri:oozie:email-action:0.2">
            <to>data-team@company.com</to>
            <subject>Database Extraction Failed - ${processDate}</subject>
            <body>Database extraction failed for date ${processDate}. Please check database connectivity and data availability.</body>
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

### Q37: How would you handle a scenario where Oozie workflows need to process data across multiple time zones?
**Answer:**
**Multi-timezone Processing Solution:**

**1. Timezone-aware Coordinator:**
```xml
<coordinator-app name="global-timezone-coordinator" 
                 frequency="${coord:hours(1)}" 
                 start="2024-01-01T00:00Z" 
                 end="2024-12-31T23:59Z" 
                 timezone="UTC">
    
    <parameters>
        <property>
            <name>regions</name>
            <value>us-east,us-west,europe,asia</value>
        </property>
    </parameters>
    
    <datasets>
        <!-- US East Coast data (EST/EDT) -->
        <dataset name="us-east-data" frequency="${coord:hours(1)}" 
                 initial-instance="2024-01-01T05:00Z" timezone="America/New_York">
            <uri-template>/data/regions/us-east/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_COMPLETE</done-flag>
        </dataset>
        
        <!-- US West Coast data (PST/PDT) -->
        <dataset name="us-west-data" frequency="${coord:hours(1)}" 
                 initial-instance="2024-01-01T08:00Z" timezone="America/Los_Angeles">
            <uri-template>/data/regions/us-west/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_COMPLETE</done-flag>
        </dataset>
        
        <!-- European data (CET/CEST) -->
        <dataset name="europe-data" frequency="${coord:hours(1)}" 
                 initial-instance="2024-01-01T01:00Z" timezone="Europe/London">
            <uri-template>/data/regions/europe/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_COMPLETE</done-flag>
        </dataset>
        
        <!-- Asian data (JST) -->
        <dataset name="asia-data" frequency="${coord:hours(1)}" 
                 initial-instance="2024-01-01T09:00Z" timezone="Asia/Tokyo">
            <uri-template>/data/regions/asia/${YEAR}/${MONTH}/${DAY}/${HOUR}</uri-template>
            <done-flag>_COMPLETE</done-flag>
        </dataset>
    </datasets>
    
    <input-events>
        <!-- Wait for business hours data from each region -->
        <data-in name="us-east-business" dataset="us-east-data">
            <start-instance>${coord:current(-8)}</start-instance>
            <end-instance>${coord:current(0)}</end-instance>
        </data-in>
        
        <data-in name="us-west-business" dataset="us-west-data">
            <start-instance>${coord:current(-8)}</start-instance>
            <end-instance>${coord:current(0)}</end-instance>
        </data-in>
        
        <data-in name="europe-business" dataset="europe-data">
            <start-instance>${coord:current(-8)}</start-instance>
            <end-instance>${coord:current(0)}</end-instance>
        </data-in>
        
        <data-in name="asia-business" dataset="asia-data">
            <start-instance>${coord:current(-8)}</start-instance>
            <end-instance>${coord:current(0)}</end-instance>
        </data-in>
    </input-events>
    
    <action>
        <workflow>
            <app-path>/user/oozie/workflows/timezone-processor</app-path>
            <configuration>
                <property>
                    <name>usEastData</name>
                    <value>${coord:dataIn('us-east-business')}</value>
                </property>
                <property>
                    <name>usWestData</name>
                    <value>${coord:dataIn('us-west-business')}</value>
                </property>
                <property>
                    <name>europeData</name>
                    <value>${coord:dataIn('europe-business')}</value>
                </property>
                <property>
                    <name>asiaData</name>
                    <value>${coord:dataIn('asia-business')}</value>
                </property>
                <property>
                    <name>processingTimeUTC</name>
                    <value>${coord:formatTime(coord:nominalTime(), 'yyyy-MM-dd HH:mm:ss')}</value>
                </property>
            </configuration>
        </workflow>
    </action>
</coordinator-app>
```

**2. Timezone Processing Workflow:**
```xml
<workflow-app name="timezone-processor" xmlns="uri:oozie:workflow:0.5">
    <start to="timezone-normalization"/>
    
    <action name="timezone-normalization">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-name>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>TimezoneNormalizer</name>
            <class>com.company.timezone.TimezoneNormalizer</class>
            <jar>/user/oozie/lib/timezone-processor.jar</jar>
            <arg>${usEastData}</arg>
            <arg>${usWestData}</arg>
            <arg>${europeData}</arg>
            <arg>${asiaData}</arg>
            <arg>${outputPath}</arg>
            <arg>${processingTimeUTC}</arg>
        </spark>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Timezone processing failed</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**3. Timezone Processing Implementation:**
```java
public class TimezoneNormalizer {
    public static void main(String[] args) throws Exception {
        String usEastData = args[0];
        String usWestData = args[1];
        String europeData = args[2];
        String asiaData = args[3];
        String outputPath = args[4];
        String processingTimeUTC = args[5];
        
        SparkSession spark = SparkSession.builder()
            .appName("TimezoneNormalizer")
            .getOrCreate();
        
        // Define timezone mappings
        Map<String, String> timezoneMap = new HashMap<>();
        timezoneMap.put("us-east", "America/New_York");
        timezoneMap.put("us-west", "America/Los_Angeles");
        timezoneMap.put("europe", "Europe/London");
        timezoneMap.put("asia", "Asia/Tokyo");
        
        // Process each region's data
        Dataset<Row> normalizedData = null;
        
        String[] dataPaths = {usEastData, usWestData, europeData, asiaData};
        String[] regions = {"us-east", "us-west", "europe", "asia"};
        
        for (int i = 0; i < dataPaths.length; i++) {
            if (dataPaths[i] != null && !dataPaths[i].isEmpty()) {
                Dataset<Row> regionData = spark.read()
                    .option("header", "true")
                    .csv(dataPaths[i]);
                
                // Add region and normalize timestamps
                Dataset<Row> processedRegion = regionData
                    .withColumn("region", lit(regions[i]))
                    .withColumn("source_timezone", lit(timezoneMap.get(regions[i])))
                    .withColumn("timestamp_utc", 
                        from_utc_timestamp(
                            to_utc_timestamp(col("timestamp"), timezoneMap.get(regions[i])),
                            "UTC"
                        )
                    )
                    .withColumn("processing_time_utc", lit(processingTimeUTC));
                
                if (normalizedData == null) {
                    normalizedData = processedRegion;
                } else {
                    normalizedData = normalizedData.union(processedRegion);
                }
            }
        }
        
        // Write normalized data
        if (normalizedData != null) {
            normalizedData
                .coalesce(1)
                .write()
                .mode("overwrite")
                .option("header", "true")
                .csv(outputPath);
        }
        
        spark.stop();
    }
}
```

### Q38: Design a disaster recovery strategy for a critical Oozie-based data pipeline
**Answer:**
**Comprehensive Disaster Recovery Strategy:**

**1. Multi-site Replication Setup:**
```bash
#!/bin/bash
# Disaster Recovery Setup Script

PRIMARY_SITE="datacenter-east"
DR_SITE="datacenter-west"
REPLICATION_INTERVAL="15m"

# Setup cross-site replication
setup_cross_site_replication() {
    echo "Setting up cross-site replication..."
    
    # Database replication (MySQL Master-Slave)
    setup_database_replication
    
    # HDFS replication
    setup_hdfs_replication
    
    # Oozie configuration replication
    setup_config_replication
}

setup_database_replication() {
    # Configure MySQL replication
    cat > /etc/mysql/conf.d/replication.cnf << EOF
[mysqld]
server-id = 1
log-bin = mysql-bin
binlog-do-db = oozie
binlog-format = ROW
EOF
    
    # Create replication user
    mysql -u root -p << EOF
CREATE USER 'replication'@'%' IDENTIFIED BY 'replication_password';
GRANT REPLICATION SLAVE ON *.* TO 'replication'@'%';
FLUSH PRIVILEGES;
EOF
    
    # Setup slave on DR site
    ssh "$DR_SITE" << 'EOF'
mysql -u root -p << EOSQL
CHANGE MASTER TO
    MASTER_HOST='datacenter-east-db',
    MASTER_USER='replication',
    MASTER_PASSWORD='replication_password',
    MASTER_LOG_FILE='mysql-bin.000001',
    MASTER_LOG_POS=0;
START SLAVE;
EOSQL
EOF
}

setup_hdfs_replication() {
    # Setup DistCp for HDFS replication
    cat > /etc/cron.d/hdfs-replication << EOF
# HDFS replication every 15 minutes
*/15 * * * * hdfs hadoop distcp -update -delete hdfs://primary-cluster/user/oozie hdfs://dr-cluster/user/oozie
*/15 * * * * hdfs hadoop distcp -update -delete hdfs://primary-cluster/data hdfs://dr-cluster/data
EOF
}

# Failover procedure
failover_to_dr() {
    echo "Initiating failover to DR site..."
    
    # Stop primary site services
    stop_primary_services
    
    # Promote DR database to master
    promote_dr_database
    
    # Update DNS/Load balancer
    update_dns_records
    
    # Start DR site services
    start_dr_services
    
    # Verify failover
    verify_failover
}

stop_primary_services() {
    ssh "$PRIMARY_SITE" << 'EOF'
systemctl stop oozie
systemctl stop hadoop-yarn-resourcemanager
systemctl stop hadoop-hdfs-namenode
EOF
}

promote_dr_database() {
    ssh "$DR_SITE" << 'EOF'
mysql -u root -p << EOSQL
STOP SLAVE;
RESET SLAVE ALL;
EOSQL

# Update Oozie configuration to point to local database
sed -i 's/primary-db-server/localhost/g' /opt/oozie/conf/oozie-site.xml
EOF
}

start_dr_services() {
    ssh "$DR_SITE" << 'EOF'
systemctl start hadoop-hdfs-namenode
systemctl start hadoop-yarn-resourcemanager
systemctl start oozie

# Wait for services to be ready
sleep 60

# Verify services
curl -f http://localhost:11000/oozie/v1/admin/status
EOF
}
```

**2. Automated Failback Procedure:**
```bash
#!/bin/bash
# Automated Failback Script

failback_to_primary() {
    echo "Starting failback to primary site..."
    
    # Sync data from DR to primary
    sync_data_to_primary
    
    # Stop DR services
    stop_dr_services
    
    # Start primary services
    start_primary_services
    
    # Restore replication
    restore_replication
    
    # Update DNS back to primary
    update_dns_to_primary
    
    # Verify failback
    verify_primary_operations
}

sync_data_to_primary() {
    echo "Syncing data from DR to primary..."
    
    # Database sync
    ssh "$DR_SITE" << 'EOF'
mysqldump -u root -p --single-transaction --routines --triggers oozie > /tmp/oozie_failback.sql
scp /tmp/oozie_failback.sql primary-site:/tmp/
EOF
    
    ssh "$PRIMARY_SITE" << 'EOF'
mysql -u root -p oozie < /tmp/oozie_failback.sql
EOF
    
    # HDFS sync
    hadoop distcp -update -delete hdfs://dr-cluster/user/oozie hdfs://primary-cluster/user/oozie
    hadoop distcp -update -delete hdfs://dr-cluster/data hdfs://primary-cluster/data
}
```

### Q39: How would you optimize an Oozie workflow that processes 100TB of data daily?
**Answer:**
**Large-scale Data Processing Optimization:**

**1. Optimized Workflow Architecture:**
```xml
<workflow-app name="large-scale-processing" xmlns="uri:oozie:workflow:0.5">
    <global>
        <job-tracker>${jobTracker}</job-tracker>
        <name-node>${nameNode}</name-node>
        <configuration>
            <!-- Optimize for large datasets -->
            <property>
                <name>mapreduce.job.reduces</name>
                <value>1000</value>
            </property>
            <property>
                <name>mapreduce.input.fileinputformat.split.maxsize</name>
                <value>268435456</value> <!-- 256MB -->
            </property>
            <property>
                <name>mapreduce.map.memory.mb</name>
                <value>4096</value>
            </property>
            <property>
                <name>mapreduce.reduce.memory.mb</name>
                <value>8192</value>
            </property>
        </configuration>
    </global>
    
    <start to="data-partitioning"/>
    
    <!-- Intelligent data partitioning -->
    <action name="data-partitioning">
        <java>
            <main-class>com.company.optimization.DataPartitioner</main-class>
            <arg>${inputPath}</arg>
            <arg>${partitionedPath}</arg>
            <arg>100</arg> <!-- Number of partitions -->
            <capture-output/>
        </java>
        <ok to="parallel-processing"/>
        <error to="fail"/>
    </action>
    
    <!-- Massive parallel processing -->
    <fork name="parallel-processing">
        <path start="process-partition-batch-1"/>
        <path start="process-partition-batch-2"/>
        <path start="process-partition-batch-3"/>
        <path start="process-partition-batch-4"/>
        <path start="process-partition-batch-5"/>
    </fork>
    
    <!-- Each batch processes 20 partitions -->
    <action name="process-partition-batch-1">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <master>yarn</master>
            <mode>cluster</mode>
            <name>LargeScaleProcessor-Batch1</name>
            <class>com.company.processing.OptimizedProcessor</class>
            <jar>/user/oozie/lib/optimized-processor.jar</jar>
            <spark-opts>
                --executor-memory 16g
                --executor-cores 8
                --num-executors 50
                --driver-memory 8g
                --conf spark.sql.adaptive.enabled=true
                --conf spark.sql.adaptive.coalescePartitions.enabled=true
                --conf spark.sql.adaptive.skewJoin.enabled=true
                --conf spark.serializer=org.apache.spark.serializer.KryoSerializer
                --conf spark.sql.execution.arrow.pyspark.enabled=true
            </spark-opts>
            <arg>${partitionedPath}/batch-1</arg>
            <arg>${outputPath}/batch-1</arg>
            <arg>1</arg>
            <arg>20</arg>
        </spark>
        <ok to="join-processing"/>
        <error to="fail"/>
    </action>
    
    <join name="join-processing" to="data-consolidation"/>
    
    <!-- Efficient data consolidation -->
    <action name="data-consolidation">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <master>yarn</master>
            <mode>cluster</mode>
            <name>DataConsolidator</name>
            <class>com.company.processing.DataConsolidator</class>
            <jar>/user/oozie/lib/consolidator.jar</jar>
            <spark-opts>
                --executor-memory 32g
                --executor-cores 16
                --num-executors 20
                --driver-memory 16g
                --conf spark.sql.adaptive.enabled=true
                --conf spark.sql.adaptive.coalescePartitions.enabled=true
            </spark-opts>
            <arg>${outputPath}/batch-*</arg>
            <arg>${finalOutputPath}</arg>
        </spark>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    
    <kill name="fail">
        <message>Large-scale processing failed</message>
    </kill>
    
    <end name="end"/>
</workflow-app>
```

**2. Performance Optimization Implementation:**
```java
public class OptimizedProcessor {
    public static void main(String[] args) throws Exception {
        String inputPath = args[0];
        String outputPath = args[1];
        int batchId = Integer.parseInt(args[2]);
        int partitionCount = Integer.parseInt(args[3]);
        
        SparkSession spark = SparkSession.builder()
            .appName("OptimizedProcessor-Batch" + batchId)
            .config("spark.sql.adaptive.enabled", "true")
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
            .config("spark.sql.adaptive.skewJoin.enabled", "true")
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate();
        
        // Read data with optimized partitioning
        Dataset<Row> data = spark.read()
            .option("multiline", "false")
            .option("inferSchema", "false")
            .schema(getOptimizedSchema())
            .parquet(inputPath);
        
        // Optimize partitioning for processing
        data = data.repartition(partitionCount, col("partition_key"));
        
        // Cache frequently accessed data
        data.cache();
        
        // Perform optimized transformations
        Dataset<Row> processed = data
            .filter(col("status").equalTo("active"))
            .groupBy("category", "region")
            .agg(
                sum("amount").alias("total_amount"),
                count("*").alias("record_count"),
                avg("amount").alias("avg_amount"),
                max("timestamp").alias("latest_timestamp")
            )
            .withColumn("processing_batch", lit(batchId))
            .withColumn("processing_time", current_timestamp());
        
        // Write with optimal partitioning
        processed
            .repartition(col("region"))
            .write()
            .mode("overwrite")
            .partitionBy("region", "category")
            .option("compression", "snappy")
            .parquet(outputPath);
        
        // Cleanup
        data.unpersist();
        spark.stop();
    }
    
    private static StructType getOptimizedSchema() {
        return new StructType(new StructField[]{
            new StructField("id", DataTypes.LongType, false, Metadata.empty()),
            new StructField("category", DataTypes.StringType, false, Metadata.empty()),
            new StructField("region", DataTypes.StringType, false, Metadata.empty()),
            new StructField("amount", DataTypes.DoubleType, false, Metadata.empty()),
            new StructField("status", DataTypes.StringType, false, Metadata.empty()),
            new StructField("timestamp", DataTypes.TimestampType, false, Metadata.empty()),
            new StructField("partition_key", DataTypes.StringType, false, Metadata.empty())
        });
    }
}
```

### Q40: How would you implement a real-time alerting system for Oozie workflow failures?
**Answer:**
**Real-time Alerting System:**

**1. Webhook-based Alert System:**
```java
public class OozieAlertSystem {
    private static final String SLACK_WEBHOOK = System.getenv("SLACK_WEBHOOK_URL");
    private static final String PAGERDUTY_API = System.getenv("PAGERDUTY_API_URL");
    
    public static void main(String[] args) throws Exception {
        String workflowId = args[0];
        String workflowName = args[1];
        String errorMessage = args[2];
        String severity = args[3]; // CRITICAL, WARNING, INFO
        
        AlertContext context = new AlertContext(workflowId, workflowName, errorMessage, severity);
        
        // Send alerts based on severity
        switch (severity.toUpperCase()) {
            case "CRITICAL":
                sendPagerDutyAlert(context);
                sendSlackAlert(context);
                sendEmailAlert(context);
                break;
            case "WARNING":
                sendSlackAlert(context);
                sendEmailAlert(context);
                break;
            case "INFO":
                sendSlackAlert(context);
                break;
        }
        
        // Log to centralized logging system
        logToElasticsearch(context);
    }
    
    private static void sendSlackAlert(AlertContext context) {
        try {
            String payload = createSlackPayload(context);
            
            HttpClient client = HttpClients.createDefault();
            HttpPost post = new HttpPost(SLACK_WEBHOOK);
            post.setEntity(new StringEntity(payload, ContentType.APPLICATION_JSON));
            
            HttpResponse response = client.execute(post);
            System.out.println("Slack alert sent: " + response.getStatusLine().getStatusCode());
            
        } catch (Exception e) {
            System.err.println("Failed to send Slack alert: " + e.getMessage());
        }
    }
    
    private static String createSlackPayload(AlertContext context) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("channel", "#data-alerts");
        payload.put("username", "Oozie Alert Bot");
        payload.put("icon_emoji", ":warning:");
        
        String color = context.getSeverity().equals("CRITICAL") ? "danger" : "warning";
        String text = String.format("*Oozie Workflow Alert*\n" +
            "Severity: %s\n" +
            "Workflow: %s (%s)\n" +
            "Error: %s\n" +
            "Time: %s",
            context.getSeverity(),
            context.getWorkflowName(),
            context.getWorkflowId(),
            context.getErrorMessage(),
            Instant.now().toString()
        );
        
        Map<String, Object> attachment = new HashMap<>();
        attachment.put("color", color);
        attachment.put("text", text);
        attachment.put("mrkdwn_in", Arrays.asList("text"));
        
        payload.put("attachments", Arrays.asList(attachment));
        
        ObjectMapper mapper = new ObjectMapper();
        try {
            return mapper.writeValueAsString(payload);
        } catch (Exception e) {
            return "{}";
        }
    }
    
    private static void sendPagerDutyAlert(AlertContext context) {
        try {
            Map<String, Object> event = new HashMap<>();
            event.put("routing_key", System.getenv("PAGERDUTY_ROUTING_KEY"));
            event.put("event_action", "trigger");
            event.put("dedup_key", context.getWorkflowId());
            
            Map<String, Object> payload = new HashMap<>();
            payload.put("summary", "Oozie Workflow Failure: " + context.getWorkflowName());
            payload.put("severity", "critical");
            payload.put("source", "oozie-cluster");
            payload.put("component", "workflow-engine");
            payload.put("group", "data-platform");
            payload.put("class", "workflow-failure");
            
            Map<String, Object> customDetails = new HashMap<>();
            customDetails.put("workflow_id", context.getWorkflowId());
            customDetails.put("workflow_name", context.getWorkflowName());
            customDetails.put("error_message", context.getErrorMessage());
            customDetails.put("timestamp", Instant.now().toString());
            
            payload.put("custom_details", customDetails);
            event.put("payload", payload);
            
            ObjectMapper mapper = new ObjectMapper();
            String jsonPayload = mapper.writeValueAsString(event);
            
            HttpClient client = HttpClients.createDefault();
            HttpPost post = new HttpPost(PAGERDUTY_API);
            post.setEntity(new StringEntity(jsonPayload, ContentType.APPLICATION_JSON));
            
            HttpResponse response = client.execute(post);
            System.out.println("PagerDuty alert sent: " + response.getStatusLine().getStatusCode());
            
        } catch (Exception e) {
            System.err.println("Failed to send PagerDuty alert: " + e.getMessage());
        }
    }
}
```

**2. Workflow Integration:**
```xml
<workflow-app name="alert-enabled-workflow" xmlns="uri:oozie:workflow:0.5">
    <start to="main-processing"/>
    
    <action name="main-processing">
        <spark xmlns="uri:oozie:spark-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-name>
            <master>yarn</master>
            <mode>cluster</mode>
            <name>MainProcessing</name>
            <class>com.company.MainProcessor</class>
            <jar>/user/oozie/lib/processor.jar</jar>
            <arg>${inputPath}</arg>
            <arg>${outputPath}</arg>
        </spark>
        <ok to="success-notification"/>
        <error to="failure-alert"/>
    </action>
    
    <action name="success-notification">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.alerts.OozieAlertSystem</main-class>
            <arg>${wf:id()}</arg>
            <arg>${wf:name()}</arg>
            <arg>Workflow completed successfully</arg>
            <arg>INFO</arg>
        </java>
        <ok to="end"/>
        <error to="end"/>
    </action>
    
    <action name="failure-alert">
        <java>
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <main-class>com.company.alerts.OozieAlertSystem</main-class>
            <arg>${wf:id()}</arg>
            <arg>${wf:name()}</arg>
            <arg>${wf:errorMessage(wf:lastErrorNode())}</arg>
            <arg>CRITICAL</arg>
        </java>
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

**🎯 Summary**

This comprehensive Apache Oozie interview questions collection covers:

- **Basic Level (Q1-Q10)**: Core concepts, architecture, job types, and basic operations
- **Intermediate Level (Q11-Q20)**: Complex dependencies, EL functions, parallel processing, and advanced features
- **Advanced Level (Q21-Q25)**: Custom extensions, workflow patterns, error handling, and versioning
- **Architecture & Performance (Q26-Q30)**: Optimization, high availability, monitoring, security, and disaster recovery
- **Streaming & Real-time (Q31-Q33)**: Near real-time processing, Kafka integration, and backpressure handling
- **Production & Operations (Q34-Q35)**: Logging, monitoring, and automated testing
- **Scenario-Based (Q36-Q40)**: Complex ETL pipelines, multi-timezone processing, disaster recovery, large-scale optimization, and real-time alerting

Each question includes detailed answers with practical code examples, configuration snippets, and real-world implementation strategies suitable for data engineering interviews.