"""Settings and configuration management."""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings managed from environment variables."""

    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "@Anvesha94")
    DB_NAME: str = os.getenv("DB_NAME", "agentic_bi")

    # Google Gemini API
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.3"))

    # App Configuration
    APP_NAME: str = "Agentic BI"
    APP_VERSION: str = "0.8.0"
    DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "False").lower() == "true"
    MAX_QUERY_ATTEMPTS: int = int(os.getenv("MAX_QUERY_ATTEMPTS", "3"))
    QUERY_TIMEOUT: int = int(os.getenv("QUERY_TIMEOUT", "30"))
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "True").lower() == "true"

    # UI Configuration
    PAGE_ICON: str = "📊"
    THEME: str = os.getenv("THEME", "dark")
    PRIMARY_COLOR: str = "#0891B2"
    SECONDARY_COLOR: str = "#065A82"
    ACCENT_COLOR: str = "#0891B2"
    BG_COLOR: str = "#0F172A"
    TEXT_COLOR: str = "#F8FAFC"

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 500

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL database URL."""
        from urllib.parse import quote_plus

        password = quote_plus(self.DB_PASSWORD)
        return f"postgresql://{self.DB_USER}:{password}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def is_configured(self) -> bool:
        """Check if all required settings are configured."""
        return bool(self.GOOGLE_API_KEY and self.DB_PASSWORD)


# Global settings instance
settings = Settings()
