from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.user import User, UserCreate, UserUpdate
from ..services.user_service import get_user_by_id, get_all_users, create_user, update_user, delete_user
from ..dependencies import get_db, get_current_active_user
from ..utils.utilities import logger_setup

router = APIRouter()

# Initialize logger
logger = logger_setup(__name__)


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        users = get_all_users(db, skip=skip, limit=limit)
        return users
    except HTTPException as e:
        logger.error(f"Error reading users: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in read_users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        db_user = get_user_by_id(db, user_id)
        if db_user is None:
            logger.info(f"User with id {user_id} not found")
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except HTTPException as e:
        logger.error(f"Error reading user by ID: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in read_user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db, user)
        return new_user
    except HTTPException as e:
        logger.error(f"Error creating user: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_new_user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{user_id}", response_model=User)
def update_user_details(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    try:
        updated_user = update_user(db, user_id, user)
        return updated_user
    except HTTPException as e:
        logger.error(f"Error updating user: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in update_user_details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    try:
        delete_user(db, user_id)
        return {"message": "User deleted successfully"}
    except HTTPException as e:
        logger.error(f"Error deleting user: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in remove_user: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
