# 🧪 Test Samples for Smart Crop & Irrigation Advisor

This document contains **CORRECTED** test scenarios generated from actual training data to ensure high confidence predictions. Each test includes expected results for all three AI models.

## 🌐 Application URL
**Local Access**: http://localhost:8503

---

## 📊 Test Cases

### 1. 🍚 **Rice Test (High Water Crop)**
```
🟤 Nitrogen (N): 80
🟠 Phosphorus (P): 47
🟡 Potassium (K): 40
🌡️ Temperature: 23.7°C
💧 Humidity: 82.2%
⚗️ pH: 6.4
🌧️ Rainfall: 233.1mm
💧 Soil Moisture: 0.35
🌬️ Wind Speed: 8 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Rice (high confidence 85%+)
- 💧 **Irrigation Decision**: High irrigation needed
- ⚡ **Optimization Amount**: High irrigation (30+ units)

**Data Source**: Generated from training data median values
**Training Data Range**: N[60-99], P[35-60], K[35-45], Temp[20-27°C], Humidity[80-85%]

---

### 2. 🌽 **Maize Test (Moderate Crop)**
```
🟤 Nitrogen (N): 76
🟠 Phosphorus (P): 48
🟡 Potassium (K): 20
🌡️ Temperature: 22.8°C
💧 Humidity: 65.3%
⚗️ pH: 6.3
🌧️ Rainfall: 83.5mm
💧 Soil Moisture: 0.28
🌬️ Wind Speed: 10 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Maize (high confidence 85%+)
- 💧 **Irrigation Decision**: Moderate irrigation needed
- ⚡ **Optimization Amount**: Moderate irrigation (15-25 units)

**Data Source**: Generated from training data median values
**Training Data Range**: N[60-100], P[35-60], K[15-25], Temp[18-27°C], Humidity[55-75%]

---

### 3. 🫘 **Chickpea Test (Drought Resistant)**
```
🟤 Nitrogen (N): 39
🟠 Phosphorus (P): 68
🟡 Potassium (K): 79
🌡️ Temperature: 18.9°C
💧 Humidity: 16.7%
⚗️ pH: 7.4
🌧️ Rainfall: 79.7mm
💧 Soil Moisture: 0.20
🌬️ Wind Speed: 12 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Chickpea (high confidence 85%+)
- 💧 **Irrigation Decision**: Low irrigation needed
- ⚡ **Optimization Amount**: Low irrigation (5-15 units)

**Data Source**: Generated from training data median values
**Training Data Range**: N[20-60], P[55-80], K[75-85], Temp[17-21°C], Humidity[14-20%]

---

### 4. 🍌 **Banana Test (Tropical Fruit)**
```
🟤 Nitrogen (N): 100
🟠 Phosphorus (P): 81
🟡 Potassium (K): 50
🌡️ Temperature: 27.4°C
💧 Humidity: 80.2%
⚗️ pH: 6.0
🌧️ Rainfall: 105.0mm
💧 Soil Moisture: 0.35
🌬️ Wind Speed: 8 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Banana (high confidence 85%+)
- 💧 **Irrigation Decision**: High irrigation needed
- ⚡ **Optimization Amount**: High irrigation (30+ units)

**Data Source**: Generated from training data median values
**Training Data Range**: N[80-120], P[70-95], K[45-55], Temp[25-30°C], Humidity[75-85%]

---

### 5. 🌿 **Cotton Test (Cash Crop)**
```
🟤 Nitrogen (N): 117
🟠 Phosphorus (P): 46
🟡 Potassium (K): 19
🌡️ Temperature: 24.0°C
💧 Humidity: 80.0%
⚗️ pH: 6.8
🌧️ Rainfall: 80.2mm
💧 Soil Moisture: 0.28
🌬️ Wind Speed: 10 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Cotton (high confidence 85%+)
- 💧 **Irrigation Decision**: Moderate irrigation needed
- ⚡ **Optimization Amount**: Moderate irrigation (15-25 units)

**Data Source**: Generated from training data median values
**Training Data Range**: N[100-140], P[35-60], K[15-25], Temp[22-26°C], Humidity[75-85%]

---

### 6. 🍎 **Apple Test (Temperate Fruit)**
```
🟤 Nitrogen (N): 24
🟠 Phosphorus (P): 136
🟡 Potassium (K): 200
🌡️ Temperature: 22.6°C
💧 Humidity: 92.4%
⚗️ pH: 5.9
🌧️ Rainfall: 113.0mm
💧 Soil Moisture: 0.28
🌬️ Wind Speed: 10 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Apple (high confidence 85%+)
- 💧 **Irrigation Decision**: Moderate irrigation needed
- ⚡ **Optimization Amount**: Moderate irrigation (15-25 units)

**Data Source**: Generated from training data median values
**Training Data Range**: N[0-40], P[120-145], K[195-205], Temp[21-24°C], Humidity[90-95%]

---

### 7. 🍉 **Watermelon Test (Summer Crop)**
```
🟤 Nitrogen (N): 99
🟠 Phosphorus (P): 17
🟡 Potassium (K): 50
🌡️ Temperature: 25.6°C
💧 Humidity: 85.0%
⚗️ pH: 6.5
🌧️ Rainfall: 50.7mm
💧 Soil Moisture: 0.35
🌬️ Wind Speed: 8 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Watermelon (high confidence 85%+)
- 💧 **Irrigation Decision**: High irrigation needed
- ⚡ **Optimization Amount**: High irrigation (30+ units)

**Data Source**: Generated from training data median values
**Training Data Range**: N[80-120], P[5-30], K[45-55], Temp[24-27°C], Humidity[80-90%]

---

### 8. ☕ **Coffee Test (Specialty Crop)**
```
🟤 Nitrogen (N): 103
🟠 Phosphorus (P): 29
🟡 Potassium (K): 30
🌡️ Temperature: 25.7°C
💧 Humidity: 57.6%
⚗️ pH: 6.8
🌧️ Rainfall: 157.8mm
💧 Soil Moisture: 0.20
🌬️ Wind Speed: 12 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Coffee (high confidence 85%+)
- 💧 **Irrigation Decision**: Moderate irrigation needed
- ⚡ **Optimization Amount**: Moderate irrigation (15-25 units)

**Data Source**: Generated from training data median values
**Training Data Range**: N[80-120], P[15-40], K[25-35], Temp[23-28°C], Humidity[50-70%]

---

### 9. 🫛 **Lentil Test (Cool Season Legume)**
```
🟤 Nitrogen (N): 16
🟠 Phosphorus (P): 68
🟡 Potassium (K): 19
🌡️ Temperature: 24.9°C
💧 Humidity: 64.1%
⚗️ pH: 7.0
🌧️ Rainfall: 46.6mm
💧 Soil Moisture: 0.20
🌬️ Wind Speed: 12 km/h
🌡️ Pressure: 101.3 kPa
```
**Expected Results**:
- 🌱 **Crop Recommendation**: Lentil (high confidence 85%+)
- 💧 **Irrigation Decision**: Low irrigation needed
- ⚡ **Optimization Amount**: Low irrigation (5-15 units)

**Data Source**: Generated from training data median values
**Training Data Range**: N[0-40], P[55-80], K[15-25], Temp[18-30°C], Humidity[60-70%]

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