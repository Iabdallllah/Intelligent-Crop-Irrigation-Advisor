# 📚 User Guide - Smart Crop Recommendation System

## 🎯 Getting Started

### What is the Crop Recommendation System?
This system helps farmers and agricultural professionals choose the best crop to plant based on soil and environmental conditions. Simply input your soil parameters and climate data, and get instant, science-based crop recommendations.

## 🖥️ Accessing the Application

### Starting the Application
You have several options to launch the app:

#### Option 1: Launcher Script (Recommended)
1. Navigate to the project folder
2. Run the launcher:
   ```bash
   python launch_app.py
   ```
3. Wait for your browser to open automatically

#### Option 2: VS Code Tasks
1. Open VS Code in the project folder
2. Use Command Palette (Ctrl+Shift+P)
3. Run task: **🌾 Run Crop Recommendation App**
4. Or use: **🚀 Launch App with Browser**

#### Option 3: Manual Start
1. Open command prompt/terminal
2. Navigate to project folder
3. Run:
   ```bash
   streamlit run app.py
   ```

### Accessing the Web Interface
Once started, open your browser and go to:
- **Local Access**: http://localhost:8501 (or displayed port)
- **Network Access**: Available to other devices on your network

## 📊 Using the Application

### Step 1: Enter Soil Data
In the left panel, you'll find input fields for soil nutrients:

#### Soil Nutrients (NPK)
- **🟤 Nitrogen (N)**: 0-200
  - Essential for leaf growth and protein synthesis
  - Higher values promote vegetative growth
  
- **🟠 Phosphorus (P)**: 0-200
  - Important for root development and flowering
  - Critical during early plant growth
  
- **🟡 Potassium (K)**: 0-200
  - Enhances disease resistance and fruit quality
  - Important for water regulation

### Step 2: Enter Environmental Data

#### Climate Parameters
- **🌡️ Temperature (°C)**: 0-50°C
  - Average temperature during growing season
  - Different crops have different temperature preferences
  
- **💧 Humidity (%)**: 0-100%
  - Relative humidity percentage
  - Affects disease susceptibility and water needs
  
- **⚗️ Soil pH**: 0-14
  - Soil acidity/alkalinity level
  - Most crops prefer pH 6.0-7.5
  
- **🌧️ Rainfall (mm)**: 0-300mm
  - Annual or seasonal rainfall amount
  - Critical for water-dependent crops

### Step 3: Get Recommendation
1. Click the **🚀 Get Recommendation** button
2. View your results in the right panel:
   - **Recommended Crop**: The best crop for your conditions
   - **Confidence Level**: How certain the model is (aim for >90%)
   - **Crop Information**: Details about the recommended crop

### Step 4: Review Input Summary
Check the **📋 Input Summary** table to verify your entered values.

## 🌾 Understanding Crop Recommendations

### Crop Categories

#### Cereals
- **🍚 Rice**: High water requirement, humid conditions
- **🌽 Maize**: Moderate water, versatile crop

#### Pulses & Legumes
- **🫘 Chickpea**: Drought tolerant, cool season
- **🫘 Kidney Beans**: Moderate water needs
- **🫛 Pigeon Peas**: Drought resistant, semi-arid regions
- **🫘 Moth Beans**: Very drought tolerant
- **🫛 Mung Bean**: Short season, moderate water
- **🫘 Black Gram**: Good for dry farming
- **🫛 Lentil**: Cool season, low water needs

#### Fruits
- **🍎 Pomegranate**: Drought tolerant fruit
- **🍌 Banana**: High water requirement, tropical
- **🥭 Mango**: Tropical fruit, moderate water
- **🍇 Grapes**: Mediterranean climate
- **🍉 Watermelon**: High water in summer
- **🍈 Muskmelon**: Warm season crop
- **🍎 Apple**: Temperate climate
- **🍊 Orange**: Warm climate citrus
- **🥭 Papaya**: Tropical, year-round
- **🥥 Coconut**: Coastal tropical

#### Cash Crops
- **🌿 Cotton**: Moderate water needs
- **🌿 Jute**: High humidity required
- **☕ Coffee**: Specific climate needs

### Confidence Levels
- **95-100%**: Excellent match, highly recommended
- **90-94%**: Very good match, recommended
- **80-89%**: Good match, consider other factors
- **Below 80%**: Poor match, review inputs

## 💡 Tips for Best Results

### Soil Testing
1. **Get Professional Soil Test**: For accurate NPK and pH values
2. **Multiple Samples**: Test different areas of your field
3. **Recent Data**: Use data from the last growing season

### Climate Data
1. **Local Weather Station**: Use nearby weather data
2. **Historical Averages**: Consider 5-10 year averages
3. **Seasonal Variations**: Account for growing season specifics

### Input Validation
- ✅ Double-check all values before clicking recommend
- ✅ Ensure values are within reasonable ranges
- ✅ Consider local farming practices and experience

## 🚨 Troubleshooting

### Common Issues

#### App Won't Start
**Problem**: Error messages when launching
**Solutions**:
1. Ensure Python is installed (3.11+)
2. Check virtual environment is activated
3. Install requirements: `pip install -r requirements.txt`
4. Try using VS Code tasks instead of direct script execution

#### Browser Doesn't Open
**Problem**: App starts but browser doesn't open
**Solutions**:
1. Manually navigate to displayed URL
2. Check firewall settings
3. Try different browser

#### Multiple Browser Windows
**Problem**: App opens multiple browser tabs
**Solutions**:
1. Use VS Code tasks for better control
2. Close duplicate tabs manually
3. Restart the application using `launch_app.py`

#### Low Confidence Predictions
**Problem**: Confidence below 80%
**Solutions**:
1. Verify input values are accurate
2. Check if values are within normal ranges
3. Consider that your conditions might be unusual
4. Consult agricultural extension services

### Getting Help
1. **Check Documentation**: Review files in `docs/` folder
2. **Verify Inputs**: Ensure all parameters are realistic
3. **Test with Known Values**: Try inputs from successful farms
4. **Contact Support**: Reach out to development team

## 📊 Interpreting Results

### Making Decisions
The recommendation is a starting point. Consider:
- **Local Experience**: What grows well in your area?
- **Market Demand**: What crops have good market prices?
- **Resources**: Do you have necessary equipment/water?
- **Crop Rotation**: What was planted previously?
- **Personal Preference**: Your farming goals and experience

### Beyond the Recommendation
Use the system as one tool among many:
- Consult local agricultural experts
- Consider economic factors
- Account for seasonal timing
- Plan for crop rotation
- Consider climate change effects

## 📈 Best Practices

### Regular Use
- Test different scenarios
- Update with current soil conditions
- Track actual results vs predictions
- Share successful combinations with community

### Data Management
- Keep records of inputs and outcomes
- Note seasonal variations
- Document local modifications needed
- Build historical database

---
**User Guide Version**: 1.0.0  
**Last Updated**: October 5, 2025  
**For Technical Support**: See README.md