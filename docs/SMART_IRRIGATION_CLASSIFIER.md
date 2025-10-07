# Smart Irrigation Classifier — Documentation

This document describes the CatBoost classifier provided in `models/Smart_Irrigation_Classifier/catboost_model.pkl` and how to use, inspect, and retrain it.

## Purpose

The classifier predicts an irrigation decision / class (for example: `irrigate` vs `do_not_irrigate`) based on environmental and soil features. It's used by the Smart Irrigation component to automate irrigation scheduling.

## Files

- `models/Smart_Irrigation_Classifier/catboost_model.pkl` — trained CatBoost model (stored with Git LFS). Do not modify directly. Use training script to regenerate.
- `models/Smart_Irrigation_Classifier/train_model.py` — training script. Review to see exact feature preparation.

## Environment & Dependencies

Recommended Python environment (example):

```
Python 3.9+
pip install -r requirements.txt
# ensure git-lfs is installed if cloning the repo and you need to fetch the .pkl
```

Key libraries used:
- catboost
- pandas
- scikit-learn (for preprocessing/splitting)
- joblib (for model save/load)

## Input features (expected)

The model expects features in the same order and format used during training. Check `train_model.py` for exact names. Typical features include:
- `soil_moisture` (float)
- `temperature` (float, °C)
- `humidity` (float, %)
- `rainfall` (float, mm)
- `crop_type` (categorical) — must be encoded the same way as in training

If training used additional engineered features (rolling averages, season flags, etc.) you must compute the same features at inference time.

## Quick inference example

```python
import joblib
import pandas as pd

model = joblib.load('models/Smart_Irrigation_Classifier/catboost_model.pkl')

sample = pd.DataFrame([{
    'soil_moisture': 0.23,
    'temperature': 28.5,
    'humidity': 60.0,
    'rainfall': 0.0,
    'crop_type': 'wheat'
}])

# If you have a preprocessing pipeline, run it here (load transformers or reimplement steps from train_model.py)
pred = model.predict(sample)
proba = model.predict_proba(sample) if hasattr(model, 'predict_proba') else None
print('pred', pred, 'proba', proba)
```

## Retraining

To retrain the model:

1. Inspect and prepare the dataset used for training. The repo contains `data/` CSVs — confirm which was used in `train_model.py`.
2. Open `models/Smart_Irrigation_Classifier/train_model.py` and follow the script steps (preprocessing, train/test split, CatBoost training parameters).
3. Update hyperparameters or features as needed and run the script. Example:

```
python models/Smart_Irrigation_Classifier/train_model.py --output models/Smart_Irrigation_Classifier/catboost_model.pkl
```

4. If retrained and you want to publish the new model file, commit and push. Since `*.pkl` is configured for Git LFS (see `.gitattributes`), Git LFS will handle the large binary automatically.

## Versioning & Storage

- Because model binaries are large, they are tracked with Git LFS. Ensure collaborators have `git lfs` installed and run `git lfs pull` after cloning to fetch the actual binaries.

## Troubleshooting

- If `joblib.load` fails due to package version mismatch, try using the same library versions used during training.
- If performance drops after retraining, check the preprocessing steps and random seeds.