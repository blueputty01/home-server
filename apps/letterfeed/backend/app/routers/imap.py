from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.imap import _test_imap_connection, get_folders
from app.core.logging import get_logger
from app.crud.settings import create_or_update_settings, get_settings
from app.schemas.settings import Settings, SettingsCreate
from app.services.email_processor import process_emails
from app.crud.oauth2 import get_oauth2_credential, get_decrypted_credential
from app.services.oauth2 import is_token_expired, refresh_access_token
from app.core.config import settings as app_settings
import json as _json

logger = get_logger(__name__)
router = APIRouter()


@router.get("/imap/settings", response_model=Settings)
def read_settings(db: Session = Depends(get_db)):
    """Retrieve IMAP settings."""
    logger.info("Request to read IMAP settings")
    settings = get_settings(db)
    if not settings:
        logger.warning("IMAP settings not found")
        raise HTTPException(status_code=404, detail="IMAP settings not found")
    return settings


@router.post("/imap/settings", response_model=Settings)
def update_settings(settings: SettingsCreate, db: Session = Depends(get_db)):
    """Update IMAP settings."""
    logger.info("Request to update IMAP settings")
    return create_or_update_settings(db=db, settings=settings)


@router.post("/imap/test")
def test_connection(db: Session = Depends(get_db)):
    """Test the IMAP connection with current settings."""
    logger.info("Request to test IMAP connection")
    settings = get_settings(db, with_password=True)
    if not settings:
        logger.error("IMAP settings not found, cannot test connection")
        raise HTTPException(status_code=404, detail="IMAP settings not found")

    # Prefer OAuth2 for Gmail when available
    oauth2_email = None
    oauth2_token = None
    if settings.imap_server.strip().lower() == "imap.gmail.com":
        cred = get_oauth2_credential(db, settings.imap_username)
        if cred:
            tokens = get_decrypted_credential(db, settings.imap_username)
            if tokens:
                access_token, refresh_token = tokens
                if is_token_expired(cred.token_expiry):
                    if not app_settings.google_client_secrets_json:
                        raise HTTPException(
                            status_code=500,
                            detail="Google OAuth2 client secrets not configured.",
                        )
                    client_secrets = _json.loads(app_settings.google_client_secrets_json)
                    new_access, _ = refresh_access_token(client_secrets, refresh_token)
                    access_token = new_access
                oauth2_email = settings.imap_username
                oauth2_token = access_token

    is_successful, message = _test_imap_connection(
        server=settings.imap_server,
        username=settings.imap_username,
        password=settings.imap_password,
        oauth2_email=oauth2_email,
        oauth2_token=oauth2_token,
    )

    if not is_successful:
        logger.warning(f"IMAP connection test failed: {message}")
        raise HTTPException(status_code=400, detail=message)

    logger.info("IMAP connection test successful")
    return {"message": message}


@router.get("/imap/folders", response_model=List[str])
def read_folders(db: Session = Depends(get_db)):
    """Retrieve a list of IMAP folders from the configured server."""
    logger.info("Request to fetch IMAP folders")
    settings = get_settings(db, with_password=True)
    if not settings:
        logger.error("IMAP settings not found, cannot fetch folders")
        raise HTTPException(status_code=404, detail="IMAP settings not found")

    # Prefer OAuth2 for Gmail when available
    oauth2_email = None
    oauth2_token = None
    if settings.imap_server.strip().lower() == "imap.gmail.com":
        cred = get_oauth2_credential(db, settings.imap_username)
        if cred:
            tokens = get_decrypted_credential(db, settings.imap_username)
            if tokens:
                access_token, refresh_token = tokens
                if is_token_expired(cred.token_expiry):
                    if not app_settings.google_client_secrets_json:
                        raise HTTPException(
                            status_code=500,
                            detail="Google OAuth2 client secrets not configured.",
                        )
                    client_secrets = _json.loads(app_settings.google_client_secrets_json)
                    new_access, _ = refresh_access_token(client_secrets, refresh_token)
                    access_token = new_access
                oauth2_email = settings.imap_username
                oauth2_token = access_token

    folders = get_folders(
        server=settings.imap_server,
        username=settings.imap_username,
        password=settings.imap_password,
        oauth2_email=oauth2_email,
        oauth2_token=oauth2_token,
    )

    logger.info(f"Found {len(folders)} IMAP folders")
    return folders


@router.post("/imap/process")
def trigger_email_processing(db: Session = Depends(get_db)):
    """Trigger the email processing manually."""
    logger.info("Request to manually trigger email processing")
    try:
        process_emails(db)
        return {"message": "Email processing triggered successfully."}
    except Exception as e:
        logger.error(f"Error triggering email processing: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
