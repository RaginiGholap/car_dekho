import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ===============================
# Load trained artifacts
# ===============================
model = joblib.load("model.pkl")
owner_encoder = joblib.load("owner_encoder.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# Optional: load scalers if you used them during training
# mileage_scaler = joblib.load("mileage_scaler.pkl")
# engine_scaler = joblib.load("engine_scaler.pkl")
# max_power_scaler = joblib.load("max_power_scaler.pkl")
# km_driven_scaler = joblib.load("km_driven_scaler.pkl")

st.title("Car Price Prediction")

# ===============================
# User Inputs
# ===============================
owner = st.selectbox(
    "Owner Type",
    [
        'First Owner',
        'Second Owner',
        'Third Owner',
        'Fourth & Above Owner',
        'Test Drive Car'
    ]
)

fuel = st.selectbox("Fuel Type", ['Petrol', 'Diesel', 'CNG'])
seller_type = st.selectbox("Seller Type", ['Individual', 'Dealer'])
transmission = st.selectbox("Transmission", ['Manual', 'Automatic'])

km_driven = st.number_input("KM Driven", min_value=0)
seats = st.number_input("Seats", min_value=2, max_value=10)
year_old = st.number_input("Car Age (Years)", min_value=0)
mileage_value = st.number_input("Mileage (km/l)")
engine_value = st.number_input("Engine CC")
max_power_value = st.number_input("Max Power (bhp)")

# ===============================
# Create input DataFrame with all features
# ===============================
input_df = pd.DataFrame([{
    'owner': owner,
    'fuel': fuel,
    'seller_type': seller_type,
    'transmission': transmission,
    'km_driven': km_driven,
    'seats': seats,
    'year_old': year_old,
    'mileage': mileage_value,
    'engine': engine_value,
    'max_power': max_power_value
}])

# ===============================
# Encode categorical features
# ===============================
input_df['owner'] = owner_encoder.transform(input_df[['owner']])
input_df = pd.get_dummies(input_df)

# ===============================
# Add missing columns
# ===============================
for col in feature_columns:
    if col not in input_df.columns:
        input_df[col] = 0

# ===============================
# Keep correct column order
# ===============================
input_df = input_df[feature_columns]

# ===============================
# Scale numeric features if needed (uncomment if scalers are saved)
# ===============================
# input_df['km_driven'] = km_driven_scaler.transform(input_df[['km_driven']])
# input_df['mileage'] = mileage_scaler.transform(input_df[['mileage']])
# input_df['engine'] = engine_scaler.transform(input_df[['engine']])
# input_df['max_power'] = max_power_scaler.transform(input_df[['max_power']])

# ===============================
# Prediction
# ===============================
if st.button("Predict Price"):
    try:
        prediction_log = model.predict(input_df)  # If model trained on log(price)
        prediction = np.expm1(prediction_log)     # Convert back from log
        st.success(f"💰 Estimated Price: ₹ {prediction[0]:,.2f}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
