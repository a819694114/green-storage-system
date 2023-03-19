import streamlit as sl
import pandas as pd
import numpy as np
import plotly.express as px
from chart_studio import plotly
import os
import time
# import pandas_profiling
from streamlit_pandas_profiling import st_profile_report
import ydata_profiling 
from streamlit_option_menu import option_menu
import altair as alt

# ML 
from pycaret.regression import setup, compare_models, pull, save_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

global battery_df
global battery_columns

###########################################
#              Definitions                #
###########################################
# Add the custom CSS stylesheet
def local_css(file_name):
    with open(file_name) as f:
        sl.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Definition: Build Neural Network Model
def build_nn_model(df):
    X = df.iloc[:,:-1] # Using all column except for the last column as X
    Y = df.iloc[:,-1] # Selecting the last column as Y

    # Data splitting
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=(100-split_size)/100)
    
    sl.markdown('**2.1. Data splits**')
    sl.write('Training set')
    sl.info(X_train.shape)
    sl.write('Test set')
    sl.info(X_test.shape)

    sl.markdown('**2.2. Variable details**:')
    sl.write('X variable')
    sl.info(list(X.columns))
    sl.write('Y variable')
    sl.info(Y.name)

    rf = RandomForestRegressor(n_estimators=parameter_n_estimators,
        random_state=parameter_random_state,
        max_features=parameter_max_features,
        criterion=parameter_criterion,
        min_samples_split=parameter_min_samples_split,
        min_samples_leaf=parameter_min_samples_leaf,
        bootstrap=parameter_bootstrap,
        oob_score=parameter_oob_score,
        n_jobs=parameter_n_jobs)
    rf.fit(X_train, Y_train)

    sl.subheader('4. Model Evaluation')

    sl.markdown('**4.1. Training set**')
    Y_pred_train = rf.predict(X_train)
    sl.write('Coefficient of determination ($R^2$):')
    sl.info( r2_score(Y_train, Y_pred_train) )

    sl.write('Error (MSE or MAE):')
    sl.info( mean_squared_error(Y_train, Y_pred_train) )

    sl.markdown('**4.2. Test set**')
    Y_pred_test = rf.predict(X_test)
    sl.write('Coefficient of determination ($R^2$):')
    sl.info( r2_score(Y_test, Y_pred_test) )

    sl.write('Error (MSE or MAE):')
    sl.info( mean_squared_error(Y_test, Y_pred_test) )


def compute_soh(df):
    capacity_df = pd.DataFrame()
    attributes = ['cycle', 'datetime', 'capacity']
    soh_df = battery_df[attributes]
    initial_capacity = battery_df['capacity'][0]
    for i in range(len(soh_df)):
        soh_df['SoH']=(soh_df['capacity'])/initial_capacity
    return soh_df

# Modal while uploading file to prevent user from clicking any actions on screen
def loading_modal(file):
    # simulate upload by sleeping for 5 seconds
    with sl.spinner("Uploading..."):
        time.sleep(5)
    sl.success(f"Upload successful: {file.name}")

from sklearn.preprocessing import MinMaxScaler
# import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
# from tensorflow.keras.layers import Flatten
# from tensorflow.keras.layers import LSTM
from tensorflow.keras.optimizers import Adam
import numpy as np

