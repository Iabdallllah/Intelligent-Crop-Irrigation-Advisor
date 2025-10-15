import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
import plotly.express as px


# Set page configuration
st.set_page_config(
    page_title="🌾 Smart Crop & Irrigation Advisor",
    page_icon="🌱",
    layout="wide"
)


"""Streamlit dashboard for crop recommendation and irrigation advisor with IoT live data."""

# Load environment variables from .env (local) and support Streamlit Cloud secrets
# First try default .env in current working directory
load_dotenv()
# Also try loading .env from the project root (one level above models/frontend folders)
try:
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    env_path = os.path.join(repo_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path, override=False)
except Exception:
    pass

st.title("🌾 Smart Crop & Irrigation Advisor")
st.markdown("### Get intelligent crop recommendations and irrigation decisions based on soil and environmental conditions")

# --- IoT Live Data Section ---
with st.expander("💧 Live Sensor Data (IoT)", expanded=False):
    st.markdown("Click 'Refresh Data' to fetch latest readings from Supabase")
    
    # Supabase credentials (from .env or Streamlit secrets)
    SUPABASE_URL = os.getenv("SUPABASE_URL") or (st.secrets.get("SUPABASE_URL") if hasattr(st, "secrets") else None)
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or (st.secrets.get("SUPABASE_SERVICE_KEY") if hasattr(st, "secrets") else None)
    
    if SUPABASE_URL and SUPABASE_KEY:
        if st.button("🔄 Refresh Data"):
            with st.spinner("Fetching sensor data..."):
                try:
                    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
                    response = supabase.table("Sensor readings").select("*").order("created_at", desc=True).limit(100).execute()
                    data = response.data
                    if data:
                        df = pd.DataFrame(data)
                        st.subheader("Sensor Data Table")
                        st.dataframe(df)

                        st.subheader("Sensor Data Visualization")
                        # رسم بياني لدرجة الحرارة والرطوبة
                        fig = px.line(df.sort_values("created_at"), x="created_at", y=["temperature", "humidity"], markers=True, title="Temperature & Humidity Over Time")
                        st.plotly_chart(fig, use_container_width=True)

                        # رسم بياني لمستوى الماء والتربة
                        if "soil_moisture" in df.columns and "water_level" in df.columns:
                            fig2 = px.line(df.sort_values("created_at"), x="created_at", y=["soil_moisture", "water_level"], markers=True, title="Soil Moisture & Water Level Over Time")
                            st.plotly_chart(fig2, use_container_width=True)
                    else:
                        st.info("No sensor data found in Supabase.")
                except Exception as e:
                    st.error(f"Error fetching data from Supabase: {e}")
        else:
            st.info("👆 Click 'Refresh Data' to load IoT sensor readings")
    else:
        st.warning("Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in your environment.")

# Global status tracker for all models
MODEL_STATUS = {
    'crop_model': False,
    'irrigation_model': False,
    'optimization_model': False
}

def load_crop_model():
    import os
    import joblib
    
    # Get the absolute path to the repository root  
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    
    # Direct path to the crop model
    model_path = os.path.join(repo_root, "models", "crop recommendation", "crop_model.pkl")

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            MODEL_STATUS['crop_model'] = True
            return model
        except Exception as e:
            st.error(f"Error loading crop model from {model_path}: {type(e).__name__}: {e}")
            MODEL_STATUS['crop_model'] = False
            return None
    else:
        st.error(f"❌ Crop model file not found at: {model_path}")
        MODEL_STATUS['crop_model'] = False
        return None

def load_irrigation_model():
    import os
    import joblib
    
    # Get the absolute path to the repository root
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    
    # Direct path to the irrigation model
    model_path = os.path.join(repo_root, "models", "Smart_Irrigation_Classifier", "catboost_model.pkl")

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            MODEL_STATUS['irrigation_model'] = True
            return model
        except Exception as e:
            st.error(f"Error loading irrigation model from {model_path}: {type(e).__name__}: {e}")
            MODEL_STATUS['irrigation_model'] = False
            return None
    else:
        st.error(f"❌ Irrigation model file not found at: {model_path}")
        MODEL_STATUS['irrigation_model'] = False
        return None

def load_optimization_model():
    import os
    import joblib
    
    # Get the absolute path to the repository root
    current_file = os.path.abspath(__file__)
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    
    # Direct path to the optimization model
    model_path = os.path.join(repo_root, "models", "irrigation_optimization_model", "catboost_irrigation_model.pkl")

    if os.path.exists(model_path):
        try:
            model = joblib.load(model_path)
            MODEL_STATUS['optimization_model'] = True
            return model
        except Exception as e:
            st.error(f"Error loading optimization model from {model_path}: {type(e).__name__}: {e}")
            MODEL_STATUS['optimization_model'] = False
            return None
    else:
        st.error(f"❌ Optimization model file not found at: {model_path}")
        MODEL_STATUS['optimization_model'] = False
        return None

