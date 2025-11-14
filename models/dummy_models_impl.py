"""Compatibility stubs used when loading lightweight pickled 'dummy' model objects.

Some model pickle files reference classes defined under
`models.dummy_models_impl` (e.g. `DummyCropModel`, `DummyIrrigationModel`).
When those classes are not present during unpickling Python raises
ModuleNotFoundError. This file provides minimal, safe fallback
implementations that emulate scikit-learn-like predict / predict_proba
APIs so the app can continue running if the real model binaries are
missing or contain lightweight dummy wrappers.

These implementations use simple heuristics and should be replaced by
real trained models for production use.
"""

from __future__ import annotations
import numpy as np


class DummyCropModel:
    """Very small heuristic model to emulate crop recommendations.

    predict(X) -> array of string labels (one per row)
    predict_proba(X) -> array of floats (n_samples, 1) with a confidence score
    """
    def __init__(self):
        # permitted to be constructed with no args (matches pickles)
        pass

    def predict(self, X):
        # X is expected to be 2D array-like with columns [N, P, K, temp, hum, ph, rainfall]
        X = np.asarray(X)
        out = []
        for row in X:
            try:
                rainfall = float(row[6])
                temp = float(row[3])
            except Exception:
                rainfall = 0.0
                temp = 20.0
            # more responsive heuristic using multiple inputs so predictions vary
            try:
                N = float(row[0])
                P = float(row[1])
                K = float(row[2])
                hum = float(row[4])
                ph = float(row[5])
            except Exception:
                N = P = K = hum = ph = 0.0

            # compute a more responsive score which weights N/P/K and rainfall
            # to make the model react to moderate input changes in UI
            rainfall_norm = (rainfall / 300.0)  # 0..1
            n_norm = (N - 50.0) / 100.0         # roughly -0.5..+1.5
            p_norm = (P - 30.0) / 120.0
            k_norm = (K - 30.0) / 120.0
            hum_norm = (hum - 50.0) / 50.0
            temp_norm = (temp - 25.0) / 25.0

            score = (
                0.40 * rainfall_norm +
                0.30 * n_norm +
                0.10 * p_norm +
                0.05 * k_norm +
                0.10 * hum_norm -
                0.15 * temp_norm
            )

            # map score to crop choices with finer-grained thresholds
            if score > 0.45:
                out.append('rice')
            elif score > 0.20:
                out.append('maize')
            elif score > 0.05:
                out.append('mango')
            elif score > -0.15:
                out.append('chickpea')
            elif score > -0.35:
                out.append('lentil')
            else:
                out.append('mothbeans')
        return np.array(out)

    def predict_proba(self, X):
        X = np.asarray(X)
        # compute a confidence value based on feature spread; higher absolute score -> higher confidence
        probs = []
        for row in X:
            try:
                rainfall = float(row[6])
                temp = float(row[3])
                N = float(row[0])
                hum = float(row[4])
            except Exception:
                rainfall = temp = N = hum = 0.0
            # Recompute using the same normalization as predict() for consistency
            rainfall_norm = (rainfall / 300.0)
            n_norm = (N - 50.0) / 100.0
            hum_norm = (hum - 50.0) / 50.0
            temp_norm = (temp - 25.0) / 25.0
            score = abs(0.40 * rainfall_norm + 0.30 * n_norm + 0.10 * 0 - 0.15 * temp_norm + 0.10 * hum_norm)
            # normalize to [0.35, 0.99] with more spread
            conf = min(0.99, max(0.15, 0.35 + score * 0.6))
            probs.append([conf])
        return np.asarray(probs)


class DummyIrrigationModel:
    """Heuristic binary model for irrigation decision.

    predict(X) -> array of 0/1 (1 = irrigate)
    predict_proba(X) -> array of floats (n_samples, 1) with confidence
    """
    def __init__(self):
        pass

    def predict(self, X):
        X = np.asarray(X)
        out = []
        for row in X:
            # our irrigation features place soil_moisture as first column
            try:
                soil_moisture = float(row[0])
            except Exception:
                soil_moisture = 0.0
            # include temperature proxy (if present at index 1) and rainfall-like feature at index 7
            temp = float(row[1]) if len(row) > 1 else 25.0
            rain = float(row[7]) if len(row) > 7 else 0.0
            # compute irrigation need score
            need = (0.35 - soil_moisture) + max(0, (temp - 30) / 50.0) + max(0, (50 - rain) / 100.0)
            out.append(1 if need > 0.15 else 0)
        return np.array(out)

    def predict_proba(self, X):
        X = np.asarray(X)
        probs = []
        for row in X:
            try:
                soil_moisture = float(row[0])
                temp = float(row[1]) if len(row) > 1 else 25.0
                rain = float(row[7]) if len(row) > 7 else 0.0
            except Exception:
                soil_moisture = temp = rain = 0.0
            score = (0.35 - soil_moisture) + max(0, (temp - 30) / 50.0) + max(0, (50 - rain) / 100.0)
            conf = min(0.99, 0.4 + max(0, score))
            probs.append([conf])
        return np.asarray(probs)
