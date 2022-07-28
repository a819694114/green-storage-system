# Li-ion Battery Aging Datasets


This data set has been collected from a custom built battery prognostics testbed at the NASA Ames Prognostics Center of Excellence (PCoE). Li-ion batteries were run through 3 different operational profiles (charge, discharge and Electrochemical Impedance Spectroscopy) at different temperatures. Discharges were carried out at different current load levels until the battery voltage fell to preset voltage thresholds. Some of these thresholds were lower than that recommended by the OEM (2.7 V) in order to induce deep discharge aging effects. Repeated charge and discharge cycles result in accelerated aging of the batteries. The experiments were stopped when the batteries reached the end-of-life (EOL) criteria of 30% fade in rated capacity (from 2 Ah to 1.4 Ah).



**Data Acquisition:**

The testbed comprises:

* Commercially available Li-ion 18650 sized rechargeable batteries,
* Programmable 4-channel DC electronic load,
* Programmable 4-channel DC power supply,
* Voltmeter, ammeter and thermocouple sensor suite,
* Custom EIS equipment,
* Environmental chamber to impose various operational conditions,
* PXI chassis based DAQ and experiment control, and



MATLAB based experiment control, data acquisition and prognostics algorithm evaluation setup (appx. data acquisition rate is 10Hz).



**Parameter Description:**

Data Structure:

cycle: top level structure array containing the charge, discharge and impedance operations

type: operation type, can be charge, discharge or impedance

ambient_temperature: ambient temperature (degree C)

time: the date and time of the start of the cycle, in MATLAB date vector format

data: data structure containing the measurements

for charge the fields are:

Voltage_measured: Battery terminal voltage (Volts)

Current_measured: Battery output current (Amps)

Temperature_measured: Battery temperature (degree C)

Current_charge: Current measured at charger (Amps)

Voltage_charge: Voltage measured at charger (Volts)

Time: Time vector for the cycle (secs)

for discharge the fields are:

Voltage_measured: Battery terminal voltage (Volts)

Current_measured: Battery output current (Amps)

Temperature_measured: Battery temperature (degree C)



Current_charge: Current measured at load (Amps)

Voltage_charge: Voltage measured at load (Volts)

Time: Time vector for the cycle (secs)

Capacity: Battery capacity (Ahr) for discharge till 2.7V

for impedance the fields are:

Sense_current: Current in sense branch (Amps)

Battery_current: Current in battery branch (Amps)

Current_ratio: Ratio of the above currents

Battery_impedance: Battery impedance (Ohms) computed from raw data

Rectified_impedance: Calibrated and smoothed battery impedance (Ohms)

Re: Estimated electrolyte resistance (Ohms)



Rct: Estimated charge transfer resistance (Ohms)

**Intended Use:**

The data sets can serve for a variety of purposes. Because these are essentially a large number of Run-to-Failure time series, the data can be set for development of prognostic algorithms. In particular, due to the differences in depth-of-discharge (DOD), the duration of rest periods and intrinsic variability, no two cells have the same state-of-life (SOL) at the same cycle index. The aim is to be able to manage this uncertainty, which is representative of actual usage, and make reliable predictions of Remaining Useful Life (RUL) in both the End-of-Discharge (EOD) and End-of-Life (EOL) contexts.
