import pandas as pd
import numpy as np
from datetime import date, time, datetime
from carta_interview import Datasets, get_data_file
from test_02.etl.crud import add_patient_discharge
from test_02.etl.models import PatientDischarges

class DataLoader(object):
    """Load data into postgres"""

    def load_data(self):
        patient_extract1 = get_data_file(Datasets.PATIENT_EXTRACT1)
        patient_extract2 = get_data_file(Datasets.PATIENT_EXTRACT2)
        ## Implement load into postgres
        # Create Dataframes
        patient_discharges1 = self.import_excel_file(patient_extract1)
        patient_discharges2 = self.import_excel_file(patient_extract2)        

        patient_discharges = pd.concat([patient_discharges1, patient_discharges2]).drop_duplicates(subset='MRN', keep='last')

        patient_discharges.apply(lambda row: self.create_db_row(row), axis=1)
        

    def import_excel_file(self, target_file_path):
        """ Takes a filepath pointing to an excel file, imports the excel file as
        a pandas dataframe, and returns the dataframe representation.
        Args:
            target_file_path (string): Filepath of the target excel file.

        Returns:
            pandas.dataframe: A dataframe representatio of the excel file.
        """
        imported_data = pd.read_excel(target_file_path, converters={'MRN': lambda x: str(x), 'Encounter ID': lambda x: str(x)}, engine='openpyxl').dropna()
        return imported_data


    def create_db_row(self, source_row):
        """Takes a pandas row with patient discharge data and creates a database 
        record from the data.

        Args:
            source_row (pandas.dataframe): A single-row dataframe containing the 
            data to be entered into the database.
        """
        birth_date = self.get_date_from_string(source_row['Birth Date'])
        admission_datetime = self.get_datetime_from_string(source_row['Admission D/T'])
        discharge_datetime = self.get_datetime_from_string(source_row['Discharge D/T'])
        update_datetime = self.get_datetime_from_string(source_row['Update D/T'])

        new_entry = PatientDischarges(MRN=source_row['MRN'],
                                      encounter_id=source_row['Encounter ID'],
                                      first_name=source_row['First Name'],
                                      last_name=source_row['Last Name'],
                                      birth_date=birth_date,
                                      admission_dt = admission_datetime,
                                      discharge_dt = discharge_datetime,
                                      update_dt = update_datetime
                                      )

        add_patient_discharge(new_entry)
        


    def get_date_from_string(self, date_string):
        """Converts a string represenation of a date in mm/dd/yyyy format to
        a dictionary holding the integer values for the day, month, and year.

        Args:
            date_string (string): A string representation of a date in the 
            format mm/dd/yyyy.

        Returns:
            datetime.date: Date value based on attributes parsed from 
            provided string. 
        """
        date_attributes = {"month": int(date_string[0:2]),
                           "day": int(date_string[3:5]),
                           "year": int(date_string[6:10])
                           }
        
        return date(year=date_attributes['year'],
                    month=date_attributes['month'],
                    day=date_attributes['day']
                )

    def get_datetime_from_string(self, datetime_string):
        """Parses a datetime value from a provided string.

        Args:
            datetime_string (string): String representation of a datetime in 
            "mm/dd/yy hh:mm xx" format, where hh can be 1 or 2 characters, and
            xx is the am/pm information.

        Returns:
            datetime.datetime: The datetime constructed from the parsed string.
            
        """
        date_string = datetime_string[0:10]
        time_string = datetime_string[11:]

        parsed_date = self.get_date_from_string(date_string)
        parsed_time = self.get_time_from_string(time_string)

        parsed_datetime = datetime.combine(parsed_date, parsed_time)

        return parsed_datetime

    def get_time_from_string(self, time_string):
        """Parses a time value from a provided string.

        Args:
            time_string (string): String representation of a time in
            "hh:mm xx" format, where hh can be 1 or 2 characters, and
            xx is the am/pm information.

        Returns:
            datetime.time: The time constructed from the parsed string.
        """
        hour_string = ""
        minute_string = ""
        am_pm = ""
        current_time_part = "hour"

        for c in time_string:
            if current_time_part == "hour":
                if(c != ":"):
                    hour_string += c
                else:
                    current_time_part = "minute"
            elif(current_time_part == "minute"):
                if(c != " "):
                    minute_string += c
                else:
                    current_time_part = "am-pm"
            else:
                am_pm += c

        if(am_pm == "PM"):
            hour = int(hour_string) + 12
        else:
            hour = int(hour_string)

        parsed_time = time(hour=hour, minute=int(minute_string))

        return parsed_time

