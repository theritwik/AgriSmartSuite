from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import traceback
import pandas as pd

# Import joblib for model loading
from joblib import load

def load_model(model_name, paths=None):
    """
    Attempts to load a model from multiple possible paths         # Calculate statistics with proper rounding and validation
        def safe_float(value):
            try:
                return float(value) if pd.notnull(value) else 0.0
            except:
                return 0.0
                
        stats = {
            'avg_rainfall': safe_float(yield_df['average_rain_fall_mm_per_year'].mean()),
            'max_rainfall': safe_float(yield_df['average_rain_fall_mm_per_year'].max()),
            'min_rainfall': safe_float(yield_df['average_rain_fall_mm_per_year'].min()),
            'avg_temp': safe_float(yield_df['avg_temp'].mean()),
            'max_temp': safe_float(yield_df['avg_temp'].max()),
            'min_temp': safe_float(yield_df['avg_temp'].min()),
            'avg_pesticides': safe_float(yield_df['pesticides_tonnes'].mean()),
            'max_pesticides': safe_float(yield_df['pesticides_tonnes'].max()),
            'min_pesticides': safe_float(yield_df['pesticides_tonnes'].min()),
            'yield_stats': {
                'avg_yield': safe_float(yield_df['hg/ha_yield'].mean()),
                'max_yield': safe_float(yield_df['hg/ha_yield'].max()),
                'min_yield': safe_float(yield_df['hg/ha_yield'].min())
            }
    """
    if paths is None:
        paths = ['.', 'Crop_Yield_Prediction-main']
    
    errors = []
    for path in paths:
        # Try joblib format
        try:
            model_path = f"{path}/{model_name}.joblib"
            return load(model_path)
        except Exception as e:
            errors.append(f"Failed to load {model_path}: {str(e)}")
        
        # Try pickle format
        try:
            model_path = f"{path}/{model_name}.pkl"
            with open(model_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            errors.append(f"Failed to load {model_path}: {str(e)}")
    
    raise RuntimeError(f"Failed to load {model_name} from any location: {'; '.join(errors)}")

# Load Crop Recommendation models
try:
    crop_rec_model = load_model('model')
    sc = load_model('standscaler')
    mx = load_model('minmaxscaler')
except Exception as e:
    print(f"Error loading crop recommendation models: {str(e)}")
    traceback.print_exc()

# Load Crop Yield Prediction models
try:
    dtr = load_model('dtr')
    preprocessor = load_model('preprocessor')
except Exception as e:
    print(f"Error loading yield prediction models: {str(e)}")
    traceback.print_exc()

# Load and preprocess the yield dataset once when the app starts
yield_df = pd.read_csv('Crop_Yield_Prediction-main/yield_df.csv')

# Clean and validate the data
yield_df = yield_df.dropna()  # Remove rows with missing values
yield_df['Year'] = pd.to_numeric(yield_df['Year'], errors='coerce')
yield_df['average_rain_fall_mm_per_year'] = pd.to_numeric(yield_df['average_rain_fall_mm_per_year'], errors='coerce')
yield_df['pesticides_tonnes'] = pd.to_numeric(yield_df['pesticides_tonnes'], errors='coerce')
yield_df['avg_temp'] = pd.to_numeric(yield_df['avg_temp'], errors='coerce')
yield_df['hg/ha_yield'] = pd.to_numeric(yield_df['hg/ha_yield'], errors='coerce')

# Drop rows with invalid conversions
yield_df = yield_df.dropna()

# Calculate global statistics for validation and UI
GLOBAL_STATS = {
    'min_year': int(yield_df['Year'].min()),
    'max_year': int(yield_df['Year'].max()),
    'min_rain': float(yield_df['average_rain_fall_mm_per_year'].min()),
    'max_rain': float(yield_df['average_rain_fall_mm_per_year'].max()),
    'avg_rain': float(yield_df['average_rain_fall_mm_per_year'].mean()),
    'min_temp': float(yield_df['avg_temp'].min()),
    'max_temp': float(yield_df['avg_temp'].max()),
    'avg_temp': float(yield_df['avg_temp'].mean()),
    'min_pest': float(yield_df['pesticides_tonnes'].min()),
    'max_pest': float(yield_df['pesticides_tonnes'].max()),
    'avg_pest': float(yield_df['pesticides_tonnes'].mean())
}

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return jsonify({"message": "AgriSmartSuite API is running"})

@app.route("/predict-crop", methods=['POST'])
def predict_crop():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        N = float(data['Nitrogen'])
        P = float(data['Phosporus'])
        K = float(data['Potassium'])
        temp = float(data['Temperature'])
        humidity = float(data['Humidity'])
        ph = float(data['pH'])
        rainfall = float(data['Rainfall'])
        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)
        mx_features = mx.transform(single_pred)
        sc_mx_features = sc.transform(mx_features)
        prediction = crop_rec_model.predict(sc_mx_features)
        crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}
        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            message = f"{crop} is the best crop to be cultivated right there"
            data_chart = [
                {"name": crop, "value": 100},
                {"name": "Other Crops", "value": 20}
            ]
        else:
            message = "Sorry, we could not determine the best crop to be cultivated with the provided data."
            data_chart = []
        return jsonify({
            "message": message,
            "data": data_chart,
            "prediction": int(prediction[0]),
            "cropName": crop_dict.get(prediction[0], "Unknown")
        })
    except Exception as e:
        print("Error in predict_crop:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/predict-yield", methods=['POST'])
