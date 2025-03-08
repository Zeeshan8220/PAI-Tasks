import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load datasets
train_df = pd.read_csv(r"C:\Users\7300\OneDrive\Desktop\spaceship-titanic\train.csv")
test_df = pd.read_csv(r"C:\Users\7300\OneDrive\Desktop\spaceship-titanic\test.csv")


# Fill missing values
train_df.fillna(method='ffill', inplace=True)
test_df.fillna(method='ffill', inplace=True)

# Encode categorical features
categorical_cols = ["HomePlanet", "CryoSleep", "Cabin", "Destination", "VIP"]
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    combined_data = pd.concat([train_df[col], test_df[col]], axis=0, ignore_index=True).astype(str)
    le.fit(combined_data)
    train_df[col] = le.transform(train_df[col].astype(str))
    test_df[col] = le.transform(test_df[col].astype(str))
    label_encoders[col] = le

# Select features and target variable
features = ["HomePlanet", "CryoSleep", "Cabin", "Destination", "Age", "VIP", 
            "RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]
X = train_df[features]
y = train_df["Transported"].astype(int)

# Split data for validation
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Validate model
y_pred = model.predict(X_valid)
accuracy = accuracy_score(y_valid, y_pred)
print(f"Validation Accuracy: {accuracy:.4f}")

# Make predictions on test set
test_predictions = model.predict(test_df[features])

# Create submission file
submission = pd.DataFrame({
    "PassengerId": test_df["PassengerId"],
    "Transported": test_predictions.astype(bool)
})

# Save submission
submission.to_csv("submission.csv", index=False)
print(" Submission file 'submission.csv' created successfully in the current directory!")

