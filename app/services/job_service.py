from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from ..models.job import Job
from ..schemas.job import JobCreate, JobUpdate
from ..utils.utilities import logger_setup

logger = logger_setup(__name__)


def handle_db_error(error: Exception):
    logger.error(f'Database error: {error}')
    raise HTTPException(status_code=500, detail='Internal server error')


def get_job_by_id(db: Session, job_id: int) -> Job:
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job is None:
            logger.info(f'Job with id {job_id} not found')
            raise HTTPException(status_code=404, detail='Job not found')
        return job
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving job with id: {job_id}: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def get_all_jobs(db: Session, skip: int = 0, limit: int = 10):
    try:
        return db.query(Job).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving all jobs: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def create_job(db: Session, job_data: JobCreate, employer_id: int) -> Job:
    try:
        new_job = Job(**job_data.dict(), employer_id=employer_id)
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        logger.info(f'Created new job with ID: {new_job.id}')
        return new_job
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error creating job: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def update_job(db: Session, job_id: int, update_data: JobUpdate) -> Job:
    try:
        job_to_update = get_job_by_id(db, job_id)
        if not job_to_update:
            raise HTTPException(status_code=404, detail='Job not found')

        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(job_to_update, key, value)
        db.commit()
        db.refresh(job_to_update)
        logger.info(f'Updated job with ID: {job_id}')
        return job_to_update

    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error updating job with ID: {job_id}: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def delete_job(db: Session, job_id: int):
    try:
        job_to_delete = get_job_by_id(db, job_id)
        if not job_to_delete:
            raise HTTPException(status_code=404, detail='Job not found')

        db.delete(job_to_delete)
        db.commit()
        logger.info(f'Deleted job with ID: {job_id}')

    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error deleting job with ID: {job_id}: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')


def get_jobs_by_employer(db: Session, employer_id: int, skip: int = 0, limit: int = 10):
    try:
        return db.query(Job).filter(Job.employer_id == employer_id).offset(skip).limit(limit).all()
    except SQLAlchemyError as error:
        handle_db_error(error)
    except Exception as e:
        logger.error(f'Unexpected error retrieving jobs by employer with ID: {employer_id}: error: {e}')
        raise HTTPException(status_code=500, detail='Unexpected error')