# Neural Network Model
def soh_nn_model(df):

    initial_capacity = df['capacity'][0]
    Y = []

    X = df.iloc[:, 5:]
    for i in range(len(df)):
        Y.append([df['capacity'][i]]/initial_capacity)
    Y = pd.DataFrame(data=Y, columns=['SoH'])

    # sl.write(X.shape)
    # sl.write(Y.shape)
    # sl.write(X)
    # sl.write(Y)

    # Split Data
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = (100-split_size)/100)

    #Normalize training set
    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)

    # Normalize test set
    X_test = scaler.transform(X_test)

    # Display X train, X test shape
    sl.subheader('3. Model Parameters')
    sl.markdown('**3.1. Data splits**')
    sl.write('Training set')
    sl.info(X_train.shape)
    sl.write('Test set')
    sl.info(X_test.shape)

    # Display Variable Details for X and Y
    sl.markdown('**3.2. Variable details**:')
    sl.write('X variable')
    sl.info(list(X.columns))
    sl.write('Y variable')
    sl.info(Y.columns)

    # Build Model
    with sl.spinner('Building the Model...'):
        model = Sequential()
        model.add(Dense(8, activation='relu', input_dim=X_train.shape[1]))
        model.add(Dense(8, activation='relu'))
        model.add(Dense(8, activation='relu'))
        model.add(Dropout(rate=0.25))
        model.add(Dense(1))
        model.summary()
        model.compile(optimizer=Adam(beta_1=0.9, beta_2=0.999, epsilon=1e-08), loss='mean_absolute_error')
        time.sleep(1)
    sl.success('Model has been compiled!')

    # Train the NN on training data where 'fit' is used iteratively update the weights of the network to minimize loss function
    with sl.spinner('Training the Model...'):
        model.fit(x=X_train, y=Y_train.to_numpy(), batch_size=25, epochs=50)
    sl.success('Training model complete!')

    # import library for MSE
    from sklearn.metrics import mean_squared_error

    sl.subheader('4. Model Performance')
    sl.markdown('**4.1. Training set**')
    Y_train_pred = model.predict(X_train)
    sl.write('Error (MSE or MAE):')
    sl.info( mean_squared_error(Y_train, Y_train_pred) )

    sl.markdown('**4.2. Test set**')
    Y_test_pred = model.predict(X_test)
    sl.write('Error (MSE or MAE):')
    sl.info( mean_squared_error(Y_test, Y_test_pred) )

    sl.subheader('5. Prediction')
    

###########################################
#            Page Settings                #
###########################################
sl.set_page_config(page_title='', layout='wide', initial_sidebar_state='expanded') 
with open('style.css') as f:
    sl.markdown(f'<style>{f.read()}</style', unsafe_allow_html=True)

# Add and image? can add an image here: sl.image("")

### --- Make Data Accessible throughout the whole app
if os.path.exists("sourcedataset.csv"):
    battery_df = pd.read_csv("sourcedataset.csv", index_col=None)

### --- Style
with open('style.css') as f:
    sl.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


### --- FILE UPLOAD & LOAD DATAFRAME
sl.sidebar.header('Upload your CSV file.')
client_file = sl.sidebar.file_uploader(
    label= "Upload your CSV file. (200MB max)",
    type=['csv', 'xlsx']
)


# User wants to use preloaded dataset
if sl.sidebar.button('Use preloaded NASA dataset'): 
    client_file = "discharge_B0005.csv" # store file path  
    battery_df = pd.read_csv(client_file) # load NASA dataset into df
    NASA_file_name = client_file.split("/"[-1]) # store file name
    sl.sidebar.success(f"NASA dataset has been successfully selected.", icon="✅") # Display success message if user selects preloaded dataset button.
    # Create a button to remove the uploaded file
    if sl.sidebar.button("Remove file"):
        os.remove(client_file.name)
        sl.sidebar.write("File removed")

if client_file is not None:
    # print(client_file)
    battery_df = pd.read_csv(client_file)


    # try:
    #     battery_df = pd.read_csv(client_file) # read file
    #     # battery_df.to_csv("sourcedataset.csv", index=None)
    # except Exception as e:
    #     print(e)
    #     battery_df = pd.read_excel(client_file)

###########################################
#             Structure Tabs              #
###########################################
## --- Tabs
tab_headings = [
    "Overview",
    "Profile Report",
    "Prediction"
]

tabs = sl.tabs(tab_headings)

