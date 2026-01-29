---
name: task-decompose
description: Decompose complex tasks into executable small steps. Use when user mentions task decomposition, breaking down tasks, planning steps, or project planning.
metadata:
  id: skill_task_decompose
  display_name: Task Decomposition
  preconditions:
    - has_task_description
  effects:
    - has_task_list
  methodology_scores:
    meth_simple: 0.9
    meth_iterate: 0.9
  parent_methodologies:
    - meth_simple
    - meth_iterate
  called_skills: []
  tags:
    - life-management
    - planning
    - productivity
  version: "1.0.0"
  author: MindFlow
---

# Task Decomposition

## Overview

Decompose complex tasks into executable small steps. Through structured decomposition methods, make large tasks manageable and trackable.

## Execution Steps

1. Understand the final goal of the task
2. Identify key milestones
3. Break down each milestone into specific steps
4. Determine dependencies between steps
5. Output structured task list

## Decomposition Principles

### SMART Principles

Each subtask should be:
- **S**pecific: Clear about what to do
- **M**easurable: Know when it's complete
- **A**chievable: Within capability range
- **R**elevant: Related to the goal
- **T**ime-bound: Has clear deadline

### Granularity

- Each subtask should be completable within **2-4 hours**
- If exceeds 4 hours, continue decomposing
- If less than 30 minutes, consider merging

## Decomposition Template

```markdown
# Task: {{task_name}}

## Goal
{{final_goal}}

## Milestones
1. [ ] Milestone 1 - Deadline
2. [ ] Milestone 2 - Deadline
3. [ ] Milestone 3 - Deadline

## Detailed Steps

### Milestone 1: {{milestone_name}}
- [ ] Step 1.1: Specific task description (Estimated time)
- [ ] Step 1.2: Specific task description (Estimated time)
  - Depends on: Step 1.1

### Milestone 2: {{milestone_name}}
- [ ] Step 2.1: Specific task description (Estimated time)

## Dependencies
- Step 1.2 depends on Step 1.1
- Milestone 2 depends on Milestone 1

## Risks and Notes
- Risk 1: Description and mitigation measures
```

## Example

### Input
> I want to learn Python data analysis

### Output

```markdown
# Task: Learn Python Data Analysis

## Goal
Be able to perform basic data analysis using Python, including data cleaning, visualization, and simple statistics

## Milestones
1. [ ] Environment Setup - Day 1
2. [ ] Basic Syntax - Week 1
3. [ ] Pandas Basics - Week 2
4. [ ] Data Visualization - Week 3
5. [ ] Practical Project - Week 4

## Detailed Steps

### Milestone 1: Environment Setup
- [ ] Install Python 3.x (30 minutes)
- [ ] Install VS Code and Python extension (30 minutes)
- [ ] Install Jupyter Notebook (30 minutes)
- [ ] Verify environment: Run Hello World (15 minutes)

### Milestone 2: Basic Syntax
- [ ] Learn variables and data types (2 hours)
- [ ] Learn control flow (2 hours)
- [ ] Learn function definition (2 hours)
- [ ] Complete 10 practice problems (3 hours)
```

## Common Issues

### Task Too Large, Don't Know Where to Start
- Write the final goal first
- Work backwards to identify intermediate deliverables
- Each intermediate deliverable is a milestone

### Too Many Tasks After Decomposition
- Sort by priority
- Complete the most important 3-5 first
- Other tasks can be adjusted later
