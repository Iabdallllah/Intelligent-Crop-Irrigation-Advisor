# ===============================
# 📦 IMPORT LIBRARIES
# ===============================
import pandas as pd
import joblib

# ===============================
# 📂 LOAD MODEL & DATA
# ===============================
model = joblib.load('catboost_irrigation_model.pkl')
print("✅ Model loaded successfully.")

new_data = pd.read_csv('new_irrigation_data.csv')  # بيانات جديدة مثلاً

# ===============================
# 🎯 SELECT SAME FEATURES
# ===============================
features = [
    'soil_moisture', 'temperature', 'soil_humidity', 'air_temperature_(c)',
    'wind_speed_(km/h)', 'humidity', 'wind_gust_(km/h)', 'pressure_(kpa)',
    'ph', 'rainfall', 'n', 'p', 'k', 'soil_moisture_diff',
    'Relative_Soil_Saturation', 'temp_diff', 'wind_effect',
    'Evapotranspiration', 'rain_3days', 'rain_vs_soil',
    'np_ratio', 'nk_ratio', 'ph_encoded', 'crop_encoded',
    'moisture_temp_ratio', 'evapo_ratio', 'rain_effect',
    'moisture_change_rate', 'temp_scaled', 'npk_balance', 'wind_ratio'
]

# ===============================
# 🔮 MAKE PREDICTIONS
# ===============================
predictions = model.predict(new_data[features])
new_data['predicted_water_mm'] = predictions

new_data.to_csv('predicted_irrigation_results.csv', index=False)
print("💧 Predictions saved to 'predicted_irrigation_results.csv'.")
