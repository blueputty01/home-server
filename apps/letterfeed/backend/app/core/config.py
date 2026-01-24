from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

"""Configuration settings for the Letterfeed application."""

from cryptography.fernet import Fernet


class Settings(BaseSettings):
    """Application settings, loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_prefix="LETTERFEED_", frozen=True
    )

    production: bool = Field(
        False,
        validation_alias=AliasChoices("PRODUCTION", "LETTERFEED_PRODUCTION"),
    )

    database_url: str = Field(
        "sqlite:////data/letterfeed.db",
        validation_alias=AliasChoices("DATABASE_URL", "LETTERFEED_DATABASE_URL"),
    )
    app_base_url: str = Field(
        "http://backend:8000",
        validation_alias=AliasChoices("APP_BASE_URL", "LETTERFEED_APP_BASE_URL"),
    )
    imap_server: str = ""
    imap_username: str = ""
    imap_password: str = ""
    search_folder: str = "INBOX"
    move_to_folder: str | None = None
    mark_as_read: bool = False
    email_check_interval: int = 15
    auto_add_new_senders: bool = False
    auth_username: str | None = None
    auth_password: str | None = None
    secret_key: str | None = Field(
        default=None,
        validation_alias=AliasChoices("SECRET_KEY", "LETTERFEED_SECRET_KEY"),
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    # Base64-urlsafe 32-byte key as a string; will be encoded to bytes at use
    encryption_key: str = Field(
        default_factory=lambda: Fernet.generate_key().decode(),
        validation_alias=AliasChoices("ENCRYPTION_KEY", "LETTERFEED_ENCRYPTION_KEY"),
    )
    # Raw JSON string containing Google OAuth2 client secrets ("web" or "installed")
    google_client_secrets_json: str | None = Field(
        default=None,
        validation_alias=AliasChoices(
            "GOOGLE_CLIENT_SECRETS", "LETTERFEED_GOOGLE_CLIENT_SECRETS"
        ),
    )


settings = Settings()
