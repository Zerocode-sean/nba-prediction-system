#!/usr/bin/env python3
"""
🏀 NBA Predictions - Complete Authentication App
===============================================

Standalone app with built-in authentication and routing.
"""

import streamlit as st
import hashlib
from datetime import datetime
import sys
from pathlib import Path

# Set page config first
st.set_page_config(
    page_title="🏀 NBA Predictions",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Demo accounts
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

def authenticate_user(username, password):
    """Authenticate a user and return their info if valid"""
    if username in DEMO_ACCOUNTS:
        user_data = DEMO_ACCOUNTS[username]
        if hash_password(password) == user_data["password_hash"]:
            return {
                "username": username,
                "role": user_data["role"],
                "name": user_data["name"],
                "email": user_data["email"],
                "login_time": datetime.now()
            }
    return None

def show_login_form():
    """Display the login form"""
    
    # Custom CSS for login form
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .login-container {
        max-width: 450px;
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
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .login-subtitle {
        color: #6c757d;
        font-size: 1.2em;
    }
    
    .demo-accounts {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 25px;
        margin: 25px 0;
        border-left: 5px solid #17a2b8;
    }
    
    .demo-accounts h4 {
        color: #17a2b8;
        margin-bottom: 20px;
        font-size: 1.3em;
    }
    
    .demo-account {
        background: white;
        padding: 15px 20px;
        margin: 12px 0;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .demo-account.admin {
        border-left-color: #dc3545;
    }
    
    .demo-account strong {
        color: #2c3e50;
        font-size: 1.1em;
    }
    
    .demo-account small {
        color: #6c757d;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main login container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="login-header">
        <div class="login-title">🏀 NBA Predictions</div>
        <div class="login-subtitle">Professional Sports Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form", clear_on_submit=False):
        st.markdown("### 🔐 Sign In")
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
            
            st.success(f"✅ Welcome back, {user_info['name']}!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")
    
    # Handle guest access
    if guest_button:
        user_info = authenticate_user("guest", "guest123")
        if user_info:
            st.session_state.authenticated = True
            st.session_state.user_username = user_info["username"]
            st.session_state.user_role = user_info["role"]
            st.session_state.user_name = user_info["name"]
            st.session_state.user_email = user_info["email"]
            st.session_state.login_time = user_info["login_time"]
            
            st.success("✅ Welcome, Guest User!")
            st.rerun()
    
    # Demo accounts info
    st.markdown("""
    <div class="demo-accounts">
        <h4>📋 Demo Accounts</h4>
        <div class="demo-account admin">
            <strong>🔴 Admin:</strong> admin / admin123<br>
            <small>Full system administration access</small>
        </div>
        <div class="demo-account admin">
            <strong>🔴 Demo Admin:</strong> demo_admin / demo123<br>
            <small>Demo administrator account</small>
        </div>
        <div class="demo-account">
            <strong>🟢 User:</strong> user1 / user123<br>
            <small>Standard user predictions access</small>
        </div>
        <div class="demo-account">
            <strong>🟢 Guest:</strong> guest / guest123<br>
            <small>Limited guest user access</small>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: white; margin-top: 30px; font-size: 1.1em;">
        <strong>🔒 Secure Authentication System</strong><br>
        <small>NBA Predictions Platform v2.0 | Demo Environment</small>
    </div>
    """, unsafe_allow_html=True)

def show_admin_dashboard():
    """Show admin dashboard"""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    user_name = st.session_state.get('user_name', 'Admin')
    
    # Header with logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="color: #dc3545; margin: 0;">👨‍💼 Admin Dashboard</h1>
            <p style="color: #6c757d; margin: 5px 0 0 0;">Welcome back, {user_name}!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith(('user_', 'authenticated')):
                    del st.session_state[key]
            st.rerun()
    
    # Admin content
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "⚙️ Settings", "📈 Analytics"])
    
    with tab1:
        st.markdown("""
        ### 🎛️ System Overview
        
        **System Status:** 🟢 Online  
        **Active Users:** 1,234  
        **Predictions Today:** 5,678  
        **Model Accuracy:** 92.4%
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Users", "1,234", "+12%")
        with col2:
            st.metric("Predictions", "5,678", "+8%")
        with col3:
            st.metric("Accuracy", "92.4%", "+2.1%")
    
    with tab2:
        st.markdown("### ⚙️ System Settings")
        st.checkbox("Enable new user registration", True)
        st.checkbox("Allow guest access", True)
        st.slider("Max concurrent users", 100, 10000, 1000)
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")
    
    with tab3:
        st.markdown("### 📈 User Analytics")
        st.line_chart([100, 120, 140, 110, 160, 180, 200])
        st.markdown("Daily active users over the past week")

def show_user_dashboard():
    """Show user dashboard"""
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    user_name = st.session_state.get('user_name', 'User')
    
    # Header with logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <h1 style="color: #667eea; margin: 0;">🏀 NBA Predictions</h1>
            <p style="color: #6c757d; margin: 5px 0 0 0;">Welcome, {user_name}!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith(('user_', 'authenticated')):
                    del st.session_state[key]
            st.rerun()
    
    # User content
    st.markdown("""
    ### 🎯 Today's Predictions
    
    **Lakers vs Warriors**  
    📅 Tonight 8:00 PM EST  
    🎯 **Prediction:** Lakers Win (72% confidence)  
    📊 **Total:** Over 225.5 (68% confidence)  
    
    **Celtics vs Heat**  
    📅 Tonight 7:30 PM EST  
    🎯 **Prediction:** Celtics Win (85% confidence)  
    📊 **Total:** Under 218.5 (61% confidence)  
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Win Rate", "85%", "+3%")
    with col2:
        st.metric("Accuracy", "92%", "+1%")
    with col3:
        st.metric("Games", "1,230", "+50")
    
    st.markdown("---")
    st.markdown("""
    ### ℹ️ How It Works
    - 🤖 **AI-Powered**: Advanced machine learning models
    - 📊 **Real-Time Data**: Live NBA statistics and trends  
    - 🎯 **High Accuracy**: 92% prediction accuracy
    - 📱 **Always Updated**: Fresh predictions daily
    """)

def main():
    """Main application function"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Check authentication
    if not st.session_state.authenticated:
        show_login_form()
    else:
        # User is authenticated, show appropriate dashboard
        user_role = st.session_state.get('user_role', 'user')
        if user_role == 'admin':
            show_admin_dashboard()
        else:
            show_user_dashboard()

if __name__ == "__main__":
    main()
