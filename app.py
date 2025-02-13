import streamlit as st
import pandas as pd
import joblib
from fuzzywuzzy import process  # for fuzzy matching

# Load the trained model and label encoders
model = joblib.load("price_predictor_model.pkl")
label_encoders = joblib.load("label_encoders.pkl")

# Extract valid brands and models
valid_brands = label_encoders['brand'].classes_.tolist()
valid_models = label_encoders['model'].classes_.tolist()
valid_conditions = label_encoders['condition'].classes_.tolist()

# Streamlit app
st.title("📱 Used Electronics Price Predictor")
st.markdown("### Get an estimated resale price for your used electronic device.")

# Sidebar for brand and model reference
st.sidebar.header("Valid Brands & Models")
st.sidebar.write("#### Brands:")
st.sidebar.write(valid_brands)
st.sidebar.write("#### Models:")
st.sidebar.write(valid_models)

# Input fields
st.subheader("Enter Product Details")
brand = st.text_input("Enter Brand").strip().lower()  # Normalize to lowercase
model_name = st.text_input("Enter Model").strip().lower()  # Normalize to lowercase
condition = st.selectbox("Select Condition", valid_conditions)
age = st.slider("Select Age (in years)", 0, 10, 1)

# Function to suggest the closest match using fuzzy matching
def suggest_closest_match(user_input, valid_list):
    matches = process.extract(user_input, valid_list, limit=5)
    return [match[0] for match in matches]

# Initialize encoding variables
brand_encoded = None
model_encoded = None
valid_brand = True
valid_model = True

# Button to predict price
if st.button("🔍 Predict Price"):
    # Try encoding the brand and model, show suggestions if not valid
    if brand:
        # Check for exact match after converting to lowercase
        brand_matches = [b for b in valid_brands if b.lower() == brand]
        if brand_matches:
            brand_encoded = label_encoders['brand'].transform([brand_matches[0]])[0]
        else:
            valid_brand = False
            st.error(f"Brand '{brand}' not found. Did you mean one of these?")
            suggested_brands = suggest_closest_match(brand, valid_brands)
            st.write(suggested_brands)

    if model_name:
        # Check for exact match after converting to lowercase
        model_matches = [m for m in valid_models if m.lower() == model_name]
        if model_matches:
            model_encoded = label_encoders['model'].transform([model_matches[0]])[0]
        else:
            valid_model = False
            st.error(f"Model '{model_name}' not found. Did you mean one of these?")
            suggested_models = suggest_closest_match(model_name, valid_models)
            st.write(suggested_models)

    # Proceed only if both brand and model are valid or after corrections
    if valid_brand and valid_model:
        # Encode condition
        condition_encoded = label_encoders['condition'].transform([condition])[0]

        # Make the price prediction
        input_data = pd.DataFrame({
            'brand': [brand_encoded],
            'model': [model_encoded],
            'condition': [condition_encoded],
            'age': [age]
        })
        prediction = model.predict(input_data)
        st.success(f"💰 Estimated Price: **${prediction[0]:.2f}**")
    else:
        st.warning("Please enter a valid brand and model before predicting the price.")
