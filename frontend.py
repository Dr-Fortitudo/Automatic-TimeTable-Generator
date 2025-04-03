import streamlit as st
import requests

# Streamlit UI
st.title("Faculty Login")

# Backend URL
API_URL = "https://automatic-timetable-generator-2953.onrender.com"
LOGIN_URL = f"{API_URL}/login"

# Check if backend is running
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        st.write("✅ Backend is running!")
    else:
        st.write("❌ Error connecting to the backend.")
except requests.exceptions.RequestException:
    st.write("❌ Backend is unreachable.")

# Login function
def login(username, password):
    try:
        response = requests.post(LOGIN_URL, json={"username": username, "password": password})
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        return None
    return None

# Login form
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")

if login_button:
    result = login(username, password)
    if result:
        st.success(f"Welcome {result['role']}!") 
        st.session_state["logged_in"] = True
        st.session_state["user"] = result
        st.experimental_rerun()
    else:
        st.error("Invalid username or password")

# Debugging - Display session state
st.write(st.session_state)
