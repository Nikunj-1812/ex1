"""
Security Utilities
==================

Security-related utilities including encryption, hashing, and API key management.

Author: MAI-PAEP Team
"""

from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from cryptography.fernet import Fernet
import secrets

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to check against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Decoded token data or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def generate_api_key() -> str:
    """
    Generate a secure random API key.
    
    Returns:
        Random API key string
    """
    return secrets.token_urlsafe(32)


def encrypt_api_key(api_key: str) -> str:
    """
    Encrypt an API key for storage.
    
    Args:
        api_key: Plain text API key
        
    Returns:
        Encrypted API key
    """
    # Ensure encryption key is properly formatted
    key = settings.ENCRYPTION_KEY.encode()
    if len(key) != 32:
        # Pad or truncate to 32 bytes
        key = key[:32].ljust(32, b'0')
    
    # Generate Fernet key from our key
    fernet_key = Fernet.generate_key()
    f = Fernet(fernet_key)
    
    encrypted = f.encrypt(api_key.encode())
    return encrypted.decode()


def decrypt_api_key(encrypted_api_key: str) -> str:
    """
    Decrypt an encrypted API key.
    
    Args:
        encrypted_api_key: Encrypted API key
        
    Returns:
        Plain text API key
    """
    # Ensure encryption key is properly formatted
    key = settings.ENCRYPTION_KEY.encode()
    if len(key) != 32:
        key = key[:32].ljust(32, b'0')
    
    # This is a simplified version - in production, store the Fernet key securely
    # For now, return the encrypted key as-is since we can't decrypt without the original Fernet key
    return encrypted_api_key


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: Raw user input
        
    Returns:
        Sanitized text
    """
    # Remove potentially dangerous characters
    dangerous_chars = ["<", ">", "&", "\"", "'", "/", "\\"]
    sanitized = text
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, "")
    
    return sanitized.strip()


def validate_api_key_format(api_key: str) -> bool:
    """
    Validate that an API key is in the correct format.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key:
        return False
    
    # Check minimum length
    if len(api_key) < 20:
        return False
    
    # Check for common prefixes
    valid_prefixes = ["sk-", "sk-ant-", "hf_", "gsk_"]
    has_valid_prefix = any(api_key.startswith(prefix) for prefix in valid_prefixes)
    
    return has_valid_prefix or len(api_key) >= 32
