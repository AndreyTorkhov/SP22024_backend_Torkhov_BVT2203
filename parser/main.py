import requests
import pandas as pd
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Job, Base

def fetch_hh_jobs():
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": "python developer",
        "area": "1",  # Moscow
        "per_page": 20
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        jobs = data['items']
        jobs_list = []
        for job in jobs:
            job_info = {
                "id": job["id"],
                "name": job["name"],
                "employer": job["employer"]["name"],
                "area": job["area"]["name"],
                "salary": job["salary"]["from"] if job["salary"] else None,
                "url": job["alternate_url"]
            }
            jobs_list.append(job_info)
        return pd.DataFrame(jobs_list)
    else:
        print("Failed to fetch jobs")
        return pd.DataFrame()

def load_jobs_to_db(jobs_df):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for index, row in jobs_df.iterrows():
            job = Job(
                id=row['id'],
                name=row['name'],
                employer=row['employer'],
                area=row['area'],
                salary=row['salary'],
                url=row['url']
            )
            db.merge(job)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    jobs_df = fetch_hh_jobs()
    if not jobs_df.empty:
        print(jobs_df.head())
        load_jobs_to_db(jobs_df)
        print("Data loaded to the database successfully.")
    else:
        print("No data fetched")
