"""
Global configuration for Mindflow application
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "your_secret_key_here"

    # LLM Configuration
    llm_provider: str = "claude"
    claude_api_key: Optional[str] = None
    claude_model: str = "claude-3-5-haiku-20241022"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    deepseek_api_key: Optional[str] = None
    deepseek_model: str = "deepseek-chat"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"

    # Database
    database_url: str = "sqlite:///./data/mindflow.db"
    database_echo: bool = False

    # Gradio
    gradio_host: str = "0.0.0.0"
    gradio_port: int = 7860
    gradio_share: bool = False
    gradio_reload: bool = False

    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = "logs/mindflow.log"

    # Scheduler
    enable_scheduler: bool = True
    daily_review_time: str = "20:00"
    daily_plan_time: str = "09:00"

    # Data
    data_dir: str = "./data"
    auto_backup: bool = True
    backup_interval: int = 24
    max_backups: int = 7

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:7860"]

    class Config:
        """Pydantic config"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.app_env == "production"

    @property
    def database_url_path(self) -> str:
        """Get the database URL path"""
        if self.database_url.startswith("sqlite"):
            # Extract path from sqlite:///path/to/db
            path = self.database_url.replace("sqlite:///", "./")
            return str(Path(path).resolve())
        return self.database_url


# Load settings from environment
settings = Settings()

# Ensure data directories exist
os.makedirs(settings.data_dir, exist_ok=True)
if settings.log_file:
    log_dir = os.path.dirname(settings.log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
