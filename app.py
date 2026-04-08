# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import OrdinalEncoder

# ===============================
# Load trained artifacts
# ===============================
model = joblib.load("model.pkl")
owner_encoder = joblib.load("owner_encoder.pkl")
feature_columns = joblib.load("feature_columns.pkl")

st.title("Car Price Prediction 💰")

# ===============================
# User Inputs with unique keys
# ===============================
owner = st.selectbox(
    "Owner Type",
    ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car'],
    key="owner_type"
)

fuel = st.selectbox(
    "Fuel Type",
    ['Petrol', 'Diesel', 'CNG'],
    key="fuel_type"
)

seller_type = st.selectbox(
    "Seller Type",
    ['Individual', 'Dealer'],
    key="seller_type"
)

transmission = st.selectbox(
    "Transmission",
    ['Manual', 'Automatic'],
    key="transmission_type"
)

km_driven = st.number_input("KM Driven", min_value=0, max_value=300000, key="km_driven_input")
seats = st.number_input("Seats", min_value=2, max_value=10, key="seats_input")
car_age = st.number_input("Car Age (Years)", min_value=0, max_value=30, key="car_age_input")
mileage_value = st.number_input("Mileage", min_value=0.0, key="mileage_input")
engine_value = st.number_input("Engine CC", min_value=0.0, key="engine_input")
max_power_value = st.number_input("Max Power", min_value=0.0, key="max_power_input")

# ===============================
# Create input DataFrame
# ===============================
input_df = pd.DataFrame([{
    'owner': owner,
    'fuel': fuel,
    'seller_type': seller_type,
    'transmission': transmission,
    'km_driven': km_driven,
    'seats': seats,
    'car_age': car_age,
    'mileage': mileage_value,
    'engine': engine_value,
    'max_power': max_power_value
}])

# ===============================
# Encode categorical features safely
# ===============================
input_df['owner'] = owner_encoder.transform(input_df[['owner']])

# One-hot encode remaining categorical features
input_df = pd.get_dummies(input_df)

# Add missing columns (set 0) and keep correct order
for col in feature_columns:
    if col not in input_df.columns:
        input_df[col] = 0
input_df = input_df[feature_columns]

# ===============================
# Prediction
# ===============================
if st.button("Predict Price", key="predict_button"):
    try:
        prediction = model.predict(input_df)
        # Convert log(price) back if model was trained on log
        prediction = np.exp(prediction)
    except:
        prediction = model.predict(input_df)

    # Ensure prediction is always positive
    min_price = 1000  # minimum realistic price in ₹
    prediction = np.maximum(prediction, min_price)

    st.success(f"💰 Estimated Price: ₹ {prediction[0]:,.2f}")
