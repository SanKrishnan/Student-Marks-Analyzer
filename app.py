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
@app.route("/analyze", methods=["POST"])
@app.route("/analyze", methods=["POST"])
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json() if request.is_json else request.form

        semester = int(data.get("semester"))
        pass_mark = int(data.get("pass_mark"))

        # Courses expected as list
        courses = data.get("courses")

        # If coming from form-data (string), convert to list
        if isinstance(courses, str):
            courses = courses.split(",")
            courses = [int(c.strip()) for c in courses]

        if not courses or len(courses) == 0:
            return jsonify({"error": "At least one course is required"}), 400

        marks = list(map(int, courses))
        total_courses = len(marks)
        total = sum(marks)
        average = round(total / total_courses, 2)

        # Check pass/fail
        course_results = [
            "Pass" if m >= pass_mark else "Fail"
        for m in marks
        ]
        result = "Pass" if all(m >= pass_mark for m in marks) else "Fail"


        return jsonify({
            "semester": semester,
            "total_courses": total_courses,
            "pass_mark": pass_mark,
            "marks": marks,
            "course_results": course_results,
            "total": total,
            "average": average,
            "result": result
        }), 200

    except ValueError:
        return jsonify({"error": "Invalid number format"}), 400
    except Exception as e:
        print("Analyze error:", e)
        return jsonify({"error": "Internal server error"}), 500

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





