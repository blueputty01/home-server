"""Encryption utilities for sensitive credentials like OAuth2 tokens."""

from cryptography.fernet import Fernet
from app.core.config import settings


def get_cipher() -> Fernet:
    """Get the Fernet cipher for encryption/decryption.

    Uses the LETTERFEED_ENCRYPTION_KEY from settings. In development, a
    generated key is used if none is provided.
    """
    key = settings.encryption_key.encode() if isinstance(settings.encryption_key, str) else settings.encryption_key
    return Fernet(key)


def encrypt_token(token: str) -> str:
    """Encrypt a token string.
    
    Args:
        token: The plaintext token to encrypt.
        
    Returns:
        The encrypted token as a string.
    """
    cipher = get_cipher()
    return cipher.encrypt(token.encode()).decode()


def decrypt_token(encrypted_token: str) -> str:
    """Decrypt an encrypted token string.
    
    Args:
        encrypted_token: The encrypted token string.
        
    Returns:
        The decrypted plaintext token.
        
    Raises:
        cryptography.fernet.InvalidToken: If decryption fails.
    """
    cipher = get_cipher()
    return cipher.decrypt(encrypted_token.encode()).decode()
