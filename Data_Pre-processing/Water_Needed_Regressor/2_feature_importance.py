# ======================================================
# 📁 FILE: 2_feature_importance.py
# 📌 PURPOSE:
#   - Load trained CatBoost model
#   - Visualize feature importance
# ======================================================

import joblib
import pandas as pd
import matplotlib.pyplot as plt

model = joblib.load('catboost_model.pkl')

X = pd.read_csv('/content/Final_irregation_optimization_data_m2.csv').drop(columns=['status'])

feature_importances = model.get_feature_importance()
feature_names = model.feature_names_

fi_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False).reset_index(drop=True)
print(fi_df)

plt.figure(figsize=(10,6))
plt.barh(fi_df['Feature'], fi_df['Importance'], color='skyblue')
plt.gca().invert_yaxis()
plt.xlabel('Importance Score')
plt.title('Feature Importance - Irrigation Model')
plt.show()
