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

            # simple heuristic: high rainfall and moderate temp -> rice, else maize
            if rainfall > 150 and temp < 30:
                out.append('rice')
            else:
                out.append('maize')
        return np.array(out)

    def predict_proba(self, X):
        X = np.asarray(X)
        # return a single-column confidence (best class) to be compatible with .max()
        probs = []
        for _ in X:
            probs.append([0.9])
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
            # if soil moisture low -> irrigate
            out.append(1 if soil_moisture < 0.3 else 0)
        return np.array(out)

    def predict_proba(self, X):
        X = np.asarray(X)
        probs = []
        for row in X:
            try:
                soil_moisture = float(row[0])
            except Exception:
                soil_moisture = 0.0
            conf = 0.9 if soil_moisture < 0.3 else 0.85
            probs.append([conf])
        return np.asarray(probs)
