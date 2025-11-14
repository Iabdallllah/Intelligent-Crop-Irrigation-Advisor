from flask import Flask, render_template, request, redirect, url_for
import os
import joblib
import numpy as np
from flask import jsonify
import pandas as pd

app = Flask(__name__)

MODEL_STATUS = {
    'crop_model': False,
    'irrigation_model': False,
    'optimization_model': False
}


# Lightweight mock model available per-request (so UI can toggle mock predictions)
class MockModel:
    def __init__(self, name='mock'):
        self.name = name

    def predict(self, X):
        if 'crop' in self.name:
            return ['maize']
        if 'irrigation' in self.name:
            return [0]
        return [10.0]

    def predict_proba(self, X):
        import numpy as _np
        # return a two-class like array for compatibility
        return _np.array([[0.1, 0.9]])

def compute_results(inputs: dict, use_mock: bool = False):
    """Compute prediction results from input dict. Returns a serializable dict.
    This is reused by both template rendering and the JSON API.
    """
    N = inputs.get('N')
    P = inputs.get('P')
    K = inputs.get('K')
    temp = inputs.get('temp')
    hum = inputs.get('hum')
    ph = inputs.get('ph')
    rain = inputs.get('rain')
    soil_moisture = inputs.get('soil_moisture')
    wind_speed = inputs.get('wind_speed')
    pressure = inputs.get('pressure')

    results = {'input_summary': inputs}

    # Crop
    if use_mock:
        try:
            mock = MockModel('crop')
            prediction = mock.predict(None)[0]
            confidence = float(mock.predict_proba(None).max())
            results['crop'] = {'status': 'ok', 'value': str(prediction), 'confidence': confidence}
        except Exception as e:
            results['crop'] = {'status': 'error', 'msg': str(e)}
    elif crop_model and MODEL_STATUS['crop_model']:
        try:
            feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            input_data = pd.DataFrame([[N, P, K, temp, hum, ph, rain]], columns=feature_names)
            prediction = crop_model.predict(input_data)[0]
            try:
                confidence = float(crop_model.predict_proba(input_data).max())
            except Exception:
                confidence = None

            if confidence is not None and confidence < 0.7:
                results['crop'] = {'status': 'low_confidence', 'value': None, 'confidence': confidence}
            else:
                results['crop'] = {'status': 'ok', 'value': str(prediction), 'confidence': confidence}
        except Exception as e:
            results['crop'] = {'status': 'error', 'msg': str(e)}
    else:
        results['crop'] = {'status': 'unavailable'}

    # Irrigation
    if use_mock:
        try:
            mock = MockModel('irrigation')
            pred = mock.predict(None)[0]
            prob = float(mock.predict_proba(None).max())
            results['irrigation'] = {'pred': str(pred), 'prob': prob}
        except Exception as e:
            results['irrigation'] = {'status': 'error', 'msg': str(e)}
    elif irrigation_model and MODEL_STATUS['irrigation_model']:
        try:
            feats = create_irrigation_features(soil_moisture, temp, hum, ph, N, P, K, rain)
            pred = irrigation_model.predict(feats)[0]
            try:
                prob = float(irrigation_model.predict_proba(feats).max())
            except Exception:
                prob = None

            results['irrigation'] = {'pred': str(pred), 'prob': prob}
        except Exception as e:
            results['irrigation'] = {'status': 'error', 'msg': str(e)}
    else:
        results['irrigation'] = {'status': 'unavailable'}

    # Optimization
    if use_mock:
        try:
            mock = MockModel('optimization')
            opt = float(mock.predict(None)[0])
            results['optimization'] = {'value': opt}
        except Exception as e:
            results['optimization'] = {'status': 'error', 'msg': str(e)}
    elif optimization_model and MODEL_STATUS['optimization_model']:
        try:
            ofeats = create_optimization_features(soil_moisture, temp, hum, ph, N, P, K, rain)
            opt = optimization_model.predict(ofeats)[0]
            results['optimization'] = {'value': float(opt)}
        except Exception as e:
            results['optimization'] = {'status': 'error', 'msg': str(e)}
    else:
        results['optimization'] = {'status': 'unavailable'}

    return results


