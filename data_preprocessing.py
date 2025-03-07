import pandas as pd
from sqlalchemy import create_engine
import joblib  # Import joblib to save the dictionaries

# Function to connect to MySQL using SQLAlchemy
def get_connection():
    # Create a connection string for SQLAlchemy
    connection_string = "mysql+pymysql://root:123123Yn.,@localhost:3306/electronics_db"
    engine = create_engine(connection_string)
    return engine

# Fetch data from MySQL
engine = get_connection()
query = "SELECT brand, model, device_condition, age, price FROM used_electronics"
data = pd.read_sql(query, engine)

# Preprocessing
data = data.dropna()  # Remove missing values
data = data.drop_duplicates()  # Remove duplicates

# Encode categorical variables
brand_dict = {brand: idx for idx, brand in enumerate(data['brand'].unique())}
model_dict = {model: idx for idx, model in enumerate(data['model'].unique())}
condition_dict = {condition: idx for idx, condition in enumerate(data['device_condition'].unique())}

# Save encodings for app usage
joblib.dump(brand_dict, "brand_dict.pkl")  # Save brand_dict
joblib.dump(model_dict, "model_dict.pkl")  # Save model_dict
joblib.dump(condition_dict, "condition_dict.pkl")  # Save condition_dict

# Convert categorical values into numeric values
data['brand'] = data['brand'].map(brand_dict)
data['model'] = data['model'].map(model_dict)
data['device_condition'] = data['device_condition'].map(condition_dict)

# Split data into features and target
X = data[['brand', 'model', 'device_condition', 'age']]
y = data['price']

# Train-test split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Save processed data
X_train.to_csv("X_train.csv", index=False)
X_test.to_csv("X_test.csv", index=False)
y_train.to_csv("y_train.csv", index=False)
y_test.to_csv("y_test.csv", index=False)

print("✅ Data preprocessing complete! Data loaded from MySQL and processed.")