# Load all models
crop_model = load_crop_model()
irrigation_model = load_irrigation_model()
optimization_model = load_optimization_model()

# Feature engineering functions
def create_irrigation_features(soil_moisture, temperature, humidity, ph, n, p, k, rainfall=0):
    """Create all required features for irrigation model"""
    import numpy as np
    
    # Basic features
    soil_humidity = humidity * 0.8  # Approximate soil humidity
    air_temperature = temperature
    
    # Derived features
    relative_soil_saturation = min(soil_moisture / 100.0, 1.0)
    temp_diff = abs(temperature - 25)  # Difference from optimal temp
    evapotranspiration = max(0, (temperature - 10) * 0.1 + (100 - humidity) * 0.05)
    rain_vs_soil = rainfall / max(soil_moisture, 1)
    ph_encoded = 1 if ph > 7 else 0  # Alkaline vs acidic
    
    # NPK ratios
    np_ratio = n / max(p, 1)
    nk_ratio = n / max(k, 1)
    npk_balance = (n + p + k) / 3
    
    # Additional derived features
    crop_encoded = 1  # Default crop type
    rain_3days = rainfall * 3  # Assume same rainfall for 3 days
    moisture_temp_ratio = soil_moisture / max(temperature, 1)
    evapo_ratio = evapotranspiration / max(rainfall, 0.1)
    rain_effect = min(rainfall / 10, 1.0)
    moisture_change_rate = 0.1  # Default change rate
    temp_scaled = temperature / 40  # Scale temperature
    wind_ratio = 0.5  # Default wind effect
    
    return np.array([[
        soil_moisture, temperature, soil_humidity, relative_soil_saturation,
        temp_diff, evapotranspiration, rain_vs_soil, rainfall, ph_encoded,
        n, p, k, np_ratio, nk_ratio, crop_encoded, rain_3days,
        moisture_temp_ratio, evapo_ratio, rain_effect, moisture_change_rate,
        temp_scaled, npk_balance, wind_ratio
    ]])

def create_optimization_features(soil_moisture, temperature, humidity, ph, n, p, k, rainfall=0):
    """Create all required features for optimization model"""
    import numpy as np
    
    # Basic environmental features
    soil_humidity = humidity * 0.8
    air_temperature = temperature
    wind_speed = 10  # Default wind speed
    wind_gust = wind_speed * 1.5
    pressure = 101.325  # Standard atmospheric pressure
    
    # Derived features
    soil_moisture_diff = 0.1  # Default change
    relative_soil_saturation = min(soil_moisture / 100.0, 1.0)
    temp_diff = abs(temperature - 25)
    wind_effect = wind_speed * 0.1
    evapotranspiration = max(0, (temperature - 10) * 0.1 + (100 - humidity) * 0.05)
    rain_3days = rainfall * 3
    rain_vs_soil = rainfall / max(soil_moisture, 1)
    
    # NPK features
    np_ratio = n / max(p, 1)
    nk_ratio = n / max(k, 1)
    npk_balance = (n + p + k) / 3
    
    # Encoded features
    ph_encoded = 1 if ph > 7 else 0
    crop_encoded = 1
    
    # Additional ratios
    moisture_temp_ratio = soil_moisture / max(temperature, 1)
    evapo_ratio = evapotranspiration / max(rainfall, 0.1)
    rain_effect = min(rainfall / 10, 1.0)
    moisture_change_rate = 0.1
    temp_scaled = temperature / 40
    wind_ratio = wind_speed / 50
    
    return np.array([[
        soil_moisture, temperature, soil_humidity, air_temperature,
        wind_speed, humidity, wind_gust, pressure, ph, rainfall,
        n, p, k, soil_moisture_diff, relative_soil_saturation,
        temp_diff, wind_effect, evapotranspiration, rain_3days,
        rain_vs_soil, np_ratio, nk_ratio, ph_encoded, crop_encoded,
        moisture_temp_ratio, evapo_ratio, rain_effect, moisture_change_rate,
        temp_scaled, npk_balance, wind_ratio
    ]])

# Check overall system status
def check_system_status():
    """Returns True only if ALL required models are loaded successfully"""
    all_loaded = all(MODEL_STATUS.values())
    if not all_loaded:
        failed_models = [model for model, status in MODEL_STATUS.items() if not status]
        st.error(f"🚨 **System Status: FAILED** - Models not loaded: {', '.join(failed_models)}")
        st.warning("⚠️ **Fail-Safe Mode**: All predictions will return 0/False due to missing models")
        return False
    else:
        st.success("✅ **System Status: OPERATIONAL** - All models loaded successfully")
        return True

