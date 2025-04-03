import streamlit as st
import requests

st.title("Automated Timetable System")

# Backend URL
API_URL = "https://automatic-timetable-generator-2953.onrender.com"

# Fetch data from backend
response = requests.get(API_URL)
if response.status_code == 200:
    data = response.json()
    st.write(f"Backend Response: {data['message']}")
else:
    st.write("Error connecting to the backend.")
