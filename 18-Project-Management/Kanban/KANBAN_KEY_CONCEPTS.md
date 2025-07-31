# Kanban Key Concepts

## 1. Visual Workflow Management System
**What it is**: Lean method for managing and improving work across human systems, emphasizing continuous delivery and workflow optimization.

**Core Principles**:
- **Visualize work**: Make work and workflow visible
- **Limit WIP**: Constrain work in progress
- **Manage flow**: Focus on smooth work flow
- **Make policies explicit**: Define and communicate rules
- **Implement feedback loops**: Regular review and improvement
- **Improve collaboratively**: Evolve experimentally

## 2. Kanban Board Structure
**Basic Board Layout**:
```yaml
# Simple 3-Column Board
To Do | In Progress | Done

# Extended Board
Backlog | Ready | In Progress | Review | Testing | Done

# Data Engineering Board
Ideas | Backlog | Analysis | Development | Testing | Deployment | Done
```

**Column Definitions**:
```yaml
# Backlog
Purpose: Store prioritized work items
WIP Limit: None (or high limit)
Entry Criteria: Item is defined and prioritized
Exit Criteria: Item is ready to start

# In Progress  
Purpose: Active development work
WIP Limit: 3-5 items per person
Entry Criteria: Developer available, dependencies met
Exit Criteria: Development complete, ready for review

# Done
Purpose: Completed work
WIP Limit: None
Entry Criteria: All acceptance criteria met
Exit Criteria: Item deployed to production
```

## 3. Work Item Types
**Card Types**:
```yaml
# Feature Cards
- New functionality
- User stories
- Enhancements

# Bug Cards
- Defects
- Issues
- Fixes

# Technical Cards
- Refactoring
- Infrastructure
- Technical debt

# Expedite Cards
- Urgent items
- Production issues
- Critical fixes
```

**Card Information**:
```yaml
# Essential Fields
- Title/Summary
- Description
- Assignee
- Priority
- Due date
- Blocked status

# Additional Fields
- Story points/Size
- Business value
- Dependencies
- Tags/Labels
```

## 4. Work in Progress (WIP) Limits
**Setting WIP Limits**:
```yaml
# Guidelines
- Start with team size + 1
- Adjust based on flow metrics
- Different limits per column
- Consider skill specialization

# Example Limits
Backlog: No limit
Ready: 10 items
In Progress: 6 items (team of 5)
Review: 4 items
Testing: 3 items
Done: No limit
```

**WIP Limit Benefits**:
```yaml
# Improved Flow
- Reduces context switching
- Identifies bottlenecks
- Encourages collaboration
- Improves quality

# Team Benefits
- Better focus
- Reduced stress
- Faster delivery
- Continuous improvement
```

## 5. Flow Metrics
**Lead Time**:
```yaml
Definition: Time from request to delivery
Measurement: From backlog entry to done
Usage: Customer satisfaction, planning
Target: Minimize and stabilize

Calculation:
Lead Time = Done Date - Request Date
```

**Cycle Time**:
```yaml
Definition: Time from start to completion
Measurement: From "In Progress" to "Done"
Usage: Team performance, capacity planning
Target: Minimize and predict

Calculation:
Cycle Time = Done Date - Start Date
```

**Throughput**:
```yaml
Definition: Number of items completed per time period
Measurement: Items moved to "Done" per week/month
Usage: Capacity planning, forecasting
Target: Maximize sustainable rate

Example:
Week 1: 8 items completed
Week 2: 6 items completed
Week 3: 10 items completed
Average Throughput: 8 items/week
```

## 6. Cumulative Flow Diagram (CFD)
**CFD Components**:
```yaml
# Axes
X-axis: Time (days/weeks)
Y-axis: Number of work items

# Colored Bands
Each column represented by colored band
Band width = number of items in that column
Band height changes = flow rate

# Key Insights
- Bottlenecks (widening bands)
- Flow stability (parallel bands)
- WIP trends (total height)
```

**CFD Analysis**:
```yaml
# Healthy Flow
- Parallel bands
- Consistent throughput
- Stable WIP levels
- Smooth delivery

# Problem Indicators
- Widening bands (bottlenecks)
- Flat bands (no progress)
- Increasing total height (growing WIP)
- Irregular patterns (unstable flow)
```

## 7. Classes of Service
**Service Classes**:
```yaml
# Expedite
- Highest priority
- No WIP limit
- Immediate attention
- Example: Production outages

# Fixed Date
- Specific deadline
- Scheduled work
- Example: Compliance requirements

# Standard
- Normal priority
- Regular flow
- Example: Feature development

# Intangible
- Low priority
- Fill spare capacity
- Example: Technical debt, learning
```