# Check system status
system_operational = check_system_status()

# Create two columns layout
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📊 Soil & Environment Data")
    
    # Input fields for crop recommendation
    N = st.number_input("🟤 Nitrogen (N)", min_value=0, max_value=200, value=50, help="Nitrogen content in soil")
    P = st.number_input("🟠 Phosphorus (P)", min_value=0, max_value=200, value=50, help="Phosphorus content in soil")
    K = st.number_input("🟡 Potassium (K)", min_value=0, max_value=200, value=50, help="Potassium content in soil")
    
    st.divider()
    
    temp = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, help="Average temperature")
    hum = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=80.0, help="Relative humidity")
    ph = st.number_input("⚗️ Soil pH", min_value=0.0, max_value=14.0, value=6.5, help="Soil pH level")
    rain = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=300.0, value=100.0, help="Annual rainfall")
    
    st.divider()
    
    # Additional inputs for irrigation models
    soil_moisture = st.number_input("💧 Soil Moisture", min_value=0.0, max_value=1.0, value=0.25, step=0.01, help="Volumetric soil moisture content")
    wind_speed = st.number_input("🌬️ Wind Speed (km/h)", min_value=0.0, max_value=50.0, value=10.0, help="Wind speed")
    pressure = st.number_input("🌡️ Pressure (kPa)", min_value=80.0, max_value=110.0, value=101.3, help="Atmospheric pressure")

