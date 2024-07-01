from sqlalchemy import Column, Integer, String, Float
from parser.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    employer = Column(String, index=True)
    area = Column(String, index=True)
    salary = Column(Float, index=True, nullable=True)
    url = Column(String, index=True)
