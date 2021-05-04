# You can use whatever package(s) you like to handle the timeseries data
import json
import numpy as np
import pandas as pd
import traces
import matplotlib.pyplot as plt


class VISCalculator:

    def __init__(self, medications_filename, medication_administrations_filename, note_filename, procedures_filename):
        self.medications_filename = medications_filename
        self.medication_administrations_filename = medication_administrations_filename
        self.note_filename = note_filename
        self.procedures_filename = procedures_filename

    def make_procedures_from_log(self):
        pass

    def make_procedures_from_note(self):
        pass

    def make_encounters_from_note(self):
        pass

    def make_fhir_resources(self):
        pass

    def calculate_vis_timeseries(self):
        """ Return the VIS timeseries
        """
        pass

    def plot_vis_timeseries(self):
        """ Return filename that you saved the VIS timeseries to (.png)
        """
        pass

    def get_max_vis_score_info(self):
        """ Return dictionary with required info about the max VIS score
        """
        pass

