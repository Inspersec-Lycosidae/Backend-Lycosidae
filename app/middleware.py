# middleware.py
# Functions that are ran before the calling of my authenticated routes, for veryfying the
# session token and extracting its info for use in the routes functions
from fastapi import Request, HTTPException, Depends
from datetime import datetime, timedelta, timezone
from app.schemas import AuthToken
from app.logger import get_logger
from typing import Dict
import jwt
import os
import dotenv

# Logger configuration
logger = get_logger(__name__)
dotenv.load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

if not JWT_SECRET:
    logger.error("Environment variable JWT_SECRET is not set")
    raise RuntimeError("Environment variable JWT_SECRET is not set.")

# JWT_EXPIRATION is given in seconds as by JWT standard (Unix timestamp (int)
JWT_EXPIRATION = os.getenv("JWT_EXPIRATION") 

if not JWT_EXPIRATION:
    JWT_EXPIRATION = 1800
    logger.info(f"JWT_EXPIRATION not set, using default: {JWT_EXPIRATION} seconds")
elif type(JWT_EXPIRATION) == str:
    try:
        JWT_EXPIRATION = int(JWT_EXPIRATION)
        logger.info(f"JWT_EXPIRATION configured: {JWT_EXPIRATION} seconds")
    except:
        logger.error("Environment variable JWT_EXPIRATION is not properly set")
        raise RuntimeError("Environment variable JWT_EXPIRATION is not properly set.")

# Sets the defaults for cookie-reading and veryfing; mutable depending on the application
ALGORITHM = "HS256"
COOKIE_NAME = "session_token"

######################################################
### Helper Function to extract token from a Bearer ###
######################################################

def extract_token(request: Request) -> str:
    """

    Extract JWT from cookie or Authorization header
    Input: http/https request
    Output: String of the token

    """
    logger.debug("Attempting to extract token from request")
    # First try cookie
    token = request.cookies.get(COOKIE_NAME)
    if token:
        logger.debug("Token found in cookie")
        return token

    #Try Authorization header
    auth_header = request.headers.get("Authorization")
    if auth_header:
        if auth_header.lower().startswith("bearer "):
            logger.debug("Token found in Authorization header")
            return auth_header[7:].strip()
    
    logger.warning("No valid token found in request")
    raise HTTPException(status_code=401, detail="User not authenticated")

def get_cookie_as_dict(request: Request) -> Dict:
    """

    Receives a http/https request and returns the session_token JWT as a Python Dictionary
    Input: http/https request
    Output: Python Dict object

    """
    token = extract_token(request)

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        logger.debug(f"Token decoded successfully for user: {payload.get('username', 'unknown')}")
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        logger.warning("Invalid token provided")
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_cookie_as_model(request: Request) -> AuthToken:
    """
    
    Receives a http/https request and returns the session_token JWT as a AuthToken object
    Input: http/https request
    Output: AuthToken object
    
    """
    payload = get_cookie_as_dict(request)
    try:
        auth_token = AuthToken(**payload)
        logger.debug(f"AuthToken model created successfully for user: {auth_token.username}")
        return auth_token
    except Exception as e:
        logger.error(f"Failed to create AuthToken model: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or malformed token")
    
def make_cookie_from_dict(payload: Dict) -> str:
    """
    
    Receives a python dictionary and returns a valid JWT token string
    Input: Python Dictionary
    Output: JWT String
    
    """
    payload = payload.copy()
    logger.debug(f"Creating JWT token for user: {payload.get('username', 'unknown')}")

    expire = datetime.now(timezone.utc) + timedelta(seconds=JWT_EXPIRATION)
    payload["exp"] = int(expire.timestamp())

    try:
        token = jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
        logger.debug("JWT token created successfully")
        return token
    except Exception as e:
        logger.error(f"Error generating JWT token: {str(e)}")
        raise RuntimeError(f"Error generating token: {e}")
    
def make_cookie_from_model(auth_token: AuthToken) -> str:
    """
    
    Receives a AuthToken object and returns a valid JWT token string
    Input: AuthToken Object
    Output: JWT String
    
    """
    logger.debug(f"Creating JWT token from AuthToken model for user: {auth_token.username}")
    payload = auth_token.model_dump(exclude_none=True)
    return make_cookie_from_dict(payload)

def get_current_user(auth: AuthToken = Depends(get_cookie_as_model)) -> AuthToken:
    """

    Dependency: return the current authenticated user payload.
    Can be used in protected routes as:
    
        @router.get("/me")
        async def me(current_user: AuthToken = Depends(get_current_user)):
            return current_user
    
    """
    return auth