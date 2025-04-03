import os
from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Load Firebase Credentials
firebase_credentials = json.loads(os.getenv("FIREBASE_CREDENTIALS"))
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/")
def home():
    return jsonify({"message": "Flask API is running!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned PORT or default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
