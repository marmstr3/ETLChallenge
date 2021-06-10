# Coding Takehome Test (Test 02)
## Michael Armstrong - For Carta Healthcare

## Design Decisions & Assumptions
- Due to xlrd no longer supporting .xlsx filetype, pandas could not import the data files. To solve this, a dependency on the openpyxl library was added to the project.
- MRN and Encounter ID are stored as strings in the database to preserve the leading zeroes.
- FHIR R3 requires patient resources to have a gender. However, no gender information was provided in the data. Because of this, all patient genders were set to "unknown".
- The provided data had no patients with multiple encounters. Because of this, no functionality was built to identify multiple encounters. For production, this would need to be addressed, and would affect the method used to merge the datasets in load.py as well, since duplicate MRNs would not automatically mean a duplicate encounter.
- MRN 002 has two names in the provided data. This could be due to a name change, the patient having multiple names, or a clerical error. Without further information, which situation it is cannot be determined. Because of this, I assumed that it was a clerical error and used the most up-to-date data to store in the database. If it is a case of the patient having multiple names or a name change, functionality to identify the new name and to add it to the patient profile would need to be implemented to track the multiple names. The patient resource dictionaries are already developed to allow for a list of names, so this would only require querying logic.
- Since all records have a discharge date, I have assumed that all encounters are of the status "finished".

## Possible Improvements
- the date/time/datetime from string methods in DataLoader() could be made more robust by utilizing regex.
- Input validation could be implemented to prevent malformed or adversarial data entries in the DataLoader.load_data() method.
- DataLoader.get_time_from_string() could be further optimized by utilizing slices instead of string appends.
- Encounter and patient resources would be better represented as objects, instead of as dictionaries. However, the testing schema provided does not allow for that.