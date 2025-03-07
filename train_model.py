import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder

# Function to get the MySQL connection using SQLAlchemy
def get_connection():
    connection_string = "mysql+pymysql://root:123123Yn.,@localhost:3306/electronics_db"
    engine = create_engine(connection_string)
    return engine

# Function to fetch data from the database
def fetch_data():
    try:
        engine = get_connection()
        query = "SELECT brand, model, device_condition, age, price FROM used_electronics"
        data = pd.read_sql(query, engine)
        return data
    except Exception as e:
        print("Error fetching data from database:", e)
        return None

# Function to preprocess the data
def preprocess_data(data):
    # Initialize LabelEncoders
    brand_encoder = LabelEncoder()
    model_encoder = LabelEncoder()
    condition_encoder = LabelEncoder()

    # Fit and transform the categorical columns
    data['brand'] = brand_encoder.fit_transform(data['brand'])
    data['model'] = model_encoder.fit_transform(data['model'])
    data['device_condition'] = condition_encoder.fit_transform(data['device_condition'])

    # Save the label encoders
    joblib.dump(brand_encoder, "brand_encoder.pkl")
    joblib.dump(model_encoder, "model_encoder.pkl")
    joblib.dump(condition_encoder, "condition_encoder.pkl")

    # Split the data into features (X) and target variable (y)
    X = data.drop(columns=["price"])
    y = data["price"]

    return X, y

# Function to train the model
def train_model():
    # Fetch and preprocess data
    data = fetch_data()
    if data is None:
        print("No data available to train the model.")
        return

    X_train, y_train = preprocess_data(data)

    # Train a Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, "price_predictor_model.pkl")
    print("Model trained and saved as price_predictor_model.pkl")

# Run the training process
if __name__ == "__main__":
    train_model()