def predict_yield():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Map 'Crop' to 'Item' for compatibility with the model and dataset
        crop_value = data.get('Crop', '').strip()
        data['Item'] = crop_value

        try:
            Year = int(data.get('Year', 0))
            average_rain_fall_mm_per_year = float(data.get('average_rain_fall_mm_per_year', 0))
            pesticides_tonnes = float(data.get('pesticides_tonnes', 0))
            avg_temp = float(data.get('avg_temp', 0))
            Area = str(data.get('Area', '')).strip()
            Item = str(data.get('Item', '')).strip()

            # Validate all required fields are present
            if not all([Year, average_rain_fall_mm_per_year, avg_temp, Area, Item]):
                return jsonify({
                    "error": "All fields are required: Year, average_rain_fall_mm_per_year, avg_temp, Area, Crop"
                }), 400

            # Get valid ranges from the dataset for this specific area and crop
            area_crop_data = yield_df[(yield_df['Area'] == Area) & (yield_df['Item'] == Item)]
            if area_crop_data.empty:
                return jsonify({"error": "No historical data available for this area and crop combination"}), 400

            min_year = int(area_crop_data['Year'].min())
            max_year = min(int(area_crop_data['Year'].max()) + 5, 2030)
            min_rain = float(area_crop_data['average_rain_fall_mm_per_year'].min())
            max_rain = float(area_crop_data['average_rain_fall_mm_per_year'].max())
            min_temp = float(area_crop_data['avg_temp'].min())
            max_temp = float(area_crop_data['avg_temp'].max())
            min_pest = float(area_crop_data['pesticides_tonnes'].min())
            max_pest = float(area_crop_data['pesticides_tonnes'].max())

            # Validation checks with specific ranges
            warnings = []
            if Year < min_year or Year > max_year:
                warnings.append(f"Year is outside historical range ({min_year}-{max_year}) for {Area}.")
            if average_rain_fall_mm_per_year < min_rain * 0.8 or average_rain_fall_mm_per_year > max_rain * 1.2:
                warnings.append(f"Rainfall is outside typical range ({min_rain:.1f}-{max_rain:.1f} mm) for {Area}.")
            if avg_temp < min_temp - 5 or avg_temp > max_temp + 5:
                warnings.append(f"Temperature is outside typical range ({min_temp:.1f}-{max_temp:.1f}°C) for {Area}.")
            if pesticides_tonnes < 0 or pesticides_tonnes > max_pest * 1.5:
                warnings.append(f"Pesticides are outside typical range (0-{max_pest:.1f} tonnes) for {Area}.")
            # Do not block prediction, just warn

        except (ValueError, KeyError) as e:
            return jsonify({"error": f"Invalid input data: {str(e)}"}), 400
        
        # Get historical data for this area and crop
        historical = yield_df[(yield_df['Area'] == Area) & (yield_df['Item'] == Item)].sort_values('Year', ascending=True)

        if historical.empty:
            return jsonify({
                "error": f"No historical data available for {Item} in {Area}. Please choose a different combination."
            }), 400

        # Make prediction
        features = np.array([[Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item]], dtype=object)
        transformed_features = preprocessor.transform(features)
        prediction = float(dtr.predict(transformed_features)[0])

        # Get historical data for this area and crop
        historical_by_area = yield_df[(yield_df['Area'] == Area)].groupby('Item')['hg/ha_yield'].mean().sort_values(ascending=False)

        # Get top 5 crops for this area
        top_crops = [
            {
                "name": crop,
                "value": float(yield_)
            }
            for crop, yield_ in historical_by_area.head().items()
        ]

        # Get last 5 years of historical data for this specific crop
        recent_historical = historical[historical['Year'] <= Year].tail(5)

        # Prepare response data
        historical_data = []
        if not recent_historical.empty:
            historical_data = [
                {
                    'year': int(row['Year']),
                    'yield': float(row['hg/ha_yield']),
                    'rainfall': float(row['average_rain_fall_mm_per_year']),
                    'temperature': float(row['avg_temp']),
                    'pesticides': float(row['pesticides_tonnes'])
                }
                for _, row in recent_historical.iterrows()
            ]

        # Calculate statistics
        avg_yield = float(historical['hg/ha_yield'].mean())
        yield_difference = prediction - avg_yield
        yield_difference_percent = (yield_difference / avg_yield) * 100 if avg_yield > 0 else 0

        # Determine yield assessment
        if yield_difference_percent > 15:
            assessment = f"Excellent! {Item} in {Area} shows exceptional yield potential"
            suggestion = "Perfect conditions for cultivation"
        elif yield_difference_percent > 5:
            assessment = f"Good choice! {Item} in {Area} is expected to perform well"
            suggestion = "Conditions are favorable for cultivation"
        elif yield_difference_percent > -5:
            assessment = f"{Item} in {Area} shows average yield potential"
            suggestion = "Consider factors that could improve yield"
        else:
            assessment = f"Warning: {Item} might not be optimal for {Area}"
            better_crops = [c["name"] for c in top_crops if c["name"] != Item][:3]
            suggestion = f"Consider: {', '.join(better_crops)} which historically perform better in this area"

        message = f"{assessment}. {suggestion}."

        # Prepare visualization data
        data_chart = [
            *top_crops,  # Show top performing crops in this area
            {"name": f"Predicted {Item}", "value": float(prediction)},
            {"name": f"Average {Item}", "value": float(avg_yield)}
        ]

        return jsonify({
            "message": message,
            "data": data_chart,
            "prediction": float(prediction),
            "metadata": {
                "average_historical_yield": float(avg_yield),
                "min_historical_yield": float(historical['hg/ha_yield'].min()),
                "max_historical_yield": float(historical['hg/ha_yield'].max()),
                "yield_difference": float(yield_difference),
                "yield_difference_percent": float(yield_difference_percent)
            },
            "historical_data": historical_data,
            "features": {
                "year": Year,
                "rainfall": average_rain_fall_mm_per_year,
                "pesticides": pesticides_tonnes,
                "temperature": avg_temp,
                "area": Area,
                "crop": Item
            },
            "warnings": warnings
        })
    except Exception as e:
        print("Error in predict_yield:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/api/available-options", methods=['GET'])
