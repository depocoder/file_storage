"""User utils."""
from file_storage.web.cryptography import hash_password


def verify_password(
    password: str,
    stored_hashed_password: str,
    password_salt: str,
) -> bool:
    """Verify paasword for user."""
    hashed_password = hash_password(password, password_salt)
    return stored_hashed_password == hashed_password
