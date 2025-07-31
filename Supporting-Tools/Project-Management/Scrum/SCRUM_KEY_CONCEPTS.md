# Scrum Key Concepts

## 1. Agile Framework for Product Development
**What it is**: Lightweight framework for developing, delivering, and sustaining complex products through iterative and incremental practices.

**Core Values**:
- **Individuals and interactions** over processes and tools
- **Working software** over comprehensive documentation
- **Customer collaboration** over contract negotiation
- **Responding to change** over following a plan

## 2. Scrum Roles
**Product Owner**:
```yaml
Responsibilities:
- Define product vision and strategy
- Manage product backlog
- Prioritize features and requirements
- Accept or reject work results
- Communicate with stakeholders

Key Activities:
- Write user stories
- Define acceptance criteria
- Participate in sprint planning
- Review sprint deliverables
```

**Scrum Master**:
```yaml
Responsibilities:
- Facilitate scrum events
- Remove impediments
- Coach team on scrum practices
- Protect team from distractions
- Ensure scrum process adherence

Key Activities:
- Daily standup facilitation
- Sprint retrospective guidance
- Impediment removal
- Process improvement
```

**Development Team**:
```yaml
Characteristics:
- Self-organizing and cross-functional
- 3-9 members optimal size
- Collectively responsible for deliverables
- No sub-teams or hierarchies

Responsibilities:
- Estimate user stories
- Commit to sprint goals
- Deliver potentially shippable increments
- Continuously improve processes
```

## 3. Scrum Events
**Sprint**:
```yaml
Duration: 1-4 weeks (typically 2 weeks)
Purpose: Time-boxed iteration to create working increment
Goal: Deliver potentially shippable product increment

Sprint Rules:
- No changes that endanger sprint goal
- Quality goals do not decrease
- Scope may be clarified with Product Owner
```

**Sprint Planning**:
```yaml
Duration: 8 hours for 4-week sprint (proportional for shorter)
Participants: Entire Scrum Team
Agenda:
  Part 1: What can be delivered? (Product Owner presents backlog)
  Part 2: How will work be achieved? (Team creates sprint backlog)

Outputs:
- Sprint goal
- Sprint backlog
- Team commitment
```

**Daily Scrum**:
```yaml
Duration: 15 minutes
Participants: Development Team (others may observe)
Format: Each team member answers:
  1. What did I do yesterday?
  2. What will I do today?
  3. Are there any impediments?

Purpose:
- Synchronize activities
- Plan next 24 hours
- Identify impediments
```

**Sprint Review**:
```yaml
Duration: 4 hours for 4-week sprint
Participants: Scrum Team + Stakeholders
Agenda:
- Demo completed work
- Discuss what went well/challenges
- Review product backlog
- Collaborate on next steps

Outcome:
- Feedback on increment
- Updated product backlog
- Input for next sprint planning
```

**Sprint Retrospective**:
```yaml
Duration: 3 hours for 4-week sprint
Participants: Scrum Team only
Format:
- What went well?
- What could be improved?
- What will we commit to improve?

Techniques:
- Start/Stop/Continue
- 4Ls (Liked/Learned/Lacked/Longed for)
- Sailboat (Wind/Anchors)
```

## 4. Scrum Artifacts
**Product Backlog**:
```yaml
Definition: Ordered list of features, functions, requirements
Characteristics:
- Single source of requirements
- Continuously refined and prioritized
- Estimated by development team
- Owned by Product Owner

User Story Format:
"As a [user type], I want [functionality] so that [benefit]"

Example:
"As a data analyst, I want to filter dashboard data by date range 
so that I can analyze trends for specific time periods"
```

**Sprint Backlog**:
```yaml
Definition: Product backlog items selected for sprint + plan for delivery
Components:
- Selected user stories
- Tasks to complete stories
- Estimated effort
- Sprint goal

Task Breakdown:
Story: "User login functionality"
Tasks:
- Design login UI (4 hours)
- Implement authentication (8 hours)
- Write unit tests (4 hours)
- Integration testing (2 hours)
```

**Increment**:
```yaml
Definition: Sum of all completed backlog items during sprint
Characteristics:
- Potentially shippable
- Meets Definition of Done
- Inspectable and usable
- Builds on previous increments

Definition of Done Example:
- Code written and reviewed
- Unit tests pass (>90% coverage)
- Integration tests pass
- Documentation updated
- Deployed to staging environment
```

