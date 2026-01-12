import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

def load_and_prepare_data(csv_path="data/user_logs.csv"):
    df = pd.read_csv(csv_path)

    # Label
    df["skipped"] = df["response_type"].apply(
        lambda x: 1 if x in ["skipped", "ignored"] else 0
    )

    # Time feature
    df["hour"] = df["planned_time"].str.split(":").str[0].astype(int)

    # Day of week
    df["day_of_week"] = pd.to_datetime(df["date"]).dt.dayofweek

    # Category encoding
    df = pd.get_dummies(df, columns=["category"], drop_first=True)

    X = df.drop(columns=["response_type", "skipped", "date"])
    y = df["skipped"]

    return X, y

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(model, "app/ml/models/skip_predictor.pkl")