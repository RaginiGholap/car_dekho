import streamlit as st
import pandas as pd
import joblib

# ===============================
# Load trained artifacts
# ===============================
model = joblib.load("model.pkl")
owner_encoder = joblib.load("owner_encoder.pkl")
feature_columns = joblib.load("feature_columns.pkl")

st.title("🚗 Car Price Prediction")

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
car_age = st.number_input("Car Age (Years)", min_value=0)
mileage = st.number_input("Mileage (km/l)", min_value=0.0)
engine = st.number_input("Engine CC", min_value=0.0)
max_power = st.number_input("Max Power (bhp)", min_value=0.0)

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
    'mileage': mileage,
    'engine': engine,
    'max_power': max_power
}])

# ===============================
# Encode 'owner' (OrdinalEncoder)
# ===============================
input_df[['owner']] = owner_encoder.transform(input_df[['owner']])

# ===============================
# One-hot encoding (same as training)
# ===============================
input_df = pd.get_dummies(input_df)

# ===============================
# Add missing columns
# ===============================
for col in feature_columns:
    if col not in input_df.columns:
        input_df[col] = 0

# ===============================
# Ensure correct column order
# ===============================
input_df = input_df[feature_columns]

# ===============================
# Prediction
# ===============================
if st.button("Predict Price"):

    # Basic validation
    if engine < 500 or mileage <= 0:
        st.error("⚠️ Please enter realistic values")
    else:
        prediction = model.predict(input_df)[0]

        # Ensure positive output
        prediction = abs(prediction)

        st.success(f"💰 Estimated Price: ₹ {prediction:,.2f}")
