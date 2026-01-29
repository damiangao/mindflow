# Claude API Learning Guide

## Overview

This 5-day learning plan will help you master the Claude API for integration into the MindFlow project.

## Learning Objectives

By the end of this course, you will be able to:
- ✅ Understand Claude API fundamentals
- ✅ Make API calls with proper authentication
- ✅ Use streaming responses for real-time interaction
- ✅ Implement prompt engineering best practices
- ✅ Handle errors and rate limits
- ✅ Integrate Claude into Python applications

## Prerequisites

- Python 3.8+
- Basic understanding of REST APIs
- Familiarity with async/await (helpful but not required)

## Course Structure

### Day 1: Getting Started
- API authentication and setup
- First API call
- Understanding request/response structure
- Basic message format

**Files:**
- `notes/day1_getting_started.md`
- `exercises/day1_hello_claude.py`

### Day 2: Message API Deep Dive
- System prompts and roles
- Multi-turn conversations
- Temperature and other parameters
- Token counting and limits

**Files:**
- `notes/day2_messages.md`
- `exercises/day2_conversations.py`

### Day 3: Streaming and Async
- Streaming responses
- Async API calls
- Real-time interaction patterns
- Performance optimization

**Files:**
- `notes/day3_streaming.md`
- `exercises/day3_streaming.py`

### Day 4: Prompt Engineering
- Prompt design principles
- Few-shot learning
- Chain-of-thought prompting
- XML tags for structured input

**Files:**
- `notes/day4_prompts.md`
- `exercises/day4_prompt_engineering.py`

### Day 5: Integration & Best Practices
- Error handling and retries
- Rate limiting strategies
- Cost optimization
- Production-ready patterns
- **MindFlow Integration Example**

**Files:**
- `notes/day5_best_practices.md`
- `exercises/day5_mindflow_integration.py`

## Setup Instructions

### 1. Install Dependencies

```bash
cd F:/workspace/mindflow
.venv\Scripts\activate
pip install anthropic python-dotenv
```

### 2. Get API Key

1. Visit https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

### 3. Configure Environment

Create `.env` file in project root:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### 4. Test Setup

```python
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)
print(message.content[0].text)
```

## Available Models

| Model | Context Window | Best For |
|-------|---------------|----------|
| claude-3-5-sonnet-20241022 | 200K tokens | Most tasks (recommended) |
| claude-3-5-haiku-20241022 | 200K tokens | Fast, cost-effective |
| claude-3-opus-20240229 | 200K tokens | Complex reasoning |

## Key Concepts

### Message Format
```python
{
    "role": "user",  # or "assistant"
    "content": "Your message here"
}
```

### System Prompts
```python
client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful assistant...",  # System prompt
    messages=[...]
)
```

### Streaming
```python
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[...]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

## Resources

### Official Documentation
- [Anthropic API Docs](https://docs.anthropic.com/)
- [Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

### Best Practices
- Always use environment variables for API keys
- Implement exponential backoff for retries
- Monitor token usage and costs
- Use streaming for better UX
- Cache system prompts when possible

## Daily Practice Routine

1. **Read** the day's notes (15-20 min)
2. **Run** the example code (10 min)
3. **Modify** examples to experiment (20 min)
4. **Complete** the practice exercises (30 min)
5. **Review** and document learnings (10 min)

**Total: ~1.5 hours per day**

## Progress Tracking

- [ ] Day 1: Getting Started
- [ ] Day 2: Message API Deep Dive
- [ ] Day 3: Streaming and Async
- [ ] Day 4: Prompt Engineering
- [ ] Day 5: Integration & Best Practices

## Next Steps

After completing this course:
1. Integrate Claude into MindFlow's skill execution
2. Implement prompt templates for different skill types
3. Add conversation memory for context-aware responses
4. Build a skill recommendation system using Claude

## Support

If you encounter issues:
1. Check the [official documentation](https://docs.anthropic.com/)
2. Review error messages carefully
3. Verify API key and environment setup
4. Check rate limits and quotas

---

**Version:** 1.0  
**Last Updated:** 2026-01-29  
**Author:** MindFlow Team
