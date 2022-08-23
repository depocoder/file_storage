"""Cryptogrphy module."""
import hashlib
import hmac

from file_storage.settings import settings


def hash_password(password: str, password_salt: str) -> str:
    """Sign password."""
    return hashlib.sha256(f"{password};{password_salt}".encode()).hexdigest().lower()


def sign_cookie(cookie: str) -> str:
    """Sign cookie."""
    return (
        hmac.new(
            settings.secret_key.encode(),
            msg=cookie.encode(),
            digestmod=hashlib.sha256,
        )
        .hexdigest()
        .upper()
    )
