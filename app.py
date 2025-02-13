import streamlit as st
import pandas as pd
import joblib

# Load the trained model and label encoders
model = joblib.load("price_predictor_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Streamlit app
st.title("Used Electronics Price Predictor")

# Input fields
st.header("Enter Product Details")

# Brand dropdown
brand_options = label_encoders['brand'].classes_.tolist()
brand = st.selectbox("Brand", brand_options)

# Model dropdown
model_options = label_encoders['model'].classes_.tolist()
model_name = st.selectbox("Model", model_options)

# Condition dropdown
condition_options = label_encoders['condition'].classes_.tolist()
condition = st.selectbox("Condition", condition_options)

# Age input
age = st.number_input("Age (in years)", min_value=0, max_value=10)

# Encode inputs using the saved label encoders
brand_encoded = label_encoders['brand'].transform([brand])[0]
model_encoded = label_encoders['model'].transform([model_name])[0]
condition_encoded = label_encoders['condition'].transform([condition])[0]

# Predict price
if st.button("Predict Price"):
    input_data = pd.DataFrame({
        'brand': [brand_encoded],
        'model': [model_encoded],
        'condition': [condition_encoded],
        'age': [age]
    })
    prediction = model.predict(input_data)
    st.success(f"Predicted Price: ${prediction[0]:.2f}")
