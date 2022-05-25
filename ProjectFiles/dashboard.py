from cmath import nan
from pickle import NONE
from tempfile import SpooledTemporaryFile
import dash
import plotly.express as px
from dash import Dash, html, dcc, Output, Input, dash_table
import plotly.graph_objects as go
import pandas as pd
import utilities as ut
import numpy as np
import os
import re
import logging


#-------------------------------------------------Aufgabe Zusatz Logdatei ---------------------------------------------------------------------#Logfile erstellen
Log_Format = "%(levelname)s:%(asctime)s:%(message)s" #Format

#Benennung der Datei, Dateityp
logging.basicConfig(filename = "logfile_HLM.logg",
                    filemode = "w",
                    format = Log_Format, 
                    level = logging.INFO)
                    
app = Dash(__name__)


list_of_subjects = []
subj_numbers = []
number_of_subjects = 0

folder_current = os.path.dirname(__file__) 
print(folder_current)
folder_input_data = os.path.join(folder_current, "input_data")
for file in os.listdir(folder_input_data):
    
    if file.endswith(".csv"):
        number_of_subjects += 1
        file_name = os.path.join(folder_input_data, file)
        print(file_name)
        list_of_subjects.append(ut.Subject(file_name))


df = list_of_subjects[0].subject_data


for i in range(number_of_subjects):
    subj_numbers.append(list_of_subjects[i].subject_id)

    logging.info('Subject {}{}'.format(i,' initialised'))
data_names = ["SpO2 (%)", "Blood Flow (ml/s)","Temp (C)"]
algorithm_names = ['min','max']
blood_flow_functions = ['CMA','SMA','Show Limits']


fig0= go.Figure()
fig1= go.Figure()
fig2= go.Figure()
fig3= go.Figure()

fig0 = px.line(df, x="Time (s)", y = "SpO2 (%)")
fig1 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")
fig2 = px.line(df, x="Time (s)", y = "Temp (C)")
fig3 = px.line(df, x="Time (s)", y = "Blood Flow (ml/s)")

#-------------------------------------------------Aufgabe 5 Applayout ---------------------------------------------------------------------