def repo_root_path():
    current_file = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(os.path.dirname(current_file)))


def load_crop_model():
    model_path = os.path.join(repo_root_path(), "models", "crop recommendation", "crop_model.pkl")
    if os.path.exists(model_path):
        # Detect Git LFS pointer files (small text files) and avoid trying to unpickle them
        try:
            with open(model_path, 'r', encoding='utf-8', errors='ignore') as f:
                head = f.read(128)
            if 'git-lfs' in head:
                print(f"Crop model at {model_path} appears to be a Git LFS pointer (not the real model file).")
                MODEL_STATUS['crop_model'] = False
                return None
        except Exception:
            # If reading as text fails, continue and attempt to load as a binary pickle
            pass
        try:
            m = joblib.load(model_path)
            MODEL_STATUS['crop_model'] = True
            return m
        except Exception as e:
            MODEL_STATUS['crop_model'] = False
            print(f"Error loading crop model: {e}")
    else:
        print(f"Crop model not found at {model_path}")
    return None


def load_irrigation_model():
    model_path = os.path.join(repo_root_path(), "models", "Smart_Irrigation_Classifier", "catboost_model.pkl")
    if os.path.exists(model_path):
        try:
            with open(model_path, 'r', encoding='utf-8', errors='ignore') as f:
                head = f.read(128)
            if 'git-lfs' in head:
                print(f"Irrigation model at {model_path} appears to be a Git LFS pointer (not the real model file).")
                MODEL_STATUS['irrigation_model'] = False
                return None
        except Exception:
            pass
        try:
            m = joblib.load(model_path)
            MODEL_STATUS['irrigation_model'] = True
            return m
        except Exception as e:
            MODEL_STATUS['irrigation_model'] = False
            print(f"Error loading irrigation model: {e}")
    else:
        print(f"Irrigation model not found at {model_path}")
    return None


def load_optimization_model():
    model_path = os.path.join(repo_root_path(), "models", "irrigation_optimization_model", "catboost_irrigation_model.pkl")
    if os.path.exists(model_path):
        try:
            with open(model_path, 'r', encoding='utf-8', errors='ignore') as f:
                head = f.read(128)
            if 'git-lfs' in head:
                print(f"Optimization model at {model_path} appears to be a Git LFS pointer (not the real model file).")
                MODEL_STATUS['optimization_model'] = False
                return None
        except Exception:
            pass
        try:
            m = joblib.load(model_path)
            MODEL_STATUS['optimization_model'] = True
            return m
        except Exception as e:
            MODEL_STATUS['optimization_model'] = False
            print(f"Error loading optimization model: {e}")
    else:
        print(f"Optimization model not found at {model_path}")
    return None


# Feature creation helpers (lightweight ports of Streamlit helpers)
def create_irrigation_features(soil_moisture, temperature, humidity, ph, n, p, k, rainfall=0):
    soil_humidity = humidity * 0.8
    relative_soil_saturation = min(soil_moisture / 100.0, 1.0)
    temp_diff = abs(temperature - 25)
    evapotranspiration = max(0, (temperature - 10) * 0.1 + (100 - humidity) * 0.05)
    rain_vs_soil = rainfall / max(soil_moisture, 1)
    ph_encoded = 1 if ph > 7 else 0
    np_ratio = n / max(p, 1)
    nk_ratio = n / max(k, 1)
    npk_balance = (n + p + k) / 3
    crop_encoded = 1
    rain_3days = rainfall * 3
    moisture_temp_ratio = soil_moisture / max(temperature, 1)
    evapo_ratio = evapotranspiration / max(rainfall, 0.1)
    rain_effect = min(rainfall / 10, 1.0)
    moisture_change_rate = 0.1
    temp_scaled = temperature / 40
    wind_ratio = 0.5

    return np.array([[
        soil_moisture, temperature, soil_humidity, relative_soil_saturation,
        temp_diff, evapotranspiration, rain_vs_soil, rainfall, ph_encoded,
        n, p, k, np_ratio, nk_ratio, crop_encoded, rain_3days,
        moisture_temp_ratio, evapo_ratio, rain_effect, moisture_change_rate,
        temp_scaled, npk_balance, wind_ratio
    ]])


