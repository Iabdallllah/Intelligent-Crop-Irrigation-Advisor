import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
import sys
import os

# Install required packages if not available
def install_packages():
    """Install required packages if not available"""
    required_packages = ['matplotlib', 'seaborn']
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            os.system(f"{sys.executable} -m pip install {package}")

# Install packages
install_packages()

import matplotlib.pyplot as plt
import seaborn as sns

def load_model_and_data():
    """Load model and test data"""
    try:
        # Load model from correct path (using absolute paths from project root)
        model_path = "models/crop recommendation/crop_model.pkl"
        model = joblib.load(model_path)
        print("✅ Model loaded successfully")
        
        # Load data from correct path
        data_path = "data/crop_data.csv"
        df = pd.read_csv(data_path)
        print("✅ Data loaded successfully")
        
        return model, df
    except FileNotFoundError as e:
        print(f"❌ Error loading file: {e}")
        print("📂 Please ensure the following files exist:")
        print("   - models/crop recommendation/crop_model.pkl")
        print("   - data/crop_data.csv")
        print("📁 Current working directory should be the project root")
        return None, None

def test_model_accuracy(model, df):
    """Test model accuracy"""
    print("\n🔍 Testing model accuracy...")
    
    # Prepare data
    X = df[['N','P','K','temperature','humidity','ph','rainfall']]
    y = df['label']
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Calculate accuracy
    accuracy = accuracy_score(y, y_pred)
    print(f"📊 Model accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    return y, y_pred

def test_cross_validation(model, df):
    """Test cross validation"""
    print("\n🔄 Testing cross validation...")
    
    X = df[['N','P','K','temperature','humidity','ph','rainfall']]
    y = df['label']
    
    # 5-fold cross validation
    cv_scores = cross_val_score(model, X, y, cv=5)
    
    print(f"📈 Cross validation results:")
    print(f"   Mean accuracy: {cv_scores.mean():.4f}")
    print(f"   Standard deviation: {cv_scores.std():.4f}")
    print(f"   Max accuracy: {cv_scores.max():.4f}")
    print(f"   Min accuracy: {cv_scores.min():.4f}")

def test_specific_predictions(model):
    """Test specific predictions"""
    print("\n🌱 Testing specific predictions...")
    
    # Diverse test samples
    test_samples = [
        {
            'name': 'Rice sample',
            'data': [90, 42, 43, 21, 82, 6.5, 200],
            'expected': 'rice'
        },
        {
            'name': 'Maize sample',
            'data': [80, 40, 20, 27, 65, 6.0, 60],
            'expected': 'maize'
        },
        {
            'name': 'Cotton sample',
            'data': [120, 40, 40, 25, 80, 8.0, 100],
            'expected': 'cotton'
        },
        {
            'name': 'Lentil sample',
            'data': [20, 60, 20, 24, 65, 7.0, 65],
            'expected': 'lentil'
        }
    ]
    
    for sample in test_samples:
        prediction = model.predict([sample['data']])[0]
        probability = model.predict_proba([sample['data']]).max()
        
        status = "✅" if prediction == sample['expected'] else "❌"
        print(f"{status} {sample['name']}: Predicted = {prediction}, Expected = {sample['expected']}, Probability = {probability:.3f}")

def generate_classification_report(y_true, y_pred):
    """Generate classification report"""
    print("\n📋 Detailed Classification Report:")
    print("="*50)
    report = classification_report(y_true, y_pred)
    print(report)

def plot_confusion_matrix(y_true, y_pred):
    """Plot confusion matrix"""
    print("\n📊 Creating confusion matrix...")
    
    try:
        # Calculate confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Create plot
        plt.figure(figsize=(12, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('Confusion Matrix - Crop Recommendation Model')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        print("✅ Confusion matrix saved as confusion_matrix.png")
        plt.show()
        
    except Exception as e:
        print(f"⚠️ Could not create confusion matrix: {e}")

def test_feature_importance(model):
    """Test feature importance"""
    print("\n🎯 Feature importance in the model:")
    
    features = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    importances = model.feature_importances_
    
    # Sort features by importance
    feature_importance = list(zip(features, importances))
    feature_importance.sort(key=lambda x: x[1], reverse=True)
    
    print("="*40)
    for i, (feature, importance) in enumerate(feature_importance, 1):
        print(f"{i}. {feature}: {importance:.4f} ({importance*100:.2f}%)")

def run_comprehensive_test():
    """Run comprehensive model test"""
    print("🚀 Starting comprehensive test for crop recommendation model")
    print("="*60)
    
    # Load model and data
    model, df = load_model_and_data()
    
    if model is None or df is None:
        print("❌ Failed to load model or data")
        return
    
    # Run tests
    y_true, y_pred = test_model_accuracy(model, df)
    test_cross_validation(model, df)
    test_specific_predictions(model)
    test_feature_importance(model)
    generate_classification_report(y_true, y_pred)
    plot_confusion_matrix(y_true, y_pred)
    
    print("\n✅ Comprehensive model test completed")

if __name__ == "__main__":
    run_comprehensive_test()