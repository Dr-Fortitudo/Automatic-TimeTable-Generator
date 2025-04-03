import streamlit as st
import requests

# Streamlit UI
st.title("Faculty Login")

# Backend URL
API_URL = "https://automatic-timetable-generator-2953.onrender.com"

# Fetch data from backend
response = requests.get(API_URL)
if response.status_code == 200:
    data = response.json()
    st.write(f"Backend Response: {data['message']}")
else:
    st.write("Error connecting to the backend.")

Login_URL = "https://automatic-timetable-generator-2953.onrender.com/login" 

def login(username, password):
    response = requests.post(Login_URL, json={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()
    else:
        return None

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
