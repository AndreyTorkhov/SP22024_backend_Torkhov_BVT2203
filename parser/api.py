from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/jobs/", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs

@app.get("/jobs/salary/", response_model=List[schemas.Job])
def get_jobs_with_salary(db: Session = Depends(get_db)):
    jobs = crud.get_jobs_with_salary(db)
    return jobs

@app.get("/jobs/filter/", response_model=List[schemas.Job])
def filter_jobs(employers: List[str] = Query(None), db: Session = Depends(get_db)):
    if employers:
        employers = [employer.strip() for employer in employers if employer.strip()]
    jobs = crud.filter_jobs(db, employers=employers)
    return jobs

@app.get("/jobs/sort/", response_model=List[schemas.Job])
def sort_jobs_by_id(db: Session = Depends(get_db)):
    jobs = crud.sort_jobs_by_id(db)
    return jobs

@app.get("/jobs/employers/", response_model=List[str])
def get_unique_employers(db: Session = Depends(get_db)):
    employers = crud.get_unique_employers(db)
    return employers
