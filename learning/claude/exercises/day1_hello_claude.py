"""
Day 1: Hello Claude - Practice Exercises
Learning Goal: Master basic Claude API usage

Setup:
1. Install: pip install anthropic python-dotenv
2. Create .env file with: ANTHROPIC_API_KEY=sk-ant-your-key-here
3. Run: python day1_hello_claude.py
"""

from anthropic import Anthropic, APIError, RateLimitError, APIConnectionError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("=" * 60)
print("Day 1: Hello Claude - Practice Exercises")
print("=" * 60)

# ============================================
# Exercise 1: Your First API Call
# ============================================

print("\n" + "=" * 60)
print("Exercise 1: Your First API Call")
print("=" * 60)

try:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, Claude! Introduce yourself in one sentence."}
        ]
    )
    
    print(f"\nClaude's response:")
    print(message.content[0].text)
    
    print(f"\nToken usage:")
    print(f"  Input tokens: {message.usage.input_tokens}")
    print(f"  Output tokens: {message.usage.output_tokens}")
    print(f"  Total tokens: {message.usage.input_tokens + message.usage.output_tokens}")
    
except APIError as e:
    print(f"Error: {e}")

# ============================================
# Exercise 2: Using System Prompts
# ============================================

print("\n" + "=" * 60)
print("Exercise 2: Using System Prompts")
print("=" * 60)

# Without system prompt
message1 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "What is Python?"}
    ]
)

print("\nWithout system prompt:")
print(message1.content[0].text)

# With system prompt
message2 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=100,
    system="You are a Python expert who explains concepts using simple analogies.",
    messages=[
        {"role": "user", "content": "What is Python?"}
    ]
)

print("\nWith system prompt (Python expert with analogies):")
print(message2.content[0].text)

# ============================================
# Exercise 3: Different Models Comparison
# ============================================

print("\n" + "=" * 60)
print("Exercise 3: Different Models Comparison")
print("=" * 60)

question = "Explain machine learning in 2 sentences."

# Claude 3.5 Haiku (Fast & Cheap)
haiku_response = client.messages.create(
    model="claude-3-5-haiku-20241022",
    max_tokens=100,
    messages=[{"role": "user", "content": question}]
)

print("\nClaude 3.5 Haiku:")
print(haiku_response.content[0].text)
print(f"Tokens: {haiku_response.usage.input_tokens + haiku_response.usage.output_tokens}")

# Claude 3.5 Sonnet (Balanced)
sonnet_response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=100,
    messages=[{"role": "user", "content": question}]
)

print("\nClaude 3.5 Sonnet:")
print(sonnet_response.content[0].text)
print(f"Tokens: {sonnet_response.usage.input_tokens + sonnet_response.usage.output_tokens}")

# ============================================
# Exercise 4: Error Handling
# ============================================

print("\n" + "=" * 60)
print("Exercise 4: Error Handling")
print("=" * 60)

# Test 1: Invalid model name
print("\nTest 1: Invalid model name")
try:
    message = client.messages.create(
        model="invalid-model-name",
        max_tokens=100,
        messages=[{"role": "user", "content": "Hello"}]
    )
except APIError as e:
    print(f"✓ Caught error: {type(e).__name__}")
    print(f"  Message: {str(e)[:100]}...")

# Test 2: Missing max_tokens
print("\nTest 2: Missing max_tokens")
try:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": "Hello"}]
    )
except TypeError as e:
    print(f"✓ Caught error: {type(e).__name__}")
    print(f"  Message: {str(e)[:100]}...")

# Test 3: Empty messages
print("\nTest 3: Empty messages")
try:
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=100,
        messages=[]
    )
except APIError as e:
    print(f"✓ Caught error: {type(e).__name__}")
    print(f"  Message: {str(e)[:100]}...")

# ============================================
# Exercise 5: Token Usage and Cost Estimation
# ============================================

print("\n" + "=" * 60)
print("Exercise 5: Token Usage and Cost Estimation")
print("=" * 60)

