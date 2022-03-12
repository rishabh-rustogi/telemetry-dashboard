# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pickle
import psutil
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
from random import random
import subprocess

timeCounter = 0
timeList = []
countList = []
start = time.time()
fileCPU = "CPUUsage.pkl"
fileRAM = "RAMUsage.pkl"
fileRecurrUser = "RecurrUser.pkl"

def readObject(file):
    objects = []
    with (open(file, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    
    return objects[0]
    
app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H1('Simple Telemetry Dashboard', style={'textAlign': 'center'}),
        html.H2('CPU usage over Time (%used vs time)'),
        dcc.Graph(id='live-update-graph-cpu'),
        html.H2('RAM usage over Time (%used vs time)'),
        dcc.Graph(id='live-update-graph-ram'),
        html.H2('Recurrent users over Time (#Users vs time)'),
        dcc.Graph(id='live-update-graph-recurr-usage'),
        dcc.Interval(
            id='interval-component',
            interval=10*1000
        )
    ])
)


@app.callback(Output('live-update-graph-cpu', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_cpu_usage():
    try:
        df = readObject(fileCPU)
        #print(df['processes'])
        fig = px.line(df, x="x", y="y", title="CPU uage over Times")
        fig.update_layout(yaxis_range=[0,100])
        return fig
    except:
        return go.Figure()

@app.callback(Output('live-update-graph-ram', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_ram_usage():
    try:
        df = readObject(fileRAM)
        fig = px.line(df, x="x", y="y", title="RAM uage over Times", hover_name="processes")
        return fig
    except:
        return go.Figure()

@app.callback(Output('live-update-graph-recurr-usage', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_recurr_usage():
    try:
        df = readObject(fileRecurrUser)
        fig = px.line(df, x="x", y="y") 
        return fig
    except:
        return go.Figure()

if __name__ == '__main__':
    subprocess.Popen(['python', "/Users/rishabhrustogi/Desktop/Machine Learning in Production/I3/getSystemUsage.py"])
    subprocess.Popen(['python', "/Users/rishabhrustogi/Desktop/Machine Learning in Production/I3/telemetry.py"])
    app.run_server(debug=True)