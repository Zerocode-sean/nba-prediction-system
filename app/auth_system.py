#!/usr/bin/env python3
"""
🔐 NBA Predictions - Authentication System
==========================================

Handles user authentication and routing to appropriate dashboards.
Supports both admin and regular user accounts.
"""

import streamlit as st
import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path

# Demo accounts - In production, these would be in a secure database
DEMO_ACCOUNTS = {
    "admin": {
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin",
        "name": "Administrator",
        "email": "admin@nbapredictions.com"
    },
    "demo_admin": {
        "password_hash": hashlib.sha256("demo123".encode()).hexdigest(),
        "role": "admin",
        "name": "Demo Admin",
        "email": "demo@nbapredictions.com"
    },
    "user1": {
        "password_hash": hashlib.sha256("user123".encode()).hexdigest(),
        "role": "user",
        "name": "Demo User",
        "email": "user@nbapredictions.com"
    },
    "guest": {
        "password_hash": hashlib.sha256("guest123".encode()).hexdigest(),
        "role": "user",
        "name": "Guest User",
        "email": "guest@nbapredictions.com"
    }
}

def hash_password(password):
    """Hash a password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify a password against its hash"""
    return hash_password(password) == password_hash

def authenticate_user(username, password):
    """Authenticate a user and return their info if valid"""
    if username in DEMO_ACCOUNTS:
        user_data = DEMO_ACCOUNTS[username]
        if verify_password(password, user_data["password_hash"]):
            return {
                "username": username,
                "role": user_data["role"],
                "name": user_data["name"],
                "email": user_data["email"],
                "login_time": datetime.now()
            }
    return None

def logout_user():
    """Log out the current user"""
    for key in list(st.session_state.keys()):
        if key.startswith(('user_', 'authenticated', 'login_')):
            del st.session_state[key]
    st.rerun()

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Get current user info"""
    if is_authenticated():
        return {
            "username": st.session_state.get('user_username'),
            "role": st.session_state.get('user_role'),
            "name": st.session_state.get('user_name'),
            "email": st.session_state.get('user_email'),
            "login_time": st.session_state.get('login_time')
        }
    return None

def show_login_form():
    """Display the login form"""
    
    # Custom CSS for login form
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 50px auto;
        padding: 40px;
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .login-title {
        color: #2c3e50;
        font-size: 2.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .login-subtitle {
        color: #6c757d;
        font-size: 1.1em;
    }
    
    .demo-accounts {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border-left: 4px solid #17a2b8;
    }
    
    .demo-accounts h4 {
        color: #17a2b8;
        margin-bottom: 15px;
    }
    
    .demo-account {
        background: white;
        padding: 10px 15px;
        margin: 8px 0;
        border-radius: 8px;
        border-left: 3px solid #28a745;
    }
    
    .demo-account.admin {
        border-left-color: #dc3545;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main login container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="login-header">
        <div class="login-title">🏀 NBA Predictions</div>
        <div class="login-subtitle">Sign in to access your dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            login_button = st.form_submit_button("🔑 Login", use_container_width=True)
        with col2:
            guest_button = st.form_submit_button("👤 Guest Access", use_container_width=True)
    
    # Handle login
    if login_button and username and password:
        user_info = authenticate_user(username, password)
        if user_info:
            # Store user info in session state
            st.session_state.authenticated = True
            st.session_state.user_username = user_info["username"]
            st.session_state.user_role = user_info["role"]
            st.session_state.user_name = user_info["name"]
            st.session_state.user_email = user_info["email"]
            st.session_state.login_time = user_info["login_time"]
            
            st.success(f"Welcome back, {user_info['name']}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")
    
    # Handle guest access
    if guest_button:
        # Log in as guest user
        user_info = authenticate_user("guest", "guest123")
        if user_info:
            st.session_state.authenticated = True
            st.session_state.user_username = user_info["username"]
            st.session_state.user_role = user_info["role"]
            st.session_state.user_name = user_info["name"]
            st.session_state.user_email = user_info["email"]
            st.session_state.login_time = user_info["login_time"]
            
            st.success("Welcome, Guest User!")
            st.rerun()
    
    # Demo accounts info
    st.markdown("""
    <div class="demo-accounts">
        <h4>📋 Demo Accounts</h4>
        <div class="demo-account admin">
            <strong>Admin:</strong> admin / admin123<br>
            <small>Full access to admin dashboard</small>
        </div>
        <div class="demo-account admin">
            <strong>Demo Admin:</strong> demo_admin / demo123<br>
            <small>Demo admin account</small>
        </div>
        <div class="demo-account">
            <strong>User:</strong> user1 / user123<br>
            <small>Standard user access</small>
        </div>
        <div class="demo-account">
            <strong>Guest:</strong> guest / guest123<br>
            <small>Limited guest access</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: #6c757d; margin-top: 30px;">
        <small>🔒 Secure NBA Predictions Platform | Demo Environment</small>
    </div>
    """, unsafe_allow_html=True)

def show_user_header():
    """Show header with user info and logout option"""
    user = get_current_user()
    if user:
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            role_icon = "👨‍💼" if user["role"] == "admin" else "👤"
            st.markdown(f"**{role_icon} Welcome, {user['name']}** ({user['role'].title()})")
        
        with col2:
            st.markdown(f"<small>Login: {user['login_time'].strftime('%H:%M')}</small>", unsafe_allow_html=True)
        
        with col3:
            if st.button("🚪 Logout"):
                logout_user()

def main():
    """Main authentication function"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Check authentication status
    if not is_authenticated():
        show_login_form()
        return None
    else:
        show_user_header()
        return get_current_user()

if __name__ == "__main__":
    user = main()
    if user:
        st.write(f"Authenticated as: {user}")
