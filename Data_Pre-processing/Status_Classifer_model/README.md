# 🌾 Status Classifier 

## 📘 Overview

This dataset integrates **environmental**, **soil**, and **agronomic** data to support **smart irrigation systems** and **crop recommendation models**.
It captures interactions between weather, soil composition, nutrient balance, and irrigation status — enabling data-driven insights for optimizing water use and improving crop yield.

The dataset initially contained **16 raw features**, and after feature engineering, it expanded to **27 enriched features** that provide deeper contextual understanding of soil–climate–crop relationships.

---

## 📊 Columns Description

| Feature               | Description                                                           |
| --------------------- | --------------------------------------------------------------------- |
| `soil_moisture`       | Percentage of water content in the soil (indicator of soil wetness).  |
| `temperature`         | Temperature of the soil surface in °C.                                |
| `soil_humidity`       | Amount of water vapor in the soil environment.                        |
| `time`                | Time in minutes or hours (depending on measurement setup).            |
| `air_temperature_(c)` | Ambient air temperature in °C.                                        |
| `wind_speed_(km/h)`   | Average wind velocity during the observation period.                  |
| `humidity`            | Relative atmospheric humidity in %.                                   |
| `wind_gust_(km/h)`    | Maximum short-term wind burst recorded.                               |
| `pressure_(kpa)`      | Atmospheric pressure in kilopascals.                                  |
| `ph`                  | Soil pH level indicating acidity or alkalinity.                       |
| `rainfall`            | Measured rainfall amount (mm).                                        |
| `n`, `p`, `k`         | Soil macronutrients: Nitrogen (N), Phosphorus (P), and Potassium (K). |
| `status`              | Irrigation system status (`ON` or `OFF`).                             |
| `crop`                | Crop type being cultivated (e.g., rice, coffee, wheat, etc.).         |

---

## ⚙️ Feature Engineering (New Columns)

| New Feature                | Description                                                                                                                        |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `Relative_Soil_Saturation` | Ratio of current soil moisture to maximum field capacity — measures how saturated the soil is.                                     |
| `temp_diff`                | Difference between soil and air temperature — indicates surface heat exchange and stress levels.                                   |
| `wind_effect`              | Combined effect of wind speed and gusts — estimates aerodynamic drying potential.                                                  |
| `Evapotranspiration`       | Estimated total water loss from soil and plant surfaces (based on temperature, humidity, and wind).                                |
| `rain_3days`               | Total rainfall accumulated over the past 3 days — captures recent water availability trends.                                       |
| `rain_vs_soil`             | Ratio between rainfall and soil moisture — reveals infiltration and retention efficiency.                                          |
| `np_ratio`                 | Nitrogen-to-Phosphorus ratio — assesses nutrient balance important for plant growth.                                               |
| `nk_ratio`                 | Nitrogen-to-Potassium ratio — provides additional insight into nutrient proportion for crop health.                                |
| `ph_category`              | Categorical label based on pH value: <br>• **Acidic** (pH < 6.5) <br>• **Neutral** (6.5 ≤ pH ≤ 7.5) <br>• **Alkaline** (pH > 7.5). |
| `ph_encoded`               | Numerical encoding of `ph_category`: 0 = Acidic, 1 = Neutral, 2 = Alkaline.                                                        |

---

## 🧩 Feature Engineering Rationale

Feature engineering was performed to transform raw sensor data into **interpretable, model-friendly insights**.
Here’s the reasoning behind each engineered feature:

| Feature                    | Rationale                                                                                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `Relative_Soil_Saturation` | Helps determine when the soil is close to saturation and irrigation can be paused to prevent overwatering.                     |
| `temp_diff`                | Large temperature gaps between soil and air can signal poor moisture retention or excessive evaporation.                       |
| `wind_effect`              | Wind increases evapotranspiration; combining gusts and average wind gives a better estimate of drying intensity.               |
| `Evapotranspiration`       | A key hydrological variable representing total water demand — essential for precise irrigation scheduling.                     |
| `rain_3days`               | Recent rainfall influences soil moisture levels; tracking 3-day accumulation provides temporal context.                        |
| `rain_vs_soil`             | Balances rainfall against soil moisture to understand infiltration efficiency — high ratio may indicate runoff.                |
| `np_ratio` / `nk_ratio`    | Nutrient ratios are more informative than absolute values for diagnosing crop nutrient balance.                                |
| `ph_category`              | Converts continuous pH into interpretable soil-type groups for model readability and easier correlation with crop preferences. |
| `ph_encoded`               | Provides a numeric version of pH categories for ML models requiring numerical inputs.                                          |

---

## 📈 Statistical Summary & Visualization

### Summary Statistics

```python
merged_df.describe()
```

### Feature Distributions

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

num_cols = merged_df.select_dtypes(include=np.number).columns
plt.figure(figsize=(15, 12))
for i, col in enumerate(num_cols, 1):
    plt.subplot(5, 3, i)
    sns.histplot(merged_df[col], kde=True, bins=30)
    plt.title(col)
plt.tight_layout()
plt.show()
```

These plots help:

* Detect outliers
* Visualize the distribution of soil and weather conditions
* Compare nutrient and pH balances
* Understand irrigation ON/OFF correlations across conditions

---

## 💡 Summary

This enriched dataset provides a **robust foundation** for building:

* Crop yield prediction models
* Smart irrigation control systems
* Soil health and nutrient balance analysis
* Data-driven decision support for precision agriculture

---

Last updated: 2025-11-14
