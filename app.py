import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("price_predictor_model.pkl")

# Streamlit app
st.title("Used Electronics Price Predictor")

# Input fields
st.header("Enter Product Details")
brand = st.selectbox("Brand", ["Apple", "Samsung", "Google", "Sony", "Other"])
model_name = st.text_input("Model")
condition = st.selectbox("Condition", ["New", "Like New", "Good", "Fair", "Poor"])
age = st.number_input("Age (in years)", min_value=0, max_value=10)

# Encode inputs
brand_encoded = 0 if brand == "Apple" else 1 if brand == "Samsung" else 2 if brand == "Google" else 3 if brand == "Sony" else 4
condition_encoded = 0 if condition == "New" else 1 if condition == "Like New" else 2 if condition == "Good" else 3 if condition == "Fair" else 4

# Predict price
if st.button("Predict Price"):
    input_data = pd.DataFrame({
        'brand': [brand_encoded],
        'model': [model_name],
        'condition': [condition_encoded],
        'age': [age]
    })
    prediction = model.predict(input_data)
    st.success(f"Predicted Price: ${prediction[0]:.2f}")