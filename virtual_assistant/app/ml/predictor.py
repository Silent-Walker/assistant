import joblib
import pandas as pd
import os

# Safe model loading
MODEL_PATH = "app/ml/models/skip_predictor.pkl"
model = None

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
    except Exception as e:
        print(f"[Predictor] Warning: Could not load model: {e}")
else:
    print("[Predictor] Warning: Model file not found. Run trainer.py first.")

def predict_skip_probability(hour, day_of_week, category_vector):
    # Fallback if model isn't trained yet
    if model is None:
        return 0.0

    data = {
        "hour": [hour],
        "day_of_week": [day_of_week],
        **category_vector
    }

    try:
        df = pd.DataFrame(data)
        # Ensure columns match what the model expects (alignment)
        # valid_features = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else df.columns
        # df = df.reindex(columns=valid_features, fill_value=0)
        
        probability = model.predict_proba(df)[0][1]
        return probability
    except Exception as e:
        print(f"[Predictor] Error during prediction: {e}")
        return 0.0