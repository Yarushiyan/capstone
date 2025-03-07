import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# Load your data (from SQL or CSV)
import mysql.connector

# Function to get the MySQL connection
def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Replace with your MySQL host
            user="root",       # Replace with your MySQL username
            password="123123Yn.,",  # Replace with your MySQL password
            database="electronics_db"  # Replace with your actual database name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to fetch data from the database
def fetch_data():
    try:
        conn = get_connection()
        if conn is None:
            return None

        # Updated SQL query with the correct column name 'device_condition'
        query = "SELECT brand, model, device_condition, age FROM used_electronics"
        data = pd.read_sql(query, conn)
        conn.close()
        return data
    except Exception as e:
        print("Error fetching data from database:", e)
        return None

# Load data
data = fetch_data()

# Initialize LabelEncoders
brand_encoder = LabelEncoder()
model_encoder = LabelEncoder()
condition_encoder = LabelEncoder()

# Fit the label encoders on the respective columns
brand_encoder.fit(data['brand'])
model_encoder.fit(data['model'])
condition_encoder.fit(data['device_condition'])

# Save the label encoders as pickle files
joblib.dump(brand_encoder, "brand_encoder.pkl")
joblib.dump(model_encoder, "model_encoder.pkl")
joblib.dump(condition_encoder, "condition_encoder.pkl")

print("Label encoders saved successfully!")
