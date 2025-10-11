## 🌾 Intelligent Crop Irrigation Advisor


### 🧩 Dataset Description

**File:** `Final_irregation_optimization_data_m2.csv` We used the data set of the Status Classifer model and add to it more Features 

Each row represents a daily record of soil, crop, and weather conditions with the corresponding irrigation recommendations.

| Feature                                           | Description                                          |
| ------------------------------------------------- | ---------------------------------------------------- |
| `soil_moisture`                                   | Current soil moisture percentage (%)                 |
| `temperature`                                     | Ambient temperature (°C)                             |
| `soil_humidity`                                   | Soil humidity level (%)                              |
| `air_temperature_(c)`                             | Air temperature in Celsius                           |
| `wind_speed_(km/h)`                               | Wind speed in kilometers per hour                    |
| `humidity`                                        | Relative humidity (%)                                |
| `wind_gust_(km/h)`                                | Maximum wind gust speed                              |
| `pressure_(kpa)`                                  | Atmospheric pressure (kPa)                           |
| `ph`                                              | Soil pH value                                        |
| `rainfall`                                        | Daily rainfall amount (mm)                           |
| `n`, `p`, `k`                                     | Soil nutrient concentrations                         |
| `Evapotranspiration`                              | Crop water loss due to evaporation and transpiration |
| `rain_3days`                                      | Accumulated rainfall over the last 3 days            |
| `np_ratio`, `nk_ratio`, `npk_balance`             | Calculated nutrient balance ratios                   |
| `crop`                                            | Crop type (e.g., rice, maize, banana, mango, etc.)   |
| `status`                                          | Boolean indicator (True = needs irrigation)          |
| `recommended_water_mm`                            | Predicted irrigation water amount in mm              |
| `recommended_N`, `recommended_P`, `recommended_K` | Recommended NPK fertilizer levels                    |
| `soil_moisture_updated`                           | Updated soil moisture after irrigation               |

Total Features: **40 columns**
Total Rows: Depends on collected data records.

---

### ⚙️ Workflow Summary

1. **Data Loading & Inspection**

   * Read dataset using pandas.
   * Display structure, missing values, and duplicates.

2. **Feature Importance Extraction**

   * Load a pre-trained `CatBoost` model (`catboost_model.pkl`).
   * Visualize feature importance to understand influential factors in irrigation needs.

3. **Water & Nutrient Simulation**

   * Iterates through each data row to:

     * Compute **ETc (Evapotranspiration × Kc)**.
     * Calculate **water deficit** adjusted by soil moisture and rainfall.
     * Recommend **NPK values** based on crop, pH, and irrigation level.
   * Updates soil moisture dynamically after each irrigation step.
   * Results stored in `irrigation_npk_scientific_safe.csv`.
