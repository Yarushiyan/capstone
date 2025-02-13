import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load preprocessed data
X_train = pd.read_csv("X_train.csv")
y_train = pd.read_csv("y_train.csv")

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train.values.ravel())

# Save the trained model
joblib.dump(model, "price_predictor_model.pkl")
print("Model trained and saved as price_predictor_model.pkl")