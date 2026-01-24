"""CRUD operations for Gmail OAuth2 credentials."""

from datetime import datetime

from sqlalchemy.orm import Session

from app.core.encryption import decrypt_token, encrypt_token
from app.models.settings import GmailOAuth2Credential


def create_or_update_oauth2_credential(
    db: Session,
    email: str,
    access_token: str,
    refresh_token: str,
    token_expiry: datetime | None,
) -> GmailOAuth2Credential:
    """Create or update a Gmail OAuth2 credential.
    
    Args:
        db: Database session.
        email: Gmail email address.
        access_token: OAuth2 access token.
        refresh_token: OAuth2 refresh token.
        token_expiry: Token expiration timestamp.
        
    Returns:
        The created or updated credential.
    """
    credential = db.query(GmailOAuth2Credential).filter_by(email=email).first()
    
    encrypted_access = encrypt_token(access_token)
    encrypted_refresh = encrypt_token(refresh_token)
    
    if credential:
        credential.encrypted_access_token = encrypted_access
        credential.encrypted_refresh_token = encrypted_refresh
        credential.token_expiry = token_expiry
        credential.updated_at = datetime.utcnow()
    else:
        credential = GmailOAuth2Credential(
            email=email,
            encrypted_access_token=encrypted_access,
            encrypted_refresh_token=encrypted_refresh,
            token_expiry=token_expiry,
        )
        db.add(credential)
    
    db.commit()
    db.refresh(credential)
    return credential


def get_oauth2_credential(db: Session, email: str) -> GmailOAuth2Credential | None:
    """Get a Gmail OAuth2 credential by email.
    
    Args:
        db: Database session.
        email: Gmail email address.
        
    Returns:
        The credential if found, None otherwise.
    """
    return db.query(GmailOAuth2Credential).filter_by(email=email).first()


def get_all_oauth2_credentials(db: Session) -> list[GmailOAuth2Credential]:
    """Get all Gmail OAuth2 credentials.
    
    Args:
        db: Database session.
        
    Returns:
        List of all credentials.
    """
    return db.query(GmailOAuth2Credential).all()


def delete_oauth2_credential(db: Session, email: str) -> bool:
    """Delete a Gmail OAuth2 credential.
    
    Args:
        db: Database session.
        email: Gmail email address.
        
    Returns:
        True if deleted, False if not found.
    """
    credential = db.query(GmailOAuth2Credential).filter_by(email=email).first()
    if credential:
        db.delete(credential)
        db.commit()
        return True
    return False


def get_decrypted_credential(
    db: Session, email: str
) -> tuple[str, str] | None:
    """Get decrypted access and refresh tokens for a Gmail account.
    
    Args:
        db: Database session.
        email: Gmail email address.
        
    Returns:
        Tuple of (access_token, refresh_token) if found, None otherwise.
    """
    credential = get_oauth2_credential(db, email)
    if not credential:
        return None
    
    try:
        access_token = decrypt_token(credential.encrypted_access_token)
        refresh_token = decrypt_token(credential.encrypted_refresh_token)
        return access_token, refresh_token
    except Exception:
        return None


def update_oauth2_tokens(
    db: Session, email: str, access_token: str, token_expiry: datetime | None
) -> GmailOAuth2Credential | None:
    """Update OAuth2 tokens (typically after refresh).
    
    Args:
        db: Database session.
        email: Gmail email address.
        access_token: New access token.
        token_expiry: New expiration timestamp.
        
    Returns:
        Updated credential, or None if not found.
    """
    credential = db.query(GmailOAuth2Credential).filter_by(email=email).first()
    if not credential:
        return None
    
    credential.encrypted_access_token = encrypt_token(access_token)
    credential.token_expiry = token_expiry
    credential.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(credential)
    return credential
