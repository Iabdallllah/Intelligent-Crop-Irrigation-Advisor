import streamlit as st
import joblib
import numpy as np
import pandas as pd
import os
import sys
import requests
from dotenv import load_dotenv
from supabase import create_client
import plotly.express as px


# Set page configuration
st.set_page_config(
    page_title="AgriTech",
    page_icon="🌱",
    layout="wide"
)


# Load environment variables from .env (local) and support Streamlit Cloud secrets
# First try default .env in current working directory
load_dotenv()
# Establish repository root (robustly) and ensure it's on sys.path so
# pickled models that reference top-level package imports (e.g. `models`)
# can be imported during unpickling.
try:
    current_file = os.path.abspath(__file__)
    # repo root is three levels up from frontend/streamlit_dashboard/app.py
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
except Exception:
    repo_root = os.path.abspath(os.curdir)

if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Also try loading .env from the project root (one level above models/frontend folders)
try:
    env_path = os.path.join(repo_root, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path, override=False)
except Exception:
    pass

st.title("🌾 AgriTech")
st.markdown("### Get intelligent crop recommendations and irrigation decisions based on soil and environmental conditions")

# --- IoT Live Data Section ---
with st.expander("Live Sensor Data (IoT)", expanded=False):
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
                        # Plot temperature and humidity over time
                        fig = px.line(df.sort_values("created_at"), x="created_at", y=["temperature", "humidity"], markers=True, title="Temperature & Humidity Over Time")
                        st.plotly_chart(fig, use_container_width=True)

                        # Plot soil moisture and water level over time
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


def recommend_from_dataset(N, P, K, temperature, humidity, ph, rainfall, k=5):
    """Lightweight nearest-neighbour recommender that uses data/crop_data.csv.

    Returns (label, confidence) where confidence is fraction of the k nearest neighbors
    that agree with the predicted label.
    """
    import pandas as _pd
    import numpy as _np
    import os as _os

    cache_name = '_crop_dataset_cache'
    if cache_name not in globals():
        data_path = _os.path.join(repo_root, 'data', 'crop_data.csv')
        if not _os.path.exists(data_path):
            raise FileNotFoundError(f"Dataset not found: {data_path}")
        df = _pd.read_csv(data_path)
        feats = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].values.astype(float)
        labels = df['label'].astype(str).values
        mean = feats.mean(axis=0)
        std = feats.std(axis=0)
        std[std == 0] = 1.0
        globals()[cache_name] = {'feats': feats, 'labels': labels, 'mean': mean, 'std': std}

    cache = globals()[cache_name]
    feat = _np.array([N, P, K, temperature, humidity, ph, rainfall], dtype=float)
    norm = (feat - cache['mean']) / cache['std']
    feats_norm = (cache['feats'] - cache['mean']) / cache['std']
    dists = _np.linalg.norm(feats_norm - norm, axis=1)
    idx = _np.argsort(dists)[:k]
    top_labels = cache['labels'][idx]
    uniques, counts = _np.unique(top_labels, return_counts=True)
    mode = uniques[counts.argmax()]
    conf = float(counts.max()) / float(k)
    return str(mode), conf


