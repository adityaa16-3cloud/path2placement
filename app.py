import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pickle
import pandas as pd
import numpy as np
import os
from chatbot import chatbot_response

app = Flask(__name__)


# --------------------------------------------------
# BASE DIR
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------
# LOAD MODELS
# --------------------------------------------------
performance_model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
placement_model = pickle.load(open(os.path.join(BASE_DIR, "models", "placement_model.pkl"), "rb"))

CSV_FILE = "student_predictions.csv"

def save_to_csv(row):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)


# --------------------------------------------------
# GLOBAL STATE (CHATBOT CONTEXT)
# --------------------------------------------------
last_prediction = None            # 0 or 1
last_placement_prediction = None  # 0 or 1

# --------------------------------------------------
# ROOT → WELCOME PAGE
# --------------------------------------------------
@app.route("/")
def root():
    return redirect(url_for("welcome"))

# --------------------------------------------------
# WELCOME PAGE
# --------------------------------------------------
@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

# --------------------------------------------------
# STUDENT PERFORMANCE PAGE
# --------------------------------------------------
@app.route("/performance")
def performance_page():
    return render_template("index.html")

# --------------------------------------------------
# PERFORMANCE PREDICTION
# --------------------------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    global last_prediction

    attendance = int(request.form["attendance"])
    study_hours = int(request.form["study_hours"])
    internal_marks = int(request.form["internal_marks"])
    assignment_score = int(request.form["assignment_score"])

    input_data = pd.DataFrame([{
        "attendance": attendance,
        "study_hours": study_hours,
        "internal_marks": internal_marks,
        "assignment_score": assignment_score
    }])

    prediction = performance_model.predict(input_data)[0]
    last_prediction = prediction

    result = "PASS" if prediction == 1 else "FAIL"

    # 🔥 SAVE PARTIAL DATA (placement will update later)
    save_to_csv({
        "timestamp": datetime.now(),
        "attendance": attendance,
        "study_hours": study_hours,
        "internal_marks": internal_marks,
        "assignment_score": assignment_score,
        "performance_result": result,
        "cgpa": "",
        "internships": "",
        "projects": "",
        "aptitude": "",
        "skills": "",
        "communication": "",
        "backlogs": "",
        "placement_result": "",
        "placement_probability": ""
    })

    return render_template("index.html", prediction_text=result)


# --------------------------------------------------
# PLACEMENT PAGE
# --------------------------------------------------
@app.route("/placement")
def placement_page():
    return render_template("placement.html")

# --------------------------------------------------
# PLACEMENT PREDICTION
# --------------------------------------------------
@app.route("/placement_predict", methods=["POST"])
def placement_predict():
    global last_placement_prediction

    cgpa = float(request.form["cgpa"])
    internships = int(request.form["internships"])
    projects = int(request.form["projects"])
    aptitude = int(request.form["aptitude"])
    skills = int(request.form["skills"])
    communication = int(request.form["communication"])
    backlogs = int(request.form["backlogs"])

    data = np.array([
        cgpa, internships, projects,
        aptitude, skills, communication, backlogs
    ]).reshape(1, -1)

    pred = placement_model.predict(data)[0]
    prob = placement_model.predict_proba(data)[0][1] * 100

    last_placement_prediction = pred

    result = "PLACED" if pred == 1 else "NOT PLACED"

    # 🔥 SAVE PLACEMENT DATA
    save_to_csv({
        "timestamp": datetime.now(),
        "attendance": "",
        "study_hours": "",
        "internal_marks": "",
        "assignment_score": "",
        "performance_result": "",
        "cgpa": cgpa,
        "internships": internships,
        "projects": projects,
        "aptitude": aptitude,
        "skills": skills,
        "communication": communication,
        "backlogs": backlogs,
        "placement_result": result,
        "placement_probability": round(prob, 2)
    })

    return render_template(
        "placement.html",
        placement_result=f"{result} ({prob:.2f}%)",
        cgpa=cgpa,
        internships=internships,
        projects=projects,
        aptitude=aptitude,
        skills=skills,
        communication=communication,
        backlogs=backlogs
    )

# --------------------------------------------------
# STUDENT DASHBOARD
# --------------------------------------------------
@app.route("/student_dashboard")
def student_dashboard():
    return render_template(
        "student_dashboard.html",

        # predictions (safe)
        performance_prediction=last_prediction,
        placement_prediction=last_placement_prediction,

        # academic inputs (safe defaults)
        attendance=0,
        study_hours=0,
        internal_marks=0,
        assignment_score=0,

        # placement inputs (safe defaults)
        cgpa=0,
        internships=0,
        projects=0,
        skills=0,
        communication=0
    )



# --------------------------------------------------
# 🔥 CHATBOT API (POPUP CHATBOT)
# --------------------------------------------------
@app.route("/chat_api", methods=["POST"])
def chat_api():
    global last_prediction, last_placement_prediction

    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"reply": "Please ask a question."})

    reply = chatbot_response(
        message,
        performance_prediction=last_prediction,
        placement_prediction=last_placement_prediction
    )

    # ✅ SAFETY NET
    if not reply or not isinstance(reply, str):
        reply = "Please make a prediction first so I can guide you better."

    # 🔥 CLEAN TEXT (important for speech synthesis)
    reply = reply.replace("\n", ". ").strip()

    return jsonify({"reply": reply})

# --------------------------------------------------
# (OPTIONAL) FULL CHATBOT PAGE
# --------------------------------------------------
@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

@app.route("/chat", methods=["POST"])
def chat():
    reply = chatbot_response(
        request.form.get("message", ""),
        performance_prediction=last_prediction,
        placement_prediction=last_placement_prediction
    )
    return render_template("chatbot.html", chat_response=reply)



@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/get-started")
def get_started():
    return render_template("get_started.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")




# --------------------------------------------------
# RUN APP
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
