"""
3_data_merging.py
-----------------
Purpose:
    - Merge TARP and Crop datasets using Nearest Neighbors
"""

import pandas as pd
from sklearn.neighbors import NearestNeighbors

big_df = pd.read_csv("outlier_free_data.csv")
small_df = pd.read_csv("cleaned_small_data.csv")

big_df.columns = big_df.columns.str.strip().str.lower().str.replace(' ', '_')
small_df.columns = small_df.columns.str.strip().str.lower().str.replace(' ', '_')

small_df = small_df.rename(columns={'label': 'crop'})

common_cols = ['temperature', 'humidity', 'ph', 'rainfall']
big_df_clean = big_df.dropna(subset=common_cols)
small_df_clean = small_df.dropna(subset=common_cols)

nn = NearestNeighbors(n_neighbors=1)
nn.fit(small_df_clean[common_cols])

distances, indices = nn.kneighbors(big_df_clean[common_cols])
matched_small = small_df_clean.iloc[indices.flatten()].reset_index(drop=True)

for col in ['n', 'p', 'k', 'temperature', 'humidity', 'ph', 'rainfall']:
    big_df_clean[col] = big_df_clean[col].fillna(matched_small[col])

big_df_clean['crop'] = matched_small['crop']
big_df_clean.to_csv("merged_data.csv", index=False)

print("✅ Datasets merged successfully!")