###########################################
#             Overview Tab                #
###########################################
with tabs[0]:

    # Title of Tab: Battery Dataset Dashboard
    sl.write("""
    # Battery Dashboard
    This dashboard analyzes the State of Charge, State of Health, and Remaining Useful LIfe of a battery.
    """)

    if client_file is not None:
        loading_modal(client_file)
        # sl.markdown('**Glimpse of battery dataset**')
        # sl.write(battery_df)
    try:
        # sl.write(battery_df)
        battery_columns = list(battery_df.select_dtypes(['float','int']).columns)
    except Exception as e:
        print(e)
        sl.info('Awaiting for battery CSV file to be uploaded.')

    # select widget for chart type on sidebar
    # chart_type = sl.selectbox(
    #     label="Select desired chart type",
    #     options=["Scatterplots", 'Lineplots', 'Historgram', 'Boxplot']
    # )

    # if chart_type == 'Scatterplots':
    #     sl.subheader("Scatterplot Settings")
    #     try:
    #         x_values = sl.selectbox('X axis', options=battery_columns)
    #         y_values = sl.selectbox('Y axis', options = battery_columns)
    #         plot = px.scatter(data_frame=battery_df, x=x_values, y=y_values)
    if client_file is not None:
        try:

            # display graph
            # sl.markdown('### Capacity Degradation for discharge cycles')
            # sl.plotly_chart(plot)

            ### --- Row A: Metrics
            # Displays total cycles, min temperature, max temperature, and average temperature
            total_cycles=(battery_df['cycle'].max())
            min_temperature=(battery_df['temperature_measured'].min().round(2))
            max_temperature=(battery_df['temperature_measured'].max().round(2))
            average_temperature=(battery_df['temperature_measured'].mean().round(2))

            sl.markdown('### Metrics')
            c1, c2, c3, c4 = sl.columns(4)
            c1.metric("Total Cycles", f'{total_cycles}')
            c2.metric("Min Temperature", f'{min_temperature}' " °F")
            c3.metric("Max Temperature", f'{max_temperature}' " °F")
            c4.metric("Average Temperature", f'{average_temperature}' " °F")

            ### -- Row C: Line graph
            sl.markdown('### Capacity degradation')
            sl.line_chart(battery_df, x="cycle", y="capacity")

            ### -- Display filtered data in a table
            # Create a progress bar based on the selected metric
            col1, col2 = sl.columns(2)

            with col1:
                sl.subheader('State of Charge')
                soc = battery_df['capacity'].iloc[-1] / battery_df['capacity'].max() * 100
                sl.write(f"State of Charge: {soc:.2f}%")
                sl.progress(soc/100)
                import plotly.graph_objs as go
                # Create the progress bar figure
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = soc/100,
                    gauge = {'axis': {'range': [None, 100]},
                            'bar': {'color': 'green', 'thickness': 0.2},
                            'bgcolor': 'white',
                            'borderwidth': 2,
                            'bordercolor': 'gray',
                            'steps': [
                                {'range': [0, 50], 'color': 'red'},
                                {'range': [50, 80], 'color': 'yellow'},
                                {'range': [80, 100], 'color': 'green'}],
                            'threshold': {'line': {'color': 'red', 'width': 2},
                                        'thickness': 0.75,
                                        'value': soc}}))
            
                # Update the layout to remove the axis and legend
                fig.update_layout(paper_bgcolor='white', font_size=16, width=200, height=200,
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False, 
                    xaxis={'visible': False},
                    yaxis={'visible': False})

                # Display the figure
                sl.plotly_chart(fig, use_container_width=True)

            with col2:
                sl.subheader('State of Health')
                soh = (battery_df['voltage_measured'].iloc[-1] * battery_df['temperature_measured'].iloc[-1] * battery_df['current_load'].iloc[-1]) / (battery_df['voltage_measured'].mean() * battery_df['temperature_measured'].mean() * battery_df['current_load'].mean()) * 100
                sl.write(f"State of Health: {soh:.2f}%")
                sl.progress(soh/100)

                # Create the progress bar figure
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = soh/100,
                    gauge = {'axis': {'range': [None, 100]},
                            'bar': {'color': 'green', 'thickness': 0.2},
                            'bgcolor': 'white',
                            'borderwidth': 2,
                            'bordercolor': 'gray',
                            'steps': [
                                {'range': [0, 50], 'color': 'red'},
                                {'range': [50, 80], 'color': 'yellow'},
                                {'range': [80, 100], 'color': 'green'}],
                            'threshold': {'line': {'color': 'red', 'width': 2},
                                        'thickness': 0.75,
                                        'value': soh}}))
            
                # Update the layout to remove the axis and legend
                fig.update_layout(paper_bgcolor='white', font_size=16, width=200, height=200,
                    margin=dict(l=20, r=20, t=20, b=20),
                    showlegend=False, 
                    xaxis={'visible': False},
                    yaxis={'visible': False})

                # Display the figure
                sl.plotly_chart(fig, use_container_width=True)


        except Exception as e:
            print(e)

