import streamlit as st
import numpy as np
import pandas as pd
import requests
from bokeh.plotting import figure

url = "https://demo.dev.dynatracelabs.com/api/v2/"
apiToken = st.sidebar.text_input('API token', '', None, None, 'password')

r = requests.get('https://demo.dev.dynatracelabs.com/api/v2/entities?entitySelector=type%28HOST%29', headers={"Authorization": 'Api-Token '+apiToken, "accept": "application/json; charset=utf-8"})
resultData = r.json()

entityIds = []

for host in resultData['entities']:
   entityIds.append(host['entityId'])

selectedEntityId = st.sidebar.selectbox(
    'Select host: ',
    entityIds
)


selectedMetricId = st.sidebar.selectbox(
    'Select metric: ',
    ('builtin:host.disk.bytesWritten', 'builtin:host.disk.readTime', 'builtin:host.net.nic.packets.tx', 'builtin:host.net.nic.trafficIn'))

metricDataResult = requests.get('https://demo.dev.dynatracelabs.com/api/v2/metrics/query?metricSelector='+selectedMetricId+'&entitySelector=entityId('+selectedEntityId+')&from=-12h', headers={"Authorization": 'Api-Token '+apiToken, "accept": "application/json; charset=utf-8"})
metricDataResult = metricDataResult.json()
st.json(metricDataResult)


p = figure(
    title='simple line example',
    x_axis_label='x',
    y_axis_label='y')

timestamps = metricDataResult['result'][0]['data'][0]['timestamps']
values = metricDataResult['result'][0]['data'][0]['values']

p.line(timestamps, values, legend='Trend', line_width=2)

st.bokeh_chart(p, use_container_width=True)


add_slider = st.sidebar.slider(
    'The "I do nothing" slider',
    0.0, 100.0, (25.0, 75.0)
)