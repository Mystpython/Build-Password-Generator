import streamlit as st
import string
import secrets
import pyperclip

# Page configuration
st.set_page_config(page_title="Secure Password Generator", page_icon="🔐", layout="centered")

# Title and header
st.title("🔐 Secure Password Generator")
st.write("Generate a cryptographically strong and secure password for yourself.")
st.markdown("---")

# Main core function
def generate_secure_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    upper_chars = string.ascii_uppercase
    lower_chars = string.ascii_lowercase
    digit_chars = string.digits
    symbol_chars = "!@#$%^&*()-_=+"

    if exclude_ambiguous:
        upper_chars = upper_chars.replace('I', '').replace('O', '')
        lower_chars = lower_chars.replace('l', '')
        digit_chars = digit_chars.replace('1', '').replace('0', '')

    char_pool = ""
    guaranteed = []

    if use_upper:
        char_pool += upper_chars
        guaranteed.append(secrets.choice(upper_chars))
    if use_lower:
        char_pool += lower_chars
        guaranteed.append(secrets.choice(lower_chars))
    if use_digits:
        char_pool += digit_chars
        guaranteed.append(secrets.choice(digit_chars))
    if use_symbols:
        char_pool += symbol_chars
        guaranteed.append(secrets.choice(symbol_chars))

    if not char_pool:
        return "Error"

    if length < len(guaranteed):
        length = len(guaranteed)

    remaining = length - len(guaranteed)
    password_list = guaranteed + [secrets.choice(char_pool) for _ in range(remaining)]
    
    secrets.SystemRandom().shuffle(password_list)
    return "".join(password_list)

def check_strength(password):
    length = len(password)
    if length < 8:
        return "Weak [X] 🔴", "error"
    elif length < 12:
        return "Medium [/] 🟡", "warning"
    else:
        return "Strong [VERY SECURE] 🟢", "success"

# --- Sidebar / Controls ---
st.subheader("⚙️ Password Settings")

# Length Control Slider
user_length = st.slider("Choose your password length:", min_value=6, max_value=32, value=12)

# Features Checkboxes
col1, col2 = st.columns(2)
with col1:
    inc_upper = st.checkbox("Include uppercase letters (A-Z)", value=True)
    inc_lower = st.checkbox("Include lowercase letters (a-z)", value=True)
with col2:
    inc_digits = st.checkbox("Include numbers (0-9)", value=True)
    inc_symbols = st.checkbox("Include special symbols (!@#$)", value=True)

exc_ambig = st.checkbox("Exclude confusing characters (l, 1, O, 0)", value=True)

st.markdown("---")

# --- Generate Button ---
if st.button("✨ Generate Password", type="primary"):
    password = generate_secure_password(user_length, inc_upper, inc_lower, inc_digits, inc_symbols, exc_ambig)
    
    if password == "Error":
        st.error("At least one character type must be selected!")
    else:
        # Display Password Box
        st.subheader("Your Password:")
        st.code(password, language="")
        
        # Strength Meter
        strength_msg, level = check_strength(password)
        if level == "error":
            st.error(f"Password Strength: {strength_msg}")
        elif level == "warning":
            st.warning(f"Password Strength: {strength_msg}")
        else:
            st.success(f"Password Strength: {strength_msg}")
            
        # Copy to Clipboard
        pyperclip.copy(password)
        st.toast("-> Password auto-copied! 📋")