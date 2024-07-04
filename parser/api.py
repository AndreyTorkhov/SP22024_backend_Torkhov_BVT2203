from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/jobs/accredited/", response_model=List[schemas.Job])
def get_accredited_jobs(accredited: bool, db: Session = Depends(get_db)):
    jobs = crud.get_accredited_jobs(db, accredited)
    return jobs

@app.get("/jobs/filter/", response_model=List[schemas.Job])
def filter_jobs(employers: Optional[List[str]] = Query(None), db: Session = Depends(get_db)):
    jobs = crud.filter_jobs(db, employers=employers)
    return jobs

@app.get("/jobs/schedule/", response_model=List[schemas.Job])
def get_jobs_by_schedule(schedule_names: Optional[List[str]] = Query(None), db: Session = Depends(get_db)):
    jobs = crud.get_jobs_by_schedules(db, schedule_names)
    return jobs

@app.get("/jobs/sort/", response_model=List[schemas.Job])
def sort_jobs_by_id(db: Session = Depends(get_db)):
    jobs = crud.sort_jobs_by_id(db)
    return jobs

@app.get("/jobs/employers/", response_model=List[str])
def get_unique_employers(db: Session = Depends(get_db)):
    employers = crud.get_unique_employers(db)
    return employers

@app.get("/jobs/schedules/", response_model=List[str])
def get_unique_schedules(db: Session = Depends(get_db)):
    schedules = crud.get_unique_schedules(db)
    return schedules
