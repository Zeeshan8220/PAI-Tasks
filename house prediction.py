import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

# Load the dataset
df = pd.read_csv("data.csv")

# Drop unnecessary columns that won't contribute to predictions
df.drop(columns=["date", "street", "country"], inplace=True)

# Feature Engineering: Create new features
df["house_age"] = 2024 - df["yr_built"]
df.drop(columns=["yr_built"], inplace=True)

# Handle categorical variables
categorical_features = ["city", "statezip"]
one_hot_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
categorical_encoded = one_hot_encoder.fit_transform(df[categorical_features])
categorical_df = pd.DataFrame(categorical_encoded, columns=one_hot_encoder.get_feature_names_out(categorical_features))

# Merge encoded categorical data and drop original categorical columns
df = df.drop(columns=categorical_features)
df = pd.concat([df, categorical_df], axis=1)

# Define features and target variable
X = df.drop(columns=["price"])
y = np.log1p(df["price"])  # Apply log transformation to stabilize variance

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize numerical features for better performance
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Initialize and train the XGBoost model
model = XGBRegressor(n_estimators=200, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)
y_pred = np.expm1(y_pred)  # Reverse log transformation

# Evaluate model performance
mae = mean_absolute_error(np.expm1(y_test), y_pred)
mse = mean_squared_error(np.expm1(y_test), y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(np.expm1(y_test), y_pred)

# Print evaluation metrics
print("Model Performance:")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared Score (R²): {r2:.2f}")
