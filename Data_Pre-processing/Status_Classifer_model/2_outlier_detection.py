"""
2_outlier_detection.py
----------------------
Purpose:
    - Detect and handle outliers logically
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

big_df = pd.read_csv("cleaned_big_data.csv")

numeric_cols = big_df.select_dtypes(include='number').columns

# Visual inspection
plt.figure(figsize=(15, 10))
for i, col in enumerate(numeric_cols[:16], 1):
    plt.subplot(4, 4, i)
    sns.boxplot(x=big_df[col], color='skyblue')
    plt.title(col)
plt.tight_layout()
plt.show()

# Logical limits
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
    "K": (0, 200)
}

for col, (low, high) in logical_limits.items():
    if col in big_df.columns:
        outliers = big_df[(big_df[col] < low) | (big_df[col] > high)]
        print(f"{col} - True outliers: {len(outliers)}")
        big_df.loc[big_df[col] < low, col] = big_df[col].median()
        big_df.loc[big_df[col] > high, col] = big_df[col].median()

big_df.to_csv("outlier_free_data.csv", index=False)
print("✅ Outliers handled successfully!")
