import joblib
import pandas as pd

model = joblib.load("app/ml/models/skip_predictor.pkl")

def predict_skip_probability(hour, day_of_week, category_vector):
    data = {
        "hour": [hour],
        "day_of_week": [day_of_week],
        **category_vector
    }

    df = pd.DataFrame(data)
    probability = model.predict_proba(df)[0][1]

    return probability
