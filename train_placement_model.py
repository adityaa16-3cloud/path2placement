import os

os.makedirs("models", exist_ok=True)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
import pickle

# Load dataset
data = pd.read_csv("dataset/placement_data.csv")

# Encode target
le = LabelEncoder()
data["placed"] = le.fit_transform(data["placed"])  # Yes=1, No=0

X = data.drop("placed", axis=1)
y = data["placed"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save model
with open("models/placement_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Placement model trained & saved successfully")
