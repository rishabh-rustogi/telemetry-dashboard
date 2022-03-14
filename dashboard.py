# Run this app with `python dashboard.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import subprocess
import pandas as pd
import pickle
import psutil

# Plotly related imports
import plotly.express as px
import plotly.graph_objects as go

# Dash related imports
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html


# Pickle files to read data
fileCPU = "CPUUsage.pkl"
fileRAM = "RAMUsage.pkl"
fileRecurrUser = "RecurrUser.pkl"

# Function that returns python object from pickle file
def readObject(file):
    objects = []
    with (open(file, "rb")) as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
    
    return objects[0]
    
# Create a Dash App
app = dash.Dash(__name__)

# Setup webpage Dash Layout
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

# Callback for Interval trigger to update CPU Graph periodically
@app.callback(Output('live-update-graph-cpu', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_cpu_usage():
    try:
        # Read the pickle file and get a dataFrame
        df = readObject(fileCPU)
        
        # Create a interactive Plotly line graph using the dataFrame
        fig = px.line(df, x="timeList", y="countCPUList", title="CPU uage over Times")
        
        # Set the Plotly figure Layout
        fig.update_layout(yaxis_range=[0,100])
        
        # Return the plotly object
        return fig
    except:
        
        # In case of any error, return an empty figure
        return go.Figure()

    
# Callback for Interval trigger to update RAM Graph periodically
@app.callback(Output('live-update-graph-ram', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_ram_usage():
    try:
        
        # Read the pickle file and get a dataFrame
        df = readObject(fileRAM)
        
        # Create a interactive Plotly line graph using the dataFrame with hover data (top 5 processes)
        fig = px.line(df, x="timeList", y="countRAMList", title="RAM uage over Times", hover_name="processes")
        
        # Set the Plotly figure Layout
        return fig
    except:
        
        # In case of any error, return an empty figure
        return go.Figure()

    
# Callback for Interval trigger to update Recurrent users for Movie recommendation service
@app.callback(Output('live-update-graph-recurr-usage', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_recurr_usage():
    try:
        
        # Read the pickle file and get a dataFrame
        df = readObject(fileRecurrUser)
        
        # Create a interactive Plotly line graph using the dataFrame
        fig = px.line(df, x="timeList", y="countRecurrList") 
        
         # Set the Plotly figure Layout
        return fig
    except:
        
        # In case of any error, return an empty figure
        return go.Figure()

if __name__ == '__main__':
    
    # Initiate the getSystemUsage.py and telemetry.py to run in background to update the pickle files
    subprocess.Popen(['python', "<file location>/getSystemUsage.py"])
    subprocess.Popen(['python', "<file location>/telemetry.py"])
    
    # Initiate the Dash app (currently in debug mode)
    app.run_server(debug=True)
