# Introduction
This is a test for seeing how well you can get around with typically messy clinical data provided in various forms, including clinical notes processed with NLP, and the ability to interpret published literature to a real-world use-case.

In this analysis, you are assuming the role of a data scientist assigned the goal of automating a field in a cardiac registry concerned with pharmacologic cardiovascular support in infants undergoing cardiac surgery with bypass.  In particular, you will be examining the vasoactive-inotropic score (VIS) as defined in the following publication:  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4159673/.  The full text has also been provided as a PDF.

You have been given a dataset of the medications that are used for each medication administration, a sample clinical note, and a procedure log.

You will use [FHIR](https://www.hl7.org/fhir) as a common schema across the various data sources.  You can find the specifications for all FHIR resources [here](https://www.hl7.org/fhir/resourcelist.html).


# The Goal
Your goal is to answer the following questions:

 1. What clean FHIR resources can be extracted from the parsed clinical note and procedure log?
 2. What was the patient's VIS score at all times from hospital admission to discharge?
 3. What was the patient's maximum VIS score in their first 24 hours after CICU admission?
 4. What VIS category does the patient fall into?

### FHIR Resources
The output for 1) should be a function or functions which examine the parsed clinical note and procedure log, and produce [FHIR Encounter resources](https://www.hl7.org/fhir/encounter.html) (one for the hospitalization and one for the CICU stay), and [FHIR Procedure resources](https://www.hl7.org/fhir/procedure.html) following the official documentation.  All FHIR resources can be in the form of Python dictionaries which follow the schema in the documentation.

Each FHIR resource should be saved to following named .json file.
* results/fhir_resources.json

Bonus / Optional:
* Patient resource(s)
* Practitioner resource(s)
* Condition resource(s)

### VIS Score Time-Series
The output for 2) should look like a plot with time on the X-axis, and VIS score on the Y-axis.  Significant points in time should be clearly indicated.  This plot should start at hospital admit and end at hospital discharge.  Also save the raw data as a .csv file with the columns:  timestamp, vis_score

* results/VIS_timeseries.png
* results/VIS_timeseries.csv

### Max VIS Score
The output for 3) should be a function which takes only FHIR resources as inputs, and returns the following
```
{
    "value":  <the max VIS score in first 24hr after CICU admission>,
    "start_datetime":  <when the patient had the max VIS score (start of interval)>,
    "duration":  <total number of minutes the patient was at the maximum VIS score>,
    "classification_group":  <number 1,2,3,4,5 based on VIS paper Table 1>
}
```

These results should be saved to the following named .json file.
* results/maximum_VIS_score_info.json



# Dataset Overview
Here is an explanation of the dataset you have been given:


## raw-sample-note.txt
The raw text of the sample clinical note provided for your reference.  No processing should be performed directly on this note.

## parsed-sample-note.json
The output after the raw sample note is fed through the Natural Language Processing pipeline.  Entities in the note are coded under the [Unified Medical Language System (UMLS)](https://www.nlm.nih.gov/research/umls/index.html).  Use the coded entities to find relevant information and construct the required FHIR resources.  [Semantic types](https://metamap.nlm.nih.gov/Docs/SemanticTypes_2018AB.txt) are broad categories of medical terms in the UMLS.

### Relevant UMLS terms/codes

| UMLS Code | Term |
|----------|------------------------|
| C0018817 | Atrial Septal Defect   |
| C0803906 | Birth Date             |
| C0086582 | Male                   |
| C0086287 | Female                 |
| C0184666 | Hospital Admission     |
| C0586003 | Hospital Discharge     |
| C5240707 | ICU admission date     |
| C5240710 | ICU discharge date     |
| C2243117 | Echocardiogram         |


## medication-administrations.json
This is a list of [FHIR MedicationAdministration resources](https://www.hl7.org/fhir/medicationadministration.html) for the sample patient.

## medications.json
This is a list of [FHIR Medication resources](https://www.hl7.org/fhir/medication.html) for the sample patient.

## procedure_log.csv
This is an extract of historical inpatient procedures, including both surgical procedures and other inpatient procedures.

```
mrn:  The patient's Medical Record Number
case_id: A unique identifier for a single procedure
practitioner: Who performed the procedure
primary_procedure_name: The name of the procedure that was performed
primary_procedure_code: A SNOMED-CT code for the procedure
procedure_date: The date the procedure was performed
procedure_time: The time of day the procedure was performed
```


# Solution Presentation
The final deliverable is for the following command to output each of the three outputs described above, saved to the test_05/results directory:
```
python test_05/run.py
```

# Notes
Feel free to change out any stub class implementations, add unit tests (pytest), etc. Whatever 
you'd do normally as part of your workflow! The only thing that matters is that `python test_05/run.py`
will produce the answers we're looking for.


# References:
SNOMED-CT:  https://www.nlm.nih.gov/healthit/snomedct/index.html.  Many browsers can be found online.
