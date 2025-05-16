# AgriSmartSuite

# 🌾 AgriSmartSuite - Smart Agriculture Solution

**AgriSmartSuite** is a full-stack AI-powered web application designed to assist farmers and agri-researchers with intelligent **crop recommendation** and **crop yield prediction**. Powered by real agricultural datasets and machine learning models, the application provides smart suggestions and data-driven insights to optimize agricultural decision-making.

Built with a **Flask (Python)** backend and a modern **React (Vite + Tailwind CSS)** frontend, AgriSmartSuite delivers a responsive, interactive, and user-friendly experience.

---

## 🚀 Features

- ✅ **Crop Recommendation System** – Suggests the most suitable crop based on environmental parameters like nitrogen, phosphorus, potassium, humidity, temperature, and pH.
- 📈 **Crop Yield Prediction** – Predicts yield based on area, crop type, and conditions.
- 🌍 **Location & Crop Selectors** – Dropdowns populated dynamically from datasets.
- 📊 **Interactive Charts** – Visualizations of predictions, trends, and recommendations.
- 💡 **Machine Learning Integration** – Trained models for both recommendation and prediction.
- 🧩 **Modular Full-Stack Architecture** – Clean separation of backend and frontend.
- ⚠️ **Robust Error Handling** – Graceful management of invalid inputs or missing data.
- 🎨 **Modern UI** – Responsive and clean design with Tailwind CSS.

---

## 🏗️ Project Structure

AgriSmartSuite/
│
├── agrismart-react/ # React frontend (Vite + Tailwind)
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ ├── pages/
│ │ ├── App.jsx
│ │ └── main.jsx
│ └── vite.config.js
│
├── backend/ # Flask backend
│ ├── app.py # Main Flask app
│ ├── models/ # Trained ML models
│ ├── utils/ # Preprocessing and helper functions
│ └── requirements.txt
│
├── Crop_Recommendation-main/ # Dataset and training notebook (recommendation)
├── Crop_Yield_Prediction-main/ # Dataset and training notebook (yield)
└── README.md


---

## 🛠️ Setup Instructions (Windows)

### 🔧 Prerequisites

- **Python 3.8+** (for Flask backend)
- **Node.js v16+** (for React frontend with Vite)
- **pip** and **npm** installed

---

## 🐍 Backend Setup (Flask API)

```bash
# Navigate to backend folder
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py

The Flask server will start at http://localhost:5000.

# Navigate to frontend directory
cd agrismart-react

# Install dependencies
npm install

# Run the frontend app
npm run dev

The app will be available at http://localhost:5173.

🔁 Ensure the Flask backend is running before using the frontend to get predictions and recommendations.

📜 License
This project is licensed under the MIT License. See the LICENSE file for more details.

🙌 Credits
ML Models trained using public datasets from Kaggle

UI design inspired by modern agri-tech dashboards

Built with ❤️ by Ritwik Singh

📬 Contact
For questions or collaboration, please reach out at [theritwiksingh@gmail.com] or open an issue on GitHub.
