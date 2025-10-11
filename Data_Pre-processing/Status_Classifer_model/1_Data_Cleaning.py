"""
1_data_cleaning.py
------------------
Purpose:
    - Load Crop_recommendation.csv & TARP.csv
    - Detect & handle missing values using KNN Imputer
"""

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# Load datasets
small_df = pd.read_csv('Crop_recommendation.csv')
big_df = pd.read_csv('TARP.csv')

# Detect missing values
missing_cols = big_df.columns[big_df.isnull().any()]
print("Columns with missing values:", list(missing_cols))

# KNN Imputer test
sample = big_df[missing_cols].dropna()
if len(sample) > 1000:
    sample = sample.sample(1000, random_state=42)

masked_sample = sample.copy()
mask = np.random.rand(*sample.shape) < 0.1
masked_sample[mask] = np.nan

errors = {}
for k in [2, 3, 5, 7, 9, 11]:
    imputer = KNNImputer(n_neighbors=k)
    imputed = imputer.fit_transform(masked_sample)
    mse = mean_squared_error(sample.values[~mask], imputed[~mask])
    errors[k] = mse
    print(f"K={k} --> MSE={mse:.5f}")

best_k = min(errors, key=errors.get)
print("✅ Best K:", best_k)

plt.plot(list(errors.keys()), list(errors.values()), marker='o')
plt.xlabel("K")
plt.ylabel("MSE")
plt.title("Best K for KNN Imputer")
plt.show()

# Apply imputer
numeric_cols = big_df.select_dtypes(include=[np.number]).columns
imputer = KNNImputer(n_neighbors=best_k)
big_df[numeric_cols] = imputer.fit_transform(big_df[numeric_cols])

big_df.to_csv("cleaned_big_data.csv", index=False)
small_df.to_csv("cleaned_small_data.csv", index=False)

print("✅ Cleaned data saved!")

