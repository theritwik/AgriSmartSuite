"""Train the crop-recommendation model and preprocessing scalers.

This script is fully reproducible: running it regenerates ``model.pkl``,
``minmaxscaler.pkl`` and ``standscaler.pkl`` in the project root, which are the
artifacts loaded by ``app.py``.

Background
----------
The models originally shipped with this repository were broken: the
``MinMaxScaler`` had been fit on a *single* row of the dataset
(``data_min_ == data_max_`` for every feature), which destroyed input
normalisation and dropped the classifier's accuracy to ~16%. Retraining the
whole pipeline on the full dataset restores ~99.8% test accuracy.

Usage
-----
    python Crop_Recommendation-main/train_model.py
"""

from __future__ import annotations

import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Label -> integer mapping. MUST stay in sync with ``crop_dict`` in app.py.
CROP_TO_ID = {
    "rice": 1, "maize": 2, "jute": 3, "cotton": 4, "coconut": 5,
    "papaya": 6, "orange": 7, "apple": 8, "muskmelon": 9, "watermelon": 10,
    "grapes": 11, "mango": 12, "banana": 13, "pomegranate": 14, "lentil": 15,
    "blackgram": 16, "mungbean": 17, "mothbeans": 18, "pigeonpeas": 19,
    "kidneybeans": 20, "chickpea": 21, "coffee": 22,
}

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
RANDOM_STATE = 42

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parent
DATASET = HERE / "Crop_recommendation.csv"


def main() -> None:
    df = pd.read_csv(DATASET)
    df["label_id"] = df["label"].str.lower().map(CROP_TO_ID)
    if df["label_id"].isna().any():
        unknown = sorted(df.loc[df["label_id"].isna(), "label"].unique())
        raise ValueError(f"Unmapped crop labels in dataset: {unknown}")

    X = df[FEATURES].values
    y = df["label_id"].astype(int).values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    minmax = MinMaxScaler().fit(X_train)
    standard = StandardScaler().fit(minmax.transform(X_train))

    def preprocess(data):
        return standard.transform(minmax.transform(data))

    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(preprocess(X_train), y_train)

    accuracy = accuracy_score(y_test, model.predict(preprocess(X_test)))
    print(f"Test accuracy: {accuracy:.4f}")
    if accuracy < 0.95:
        raise RuntimeError(f"Accuracy {accuracy:.4f} below expected threshold (0.95)")

    artifacts = {
        "model.pkl": model,
        "minmaxscaler.pkl": minmax,
        "standscaler.pkl": standard,
    }
    for filename, obj in artifacts.items():
        with open(PROJECT_ROOT / filename, "wb") as fh:
            pickle.dump(obj, fh)
        print(f"Saved {filename}")


if __name__ == "__main__":
    main()
