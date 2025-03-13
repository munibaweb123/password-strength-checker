import re
import streamlit as st
from collections import deque
import string
import random

def generate_password(length,use_digits,use_special,use_upper,use_lower):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits

    if use_special:
        characters += string.punctuation
    
    if use_upper:
        characters += string.ascii_uppercase

    if use_lower:
        characters += string.ascii_lowercase

    return ''.join(random.choice(characters) for _ in range(length))
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
st.title("🔒 Password Strength Check Meter")
st.header('Generate your password from here:')
length = st.slider('select password length', min_value=5, max_value=15)
use_digits = st.checkbox('Include Digits:')
use_special = st.checkbox('Include special characters:')
use_upper = st.checkbox('Include uppercase alphabets')
use_lower = st.checkbox('Include lowercase alphabets')

# Sidebar for password history
st.sidebar.header("Password History")
if st.session_state.password_history:
    for pwd in st.session_state.password_history:
        st.sidebar.write(pwd)
else:
    st.sidebar.write("No password history available.")

if st.button('Generate password'):
    password = generate_password(length,use_digits,use_special,use_upper,use_lower)
    st.write(f'Generated Password: `{password}`')
password = st.text_input("paste your generated password or Enter your password here to check:", type="password")

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
