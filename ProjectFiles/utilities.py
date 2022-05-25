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

        __f = open(file_name)   #CSV Datei auslesen
        self.subject_data = pd.read_csv(__f)
        self.subject_data = self.subject_data.interpolate(method='slinear', axis=0) #interpolationstyp slinear 170522. Dieser ist aufgrund der kleinen Lückenausbildung + linearem Verhalten sinnvoll

        #__splited_id = re.finall(r'\d+',file_name)
        #Auswahl subject ID greift 221,222,223 ab
        self.subject_id = file_name.split('.csv')[0][-1] #-> filename aus DataX.csv Datei + nur die letzte Stelle
        self.names = self.subject_data.columns.values.tolist()
        self.time = self.subject_data["Time (s)"]        
        self.spO2 = self.subject_data["SpO2 (%)"]
        self.temp = self.subject_data["Temp (C)"]
        self.blood_flow = self.subject_data["Blood Flow (ml/s)"]
        print('Subject ' + self.subject_id + ' initialized')



   
### Aufgabe 2: Datenverarbeitung ###

def calculate_CMA(df,n):                #Berechnung CMA
    return df.expanding(n).mean()
    

def calculate_SMA(df,n):                #Berechnung SMA
    return df.rolling(n).mean()    

    #-------------------------------------------------Aufgabe 4 ---------------------------------------------------------------------

#4.1
#Der Simple Moving Average (SMA) ist ein gleitender Durchschnitt über die letzten "n"-Perioden.
#Einzelne Perioden werden unterschiedlich gewichtet. Hier haben zum Beispiel die letzten Perioden einen deutlich höheren Einflussauf den Wert des gleitenden Durchschnitts
#Er berechnet sich fortlaufend aus dem Durchschnitt eines Kurses über eine festgelegte Zeitperiode.
#das Gleiten, kommt dadurch zustande, dass sich sein Wert mit jeder Kursveränderung der fortlaufenden Periode anpasst

#Sinnvoll: Bei darstellung von Börsen Trends. Rauschen wird ausgeglichen und in einem Trend dargestellt.
#Nicht-Sinvoll: Bei Auswertung von Datensätzen mit kurzen Zeiten sowie bei fehlerbehafteten Dateien. SMA reagiert langsam bei schnellen Kursänderungen

#4.2
#desto höher "n" deste mehr Perioden werden miteinbezogen und somit wird das Signal mehr geglättet

## zusatz noch nicht fertig
#Zusatz alte Befunde in Dash dartsellen
#Datei einlesen

class Subject2():
    def __init__(self, file_name):

        __f = open(file_name)   #CSV Datei auslesen
        self.subject_data = pd.read_csv(__f)

        self.subject_id = file_name.split('findings.csv')[0] #-> filename aus DataX.csv Datei + nur die letzte Stelle
        self.names = self.subject_data.columns.values.tolist()
        self.findings = self.subject_data["Findings"]        
    
        print('Finding ' + self.subject_id + ' initialized')