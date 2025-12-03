"""
Abstract base class for LLM providers
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class LLMMessage:
    """Represents a message in the conversation"""
    role: str  # "user" or "assistant"
    content: str


class LLMProvider(ABC):
    """Abstract base class for LLM providers"""

    def __init__(self, model: str, **kwargs):
        """
        Initialize LLM provider

        Args:
            model: Model identifier
            **kwargs: Additional provider-specific arguments
        """
        self.model = model
        self.kwargs = kwargs

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate text completion

        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional arguments

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    def chat(
        self,
        messages: List[LLMMessage],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
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
        pass

    @abstractmethod
    def get_token_count(self, text: str) -> int:
        """
        Estimate token count for text

        Args:
            text: Text to count tokens for

        Returns:
            Estimated token count
        """
        pass

    def validate_api_key(self) -> bool:
        """
        Validate that API key is available

        Returns:
            True if API key is valid
        """
        raise NotImplementedError("Subclass must implement validate_api_key")

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate cost for API call

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Estimated cost in USD
        """
        raise NotImplementedError("Subclass must implement estimate_cost")
