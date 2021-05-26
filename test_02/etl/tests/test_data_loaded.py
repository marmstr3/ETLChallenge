import sqlalchemy
import pandas as pd
import pytest
from test_02.etl.load import DataLoader
from test_02.etl.fhir import FHIRDataTransformer


class TestDataLoading(object):

    @pytest.fixture(scope="session", autouse=True)
    def setup_once(self):
        # Setup the database
        pass

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

