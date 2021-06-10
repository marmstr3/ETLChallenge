import sqlalchemy
import pandas as pd
import pytest
from datetime import date, time, datetime
from test_02.etl.load import DataLoader
from test_02.etl.fhir import FHIRDataTransformer
from test_02.etl.crud import setup_database, add_patient_discharge, get_first_patient_discharge, get_record_by_MRN
from test_02.etl.models import PatientDischarges
from carta_interview import Datasets, get_data_file



class TestDataLoading(object):

    @pytest.fixture(scope="session", autouse=True)
    def setup_once(self):
        # Setup the database
        setup_database()

    def test_data_loaded(self):
        # Given
        ## Setup
        loader = DataLoader()
        transformer = FHIRDataTransformer()

        # When
        loader.load_data()
        patients = transformer.get_patient_resources()
        encounters = transformer.get_encounter_resources()

        # Then
        assert len(patients) == 4
        assert len(encounters) == 4
        names = set()
        for patient in patients:
            for name in patient["name"]:
                names.add((name["given"], name["family"]))
        
        assert ("John", "Doe") in names
        # add additional assertions (optional)

    def test_load_data(self):

        # First Record
        first_record = get_first_patient_discharge()
        assert first_record.MRN == "001"
        assert first_record.encounter_id == "1234"
        assert first_record.first_name == "John"
        assert first_record.last_name == "Doe"
        assert first_record.birth_date == date(year=1999, month=1, day=2)
        assert first_record.admission_dt == datetime(year=2002, month=4, day=12, hour=17, minute=0)
        assert first_record.discharge_dt == datetime(year=2002, month=4, day=13, hour=22, minute=0)
        assert first_record.update_dt == datetime(year=2002, month=4, day=24, hour=6, minute=0)        

        # Records With Conflicts
        conflict_record = get_record_by_MRN("002")
        assert conflict_record.MRN == "002"
        assert conflict_record.first_name == "Cosmia"

        conflict_record = get_record_by_MRN("003")
        assert conflict_record.MRN == "003"
        assert conflict_record.update_dt == datetime(year=2002, month=5, day=17, hour=6, minute=0)

    def test_add_patient_discharage(self):

        setup_database()
        new_discharge = PatientDischarges(MRN="001",
                                          encounter_id="1234",
                                          first_name="John",
                                          last_name="Doe",
                                          birth_date=date(year=2000, month=1, day=1),
                                          admission_dt=datetime(year=2021, month=1, day=1, hour=12, minute=21),
                                          discharge_dt=datetime(year=2021, month=1, day=2, hour=13, minute=0),
                                          update_dt=datetime(year=2021, month=1, day=3, hour=8, minute=30)
                                          )
        add_patient_discharge(new_discharge)

        retrieved_discharge = get_first_patient_discharge()
        assert retrieved_discharge.MRN == "001"
        assert retrieved_discharge.encounter_id == "1234"
        assert retrieved_discharge.first_name == "John"
        assert retrieved_discharge.last_name == "Doe"
        assert retrieved_discharge.birth_date == date(year=2000, month=1, day=1)
        assert retrieved_discharge.admission_dt == datetime(year=2021, month=1, day=1, hour=12, minute=21)
        assert retrieved_discharge.discharge_dt == datetime(year=2021, month=1, day=2, hour=13, minute=0)
        assert retrieved_discharge.update_dt == datetime(year=2021, month=1, day=3, hour=8, minute=30)
        


class TestLoadMethods(object):

    def test_import_excel_file(self):
        loader = DataLoader()
        test_dataframe = loader.import_excel_file(get_data_file(Datasets.PATIENT_EXTRACT1))

        # Test Dataframe Structure
        assert test_dataframe is not None
        assert list(test_dataframe) ==  ['MRN', 'Encounter ID', 'First Name', 'Last Name', 'Birth Date', 'Admission D/T', 'Discharge D/T', 'Update D/T']
        assert test_dataframe.shape[0] == 3

        # Test First Entry
        assert list(test_dataframe.iloc[0]) == ['001', '1234', 'John', 'Doe', '01/02/1999', '04/12/2002 5:00 PM', '04/13/2002 10:00 PM', '04/24/2002 6:00 AM']

        # Test Final Entry
        assert list(test_dataframe.iloc[-1]) == ['003', '3456', 'Annabelle', 'Jones', '01/02/2001', '04/21/2002 5:00 PM', '04/23/2002 2:53 AM', '04/24/2002 6:00 AM']


class TestDateTimeMethods(object):
    loader = DataLoader()

    def test_get_time_from_string_2_digit_hour_am(self):
        
        test_time = self.loader.get_time_from_string("10:21 AM")
        assert test_time == time(hour=10, minute=21)

    def test_get_time_from_string_1_digit_hour_am(self):
        
        test_time = self.loader.get_time_from_string("5:21 AM")
        assert test_time == time(hour=5, minute=21)

    def test_get_time_from_string_2_digit_hour_pm(self):

        test_time = self.loader.get_time_from_string("10:21 PM")
        assert test_time == time(hour=22, minute=21)

    def test_get_time_from_string_1_digit_hour_pm(self):
        
        test_time = self.loader.get_time_from_string("5:21 PM")
        assert test_time == time(hour=17, minute=21)
    
    def test_get_date_from_string(self):

        test_date = self.loader.get_date_from_string("04/13/2002")
        assert test_date == date(year=2002, month=4, day=13)

    def test_get_datetime_from_string(self):

        test_datetime = self.loader.get_datetime_from_string("04/13/2002 10:00 PM")
        assert test_datetime == datetime(year=2002,
                                        month=4,
                                        day=13,
                                        hour=22,
                                        minute=0
                                        )


class TestFhirMethod(object):

    # Create Database for Test
    setup_database()

    loader = DataLoader()
    loader.load_data()

    transformer = FHIRDataTransformer()
    
    def test_get_patient_resource(self):

        sample_discharge = get_first_patient_discharge()
        test_resource = self.transformer.create_patient_resource(sample_discharge)

        assert test_resource['identifier'] == {"system": "MRN",
                                              "value": sample_discharge.MRN
                                              }
        assert test_resource['name'] == [{"given": sample_discharge.first_name,
                                         "family": sample_discharge.last_name
                                         }]
        assert test_resource['gender'] == "unknown"
        assert test_resource['telecom'] == []
        assert test_resource['birthdate'] == sample_discharge.birth_date
        assert test_resource['address'] == []
        assert test_resource['language'] == []
        assert test_resource['race'] == None
        assert test_resource['ethnicity'] == None
        assert test_resource['birth sex'] == None

    def test_get_encounter_resource(self):

        sample_discharge = get_first_patient_discharge()
        test_resource = self.transformer.create_encounter_resource(sample_discharge)

        assert test_resource['status'] == "finished"
        assert test_resource['classification'] == "unknown"
        assert test_resource['type'] == "unknown"
        assert test_resource['patient'] == sample_discharge.MRN
        assert test_resource['identifier'] == sample_discharge.encounter_id
        assert test_resource['providers'] == []
        assert test_resource['period'] == {"start": sample_discharge.admission_dt,
                                           "end": sample_discharge.discharge_dt
                                           }
        assert test_resource['reason'] == None
        assert test_resource['discharge disposition'] == None
        assert test_resource['where'] == None



