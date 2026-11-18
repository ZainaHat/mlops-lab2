import pandas as pd

NUMERIC = [
    "tenure_months",
    "monthly_charges",
    "support_calls",
]

CATEGORICAL = [
    "contract",
    "internet_service",
]

FEATURES = NUMERIC + CATEGORICAL

TARGET = "churn"


def validate(df: pd.DataFrame) -> pd.DataFrame:
    required = FEATURES + [TARGET]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return df