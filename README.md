# 🎓 Student Marks Analyzer

A full-stack academic analytics web application built using Flask and Firebase that allows authenticated users to analyze student performance, calculate percentage and GPA, determine pass/fail status, and securely store analysis history in Firestore.

The application is deployed on Vercel as a serverless Flask application.

---

# 🚀 Live Deployment

✅ Deployed using Vercel Serverless Functions  
✅ Backend: Flask  
✅ Frontend: HTML, Tailwind CSS, JavaScript  
✅ Authentication: Firebase Authentication  
✅ Database: Firebase Firestore  

---

# 📌 Features

## 🔐 User Authentication

- Secure Sign Up & Login using Firebase Authentication
- Session-based authentication using Flask sessions
- Protected routes for authenticated users only
- Logout functionality with secure session clearing

---

## 📊 Student Performance Analysis

Users can:

- Enter semester details
- Add dynamic subject inputs
- Input subject marks and credits
- Analyze academic performance in real-time

The application calculates:

- Total Marks
- Percentage
- GPA (Grade Point Average)
- Subject-wise Grades
- Pass/Fail Status

---

## 🎯 GPA Calculation

The GPA is calculated using a weighted credit-based formula:

```text
GPA = Σ(Grade Point × Credits) / Σ(Credits)
```

### Grade Mapping

| Marks Range | Grade | Grade Point |
|-------------|-------|-------------|
| 90 - 100 | S | 10 |
| 80 - 89 | A | 9 |
| 70 - 79 | B | 8 |
| 60 - 69 | C | 7 |
| 50 - 59 | D | 6 |
| 40 - 49 | E | 5 |
| Below 40 | F | 0 |

---

# ☁️ Firestore Integration

- Stores every academic analysis securely in Firebase Firestore
- Data is organized user-wise
- Each record includes:
  - Semester
  - Percentage
  - GPA
  - Subject details
  - Final Result
  - Timestamp

---

# 👤 User Dashboard

The profile dashboard displays:

- Logged-in user email
- Total analyses performed
- Previous academic records
- Percentage history
- GPA history
- Pass/Fail outcomes

---

# 🎨 User Interface

- Responsive and modern UI using Tailwind CSS
- Dynamic subject input generation
- Modal-based profile dashboard
- Interactive dropdown menu for account actions
- Clean academic analytics layout

---

# 🛠️ Tech Stack

## Backend

- Python
- Flask
- Firebase Admin SDK
- Gunicorn

## Frontend

- HTML5
- Tailwind CSS
- JavaScript (ES6)

## Database & Authentication

- Firebase Authentication
- Firebase Firestore

## Deployment

- Vercel Serverless Functions

---

# 🗂️ Project Structure

```bash
├── app.py / flas.py          # Flask backend and API routes
├── index.html                # Main academic analyzer dashboard
├── Login_signup.html         # Authentication page
├── Login_signup.css          # Authentication styling
├── Loginsign.js              # Firebase authentication logic
├── requirements.txt          # Python dependencies
├── vercel.json               # Vercel deployment configuration
└── README.md
```

---

## 🔑 Environment Variables (Vercel)

The following environment variables **must be added in Vercel → Project Settings → Environment Variables**:

```env
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_PRIVATE_KEY=your_private_key
FIREBASE_CLIENT_EMAIL=your_client_email
```

⚠️ Make sure to store `FIREBASE_PRIVATE_KEY` with escaped newlines (`\n`) as required by Firebase Admin SDK.

---

## 🛠️ Tech Stack

### Backend

* Flask 
* Firebase Admin SDK
* Gunicorn (Vercel runtime) 

### Frontend

* HTML
* Tailwind CSS (CDN)
* JavaScript (ES Modules)

### Database & Auth

* Firebase Authentication
* Firebase Firestore 

---

## 📦 Installation (Local Setup)

```bash
git clone https://github.com/your-username/student-marks-analyzer.git
cd student-marks-analyzer
pip install -r requirements.txt
```

Create a `.env` file and add Firebase credentials (for local testing).

Run locally:

```bash
python flas.py
```

---

## 🌐 Deployment (Vercel)

1. Push repository to GitHub
2. Import project in **Vercel**
3. Set environment variables
4. Use `gunicorn` as runtime
5. Deploy 🚀

---

## ✅ Future Enhancements

* Export analysis as PDF
* Graphical performance reports
* Admin dashboard
* Editable analysis history
* Role-based access

## 🧠 Key Learning Outcomes

This project demonstrates:

1. Full-stack web development
2. REST API handling using Flask
3. Firebase Authentication integration
4. Firestore database operations
5. Session management
6. Cloud deployment
7. Dynamic frontend rendering
8. GPA and percentage analytics
9. Secure environment variable handling
---

## 🧑‍💻 Author

**Sanjana Krishnan**
CSE Student | Data Science Enthusiast
