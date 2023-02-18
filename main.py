import streamlit as sl
import pandas as pd
import plotly.express as px
from chart_studio import plotly

global battery_df
global battery_columns

### --- Sidebar
sl.set_page_config(layout='wide', initial_sidebar_state='expanded') 

sl.sidebar.header('Dashboard `version 2`')

## --- Tabs
tab_headings = [
    "Data Analysis",
    "Prediction"
]

tabs = sl.tabs(tab_headings)

with tabs[0]:
    sl.markdown("Data Analysis")

with tabs[1]:
    sl.markdown("Prediction Dashboard")


### --- FILE UPLOAD
client_file = sl.sidebar.file_uploader(
    label= "Upload your CSV file. (200MB max)",
    type=['csv', 'xlsx']
)

if client_file is not None:
    print(client_file)
    print("hello")

    try:
        battery_df = pd.read_csv(client_file)
    except Exception as e:
        print(e)
        battery_df = pd.read_excel(client_file)

try:
    sl.write(battery_df)
    battery_columns = list(battery_df.select_dtypes(['float','int']).columns)
except Exception as e:
    print(e)
    sl.write("Please upload file.")

# select widget for chart type on sidebar
chart_type = sl.sidebar.selectbox(
    label="Select desired chart type",
    options=["Scatterplots", 'Lineplots', 'Historgram', 'Boxplot']
)

if chart_type == 'Scatterplots':
    sl.sidebar.subheader("Scatterplot Settings")
    try:
        x_values = sl.sidebar.selectbox('X axis', options=battery_columns)
        y_values = sl.sidebar.selectbox('Y axis', options = battery_columns)
        plot = px.scatter(data_frame=battery_df, x=x_values, y=y_values)

        # display graph
        sl.markdown('### Capacity Degradation for discharge cycles')
        sl.plotly_chart(plot)

        ### --- Row A: Metrics
        sl.markdown('### Metrics')
        c1, c2, c3 = sl.columns(3)
        c1.metric("Total Cycles", 166)
        c2.metric("Total Cycles", 166)
        c3.metric("Total Cycles", 166)


        ### -- Row C: Line graph
        sl.markdown('### Line chart')
        sl.line_chart(battery_df, x="cycle", y="capacity")

    except Exception as e:
        print(e)