## 5. User Stories and Estimation
**Story Writing**:
```yaml
# INVEST Criteria
Independent: Can be developed in any order
Negotiable: Details can be discussed
Valuable: Provides value to users
Estimable: Can be sized by team
Small: Fits within sprint
Testable: Has clear acceptance criteria

# Acceptance Criteria
Given [context]
When [action]
Then [outcome]

Example:
Given I am on the login page
When I enter valid credentials
Then I should be redirected to dashboard
```

**Estimation Techniques**:
```yaml
# Planning Poker
- Team estimates using Fibonacci sequence (1,2,3,5,8,13,21)
- Discussion until consensus reached
- Relative sizing, not absolute time

# Story Points Scale
1 point: Very simple, well understood
2 points: Simple with minor complexity
3 points: Medium complexity
5 points: Complex, some unknowns
8 points: Very complex, many unknowns
13+ points: Too large, needs breakdown
```

## 6. Metrics and Tracking
**Velocity**:
```yaml
Definition: Amount of work team completes per sprint
Calculation: Sum of story points completed
Usage:
- Sprint planning capacity
- Release planning
- Team performance trends

Example:
Sprint 1: 23 points
Sprint 2: 27 points  
Sprint 3: 25 points
Average Velocity: 25 points
```

**Burndown Charts**:
```yaml
# Sprint Burndown
X-axis: Days in sprint
Y-axis: Remaining work (hours/points)
Purpose: Track sprint progress daily

# Release Burndown  
X-axis: Sprints
Y-axis: Remaining features
Purpose: Track release progress
```

**Key Performance Indicators**:
```yaml
# Team Metrics
- Velocity trend
- Sprint goal achievement
- Defect rate
- Cycle time
- Team satisfaction

# Product Metrics
- Feature usage
- Customer satisfaction
- Business value delivered
- Time to market
```

## 7. Scaling Scrum
**Scrum of Scrums**:
```yaml
Purpose: Coordinate multiple scrum teams
Participants: Representatives from each team
Frequency: Daily or as needed
Format: Each rep answers:
- What has your team done since last meeting?
- What will your team do before next meeting?
- Are there any impediments affecting other teams?
```

**SAFe (Scaled Agile Framework)**:
```yaml
Levels:
- Team Level: Individual scrum teams
- Program Level: Agile Release Train (ART)
- Large Solution Level: Multiple ARTs
- Portfolio Level: Strategic themes

Key Events:
- PI Planning: Program Increment planning
- System Demo: Integrated solution demo
- Inspect & Adapt: Program-level retrospective
```

## 8. Tools and Techniques
**Common Tools**:
```yaml
# Physical Tools
- Scrum board (To Do/In Progress/Done)
- Sticky notes for user stories
- Burndown chart on wall
- Information radiators

# Digital Tools
- Jira (issue tracking)
- Azure DevOps (Microsoft)
- Rally (CA Technologies)
- VersionOne (Digital.ai)
```

**Jira Configuration**:
```yaml
# Issue Types
- Epic
- Story  
- Task
- Bug
- Subtask

# Workflow States
- To Do
- In Progress
- Code Review
- Testing
- Done

# Custom Fields
- Story Points
- Sprint
- Epic Link
- Acceptance Criteria
```

## 9. Common Challenges and Solutions
**Typical Issues**:
```yaml
# Scope Creep
Problem: Requirements change mid-sprint
Solution: Protect sprint scope, defer changes to next sprint

# Incomplete Stories
Problem: Stories not finished by sprint end
Solution: Better estimation, smaller stories, Definition of Done

# Team Dependencies
Problem: Waiting for other teams
Solution: Identify dependencies early, coordinate in planning

# Technical Debt
Problem: Code quality degradation
Solution: Include refactoring in sprint, maintain quality standards
```

## 10. Best Practices
**Team Practices**:
```yaml
# Sprint Planning
- Prepare backlog before meeting
- Include whole team in estimation
- Create clear sprint goal
- Break down large stories

# Daily Scrum
- Keep to 15 minutes
- Focus on coordination, not status
- Address impediments immediately
- Update task board

# Sprint Review
- Demo working software
- Get stakeholder feedback
- Focus on value delivered
- Update product roadmap
```

**Product Owner Practices**:
```yaml
# Backlog Management
- Keep backlog refined and prioritized
- Write clear user stories
- Define acceptance criteria
- Be available for questions

# Stakeholder Management
- Communicate product vision
- Manage expectations
- Gather feedback regularly
- Make priority decisions
```