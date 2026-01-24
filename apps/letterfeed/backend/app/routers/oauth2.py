"""OAuth2 routes for Gmail authentication."""

import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.auth import protected_route
from app.core.config import settings
from app.core.database import get_db
from app.crud.oauth2 import (
    delete_oauth2_credential,
    get_all_oauth2_credentials,
    get_oauth2_credential,
)
from app.schemas.auth import GmailOAuth2CallbackRequest, GmailOAuth2Credential
from app.services.oauth2 import (
    exchange_code_for_tokens,
    get_authorization_url,
    get_gmail_user_info,
)

router = APIRouter(prefix="/auth/google", tags=["oauth2"])

def get_client_secrets() -> dict[str, Any]:
    """Get Google OAuth2 client secrets from config or environment.
    
    In production, this should load from an environment variable or file.
    The secrets should include: client_id, client_secret, auth_uri, token_uri.
    """
    if not settings.google_client_secrets_json:
        return {}
    try:
        return json.loads(settings.google_client_secrets_json)
    except Exception:
        return {}


@router.post("/authorize")
async def start_gmail_oauth2(
    redirect_uri: str = Query(..., description="Where to redirect after auth"),
    _: str = Depends(protected_route),
) -> dict[str, str]:
    """Start Gmail OAuth2 authorization flow.
    
    Returns a URL that the user should visit to authorize Gmail access.
    
    Args:
        redirect_uri: Frontend URL to redirect to after authorization.
        _: Authenticated user (validates that app auth is enabled).
        
    Returns:
        Dict with 'authorization_url' to visit.
        
    Raises:
        HTTPException: If client secrets not configured.
    """
    secrets = get_client_secrets()
    if not secrets:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth2 is not configured. Set LETTERFEED_GOOGLE_CLIENT_SECRETS.",
        )
    
    try:
        auth_url, state = get_authorization_url(secrets, redirect_uri)
        return {
            "authorization_url": auth_url,
            "state": state,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate authorization URL: {str(e)}",
        ) from e


@router.post("/callback")
async def handle_gmail_oauth2_callback(
    request: GmailOAuth2CallbackRequest,
    redirect_uri: str = Query(..., description="Same redirect_uri used in authorize"),
    db: Session = Depends(get_db),
    _: str = Depends(protected_route),
) -> GmailOAuth2Credential:
    """Handle OAuth2 callback from Google.
    
    Exchanges the authorization code for access and refresh tokens.
    
    Args:
        request: Callback request with authorization code.
        redirect_uri: Same redirect_uri used in authorize step.
        db: Database session.
        _: Authenticated user.
        
    Returns:
        The stored credential (without tokens).
        
    Raises:
        HTTPException: If token exchange fails.
    """
    secrets = get_client_secrets()
    if not secrets:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth2 is not configured.",
        )
    
    try:
        # Exchange code for tokens
        access_token, refresh_token, expiry = exchange_code_for_tokens(
            secrets, redirect_uri, request.code
        )
        
        # Get user email
        user_info = get_gmail_user_info(access_token)
        email = user_info.get("email")
        
        if not email:
            raise ValueError("Could not retrieve email from Google account")
        
        # Store credential
        from app.crud.oauth2 import create_or_update_oauth2_credential
        
        credential = create_or_update_oauth2_credential(
            db, email, access_token, refresh_token, expiry
        )
        
        return GmailOAuth2Credential.model_validate(credential)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to exchange authorization code: {str(e)}",
        ) from e


@router.get("/credentials")
async def list_gmail_credentials(
    db: Session = Depends(get_db),
    _: str = Depends(protected_route),
) -> list[GmailOAuth2Credential]:
    """List all connected Gmail accounts.
    
    Args:
        db: Database session.
        _: Authenticated user.
        
    Returns:
        List of connected Gmail accounts (without tokens).
    """
    credentials = get_all_oauth2_credentials(db)
    return [GmailOAuth2Credential.model_validate(c) for c in credentials]


@router.get("/credentials/{email}")
async def get_gmail_credential(
    email: str,
    db: Session = Depends(get_db),
    _: str = Depends(protected_route),
) -> GmailOAuth2Credential:
    """Get a specific Gmail credential by email.
    
    Args:
        email: Gmail email address.
        db: Database session.
        _: Authenticated user.
        
    Returns:
        The credential (without tokens).
        
    Raises:
        HTTPException: If credential not found.
    """
    credential = get_oauth2_credential(db, email)
    if not credential:
        raise HTTPException(status_code=404, detail="Gmail account not found")
    
    return GmailOAuth2Credential.model_validate(credential)


@router.delete("/credentials/{email}")
async def disconnect_gmail(
    email: str,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> dict[str, str]:
    """Disconnect a Gmail account.
    
    Removes the stored credentials and tokens.
    
    Args:
        email: Gmail email address.
        db: Database session.
        _: Authenticated user.
        
    Returns:
        Success message.
        
    Raises:
        HTTPException: If credential not found.
    """
    if not delete_oauth2_credential(db, email):
        raise HTTPException(status_code=404, detail="Gmail account not found")
    
    return {"message": f"Disconnected {email}"}