**Service Level Agreements**:
```yaml
# Expedite Items
Target Lead Time: 24 hours
Success Rate: 95%
WIP Limit: 1 item

# Standard Items  
Target Lead Time: 2 weeks
Success Rate: 85%
WIP Limit: Normal limits apply

# Intangible Items
Target Lead Time: No commitment
Success Rate: Best effort
WIP Limit: Fill available capacity
```

## 8. Kanban Cadences
**Daily Standup**:
```yaml
Focus: Flow and blockers
Questions:
- What's blocked?
- What's aging?
- Where can we help?
- Are WIP limits respected?

Duration: 15 minutes
Frequency: Daily
```

**Replenishment Meeting**:
```yaml
Purpose: Select new work for board
Participants: Product owner, team leads
Frequency: Weekly or bi-weekly
Agenda:
- Review capacity
- Prioritize backlog
- Pull new items
- Update forecasts
```

**Service Delivery Review**:
```yaml
Purpose: Review delivery performance
Participants: Team and stakeholders
Frequency: Monthly
Metrics:
- Throughput trends
- Lead time distribution
- Quality metrics
- Customer satisfaction
```

**Operations Review**:
```yaml
Purpose: Improve workflow
Participants: Team members
Frequency: Monthly or quarterly
Topics:
- Flow efficiency
- Bottleneck analysis
- Policy updates
- Process improvements
```

## 9. Digital Kanban Tools
**Tool Features**:
```yaml
# Essential Features
- Visual board interface
- WIP limit enforcement
- Card filtering/searching
- Basic reporting
- Team collaboration

# Advanced Features
- Cumulative flow diagrams
- Lead time tracking
- Automated workflows
- Integration capabilities
- Custom fields
```

**Popular Tools**:
```yaml
# Jira Kanban
- Robust reporting
- Agile metrics
- Enterprise features
- Atlassian ecosystem

# Trello
- Simple interface
- Easy to use
- Good for small teams
- Limited reporting

# Azure DevOps
- Microsoft ecosystem
- Built-in analytics
- Enterprise security
- DevOps integration
```

## 10. Kanban vs Scrum
**Key Differences**:
```yaml
# Kanban
- Continuous flow
- No fixed iterations
- Pull-based system
- Change anytime
- Focus on flow efficiency

# Scrum
- Sprint-based iterations
- Time-boxed events
- Push-based planning
- Change between sprints
- Focus on team velocity
```

**When to Use Kanban**:
```yaml
# Good Fit
- Continuous delivery
- Unpredictable work
- Support/maintenance
- Operational work
- Mature teams

# Considerations
- Requires discipline
- Less structure
- Continuous improvement focus
- Flow-based metrics
```

## 11. Implementation Best Practices
**Getting Started**:
```yaml
# Step 1: Map Current Workflow
- Identify work stages
- Define column purposes
- Set initial WIP limits
- Create board layout

# Step 2: Start Simple
- Basic 3-column board
- Conservative WIP limits
- Essential card information
- Regular team check-ins

# Step 3: Measure and Improve
- Track flow metrics
- Identify bottlenecks
- Adjust WIP limits
- Refine policies
```

**Common Pitfalls**:
```yaml
# No WIP Limits
Problem: Board becomes status tracker
Solution: Implement and enforce limits

# Ignoring Blockers
Problem: Items stuck without resolution
Solution: Daily blocker review and escalation

# No Continuous Improvement
Problem: Process stagnation
Solution: Regular retrospectives and experiments

# Over-Engineering
Problem: Complex board with too many columns
Solution: Start simple, evolve gradually
```

## 12. Advanced Concepts
**Portfolio Kanban**:
```yaml
# Strategic Level
- Epics and initiatives
- Investment decisions
- Resource allocation
- Value stream mapping

# Multi-Level Boards
- Portfolio board (epics)
- Team boards (stories)
- Operational boards (tasks)
```

**Kanban Maturity Model**:
```yaml
# Level 0: Ad-hoc
- No systematic approach
- Reactive work management

# Level 1: Emerging
- Basic visualization
- Some WIP limits
- Regular meetings

# Level 2: Defined
- Clear policies
- Consistent metrics
- Improvement culture

# Level 3: Managed
- Predictable delivery
- Data-driven decisions
- Optimized flow

# Level 4: Optimizing
- Continuous evolution
- Innovation focus
- Strategic alignment
```