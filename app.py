import streamlit as st
import pandas as pd
import joblib
from fuzzywuzzy import process
from chatgpt_integration import get_chatgpt_response
import mysql.connector  # For database fetching
import requests  # For API fetching

# Function to fetch brand-model combinations from the database
def fetch_brand_model_combinations_from_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123123Yn.,",
            database="electronics_db"
        )
        cursor = conn.cursor()
        query = "SELECT DISTINCT brand, model FROM used_electronics"
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        # Create a dictionary to store brand-model combinations
        brand_model_combinations = {}
        for brand, model in results:
            if brand.lower() not in brand_model_combinations:
                brand_model_combinations[brand.lower()] = []
            brand_model_combinations[brand.lower()].append(model.lower())
        
        return brand_model_combinations
    except Exception as e:
        print("Error fetching brand-model combinations from database:", e)
        return {}

# Function to fetch brand-model combinations from an API
def fetch_brand_model_combinations_from_api():
    try:
        response = requests.get("https://api.example.com/brand-models")
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Convert JSON response to a dictionary
    except Exception as e:
        print("Error fetching brand-model combinations from API:", e)
        return {}

# Fetch and store brand-model combinations (choose one method)
valid_brand_model_combinations = fetch_brand_model_combinations_from_db()  # From database
# valid_brand_model_combinations = fetch_brand_model_combinations_from_api()  # From API

# Load the trained model and label encoders
model = joblib.load("price_predictor_model.pkl")
brand_encoder = joblib.load("brand_encoder.pkl")
model_encoder = joblib.load("model_encoder.pkl")
condition_encoder = joblib.load("condition_encoder.pkl")

# Extract valid brands, models, and conditions from label encoders
valid_brands = brand_encoder.classes_.tolist()
valid_models = model_encoder.classes_.tolist()
valid_conditions = condition_encoder.classes_.tolist()

# Streamlit app
st.title("📱 Used Electronics Price Predictor & ChatGPT Integration")
st.markdown("### Get an estimated resale price for your used electronic device.")

# Input fields for price prediction
st.subheader("Enter Product Details")
brand = st.text_input("Enter Brand").strip().lower()
model_name = st.text_input("Enter Model").strip().lower()
condition = st.selectbox("Select Condition", valid_conditions)
age = st.slider("Select Age (in years)", 0, 10, 1)

# Function to suggest closest matches using fuzzy matching
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
    # Validate brand and model combination
    if brand in valid_brand_model_combinations:
        if model_name not in valid_brand_model_combinations[brand]:
            st.error(f"Invalid model '{model_name}' for brand '{brand}'. Please enter a valid combination.")
            st.write(f"Valid models for {brand}: {valid_brand_model_combinations[brand]}")
            valid_model = False
    else:
        st.error(f"Invalid brand '{brand}'. Please enter a valid brand.")
        st.write(f"Valid brands: {list(valid_brand_model_combinations.keys())}")
        valid_brand = False

    # Proceed only if both brand and model are valid
    if valid_brand and valid_model:
        # Handle brand input
        if brand:
            # Exact match check (case-insensitive)
            brand_matches = [b for b in valid_brands if b.lower() == brand]
            if brand_matches:
                brand_encoded = brand_encoder.transform([brand_matches[0]])[0]
            else:
                valid_brand = False
                st.error(f"Brand '{brand}' not found. Did you mean one of these?")
                suggested_brands = suggest_closest_match(brand, valid_brands)
                st.write(suggested_brands)

        # Handle model input
        if model_name:
            # Exact match check (case-insensitive)
            model_matches = [m for m in valid_models if m.lower() == model_name]
            if model_matches:
                model_encoded = model_encoder.transform([model_matches[0]])[0]
            else:
                valid_model = False
                st.error(f"Model '{model_name}' not found. Did you mean one of these?")
                suggested_models = suggest_closest_match(model_name, valid_models)
                st.write(suggested_models)

        # Proceed only if both brand and model are valid or corrected
        if valid_brand and valid_model:
            # Encode condition correctly to match the trained model
            condition_encoded = condition_encoder.transform([condition])[0]

            # Create input data for price prediction
            input_data = pd.DataFrame({
                'brand': [brand_encoded],
                'model': [model_encoded],
                'device_condition': [condition_encoded],
                'age': [age]
            })
            
            # Make the price prediction
            try:
                prediction = model.predict(input_data)
                st.success(f"💰 Estimated Price: **${prediction[0]:.2f}**")

                # Use ChatGPT to analyze or explain the predicted result
                chatgpt_prompt = f"Given the product details: Brand = {brand}, Model = {model_name}, Condition = {condition}, Age = {age} years, the predicted resale price is ${prediction[0]:.2f}. Can you explain the factors that could influence this price or give additional recommendations?"
                
                # Get response from ChatGPT
                response = get_chatgpt_response(chatgpt_prompt)
                st.write("ChatGPT's Analysis/Recommendations:")
                st.write(response)
            
            except Exception as e:
                st.error(f"Error making prediction: {e}")
        else:
            st.warning("Please enter a valid brand and model before predicting the price.")