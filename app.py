import os
import json
from flask import request, Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Load Firebase Credentials from JSON File Instead of Environment Variable
firebase_credentials_path = "timetable-b3371-firebase-adminsdk-fbsvc-d13120ed4b.json"
if not os.path.exists(firebase_credentials_path):
    raise FileNotFoundError(f"Firebase credentials file not found: {firebase_credentials_path}")

with open(firebase_credentials_path) as f:
    firebase_credentials = json.load(f)

cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Predefined passwords
FACULTY_PASSWORD = "ec@1234"
HOD_CREDENTIALS = {"username": "HOD@EC", "password": "ec@1234"}

@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Check if HOD login
    if username == HOD_CREDENTIALS["username"] and password == HOD_CREDENTIALS["password"]:
        return jsonify({"role": "HOD", "message": "Login successful"}), 200

    # Check if Faculty login
    faculty_ref = db.collection("users").document(username).get()
    if faculty_ref.exists and password == FACULTY_PASSWORD:
        return jsonify({"role": "Faculty", "message": "Login successful"}), 200

    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
