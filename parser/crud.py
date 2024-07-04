import logging
from sqlalchemy.orm import Session
from sqlalchemy import not_
from . import models, schemas
from .models import Job
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    logger.info("Fetching jobs from database")
    jobs = db.query(Job).offset(skip).limit(limit).all()
    jobs = sanitize_jobs(jobs)
    logger.info(f"Retrieved jobs: {jobs}")
    return jobs

def filter_jobs(db: Session, employers: list[str] = None):
    query = db.query(Job)

    if employers:
        query = query.filter(Job.employer.in_(employers))

    jobs = query.all()
    jobs = sanitize_jobs(jobs)
    logger.info(f"Filtered jobs: {jobs}")
    return jobs

def get_jobs_with_salary(db: Session):
    jobs = db.query(Job).filter(Job.salary.isnot(None), ~Job.salary.in_([float('NaN'), float('-inf'), float('inf'), math.nan]))
    jobs = sanitize_jobs(jobs)
    logger.info(f"Jobs with salary: {jobs}")
    return jobs

def sort_jobs_by_id(db: Session):
    jobs = db.query(Job).order_by(Job.id).all()
    jobs = sanitize_jobs(jobs)
    logger.info(f"Sorted jobs by ID: {jobs}")
    return jobs

def get_unique_employers(db: Session):
    employers = db.query(Job.employer).distinct().all()
    unique_employers = [employer[0] for employer in employers]
    logger.info(f"Unique employers: {unique_employers}")
    return unique_employers

def sanitize_jobs(jobs):
    for job in jobs:
        if job.salary is not None and (job.salary == float('inf') or job.salary == float('-inf') or job.salary != job.salary):
            job.salary = None
    return jobs

def get_accredited_jobs(db: Session, accredited: bool):
    jobs = db.query(Job).filter(Job.accredited_it_employer == accredited).all()
    jobs = sanitize_jobs(jobs)
    logger.info(f"Accredited jobs: {jobs}")
    return jobs

def get_jobs_by_schedules(db: Session, schedule_names: list[str] = None):
    query = db.query(Job)

    if schedule_names:
        query = query.filter(Job.schedule_name.in_(schedule_names))

    jobs = query.all()
    jobs = sanitize_jobs(jobs)
    logger.info(f"Jobs by schedules: {jobs}")
    return jobs

def get_unique_schedules(db: Session):
    schedules = db.query(Job.schedule_name).distinct().all()
    unique_schedules = [schedule[0] for schedule in schedules]
    logger.info(f"Unique schedules: {unique_schedules}")
    return unique_schedules
