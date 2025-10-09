# 🧪 Test Samples for Smart Crop & Irrigation Advisor

This document contains various test scenarios to validate the functionality of the Smart Crop & Irrigation Advisor application. Each test includes expected results for all three AI models.

## 🌐 Application URL
**Local Access**: http://localhost:8503

---

## 📊 Test Cases

### 1. 🍚 **Rice Test (High Water Crop)**
```
🟤 Nitrogen (N): 90
🟠 Phosphorus (P): 42
🟡 Potassium (K): 43
🌡️ Temperature: 20.8°C
💧 Humidity: 82%
⚗️ pH: 6.5
🌧️ Rainfall: 202.9mm
💧 Soil Moisture: 0.35
🌬️ Wind Speed: 8 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Rice (high confidence 95%+)
- 💧 **Irrigation Decision**: Irrigation needed
- ⚡ **Optimization Amount**: High irrigation (30+ units)

**Characteristics**: Tropical crop, high water requirement, humid conditions

---

### 2. 🌽 **Maize Test (Moderate Crop)**
```
🟤 Nitrogen (N): 75
🟠 Phosphorus (P): 60
🟡 Potassium (K): 50
🌡️ Temperature: 25°C
💧 Humidity: 65%
⚗️ pH: 6.8
🌧️ Rainfall: 120mm
💧 Soil Moisture: 0.28
🌬️ Wind Speed: 12 km/h
🌡️ Pressure: 101.5 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Maize/Corn (high confidence)
- 💧 **Irrigation Decision**: Moderate irrigation needed
- ⚡ **Optimization Amount**: Moderate irrigation (15-25 units)

**Characteristics**: Versatile crop, moderate climate tolerance

---

### 3. 🫘 **Chickpea Test (Drought Resistant)**
```
🟤 Nitrogen (N): 40
🟠 Phosphorus (P): 67
🟡 Potassium (K): 55
🌡️ Temperature: 32°C
💧 Humidity: 45%
⚗️ pH: 7.2
🌧️ Rainfall: 45mm
💧 Soil Moisture: 0.15
🌬️ Wind Speed: 18 km/h
🌡️ Pressure: 100.8 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Chickpea (high confidence)
- 💧 **Irrigation Decision**: No irrigation needed or minimal
- ⚡ **Optimization Amount**: Low irrigation (0-10 units)

**Characteristics**: Drought tolerant legume, arid conditions

---

### 4. 🍌 **Banana Test (Tropical Fruit)**
```
🟤 Nitrogen (N): 100
🟠 Phosphorus (P): 35
🟡 Potassium (K): 80
🌡️ Temperature: 28°C
💧 Humidity: 85%
⚗️ pH: 6.0
🌧️ Rainfall: 180mm
💧 Soil Moisture: 0.42
🌬️ Wind Speed: 5 km/h
🌡️ Pressure: 101.1 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Banana (high confidence)
- 💧 **Irrigation Decision**: Irrigation needed
- ⚡ **Optimization Amount**: High irrigation (35+ units)

**Characteristics**: Tropical fruit, high potassium needs, humid environment

---

### 5. 🌿 **Cotton Test (Cash Crop)**
```
🟤 Nitrogen (N): 60
🟠 Phosphorus (P): 55
🟡 Potassium (K): 45
🌡️ Temperature: 30°C
💧 Humidity: 55%
⚗️ pH: 7.0
🌧️ Rainfall: 80mm
💧 Soil Moisture: 0.22
🌬️ Wind Speed: 15 km/h
🌡️ Pressure: 101.0 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Cotton (high confidence)
- 💧 **Irrigation Decision**: Moderate irrigation needed
- ⚡ **Optimization Amount**: Moderate irrigation (20-30 units)

**Characteristics**: Cash crop, warm climate, moderate water needs

---

### 6. 🍎 **Apple Test (Temperate Fruit)**
```
🟤 Nitrogen (N): 50
🟠 Phosphorus (P): 80
🟡 Potassium (K): 70
🌡️ Temperature: 18°C
💧 Humidity: 70%
⚗️ pH: 6.2
🌧️ Rainfall: 140mm
💧 Soil Moisture: 0.30
🌬️ Wind Speed: 10 km/h
🌡️ Pressure: 102.0 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Apple (high confidence)
- 💧 **Irrigation Decision**: Low irrigation needed
- ⚡ **Optimization Amount**: Low irrigation (5-15 units)

**Characteristics**: Temperate climate fruit, moderate water needs

---

