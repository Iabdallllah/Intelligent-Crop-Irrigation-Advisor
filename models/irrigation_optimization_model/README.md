# 🌱 Smart Irrigation System using Machine Learning

This project develops an **intelligent irrigation optimization system** that uses **machine learning (CatBoost Regressor)** to predict the **optimal amount of irrigation water (mm)** based on environmental, soil, and crop conditions.  
It also provides **nutrient (NPK) recommendations** to maintain balanced soil fertility.

---

## 📘 Project Overview

Modern agriculture requires efficient resource management.  
This system aims to:
- Optimize **irrigation water usage**
- Recommend **NPK fertilizer amounts**
- Reduce waste and enhance **crop productivity**

It combines **environmental sensing, data processing, and ML prediction** to automate irrigation decisions.

---

## 🧩 Features

- ✅ Data preprocessing (cleaning, outlier detection, and imputation)
- 🌡️ Environmental & soil feature analysis
- 🧠 Machine learning model using **CatBoost Regressor**
- 📊 Performance evaluation with **MAE, RMSE, R², Adjusted R²**
- 💧 Dynamic irrigation and NPK recommendation
- 📈 Feature importance visualization

---

## 🗂️ Project Structure

smart_irrigation_system_ml/                                                                                                                                           
│
├── data/
│   ├── Final_irregation_optimization_data_m2.csv
│   └── new_irrigation_data.csv
│
├── models/
│   └── catboost_irrigation_model.pkl
│
├── scripts/
│   ├── train.py              # Train the CatBoost model
│   ├── test.py               # Predict on new data
│   └── model_analysis.py     # Analyze and visualize model features
│
├── outputs/
│   ├── predicted_irrigation_results.csv
│   └── irrigation_npk_scientific_safe.csv
│
└── README.md


## ⚙️ Installation

### 1️⃣ Clone the repository


### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

> Example main dependencies:

```txt
pandas
numpy
scikit-learn
catboost
matplotlib
seaborn
joblib
```

---

## 🚀 Usage

### 🔹 Train the Model

```bash
python scripts/train.py
```

### 🔹 Test on New Data

```bash
python scripts/test.py
```

### 🔹 Analyze Feature Importance

```bash
python scripts/model_analysis.py
```

---

## 🧠 Model Details

| Metric      | Description                    | Result |
| ----------- | ------------------------------ | ------ |
| MAE         | Mean Absolute Error            | —      |
| RMSE        | Root Mean Squared Error        | —      |
| R²          | Coefficient of Determination   | —      |
| Adjusted R² | Penalized R² for feature count | —      |

*(Actual results will appear after training.)*

---

## 🌾 Example Output

| Crop  | Soil Moisture (%) | Temperature (°C) | Recommended Water (mm) | N   | P   | K   |
| ----- | ----------------- | ---------------- | ---------------------- | --- | --- | --- |
| Maize | 45.0              | 32.5             | 27.5                   | 6.8 | 3.2 | 5.1 |
| Rice  | 55.0              | 28.0             | 12.4                   | 5.2 | 2.8 | 4.7 |

---

## 🧮 Algorithms & Methods Used

* **CatBoost Regressor** → predicts irrigation water
* **Safe division** & nutrient scaling logic for NPK
* **Kc coefficient** (FAO standard) for evapotranspiration adjustment
* **Dynamic soil moisture simulation** per record


---

## 🧾 License

This project is licensed under the **MIT License** — you’re free to use, modify, and distribute it with attribution.

---

## 🌟 Acknowledgments

* FAO (Food and Agriculture Organization) guidelines for **Evapotranspiration and Kc coefficients**
* CatBoost team for their efficient gradient boosting implementation
* Open-source data contributors in smart agriculture research