def get_available_options():
    try:
        if yield_df.empty:
            return jsonify({"error": "No data available"}), 500
        # Use 'Item' for crops, matching the CSV
        areas = sorted(yield_df['Area'].unique().tolist())
        crops = sorted(yield_df['Item'].unique().tolist())

        # Get min and max years from the dataset
        current_year = 2025  # Using the current year from context
        min_year = max(int(yield_df['Year'].min()), 1990)
        max_year = min(current_year + 5, 2030)  # Allow prediction up to 5 years ahead
        
        # Get recommended ranges based on historical data
        recommended_ranges = {
            'rainfall': {
                'low': float(yield_df['average_rain_fall_mm_per_year'].quantile(0.25)),
                'medium': float(yield_df['average_rain_fall_mm_per_year'].quantile(0.5)),
                'high': float(yield_df['average_rain_fall_mm_per_year'].quantile(0.75))
            },
            'temperature': {
                'low': float(yield_df['avg_temp'].quantile(0.25)),
                'medium': float(yield_df['avg_temp'].quantile(0.5)),
                'high': float(yield_df['avg_temp'].quantile(0.75))
            },
            'pesticides': {
                'low': float(yield_df['pesticides_tonnes'].quantile(0.25)),
                'medium': float(yield_df['pesticides_tonnes'].quantile(0.5)),
                'high': float(yield_df['pesticides_tonnes'].quantile(0.75))
            }
        }
        
        # Calculate statistics per crop and area
        stats = {
            'avg_rainfall': float(yield_df['average_rain_fall_mm_per_year'].mean()),
            'max_rainfall': float(yield_df['average_rain_fall_mm_per_year'].max()),
            'min_rainfall': float(yield_df['average_rain_fall_mm_per_year'].min()),
            'avg_temp': float(yield_df['avg_temp'].mean()),
            'max_temp': float(yield_df['avg_temp'].max()),
            'min_temp': float(yield_df['avg_temp'].min()),
            'avg_pesticides': float(yield_df['pesticides_tonnes'].mean()),
            'max_pesticides': float(yield_df['pesticides_tonnes'].max()),
            'min_pesticides': float(yield_df['pesticides_tonnes'].min()),
            'yield_stats': {
                'avg_yield': float(yield_df['hg/ha_yield'].mean()),
                'max_yield': float(yield_df['hg/ha_yield'].max()),
                'min_yield': float(yield_df['hg/ha_yield'].min())
            }
        }

        # Get top performing combinations
        top_yields = yield_df.groupby(['Area', 'Item'])['hg/ha_yield'].mean().sort_values(ascending=False).head(5)
        top_combinations = [
            {
                'area': area,
                'crop': crop,
                'average_yield': float(yield_)
            }
            for (area, crop), yield_ in top_yields.items()
        ]

        return jsonify({
            'areas': areas,
            'crops': crops,
            'yearRange': {
                'min': min_year,
                'max': max_year
            },
            'stats': stats,
            'recommended_ranges': recommended_ranges,
            'top_combinations': top_combinations
        })
    except Exception as e:
        print("Error in get_available_options:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/get_options')
def get_options():
    try:
        df = pd.read_csv('Crop_Yield_Prediction-main/yield_df.csv')
        areas = sorted(df['Area'].dropna().unique().tolist())
        crops = sorted(df['Crop'].dropna().unique().tolist())
        return jsonify({'areas': areas, 'crops': crops})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)