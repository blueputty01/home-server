from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from app.core.database import Base


class Settings(Base):
    """Represents application settings."""

    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    imap_server = Column(String, index=True, nullable=True, default="")
    imap_username = Column(String, nullable=True, default="")
    imap_password = Column(String, nullable=True)
    search_folder = Column(String, default="INBOX")
    move_to_folder = Column(String, nullable=True)
    mark_as_read = Column(Boolean, default=False)
    email_check_interval = Column(Integer, default=15)  # Interval in minutes
    auto_add_new_senders = Column(Boolean, default=False)
    auth_username = Column(String, nullable=True)
    auth_password_hash = Column(String, nullable=True)


class GmailOAuth2Credential(Base):
    """Stores encrypted Gmail OAuth2 credentials and tokens."""

    __tablename__ = "gmail_oauth2_credentials"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    encrypted_access_token = Column(Text)  # Encrypted access token
    encrypted_refresh_token = Column(Text)  # Encrypted refresh token
    token_expiry = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(
        DateTime, server_default="CURRENT_TIMESTAMP", onupdate="CURRENT_TIMESTAMP"
    )
