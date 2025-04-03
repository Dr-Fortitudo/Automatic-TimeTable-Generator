import os
import json
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Load Firebase Credentials
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_credentials:
    print("Error: FIREBASE_CREDENTIALS environment variable not found")
    exit(1)

try:
    firebase_credentials = json.loads(firebase_credentials)
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase initialized successfully")
except Exception as e:
    print(f"🔥 Error initializing Firebase: {e}")
    exit(1)

# Predefined passwords
FACULTY_PASSWORD = "ec@1234"
HOD_CREDENTIALS = {"username": "HOD@EC", "password": "ec@1234"}

@app.route("/")
def home():
    return jsonify({"message": "Backend is running"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    print(f"🔍 Received Login Request: Username={username}, Password={password}")

    # Check if HOD login
    if username == HOD_CREDENTIALS["username"] and password == HOD_CREDENTIALS["password"]:
        print("✅ HOD login successful")
        return jsonify({"role": "HOD", "message": "Login successful"}), 200

    # Check if Faculty login (fetch from Firebase)
    faculty_ref = db.collection("users").document(username).get()

    if faculty_ref.exists:
        stored_data = faculty_ref.to_dict()
        stored_password = stored_data.get("password")

        print(f"📄 Faculty Found: {stored_data}")

        if stored_password == password:
            print("✅ Faculty login successful")
            return jsonify({"role": "Faculty", "message": "Login successful"}), 200
        else:
            print("❌ Incorrect faculty password")
    else:
        print("❌ Faculty not found in database")

    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
