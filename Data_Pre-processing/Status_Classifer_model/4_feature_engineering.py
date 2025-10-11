"""
4_feature_engineering.py
------------------------
Purpose:
    - Create new derived features for irrigation prediction
"""

import pandas as pd
import numpy as np

merged_df = pd.read_csv("merged_data.csv")

merged_df['status'] = merged_df['status'].map({'ON': 1, 'OFF': 0})
merged_df['Relative_Soil_Saturation'] = merged_df['soil_moisture'] / merged_df['soil_humidity']
merged_df['temp_diff'] = merged_df['air_temperature_(c)'] - merged_df['temperature']
merged_df['wind_effect'] = merged_df['wind_speed_(km/h)'] * merged_df['wind_gust_(km/h)']
merged_df['Evapotranspiration'] = merged_df['humidity'] * merged_df['temperature']
merged_df['rain_vs_soil'] = merged_df['rainfall'] - merged_df['soil_moisture']
merged_df['np_ratio'] = merged_df['n'] / (merged_df['p'] + 1e-5)
merged_df['nk_ratio'] = merged_df['n'] / (merged_df['k'] + 1e-5)
merged_df['ph_encoded'] = merged_df['ph'].apply(lambda v: 0 if v < 6.5 else (1 if v <= 7.5 else 2))

merged_df.to_csv("feature_engineered_data.csv", index=False)
print("✅ Feature engineering complete!")
