from test_02.etl.crud import get_all_records

class FHIRDataTransformer(object):
    """Transform data in postgres into Patient/Encounter resources"""

    def get_patient_resources(self):
        ## Query data in postgres, produce array of Patient FHIR resources
        # NOTE: By FHIR R4, patient resources must have a gender. However, the 
        # provided data included no gender information. So patient resources 
        # will be created with a gender field set equal to "unknown"

        discharges = get_all_records()
        patient_resources = []
        for discharge in discharges:
            patient_resources.append(self.create_patient_resource(discharge))

        return patient_resources

    def get_encounter_resources(self):
        ## Query data in postgres, produce array of Encounter FHIR resources
        # NOTE: By FHIR R4, encounter resources must have a classification and
        # encounter type. This information was not included in the provided
        # data, so all will be set to "unknown".
        # NOTE: Since all records have a discharge date, all statuses will be
        # set to "finished".

        discharges = get_all_records()
        encounter_resources = []
        for discharge in discharges:
            encounter_resources.append(self.create_encounter_resource(discharge))

        return encounter_resources 

    def create_patient_resource(self, discharge):
        """Creates an FHIR R4 Patient Resource from a discharge record.

        Args:
            discharge (PatientDischarges): A record of a patient being
            discharged.

        Returns:
            dict: Patient Resource conforming to FHIR R4.
        """
        identifier = {"system": "MRN", "value": discharge.MRN}
        name = [{"given": discharge.first_name,
                 "family": discharge.last_name
                 }]    

        patient_resource = {"identifier": identifier,
                            "name": name,
                            "gender": "unknown",
                            "telecom": [],
                            "birthdate": discharge.birth_date,
                            "address": [],
                            "language": [],
                            "race": None,
                            "ethnicity": None,
                            "birth sex": None
                            }

        return patient_resource

    def create_encounter_resource(self, discharge):
        """Creates an FHIR R4 Encounter Resource from a discharge record.

        Args:
            discharge (PatientDischarges): A record of a patient being
            discharged.

        Returns:
            dict: Encounter Resource conforming to FHIR R4.
        """
        period = {"start": discharge.admission_dt,
                  "end": discharge.discharge_dt
                  }
        encounter_resource = {"status": "finished",
                              "classification": "unknown",
                              "type": "unknown",
                              "patient": discharge.MRN,
                              "identifier": discharge.encounter_id,
                              "providers": [],
                              "period": period,
                              "reason": None,
                              "discharge disposition": None,
                              "where": None
                              }

        return encounter_resource