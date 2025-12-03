"""
LLM configuration and factory for multi-provider support
"""

import os
from typing import Optional
from src.config import settings
from .provider import LLMProvider
from .claude import ClaudeProvider


class LLMConfig:
    """Configuration and factory for LLM providers"""

    # Supported providers
    PROVIDERS = {
        "claude": "ClaudeProvider",
        "openai": "OpenAIProvider",  # To be implemented in Phase 2
        "deepseek": "DeepSeekProvider",  # To be implemented in Phase 2
        "ollama": "OllamaProvider",  # To be implemented in Phase 2
    }

    @staticmethod
    def get_provider(provider_name: Optional[str] = None) -> LLMProvider:
        """
        Get LLM provider instance

        Args:
            provider_name: Name of provider (claude, openai, deepseek, ollama)
                          If None, uses LLM_PROVIDER environment variable

        Returns:
            LLMProvider instance

        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        provider = provider_name or settings.llm_provider

        if provider == "claude":
            api_key = settings.claude_api_key or os.getenv("CLAUDE_API_KEY")
            if not api_key:
                raise ValueError(
                    "Claude API key not found. Set CLAUDE_API_KEY environment variable."
                )
            return ClaudeProvider(api_key=api_key, model=settings.claude_model)

        elif provider == "openai":
            raise NotImplementedError("OpenAI provider will be implemented in Phase 2")

        elif provider == "deepseek":
            raise NotImplementedError("DeepSeek provider will be implemented in Phase 2")

        elif provider == "ollama":
            raise NotImplementedError("Ollama provider will be implemented in Phase 2")

        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider}. "
                f"Supported providers: {', '.join(LLMConfig.PROVIDERS.keys())}"
            )

    @staticmethod
    def list_providers() -> dict:
        """
        List all supported providers with their status

        Returns:
            Dictionary with provider status
        """
        status = {}
        for provider_name in LLMConfig.PROVIDERS.keys():
            try:
                provider = LLMConfig.get_provider(provider_name)
                is_valid = provider.validate_api_key()
                status[provider_name] = {
                    "status": "ready" if is_valid else "invalid_key",
                    "model": provider.model,
                }
            except NotImplementedError:
                status[provider_name] = {"status": "not_implemented"}
            except ValueError as e:
                status[provider_name] = {"status": "error", "error": str(e)}

        return status

    @staticmethod
    def validate_configuration() -> bool:
        """
        Validate current LLM configuration

        Returns:
            True if configuration is valid
        """
        try:
            provider = LLMConfig.get_provider()
            return provider.validate_api_key()
        except Exception as e:
            print(f"LLM configuration validation failed: {e}")
            return False


# Global LLM provider instance
_llm_provider: Optional[LLMProvider] = None


def get_llm() -> LLMProvider:
    """
    Get or create global LLM provider instance

    Returns:
        LLMProvider instance
    """
    global _llm_provider
    if _llm_provider is None:
        _llm_provider = LLMConfig.get_provider()
    return _llm_provider


def set_llm_provider(provider_name: str) -> LLMProvider:
    """
    Switch to a different LLM provider

    Args:
        provider_name: Name of provider to switch to

    Returns:
        New LLMProvider instance
    """
    global _llm_provider
    _llm_provider = LLMConfig.get_provider(provider_name)
    return _llm_provider
