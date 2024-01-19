from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from typing import List
from app.schemas.application import Application, ApplicationCreate, ApplicationUpdate
from app.services.application_service import (
    get_application_by_id, get_all_applications, create_application, update_application, delete_application
)
from ..dependencies import get_db, get_current_active_user
from ..utils.utilities import logger_setup

router = APIRouter()


logger = logger_setup(__name__)


@router.get("/", response_model=List[Application])
def read_applications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        applications = get_all_applications(db, skip=skip, limit=limit)
        return applications
    except HTTPException as e:
        logger.error(f"Error reading applications: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in read_applications: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{application_id}", response_model=Application)
def read_application(application_id: int, db: Session = Depends(get_db)):
    try:
        application = get_application_by_id(db, application_id)
        if application is None:
            logger.info(f"Application with id {application_id} not found")
            raise HTTPException(status_code=404, detail="Application not found")
        return application
    except HTTPException as e:
        logger.error(f"Error reading application by ID: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in read_application: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=Application)
def create_new_application(application: ApplicationCreate, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_active_user)):
    try:
        new_application = create_application(db, application, current_user.id)
        return new_application
    except HTTPException as e:
        logger.error(f"Error creating application: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_new_application: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{application_id}", response_model=Application)
def update_application_details(application_id: int, application: ApplicationUpdate, db: Session = Depends(get_db)):
    try:
        updated_application = update_application(db, application_id, application)
        return updated_application
    except HTTPException as e:
        logger.error(f"Error updating application: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in update_application_details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{application_id}")
def remove_application(application_id: int, db: Session = Depends(get_db)):
    try:
        delete_application(db, application_id)
        return {"message": "Application deleted successfully"}
    except HTTPException as e:
        logger.error(f"Error deleting application: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in remove_application: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
