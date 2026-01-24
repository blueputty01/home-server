"""Gmail OAuth2 service for handling authentication flow."""

from datetime import datetime, timedelta
from typing import Any

import google.auth.transport.requests
import google.oauth2.service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

from app.core.config import settings


# OAuth2 scopes needed for Gmail IMAP access
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]


def create_oauth2_flow(
    client_secrets: dict[str, Any], redirect_uri: str
) -> Flow:
    """Create an OAuth2 flow for Gmail authorization.
    
    Args:
        client_secrets: Google OAuth2 client secrets (JSON format).
        redirect_uri: Where to redirect after authorization.
        
    Returns:
        Configured OAuth2 Flow object.
    """
    flow = Flow.from_client_config(
        client_secrets, scopes=GMAIL_SCOPES, redirect_uri=redirect_uri
    )
    return flow


def get_authorization_url(
    client_secrets: dict[str, Any], redirect_uri: str
) -> tuple[str, str]:
    """Get the authorization URL for user to visit.
    
    Args:
        client_secrets: Google OAuth2 client secrets.
        redirect_uri: Redirect URI.
        
    Returns:
        Tuple of (authorization_url, state).
    """
    flow = create_oauth2_flow(client_secrets, redirect_uri)
    auth_url, state = flow.authorization_url(access_type="offline", prompt="consent")
    return auth_url, state


def exchange_code_for_tokens(
    client_secrets: dict[str, Any], redirect_uri: str, code: str
) -> tuple[str, str, datetime | None]:
    """Exchange authorization code for access and refresh tokens.
    
    Args:
        client_secrets: Google OAuth2 client secrets.
        redirect_uri: Redirect URI (must match the one used in authorization).
        code: Authorization code from Google's callback.
        
    Returns:
        Tuple of (access_token, refresh_token, expiry).
        
    Raises:
        Exception: If token exchange fails.
    """
    flow = create_oauth2_flow(client_secrets, redirect_uri)
    flow.fetch_token(code=code)
    
    credentials = flow.credentials
    return (
        credentials.token,
        credentials.refresh_token,
        credentials.expiry,
    )


def _flatten_client_secrets(secrets: dict[str, Any]) -> dict[str, str]:
    """Extract flat fields from Google client secrets.

    Supports either a flat dict or nested under "web"/"installed".
    """
    if {"client_id", "client_secret", "token_uri"}.issubset(secrets.keys()):
        return {
            "client_id": secrets["client_id"],
            "client_secret": secrets["client_secret"],
            "token_uri": secrets["token_uri"],
        }
    for key in ("web", "installed"):
        if key in secrets:
            inner = secrets[key]
            return {
                "client_id": inner["client_id"],
                "client_secret": inner["client_secret"],
                "token_uri": inner["token_uri"],
            }
    raise ValueError("Invalid Google client secrets structure")


def refresh_access_token(
    client_secrets: dict[str, Any], refresh_token: str
) -> tuple[str, datetime | None]:
    """Refresh an access token using a refresh token.
    
    Args:
        client_secrets: Google OAuth2 client secrets.
        refresh_token: The refresh token.
        
    Returns:
        Tuple of (new_access_token, new_expiry).
        
    Raises:
        Exception: If refresh fails.
    """
    flat = _flatten_client_secrets(client_secrets)
    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=flat["token_uri"],
        client_id=flat["client_id"],
        client_secret=flat["client_secret"],
    )
    
    request = Request()
    credentials.refresh(request)
    
    return credentials.token, credentials.expiry


def get_gmail_user_info(access_token: str) -> dict[str, Any]:
    """Get Gmail user info (email, name) from access token.
    
    Args:
        access_token: OAuth2 access token.
        
    Returns:
        User info dict with 'email', 'name', etc.
        
    Raises:
        Exception: If retrieval fails.
    """
    from googleapiclient.discovery import build

    credentials = Credentials(token=access_token)
    service = build("gmail", "v1", credentials=credentials)
    profile = service.users().getProfile(userId="me").execute()
    
    return {
        "email": profile.get("emailAddress"),
        "name": profile.get("displayName"),
    }


def is_token_expired(expiry: datetime | None) -> bool:
    """Check if a token is expired or close to expiring (within 5 minutes).
    
    Args:
        expiry: Token expiry datetime.
        
    Returns:
        True if expired or expiring soon, False otherwise.
    """
    if expiry is None:
        return False
    
    now = datetime.utcnow()
    expiry_threshold = expiry - timedelta(minutes=5)
    return now >= expiry_threshold
