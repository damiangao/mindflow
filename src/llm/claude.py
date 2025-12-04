"""
Anthropic Claude LLM provider implementation
"""

from typing import Optional, List
import anthropic

from .provider import LLMProvider, LLMMessage


class ClaudeProvider(LLMProvider):
    """Claude LLM provider using Anthropic API"""

    def __init__(self, api_key: str, model: str = "claude-3-5-haiku-20241022", **kwargs):
        """
        Initialize Claude provider

        Args:
            api_key: Anthropic API key
            model: Claude model identifier
            **kwargs: Additional arguments
        """
        super().__init__(model, **kwargs)
        self.api_key = api_key
        self.client = anthropic.Anthropic(api_key=api_key)

        # Model pricing (USD per 1M tokens)
        self.pricing = {
            "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
            "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
            "claude-3-opus-20250219": {"input": 15.00, "output": 75.00},
        }

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 1000,
        **kwargs
    ) -> str:
        """
        Generate text completion using Claude

        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional arguments

        Returns:
            Generated text
        """
        messages = [{"role": "user", "content": prompt}]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens or 1000,
            system=system_prompt,
            messages=messages,
            temperature=temperature,
        )

        return response.content[0].text

    def chat(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = 1000,
        **kwargs
    ) -> str:
        """
        Chat completion with conversation history

        Args:
            messages: List of messages in conversation
            system_prompt: System prompt for context
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional arguments

        Returns:
            Assistant response
        """
        # Convert LLMMessage to Anthropic format
        api_messages = [
            {"role": msg.role, "content": msg.content} for msg in messages
        ]

        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens or 1000,
            system=system_prompt,
            messages=api_messages,
            temperature=temperature,
        )

        return response.content[0].text

    def get_token_count(self, text: str) -> int:
        """
        Estimate token count using Claude's tokenizer

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        # Claude uses roughly 4 chars per token as rough estimate
        # For production, use: client.beta.messages.count_tokens()
        return len(text) // 4

    def validate_api_key(self) -> bool:
        """
        Validate Claude API key by making a test request

        Returns:
            True if API key is valid
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "ping"}],
            )
            return response.stop_reason == "end_turn"
        except Exception:
            return False

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for API call

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Estimated cost in USD
        """
        pricing = self.pricing.get(self.model, {"input": 0.00, "output": 0.00})
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost
