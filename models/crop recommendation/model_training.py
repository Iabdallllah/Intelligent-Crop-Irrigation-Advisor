import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset from correct path
df = pd.read_csv("../../data/crop_data.csv")
print(f"Data loaded successfully! Shape: {df.shape}")
print(f"Available crops: {df['label'].unique()}")

X = df[['N','P','K','temperature','humidity','ph','rainfall']]
y = df['label']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Training set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Train model
print("Training Random Forest model...")
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

# Save model
joblib.dump(model, "crop_model.pkl")
print("Model saved as crop_model.pkl")
print("Training completed successfully!")
