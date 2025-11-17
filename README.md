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
```markdown
# 🌾 Intelligent Crop Irrigation Advisor

An AI-powered web application that provides crop recommendations and irrigation advice (classification + optimization) using lightweight ML models and a Streamlit UI.

Overview
--------
- Crop recommendation (RandomForest)
- Smart irrigation decision (CatBoost classifier)
- Irrigation amount optimization (CatBoost regressor)
- Modular feature-engineering pipeline and fail-safe mechanisms for low-confidence or invalid predictions

Quick start (Linux / macOS)
---------------------------
Recommended: create and use a Python virtual environment, then run Streamlit from the repository root.

```bash
# create venv (if needed)
python -m venv .venv
source .venv/bin/activate

# install requirements (first time)
pip install -r requirements.txt

# launch the Streamlit app (default port used in this repo's tasks)
python -m streamlit run frontend/streamlit_dashboard/app.py --server.port=8503
```

Windows (PowerShell)
--------------------
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m streamlit run frontend/streamlit_dashboard/app.py --server.port=8503
```

Where to look
-------------
- App entry: `frontend/streamlit_dashboard/app.py`
- Model artifacts: `models/` (tracked with Git LFS where applicable)
- Documentation: `docs/` and per-module `README.md`

Notes and environment
---------------------
- Tested with Python 3.11+. The project may work on other Python 3.10+ runtimes but 3.11 is recommended.
- Some model artifacts are stored via Git LFS. After cloning, run `git lfs pull` if model files are missing.
- **Gemini chatbot** (Streamlit sidebar): set `GEMINI_API_KEY` in a `.env` file or Streamlit secrets. Optionally, set `GEMINI_MODEL` (default `gemini-1.5-flash`) or a fully-qualified `GEMINI_REST_URL` if you need a different Google Generative Language endpoint.

Project structure (high level)

```
Intelligent-Crop-Irrigation-Advisor/
├── frontend/streamlit_dashboard/   # Streamlit UI and launchers
├── models/                         # Trained model artifacts and training scripts
├── data/                           # Datasets used for training and testing
├── docs/                           # Extended documentation and user guides
├── tests/                          # Unit tests
└── requirements.txt                # Python dependency pinning
```

For developer documentation and detailed model docs see the `docs/` folder.

Last updated: 2025-11-14
```
   - 23 engineered features including NPK ratios, evapotranspiration, soil saturation
