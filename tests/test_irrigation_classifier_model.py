# ===============================
# 🧪 TEST MODEL SCRIPT (Full Version)
# ===============================
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ===============================
# 📂 LOAD TEST DATA
# ===============================
# Replace with your dataset path if needed
# Make sure the dataset contains the same features used during training
merged_df = pd.read_csv("your_dataset.csv")

important_features = [
    'soil_moisture', 'temperature', 'soil_humidity', 'Relative_Soil_Saturation',
    'temp_diff', 'Evapotranspiration', 'rain_vs_soil', 'rainfall', 'ph_encoded',
    'n', 'p', 'k', 'np_ratio', 'nk_ratio', 'crop_encoded', 'rain_3days',
    'moisture_temp_ratio', 'evapo_ratio', 'rain_effect', 'moisture_change_rate',
    'temp_scaled', 'npk_balance', 'wind_ratio'
]

X = merged_df[important_features].fillna(merged_df[important_features].mean())

# Check if dataset has labels
has_labels = 'status' in merged_df.columns
if has_labels:
    y = merged_df['status']

# ===============================
# 💾 LOAD TRAINED MODEL
# ===============================
print("🔹 Loading trained CatBoost model...")
model = joblib.load("catboost_model.pkl")

# ===============================
# 🔮 MAKE PREDICTIONS
# ===============================
print("🔹 Making predictions...")
predictions = model.predict(X)

# ===============================
# 📊 EVALUATE (IF LABELS AVAILABLE)
# ===============================
if has_labels:
    acc = accuracy_score(y, predictions)
    print(f"\n✅ Test Accuracy: {acc:.4f}")
    print("\nClassification Report:")
    print(classification_report(y, predictions))

    # ===============================
    # 🎯 CONFUSION MATRIX
    # ===============================
    cm = confusion_matrix(y, predictions)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png")
    print("📊 Confusion matrix saved as 'confusion_matrix.png'")
    plt.show()

else:
    print("\n⚠️ No labels found in dataset — showing sample predictions only:\n")
    print(predictions[:10])

# ===============================
# 🌟 FEATURE IMPORTANCE PLOT
# ===============================
try:
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x='Importance', y='Feature', data=feature_importance.head(15), palette="viridis")
    plt.title("Top 15 Important Features")
    plt.tight_layout()
    plt.savefig("feature_importance.png")
    print("🌟 Feature importance chart saved as 'feature_importance.png'")
    plt.show()

except AttributeError:
    print("⚠️ Feature importance not available for this model type.")

# ===============================
# 💾 SAVE TEST RESULTS
# ===============================
pd.DataFrame({
    'Predicted_Status': predictions
}).to_csv("test_predictions.csv", index=False)

print("\n📁 Test results saved to 'test_predictions.csv'")
