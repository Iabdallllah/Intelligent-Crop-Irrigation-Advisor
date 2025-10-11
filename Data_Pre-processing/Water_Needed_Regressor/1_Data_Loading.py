# ======================================================
# 📁 FILE: 1_data_cleaning.py
# 📌 PURPOSE:
#   - Load the datasets (Crop_recommendation & TARP)
#   - Detect missing values
#   - Handle missing data using KNN Imputer
#   - Save the cleaned dataset
# ======================================================

import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error

merged_df = pd.read_csv('/content/Final_irregation_optimization_data_m2.csv')

merged_df.head()
merged_df.info()
merged_df.describe()
merged_df.isnull().sum()
merged_df.duplicated().sum()
merged_df.columns