# Additional Information
sl.sidebar.info("This application allows you to build an automated ML pipeline to evaluate your battery's performance using Streamlit.")

###########################################
#         Profile Report Tab              #
###########################################

### --- Profile Report
with tabs[1]:
    # Title
    sl.write("""
    # Profile Report
    Extended analysis for the dataset provided.
    """)

    if client_file is not None:
        profile_report = battery_df.profile_report()
        # profile_report = battery_df.profile_report( title="Pandas Profiling Report")
        # ProfileReport(battery_df)
        st_profile_report(profile_report)
        

###########################################
#             Prediction Tab              #
###########################################

with tabs[2]:
    # sl.markdown("Prediction Dashboard")
    sl.write("""
    # Battery Prediction
    In this implementation, neural network model is built and trained using Tensorflow.
    Try adjusting the hyperparameters!
    """)
    sl.subheader('1. Dataset')
    # target = sl.selectbox("Select Your Target", battery_df.columns)
    # setup(battery_df, target=target, silent=True)
    # setup_df = pull()
    # sl.info("This is the ML Experiment settings")
    # sl.dataframe(setup_df)
    # best_model = compare_models()
    # compare_df = pull()
    # sl.info("This is the ML Model")
    # sl.dataframe(compare_df)
    # best_model

    if client_file is not None:
        soh_df = compute_soh(battery_df)    # compute soh of battery dataset
        sl.write(battery_df)    # display battery df

    # User wants to use preloaded dataset
    # elif sl.button('Use preloaded NASA dataset'): 
    #     NASA_file_path = "discharge_B0005.csv" # store file path  
    #     battery_df = pd.read_csv(NASA_file_path) # load NASA dataset into df
    #     NASA_file_name = NASA_file_path.split("/"[-1]) # store file name
    #     sl.success(f"NASA dataset,{NASA_file_name}, successfully selected.", icon="✅") # Display success message if user selects preloaded dataset button.
    #     # Create a button to remove the uploaded file
    #     if sl.button("Remove file"):
    #         os.remove(client_file.name)
    #         sl.write("File removed")
    else:
        sl.info('Awaiting for battery CSV file to be uploaded.')



    # Set parameter settings
    sl.subheader('2. Set Parameters')
    split_size = sl.slider('Data split ratio (% for Training Set)', 10, 90, 80, 5)

    # sl.subheader('2.1. Learning Parameters')
    # parameter_n_estimators = sl.slider('Number of estimators (n_estimators)', 0, 1000, 100, 100)
    # parameter_max_features = sl.select_slider('Max features (max_features)', options=['auto', 'sqrt', 'log2'])
    # parameter_min_samples_split = sl.slider('Minimum number of samples required to split an internal node (min_samples_split)', 1, 10, 2, 1)
    # parameter_min_samples_leaf = sl.slider('Minimum number of samples required to be at a leaf node (min_samples_leaf)', 1, 10, 2, 1)

    # sl.subheader('2.2. General Parameters')
    # parameter_random_state = sl.slider('Seed number (random_state)', 0, 1000, 42, 1)
    # parameter_criterion = sl.select_slider('Performance measure (criterion)', options=['mse', 'mae'])
    # parameter_bootstrap = sl.select_slider('Bootstrap samples when building trees (bootstrap)', options=[True, False])
    # parameter_oob_score = sl.select_slider('Whether to use out-of-bag samples to estimate the R^2 on unseen data (oob_score)', options=[False, True])
    # parameter_n_jobs = sl.select_slider('Number of jobs to run in parallel (n_jobs)', options=[1, -1])

    if client_file is not None and sl.button('Build and Train Model'):
        # Build a neural network model
        soh_nn_model(battery_df)


    
        

    
    
    
