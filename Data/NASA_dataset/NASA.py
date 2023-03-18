#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import pandas as pd
from scipy.io import loadmat
from pandas import DataFrame


# # Functions

# In[2]:


#define a function for extracting discharge and charge data
def load_discharge_data(battery):
  mat = loadmat(battery + '.mat') #get the .mat file
  print('Total data in dataset: ', len(mat[battery][0, 0]['cycle'][0])) #get the length of the data from number of cycles
  c = 0 #set a variable to zero
  disdataset = [] #create an empty list for discharge data
  capacity_data = []
  
  for i in range(len(mat[battery][0, 0]['cycle'][0])):
    row = mat[battery][0, 0]['cycle'][0, i] #get each row of the cycle
    if row['type'][0] == 'discharge': #if the row is a dicharge cycle
      ambient_temperature = row['ambient_temperature'][0][0] #get temp,date_time stamp,capacity,voltage,current etc,.
      date_time = datetime.datetime(int(row['time'][0][0]),
                               int(row['time'][0][1]),
                               int(row['time'][0][2]),
                               int(row['time'][0][3]),
                               int(row['time'][0][4])) + datetime.timedelta(seconds=int(row['time'][0][5]))
      data = row['data']
      capacity = data[0][0]['Capacity'][0][0]
      for j in range(len(data[0][0]['Voltage_measured'][0])):
        voltage_measured = data[0][0]['Voltage_measured'][0][j]
        current_measured = data[0][0]['Current_measured'][0][j]
        temperature_measured = data[0][0]['Temperature_measured'][0][j]
        current_load = data[0][0]['Current_load'][0][j]
        voltage_load = data[0][0]['Voltage_load'][0][j]
        time = data[0][0]['Time'][0][j]
        disdataset.append([c + 1, ambient_temperature, date_time, capacity,
                        voltage_measured, current_measured,
                        temperature_measured, current_load,
                        voltage_load, time])
        capacity_data.append([c + 1, ambient_temperature, date_time, capacity])
      c = c + 1
  print(disdataset[0])
  return [pd.DataFrame(data=disdataset,
                       columns=['cycle', 'ambient_temperature', 'datetime',
                                'capacity', 'voltage_measured',
                                'current_measured', 'temperature_measured',
                                'current_load', 'voltage_load', 'time']),
          pd.DataFrame(data=capacity_data,
                       columns=['cycle', 'ambient_temperature', 'datetime',
                                'capacity'])]

def load_charge_data(battery): #similarly write a fn for charge data
  mat = loadmat(battery + '.mat')
  c = 0
  chdataset = []
  
  for i in range(len(mat[battery][0, 0]['cycle'][0])):
    row = mat[battery][0, 0]['cycle'][0, i]
    if row['type'][0] == 'charge' :
            
      ambient_temperature = row['ambient_temperature'][0][0]
      date_time = datetime.datetime(int(row['time'][0][0]),
                               int(row['time'][0][1]),
                               int(row['time'][0][2]),
                               int(row['time'][0][3]),
                               int(row['time'][0][4])) + datetime.timedelta(seconds=int(row['time'][0][5]))
      data = row['data']
      for j in range(len(data[0][0]['Voltage_measured'][0])):
        voltage_measured = data[0][0]['Voltage_measured'][0][j]
        current_measured = data[0][0]['Current_measured'][0][j]
        temperature_measured = data[0][0]['Temperature_measured'][0][j]
        current_charge = data[0][0]['Current_charge'][0][j]
        voltage_charge = data[0][0]['Voltage_charge'][0][j]
        time = data[0][0]['Time'][0][j]
        chdataset.append([c + 1, ambient_temperature, date_time,
                        voltage_measured, current_measured,
                        temperature_measured, current_charge,
                        voltage_charge, time])
      c = c + 1
  print(chdataset[788])
  return chdataset


# # Load and Convert Mat Datsets to Dataframe

# In[3]:


charge_mat5 = load_charge_data('B0005')
charge_df5 =pd.DataFrame(data=charge_mat5,columns=['cycle', 'ambient_temperature', 'datetime', 
                                'voltage_measured','current_measured',
                                'temperature_measured','current',
                                'voltage', 'time'])
pd.set_option('display.max_columns', 10)
charge_df5


# In[4]:


charge_df5.describe()


# In[5]:


discharge_df5, capacity_df5 = load_discharge_data('B0005')
pd.set_option('display.max_columns', 10)
discharge_df5


# In[6]:


capacity_df5


# In[7]:


print(capacity_df5.dtypes)


# In[11]:


discharge_df5.to_csv('discharge_B0005.csv')


# In[12]:


discharge_df5.describe()


# In[13]:


cycling_df5 = pd.concat([charge_df5, discharge_df5])
cycling_df5=cycling_df5.sort_values(['cycle', 'datetime'], ascending=[True, True])
cycling_df5


# # Export Dataframes to CSV 

# In[14]:


cycling_df5.to_csv('B0005.csv')


# # Data Visualization

# 

# In[15]:


# Libraries
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# # Distributions of voltage, current, and temperature in the dataset

# ### (A) Dataset B0005 

# In[16]:


