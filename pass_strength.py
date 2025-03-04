import re
import streamlit as st
from collections import deque

# Initialize password history in session state
if 'password_history' not in st.session_state:
    st.session_state.password_history = deque(maxlen=10)

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Check if password was used in the last 10 entries
    if password in st.session_state.password_history:
        feedback.append("⚠️ This password was recently used. Please choose a new one.")
        return "❌ Old Password - Choose a unique password.", feedback
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Strength Rating
    if score == 4:
        return "✅ Strong Password!", feedback
    elif score == 3:
        return "⚠️ Moderate Password - Consider adding more security features.", feedback
    else:
        return "❌ Weak Password - Improve it using the suggestions above.", feedback

# Streamlit UI
st.title("🔒 Password Strength Checker")
password = st.text_input("Enter your password:", type="password")

if st.button("Check Strength"):
    if password:
        strength, feedback = check_password_strength(password)
        st.subheader(strength)
        for msg in feedback:
            st.write(msg)
        
        # Store password in history if it's not a duplicate
        if password not in st.session_state.password_history:
            st.session_state.password_history.append(password)
    else:
        st.error("Please enter a password to check its strength.")