def create_optimization_features(soil_moisture, temperature, humidity, ph, n, p, k, rainfall=0):
    soil_humidity = humidity * 0.8
    wind_speed = 10
    pressure = 101.325
    soil_moisture_diff = 0.1
    relative_soil_saturation = min(soil_moisture / 100.0, 1.0)
    temp_diff = abs(temperature - 25)
    wind_effect = wind_speed * 0.1
    evapotranspiration = max(0, (temperature - 10) * 0.1 + (100 - humidity) * 0.05)
    rain_3days = rainfall * 3
    rain_vs_soil = rainfall / max(soil_moisture, 1)
    np_ratio = n / max(p, 1)
    nk_ratio = n / max(k, 1)
    npk_balance = (n + p + k) / 3
    ph_encoded = 1 if ph > 7 else 0
    crop_encoded = 1
    moisture_temp_ratio = soil_moisture / max(temperature, 1)
    evapo_ratio = evapotranspiration / max(rainfall, 0.1)
    rain_effect = min(rainfall / 10, 1.0)
    moisture_change_rate = 0.1
    temp_scaled = temperature / 40
    wind_ratio = wind_speed / 50

    return np.array([[
        soil_moisture, temperature, soil_humidity, # trimmed for brevity in model
        wind_speed, humidity, wind_speed * 1.5, pressure, ph, rainfall,
        n, p, k, soil_moisture_diff, relative_soil_saturation,
        temp_diff, wind_effect, evapotranspiration, rain_3days,
        rain_vs_soil, np_ratio, nk_ratio, ph_encoded, crop_encoded,
        moisture_temp_ratio, evapo_ratio, rain_effect, moisture_change_rate,
        temp_scaled, npk_balance, wind_ratio
    ]])


# Support a mock mode when real models are not available (useful for UI testing)
MOCK_MODE = os.getenv('FLASK_MOCK_MODE', '0') in ('1', 'true', 'True')

crop_model = load_crop_model()
irrigation_model = load_irrigation_model()
optimization_model = load_optimization_model()

if MOCK_MODE:
    # Provide lightweight mock models that mimic the sklearn API used in the app
    class _MockModel:
        def __init__(self, name='mock'):
            self.name = name
        def predict(self, X):
            # return a plausible value depending on model type
            if 'crop' in self.name:
                return ['maize']
            if 'irrigation' in self.name:
                return [0]
            return [10.0]
        def predict_proba(self, X):
            import numpy as _np
            return _np.array([[0.1, 0.9]])

    if not crop_model:
        crop_model = _MockModel('crop_mock')
        MODEL_STATUS['crop_model'] = True
    if not irrigation_model:
        irrigation_model = _MockModel('irrigation_mock')
        MODEL_STATUS['irrigation_model'] = True
    if not optimization_model:
        optimization_model = _MockModel('optimization_mock')
        MODEL_STATUS['optimization_model'] = True


def system_operational():
    return all(MODEL_STATUS.values())


@app.route('/', methods=['GET'])
def index():
    status = MODEL_STATUS
    return render_template('index.html', status=status)


