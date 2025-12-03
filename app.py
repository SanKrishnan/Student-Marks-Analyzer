from flask import Flask, request, jsonify, render_template, session
import firebase_admin
from firebase_admin import credentials, auth, firestore
from flask import redirect


app = Flask(__name__,template_folder='.',static_folder='.',static_url_path='')

app.secret_key = "sanjana-secret"

# Firebase Admin
import os
import firebase_admin
from firebase_admin import credentials

if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.environ["FIREBASE_PROJECT_ID"],
        "private_key": os.environ["FIREBASE_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": os.environ["FIREBASE_CLIENT_EMAIL"],
        "token_uri": "https://oauth2.googleapis.com/token"
    })
    firebase_admin.initialize_app(cred)


# ---------------------------------------------------
# SESSION LOGIN (after Firebase client login)
# ---------------------------------------------------
@app.route("/api/session-login", methods=["POST"])
def session_login():
    id_token = request.json.get("idToken")

    try:
        decoded = auth.verify_id_token(id_token)
        session["email"] = decoded["email"]
        return jsonify({"message": "Session created"}), 200
    except:
        return jsonify({"error": "Invalid token"}), 401


# ---------------------------------------------------
# SAVE MARKS IN FIRESTORE
# ---------------------------------------------------
from datetime import datetime

@app.route("/api/save-marks", methods=["POST"])
def save_marks():
    if "email" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.json
    user_email = session["email"]

    # ✅ Add timestamp
    data["createdAt"] = datetime.utcnow()

    # ✅ Save to Firestore
    db.collection("users") \
      .document(user_email) \
      .collection("marks") \
      .add(data)

    return jsonify({"message": "Saved in Firestore"}), 200



# ---------------------------------------------------
# ANALYZE
# ---------------------------------------------------
print("🔥 Flask started, routes loading. ✅")
@app.route("/api/session-login", methods=["POST"])

@app.route("/analyze", methods=["POST"])
def analyze():
    print("✅ /analyze route HIT")
    try:
        name = request.form.get("student_name")
        c1 = request.form.get("Course1")
        c2 = request.form.get("Course2")
        c3 = request.form.get("Course3")

        if not (name and c1 and c2 and c3):
            return jsonify({"error": "All fields are required"}), 400

        c1, c2, c3 = int(c1), int(c2), int(c3)

        total = c1 + c2 + c3
        avg = round(total / 3, 2)
        result = "Pass" if min(c1, c2, c3) >= 40 else "Fail"

        return jsonify({
            "student": name,
            "course1": c1,
            "course2": c2,
            "course3": c3,
            "total": total,
            "average": avg,
            "result": result
        }), 200

    except Exception as e:
        print("❌ Analyze error:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/api/profile")
def profile():
    if "email" not in session:
        return jsonify({"error": "Login required"}), 401

    email = session["email"]
    marks_ref = db.collection("users").document(email).collection("marks")

    docs = marks_ref.order_by("createdAt").stream()
    records = [doc.to_dict() for doc in docs]

    return jsonify({
        "email": email,
        "totalAnalyses": len(records),
        "records": records
    })


@app.route("/")
def index():
    if "email" not in session:
        return redirect("/login")
    return render_template("index.html")


@app.route("/login")
def login_page():
    return render_template("Login_signup.html")




