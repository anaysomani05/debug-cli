"""Configuration management for the debug CLI."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv


class Config:
    """Configuration manager for the debug CLI."""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file: Path to configuration file, defaults to .env in current directory
        """
        self.config_file = config_file or ".env"
        self._load_config()

    def _load_config(self):
        """Load configuration from environment variables and config file."""
        # Load from .env file if it exists
        if Path(self.config_file).exists():
            load_dotenv(self.config_file)

        # Also try loading from home directory
        home_env = Path.home() / ".debug-cli" / ".env"
        if home_env.exists():
            load_dotenv(home_env)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return os.getenv(key, default)

    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get a boolean configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Boolean configuration value
        """
        value = self.get(key, str(default)).lower()
        return value in ("true", "1", "yes", "on", "enabled")

    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get an integer configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Integer configuration value
        """
        try:
            return int(self.get(key, str(default)))
        except ValueError:
            return default

    def get_float(self, key: str, default: float = 0.0) -> float:
        """
        Get a float configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Float configuration value
        """
        try:
            return float(self.get(key, str(default)))
        except ValueError:
            return default

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key."""
        return self.get("OPENAI_API_KEY")

    @property
    def openai_model(self) -> str:
        """Get OpenAI model to use."""
        return self.get("OPENAI_MODEL", "gpt-3.5-turbo")

    @property
    def backend_url(self) -> Optional[str]:
        """Get backend API URL."""
        return self.get("BACKEND_URL")

    @property
    def api_timeout(self) -> int:
        """Get API timeout in seconds."""
        return self.get_int("API_TIMEOUT", 30)

    @property
    def redis_url(self) -> Optional[str]:
        """Get Redis URL for caching."""
        return self.get("REDIS_URL")

    @property
    def cache_ttl(self) -> int:
        """Get cache TTL in seconds."""
        return self.get_int("CACHE_TTL", 3600)

    @property
    def default_explanation_style(self) -> str:
        """Get default explanation style."""
        return self.get("DEFAULT_EXPLANATION_STYLE", "detailed")

    @property
    def enable_colors(self) -> bool:
        """Get whether to enable colored output."""
        return self.get_bool("ENABLE_COLORS", True)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "openai_api_key": self.openai_api_key,
            "openai_model": self.openai_model,
            "backend_url": self.backend_url,
            "api_timeout": self.api_timeout,
            "redis_url": self.redis_url,
            "cache_ttl": self.cache_ttl,
            "default_explanation_style": self.default_explanation_style,
            "enable_colors": self.enable_colors,
        }

    def validate(self) -> Dict[str, str]:
        """
        Validate configuration.

        Returns:
            Dictionary of validation errors (empty if valid)
        """
        errors = {}

        if not self.openai_api_key:
            errors["openai_api_key"] = "OpenAI API key is required"

        if self.api_timeout <= 0:
            errors["api_timeout"] = "API timeout must be positive"

        if self.cache_ttl <= 0:
            errors["cache_ttl"] = "Cache TTL must be positive"

        return errors