app.layout = html.Div(children=[
    #Hauptüberschrift zentriert und mit Hintergrund
    html.H1(children='Cardiopulmonary Bypass Dashboard', style = {'color':'#263238', 'text-align':'center', 'backgroundColor': '#E0E0E0'}), #Zentrierung der Überschrift

    html.Div([
        
        html.Div(
            [
                html.H2('Select your subject:', style = {'color':'#263238', 'marign':'1em'}), #Beschriftung Auswahl Subject
            ]
        ),
        dcc.Dropdown(options = subj_numbers, placeholder='Select a subject', value='1', id='subject-dropdown'),
        html.Div(id='dd-output-container')
        ],
        style={"width": "10%", "display": "inline-10"}
    ),

        html.Div(
            [
                html.H2('Select your filter:', style = {'color':'#263238', 'marign':'1em'}), #Beschriftung Auswahl Filter
            ]
        ),        
        #Checkliste Min/Max
        dcc.Checklist(
            id= 'checklist-algo',
            options=algorithm_names,

            style={'display': 'inline'}, 
            labelStyle={"font-family": "Arial, Helvetica, sans-serif",
                "color": "#424242",
                'display': 'inline'},
            inputStyle={"margin-right": "7.5px", "margin-left": "15px"}
        ),

        # Checkliste CMA/SMA/Limits
        dcc.Checklist(
            id= 'checklist-bloodflow',
            options=blood_flow_functions,

            # CSS Attribute für Checklisten wegen label und input nicht in style.css ausgelagert
            style={'display': 'inline'},
            labelStyle={"font-family": "Arial, Helvetica, sans-serif",
                "color": "#424242",
                'display': 'inline'},
            inputStyle={"margin-right": "7.5px", "margin-left": "15px"}
        ),
    
    #Darstellung Graphen
    #Graph SP02
     dcc.Graph(
        id='dash-graph0',
        figure=fig0
     ),
    
    #Graph Blood flow
    dcc.Graph(
        id='dash-graph1',
        figure=fig1
    ),

    #Graph Temp
    dcc.Graph(
        id='dash-graph2',
        figure=fig2
    ),

    #Graph Blood Flow
    dcc.Graph(
        id='dash-graph3',
        figure=fig3
    ),
    
    #Auswahlfenster für gespeicherte Patienten Befunde der letzten Sitzungen #To Do: Input Daten bereitstellen und darstellen
    html.Div([
        html.Div(
            [
                html.H2('ADDITIONAL SUBJECT DATA:', style = {'color':'#263238', 'marign':'2em'}), #Beschriftung Dropdown Menü1
            ]
        ),
            dcc.Dropdown(id = 'input-type:',
            options = [{'label':'FINDINGS 2020:', 'value':'OPT1'},{'label':'FINDINGS 2021:', 'value': 'OPT2'}], #Hier sollen noch Befunde dargestellt werden
            multi = False,
            placeholder = 'CHOOSE FINDING',
            style={'width': '50%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ], style = {'display': 'flex'}),
])


### Callback Functions ###
## Graph Update Callback
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph0', 'figure'),
    Output('dash-graph1', 'figure'),
    Output('dash-graph2', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-algo','value')
)
def update_figure(value, algorithm_checkmarks):
    print("Current Subject: ",value)
    print("current checked checkmarks are: ", algorithm_checkmarks)
    ts = list_of_subjects[int(value)-1].subject_data
    #SpO2
    fig0 = px.line(ts, x="Time (s)", y = data_names[0])
    # Blood Flow
    fig1 = px.line(ts, x="Time (s)", y = data_names[1])
    # Blood Temperature
    fig2 = px.line(ts, x="Time (s)", y = data_names[2])
    
    ###Aufabe 2 Minimum und Maximum je Auswahl Button direkt im graphen anzeigen 

    #list of functions 
    grp = ts.agg(['min', 'max', 'idxmin', 'idxmax']) 
    print(grp)
    
    if algorithm_checkmarks is not None:

        #add trace to graph for 'min' function
        if 'min' in algorithm_checkmarks:
            #starte Log bei Auswahl
            logging.info('min initialized')
            fig0.add_trace(go.Scatter(x = [grp.loc['idxmin', data_names[0]]], y = [grp.loc['min', data_names[0]]], mode = 'markers', name = 'min', marker_symbol = 6, marker_size = 12, marker_color = '#F44336')) #Symbole deren Größe usw.
            fig1.add_trace(go.Scatter(x = [grp.loc['idxmin', data_names[1]]], y = [grp.loc['min', data_names[1]]], mode = 'markers', name = 'min', marker_symbol = 6, marker_size = 12, marker_color = '#F44336'))
            fig2.add_trace(go.Scatter(x = [grp.loc['idxmin', data_names[2]]], y = [grp.loc['min', data_names[2]]], mode = 'markers', name = 'min', marker_symbol = 6, marker_size = 12, marker_color = '#F44336'))

        #add trace to graph for 'max' functon 
        if 'max' in algorithm_checkmarks:
            #starte Log bei Auswahl
            logging.info('max initialized')
            fig0.add_trace(go.Scatter(x = [grp.loc['idxmax', data_names[0]]], y = [grp.loc['max', data_names[0]]], mode = 'markers', name = 'max', marker_symbol = 5, marker_size = 12, marker_color = '#4A8D19'))
            fig1.add_trace(go.Scatter(x = [grp.loc['idxmax', data_names[1]]], y = [grp.loc['max', data_names[1]]], mode = 'markers', name = 'max', marker_symbol = 5, marker_size = 12, marker_color = '#4A8D19'))
            fig2.add_trace(go.Scatter(x = [grp.loc['idxmax', data_names[2]]], y = [grp.loc['max', data_names[2]]], mode = 'markers', name = 'max', marker_symbol = 5, marker_size = 12, marker_color = '#4A8D19'))
    
    #fig0.update_traces(update_lines_color = '#194a8d')
    # fig1.update_traces(update_lines_cols = '#4a8d19')
    # fig2.update_traces(update_lines_cols = '#194a8d')
    #Hilfestellung -> #fig.add_trace(go.Scatter(x=data["Time"], y=data["OD"], mode='markers', marker=dict(color=data["C-source"], size=data["C:A 1 ratio"])))    
    return fig0, fig1, fig2 


## Blodflow Simple Moving Average Update
@app.callback(
    # In- or Output('which html element','which element property')
    Output('dash-graph3', 'figure'),
    Input('subject-dropdown', 'value'),
    Input('checklist-bloodflow','value')
)
def bloodflow_figure(value, bloodflow_checkmarks):
    
    ## Calculate Moving Average: Aufgabe 2 #Caluclation in utilities
    print(bloodflow_checkmarks)
    bf = list_of_subjects[int(value)-1].subject_data # bf deklaration
    fig3 = px.line(bf, x="Time (s)", y="Blood Flow (ml/s)") #fig 3 Darstellung

    if bloodflow_checkmarks is not None:

        if 'SMA' in bloodflow_checkmarks: #Abfrage SMA Button
            logging.info('SMA initialized') #Logging
            bf['Simple Moving Average']=ut.calculate_SMA(bf['Blood Flow (ml/s)'],10) #n=10 Perioden für SMA
            fig3 = px.line(bf, x="Time (s)", y="Simple Moving Average")

        if 'CMA' in bloodflow_checkmarks:
            logging.info('CMA initialized') #Logging
            bf['Cumulative Moving Average']=ut.calculate_CMA(bf['Blood Flow (ml/s)'],2)
            fig3 = px.line(bf, x="Time (s)", y="Cumulative Moving Average")

    ## Durchschnitt: Aufgabe 3
        if 'Show Limits' in bloodflow_checkmarks:
            avg=bf.mean()
            x=[0,480]
            y=avg.loc['Blood Flow (ml/s)']
            fig3.add_trace(go.Scatter(x=x,y=[y,y],mode='lines',name='Average',marker_color='#4A8D19'))

            y_up=avg.loc['Blood Flow (ml/s)']*1.15 #Grenze von +15%
            y_down=avg.loc['Blood Flow (ml/s)']*0.85 #Grenze von -15%

            fig3.add_trace(go.Scatter(x=x,y=[y_up,y_up],mode='lines',name='+15%',marker_color='#F44336'))
            fig3.add_trace(go.Scatter(x=x,y=[y_down,y_down],mode='lines',name='-15%',marker_color='#F44336'))

    #fig3.update_traces(update_lines_cols = '#4A8D19') #Änderung der Farbe des Trends
    return fig3
    
if __name__ == '__main__':
    app.run_server(debug=True)