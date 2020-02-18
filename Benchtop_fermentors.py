import pandas as pd
import os
import numpy as np
import glob
import plotly.graph_objs as go
# offline plotting
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import datetime as dt
import time
import re

date = input('A kísérlet dátuma (YYYYMMDD):')
folder = []
for root, dirs, files in os.walk(r"D:\PROGRAMOZÁS\PYTHON\BenchtopFermentors\03.measurement"):
    for name in dirs:
        if re.match(r'.*'+date+'.*', name) is not None:
            print(os.path.join(root, name))
            folder.append(os.path.join(root, name))
if folder == []:
    print('Nincs ilyen kísérlet')

folder = tuple(folder)
print(folder)

# init_notebook_mode(connected=True)  # initiate notebook mode
traces = []
for i in folder:
    paths = glob.glob(i+'/*.txt')
    df = pd.concat(pd.read_table(f, header=12) for f in paths)
    df = df.reset_index()
    df['DateTime'] = df.Date+' '+df.Time
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['ElapsedTime'] = df.DateTime-df.DateTime[0]
    ElapsedHours = []
    for x in df['ElapsedTime']:
        ElapsedHours.append(x.total_seconds()/3600)
    df['ElapsedHours'] = ElapsedHours
    name = input('Trace=')
    trace = go.Scatter(x=df.ElapsedHours, y=df.pH, name=name)
    layout = go.Layout(title='pH change of the reactors', xaxis=dict(
        title='Elapsed Time (h)'), yaxis=dict(title='pH'))
    traces.append(trace)

fig = go.Figure(data=traces, layout=layout)
iplot(fig)
