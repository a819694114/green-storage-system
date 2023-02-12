import streamlit as sl
import pandas as pd
import plotly.express as px
from chart_studio import plotly

global battery_df
global battery_columns

# Sidebar expanded by default
sl.set_page_config(layout='wide', initial_sidebar_state='expanded')

sl.sidebar.header('Dashboard `version 2`')

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
        sl.plotly_chart(plot)
    except Exception as e:
        print(e)