### 7. 🍉 **Watermelon Test (Summer Crop)**
```
🟤 Nitrogen (N): 80
🟠 Phosphorus (P): 45
🟡 Potassium (K): 60
🌡️ Temperature: 35°C
💧 Humidity: 50%
⚗️ pH: 6.8
🌧️ Rainfall: 60mm
💧 Soil Moisture: 0.18
🌬️ Wind Speed: 20 km/h
🌡️ Pressure: 100.5 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Watermelon (high confidence)
- 💧 **Irrigation Decision**: High irrigation needed
- ⚡ **Optimization Amount**: High irrigation (40+ units)

**Characteristics**: Summer crop, high water requirement in hot weather

---

### 8. ☕ **Coffee Test (Specialty Crop)**
```
🟤 Nitrogen (N): 55
🟠 Phosphorus (P): 25
🟡 Potassium (K): 35
🌡️ Temperature: 22°C
💧 Humidity: 75%
⚗️ pH: 5.8
🌧️ Rainfall: 200mm
💧 Soil Moisture: 0.38
🌬️ Wind Speed: 6 km/h
🌡️ Pressure: 101.8 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Coffee (high confidence)
- 💧 **Irrigation Decision**: Moderate irrigation needed
- ⚡ **Optimization Amount**: Moderate irrigation (15-25 units)

**Characteristics**: Specialty crop, specific climate requirements, acidic soil

---

### 9. 🫛 **Lentil Test (Cool Season Legume)**
```
🟤 Nitrogen (N): 30
🟠 Phosphorus (P): 85
🟡 Potassium (K): 40
🌡️ Temperature: 16°C
💧 Humidity: 60%
⚗️ pH: 6.8
🌧️ Rainfall: 90mm
💧 Soil Moisture: 0.25
🌬️ Wind Speed: 12 km/h
🌡️ Pressure: 102.2 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Lentil (high confidence)
- 💧 **Irrigation Decision**: Low irrigation needed
- ⚡ **Optimization Amount**: Low irrigation (5-12 units)

**Characteristics**: Cool season pulse, low water requirement

---

### 10. 🥥 **Coconut Test (Coastal Tropical)**
```
🟤 Nitrogen (N): 65
🟠 Phosphorus (P): 30
🟡 Potassium (K): 95
🌡️ Temperature: 29°C
💧 Humidity: 88%
⚗️ pH: 6.1
🌧️ Rainfall: 250mm
💧 Soil Moisture: 0.45
🌬️ Wind Speed: 8 km/h
🌡️ Pressure: 101.0 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Coconut (high confidence)
- 💧 **Irrigation Decision**: Moderate irrigation needed
- ⚡ **Optimization Amount**: Moderate irrigation (20-30 units)

**Characteristics**: Coastal tropical crop, high humidity tolerance

---

## 🎯 **Testing Instructions**

### Step-by-Step Testing Process:
1. **Open Application**: Navigate to http://localhost:8503
2. **Enter Data**: Copy values from any test case above
3. **Test Sequence**: Click buttons in this order:
   - 🚀 **Get Crop Recommendation** (first)
   - 🔍 **Smart Irrigation Check** (second)
   - ⚡ **Irrigation Optimization** (third)
4. **Verify Results**: Compare with expected outcomes
5. **Check Confidence**: Ensure confidence levels are acceptable
6. **Review Summary**: Verify input summary table

### Expected System Behavior:
- ✅ **System Status**: Should show "OPERATIONAL"
- ✅ **Confidence Levels**: >50% for crops, >60% for irrigation
- ✅ **Range Validation**: Irrigation amounts 0-100 units
- ✅ **Error Handling**: Clear messages for any issues

---

## 🔧 **Troubleshooting Test Cases**

### Low Confidence Test (Edge Case)
```
🟤 Nitrogen (N): 200
🟠 Phosphorus (P): 5
🟡 Potassium (K): 200
🌡️ Temperature: 50°C
💧 Humidity: 10%
⚗️ pH: 9.5
🌧️ Rainfall: 300mm
💧 Soil Moisture: 0.05
🌬️ Wind Speed: 50 km/h
🌡️ Pressure: 80.0 kPa
```
**Expected**: Low confidence warnings, fail-safe activation

### Invalid Range Test
```
🟤 Nitrogen (N): -10
🟠 Phosphorus (P): 250
🟡 Potassium (K): -5
🌡️ Temperature: 60°C
💧 Humidity: 120%
⚗️ pH: 15.0
🌧️ Rainfall: -50mm
💧 Soil Moisture: 2.0
🌬️ Wind Speed: -10 km/h
🌡️ Pressure: 50.0 kPa
```
**Expected**: Input validation errors, system protection

---

## 📊 **Success Criteria**

### Model Performance Indicators:
- 🎯 **Crop Model**: >90% confidence for clear cases
- 💧 **Irrigation Model**: >80% confidence for decisions
- ⚡ **Optimization Model**: Realistic values (0-100 range)

### System Reliability:
- 🛡️ **Fail-Safe**: Activates for problematic inputs
- 🔄 **Error Recovery**: Graceful handling of exceptions
- 📱 **UI Responsiveness**: Fast, intuitive interface

---

**Test Document Version**: 1.0  
**Last Updated**: October 9, 2025  
**Compatible with**: Smart Crop & Irrigation Advisor v2.0  
**Application URL**: http://localhost:8503