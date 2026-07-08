"""Smoke and regression tests for the AgriSmartSuite Flask API.

Run from the project root with:  pytest
"""

import os
import sys

import pytest

# Make the project root importable regardless of where pytest is invoked from.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as agri_app  # noqa: E402


@pytest.fixture()
def client():
    agri_app.app.config.update(TESTING=True)
    return agri_app.app.test_client()


def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "AgriSmartSuite" in resp.get_json()["message"]


def test_get_options_returns_areas_and_crops(client):
    """Regression: /get_options used to read a non-existent 'Crop' column."""
    resp = client.get("/get_options")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["areas"], "expected a non-empty list of areas"
    assert data["crops"], "expected a non-empty list of crops"


def test_available_options(client):
    resp = client.get("/api/available-options")
    assert resp.status_code == 200
    data = resp.get_json()
    for key in ("areas", "crops", "yearRange", "stats"):
        assert key in data


def test_predict_crop_missing_body(client):
    resp = client.post("/predict-crop", json={})
    # Empty JSON body -> 400 (no data) or 500 (missing key); must not 200.
    assert resp.status_code in (400, 500)


@pytest.mark.parametrize(
    "payload,expected",
    [
        ({"Nitrogen": 90, "Phosporus": 42, "Potassium": 43, "Temperature": 20.88,
          "Humidity": 82, "pH": 6.5, "Rainfall": 202.94}, "Rice"),
        ({"Nitrogen": 20, "Phosporus": 134, "Potassium": 200, "Temperature": 22.6,
          "Humidity": 92.3, "pH": 5.9, "Rainfall": 112.6}, "Apple"),
        ({"Nitrogen": 100, "Phosporus": 28, "Potassium": 30, "Temperature": 25.5,
          "Humidity": 58.9, "pH": 6.8, "Rainfall": 158.9}, "Coffee"),
    ],
)
def test_predict_crop_known_samples(client, payload, expected):
    """Regression: the shipped scalers were fit on one row, giving ~16% accuracy.

    These canonical dataset samples must map to their true crop.
    """
    resp = client.post("/predict-crop", json=payload)
    assert resp.status_code == 200
    assert resp.get_json()["cropName"] == expected


def test_predict_yield_known_sample(client):
    resp = client.post(
        "/predict-yield",
        json={"Area": "Albania", "Crop": "Maize", "Year": 2000,
              "average_rain_fall_mm_per_year": 1485, "pesticides_tonnes": 121,
              "avg_temp": 16.37},
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["prediction"] > 0
    assert "metadata" in body


def test_predict_yield_unknown_combination(client):
    resp = client.post(
        "/predict-yield",
        json={"Area": "Atlantis", "Crop": "Unobtainium", "Year": 2000,
              "average_rain_fall_mm_per_year": 1000, "pesticides_tonnes": 10,
              "avg_temp": 20},
    )
    assert resp.status_code == 400
