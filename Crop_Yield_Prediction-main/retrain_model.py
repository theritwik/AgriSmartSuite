import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeRegressor
from joblib import dump
import sklearn
print(f"Using scikit-learn version: {sklearn.__version__}")

# Load and prepare data
df = pd.read_csv("yield_df.csv")
df.drop('Unnamed: 0', axis=1, inplace=True)
df.drop_duplicates(inplace=True)

# Select relevant columns
col = ['Year','average_rain_fall_mm_per_year','pesticides_tonnes', 'avg_temp','Area', 'Item', 'hg/ha_yield']
df = df[col]

# Split features and target
X = df.drop('hg/ha_yield', axis=1)
y = df['hg/ha_yield']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, shuffle=True)

# Create and fit preprocessor
ohe = OneHotEncoder(drop='first')
scale = StandardScaler()

preprocessor = ColumnTransformer(
    transformers=[
        ('StandardScale', scale, [0,1,2,3]),
        ('OneHotEncode', ohe, [4,5])
    ],
    remainder='passthrough'
)

# Transform the data
X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

# Train model
dtr = DecisionTreeRegressor()
dtr.fit(X_train_transformed, y_train)

# Save models using joblib
print("Saving models...")
dump(dtr, 'dtr.joblib')
dump(preprocessor, 'preprocessor.joblib')
print("Models saved successfully!")

# Test prediction
def test_prediction(Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item):
    features = np.array([[Year, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, Area, Item]], dtype=object)
    transform_features = preprocessor.transform(features)
    predicted_yield = dtr.predict(transform_features).reshape(-1,1)
    return predicted_yield[0][0]

# Test the model with a sample prediction
test_result = test_prediction(1990, 1485.0, 121.0, 16.37, 'Albania', 'Maize')
print(f"\nTest prediction result: {test_result}")
