from pydantic import BaseModel, EmailStr
from typing import Optional

class AuthToken(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str