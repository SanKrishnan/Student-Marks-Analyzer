# 🎓 Student Marks Analyzer

A **Flask + Firebase** web application that allows authenticated users to analyze student marks, calculate totals and averages, determine pass/fail status, and securely store analysis history in **Firestore**.
The application is **deployed on Vercel** as a serverless Flask app.

---

## 🚀 Live Deployment

✅ Deployed using **Vercel Serverless Functions**
✅ Backend: Flask
✅ Frontend: HTML, Tailwind CSS, JavaScript
✅ Authentication: Firebase Authentication
✅ Database: Firebase Firestore

---

## 📌 Features

* 🔐 **User Authentication**

  * Sign up & login using Firebase Authentication
  * Secure session handling using Flask sessions 

* 📊 **Marks Analysis**

  * Input marks for three courses
  * Calculates:

    * Total marks
    * Average marks
    * Pass/Fail result (minimum 40 per subject)
  * Real-time analysis response

* ☁️ **Firestore Integration**

  * Stores every analysis with timestamp
  * Data is saved per authenticated user
  * Profile page shows past analysis history 

* 👤 **User Profile Dashboard**

  * Displays:

    * Logged-in email
    * Total analyses performed
    * Previous results with averages and outcomes 

* 🎨 **Clean UI**

  * Tailwind CSS for modern UI
  * Modal-based profile viewer
  * Dropdown user menu with logout and profile options 

---

## 🗂️ Project Structure

```
├── app.py / flas.py        # Flask backend (API + session handling)
├── index.html              # Main marks analyzer UI
├── Login_signup.html       # Login & signup page
├── Login_signup.css        # Authentication page styles
├── Loginsign.js            # Firebase auth logic + session creation
├── requirements.txt        # Python dependencies
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

---

## 🧑‍💻 Author

**Sanjana Krishnan**
CSE Student | Web Development & Data Science Enthusiast