sns.displot(cycling_df5['voltage_measured'], stat="density")
sns.displot(cycling_df5['current_measured'], stat="density")
sns.displot(cycling_df5['temperature_measured'], stat="density")


# # Capacity Degradation of datasets B0005

# In[17]:


# B0005
graph_df5 = capacity_df5.loc[(capacity_df5['cycle']>=1),['cycle','capacity']]
sns.set_style("darkgrid")
plt.figure(figsize=(12, 8))
plt.plot(graph_df5['cycle'], graph_df5['capacity'])

# make y-axis ticks legible
plt.ylabel('Capacity (Ahr)')

# make x-axis ticks legible
adf = plt.gca().get_xaxis().get_major_formatter()
plt.xlabel('Cycles')
plt.title('Capacity degradation at ambient temperature of 24 degrees Celcius')
plt.show()


# # Calculate SoH

# In[ ]:





# In[18]:


# SoH for B0005
attributes = ['cycle', 'datetime', 'capacity']
SoH_df5 = capacity_df5[attributes]
initial_capacity_df5 = SoH_df5['capacity'][0]
print(initial_capacity_df5)
for i in range(len(SoH_df5)):
    SoH_df5['SoH']=(SoH_df5['capacity'])/initial_capacity_df5
print(SoH_df5.head(5))
display(SoH_df5)


# In[ ]:





# # SoH Visualization

# In[19]:


plot_df = SoH_df5.loc[(SoH_df5['cycle']>=1),['cycle','SoH']]
sns.set_style("white")
plt.figure(figsize=(8, 5))
plt.plot(SoH_df5['cycle'], SoH_df5['SoH'])

# make x-axis ticks legible
adf = plt.gca().get_xaxis().get_major_formatter()
plt.ylabel('SoH')
plt.xlabel('Cycle')
plt.title('SoH vs. cycle')


# # SoH Training

# In[20]:


from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import LSTM
from tensorflow.keras.optimizers import Adam
import numpy as np


# In[21]:


C5 = discharge_df5['capacity'][0]
soh = []
for i in range(len(discharge_df5)):
  soh.append([discharge_df5['capacity'][i] / C5])
soh = pd.DataFrame(data=soh, columns=['SoH'])

attribs=['capacity', 'voltage_measured', 'current_measured',
         'temperature_measured', 'current_load', 'voltage_load', 'time']
train_dataset = discharge_df5[attribs]
sc = MinMaxScaler(feature_range=(0,1))
train_dataset = sc.fit_transform(train_dataset)
print(train_dataset.shape)
print(soh.shape)


# In[22]:


print(soh)


# In[23]:


model = Sequential()
model.add(Dense(8, activation='relu', input_dim=train_dataset.shape[1]))
model.add(Dense(8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dropout(rate=0.25))
model.add(Dense(1))
model.summary()
model.compile(optimizer=Adam(beta_1=0.9, beta_2=0.999, epsilon=1e-08), loss='mean_absolute_error')


# In[24]:


model.fit(x=train_dataset, y=soh.to_numpy(), batch_size=25, epochs=50)


# # Testing correctness of SoH prediction

# In[20]:


dataset_val, capacity_val = load_discharge_data('B0005')
attrib=['cycle', 'datetime', 'capacity']
dis_ele = capacity_val[attrib]
C5_new = dis_ele['capacity'][0]
for i in range(len(dis_ele)):
    dis_ele['SoH']=(dis_ele['capacity']) / C5_new
print(dataset_val.head(5))
print(dis_ele.head(5))


# In[21]:


from sklearn.metrics import mean_squared_error


# In[23]:


attrib=['capacity', 'voltage_measured', 'current_measured',
        'temperature_measured', 'current_load', 'voltage_load', 'time']
soh_pred = model.predict(sc.fit_transform(dataset_val[attrib]))
print(soh_pred.shape)

C = dataset_val['capacity'][0]
soh = []
for i in range(len(dataset_val)):
  soh.append(dataset_val['capacity'][i] / C5)
new_soh = dataset_val.loc[(dataset_val['cycle'] >= 1), ['cycle']]
new_soh['SoH'] =  soh
new_soh['NewSoH'] = soh_pred
new_soh = new_soh.groupby(['cycle']).mean().reset_index()
print(new_soh.head(10))
rms = np.sqrt(mean_squared_error(new_soh['SoH'], new_soh['NewSoH']))
print('Root Mean Square Error: ', rms)


# In[27]:


plot_df = new_soh.loc[(new_soh['cycle']>=1),['cycle','SoH', 'NewSoH']]
sns.set_style("white")
plt.figure(figsize=(16, 10))
plt.plot(plot_df['cycle'], plot_df['SoH'], label='SoH')
plt.plot(plot_df['cycle'], plot_df['NewSoH'], label='Predicted SoH')
#Draw threshold
#plt.plot([0.,len(capacity)], [0.70, 0.70], label='Threshold')
plt.ylabel('SOH')
# make x-axis ticks legible
adf = plt.gca().get_xaxis().get_major_formatter()
plt.xlabel('cycle')
plt.legend()
plt.title('Discharge B0005')


# In[ ]:




