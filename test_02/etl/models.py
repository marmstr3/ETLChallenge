from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date

Base = declarative_base()

class PatientDischarges(Base):
    __tablename__ = "PatientData"
    id = Column(Integer, primary_key=True)
    MRN = Column(String)
    encounter_id = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)
    admission_dt = Column(DateTime)
    discharge_dt = Column(DateTime)
    update_dt = Column(DateTime)