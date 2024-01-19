from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from .user_service import get_user_by_username
from ..models.user import User
from ..schemas.user import UserInDB
from ..utils.utilities import logger_setup, get_key

# Logger setup
logger = logger_setup(__name__)

# Configuration for JWT
SECRET_KEY = get_key("SECRET_KEY")
ALGORITHM = get_key("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_key("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Configuration for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> Optional[User]:
    try:
        user = get_user_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            logger.warning(f"Authentication failed for user: {username}")
            return None
        return user
    except Exception as e:
        logger.error(f"Error in authenticate_user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError as e:
        logger.error(f"JWT Encoding error: {e}")
        raise HTTPException(status_code=500, detail="Error creating access token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user
    except JWTError as e:
        logger.warning(f"JWT decoding error: {e}")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {e}")
        raise credentials_exception
