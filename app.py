from flask import Flask, request, jsonify, render_template, session, redirect
import firebase_admin
from firebase_admin import credentials, auth, firestore
import os
from datetime import datetime

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

app.secret_key = "sanjana-secret"
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

# ----------------------------------
# Firebase Admin Initialization
# ----------------------------------
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.environ["FIREBASE_PROJECT_ID"],
        "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
        "token_uri": "https://oauth2.googleapis.com/token"
    })
    firebase_admin.initialize_app(cred)

db = firestore.client()   # ✅ NOW CORRECT PLACE

print("✅ Firebase and Firestore initialized")

# ----------------------------------
# Session Login
# ----------------------------------
@app.route("/api/session-login", methods=["POST"])
def session_login():
    id_token = request.json.get("idToken")

    try:
        decoded = auth.verify_id_token(id_token)
        session["email"] = decoded["email"]
        return jsonify({"message": "Session created"}), 200
    except:
        return jsonify({"error": "Invalid token"}), 401

# ----------------------------------
# Save Marks
# ----------------------------------
@app.route("/api/save-marks", methods=["POST"])
def save_marks():
    if "email" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.json
    data["createdAt"] = datetime.utcnow()

    db.collection("users") \
        .document(session["email"]) \
        .collection("marks") \
        .add(data)

    return jsonify({"message": "Saved in Firestore"}), 200

# ----------------------------------
# Analyze
# ----------------------------------
# ----------------------------------
# Analyze + GPA
# ----------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        data = request.get_json()

        semester = int(data.get("semester"))
        pass_mark = int(data.get("pass_mark"))

        subjects = data.get("subjects")

        if not subjects or len(subjects) == 0:
            return jsonify({
                "error": "At least one subject is required"
            }), 400

        total_marks = 0
        total_credit_points = 0
        total_credits = 0

        subject_results = []

        for subject in subjects:

            name = subject.get("name")
            marks = int(subject.get("marks"))
            credits = int(subject.get("credits"))

            total_marks += marks

            # ---------------------------
            # Grade Logic
            # ---------------------------
            if marks >= 90:
                grade_point = 10
                grade = "S"

            elif marks >= 80:
                grade_point = 9
                grade = "A"

            elif marks >= 70:
                grade_point = 8
                grade = "B"

            elif marks >= 60:
                grade_point = 7
                grade = "C"

            elif marks >= 50:
                grade_point = 6
                grade = "D"

            elif marks >= 40:
                grade_point = 5
                grade = "E"

            else:
                grade_point = 0
                grade = "F"

            total_credit_points += grade_point * credits
            total_credits += credits

            subject_results.append({
                "subject": name,
                "marks": marks,
                "credits": credits,
                "grade": grade,
                "grade_point": grade_point,
                "result": "Pass" if marks >= pass_mark else "Fail"
            })

        total_subjects = len(subjects)

        percentage = round(
            (total_marks / (total_subjects * 100)) * 100,
            2
        )

        gpa = round(
            total_credit_points / total_credits,
            2
        )

        final_result = (
            "Pass"
            if all(
                subject["marks"] >= pass_mark
                for subject in subject_results
            )
            else "Fail"
        )

        response_data = {
            "semester": semester,
            "pass_mark": pass_mark,
            "subjects": subject_results,
            "total_subjects": total_subjects,
            "total_marks": total_marks,
            "percentage": percentage,
            "gpa": gpa,
            "result": final_result
        }

        return jsonify(response_data), 200

    except Exception as e:
        print("Analyze Error:", e)
        return jsonify({
            "error": "Internal Server Error"
        }), 500
# ----------------------------------
# Profile
# ----------------------------------
@app.route("/api/profile")
def profile():
    if "email" not in session:
        return jsonify({"error": "Login required"}), 401

    docs = db.collection("users") \
        .document(session["email"]) \
        .collection("marks") \
        .order_by("createdAt") \
        .stream()

    records = [doc.to_dict() for doc in docs]

    return jsonify({
        "email": session["email"],
        "totalAnalyses": len(records),
        "records": records
    })

# ----------------------------------
# Pages
# ----------------------------------
@app.route("/")
def index():
    if "email" not in session:
        return redirect("/login")
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("Login_signup.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")





