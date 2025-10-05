import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="🌾 Smart Crop Recommendation",
    page_icon="🌱",
    layout="wide"
)

st.title("🌾 Smart Crop Recommendation System")
st.markdown("### Get intelligent crop recommendations based on soil and environmental conditions")

# Load the model
@st.cache_resource
def load_model():
    # Load model from correct path (relative to project root)
    model_path = "../../models/crop recommendation/crop_model.pkl"
    return joblib.load(model_path)

model = load_model()

# Create two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📊 Enter Farm Data")
    
    # Input fields with better formatting
    N = st.number_input("🟤 Nitrogen (N)", min_value=0, max_value=200, value=50, help="Nitrogen content in soil")
    P = st.number_input("🟠 Phosphorus (P)", min_value=0, max_value=200, value=50, help="Phosphorus content in soil")
    K = st.number_input("🟡 Potassium (K)", min_value=0, max_value=200, value=50, help="Potassium content in soil")
    
    st.divider()
    
    temp = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0, help="Average temperature")
    hum = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=80.0, help="Relative humidity")
    ph = st.number_input("⚗️ Soil pH", min_value=0.0, max_value=14.0, value=6.5, help="Soil pH level")
    rain = st.number_input("🌧️ Rainfall (mm)", min_value=0.0, max_value=300.0, value=100.0, help="Annual rainfall")

with col2:
    st.header("🎯 Crop Recommendation")
    
    if st.button("🚀 Get Recommendation", type="primary", width="stretch"):
        # Create DataFrame with proper column names to avoid warnings
        feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        input_data = pd.DataFrame([[N, P, K, temp, hum, ph, rain]], columns=feature_names)
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        confidence = model.predict_proba(input_data).max()
        
        # Display results
        st.success(f"🌱 **Recommended Crop: {prediction.title()}**")
        st.info(f"🎯 **Confidence: {confidence:.2%}**")
        
        # Add crop information
        crop_info = {
            'rice': '🍚 Rice - High water requirement, suitable for humid conditions',
            'maize': '🌽 Maize - Moderate water requirement, good for moderate climate',
            'chickpea': '🫘 Chickpea - Low water requirement, drought tolerant',
            'kidneybeans': '🫘 Kidney Beans - Moderate water requirement',
            'pigeonpeas': '🫛 Pigeon Peas - Drought tolerant, good for semi-arid regions',
            'mothbeans': '🫘 Moth Beans - Very drought tolerant',
            'mungbean': '🫛 Mung Bean - Short growing season, moderate water needs',
            'blackgram': '🫘 Black Gram - Good for dry farming',
            'lentil': '🫛 Lentil - Cool season crop, low water requirement',
            'pomegranate': '🍎 Pomegranate - Drought tolerant fruit crop',
            'banana': '🍌 Banana - High water requirement, tropical fruit',
            'mango': '🥭 Mango - Tropical fruit, moderate water needs',
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
    
    # Display input summary
    st.subheader("📋 Input Summary")
    summary_data = {
        'Parameter': ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall'],
        'Value': [f"{N}", f"{P}", f"{K}", f"{temp}°C", f"{hum}%", f"{ph}", f"{rain}mm"],
        'Status': ['✅' if val > 0 else '⚠️' for val in [N, P, K, temp, hum, ph, rain]]
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, hide_index=True, width="stretch")

# Footer
st.markdown("---")
st.markdown("🌱 **Smart Crop Recommendation System** - Helping farmers make informed decisions")
st.markdown("💡 *Tip: Adjust the input parameters to see how they affect the crop recommendation*")