def estimate_cost(message, model_name="sonnet"):
    """Estimate API call cost based on token usage"""
    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    
    # Pricing (as of 2024, check current rates)
    if "haiku" in model_name.lower():
        input_price = 0.25 / 1_000_000   # $0.25 per million
        output_price = 1.25 / 1_000_000  # $1.25 per million
    elif "sonnet" in model_name.lower():
        input_price = 3 / 1_000_000      # $3 per million
        output_price = 15 / 1_000_000    # $15 per million
    else:  # opus
        input_price = 15 / 1_000_000     # $15 per million
        output_price = 75 / 1_000_000    # $75 per million
    
    input_cost = input_tokens * input_price
    output_cost = output_tokens * output_price
    total_cost = input_cost + output_cost
    
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost
    }

# Make a test call
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=500,
    messages=[
        {"role": "user", "content": "Write a short poem about programming."}
    ]
)

print(f"\nResponse:")
print(message.content[0].text)

cost_info = estimate_cost(message, "sonnet")
print(f"\nCost Analysis:")
print(f"  Input tokens: {cost_info['input_tokens']}")
print(f"  Output tokens: {cost_info['output_tokens']}")
print(f"  Total tokens: {cost_info['total_tokens']}")
print(f"  Input cost: ${cost_info['input_cost']:.6f}")
print(f"  Output cost: ${cost_info['output_cost']:.6f}")
print(f"  Total cost: ${cost_info['total_cost']:.6f}")

# ============================================
# Practice Tasks
# ============================================

print("\n" + "=" * 60)
print("Practice Tasks")
print("=" * 60)

print("""
Complete these tasks to practice:

1. Create a system prompt that makes Claude respond as a:
   - Pirate
   - Shakespeare character
   - Technical documentation writer

2. Compare token usage between:
   - Short vs long prompts
   - Different models (Haiku vs Sonnet)
   - With and without system prompts

3. Build a simple cost calculator that:
   - Takes a prompt as input
   - Estimates tokens (rough: 1 token ≈ 4 chars)
   - Calculates expected cost before calling API

4. Experiment with max_tokens:
   - Set to 10, 50, 100, 500
   - Observe how responses are truncated
   - Find the sweet spot for your use case

5. Error handling practice:
   - Simulate network errors
   - Handle rate limits gracefully
   - Implement retry logic with exponential backoff
""")

# ============================================
# Bonus: Helper Function
# ============================================

print("\n" + "=" * 60)
print("Bonus: Reusable Helper Function")
print("=" * 60)

def ask_claude(
    prompt: str,
    system: str = None,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: int = 1024,
    temperature: float = 1.0
) -> dict:
    """
    Simplified Claude API wrapper
    
    Args:
        prompt: User's question or instruction
        system: System prompt (optional)
        model: Model to use
        max_tokens: Maximum tokens to generate
        temperature: Randomness (0-1)
    
    Returns:
        dict with 'text', 'usage', and 'cost' keys
    """
    try:
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": prompt}]
        )
        
        cost_info = estimate_cost(message, model)
        
        return {
            "text": message.content[0].text,
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
                "total_tokens": message.usage.input_tokens + message.usage.output_tokens
            },
            "cost": cost_info["total_cost"],
            "stop_reason": message.stop_reason
        }
    except APIError as e:
        return {
            "error": str(e),
            "text": None
        }

# Test the helper function
print("\nTesting helper function:")
result = ask_claude(
    prompt="What are the three laws of robotics?",
    system="You are Isaac Asimov.",
    max_tokens=200
)

if result.get("text"):
    print(f"\nResponse: {result['text']}")
    print(f"Tokens: {result['usage']['total_tokens']}")
    print(f"Cost: ${result['cost']:.6f}")
else:
    print(f"Error: {result['error']}")

print("\n" + "=" * 60)
print("Day 1 Complete! 🎉")
print("=" * 60)
print("""
Key Learnings:
1. ✅ Basic API structure: model, max_tokens, messages
2. ✅ System prompts change Claude's behavior
3. ✅ Different models have different trade-offs
4. ✅ Always handle errors gracefully
5. ✅ Monitor token usage for cost control

Next: Day 2 - Multi-turn conversations and advanced parameters
""")
