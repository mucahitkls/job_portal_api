from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserInDB
from .auth_service import get_password_hash
from ..utils.utilities import logger_setup
from typing import List, Type

logger = logger_setup(__name__)


def handle_db_error(error: Exception):
    logger.error(f'Database error: {error}')
    raise HTTPException(status_code=500, detail='Internal server error')


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[Type[User]]:
    try:
        return db.query(User).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving all users: {e}')


def get_user_by_id(db: Session, user_id: int) -> User:
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            logger.info(f'User with id {user_id} not found')
            raise HTTPException(status_code=404, detail='User not found')
        return user
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving user with id: {user_id}: error: {e}')


def get_user_by_username(db: Session, username: str) -> Type[User]:
    try:
        return db.query(User).filter(User.username == username).first()
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving user with username: {username}: error: {e}')


def get_user_by_email(db: Session, email: str) -> Type[User]:
    try:
        return db.query(User).filter(User.email == email).first()
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving user with email: {email}: error: {e}')


def create_user(db: Session, user_data: UserCreate) -> UserInDB:
    try:
        existing_user = get_user_by_email(db, user_data.email)
        if existing_user:
            logger.warning(f'Attempt to create user with existing email: {user_data.email}')
            raise HTTPException(status_code=400, detail='Email already registered')

        hashed_password = get_password_hash(user_data.password)
        new_user = User(**user_data.dict(), hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f'Created new user with ID: {new_user.id}')
        return new_user
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error creating user with email: {user_data.email}: error: {e}')


def update_user(db: Session, user_id: int, update_data: UserUpdate) -> UserInDB:
    try:
        user_to_update = get_user_by_id(db, user_id)
        if not user_to_update:
            raise HTTPException(status_code=404, detail='User not found')

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(user_to_update, key, value if key != 'password' else get_password_hash(value))
        db.commit()
        db.refresh(user_to_update)
        logger.info(f'Updated user with ID: {user_id}')
        return user_to_update

    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error updating user with ID: {user_id}: error: {e}')


def delete_user(db: Session, user_id: int):
    try:
        user_to_delete = get_user_by_id(db, user_id)
        if not user_to_delete:
            raise HTTPException(status_code=404, detail='User not found')

        db.delete(user_to_delete)
        db.commit()
        logger.info(f'Deleted user with ID: {user_id}')

    except SQLAlchemyError as error:
        handle_db_error(error)

    except Exception as e:
        logger.error(f'Unexpected error deleting user with ID: {user_id}: error: {e}')
