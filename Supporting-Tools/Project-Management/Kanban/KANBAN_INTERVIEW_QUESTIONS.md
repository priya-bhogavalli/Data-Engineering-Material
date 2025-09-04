# Kanban Interview Questions & Answers

## 📋 Table of Contents
1. [Basic Concepts](#basic-concepts)
2. [Kanban Board Design](#kanban-board-design)
3. [Work in Progress Limits](#work-in-progress-limits)
4. [Metrics and Flow](#metrics-and-flow)
5. [Implementation](#implementation)

---

## Basic Concepts

### 1. What is Kanban and how does it benefit data engineering workflows?

**Answer:**
Kanban is a visual workflow management method that helps teams visualize work, limit work-in-progress, and maximize efficiency.

**Core Principles:**
- **Visualize Work**: Make all work visible on a board
- **Limit WIP**: Constrain work in progress to improve flow
- **Manage Flow**: Monitor and optimize the flow of work
- **Make Policies Explicit**: Define and communicate process rules
- **Continuous Improvement**: Evolve through feedback and metrics

**Benefits for Data Engineering:**
```yaml
visibility:
  - Clear view of pipeline development status
  - Bottleneck identification
  - Resource allocation transparency

flow_optimization:
  - Reduced context switching
  - Faster delivery cycles
  - Improved throughput

flexibility:
  - Easy priority changes
  - No fixed sprint commitments
  - Continuous delivery capability
```

### 2. How does Kanban differ from Scrum for data engineering teams?

**Answer:**
Kanban and Scrum have different approaches to managing work and team structure.

**Key Differences:**
| Aspect | Kanban | Scrum |
|--------|--------|-------|
| **Timeboxing** | Continuous flow | Fixed sprints |
| **Roles** | No prescribed roles | 3 defined roles |
| **Planning** | On-demand | Sprint planning |
| **Commitment** | Flexible | Sprint commitment |
| **Changes** | Anytime | Between sprints |

**When to Use Kanban:**
- Maintenance and support work
- Continuous delivery environments
- Unpredictable work patterns
- Operational data engineering tasks

---

## Kanban Board Design

### 3. How do you design an effective Kanban board for data pipeline development?

**Answer:**
An effective Kanban board reflects the actual workflow and provides clear visibility into work status.

**Basic Board Structure:**
```
Backlog → Analysis → Development → Testing → Deployment → Done
```

**Data Engineering Board Example:**
```
| Backlog | Ready | In Progress | Code Review | Testing | Staging | Production | Done |
|---------|-------|-------------|-------------|---------|---------|------------|------|
| Story A | Story B | Story C   | Story D     | Story E | Story F | Story G    | Story H |
| Story I | Story J |           |             |         |         |            | Story K |
| Story L |         |           |             |         |         |            |        |
```

**Advanced Board with Swimlanes:**
```markdown
# Data Platform Kanban Board

## Swimlane: Data Pipelines
| Backlog | Analysis | Development | Review | Testing | Deploy | Done |
|---------|----------|-------------|--------|---------|--------|------|
| Pipeline A | Pipeline B | Pipeline C | | | Pipeline D | Pipeline E |

## Swimlane: Infrastructure
| Backlog | Planning | Implementation | Review | Testing | Deploy | Done |
|---------|----------|----------------|--------|---------|--------|------|
| Infra A | | Infra B | Infra C | | | Infra D |

## Swimlane: Bug Fixes
| Reported | Triaged | In Progress | Review | Testing | Deploy | Done |
|----------|---------|-------------|--------|---------|--------|------|
| Bug A | Bug B | Bug C | | | | Bug D |
```

### 4. What are the key elements of a well-designed Kanban card?

**Answer:**
Kanban cards should contain essential information for team members to understand and work on the item.

**Card Elements:**
```markdown
# Kanban Card Template

## Card ID: DE-123
## Title: Implement real-time customer event processing

### Description:
Build Kafka consumer to process customer events in real-time
and store processed data in data lake for analytics.

### Acceptance Criteria:
- [ ] Kafka consumer processes events with <1s latency
- [ ] Data validation rules applied
- [ ] Processed data stored in S3 partitioned by date
- [ ] Monitoring and alerting configured

### Metadata:
- **Assignee**: John Doe
- **Priority**: High
- **Size**: Large (8 points)
- **Type**: Feature
- **Due Date**: 2023-12-15
- **Dependencies**: Kafka cluster setup (DE-120)

### Labels:
#kafka #real-time #analytics #customer-data
```

**Visual Indicators:**
- Color coding by priority or type
- Blocked indicators (red flag)
- Age indicators (card aging)
- Class of service (expedite, standard, fixed date)

---

## Work in Progress Limits

### 5. How do you determine and implement WIP limits for data engineering workflows?

**Answer:**
WIP limits should be based on team capacity, workflow analysis, and continuous optimization.

**Determining WIP Limits:**
```yaml
team_analysis:
  team_size: 6 developers
  parallel_capacity: 4-5 items
  context_switching_cost: high
  
workflow_analysis:
  bottleneck_stage: code_review
  average_cycle_time: 5_days
  throughput: 8_items_per_week
  
initial_limits:
  analysis: 3
  development: 4
  code_review: 2
  testing: 3
  deployment: 2
```

**WIP Limit Implementation:**
```markdown
# Data Engineering Team WIP Limits

## Column Limits:
- **Backlog**: No limit (prioritized queue)
- **Analysis**: 2 items max
- **Development**: 4 items max
- **Code Review**: 2 items max
- **Testing**: 3 items max
- **Deployment**: 1 item max

## Rules:
1. Cannot pull new work if column at limit
2. Team swarms on blocked items
3. Review limits weekly in team meeting
4. Adjust based on flow metrics
```

### 6. What happens when WIP limits are exceeded and how do you handle it?

**Answer:**
WIP limit violations indicate process problems that need immediate attention.

**Common Causes:**
- Urgent work bypassing normal flow
- Bottlenecks in downstream processes
- Team members multitasking
- External dependencies blocking work

**Response Actions:**
```markdown
# WIP Limit Violation Response

## Immediate Actions:
1. **Stop pulling new work** into the column
2. **Identify root cause** of the violation
3. **Swarm on blocked items** to clear bottleneck
4. **Escalate dependencies** if needed

## Example Scenario:
**Situation**: Code Review column has 4 items (limit: 2)
**Root Cause**: Two reviewers on vacation
**Actions**:
- Temporarily increase review capacity
- Cross-train additional reviewers
- Consider pair programming for complex items
- Adjust WIP limits for vacation periods
```

---

## Metrics and Flow

### 7. What key metrics do you track in Kanban for data engineering teams?

**Answer:**
Kanban metrics focus on flow efficiency and predictability rather than velocity.

**Primary Metrics:**
```yaml
flow_metrics:
  lead_time:
    definition: "Time from request to delivery"
    target: "<10 days for standard features"
    measurement: "Entry to Done column"
  
  cycle_time:
    definition: "Time from start to finish"
    target: "<7 days for development work"
    measurement: "In Progress to Done"
  
  throughput:
    definition: "Items completed per time period"
    target: "8-10 items per week"
    measurement: "Items moved to Done"
  
  work_in_progress:
    definition: "Items currently being worked on"
    target: "Within WIP limits"
    measurement: "Items in active columns"
```

**Cumulative Flow Diagram:**
```
Items
  ^
  |     Done
  |   ████████
  |  ████████████  Deployment
  | ████████████████  Testing
  |████████████████████  Development
  |████████████████████████  Analysis
  |████████████████████████████  Backlog
  +--------------------------------> Time
```

### 8. How do you use flow metrics to improve data engineering processes?

**Answer:**
Flow metrics reveal bottlenecks and improvement opportunities in the development process.

**Metric Analysis:**
```markdown
# Flow Analysis Example

## Current State:
- **Lead Time**: 15 days (target: 10 days)
- **Cycle Time**: 12 days (target: 7 days)
- **Throughput**: 5 items/week (target: 8 items/week)

## Bottleneck Analysis:
1. **Code Review**: Average 4 days (should be 1 day)
2. **Testing**: Average 3 days (should be 2 days)
3. **Deployment**: Average 2 days (should be 0.5 days)

## Improvement Actions:
### Code Review Bottleneck:
- Add more reviewers to rotation
- Implement automated code quality checks
- Reduce review batch size
- Set review SLA (24 hours)

### Testing Bottleneck:
- Increase test automation coverage
- Parallel test execution
- Dedicated test environment per developer

### Deployment Bottleneck:
- Implement automated deployment pipeline
- Feature flags for safer releases
- Infrastructure as code
```

---

## Implementation

### 9. How do you transition a data engineering team from Scrum to Kanban?

**Answer:**
Transitioning requires gradual change management and team buy-in.

**Transition Plan:**
```yaml
phase_1_preparation:
  duration: 2_weeks
  activities:
    - Team education on Kanban principles
    - Current workflow mapping
    - Initial board design
    - WIP limit calculation

phase_2_pilot:
  duration: 4_weeks
  activities:
    - Start with current Scrum board
    - Add WIP limits gradually
    - Remove sprint boundaries
    - Focus on flow metrics

phase_3_optimization:
  duration: 4_weeks
  activities:
    - Refine board structure
    - Optimize WIP limits
    - Implement flow metrics
    - Continuous improvement
```

**Change Management:**
```markdown
# Team Transition Support

## Training:
- Kanban fundamentals workshop
- Flow metrics training
- Tool training (Jira, Azure DevOps)
- Continuous improvement practices

## Support:
- Daily coaching during transition
- Weekly retrospectives
- Metric tracking and analysis
- Regular process adjustments
```

### 10. How do you handle different types of work (features, bugs, maintenance) in Kanban?

**Answer:**
Different work types require different treatment while maintaining overall flow.

**Work Type Management:**
```markdown
# Multi-Class Service System

## Class of Service Definitions:

### Expedite (Red)
- **Examples**: Production outages, critical bugs
- **Policy**: Bypass WIP limits, immediate attention
- **SLA**: 4 hours response time
- **Capacity**: Max 1 item at a time

### Fixed Date (Orange)
- **Examples**: Compliance requirements, scheduled maintenance
- **Policy**: Plan backwards from due date
- **SLA**: Must meet deadline
- **Capacity**: 20% of team capacity

### Standard (Blue)
- **Examples**: New features, enhancements
- **Policy**: Normal flow, respect WIP limits
- **SLA**: 10 days lead time
- **Capacity**: 60% of team capacity

### Intangible (Green)
- **Examples**: Technical debt, research, training
- **Policy**: Fill gaps in workflow
- **SLA**: No specific SLA
- **Capacity**: 20% of team capacity
```

**Board Implementation:**
```
| Backlog | Ready | In Progress | Review | Testing | Deploy | Done |
|---------|-------|-------------|--------|---------|--------|------|
| 🔴 Bug A | 🔵 Feature B | 🟠 Compliance C | 🔵 Feature D | 🟢 Tech Debt E | 🔵 Feature F | 🔴 Bug G |
| 🔵 Feature H | 🟢 Research I | 🔵 Feature J | | | | 🔵 Feature K |
```

---

## Summary

Kanban provides continuous flow management for data engineering teams through:

1. **Visual Management**: Clear workflow visibility
2. **Flow Optimization**: WIP limits and bottleneck management  
3. **Metrics-Driven**: Lead time, cycle time, and throughput focus
4. **Flexibility**: Continuous delivery without fixed iterations
5. **Continuous Improvement**: Regular process optimization