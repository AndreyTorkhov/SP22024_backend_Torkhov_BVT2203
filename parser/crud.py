import logging
from sqlalchemy.orm import Session
from . import models, schemas
from .models import Job

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_jobs(db: Session, skip: int = 0, limit: int = 10):
    logger.info("Fetching jobs from database")
    jobs = db.query(Job).offset(skip).limit(limit).all()
    logger.info(f"Retrieved jobs: {jobs}")

    # Проверка и замена недопустимых значений
    for job in jobs:
        if job.salary is not None and (
                job.salary == float('inf') or job.salary == float('-inf') or job.salary != job.salary):
            job.salary = None

    return jobs


def get_job(db: Session, job_id: int):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    logger.info(f"Retrieved job: {job}")
    if job.salary is not None and (
            job.salary == float('inf') or job.salary == float('-inf') or job.salary != job.salary):
        job.salary = None
    return job


def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(
        name=job.name,
        employer=job.employer,
        area=job.area,
        salary=job.salary,
        url=job.url
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    logger.info(f"Created job: {db_job}")
    return db_job
