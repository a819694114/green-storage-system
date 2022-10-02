# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 20:45:36 2022

@author: xurui
"""

# first run **zip_to_npy.py** to extract all the files

import numpy as np
import pandas as pd
import os
import glob

base_dir = 'D:\research\green storage\lead acid'
os.chdir(base_dir)
files = glob.glob('.\*.npy') # all the npy files

df0 = pd.DataFrame(np.load(files[0]), columns = ['TIMESTAMP', 'Current_A', 'Voltage_V', 'Temperature_C'])
df0['Datetime'] = pd.to_datetime(df0['TIMESTAMP'], unit='s')

# if save file in csv format, file size is 73.8 MB. While in npy format, file size is 24 MB.


