import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../mlflow_tools'))
from mlflow_config import setup_mlflow, log_dataset_info

# Setup MLflow
setup_mlflow('crop_recommendation')

# Start MLflow run
with mlflow.start_run(run_name="RandomForest_Crop_Recommendation"):
    
    # Log parameters
    mlflow.log_param("model_type", "RandomForestClassifier")
    mlflow.log_param("n_estimators", 200)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("test_size", 0.2)
    
    # Load dataset from correct path
    df = pd.read_csv("../../data/crop_data.csv")
    print(f"Data loaded successfully! Shape: {df.shape}")
    print(f"Available crops: {df['label'].unique()}")
    
    # Log dataset info
    log_dataset_info(df, "crop_dataset")
    mlflow.log_param("num_crops", len(df['label'].unique()))
    mlflow.log_param("crops_list", list(df['label'].unique()))
    
    X = df[['N','P','K','temperature','humidity','ph','rainfall']]
    y = df['label']
    
    # Log features
    mlflow.log_param("features", list(X.columns))
    mlflow.log_param("num_features", len(X.columns))
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    mlflow.log_param("train_samples", X_train.shape[0])
    mlflow.log_param("test_samples", X_test.shape[0])
    
    # Train model
    print("Training Random Forest model...")
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"Model Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)
    mlflow.log_metric("f1_score", f1)
    
    # Log feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for idx, row in feature_importance.iterrows():
        mlflow.log_metric(f"importance_{row['feature']}", row['importance'])
    
    # Save and log classification report
    report = classification_report(y_test, y_pred)
    with open("classification_report.txt", "w") as f:
        f.write(report)
    mlflow.log_artifact("classification_report.txt")
    os.remove("classification_report.txt")
    
    # Log model with signature
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.sklearn.log_model(
        model,
        "crop_recommendation_model",
        signature=signature,
        registered_model_name="CropRecommendationModel"
    )
    
    # Save model locally
    joblib.dump(model, "crop_model.pkl")
    mlflow.log_artifact("crop_model.pkl")
    print("Model saved as crop_model.pkl")
    
    print("\n✅ Training completed successfully!")
    print(f"🔗 MLflow Run ID: {mlflow.active_run().info.run_id}")
    print("📊 View results: mlflow ui")
