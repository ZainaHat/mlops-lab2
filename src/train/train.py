"""Train the Lab 1 churn model and save it for the API."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "artifacts" / "model.joblib"

NUMERIC = ["tenure_months", "monthly_charges", "support_calls"]
CATEGORICAL = ["contract", "internet_service"]
FEATURES = NUMERIC + CATEGORICAL


def train():
    df = pd.read_csv(
        ROOT / "churn_v1.csv",
        keep_default_na=False,
    )
    X = df[FEATURES]
    y = df["churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = Pipeline([
        ("prep", ColumnTransformer([
            ("num", StandardScaler(), NUMERIC),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ])),
        ("clf", LogisticRegression(max_iter=1000, random_state=42)),
    ])

    model.fit(X_train, y_train)
    probabilities = model.predict_proba(X_test)[:, 1]

    print(f"F1: {f1_score(y_test, probabilities > 0.5):.3f}")
    print(f"AUC: {roc_auc_score(y_test, probabilities):.3f}")

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Saved model: {MODEL_PATH}")
    return model


if __name__ == "__main__":
    train()
