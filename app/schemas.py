# schemas.py
from typing import Optional
from pydantic import BaseModel

#########################################################################
##### Uses pydantic for cache/dynamic objects; not referenced in DB #####
#########################################################################

#Base JWT AuthToken model
class AuthToken(BaseModel):
    """

    Schema for JWT payload used in authentication.

    Fields:
        id (int): User ID (maps to DB primary key).
        username (str): Username of the authenticated user.
        email (str): Email of the user.
        role (Optional[str]): Authorization role (e.g., "admin", "player", "student", ...).
        exp (Optional[int]): Expiration timestamp (Unix epoch).
    
    Notes:
        - `extra = "allow"` enables flexible extension of the JWT payload
          (e.g., "permissions", "debugged", etc.).
        - Be cautious: never trust unvalidated extra fields for security-critical logic.

    """
    id : int
    username : str
    email : str
    role : Optional[str] = None
    exp : Optional[int] = None

    # Allow any additional fields in JWT
    class Config:
        extra = "allow"

class UserCreateDTO(BaseModel):
    """

    Schema for registering a new user.

    Fields:
        username (str): Desired username, must be unique.
        email (str): Valid email address, must be unique.
        password (str): Plain text password (will be hashed before storing).

    """
    username: str
    email: str
    password: str

class UserLoginDTO(BaseModel):
    """

    Schema for user login requests.

    Fields:
        email (str): Registered email of the user.
        password (str): Plain text password for authentication.

    """
    email: str
    password: str

class UserReadDTO(BaseModel):
    """

    Schema for returning user info (safe response).

    Fields:
        id (int): Unique identifier of the user.
        username (str): Username of the user.
        email (str): Email address of the user.

    Notes:
        - Sensitive fields like password are never exposed in responses.

    """
    id: int
    username: str
    email: str

class UserUpdateDTO(BaseModel):
    """

    Schema for updating user profile information.

    Fields:
        username (Optional[str]): New username (must be unique).
        email (Optional[str]): New email (must be unique).
        password (Optional[str]): New password (will be hashed before storing).

    Notes:
        - All fields are optional; only provided fields will be updated.

    """
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None