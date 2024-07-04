from pydantic import BaseModel
from typing import Optional

class JobBase(BaseModel):
    name: str
    employer: str
    area: Optional[str] = None
    salary: Optional[float] = None
    url: Optional[str] = None
    schedule_name: Optional[str] = None
    accredited_it_employer: Optional[bool] = None

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True
