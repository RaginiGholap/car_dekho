# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import joblib
import numpy as np

# ===============================
# Load trained artifacts
# ===============================
model = joblib.load("model.pkl")
owner_encoder = joblib.load("owner_encoder.pkl")
fuel_encoder = joblib.load("fuel_encoder.pkl")
seller_encoder = joblib.load("seller_encoder.pkl")
transmission_encoder = joblib.load("transmission_encoder.pkl")
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
# Encode categorical features using saved encoders
# ===============================
input_df['owner'] = owner_encoder.transform(input_df[['owner']])
input_df['fuel'] = fuel_encoder.transform(input_df[['fuel']])
input_df['seller_type'] = seller_encoder.transform(input_df[['seller_type']])
input_df['transmission'] = transmission_encoder.transform(input_df[['transmission']])

# ===============================
# One-hot encode all categorical features
# ===============================
input_df = pd.get_dummies(input_df)

# ===============================
# Ensure all model features exist
# ===============================
for col in feature_columns:
    if col not in input_df.columns:
        input_df[col] = 0

# Keep the column order same as training
input_df = input_df[feature_columns]

# Debugging: show input dataframe before prediction
st.write("Input features going to model:")
st.write(input_df)

# ===============================
# Prediction
# ===============================
if st.button("Predict Price", key="predict_button"):
    try:
        prediction = model.predict(input_df)
        # If model trained on log(price), convert back
        prediction = np.exp(prediction)
    except:
        prediction = model.predict(input_df)

    # Ensure positive and reasonable price
    min_price = 10000  # ₹10,000 minimum
    prediction = np.maximum(prediction, min_price)

    st.success(f"💰 Estimated Price: ₹ {prediction[0]:,.2f}")
