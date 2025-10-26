"""Configuration settings for WordPress MCP Server."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings loaded from environment variables."""
    
    # WordPress Configuration
    WORDPRESS_URL: str = os.getenv("WORDPRESS_URL", "")
    WORDPRESS_USERNAME: str = os.getenv("WORDPRESS_USERNAME", "")
    WORDPRESS_APP_PASSWORD: str = os.getenv("WORDPRESS_APP_PASSWORD", "")
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Default Settings
    DEFAULT_POST_STATUS: str = os.getenv("DEFAULT_POST_STATUS", "draft")
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "da")
    
    # API Settings
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required settings are present."""
        required = [
            cls.WORDPRESS_URL,
            cls.WORDPRESS_USERNAME,
            cls.WORDPRESS_APP_PASSWORD,
        ]
        return all(required)
    
    @classmethod
    def get_wordpress_api_url(cls) -> str:
        """Get the WordPress REST API base URL."""
        return f"{cls.WORDPRESS_URL.rstrip('/')}/wp-json/wp/v2"


# Create settings instance
settings = Settings()

