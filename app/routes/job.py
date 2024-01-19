from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..schemas.job import Job, JobCreate, JobUpdate
from ..services.job_service import get_job_by_id, get_all_jobs, create_job, update_job, delete_job
from ..dependencies import get_db
from ..utils.utilities import logger_setup

router = APIRouter()

# Initialize logger
logger = logger_setup(__name__)


@router.get("/", response_model=List[Job])
def read_jobs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        jobs = get_all_jobs(db, skip=skip, limit=limit)
        return jobs
    except HTTPException as e:
        logger.error(f"Error reading jobs: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in read_jobs: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{job_id}", response_model=Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    try:
        db_job = get_job_by_id(db, job_id)
        if db_job is None:
            logger.info(f"Job with id {job_id} not found")
            raise HTTPException(status_code=404, detail="Job not found")
        return db_job
    except HTTPException as e:
        logger.error(f"Error reading job by ID: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in read_job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/", response_model=Job)
def create_new_job(job: JobCreate, db: Session = Depends(get_db)):
    try:
        new_job = create_job(db, job)
        return new_job
    except HTTPException as e:
        logger.error(f"Error creating job: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in create_new_job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{job_id}", response_model=Job)
def update_job_details(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    try:
        updated_job = update_job(db, job_id, job)
        return updated_job
    except HTTPException as e:
        logger.error(f"Error updating job: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in update_job_details: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{job_id}")
def remove_job(job_id: int, db: Session = Depends(get_db)):
    try:
        delete_job(db, job_id)
        return {"message": "Job deleted successfully"}
    except HTTPException as e:
        logger.error(f"Error deleting job: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in remove_job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
