from pydantic import BaseModel
from typing import Optional

class JobBase(BaseModel):
    name: str
    employer: str
    area: Optional[str] = None
    salary: Optional[float] = None
    url: Optional[str] = None

class Job(JobBase):
    id: int

    class Config:
        orm_mode = True
