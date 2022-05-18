# Import external packages

from fileinput import filename
from multiprocessing.connection import wait
import pandas as pd
from datetime import datetime
import numpy as np
import re

# Classes 

class Subject():
    def __init__(self, file_name):

        ### Aufgabe 1: Interpolation ###

        __f = open(file_name)
        self.subject_data = pd.read_csv(__f)
        self.subject_data = self.subject_data.interpolate(method='slinear', axis=0) #interpolationstyp slinear 170522
        #__splited_id = re.findall(r'\d+',file_name)
        #Auswahl subject ID greift 221,222,223 ab
        self.subject_id = file_name.split('.csv')[0][-1] #-> filename aus DataX.csv Datei + nur die letzte Stelle
        self.names = self.subject_data.columns.values.tolist()
        self.time = self.subject_data["Time (s)"]        
        self.spO2 = self.subject_data["SpO2 (%)"]
        self.temp = self.subject_data["Temp (C)"]
        self.blood_flow = self.subject_data["Blood Flow (ml/s)"]
        print('Subject ' + self.subject_id + ' initialized')



   
### Aufgabe 2: Datenverarbeitung ###

def calculate_CMA(df,n):
    pass
    

def calculate_SMA(df,n):
    pass     

### Aufgabe 2: Datenverarbeitung ###

#class Average():
 #   def calculate_CMA(df,n):

    #Eingabedaten auswählen
    #Subject





#    pass
#def calculate_SMA(df,n):
  #  pass