@app.route('/predict', methods=['POST'])
def predict():
    # Parse inputs
    try:
        N = float(request.form.get('N', 80))
        P = float(request.form.get('P', 48))
        K = float(request.form.get('K', 40))
        temp = float(request.form.get('temp', 23.0))
        hum = float(request.form.get('hum', 82.0))
        ph = float(request.form.get('ph', 6.7))
        rain = float(request.form.get('rain', 240.0))
        soil_moisture = float(request.form.get('soil_moisture', 0.35))
        wind_speed = float(request.form.get('wind_speed', 8.0))
        pressure = float(request.form.get('pressure', 101.3))
    except Exception as e:
        return render_template('result.html', error=f"Invalid inputs: {e}")

    results = {
        'input_summary': {
            'N': N, 'P': P, 'K': K, 'temp': temp, 'hum': hum, 'ph': ph, 'rain': rain,
            'soil_moisture': soil_moisture, 'wind_speed': wind_speed, 'pressure': pressure
        }
    }

    use_mock = request.form.get('use_mock') == 'on'

    # Crop recommendation
    if use_mock:
        # use per-request mock regardless of server MOCK_MODE
        try:
            mock = MockModel('crop')
            prediction = mock.predict(None)[0]
            confidence = mock.predict_proba(None).max()
            results['crop'] = {'status': 'ok', 'value': str(prediction), 'confidence': float(confidence)}
        except Exception as e:
            results['crop'] = {'status': 'error', 'msg': str(e)}
    elif crop_model and MODEL_STATUS['crop_model']:
        try:
            feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
            input_data = pd.DataFrame([[N, P, K, temp, hum, ph, rain]], columns=feature_names)
            prediction = crop_model.predict(input_data)[0]
            try:
                confidence = float(crop_model.predict_proba(input_data).max())
            except Exception:
                confidence = None

            if confidence is not None and confidence < 0.7:
                results['crop'] = {'status': 'low_confidence', 'value': None, 'confidence': confidence}
            else:
                results['crop'] = {'status': 'ok', 'value': str(prediction), 'confidence': confidence}
        except Exception as e:
            results['crop'] = {'status': 'error', 'msg': str(e)}
    else:
        results['crop'] = {'status': 'unavailable'}

    # Irrigation decision
    if use_mock:
        try:
            mock = MockModel('irrigation')
            pred = mock.predict(None)[0]
            prob = float(mock.predict_proba(None).max())
            results['irrigation'] = {'pred': str(pred), 'prob': prob}
        except Exception as e:
            results['irrigation'] = {'status': 'error', 'msg': str(e)}
    elif irrigation_model and MODEL_STATUS['irrigation_model']:
        try:
            feats = create_irrigation_features(soil_moisture, temp, hum, ph, N, P, K, rain)
            pred = irrigation_model.predict(feats)[0]
            try:
                prob = float(irrigation_model.predict_proba(feats).max())
            except Exception:
                prob = None

            results['irrigation'] = {'pred': str(pred), 'prob': prob}
        except Exception as e:
            results['irrigation'] = {'status': 'error', 'msg': str(e)}
    else:
        results['irrigation'] = {'status': 'unavailable'}

    # Optimization
    if use_mock:
        try:
            mock = MockModel('optimization')
            opt = float(mock.predict(None)[0])
            results['optimization'] = {'value': opt}
        except Exception as e:
            results['optimization'] = {'status': 'error', 'msg': str(e)}
    elif optimization_model and MODEL_STATUS['optimization_model']:
        try:
            ofeats = create_optimization_features(soil_moisture, temp, hum, ph, N, P, K, rain)
            opt = optimization_model.predict(ofeats)[0]
            results['optimization'] = {'value': float(opt)}
        except Exception as e:
            results['optimization'] = {'status': 'error', 'msg': str(e)}
    else:
        results['optimization'] = {'status': 'unavailable'}

    return render_template('result.html', results=results)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    # Accept JSON or form data
    if request.is_json:
        payload = request.get_json()
    else:
        payload = request.form.to_dict()

    # Convert numeric fields
    def _getf(d, key, default=0.0):
        try:
            return float(d.get(key, default))
        except Exception:
            return default

    inputs = {
        'N': _getf(payload, 'N', 80),
        'P': _getf(payload, 'P', 48),
        'K': _getf(payload, 'K', 40),
        'temp': _getf(payload, 'temp', 23.0),
        'hum': _getf(payload, 'hum', 82.0),
        'ph': _getf(payload, 'ph', 6.7),
        'rain': _getf(payload, 'rain', 240.0),
        'soil_moisture': _getf(payload, 'soil_moisture', 0.35),
        'wind_speed': _getf(payload, 'wind_speed', 8.0),
        'pressure': _getf(payload, 'pressure', 101.3)
    }

    use_mock = payload.get('use_mock') in (True, 'true', '1', 'on', 'yes')

    results = compute_results(inputs, use_mock=use_mock)

    return jsonify(results)


if __name__ == '__main__':
    # Run with a port commonly used by the Streamlit app so it's easy to compare
    app.run(host='0.0.0.0', port=8503, debug=True)
