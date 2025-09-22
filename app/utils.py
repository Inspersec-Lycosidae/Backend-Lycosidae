# utils.py
import hashlib
import os
import dotenv

dotenv.load_dotenv()
PASS_SALT = os.getenv("PASS_SALT")
if not PASS_SALT:
    raise ValueError("Environment variable PASS_SALT is not set.")

def pass_hasher(password: str) -> str:
    """

    Hash a password using SHA256 + SALT.

    Args:
        password (str): Plain text password.
    Returns:
        str: Hashed password.

    """
    hasher = hashlib.sha256()
    hasher.update((password + PASS_SALT).encode("utf-8"))
    return hasher.hexdigest()
