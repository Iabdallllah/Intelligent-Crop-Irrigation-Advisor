# ======================================================
# 📁 FILE: 3_irrigation_npk_calculation.py
# 📌 PURPOSE:
#   - Simulate irrigation & nutrient recommendation
# ======================================================

import pandas as pd
import numpy as np

merged_df = pd.read_csv('/content/Final_irregation_optimization_data_m2.csv')

# Initialize columns
merged_df['recommended_water_mm'] = 0.0
merged_df['soil_moisture_updated'] = merged_df['soil_moisture']
merged_df['recommended_N'] = 0.0
merged_df['recommended_P'] = 0.0
merged_df['recommended_K'] = 0.0

merged_df['crop'].unique()

# Dictionaries (your same code)
crop_Kc = {
    'rice': 1.2,
    'maize': 1.15,
    'chickpea': 0.9,
    'kidneybeans': 0.95,
    'pigeonpeas': 0.9,
    'mothbeans': 0.85,
    'mungbean': 0.85,
    'blackgram': 0.85,
    'lentil': 0.85,
    'pomegranate': 0.9,
    'banana': 1.1,
    'mango': 0.95,
    'grapes': 0.95,
    'watermelon': 0.9,
    'muskmelon': 0.9,
    'apple': 0.95,
    'orange': 0.95,
    'papaya': 1.0,
    'coconut': 1.0,
    'cotton': 1.0,
    'jute': 1.0,
    'coffee': 1.0,
}

crop_NPK_max = {
    'rice': {'N':12, 'P':6, 'K':8},
    'maize': {'N':10, 'P':5, 'K':7},
    'chickpea': {'N':8, 'P':4, 'K':6},
    'kidneybeans': {'N':9, 'P':4, 'K':6},
    'pigeonpeas': {'N':9, 'P':4, 'K':6},
    'mothbeans': {'N':8, 'P':3, 'K':5},
    'mungbean': {'N':8, 'P':3, 'K':5},
    'blackgram': {'N':8, 'P':3, 'K':5},
    'lentil': {'N':8, 'P':3, 'K':5},
    'pomegranate': {'N':10, 'P':5, 'K':7},
    'banana': {'N':10, 'P':5, 'K':8},
    'mango': {'N':10, 'P':5, 'K':7},
    'grapes': {'N':10, 'P':5, 'K':7},
    'watermelon': {'N':9, 'P':4, 'K':6},
    'muskmelon': {'N':9, 'P':4, 'K':6},
    'apple': {'N':10, 'P':5, 'K':7},
    'orange': {'N':10, 'P':5, 'K':8},
    'papaya': {'N':10, 'P':5, 'K':7},
    'coconut': {'N':9, 'P':4, 'K':7},
    'cotton': {'N':8, 'P':4, 'K':6},
    'jute': {'N':8, 'P':4, 'K':6},
    'coffee': {'N':10, 'P':5, 'K':8},
}

root_zone_depth = 200
field_capacity = 100

def safe_divide(a, b):
    if b == 0 or pd.isna(b):
        return a
    return a / b

def calculate_irrigation(row):
    if not row['status']:
        return 0
    crop = row['crop']
    Kc = crop_Kc.get(crop, 1.0)
    ETc = row['Evapotranspiration'] * Kc
    soil_water_available = (row['soil_moisture_updated'] / 100) * root_zone_depth
    rain_effect = row['rain_3days']
    water_deficit = max(ETc - soil_water_available - rain_effect, 0)

    if row['soil_moisture_updated'] < 30:
        water_deficit *= 1.2
    elif row['soil_moisture_updated'] > 70:
        water_deficit *= 0.5

    max_irrigation = 50
    return round(min(water_deficit, max_irrigation), 2)

def calculate_npk(row, irrigation_mm):
    crop = row['crop']
    N_max = crop_NPK_max.get(crop, {'N':10,'P':5,'K':7})['N']
    P_max = crop_NPK_max.get(crop, {'N':10,'P':5,'K':7})['P']
    K_max = crop_NPK_max.get(crop, {'N':10,'P':5,'K':7})['K']

    N = safe_divide(N_max, row.get('np_ratio',1))
    P = safe_divide(P_max, row.get('npk_balance',1))
    K = safe_divide(K_max, row.get('nk_ratio',1))

    ph = row.get('ph',7)
    if ph < 5.5 or ph > 7.5:
        N *= 0.8
        P *= 0.8
        K *= 0.8

    factor = irrigation_mm / 50
    N *= factor
    P *= factor
    K *= factor

    return round(N,2), round(P,2), round(K,2)

water_list = []
soil_moisture_list = []
N_list, P_list, K_list = [], [], []

for idx, row in merged_df.iterrows():
    water = calculate_irrigation(row)
    water_list.append(water)

    new_moisture = row['soil_moisture_updated'] + (water + row['rain_3days']) * 100 / root_zone_depth
    new_moisture = min(new_moisture, field_capacity)
    soil_moisture_list.append(new_moisture)

    N, P, K = calculate_npk(row, water)
    N_list.append(N)
    P_list.append(P)
    K_list.append(K)

    if idx+1 < len(merged_df):
        merged_df.at[idx+1, 'soil_moisture_updated'] = new_moisture

merged_df['recommended_water_mm'] = water_list
merged_df['soil_moisture_updated'] = soil_moisture_list
merged_df['recommended_N'] = N_list
merged_df['recommended_P'] = P_list
merged_df['recommended_K'] = K_list
merged_df.to_csv('irrigation_npk_scientific_safe.csv', index=False)
merged_df.head()
