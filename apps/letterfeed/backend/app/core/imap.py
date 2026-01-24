"""IMAP utility functions for connecting to mail servers and fetching folders."""

import base64
import imaplib
from typing import Literal

from app.core.logging import get_logger

logger = get_logger(__name__)


def _create_oauth2_auth_string(email: str, access_token: str) -> str:
    """Create IMAP XOAUTH2 authentication string.
    
    Args:
        email: Gmail email address.
        access_token: OAuth2 access token.
        
    Returns:
        XOAUTH2 authentication string.
    """
    auth_string = f"user={email}\x01auth=Bearer {access_token}\x01\x01"
    return base64.b64encode(auth_string.encode()).decode()


def _test_imap_connection(
    server: str,
    username: str,
    password: str | None = None,
    oauth2_email: str | None = None,
    oauth2_token: str | None = None,
) -> tuple[bool, str]:
    """Test the IMAP connection with the given credentials.
    
    Supports both password-based and OAuth2 authentication.
    """
    logger.info(f"Testing IMAP connection to {server} for user {username}")
    try:
        mail = imaplib.IMAP4_SSL(server)
        
        if oauth2_email and oauth2_token:
            # OAuth2 authentication
            auth_string = _create_oauth2_auth_string(oauth2_email, oauth2_token)
            mail.authenticate("XOAUTH2", lambda x: auth_string)
        else:
            # Password authentication
            mail.login(username, password)
        
        mail.logout()
        logger.info("IMAP connection successful")
        return True, "Connection successful"
    except Exception as e:
        logger.error(f"IMAP connection failed: {e}")
        return False, str(e)


def get_folders(
    server: str,
    username: str,
    password: str | None = None,
    oauth2_email: str | None = None,
    oauth2_token: str | None = None,
) -> list[str]:
    """Fetch a list of IMAP folders from the mail server.
    
    Supports both password-based and OAuth2 authentication.
    """
    logger.info(f"Fetching IMAP folders from {server} for user {username}")
    try:
        mail = imaplib.IMAP4_SSL(server)
        
        if oauth2_email and oauth2_token:
            # OAuth2 authentication
            auth_string = _create_oauth2_auth_string(oauth2_email, oauth2_token)
            mail.authenticate("XOAUTH2", lambda x: auth_string)
        else:
            # Password authentication
            mail.login(username, password)
        
        status, folders = mail.list()
        mail.logout()
        if status == "OK":
            folder_list = [
                folder.decode().split(' "/" ')[1].strip('"') for folder in folders
            ]
            logger.info(f"Found {len(folder_list)} folders")
            return folder_list
        logger.warning(f"Failed to list IMAP folders, status: {status}")
        return []
    except Exception as e:
        logger.error(f"Error fetching IMAP folders: {e}")
        return []
