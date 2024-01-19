from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from ..models.application import Application
from ..schemas.application import ApplicationCreate, ApplicationUpdate
from ..utils.utilities import logger_setup
from typing import List, Type

logger = logger_setup(__name__)


def handle_db_error(error: Exception):
    logger.error(f'Database error: {error}')
    raise HTTPException(status_code=500, detail='Internal server error')


def get_application_by_id(db: Session, application_id: int) -> Type[Application]:
    try:
        application = db.query(Application).filter(Application.id == application_id).first()
        if application is None:
            logger.info(f'Application with id {application_id} not found')
            raise HTTPException(status_code=404, detail='Application not found')
        return application
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving application with id: {application_id}: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def get_all_applications(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(Application).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving all applications: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def create_application(db: Session, application_data: ApplicationCreate, user_id: int) -> Application:
    try:
        new_application = Application(**application_data.dict(), applicant_id=user_id)
        db.add(new_application)
        db.commit()
        db.refresh(new_application)
        logger.info(f'Created new application with ID: {new_application.id}')
        return new_application
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error creating application: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def update_application(db: Session, application_id: int, update_data: ApplicationUpdate) -> Type[Application]:
    try:
        application_to_update = get_application_by_id(db, application_id)
        if not application_to_update:
            raise HTTPException(status_code=404, detail='Application not found')

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(application_to_update, key, value)
        db.commit()
        db.refresh(application_to_update)
        logger.info(f'Updated application with ID: {application_id}')
        return application_to_update

    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error updating application with ID: {application_id}: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def delete_application(db: Session, application_id: int):
    try:
        application_to_delete = get_application_by_id(db, application_id)
        if not application_to_delete:
            raise HTTPException(status_code=404, detail='Application not found')

        db.delete(application_to_delete)
        db.commit()
        logger.info(f'Deleted application with ID: {application_id}')

    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error deleting application with ID: {application_id}: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def get_applications_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    try:
        return db.query(Application).filter(Application.applicant_id == user_id).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving applications by user with ID: {user_id}: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')
