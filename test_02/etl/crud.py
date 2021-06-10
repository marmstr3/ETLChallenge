import sqlalchemy
from sqlalchemy.orm import sessionmaker
from test_02.etl.models import Base, PatientDischarges

# Global Scope
DATABASE_URI = "postgres+psycopg2://:@localhost:5432"
engine = sqlalchemy.create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Create Functions
def setup_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def add_patient_discharge(patient_discharge_entry):
    s = Session()
    s.add(patient_discharge_entry)
    s.commit()
    s.close()

# Read Functions
def get_first_patient_discharge():
    s = Session()
    first_patient_discharge = s.query(PatientDischarges).first()
    s.close()

    return first_patient_discharge

def get_record_by_MRN(target_MRN):
    s = Session()
    target_patient_discharge = s.query(PatientDischarges).filter_by(MRN=target_MRN).first()
    s.close()

    return target_patient_discharge

def get_all_records():
    s = Session()
    patient_discharges = s.query(PatientDischarges).all()
    s.close()

    return patient_discharges

# Update Functions

# Delete Functions