def call_gemini_chat(prompt, context=None, system_instruction=None):
    """Call the Gemini REST API and return the generated text."""
    api_key = os.getenv("GEMINI_API_KEY") or (st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") else None)
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in .env or Streamlit secrets.")

    endpoint = os.getenv("GEMINI_REST_URL", "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent")
    headers = {
        "Content-Type": "application/json"
    }

    user_parts = [
        {"text": prompt}
    ]
    if context:
        user_parts.append({"text": f"\nContext:\n{context}"})

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": user_parts
            }
        ]
    }

    if system_instruction:
        payload["system_instruction"] = {
            "parts": [{"text": system_instruction}]
        }

    response = requests.post(
        endpoint,
        params={"key": api_key},
        headers=headers,
        json=payload,
        timeout=30
    )
    response.raise_for_status()
    data = response.json()

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError, TypeError):
        text = ""

    if not text:
        text = "No response returned from Gemini."

    return text

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
    N = st.number_input("🟤 Nitrogen (N)", min_value=0, max_value=200, value=80, help="Nitrogen content in soil")
    P = st.number_input("🟠 Phosphorus (P)", min_value=0, max_value=200, value=48, help="Phosphorus content in soil")
    K = st.number_input("🟡 Potassium (K)", min_value=0, max_value=200, value=40, help="Potassium content in soil")
    
    st.divider()
    
    temp = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=50.0, value=23.0, help="Average temperature")
    hum = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=82.0, help="Relative humidity")
    ph = st.number_input("⚗️ Soil pH", min_value=0.0, max_value=14.0, value=6.7, help="Soil pH level")
    rain = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=300.0, value=240.0, help="Annual rainfall")
    
    st.divider()
    
    # Additional inputs for irrigation models
    soil_moisture = st.number_input("💧 Soil Moisture", min_value=0.0, max_value=1.0, value=0.35, step=0.01, help="Volumetric soil moisture content")
    wind_speed = st.number_input("🌬️ Wind Speed (km/h)", min_value=0.0, max_value=50.0, value=8.0, help="Wind speed")
    pressure = st.number_input("🌡️ Pressure (kPa)", min_value=80.0, max_value=110.0, value=101.3, help="Atmospheric pressure")

