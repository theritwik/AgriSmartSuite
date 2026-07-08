# 🌾 AgriSmartSuite — Smart Agriculture Solution

**AgriSmartSuite** is a full-stack, AI-powered web application that helps farmers
and agri-researchers with intelligent **crop recommendation** and **crop yield
prediction**. It pairs a **Flask (Python)** ML backend with a modern
**React (Vite + Tailwind CSS)** frontend.

---

## 🚀 Features

- ✅ **Crop Recommendation** — suggests the best crop from soil/climate inputs
  (N, P, K, temperature, humidity, pH, rainfall). Model test accuracy: **~99.8%**.
- 📈 **Crop Yield Prediction** — estimates yield (hg/ha) from area, crop, year,
  rainfall, pesticide use and temperature, with historical context and warnings.
- 📊 **Interactive charts** — yield trends and recommendation breakdowns (Recharts).
- 🧩 **Clean full-stack architecture** — Flask JSON API + React SPA.
- ⚠️ **Robust validation** — graceful handling of unknown area/crop combinations
  and out-of-range inputs.

---

## 🏗️ Project Structure

```
AgriSmartSuite/
├── app.py                     # Flask JSON API (main backend entry point)
├── requirements.txt           # Backend Python dependencies
├── model.pkl                  # Crop-recommendation classifier
├── minmaxscaler.pkl           # Crop-recommendation preprocessing
├── standscaler.pkl            # Crop-recommendation preprocessing
├── dtr.joblib / dtr.pkl       # Crop-yield regressor
├── preprocessor.joblib/.pkl   # Crop-yield preprocessing
├── tests/                     # pytest API + regression tests
│
├── agrismart-react/           # React frontend (Vite + Tailwind)
│   └── src/
│       ├── components/
│       ├── App.jsx
│       └── main.jsx
│
├── Crop_Recommendation-main/  # Recommendation dataset, notebook & training script
│   ├── Crop_recommendation.csv
│   └── train_model.py         # Reproduces model.pkl / *scaler.pkl
│
└── Crop_Yield_Prediction-main/# Yield dataset, notebook & training script
    ├── yield_df.csv
    └── retrain_model.py
```

---

## 🛠️ Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm**

---

## 🐍 Backend Setup (Flask API)

```bash
# From the project root
python -m venv .venv

# Activate it
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows (PowerShell/CMD)

pip install -r requirements.txt
python app.py
```

The API starts at **http://localhost:5000**.

### Configuration (environment variables)

| Variable      | Default     | Description                          |
|---------------|-------------|--------------------------------------|
| `FLASK_HOST`  | `127.0.0.1` | Interface to bind to                 |
| `FLASK_PORT`  | `5000`      | Port to listen on                    |
| `FLASK_DEBUG` | `false`     | Enable Flask debug/reloader          |

See `.env.example`. For development you can run `FLASK_DEBUG=true python app.py`.

---

## ⚛️ Frontend Setup (React + Vite)

```bash
cd agrismart-react
npm install
npm run dev
```

The app is served at **http://localhost:5173** and proxies API calls to the
Flask backend (see `vite.config.js`), so start the backend first.

---

## 📡 API Reference

| Method | Endpoint                 | Description                                        |
|--------|--------------------------|----------------------------------------------------|
| GET    | `/`                      | Health check                                       |
| POST   | `/predict-crop`          | Recommend a crop from soil/climate parameters      |
| POST   | `/predict-yield`         | Predict crop yield with historical context         |
| GET    | `/api/available-options` | Areas, crops, valid ranges and dataset statistics  |
| GET    | `/get_options`           | Simple list of areas and crops                     |

**Example — crop recommendation**

```bash
curl -X POST http://localhost:5000/predict-crop \
  -H "Content-Type: application/json" \
  -d '{"Nitrogen":90,"Phosporus":42,"Potassium":43,"Temperature":20.88,
       "Humidity":82,"pH":6.5,"Rainfall":202.94}'
# -> {"cropName": "Rice", ...}
```

---

## 🧪 Testing

```bash
pip install -r requirements.txt
pytest
```

The suite covers every endpoint and includes regression tests that guard the
crop-recommendation accuracy (canonical dataset samples must resolve to their
true crop).

---

## 🔁 Retraining the Models

```bash
# Crop recommendation -> model.pkl, minmaxscaler.pkl, standscaler.pkl
python Crop_Recommendation-main/train_model.py

# Crop yield -> dtr.joblib, preprocessor.joblib
cd Crop_Yield_Prediction-main && python retrain_model.py
```

---

## 📜 License

Licensed under the [MIT License](LICENSE).

## 🙌 Credits

- ML models trained on public datasets from Kaggle.
- Built with ❤️ by Ritwik Singh.

## 📬 Contact

For questions or collaboration, open an issue on GitHub.