with col2:
    st.header("🎯 Recommendations & Decisions")
    
    # === CROP RECOMMENDATION SECTION ===
    st.subheader("🌱 Crop Recommendation")
    
    if st.button("🚀 Get Crop Recommendation", type="primary", width="stretch", key="crop_recommendation"):
        if not system_operational:
            st.error("❌ **FAIL-SAFE ACTIVATED**: Cannot provide recommendations due to system failure")
            st.info("🔄 **Returned Value**: 0 (Safe failure mode)")
        else:
            try:
                # Create DataFrame with proper column names to avoid warnings
                feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                input_data = pd.DataFrame([[N, P, K, temp, hum, ph, rain]], columns=feature_names)
                
                # Make prediction
                prediction = crop_model.predict(input_data)[0]
                confidence = crop_model.predict_proba(input_data).max()
                
                # Validation check - if confidence is too low, return 0/failure
                if confidence < 0.8:  # Less than 80% confidence
                    st.error("❌ **LOW CONFIDENCE PREDICTION**")
                    st.warning("⚠️ **Please review your inputs** - The model confidence is below 80%")
                    st.info("🔄 **Returned Value**: 0 (Low confidence fail-safe)")
                    st.info("💡 **Suggestion**: Check soil parameters (N, P, K, pH) and environmental conditions")
                else:
                    # Display results
                    st.success(f"🌱 **Recommended Crop: {prediction.title()}**")
                    st.info(f"🎯 **Confidence: {confidence:.2%}**")
                    
                    # Add crop information
                    crop_info = {
                        'rice': '🍚 Rice - High water requirement, suitable for humid conditions',
                        'maize': '🌽 Maize - Moderate water requirement, good for moderate climate',
                        'chickpea': '🫘 Chickpea - Low water requirement, drought tolerant',
                        'kidneybeans': '🫘 Kidney Beans - Nitrogen-fixing legume',
                        'pigeonpeas': '🫛 Pigeon Peas - Drought resistant pulse crop',
                        'mothbeans': '🫘 Moth Beans - Heat and drought tolerant',
                        'mungbean': '🫛 Mung Bean - Quick growing pulse crop',
                        'blackgram': '🫘 Black Gram - Protein-rich pulse crop',
                        'lentil': '🟤 Lentil - Cool season pulse crop',
                        'pomegranate': '🍎 Pomegranate - Antioxidant-rich fruit',
                        'banana': '🍌 Banana - Tropical fruit, high potassium needs',
                        'mango': '🥭 Mango - King of fruits, tropical climate',
                        'grapes': '🍇 Grapes - Mediterranean climate preferred',
                        'watermelon': '🍉 Watermelon - High water requirement in summer',
                        'muskmelon': '🍈 Muskmelon - Warm season crop',
                        'apple': '🍎 Apple - Temperate climate fruit',
                        'orange': '🍊 Orange - Citrus fruit, warm climate',
                        'papaya': '🥭 Papaya - Tropical fruit, year-round growing',
                        'coconut': '🥥 Coconut - Coastal tropical crop',
                        'cotton': '🌿 Cotton - Cash crop, moderate water needs',
                        'jute': '🌿 Jute - Fiber crop, high humidity required',
                        'coffee': '☕ Coffee - Shade-grown, specific climate needs'
                    }
                    
                    if prediction.lower() in crop_info:
                        st.info(crop_info[prediction.lower()])
                        
            except Exception as e:
                st.error(f"❌ **PREDICTION FAILED**: {str(e)}")
                st.info("🔄 **Returned Value**: 0 (Exception fail-safe)")
    
    # === IRRIGATION DECISIONS SECTION ===
    st.divider()
    st.subheader("💧 Irrigation Decisions")
    
    # Smart Irrigation Classifier
    if st.button("🔍 Smart Irrigation Check", width="stretch", key="irrigation_check"):
        if not system_operational or not MODEL_STATUS['irrigation_model']:
            st.error("❌ **FAIL-SAFE ACTIVATED**: Irrigation model unavailable")
            st.info("🔄 **Returned Value**: 0 (Safe failure mode)")
        else:
            try:
                # Create features for irrigation model
                irrigation_features = create_irrigation_features(
                    soil_moisture, temp, hum, ph, N, P, K, rain
                )
                
                pred = irrigation_model.predict(irrigation_features)[0]
                
                # Get prediction probability if available
                try:
                    prob = irrigation_model.predict_proba(irrigation_features).max()
                    confidence_text = f" (Confidence: {prob:.2%})"
                except:
                    confidence_text = ""
                
                # Validation check
                if prob and prob < 0.8:  # Less than 80% confidence
                    st.error("❌ **LOW CONFIDENCE IRRIGATION DECISION**")
                    st.warning("⚠️ **Please review your inputs** - The model confidence is below 80%")
                    st.info("🔄 **Returned Value**: 0 (Low confidence fail-safe)")
                    st.info("💡 **Suggestion**: Verify soil moisture, weather conditions, and nutrient levels")
                else:
                    if pred == 1 or pred == 'irrigate':
                        st.success(f"💧 **Irrigation Needed**")
                    else:
                        st.info(f"🚫 **No Irrigation Needed**")
                    
                    if prob:
                        st.info(f"🎯 **Confidence: {prob:.2%}**")
                        
            except Exception as e:
                st.error(f"❌ **IRRIGATION PREDICTION FAILED**: {str(e)}")
                st.info("🔄 **Returned Value**: 0 (Exception fail-safe)")
    
    # Irrigation Optimization
    if st.button("⚡ Irrigation Optimization", width="stretch", key="irrigation_optimization"):
        if not system_operational or not MODEL_STATUS['optimization_model']:
            st.error("❌ **FAIL-SAFE ACTIVATED**: Optimization model unavailable") 
            st.info("🔄 **Returned Value**: 0 (Safe failure mode)")
        else:
            try:
                # Create features for optimization model
                optimization_features = create_optimization_features(
                    soil_moisture, temp, hum, ph, N, P, K, rain
                )
                
                optimization_pred = optimization_model.predict(optimization_features)[0]
                
                # Validation check
                if optimization_pred < 0 or optimization_pred > 100:  # Unrealistic values
                    st.error("❌ **INVALID OPTIMIZATION RESULT**")
                    st.info("🔄 **Returned Value**: 0 (Validation fail-safe)")
                else:
                    st.success(f"⚡ **Optimal Irrigation: {optimization_pred:.2f} units**")
                    
                    # Add interpretation
                    if optimization_pred < 10:
                        st.info("💧 Low irrigation requirement")
                    elif optimization_pred < 30:
                        st.info("💧💧 Moderate irrigation requirement") 
                    else:
                        st.info("💧💧💧 High irrigation requirement")
                    
            except Exception as e:
                st.error(f"❌ **OPTIMIZATION FAILED**: {str(e)}")
                st.info("🔄 **Returned Value**: 0 (Exception fail-safe)")

# Display input summary at the bottom
st.subheader("📋 Input Summary")
summary_data = {
    'Parameter': ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall', 'Soil Moisture', 'Wind Speed', 'Pressure'],
    'Value': [f"{N}", f"{P}", f"{K}", f"{temp}°C", f"{hum}%", f"{ph}", f"{rain}mm", f"{soil_moisture}", f"{wind_speed}km/h", f"{pressure}kPa"],
    'Status': ['✅' if val > 0 else '⚠️' for val in [N, P, K, temp, hum, ph, rain, soil_moisture, wind_speed, pressure]]
}

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df, hide_index=True, width="stretch")

# Footer
st.markdown("---")
st.markdown("🌱 **Smart Crop Recommendation System** - Helping farmers make informed decisions")
st.markdown("💡 *Tip: Adjust the input parameters to see how they affect the recommendations*")