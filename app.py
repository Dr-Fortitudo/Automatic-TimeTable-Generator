import os
import json
from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Load Firebase Credentials
firebase_credentials = json.loads(os.getenv("FIREBASE_CREDENTIALS"))
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Predefined passwords
FACULTY_PASSWORD = "fac1234"
HOD_CREDENTIALS = {"username": "HOD@EC", "password": "ec@1234"}

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
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned PORT or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
