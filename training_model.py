import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

# STEP 1: Load dataset
data = pd.read_csv("dataset/student_data.csv")

# STEP 2: Convert Pass/Fail into numbers
le = LabelEncoder()
data['result'] = le.fit_transform(data['result'])

# STEP 3: Separate input and output
X = data.drop(['name', 'result'], axis=1)
y = data['result']

# STEP 4: Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# STEP 5: Train the ML model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# STEP 6: Save the trained model
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained successfully and saved!")
