from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..schemas.user import User, UserCreate
from ..schemas.token import Token  # Import the Token model
from ..services.auth_service import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..services.user_service import create_user
from ..dependencies import get_db
from ..utils.utilities import logger_setup

router = APIRouter()

# Initialize logger
logger = logger_setup(__name__)


@router.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            logger.warning(f"Failed login attempt for username: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        logger.error(f"Unexpected error in login_for_access_token: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/signup", response_model=User)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)
        return db_user
    except HTTPException as e:
        logger.error(f"Error in user signup: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_new_user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
