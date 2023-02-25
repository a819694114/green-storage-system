import streamlit as sl
import pandas as pd
import plotly.express as px
from chart_studio import plotly

global battery_df
global battery_columns


### --- Sidebar
sl.set_page_config(layout='wide', initial_sidebar_state='expanded') 

sl.sidebar.header('Dashboard `version 2`')

### --- Style
with open('style.css') as f:
    sl.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

### --- FILE UPLOAD & LOAD DATAFRAME
client_file = sl.sidebar.file_uploader(
    label= "Upload your CSV file. (200MB max)",
    type=['csv', 'xlsx']
)
if client_file is not None:
    print(client_file)
    print("hello")

    try:
        battery_df = pd.read_csv(client_file) # read file
    except Exception as e:
        print(e)
        battery_df = pd.read_excel(client_file)

## --- Tabs
tab_headings = [
    "Data Analysis",
    "Prediction"
]

tabs = sl.tabs(tab_headings)

### --- Data Analysis Tab
with tabs[0]:
    sl.markdown("Data Analysis")

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

            total_cycles=(battery_df['cycle'].count())
            min_temperature=(battery_df['temperature_measured'].min().round(2))
            max_temperature=(battery_df['temperature_measured'].max().round(2))
            average_temperature=(battery_df['temperature_measured'].mean().round(2))

            sl.markdown('### Metrics')
            c1, c2, c3, c4 = sl.columns(4)
            c1.metric("Total Cycles", f'{total_cycles}')
            c2.metric("Min Temperature", f'{min_temperature}')
            c3.metric("Max Temperature", f'{max_temperature}')
            c4.metric("Average Temperature", f'{average_temperature}')


            ### -- Row C: Line graph
            sl.markdown('### Line chart')
            sl.line_chart(battery_df, x="cycle", y="capacity")

        except Exception as e:
            print(e)

### --- Prediction Tab
with tabs[1]:
    sl.markdown("Prediction Dashboard")