---
name: daily-review
description: Daily work and learning review. Use when user mentions daily review, daily summary, today's review, or work log.
metadata:
  id: skill_daily_review
  display_name: Daily Review
  preconditions:
    - has_daily_activities
  effects:
    - has_review_notes
  methodology_scores:
    meth_reflect: 0.9
    meth_iterate: 0.8
  parent_methodologies:
    - meth_reflect
    - meth_iterate
  called_skills: []
  tags:
    - life-management
    - review
    - productivity
  version: "1.0.0"
  author: MindFlow
---

# Daily Review

## Overview

Daily work and learning review. Through a structured review process, helps accumulate experience, identify problems, and continuously improve.

## Execution Steps

1. Review tasks completed today
2. Record problems encountered and solutions
3. Summarize lessons learned
4. Plan key tasks for tomorrow
5. Output structured review notes

## Review Template

```markdown
# Daily Review - {{date}}

## Completed Today
- [ ] Task 1
- [ ] Task 2

## Problems Encountered
1. Problem description
   - Solution: ...

## Lessons Learned
- What I learned
- What can be improved next time

## Tomorrow's Plan
1. Key task 1
2. Key task 2

## Mood/Status
😊 / 😐 / 😔
```

## Best Practices

### Fixed Time
- Recommended 15-30 minutes before end of workday
- Consistent timing helps build habits

### Focus on Key Points
- No need to record every detail
- Focus on valuable experiences and lessons

### Action-Oriented
- Every problem should have a solution or next action
- Tomorrow's plan should be specific and actionable
