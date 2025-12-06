import { initializeApp } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.1.0/firebase-analytics.js";
import {
  getAuth,
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword
} from "https://www.gstatic.com/firebasejs/11.1.0/firebase-auth.js";

/* ================= Firebase Config ================= */
const firebaseConfig = {
  apiKey: "AIzaSyCrsodPcoKohu381Nyr37nqG4WBgXEwljU",
  authDomain: "marks-analysis-58fc4.firebaseapp.com",
  projectId: "marks-analysis-58fc4",
  storageBucket: "marks-analysis-58fc4.firebasestorage.app",
  messagingSenderId: "165564992288",
  appId: "1:165564992288:web:57b68b4f70948b4e182545",
  measurementId: "G-G4DNFWZHJJ"
};

/* ================= Init ================= */
const app = initializeApp(firebaseConfig);
getAnalytics(app);
const auth = getAuth(app);

/* ================= DOM Elements ================= */
const submitButton = document.getElementById("submit");
const signupButton = document.getElementById("sign-up");
const returnBtn = document.getElementById("return-btn");

const main = document.getElementById("main");
const createacct = document.getElementById("create-acct");

const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");

const signupEmailIn = document.getElementById("email-signup");
const confirmSignupEmailIn = document.getElementById("confirm-email-signup");
const signupPasswordIn = document.getElementById("password-signup");
const confirmSignupPasswordIn = document.getElementById("confirm-password-signup");

const createacctbtn = document.getElementById("create-acct-btn");

/* ================= Sign Up ================= */
createacctbtn.addEventListener("click", async (e) => {
  e.preventDefault();

  const signupEmail = signupEmailIn.value.trim();
  const confirmSignupEmail = confirmSignupEmailIn.value.trim();
  const signupPassword = signupPasswordIn.value;
  const confirmSignupPassword = confirmSignupPasswordIn.value;

  if (!signupEmail || !confirmSignupEmail || !signupPassword || !confirmSignupPassword) {
    alert("Please fill out all required fields.");
    return;
  }

  if (signupEmail !== confirmSignupEmail) {
    alert("Email fields do not match.");
    return;
  }

  if (signupPassword !== confirmSignupPassword) {
    alert("Password fields do not match.");
    return;
  }

  if (signupPassword.length < 6) {
    alert("Password must be at least 6 characters.");
    return;
  }

  try {
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      signupEmail,
      signupPassword
    );

    await createFlaskSession(userCredential.user);
    alert("Account created successfully!");
    window.location.href = "/";

  } catch (error) {
    console.error("Firebase Signup Error:", error);
    alert(error.code + " : " + error.message);
  }
});

/* ================= Login ================= */
submitButton.addEventListener("click", async (e) => {
  e.preventDefault();

  const email = emailInput.value.trim();
  const password = passwordInput.value;

  if (!email || !password) {
    alert("Email and password are required.");
    return;
  }

  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);

    await createFlaskSession(userCredential.user);
    alert("Login successful!");
    window.location.href = "/";

  } catch (error) {
    console.error("Firebase Login Error:", error);
    alert(error.code + " : " + error.message);
  }
});

/* ================= UI Toggle ================= */
signupButton.addEventListener("click", () => {
  main.style.display = "none";
  createacct.style.display = "block";
});

returnBtn.addEventListener("click", () => {
  main.style.display = "block";
  createacct.style.display = "none";
});

/* ================= Flask Session ================= */
async function createFlaskSession(user) {
  const idToken = await user.getIdToken();

  const res = await fetch("/api/session-login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ idToken })
  });

  if (!res.ok) {
    throw new Error("Flask session creation failed");
  }
}
