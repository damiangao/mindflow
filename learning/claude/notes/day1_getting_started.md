# Day 1: Getting Started with Claude API

## Learning Objectives

- Understand Claude API basics
- Set up authentication
- Make your first API call
- Understand request/response structure

## 1. What is Claude API?

Claude is Anthropic's family of large language models. The API allows you to:
- Generate text responses
- Have multi-turn conversations
- Process and analyze content
- Build AI-powered applications

## 2. API Authentication

### API Key Structure
- Format: `sk-ant-api03-...`
- Keep it secret! Never commit to git
- Store in environment variables

### Best Practices
```python
# ✅ Good: Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# ❌ Bad: Hardcode in code
api_key = "sk-ant-api03-..."  # Never do this!
```

## 3. Basic Request Structure

### Minimal Request
```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Request Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `model` | Yes | Model identifier |
| `max_tokens` | Yes | Maximum tokens to generate |
| `messages` | Yes | List of conversation messages |
| `system` | No | System prompt for behavior |
| `temperature` | No | Randomness (0-1, default 1) |
| `top_p` | No | Nucleus sampling (0-1) |
| `top_k` | No | Top-k sampling |

## 4. Response Structure

### Response Object
```python
{
    "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "Hello! How can I help you today?"
        }
    ],
    "model": "claude-3-5-sonnet-20241022",
    "stop_reason": "end_turn",
    "usage": {
        "input_tokens": 10,
        "output_tokens": 20
    }
}
```

### Key Fields
- `content[0].text`: The actual response text
- `usage`: Token consumption (for billing)
- `stop_reason`: Why generation stopped
  - `end_turn`: Natural completion
  - `max_tokens`: Hit token limit
  - `stop_sequence`: Hit stop sequence

## 5. Message Roles

### User Role
```python
{"role": "user", "content": "What is Python?"}
```
- Represents user input
- Can include questions, instructions, or data

### Assistant Role
```python
{"role": "assistant", "content": "Python is a programming language..."}
```
- Represents Claude's responses
- Used in multi-turn conversations

### System Prompt (Special)
```python
client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful Python tutor.",  # Not in messages array
    messages=[...]
)
```
- Sets Claude's behavior and context
- Not counted as a message
- Applied to entire conversation

## 6. Error Handling

### Common Errors

```python
from anthropic import APIError, RateLimitError, APIConnectionError

try:
    message = client.messages.create(...)
except RateLimitError:
    print("Rate limit exceeded. Wait and retry.")
except APIConnectionError:
    print("Network error. Check connection.")
except APIError as e:
    print(f"API error: {e}")
```

### Error Types
- `RateLimitError`: Too many requests
- `APIConnectionError`: Network issues
- `AuthenticationError`: Invalid API key
- `BadRequestError`: Invalid parameters

## 7. Token Counting

### What are Tokens?
- Tokens ≈ words or word pieces
- English: ~1 token per 4 characters
- Chinese: ~1 token per 2-3 characters

### Estimating Costs
```python
# Check usage after each call
print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")

# Approximate cost (check current pricing)
# Sonnet: $3 per million input tokens, $15 per million output tokens
input_cost = message.usage.input_tokens * 3 / 1_000_000
output_cost = message.usage.output_tokens * 15 / 1_000_000
total_cost = input_cost + output_cost
print(f"Estimated cost: ${total_cost:.6f}")
```

## 8. Model Selection

### Claude 3.5 Sonnet (Recommended)
- **Best for:** Most tasks
- **Speed:** Fast
- **Cost:** Moderate
- **Use when:** General purpose, balanced performance

### Claude 3.5 Haiku
- **Best for:** Simple tasks, high volume
- **Speed:** Very fast
- **Cost:** Low
- **Use when:** Cost-sensitive, speed critical

### Claude 3 Opus
- **Best for:** Complex reasoning
- **Speed:** Slower
- **Cost:** High
- **Use when:** Difficult problems, highest quality needed

## 9. Quick Reference

### Complete Example
```python
from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Create message
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a helpful assistant.",
    messages=[
        {"role": "user", "content": "Explain Python in one sentence."}
    ]
)

# Print response
print(message.content[0].text)

# Print usage
print(f"\nTokens used: {message.usage.input_tokens + message.usage.output_tokens}")
```

## Practice Exercises

See `exercises/day1_hello_claude.py` for hands-on practice.

## Key Takeaways

1. ✅ Always use environment variables for API keys
2. ✅ `model`, `max_tokens`, and `messages` are required
3. ✅ Response text is in `message.content[0].text`
4. ✅ Monitor token usage for cost control
5. ✅ Handle errors gracefully

## Next Steps

Tomorrow (Day 2), we'll explore:
- System prompts in detail
- Multi-turn conversations
- Temperature and sampling parameters
- Advanced message formatting

---

**Day 1 Complete!** 🎉  
Move on to `exercises/day1_hello_claude.py` to practice.
