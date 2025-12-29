import pickle

# STEP 1: Load the saved model
model = pickle.load(open("model.pkl", "rb"))

# STEP 2: Give sample student data
# Format: [attendance, study_hours, internal_marks, assignment_score]
sample_student = [[80, 3, 65, 70]]

# STEP 3: Predict result
prediction = model.predict(sample_student)

# STEP 4: Print result
if prediction[0] == 1:
    print("Prediction Result: PASS ✅")
else:
    print("Prediction Result: FAIL ❌")
