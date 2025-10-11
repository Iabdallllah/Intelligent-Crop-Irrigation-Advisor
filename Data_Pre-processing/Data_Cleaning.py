# ======================================================
# 📁 FILE: 1_data_cleaning.py
# 📌 PURPOSE:
#   - Load the datasets (Crop_recommendation & TARP)
#   - Detect missing values
#   - Handle missing data using KNN Imputer
#   - Detect and handle outliers logically
# ======================================================

# Install CatBoost (required later in the pipeline)
!pip install catboost

# ======================================================
# 📦 IMPORTS
# ======================================================
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================================
# 📊 LOAD DATASETS
# ======================================================

# Small dataset (crop recommendation)
small_df = pd.read_csv('/content/sample_data/Crop_recommendation.csv')
print("✅ Crop Recommendation Data Loaded")
small_df.info()

# Large dataset (TARP sensor data)
big_df = pd.read_csv('/content/sample_data/TARP.csv')
print("✅ TARP Data Loaded")
big_df.info()

# ======================================================
# 🧩 HANDLE MISSING VALUES USING KNN IMPUTER
# ======================================================

# Identify columns with missing values
missing_cols = big_df.columns[big_df.isnull().any()]
print("Columns with missing values:", list(missing_cols))

# Take a random sample to test KNN performance
sample = big_df[missing_cols].dropna()
if len(sample) > 1000:
    sample = sample.sample(1000, random_state=42)
print("Sample shape for imputation test:", sample.shape)

# Mask 10% of the sample to simulate missing data
masked_sample = sample.copy()
mask = np.random.rand(*sample.shape) < 0.1
masked_sample[mask] = np.nan
print("Number of hidden (masked) values:", mask.sum())

# Check for duplicates
duplicates_ratio = big_df.duplicated().mean()
print(f"Duplicate rows ratio: {duplicates_ratio:.2%}")

# Evaluate KNN Imputer with different k values
errors = {}
for k in [2, 3, 5, 7, 9, 11]:
    imputer = KNNImputer(n_neighbors=k)
    imputed = imputer.fit_transform(masked_sample)
    mse = mean_squared_error(sample.values[~mask], imputed[~mask])
    errors[k] = mse
    print(f"K={k} --> MSE={mse:.5f}")

# Validate the best K with another random masking test
mask = np.random.rand(*sample.shape) < 0.05
masked_sample = sample.copy()
masked_sample[mask] = np.nan
imputer = KNNImputer(n_neighbors=5)
imputed = imputer.fit_transform(masked_sample)
mse = mean_squared_error(sample.values[mask], imputed[mask])
print(f"Second test MSE (K=5): {mse}")

# Select best k
best_k = min(errors, key=errors.get)
print("\n✅ Best K value:", best_k)

# Plot MSE vs K
plt.figure(figsize=(8, 5))
plt.plot(list(errors.keys()), list(errors.values()), marker='o')
plt.xlabel('K (number of neighbors)')
plt.ylabel('Mean Squared Error')
plt.title('Choosing the Best K for KNN Imputer')
plt.grid(True)
plt.show()

# ======================================================
# 🧮 IMPUTE MISSING VALUES IN BIG DATASET
# ======================================================
numeric_columns = big_df.select_dtypes(include=[np.number]).columns
non_numeric_columns = big_df.select_dtypes(exclude=[np.number]).columns

numeric_df = big_df[numeric_columns]
imputer = KNNImputer(n_neighbors=best_k)
imputed_array = imputer.fit_transform(numeric_df)
imputed_df = pd.DataFrame(imputed_array, columns=numeric_columns)

# Combine imputed numeric with original categorical columns
big_df = pd.concat(
    [imputed_df, big_df[non_numeric_columns].reset_index(drop=True)],
    axis=1
)
print("✅ Missing values imputed successfully.")
big_df.info()

# ======================================================
# 📈 OUTLIER DETECTION
# ======================================================
plt.figure(figsize=(15, 10))
for i, col in enumerate(numeric_columns, 1):
    plt.subplot(4, 4, i)
    sns.boxplot(x=big_df[col], color='skyblue')
    plt.title(col)
plt.tight_layout()
plt.show()

# Count outliers per column (using IQR)
outliers_info = {}
for col in numeric_columns:
    Q1 = big_df[col].quantile(0.25)
    Q3 = big_df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower, upper = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    outliers = big_df[(big_df[col] < lower) | (big_df[col] > upper)]
    outliers_info[col] = len(outliers)

outliers_df = pd.DataFrame(list(outliers_info.items()), columns=['Column', 'Outlier Count'])
outliers_df.sort_values(by='Outlier Count', ascending=False)

# ======================================================
# ⚙️ LOGICAL LIMITS FOR OUTLIERS
# ======================================================
logical_limits = {
    "Air temperature (C)": (0, 50),
    "Wind speed (Km/h)": (0, 120),
    "Wind gust (Km/h)": (0, 150),
    "Air humidity (%)": (0, 100),
    "Pressure (KPa)": (90, 110),
    "ph": (3, 9),
    "rainfall": (0, 300),
    "N": (0, 150),
    "P": (0, 150),
    "K": (0, 200),
    "Soil Moisture": (0, 100),
    "Soil Humidity": (0, 100),
    "Temperature": (0, 50),
}

true_outliers = {}
for col, (low, high) in logical_limits.items():
    if col in big_df.columns:
        mask = (big_df[col] < low) | (big_df[col] > high)
        outliers = big_df.loc[mask, col]
        true_outliers[col] = outliers

for col, outliers in true_outliers.items():
    print(f"\n{col} — True outliers count: {len(outliers)}")
    if len(outliers) > 0:
        print(outliers.head(10))

# ======================================================
# 🧴 REPLACE OUTLIERS WITH MEDIAN VALUES
# ======================================================
big_df.loc[big_df["ph"] > 9, "ph"] = big_df["ph"].median()
big_df.loc[big_df["K"] > 200, "K"] = big_df["K"].median()

# Final check for logical range validity
for col, (low, high) in logical_limits.items():
    if col in big_df.columns:
        mask = (big_df[col] < low) | (big_df[col] > high)
        outliers = big_df.loc[mask, col]
        print(f"\n{col} — Remaining outliers: {len(outliers)}")

print("\n✅ Data cleaning completed successfully.")