with col2:
    st.header("🎯 Recommendations & Decisions")
    # Developer debug toggle: show raw inputs/outputs on the page
    show_debug = st.checkbox("🔧 Show raw inputs & model outputs", value=False, key="show_debug")
    # Option to use the dataset-based recommender (falls back to this when dummy model is present)
    use_data_recommender = st.checkbox("📚 Use dataset-based recommender (from data/crop_data.csv)", value=True, key="use_data_recommender")
    # Short explanation for users: dataset recommender is a k-NN over `data/crop_data.csv`.
    # It works even if the pickled/trained crop model is missing, but it only
    # reflects nearest examples from the CSV and may not generalize beyond them.
    st.info("📚 Dataset recommender: uses k-NN over `data/crop_data.csv`. Works as a fallback when a trained model is unavailable. It returns recommendations based on similar examples in the dataset and may not generalize.")
    
    # === CROP RECOMMENDATION SECTION ===
    st.subheader("🌱 Crop Recommendation")
    
    if st.button("🚀 Get Crop Recommendation", type="primary", width="stretch", key="crop_recommendation"):
        # Allow dataset-based recommender to run even if some models failed to load.
        # Previously the UI blocked all recommendations when any model failed to load.
        if not system_operational and not use_data_recommender:
            st.error("❌ **FAIL-SAFE ACTIVATED**: Cannot provide recommendations due to system failure")
            st.info("🔄 **Returned Value**: 0 (Safe failure mode)")
        else:
            try:
                # Create DataFrame with proper column names to avoid warnings
                feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
                input_data = pd.DataFrame([[N, P, K, temp, hum, ph, rain]], columns=feature_names)
                # Debug: log inputs to help trace behavior and optionally show on the page
                crop_inputs_dict = input_data.to_dict(orient='records')[0]
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"CROP_INPUTS: {crop_inputs_dict}\n")
                except Exception:
                    pass

                # Make prediction
                prediction = None
                confidence = None

                # If requested, use dataset-based recommender which uses nearest-neighbors
                if use_data_recommender:
                    try:
                        pred_label, conf_score = recommend_from_dataset(
                            N, P, K, temp, hum, ph, rain, k=5
                        )
                        prediction = pred_label
                        confidence = conf_score
                    except Exception:
                        # If dataset recommender fails, try crop_model if it's loaded
                        if MODEL_STATUS.get('crop_model') and crop_model is not None:
                            try:
                                prediction = crop_model.predict(input_data)[0]
                                try:
                                    confidence = crop_model.predict_proba(input_data).max()
                                except Exception:
                                    confidence = None
                            except Exception:
                                prediction = 'unknown'
                                confidence = None
                        else:
                            prediction = 'unknown'
                            confidence = None
                else:
                    # Use the loaded crop_model if available, otherwise warn and return unknown
                    if MODEL_STATUS.get('crop_model') and crop_model is not None:
                        try:
                            prediction = crop_model.predict(input_data)[0]
                            try:
                                confidence = crop_model.predict_proba(input_data).max()
                            except Exception:
                                confidence = None
                        except Exception:
                            prediction = 'unknown'
                            confidence = None
                    else:
                        st.warning("⚠️ Crop model not loaded. Enable 'Use dataset-based recommender' to get recommendations from dataset.")
                        prediction = 'unknown'
                        confidence = None
                # Debug: log model outputs as well and (optionally) print them to the page
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"CROP_OUTPUT: pred={prediction}, conf={confidence}\n")
                except Exception:
                    pass

                if show_debug:
                    st.markdown("**Debug — crop model inputs**")
                    st.write(input_data)
                    st.markdown("**Debug — crop model outputs**")
                    st.write({"prediction": str(prediction), "confidence": float(confidence) if confidence is not None else None})

                # Display results (no hard confidence threshold)
                st.success(f"🌱 **Recommended Crop: {prediction.title()}**")
                if confidence is not None:
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
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"IRR_INPUTS: soil_moisture={soil_moisture}, temp={temp}, hum={hum}, ph={ph}, N={N}, P={P}, K={K}, rain={rain}\n")
                except Exception:
                    pass
                
                pred = irrigation_model.predict(irrigation_features)[0]
                
                # Get prediction probability if available
                try:
                    prob = irrigation_model.predict_proba(irrigation_features).max()
                except Exception:
                    prob = None
                try:
                    with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                        _dbg.write(f"IRR_OUTPUT: pred={pred}, conf={prob}\n")
                except Exception:
                    pass

                if show_debug:
                    st.markdown("**Debug — irrigation model inputs**")
                    # show the vector we passed to the model
                    st.write(irrigation_features.tolist())
                    st.markdown("**Debug — irrigation model outputs**")
                    st.write({"prediction": str(pred), "confidence": float(prob) if prob is not None else None})

                # Display irrigation decision (no hard confidence threshold)
                if pred == 1 or pred == 'irrigate':
                    st.success(f"💧 **Irrigation Needed**")
                else:
                    st.info(f"🚫 **No Irrigation Needed**")

                if prob is not None:
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

    st.divider()
    st.subheader("🤖 Gemini Chatbot")
    st.markdown("Get quick crop & irrigation tips powered by Gemini.")

    gemini_prompt = st.text_area(
        "💬 Enter your question or request",
        placeholder="Example: What's the best way to irrigate rice during a heat wave?",
        key="gemini_prompt",
        height=120
    )

    context_snippet = (
        f"Current soil inputs -> N:{N}, P:{P}, K:{K}, Temp:{temp}°C, Humidity:{hum}%, pH:{ph}, Rainfall:{rain}mm, "
        f"Soil moisture:{soil_moisture}, Wind:{wind_speed}km/h, Pressure:{pressure}kPa"
    )

    if st.button("✨ Ask Gemini", type="primary", key="gemini_button"):
        clean_prompt = gemini_prompt.strip()
        if not clean_prompt:
            st.warning("⚠️ Please type a question first.")
        else:
            with st.spinner("Contacting Gemini..."):
                try:
                    try:
                        with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                            _dbg.write(f"GEMINI_PROMPT: {clean_prompt}\n")
                    except Exception:
                        pass

                    system_instruction = (
                        "You are AgriTech Assistant (Gemini) that explains crop and irrigation guidance in concise, practical English. "
                        "Use the provided soil context when relevant and keep responses under 200 words."
                    )
                    gemini_response = call_gemini_chat(
                        clean_prompt,
                        context=context_snippet,
                        system_instruction=system_instruction
                    )

                    st.success("✅ Response from Gemini")
                    st.markdown(gemini_response)

                    try:
                        with open(os.path.join(repo_root, 'streamlit_debug_predictions.log'), 'a') as _dbg:
                            _dbg.write(f"GEMINI_RESPONSE: {gemini_response}\n")
                    except Exception:
                        pass

                except Exception as e:
                    st.error(f"❌ Gemini API error: {str(e)}")
                    st.info("Please verify your API key and internet connection, then try again.")

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
st.markdown("**AgriTech - Smart Agriculture Advisor** - Empowering farmers with AI-driven crop and irrigation insights")
st.markdown("💡 *Tip: Adjust the input parameters to see how they affect the recommendations*")
