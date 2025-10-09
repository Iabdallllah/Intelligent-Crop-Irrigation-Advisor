# 🌾 Intelligent Crop Irrigation Advisor

An AI-powered web application that provide### Dependencies (Verified Working)
- Python 3.11+
- Streamlit 1.50.0
- CatBoost 1.2.8 (for irrigation models)
- Scikit-learn 1.7.2 (for crop recommendation)
- NumPy 2.3.3
- Pandas 2.3.3
- Joblib (for model loading)

## ✅ Advanced Fail-Safe System

### Multi-Layer Protection
1. **Model Loading Validation**: Comprehensive checks for all 3 models
2. **Input Validation**: Range checking and realistic value verification  
3. **Prediction Confidence**: Minimum thresholds for reliable results
4. **Exception Handling**: Graceful fallback to safe default values
5. **User Feedback**: Clear status messages and error explanations

### Confidence Thresholds
- **Crop Recommendations**: Require >50% confidence
- **Irrigation Decisions**: Require >60% confidence  
- **Optimization Results**: Validated for range 0-100 units
- **Low Confidence**: Returns safe fallback value (0) with clear explanationcrop recommendations and irrigation optimization using machine learning models. Clean, modern interface with advanced fail-safe mechanisms.

## ✨ Features

- **🌱 Smart Crop Recommendation**: Get crop suggestions based on soil and climate conditions using RandomForest
- **💧 Intelligent Irrigation Decisions**: Smart irrigation recommendations using CatBoost classifier with 23 engineered features
- **⚡ Water Optimization**: Optimize irrigation amounts with CatBoost regression using 31 features
- **🔄 Advanced Fail-Safe System**: Comprehensive error handling and fallback mechanisms
- **🧪 Feature Engineering**: Complex feature creation including NPK ratios, evapotranspiration, and soil saturation
- **📱 Clean 2-Column Interface**: Modern, intuitive layout with recommendations before irrigation decisions

## 🚀 Quick Start

### Easy Launch
```bash
# Activate virtual environment
.\.venv\Scripts\activate

# Launch application
python -m streamlit run frontend\streamlit_dashboard\app.py --server.port=8503
```

### Alternative Methods
```bash
# Using VS Code Task
# Open Command Palette (Ctrl+Shift+P) → Run Task → "🌾 Run Crop Recommendation App"

# Or manual installation
pip install -r requirements.txt
python -m streamlit run frontend\streamlit_dashboard\app.py
```

## 🧪 Testing with Sample Data

**Rice Example (High Water Crop):**
- N: 90, P: 42, K: 43
- Temperature: 20.8°C, Humidity: 82%
- pH: 6.5, Rainfall: 202.9mm
- Soil Moisture: 0.35, Wind: 8 km/h
- Expected: Rice recommendation + irrigation needed

**Drought-Resistant Crop:**
- N: 40, P: 60, K: 55
- Temperature: 35°C, Humidity: 45%
- pH: 7.2, Rainfall: 50mm
- Soil Moisture: 0.15, Wind: 15 km/h
- Expected: Chickpea/Cotton + minimal irrigation

## 🔧 Technical Architecture

### Machine Learning Models
1. **Crop Recommendation**: RandomForestClassifier 
   - 22 crop types supported
   - 7 input features (N, P, K, temperature, humidity, pH, rainfall)
   - 99.32% accuracy

2. **Smart Irrigation Classifier**: CatBoostClassifier
   - Binary classification (irrigate/don't irrigate)
   - 23 engineered features including NPK ratios, evapotranspiration, soil saturation
   - Advanced feature engineering with fail-safe mechanisms

3. **Irrigation Optimization**: CatBoostRegressor
   - Predicts optimal irrigation amount
   - 31 engineered features including weather effects, wind factors, pressure
   - Range validation (0-100 units)

### User Interface
- **Layout**: Clean 2-column design
- **Left Column**: All input parameters (NPK, climate, soil conditions)
- **Right Column**: Recommendations first, then irrigation decisions
- **Features**: Real-time validation, comprehensive input summary

### Feature Engineering Pipeline
```python
# Irrigation Model (23 features)
- Basic: soil_moisture, temperature, humidity, pH, N, P, K
- Derived: evapotranspiration, soil_saturation, NPK_ratios
- Weather: temp_diff, rain_effect, moisture_temp_ratio

# Optimization Model (31 features)  
- Extended: wind_speed, pressure, humidity variations
- Advanced: wind_effects, pressure_impacts, seasonal_factors
```

### Dependencies
- Python 3.11+
- Streamlit 1.50.0
- CatBoost 1.2.8
- Scikit-learn 1.7.2
- NumPy 2.3.3
- Pandas 2.3.3

## �️ Fail-Safe Mechanisms

- **Model Loading**: Graceful fallback when models fail to load
- **Prediction Validation**: Confidence thresholds and range checking
- **Error Handling**: Returns safe default values (0) on any failure
- **User Feedback**: Clear status messages for all operations

## 📊 Model Performance & Validation

### Crop Recommendation Model
- **Accuracy**: 99.32% on test data
- **Crops Supported**: 22 types across cereals, pulses, fruits, cash crops
- **Confidence**: Returns prediction confidence percentage
- **Validation**: Requires >50% confidence for recommendations

### Irrigation Models  
- **Smart Classifier**: Binary irrigation decisions with 23-feature engineering
- **Optimization Model**: Precise irrigation amounts using 31 advanced features
- **Validation**: Range checking and confidence thresholds
- **Fail-Safe**: Returns 0 for invalid/low-confidence predictions

## 🌐 Access Application

**Primary URL**: http://localhost:8503 (or displayed port)
**Network Access**: Available to other devices on your local network

The application features:
- 📱 **Responsive Design**: Works on desktop and mobile
- ⚡ **Real-time Processing**: Instant predictions as you input data
- 📊 **Visual Feedback**: Clear status indicators and confidence levels
- 🔄 **Input Summary**: Comprehensive overview of all parameters

## 📁 Project Structure

```
📂 Intelligent-Crop-Irrigation-Advisor/
├── 📂 frontend/streamlit_dashboard/
│   └── 📄 app.py                 # Main application (clean, 2-column)
├── 📂 models/
│   ├── 📂 crop recommendation/   # RandomForest model
│   ├── 📂 Smart_Irrigation_Classifier/  # CatBoost classifier
│   └── 📂 irrigation_optimization_model/ # CatBoost regressor
├── 📂 data/                      # Training datasets
├── 📂 docs/                      # Documentation
├── 📂 tests/                     # Unit tests
└── 📄 requirements.txt           # Dependencies
```
