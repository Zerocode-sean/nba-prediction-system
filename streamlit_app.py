#!/usr/bin/env python3
"""
🏀 NBA Predictions - Clean Working Version
==========================================

Clean version that properly imports and uses our enhanced user dashboard.
"""

import streamlit as st
import hashlib
import sys
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from pathlib import Path

# Set page config first
st.set_page_config(
    page_title="🏀 NBA Predictions",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add app directory to path for imports
app_dir = Path(__file__).parent / "app"
sys.path.append(str(app_dir))

# Import our enhanced dashboard
try:
    from user_dashboard import main as enhanced_dashboard_main
    ENHANCED_DASHBOARD_AVAILABLE = True
    print("✅ Enhanced dashboard imported successfully")
except ImportError as e:
    print(f"❌ Enhanced dashboard import error: {e}")
    enhanced_dashboard_main = None
    ENHANCED_DASHBOARD_AVAILABLE = False

# Demo accounts
DEMO_ACCOUNTS = {
    "user1": {
        "password_hash": hashlib.sha256("user123".encode()).hexdigest(),
        "role": "user",
        "name": "Demo User",
        "email": "user@nbapredictions.com"
    },
    "demo_user": {
        "password_hash": hashlib.sha256("demo123".encode()).hexdigest(),
        "role": "user",
        "name": "Demo User 2",
        "email": "demo@nbapredictions.com"
    },
    "guest": {
        "password_hash": hashlib.sha256("guest123".encode()).hexdigest(),
        "role": "user",
        "name": "Guest User", 
        "email": "guest@nbapredictions.com"
    },
    "admin": {
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin",
        "name": "Administrator",
        "email": "admin@nbapredictions.com"
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

def apply_login_styling():
    """Apply modern login page styling"""
    st.markdown("""
    <style>
    /* Hide Streamlit default elements */
    .stApp > header {
        display: none !important;
    }
    
    /* Hide main menu */
    #MainMenu {
        display: none !important;
    }
    
    /* Hide footer */
    footer {
        display: none !important;
    }
    
    /* Hide toolbar */
    .stToolbar {
        display: none !important;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background-color: rgba(0, 255, 136, 0.1) !important;
        border: 1px solid rgba(0, 255, 136, 0.3) !important;
        color: #00FF88 !important;
    }
    
    .stError {
        background-color: rgba(255, 75, 75, 0.1) !important;
        border: 1px solid rgba(255, 75, 75, 0.3) !important;
        color: #FF4B4B !important;
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #0B0808 0%, #18181C 100%);
        color: #ffffff;
    }
    
    /* Login wrapper */
    .login-wrapper {
        background: linear-gradient(135deg, #0B0808 0%, #18181C 100%);
        min-height: 100vh;
        display: flex;
        flex-direction: row;
        overflow: hidden;
        margin: 0;
        padding: 0;
    }
    
    /* Branding side */
    .login-brand {
        flex: 1;
        background: linear-gradient(45deg, #dfe31d 0%, #00FF88 100%);
        padding: 3rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .login-brand h1 {
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 1rem;
        color: #0B0808;
        text-shadow: 2px 2px 4px rgba(11, 8, 8, 0.2);
    }
    
    .login-brand p {
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 2.5rem;
        color: #0B0808;
        opacity: 0.9;
    }
    
    .brand-features {
        background: rgba(11, 8, 8, 0.1);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(11, 8, 8, 0.15);
        width: 100%;
        max-width: 400px;
    }
    
    .brand-features div {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #0B0808;
        display: flex;
        align-items: center;
        justify-content: flex-start;
    }
    
    .brand-features span {
        margin-right: 0.8rem;
        font-size: 1.4rem;
    }
    
    /* Form side */
    .login-form {
        flex: 1;
        background: linear-gradient(135deg, #0B0808 0%, #18181C 100%);
        padding: 3rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .form-title {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .form-title h2 {
        color: #dfe31d;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(223, 227, 29, 0.3);
    }
    
    .form-title p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: #2a2a2e !important;
        border: 2px solid #3a3a3e !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #dfe31d !important;
        box-shadow: 0 0 0 2px rgba(223, 227, 29, 0.2) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888888 !important;
    }
    
    /* Labels styling */
    .stTextInput > label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Additional label selectors */
    .stTextInput label {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Text input container */
    .stTextInput > div {
        margin-bottom: 1rem !important;
    }
    
    /* Make sure labels are visible */
    div[data-testid="stTextInputLabel"] {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Alternative label selector */
    .stTextInput p {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        margin-bottom: 8px !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Markdown text styling */
    .stMarkdown h3 {
        color: #dfe31d !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
    }
    
    .stMarkdown p strong {
        color: #dfe31d !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        display: block !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stMarkdown {
        color: #ffffff !important;
    }
    .stTextInput *, 
    .stTextInput label *, 
    .stTextInput p *,
    .stTextInput div * {
        color: #ffffff !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Ensure input containers are visible */
    .stTextInput {
        color: #ffffff !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
    
    /* Override any hidden text */
    .stApp [data-testid="stTextInput"] label,
    .stApp [data-testid="stTextInput"] p {
        color: #dfe31d !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        visibility: visible !important;
        opacity: 1 !important;
        display: block !important;
    }
    
    /* Form styling improvements */
    .stForm {
        background: rgba(24, 24, 28, 0.8) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        border: 1px solid rgba(223, 227, 29, 0.2) !important;
    }
    .stFormSubmitButton > button {
        background: linear-gradient(45deg, #dfe31d, #00FF88) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        width: 100% !important;
    }
    
    .stFormSubmitButton > button:hover {
        background: linear-gradient(45deg, #00FF88, #dfe31d) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(223, 227, 29, 0.4) !important;
    }
    
    /* Demo accounts styling */
    .demo-accounts {
        background: rgba(223, 227, 29, 0.1);
        border: 1px solid rgba(223, 227, 29, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        width: 100%;
        max-width: 450px;
    }
    
    .demo-accounts h4 {
        color: #dfe31d;
        margin-bottom: 1rem;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .demo-account {
        background: rgba(42, 42, 46, 0.5);
        border-radius: 8px;
        padding: 0.8rem;
        margin-bottom: 0.5rem;
        border-left: 3px solid #dfe31d;
        color: #ffffff;
    }
    
    .demo-account strong {
        color: #dfe31d;
    }
    
    .demo-account code {
        background: rgba(223, 227, 29, 0.2);
        color: #dfe31d;
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .login-wrapper {
            flex-direction: column;
        }
        
        .login-brand {
            flex: none;
            min-height: 40vh;
            padding: 2rem;
        }
        
        .login-brand h1 {
            font-size: 2.5rem;
        }
        
        .login-form {
            flex: 1;
            padding: 2rem;
        }
    }
    
    /* Enhanced Settings Tab Styles */
    .settings-section {
        background: rgba(42, 42, 46, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(223, 227, 29, 0.2);
    }
    
    .settings-section h4 {
        color: #dfe31d;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .settings-metric {
        background: rgba(223, 227, 29, 0.1);
        border-radius: 8px;
        padding: 0.8rem;
        text-align: center;
        border: 1px solid rgba(223, 227, 29, 0.3);
    }
    
    .settings-metric h3 {
        color: #dfe31d;
        margin: 0;
        font-size: 1.2rem;
    }
    
    .settings-metric p {
        color: #ffffff;
        margin: 0.3rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* Settings toggle improvements */
    .stCheckbox > div {
        background: rgba(42, 42, 46, 0.5);
        border-radius: 8px;
        padding: 0.5rem;
        border: 1px solid rgba(223, 227, 29, 0.2);
    }
    
    /* Settings slider improvements */
    .stSlider > div > div > div {
        background: rgba(223, 227, 29, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def show_login_form():
    """Display the modern two-sided responsive login form"""
    apply_login_styling()
    
    # Create the main login layout
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-brand">
            <h1>🏀 NBA</h1>
            <p>Professional Basketball Predictions</p>
            <div class="brand-features">
                <div><span>🤖</span> AI-Powered Predictions</div>
                <div><span>📊</span> Real-Time Analytics</div>
                <div><span>💰</span> Profit Tracking</div>
                <div><span>🔥</span> Hot Picks Daily</div>
            </div>
        </div>
        <div class="login-form">
            <div class="form-title">
                <h2>Welcome Back</h2>
                <p>Sign in to access your dashboard</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a container for the form
    with st.container():
        st.markdown("""
        <div style="background: rgba(24, 24, 28, 0.9); padding: 2rem; border-radius: 15px; border: 1px solid rgba(223, 227, 29, 0.3); margin: 2rem auto; max-width: 500px;">
        """, unsafe_allow_html=True)
        
        st.markdown("### 🔐 Login to Your Dashboard")
        st.markdown("---")
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            st.markdown("**👤 Username:**")
            username = st.text_input("Username", placeholder="Enter your username", key="username_input", label_visibility="collapsed")
            
            st.markdown("**🔒 Password:**")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="password_input", label_visibility="collapsed")
            
            st.markdown("")  # Spacing
            
            # Button columns
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                login_button = st.form_submit_button("🔑 Login", use_container_width=True)
            with btn_col2:
                guest_button = st.form_submit_button("👤 Guest", use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Handle login
        if login_button and username and password:
            user_info = authenticate_user(username, password)
            if user_info:
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
                
                st.success(f"✅ Welcome, {user_info['name']}!")
                st.rerun()
    
    # Demo accounts section
    st.markdown("""
    <div class="demo-accounts">
        <h4>� Demo Accounts</h4>
        <div class="demo-account">
            <strong>User Account:</strong> <code>user1</code> / <code>user123</code>
        </div>
        <div class="demo-account">
            <strong>Demo User:</strong> <code>demo_user</code> / <code>demo123</code>
        </div>
        <div class="demo-account">
            <strong>Guest Access:</strong> Click the "👤 Guest" button for instant access
        </div>
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
            if st.button("🚪 Logout", key="logout_btn"):
                logout_user()

def show_user_dashboard(user):
    """Show user dashboard - route to enhanced version"""
    if ENHANCED_DASHBOARD_AVAILABLE and enhanced_dashboard_main:
        st.sidebar.success("✅ Enhanced Dashboard Loaded")
        enhanced_dashboard_main(user)
    else:
        st.sidebar.error("❌ Enhanced dashboard unavailable")
        st.error("Enhanced dashboard not available. Please check the user_dashboard.py file.")
        st.title("🏀 Basic NBA Dashboard")
        st.write(f"Welcome {user['name']}! Basic dashboard is loading...")

def show_admin_dashboard(user):
    """Show comprehensive admin dashboard"""
    
    # Ensure user is a dictionary (not pandas Series)
    if hasattr(user, 'to_dict'):
        user = user.to_dict()
    
    # Get admin name safely
    admin_name = user.get('name', user.get('username', 'Unknown Admin'))
    
    # Apply admin dashboard styling
    st.markdown("""
    <style>
    /* Admin Dashboard Styling */
    .admin-header {
        background: linear-gradient(45deg, #FF4B4B, #FF8C00);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    .admin-metric-card {
        background: linear-gradient(135deg, #0B0808 0%, #18181C 100%);
        border: 2px solid #FF4B4B;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .admin-section {
        background: rgba(255, 75, 75, 0.1);
        border: 1px solid rgba(255, 75, 75, 0.3);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .admin-section h4 {
        color: #FF4B4B;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .status-online { color: #00FF88; }
    .status-warning { color: #FFD700; }
    .status-error { color: #FF4B4B; }
    </style>
    """, unsafe_allow_html=True)
    
    # Admin Header
    st.markdown("""
    <div class="admin-header">
        <h1>👨‍💼 Admin Dashboard</h1>
        <p>Welcome back, Administrator! Here's your system overview.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="admin-metric-card">
            <h2 style="color: #FF4B4B;">👥 Users</h2>
            <h1 style="color: #00FF88;">1,247</h1>
            <p style="color: #888;">+23 today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="admin-metric-card">
            <h2 style="color: #FF4B4B;">🏀 Predictions</h2>
            <h1 style="color: #dfe31d;">8,456</h1>
            <p style="color: #888;">+145 today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="admin-metric-card">
            <h2 style="color: #FF4B4B;">📊 Accuracy</h2>
            <h1 style="color: #00FF88;">73.2%</h1>
            <p style="color: #888;">+2.1% this week</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="admin-metric-card">
            <h2 style="color: #FF4B4B;">💰 Revenue</h2>
            <h1 style="color: #00FF88;">$12,847</h1>
            <p style="color: #888;">+$234 today</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different admin sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analytics", 
        "👥 User Management", 
        "🏀 Predictions", 
        "⚙️ Settings", 
        "📈 Reports"
    ])
    
    with tab1:
        st.markdown("""
        <div class="admin-section">
            <h4>📊 System Analytics</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Real-time system status with refresh
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔧 System Health")
            
            # Auto-refresh system status
            if st.button("🔄 Refresh Status", key="refresh_status_btn"):
                st.rerun()
            
            # Simulate real system checks
            import time
            current_time = datetime.now()
            
            # API Status
            api_status = "online" if current_time.second % 2 == 0 else "online"
            api_color = "status-online" if api_status == "online" else "status-error"
            st.markdown(f"**API Status:** <span class='{api_color}'>●</span> {api_status.title()}", unsafe_allow_html=True)
            
            # Database Status
            db_response_time = np.random.randint(50, 200)
            db_color = "status-online" if db_response_time < 150 else "status-warning"
            st.markdown(f"**Database:** <span class='{db_color}'>●</span> Connected ({db_response_time}ms)", unsafe_allow_html=True)
            
            # ML Models Status
            model_accuracy = round(np.random.uniform(70, 85), 1)
            model_color = "status-online" if model_accuracy > 75 else "status-warning"
            st.markdown(f"**ML Models:** <span class='{model_color}'>●</span> Active ({model_accuracy}%)", unsafe_allow_html=True)
            
            # Cache Status
            cache_usage = np.random.randint(75, 95)
            cache_color = "status-online" if cache_usage < 85 else "status-warning"
            st.markdown(f"**Cache:** <span class='{cache_color}'>●</span> {cache_usage}% Full", unsafe_allow_html=True)
            
            # Real-time metrics
            uptime_value = round(np.random.uniform(99.5, 99.9), 1)
            response_time = np.random.randint(100, 200)
            
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric("🕐 Uptime", f"{uptime_value}%", f"{round(np.random.uniform(-0.5, 0.5), 1)}%")
            with col_metric2:
                st.metric("⚡ Response Time", f"{response_time}ms", f"{np.random.randint(-20, 20)}ms")
            
            # Memory and CPU usage
            st.subheader("� Server Resources")
            
            cpu_usage = np.random.randint(20, 80)
            memory_usage = np.random.randint(40, 85)
            disk_usage = np.random.randint(30, 70)
            
            # Progress bars for resource usage
            st.metric("🖥️ CPU Usage", f"{cpu_usage}%")
            st.progress(cpu_usage / 100)
            
            st.metric("🧠 Memory Usage", f"{memory_usage}%")
            st.progress(memory_usage / 100)
            
            st.metric("💾 Disk Usage", f"{disk_usage}%")
            st.progress(disk_usage / 100)
        
        with col2:
            st.subheader("📈 Usage Analytics")
            
            # Enhanced chart with multiple metrics
            days_back = st.slider("📅 Days to Show", 7, 30, 14, key="analytics_days_slider")
            
            # Generate realistic data
            dates = pd.date_range(start=datetime.now() - timedelta(days=days_back), 
                                 end=datetime.now(), freq='D')
            
            # Simulate realistic patterns
            base_users = 1000
            users = [base_users + int(100 * np.sin(i/3) + np.random.randint(-50, 100)) 
                    for i in range(len(dates))]
            
            predictions = [int(user_count * 0.15 + np.random.randint(-20, 50)) 
                          for user_count in users]
            
            accuracy = [round(73 + np.random.uniform(-5, 5), 1) for _ in range(len(dates))]
            
            chart_data = pd.DataFrame({
                'Date': dates,
                'Active Users': users,
                'Daily Predictions': predictions,
                'Model Accuracy': accuracy
            })
            
            # Tabs for different chart views
            chart_tab1, chart_tab2, chart_tab3 = st.tabs(["👥 Users", "🏀 Predictions", "📊 Accuracy"])
            
            with chart_tab1:
                st.line_chart(chart_data.set_index('Date')[['Active Users']], color='#00FF88')
                
            with chart_tab2:
                st.bar_chart(chart_data.set_index('Date')[['Daily Predictions']], color='#dfe31d')
                
            with chart_tab3:
                st.line_chart(chart_data.set_index('Date')[['Model Accuracy']], color='#FF4B4B')
        
        # Enhanced analytics section
        st.markdown("---")
        st.subheader("📊 Detailed Analytics")
        
        # Performance analytics
        perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
        
        with perf_col1:
            # Peak hours analysis
            st.markdown("**🕐 Peak Hours**")
            peak_hours = pd.DataFrame({
                'Hour': ['14:00', '15:00', '16:00', '20:00', '21:00'],
                'Users': [450, 520, 480, 380, 420]
            })
            st.bar_chart(peak_hours.set_index('Hour'))
        
        with perf_col2:
            # Top performing models
            st.markdown("**🎯 Model Performance**")
            model_data = pd.DataFrame({
                'Model': ['NBA-AI-v3', 'NBA-AI-v2', 'Legacy'],
                'Accuracy': [78.5, 73.2, 68.1]
            })
            st.bar_chart(model_data.set_index('Model'), color='#FF8C00')
        
        with perf_col3:
            # User engagement
            st.markdown("**👥 User Engagement**")
            engagement_data = pd.DataFrame({
                'Type': ['Daily', 'Weekly', 'Monthly'],
                'Users': [850, 1100, 1250]
            })
            st.bar_chart(engagement_data.set_index('Type'), color='#00FF88')
        
        with perf_col4:
            # Error rates
            st.markdown("**⚠️ Error Rates**")
            error_data = pd.DataFrame({
                'Type': ['API', 'DB', 'Model', 'Cache'],
                'Errors': [2.1, 0.8, 1.5, 0.3]
            })
            st.bar_chart(error_data.set_index('Type'), color='#FF4B4B')
        
        # Real-time alerts and notifications
        st.markdown("---")
        st.subheader("🚨 Live System Alerts")
        
        # Simulate real-time alerts
        alert_col1, alert_col2 = st.columns(2)
        
        with alert_col1:
            st.markdown("**🔥 Active Alerts**")
            if cache_usage > 90:
                st.error(f"🚨 Cache usage critical: {cache_usage}%")
            elif cache_usage > 85:
                st.warning(f"⚠️ Cache usage high: {cache_usage}%")
            else:
                st.success("✅ All systems operational")
            
            if response_time > 180:
                st.warning(f"⚠️ High response time: {response_time}ms")
            
            if model_accuracy < 70:
                st.error(f"🚨 Model accuracy low: {model_accuracy}%")
        
        with alert_col2:
            st.markdown("**📈 Performance Trends**")
            trend_direction = "📈" if np.random.choice([True, False]) else "📉"
            trend_color = "green" if trend_direction == "📈" else "orange"
            
            st.markdown(f"Users: {trend_direction} <span style='color: {trend_color}'>+5.2%</span>", unsafe_allow_html=True)
            st.markdown(f"Predictions: {trend_direction} <span style='color: {trend_color}'>+12.8%</span>", unsafe_allow_html=True)
            st.markdown(f"Accuracy: {trend_direction} <span style='color: {trend_color}'>+2.1%</span>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        <div class="admin-section">
            <h4>👥 User Management</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize session state for user management
        if 'users_data' not in st.session_state:
            # Create realistic user database
            st.session_state.users_data = pd.DataFrame({
                'ID': range(1, 21),
                'Username': [f'user{i}' if i <= 10 else f'premium_user{i-10}' if i <= 15 else f'vip_user{i-15}' 
                           for i in range(1, 21)],
                'Email': [f'user{i}@nbapredictions.com' if i <= 10 else 
                         f'premium{i-10}@nbapredictions.com' if i <= 15 else 
                         f'vip{i-15}@nbapredictions.com' for i in range(1, 21)],
                'Role': ['User'] * 10 + ['Premium'] * 5 + ['VIP'] * 5,
                'Status': np.random.choice(['Active', 'Inactive', 'Suspended'], 20, p=[0.8, 0.15, 0.05]),
                'Last Login': [datetime.now() - timedelta(days=np.random.randint(0, 30)) for _ in range(20)],
                'Predictions': np.random.randint(5, 200, 20),
                'Join Date': [datetime.now() - timedelta(days=np.random.randint(30, 365)) for _ in range(20)],
                'Total Profit': np.random.randint(-500, 2000, 20)
            })
        
        if 'user_action_log' not in st.session_state:
            st.session_state.user_action_log = []
        
        # User search and filters
        col1, col2, col3 = st.columns(3)
        with col1:
            search_user = st.text_input("🔍 Search Users", placeholder="Username or email", key="search_users_input")
        with col2:
            user_filter = st.selectbox("📊 Filter by Status", 
                ["All Users", "Active", "Inactive", "Suspended"])
        with col3:
            role_filter = st.selectbox("👤 Filter by Role", 
                ["All Roles", "User", "Premium", "VIP", "Admin"])
        
        # Apply filters
        filtered_data = st.session_state.users_data.copy()
        
        # Search filter
        if search_user:
            mask = (filtered_data['Username'].str.contains(search_user, case=False, na=False) |
                   filtered_data['Email'].str.contains(search_user, case=False, na=False))
            filtered_data = filtered_data[mask]
        
        # Status filter
        if user_filter != "All Users":
            filtered_data = filtered_data[filtered_data['Status'] == user_filter]
        
        # Role filter
        if role_filter != "All Roles":
            filtered_data = filtered_data[filtered_data['Role'] == role_filter]
        
        # User statistics
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        
        with stats_col1:
            total_users = len(st.session_state.users_data)
            st.metric("👥 Total Users", total_users)
        
        with stats_col2:
            active_users = len(st.session_state.users_data[st.session_state.users_data['Status'] == 'Active'])
            st.metric("✅ Active Users", active_users, f"{round(active_users/total_users*100, 1)}%")
        
        with stats_col3:
            new_users_week = len(st.session_state.users_data[
                st.session_state.users_data['Join Date'] > (datetime.now() - timedelta(days=7))
            ])
            st.metric("🆕 New This Week", new_users_week)
        
        with stats_col4:
            avg_predictions = round(st.session_state.users_data['Predictions'].mean(), 1)
            st.metric("📊 Avg Predictions", avg_predictions)
        
        # User data table with selection
        st.subheader("📋 User Database")
        
        # Format the data for display
        display_data = filtered_data.copy()
        display_data['Last Login'] = display_data['Last Login'].dt.strftime('%Y-%m-%d')
        display_data['Join Date'] = display_data['Join Date'].dt.strftime('%Y-%m-%d')
        display_data['Total Profit'] = display_data['Total Profit'].apply(lambda x: f"${x:,}")
        
        # User selection
        if len(display_data) > 0:
            selected_indices = st.dataframe(
                display_data, 
                use_container_width=True,
                on_select="rerun",
                selection_mode="multi-row"
            )
            
            # Get selected users
            if hasattr(selected_indices, 'selection') and len(selected_indices.selection['rows']) > 0:
                selected_user_ids = display_data.iloc[selected_indices.selection['rows']]['ID'].tolist()
                selected_users = st.session_state.users_data[st.session_state.users_data['ID'].isin(selected_user_ids)]
                
                st.info(f"📌 Selected {len(selected_users)} user(s)")
                
                # Show selected user details
                with st.expander("👁️ View Selected Users"):
                    for _, user in selected_users.iterrows():
                        st.markdown(f"""
                        **{user['Username']}** ({user['Role']})
                        - Email: {user['Email']}
                        - Status: {user['Status']}
                        - Predictions: {user['Predictions']}
                        - Profit: ${user['Total Profit']:,}
                        """)
            else:
                selected_users = pd.DataFrame()
        else:
            st.info("No users found matching the current filters.")
            selected_users = pd.DataFrame()
        
        # User actions section
        st.markdown("---")
        st.subheader("👨‍💼 User Actions")
        
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            # Add new user
            with st.expander("➕ Add New User"):
                new_username = st.text_input("Username", key="new_username")
                new_email = st.text_input("Email", key="new_email")
                new_role = st.selectbox("Role", ["User", "Premium", "VIP"], key="new_role")
                
                if st.button("✅ Create User", use_container_width=True, key="create_user_btn"):
                    if new_username and new_email:
                        # Check if username exists
                        if new_username in st.session_state.users_data['Username'].values:
                            st.error("❌ Username already exists!")
                        else:
                            # Add new user
                            new_id = st.session_state.users_data['ID'].max() + 1
                            new_user = pd.DataFrame({
                                'ID': [new_id],
                                'Username': [new_username],
                                'Email': [new_email],
                                'Role': [new_role],
                                'Status': ['Active'],
                                'Last Login': [datetime.now()],
                                'Predictions': [0],
                                'Join Date': [datetime.now()],
                                'Total Profit': [0]
                            })
                            
                            st.session_state.users_data = pd.concat([st.session_state.users_data, new_user], ignore_index=True)
                            
                        # Log action
                        st.session_state.user_action_log.append({
                            'timestamp': datetime.now(),
                            'admin': admin_name,
                            'action': 'User Created',
                            'target': new_username,
                            'details': f"Role: {new_role}"
                        })
                        
                        st.success(f"✅ User '{new_username}' created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all required fields!")
            
            # Edit user
            with st.expander("✏️ Edit User"):
                if len(selected_users) == 1:
                    edit_user = selected_users.iloc[0]
                    
                    edit_username = st.text_input("Username", value=edit_user['Username'], key="edit_username")
                    edit_email = st.text_input("Email", value=edit_user['Email'], key="edit_email")
                    edit_role = st.selectbox("Role", ["User", "Premium", "VIP"], 
                                           index=["User", "Premium", "VIP"].index(edit_user['Role']), 
                                           key="edit_role")
                    edit_status = st.selectbox("Status", ["Active", "Inactive", "Suspended"],
                                             index=["Active", "Inactive", "Suspended"].index(edit_user['Status']),
                                             key="edit_status")
                    
                    if st.button("💾 Save Changes", use_container_width=True, key="save_user_changes"):
                        # Update user
                        user_idx = st.session_state.users_data[st.session_state.users_data['ID'] == edit_user['ID']].index[0]
                        st.session_state.users_data.loc[user_idx, 'Username'] = edit_username
                        st.session_state.users_data.loc[user_idx, 'Email'] = edit_email
                        st.session_state.users_data.loc[user_idx, 'Role'] = edit_role
                        st.session_state.users_data.loc[user_idx, 'Status'] = edit_status
                        
                        # Log action
                        st.session_state.user_action_log.append({
                            'timestamp': datetime.now(),
                            'admin': admin_name,
                            'action': 'User Updated',
                            'target': edit_username,
                            'details': f"Role: {edit_role}, Status: {edit_status}"
                        })
                        
                        st.success(f"✅ User '{edit_username}' updated successfully!")
                        st.rerun()
                else:
                    st.info("📌 Please select exactly one user to edit.")
        
        with action_col2:
            # Bulk actions
            with st.expander("📦 Bulk Actions"):
                if len(selected_users) > 0:
                    bulk_action = st.selectbox("Choose Action", [
                        "Change Status",
                        "Change Role", 
                        "Send Message",
                        "Export Data",
                        "Delete Users"
                    ])
                    
                    if bulk_action == "Change Status":
                        new_status = st.selectbox("New Status", ["Active", "Inactive", "Suspended"], key="bulk_status_select")
                        if st.button(f"🔄 Update Status for {len(selected_users)} users", use_container_width=True, key="bulk_update_status_btn"):
                            for user_id in selected_users['ID']:
                                user_idx = st.session_state.users_data[st.session_state.users_data['ID'] == user_id].index[0]
                                old_status = st.session_state.users_data.loc[user_idx, 'Status']
                                st.session_state.users_data.loc[user_idx, 'Status'] = new_status
                                
                                # Log action
                                username = st.session_state.users_data.loc[user_idx, 'Username']
                                st.session_state.user_action_log.append({
                                    'timestamp': datetime.now(),
                                    'admin': admin_name,
                                    'action': 'Status Changed',
                                    'target': username,
                                    'details': f"{old_status} → {new_status}"
                                })
                            
                            st.success(f"✅ Status updated for {len(selected_users)} users!")
                            st.rerun()
                    
                    elif bulk_action == "Change Role":
                        new_role = st.selectbox("New Role", ["User", "Premium", "VIP"], key="bulk_role_select")
                        if st.button(f"👤 Update Role for {len(selected_users)} users", use_container_width=True, key="bulk_update_role_btn"):
                            for user_id in selected_users['ID']:
                                user_idx = st.session_state.users_data[st.session_state.users_data['ID'] == user_id].index[0]
                                old_role = st.session_state.users_data.loc[user_idx, 'Role']
                                st.session_state.users_data.loc[user_idx, 'Role'] = new_role
                                
                                # Log action
                                username = st.session_state.users_data.loc[user_idx, 'Username']
                                st.session_state.user_action_log.append({
                                    'timestamp': datetime.now(),
                                    'admin': admin_name,
                                    'action': 'Role Changed',
                                    'target': username,
                                    'details': f"{old_role} → {new_role}"
                                })
                            
                            st.success(f"✅ Role updated for {len(selected_users)} users!")
                            st.rerun()
                    
                    elif bulk_action == "Send Message":
                        message_subject = st.text_input("Subject", placeholder="Important Update", key="bulk_message_subject")
                        message_body = st.text_area("Message", placeholder="Dear user...", key="bulk_message_body")
                        
                        if st.button(f"📧 Send to {len(selected_users)} users", use_container_width=True, key="bulk_send_message_btn"):
                            if message_subject and message_body:
                                # Simulate sending messages
                                with st.spinner("Sending messages..."):
                                    import time
                                    time.sleep(1)
                                
                                # Log action
                                for user_id in selected_users['ID']:
                                    username = st.session_state.users_data[st.session_state.users_data['ID'] == user_id].iloc[0]['Username']
                                    st.session_state.user_action_log.append({
                                        'timestamp': datetime.now(),
                                        'admin': admin_name,
                                        'action': 'Message Sent',
                                        'target': username,
                                        'details': f"Subject: {message_subject}"
                                    })
                                
                                st.success(f"✅ Message sent to {len(selected_users)} users!")
                            else:
                                st.error("❌ Please fill in subject and message!")
                    
                    elif bulk_action == "Export Data":
                        export_format = st.selectbox("Format", ["CSV", "Excel", "JSON"], key="export_format_select")
                        
                        if st.button(f"📥 Export {len(selected_users)} users", use_container_width=True, key="bulk_export_users_btn"):
                            # Prepare export data
                            export_data = selected_users.copy()
                            export_data['Last Login'] = export_data['Last Login'].dt.strftime('%Y-%m-%d %H:%M:%S')
                            export_data['Join Date'] = export_data['Join Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
                            
                            if export_format == "CSV":
                                csv_data = export_data.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download CSV",
                                    data=csv_data,
                                    file_name=f"users_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv",
                                    key="download_users_csv_btn"
                                )
                            
                            # Log action
                            st.session_state.user_action_log.append({
                                'timestamp': datetime.now(),
                                'admin': admin_name,
                                'action': 'Data Exported',
                                'target': f"{len(selected_users)} users",
                                'details': f"Format: {export_format}"
                            })
                            
                            st.success(f"✅ Export prepared for {len(selected_users)} users!")
                    
                    elif bulk_action == "Delete Users":
                        st.warning("⚠️ **DANGER ZONE** - This action cannot be undone!")
                        confirm_delete = st.checkbox("I understand this will permanently delete the selected users", key="confirm_bulk_delete")
                        
                        if confirm_delete and st.button(f"🗑️ DELETE {len(selected_users)} users", use_container_width=True, key="bulk_delete_users_btn"):
                            # Delete users
                            deleted_usernames = selected_users['Username'].tolist()
                            st.session_state.users_data = st.session_state.users_data[~st.session_state.users_data['ID'].isin(selected_users['ID'])]
                            
                            # Log action
                            for username in deleted_usernames:
                                st.session_state.user_action_log.append({
                                    'timestamp': datetime.now(),
                                    'admin': admin_name,
                                    'action': 'User Deleted',
                                    'target': username,
                                    'details': "Permanent deletion"
                                })
                            
                            st.error(f"🗑️ Deleted {len(selected_users)} users permanently!")
                            st.rerun()
                else:
                    st.info("📌 Select users to perform bulk actions.")
            
            # User activity log
            with st.expander("📋 Activity Log"):
                if st.session_state.user_action_log:
                    log_df = pd.DataFrame(st.session_state.user_action_log)
                    log_df['timestamp'] = log_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Show recent actions (last 10)
                    recent_log = log_df.tail(10).iloc[::-1]  # Reverse to show newest first
                    st.dataframe(recent_log, use_container_width=True)
                    
                    # Clear log option
                    if st.button("🧹 Clear Log", key="clear_activity_log_btn"):
                        st.session_state.user_action_log = []
                        st.success("✅ Activity log cleared!")
                        st.rerun()
                else:
                    st.info("No activity logged yet.")
    
    with tab3:
        st.markdown("""
        <div class="admin-section">
            <h4>🏀 Prediction Management</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize session state for predictions
        if 'predictions_data' not in st.session_state:
            # Create realistic prediction database
            teams = ['Lakers', 'Warriors', 'Celtics', 'Heat', 'Nets', '76ers', 'Bulls', 'Knicks', 
                    'Mavs', 'Suns', 'Nuggets', 'Jazz', 'Clippers', 'Blazers', 'Kings', 'Hawks']
            
            prediction_records = []
            for i in range(50):
                home_team = np.random.choice(teams)
                away_team = np.random.choice([t for t in teams if t != home_team])
                
                # Simulate realistic predictions
                confidence = round(np.random.uniform(65, 95), 1)
                predicted_winner = np.random.choice([home_team, away_team])
                actual_winner = predicted_winner if np.random.random() < (confidence/100) else (away_team if predicted_winner == home_team else home_team)
                
                prediction_records.append({
                    'ID': i + 1,
                    'Game': f"{away_team} @ {home_team}",
                    'Date': datetime.now() - timedelta(days=np.random.randint(0, 30)),
                    'Prediction': f"{predicted_winner} Win",
                    'Confidence': confidence,
                    'Actual_Result': f"{actual_winner} Won" if np.random.random() < 0.8 else "Pending",
                    'Status': 'Correct' if actual_winner == predicted_winner and np.random.random() < 0.8 else 'Incorrect' if np.random.random() < 0.8 else 'Pending',
                    'Model_Used': np.random.choice(['NBA-AI-v3', 'NBA-AI-v2', 'Legacy-Model']),
                    'User_Count': np.random.randint(50, 500),
                    'Hot_Pick': np.random.choice([True, False], p=[0.2, 0.8]),
                    'Profit_Impact': np.random.randint(-200, 800)
                })
            
            st.session_state.predictions_data = pd.DataFrame(prediction_records)
        
        if 'model_performance' not in st.session_state:
            st.session_state.model_performance = {
                'NBA-AI-v3': {'accuracy': 78.5, 'predictions': 150, 'profit': 12500},
                'NBA-AI-v2': {'accuracy': 73.2, 'predictions': 200, 'profit': 8900},
                'Legacy-Model': {'accuracy': 68.1, 'predictions': 100, 'profit': 3200}
            }
        
        if 'prediction_settings' not in st.session_state:
            st.session_state.prediction_settings = {
                'min_confidence': 65.0,
                'hot_pick_threshold': 80.0,
                'max_daily_predictions': 200,
                'auto_approve_predictions': True,
                'enable_live_updates': True
            }
        
        # Prediction metrics overview
        col1, col2, col3, col4 = st.columns(4)
        
        total_predictions = len(st.session_state.predictions_data)
        correct_predictions = len(st.session_state.predictions_data[st.session_state.predictions_data['Status'] == 'Correct'])
        pending_predictions = len(st.session_state.predictions_data[st.session_state.predictions_data['Status'] == 'Pending'])
        hot_picks = len(st.session_state.predictions_data[st.session_state.predictions_data['Hot_Pick'] == True])
        
        with col1:
            accuracy = round((correct_predictions / (total_predictions - pending_predictions)) * 100, 1) if (total_predictions - pending_predictions) > 0 else 0
            st.metric("📊 Overall Accuracy", f"{accuracy}%", f"{round(np.random.uniform(-2, 3), 1)}%")
        
        with col2:
            st.metric("📈 Total Predictions", total_predictions, f"+{np.random.randint(5, 20)}")
        
        with col3:
            st.metric("✅ Correct Predictions", correct_predictions, f"+{np.random.randint(2, 8)}")
        
        with col4:
            st.metric("🔥 Hot Picks", hot_picks, f"+{np.random.randint(1, 5)}")
        
        # Model performance comparison
        st.subheader("🤖 Model Performance Analysis")
        
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            # Model accuracy chart
            model_data = pd.DataFrame(list(st.session_state.model_performance.items()), 
                                    columns=['Model', 'Data'])
            model_data['Accuracy'] = model_data['Data'].apply(lambda x: x['accuracy'])
            model_data['Predictions'] = model_data['Data'].apply(lambda x: x['predictions'])
            model_data['Profit'] = model_data['Data'].apply(lambda x: x['profit'])
            
            st.markdown("**📊 Model Accuracy Comparison**")
            st.bar_chart(model_data.set_index('Model')[['Accuracy']], color='#00FF88')
            
            # Model management
            st.markdown("**🔧 Model Controls**")
            selected_model = st.selectbox("Select Model", list(st.session_state.model_performance.keys()), key="model_retrain_select")
            
            if st.button("🔄 Retrain Selected Model", use_container_width=True, key="retrain_model_btn"):
                with st.spinner(f"Retraining {selected_model}..."):
                    import time
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    stages = [
                        "Loading training data...",
                        "Preprocessing features...",
                        "Training neural network...",
                        "Validating model...",
                        "Optimizing parameters...",
                        "Testing accuracy...",
                        "Deploying model..."
                    ]
                    
                    for i, stage in enumerate(stages):
                        status_text.text(stage)
                        progress_bar.progress((i + 1) * 100 // len(stages))
                        time.sleep(0.5)
                    
                    # Update model performance
                    old_accuracy = st.session_state.model_performance[selected_model]['accuracy']
                    new_accuracy = round(old_accuracy + np.random.uniform(-2, 5), 1)
                    st.session_state.model_performance[selected_model]['accuracy'] = new_accuracy
                    
                    st.success(f"✅ {selected_model} retrained successfully!")
                    st.info(f"📊 Accuracy: {old_accuracy}% → {new_accuracy}% ({new_accuracy - old_accuracy:+.1f}%)")
                    st.rerun()
        
        with perf_col2:
            # Profit comparison
            st.markdown("**💰 Model Profit Impact**")
            st.bar_chart(model_data.set_index('Model')[['Profit']], color='#dfe31d')
            
            # Real-time model status
            st.markdown("**⚡ Real-Time Model Status**")
            for model, data in st.session_state.model_performance.items():
                status_color = "🟢" if data['accuracy'] > 75 else "🟡" if data['accuracy'] > 70 else "🔴"
                st.markdown(f"{status_color} **{model}**: {data['accuracy']}% | {data['predictions']} predictions")
        
        # Prediction filtering and management
        st.markdown("---")
        st.subheader("📋 Prediction Database")
        
        # Filters
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        
        with filter_col1:
            status_filter = st.selectbox("Status Filter", ["All", "Correct", "Incorrect", "Pending"], key="prediction_status_filter")
        
        with filter_col2:
            model_filter = st.selectbox("Model Filter", ["All Models"] + list(st.session_state.model_performance.keys()), key="prediction_model_filter")
        
        with filter_col3:
            hot_pick_filter = st.selectbox("Hot Picks", ["All Predictions", "Hot Picks Only", "Regular Picks"], key="prediction_hot_pick_filter")
        
        with filter_col4:
            date_range = st.selectbox("Date Range", ["All Time", "Last 7 Days", "Last 30 Days", "This Month"], key="prediction_date_range_filter")
        
        # Apply filters
        filtered_predictions = st.session_state.predictions_data.copy()
        
        if status_filter != "All":
            filtered_predictions = filtered_predictions[filtered_predictions['Status'] == status_filter]
        
        if model_filter != "All Models":
            filtered_predictions = filtered_predictions[filtered_predictions['Model_Used'] == model_filter]
        
        if hot_pick_filter == "Hot Picks Only":
            filtered_predictions = filtered_predictions[filtered_predictions['Hot_Pick'] == True]
        elif hot_pick_filter == "Regular Picks":
            filtered_predictions = filtered_predictions[filtered_predictions['Hot_Pick'] == False]
        
        if date_range != "All Time":
            days_back = {"Last 7 Days": 7, "Last 30 Days": 30, "This Month": 30}.get(date_range, 365)
            cutoff_date = datetime.now() - timedelta(days=days_back)
            filtered_predictions = filtered_predictions[filtered_predictions['Date'] >= cutoff_date]
        
        # Display predictions table
        if len(filtered_predictions) > 0:
            # Prepare display data
            display_predictions = filtered_predictions.copy()
            display_predictions['Date'] = display_predictions['Date'].dt.strftime('%Y-%m-%d')
            display_predictions['Confidence'] = display_predictions['Confidence'].apply(lambda x: f"{x}%")
            display_predictions['Hot_Pick'] = display_predictions['Hot_Pick'].apply(lambda x: "🔥" if x else "")
            display_predictions['Profit_Impact'] = display_predictions['Profit_Impact'].apply(lambda x: f"${x:,}")
            
            # Select columns to display
            display_columns = ['Game', 'Date', 'Prediction', 'Confidence', 'Status', 'Model_Used', 'Hot_Pick', 'User_Count', 'Profit_Impact']
            
            selected_predictions = st.dataframe(
                display_predictions[display_columns],
                use_container_width=True,
                on_select="rerun",
                selection_mode="multi-row"
            )
            
            st.info(f"📊 Showing {len(filtered_predictions)} of {total_predictions} predictions")
            
            # Prediction actions
            if hasattr(selected_predictions, 'selection') and len(selected_predictions.selection['rows']) > 0:
                selected_pred_indices = selected_predictions.selection['rows']
                selected_pred_data = filtered_predictions.iloc[selected_pred_indices]
                
                st.markdown("---")
                st.subheader("🎯 Prediction Actions")
                
                action_col1, action_col2, action_col3 = st.columns(3)
                
                with action_col1:
                    # Mark as Hot Pick
                    if st.button("🔥 Mark as Hot Pick", use_container_width=True, key="mark_hot_pick_btn"):
                        for idx in selected_pred_indices:
                            pred_id = filtered_predictions.iloc[idx]['ID']
                            st.session_state.predictions_data.loc[
                                st.session_state.predictions_data['ID'] == pred_id, 'Hot_Pick'
                            ] = True
                        
                        st.success(f"✅ Marked {len(selected_pred_indices)} predictions as Hot Picks!")
                        st.rerun()
                
                with action_col2:
                    # Update prediction status
                    new_status = st.selectbox("Update Status", ["Correct", "Incorrect", "Pending"], key="update_prediction_status_select")
                    if st.button("📝 Update Status", use_container_width=True, key="update_prediction_status_btn"):
                        for idx in selected_pred_indices:
                            pred_id = filtered_predictions.iloc[idx]['ID']
                            st.session_state.predictions_data.loc[
                                st.session_state.predictions_data['ID'] == pred_id, 'Status'
                            ] = new_status
                        
                        st.success(f"✅ Updated {len(selected_pred_indices)} predictions to {new_status}!")
                        st.rerun()
                
                with action_col3:
                    # Delete predictions
                    if st.button("🗑️ Delete Predictions", use_container_width=True, key="delete_predictions_btn"):
                        confirm_delete = st.checkbox("⚠️ Confirm deletion")
                        if confirm_delete:
                            for idx in selected_pred_indices:
                                pred_id = filtered_predictions.iloc[idx]['ID']
                                st.session_state.predictions_data = st.session_state.predictions_data[
                                    st.session_state.predictions_data['ID'] != pred_id
                                ]
                            
                            st.error(f"🗑️ Deleted {len(selected_pred_indices)} predictions!")
                            st.rerun()
        else:
            st.info("No predictions found matching the current filters.")
        
        # Prediction settings
        st.markdown("---")
        st.subheader("⚙️ Prediction Settings")
        
        settings_col1, settings_col2 = st.columns(2)
        
        with settings_col1:
            st.markdown("**🎯 Confidence Thresholds**")
            
            new_min_confidence = st.slider(
                "Minimum Confidence for Predictions",
                50.0, 90.0, 
                st.session_state.prediction_settings['min_confidence'],
                step=0.5
            )
            
            new_hot_pick_threshold = st.slider(
                "Hot Pick Threshold",
                70.0, 95.0,
                st.session_state.prediction_settings['hot_pick_threshold'],
                step=0.5
            )
            
            new_max_daily = st.number_input(
                "Max Daily Predictions",
                50, 500,
                st.session_state.prediction_settings['max_daily_predictions']
            )
        
        with settings_col2:
            st.markdown("**🔧 System Settings**")
            
            new_auto_approve = st.toggle(
                "Auto-approve Predictions",
                st.session_state.prediction_settings['auto_approve_predictions']
            )
            
            new_live_updates = st.toggle(
                "Enable Live Updates",
                st.session_state.prediction_settings['enable_live_updates']
            )
            
            # Prediction generation
            st.markdown("**🎲 Generate New Predictions**")
            num_predictions = st.number_input("Number of Predictions", 1, 20, 5, key="generate_predictions_count")
            
            if st.button("🎯 Generate Predictions", use_container_width=True, key="generate_predictions_btn"):
                with st.spinner("Generating new predictions..."):
                    import time
                    time.sleep(1)
                    
                    # Generate new predictions
                    teams = ['Lakers', 'Warriors', 'Celtics', 'Heat', 'Nets', '76ers']
                    new_predictions = []
                    
                    for i in range(num_predictions):
                        home_team = np.random.choice(teams)
                        away_team = np.random.choice([t for t in teams if t != home_team])
                        confidence = round(np.random.uniform(new_min_confidence, 95), 1)
                        predicted_winner = np.random.choice([home_team, away_team])
                        
                        new_pred = {
                            'ID': st.session_state.predictions_data['ID'].max() + i + 1,
                            'Game': f"{away_team} @ {home_team}",
                            'Date': datetime.now(),
                            'Prediction': f"{predicted_winner} Win",
                            'Confidence': confidence,
                            'Actual_Result': "Pending",
                            'Status': 'Pending',
                            'Model_Used': 'NBA-AI-v3',
                            'User_Count': 0,
                            'Hot_Pick': confidence >= new_hot_pick_threshold,
                            'Profit_Impact': 0
                        }
                        new_predictions.append(new_pred)
                    
                    # Add to database
                    new_df = pd.DataFrame(new_predictions)
                    st.session_state.predictions_data = pd.concat([st.session_state.predictions_data, new_df], ignore_index=True)
                    
                    st.success(f"✅ Generated {num_predictions} new predictions!")
                    st.rerun()
        
        # Save settings
        if st.button("💾 Save Prediction Settings", type="primary", use_container_width=True, key="save_prediction_settings"):
            st.session_state.prediction_settings.update({
                'min_confidence': new_min_confidence,
                'hot_pick_threshold': new_hot_pick_threshold,
                'max_daily_predictions': new_max_daily,
                'auto_approve_predictions': new_auto_approve,
                'enable_live_updates': new_live_updates
            })
            
            st.success("✅ Prediction settings saved successfully!")
            st.balloons()
        
        # Analytics and reports
        st.markdown("---")
        st.subheader("📈 Prediction Analytics")
        
        analytics_col1, analytics_col2 = st.columns(2)
        
        with analytics_col1:
            # Accuracy trend over time
            st.markdown("**📊 Accuracy Trend (Last 30 Days)**")
            
            # Generate trend data
            dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
            accuracy_trend = [round(73 + 5 * np.sin(i/5) + np.random.uniform(-3, 3), 1) for i in range(len(dates))]
            
            trend_data = pd.DataFrame({
                'Date': dates,
                'Accuracy': accuracy_trend
            })
            
            st.line_chart(trend_data.set_index('Date'), color='#00FF88')
        
        with analytics_col2:
            # Model usage distribution
            st.markdown("**🤖 Model Usage Distribution**")
            
            model_usage = st.session_state.predictions_data['Model_Used'].value_counts()
            st.bar_chart(model_usage, color='#dfe31d')
            
            # Hot picks performance
            st.markdown("**🔥 Hot Picks Performance**")
            hot_picks_data = st.session_state.predictions_data[st.session_state.predictions_data['Hot_Pick'] == True]
            if len(hot_picks_data) > 0:
                hot_picks_accuracy = len(hot_picks_data[hot_picks_data['Status'] == 'Correct']) / len(hot_picks_data[hot_picks_data['Status'] != 'Pending']) * 100 if len(hot_picks_data[hot_picks_data['Status'] != 'Pending']) > 0 else 0
                st.metric("Hot Picks Accuracy", f"{hot_picks_accuracy:.1f}%")
            else:
                st.info("No hot picks data available.")
    
    with tab4:
        st.markdown("""
        <div class="admin-section">
            <h3>⚙️ System Settings & Configuration</h3>
            <p style="color: #888; margin-bottom: 20px;">Manage application settings, feature flags, and system configuration</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Settings tabs
        settings_tab1, settings_tab2, settings_tab3, settings_tab4, settings_tab5 = st.tabs([
            "🔧 Application", "🤖 ML Models", "🔒 Security", "🎨 UI/UX", "⚡ Performance"
        ])
        
        with settings_tab1:
            st.markdown("### 🔧 Application Configuration")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🚦 System Status")
                maintenance_mode = st.toggle("🚧 Maintenance Mode", value=False, key="maintenance_mode_toggle", 
                                            help="Put the application in maintenance mode to prevent user access")
                if maintenance_mode:
                    st.warning("⚠️ Application is in maintenance mode - users cannot access the system")
                    maintenance_message = st.text_area("Maintenance Message", 
                                                      value="System is temporarily unavailable for maintenance. Please check back later.",
                                                      key="maintenance_message", height=100)
                
                debug_mode = st.toggle("🐛 Debug Mode", value=False, key="debug_mode_toggle",
                                     help="Enable debug mode for detailed logging")
                
                st.markdown("#### 👥 User Access")
                new_registrations = st.toggle("👥 Allow New Registrations", value=True, key="new_registrations_toggle",
                                             help="Allow new users to register for accounts")
                guest_access = st.toggle("👤 Allow Guest Access", value=True, key="guest_access_toggle",
                                        help="Allow users to browse without logging in")
                email_verification = st.toggle("📧 Require Email Verification", value=True, key="email_verification_toggle",
                                              help="Require email verification for new accounts")
            
            with col2:
                st.markdown("#### 🎯 Feature Flags")
                hot_picks = st.toggle("🔥 Hot Picks Feature", value=True, key="hot_picks_feature_toggle",
                                    help="Enable the hot picks recommendation system")
                profit_calculator = st.toggle("💰 Profit Calculator", value=True, key="profit_calculator_toggle",
                                             help="Enable profit calculation tools for users")
                notifications = st.toggle("🔔 Push Notifications", value=True, key="notifications_toggle",
                                         help="Enable push notifications for users")
                live_scores = st.toggle("📺 Live Scores", value=True, key="live_scores_toggle",
                                      help="Enable live score updates")
                social_features = st.toggle("👥 Social Features", value=False, key="social_features_toggle",
                                           help="Enable user comments and social interactions")
                
                st.markdown("#### 📊 Analytics")
                user_tracking = st.toggle("📈 User Analytics", value=True, key="user_tracking_toggle",
                                         help="Track user behavior for analytics")
                performance_monitoring = st.toggle("⚡ Performance Monitoring", value=True, key="performance_monitoring_toggle",
                                                  help="Monitor application performance metrics")
        
        with settings_tab2:
            st.markdown("### 🤖 Machine Learning & Prediction Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Model Configuration")
                model_confidence = st.slider("📊 Minimum Confidence Threshold", 0.5, 0.95, 0.65, 
                                            key="model_confidence_slider", step=0.05,
                                            help="Minimum confidence required for predictions to be shown")
                hot_picks_threshold = st.slider("🔥 Hot Picks Threshold", 0.7, 0.95, 0.8, 
                                               key="hot_picks_threshold_slider", step=0.05,
                                               help="Confidence threshold for hot pick recommendations")
                max_predictions = st.number_input("📈 Max Daily Predictions", 50, 500, 200, key="max_predictions_input",
                                                help="Maximum number of predictions generated per day")
                
                st.markdown("#### 🔄 Model Updates")
                auto_retrain = st.toggle("🔄 Auto-Retrain Models", value=True, key="auto_retrain_toggle",
                                       help="Automatically retrain models with new data")
                retrain_frequency = st.selectbox("🕐 Retrain Frequency", 
                                                ["Daily", "Weekly", "Monthly"], 
                                                index=1, key="retrain_frequency_select")
                model_validation = st.toggle("✅ Model Validation", value=True, key="model_validation_toggle",
                                            help="Validate model performance before deployment")
            
            with col2:
                st.markdown("#### 🎯 Prediction Settings")
                prediction_types = st.multiselect("🏀 Prediction Types", 
                                                 ["Game Winner", "Point Spread", "Total Points", "Player Performance"],
                                                 default=["Game Winner", "Point Spread"],
                                                 key="prediction_types_multiselect")
                
                early_predictions = st.toggle("⏰ Early Predictions", value=True, key="early_predictions_toggle",
                                             help="Generate predictions early (24 hours before games)")
                
                st.markdown("#### 📡 Data Sources")
                primary_data_source = st.selectbox("📊 Primary Data Source",
                                                  ["NBA API", "ESPN API", "Custom Feed"],
                                                  key="primary_data_source_select")
                backup_data_source = st.selectbox("🔄 Backup Data Source",
                                                 ["ESPN API", "NBA API", "Manual Entry"],
                                                 key="backup_data_source_select")
                data_refresh_interval = st.number_input("🔄 Data Refresh (minutes)", 5, 60, 15, 
                                                       key="data_refresh_interval")
        
        with settings_tab3:
            st.markdown("### 🔒 Security & Privacy Settings")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔐 Authentication")
                session_timeout = st.number_input("⏱️ Session Timeout (hours)", 1, 24, 8, key="session_timeout")
                two_factor_auth = st.toggle("🔐 Two-Factor Authentication", value=False, key="two_factor_toggle",
                                           help="Require 2FA for admin accounts")
                password_complexity = st.toggle("🔒 Strong Password Requirements", value=True, key="password_complexity_toggle")
                
                st.markdown("#### 🛡️ Access Control")
                max_login_attempts = st.number_input("🚫 Max Login Attempts", 3, 10, 5, key="max_login_attempts")
                ip_whitelist = st.toggle("🌐 IP Whitelist", value=False, key="ip_whitelist_toggle",
                                       help="Restrict access to specific IP addresses")
                if ip_whitelist:
                    allowed_ips = st.text_area("Allowed IP Addresses (one per line)", 
                                             placeholder="192.168.1.1\n10.0.0.1", 
                                             key="allowed_ips_textarea")
            
            with col2:
                st.markdown("#### 🔍 Data Privacy")
                data_encryption = st.toggle("🔐 Data Encryption", value=True, key="data_encryption_toggle",
                                           help="Encrypt sensitive user data")
                anonymize_analytics = st.toggle("🕶️ Anonymize Analytics", value=True, key="anonymize_analytics_toggle",
                                               help="Remove personal identifiers from analytics data")
                gdpr_compliance = st.toggle("🇪🇺 GDPR Compliance Mode", value=True, key="gdpr_compliance_toggle")
                
                st.markdown("#### 📋 Audit & Logging")
                audit_logging = st.toggle("📝 Audit Logging", value=True, key="audit_logging_toggle",
                                         help="Log all admin actions for security auditing")
                log_retention = st.number_input("📅 Log Retention (days)", 30, 365, 90, key="log_retention_days")
                security_alerts = st.toggle("🚨 Security Alerts", value=True, key="security_alerts_toggle",
                                           help="Send alerts for security events")
        
        with settings_tab4:
            st.markdown("### 🎨 User Interface & Experience")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎨 Theme & Appearance")
                default_theme = st.selectbox("🌓 Default Theme", 
                                           ["Dark", "Light", "Auto"],
                                           index=0, key="default_theme_select")
                accent_color = st.selectbox("🎨 Accent Color",
                                          ["Orange", "Blue", "Green", "Purple", "Red"],
                                          key="accent_color_select")
                
                compact_mode = st.toggle("📱 Compact Mode", value=False, key="compact_mode_toggle",
                                        help="Use compact layout for smaller screens")
                animations = st.toggle("✨ UI Animations", value=True, key="animations_toggle",
                                      help="Enable smooth animations and transitions")
                
                st.markdown("#### 🌐 Localization")
                default_language = st.selectbox("🗣️ Default Language",
                                               ["English", "Spanish", "French", "German"],
                                               key="default_language_select")
                timezone = st.selectbox("🕐 Default Timezone",
                                       ["UTC", "EST", "PST", "CST", "MST"],
                                       index=1, key="default_timezone_select")
            
            with col2:
                st.markdown("#### 📊 Dashboard Layout")
                default_dashboard = st.selectbox("🏠 Default Dashboard View",
                                                ["Overview", "Hot Picks", "My Predictions", "Analytics"],
                                                key="default_dashboard_select")
                cards_per_row = st.slider("📋 Cards per Row", 1, 4, 3, key="cards_per_row_slider")
                show_tooltips = st.toggle("💬 Show Help Tooltips", value=True, key="show_tooltips_toggle")
                
                st.markdown("#### 📱 Mobile Settings")
                mobile_sidebar = st.toggle("📱 Mobile Sidebar", value=True, key="mobile_sidebar_toggle",
                                          help="Show sidebar on mobile devices")
                mobile_notifications = st.toggle("📳 Mobile Push Notifications", value=True, key="mobile_notifications_toggle")
                responsive_tables = st.toggle("📊 Responsive Tables", value=True, key="responsive_tables_toggle")
        
        with settings_tab5:
            st.markdown("### ⚡ Performance & System Resources")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 💾 Data & Storage")
                retention_days = st.number_input("📅 Data Retention (days)", 30, 365, 90, key="retention_days_input",
                                                help="How long to keep user data and predictions")
                backup_frequency = st.selectbox("💾 Backup Frequency", 
                                               ["Daily", "Weekly", "Monthly"], 
                                               key="backup_frequency_select")
                auto_cleanup = st.toggle("🧹 Auto Cleanup", value=True, key="auto_cleanup_toggle",
                                       help="Automatically remove old data based on retention policy")
                
                st.markdown("#### 🚀 Caching")
                enable_caching = st.toggle("⚡ Enable Caching", value=True, key="enable_caching_toggle")
                cache_duration = st.number_input("⏱️ Cache Duration (hours)", 1, 24, 6, key="cache_duration")
                max_cache_size = st.number_input("💾 Max Cache Size (MB)", 100, 1000, 500, key="max_cache_size")
            
            with col2:
                st.markdown("#### 🔄 API & Requests")
                api_rate_limit = st.number_input("🚦 API Rate Limit (req/min)", 10, 1000, 100, key="api_rate_limit")
                request_timeout = st.number_input("⏱️ Request Timeout (seconds)", 5, 60, 30, key="request_timeout")
                max_concurrent_users = st.number_input("👥 Max Concurrent Users", 50, 1000, 200, key="max_concurrent_users")
                
                st.markdown("#### 📊 Monitoring")
                health_check_interval = st.number_input("❤️ Health Check Interval (minutes)", 1, 60, 5, key="health_check_interval")
                alert_thresholds = st.slider("🚨 Alert CPU Threshold (%)", 50, 95, 80, key="cpu_threshold_slider")
                memory_threshold = st.slider("🧠 Alert Memory Threshold (%)", 50, 95, 85, key="memory_threshold_slider")
        
        # Settings action buttons
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save All Settings", type="primary", use_container_width=True, key="save_all_settings"):
                # Save all settings to session state or database
                settings_data = {
                    "maintenance_mode": maintenance_mode,
                    "new_registrations": new_registrations,
                    "guest_access": guest_access,
                    "hot_picks": hot_picks,
                    "profit_calculator": profit_calculator,
                    "notifications": notifications,
                    "model_confidence": model_confidence,
                    "hot_picks_threshold": hot_picks_threshold,
                    "max_predictions": max_predictions,
                    "retention_days": retention_days,
                    "backup_frequency": backup_frequency,
                    # Add all other settings...
                }
                
                # In a real app, save to database
                st.session_state.system_settings = settings_data
                st.success("✅ All settings saved successfully!")
                st.balloons()
        
        with col2:
            if st.button("🔄 Reset to Defaults", use_container_width=True, key="reset_settings"):
                st.warning("⚠️ This will reset all settings to default values!")
                if st.button("✅ Confirm Reset", key="confirm_reset_settings"):
                    st.success("✅ Settings reset to defaults!")
                    st.rerun()
        
        with col3:
            if st.button("📤 Export Config", use_container_width=True, key="export_config"):
                import json
                config_data = {
                    "exported_at": datetime.now().isoformat(),
                    "version": "1.0",
                    "settings": {
                        "maintenance_mode": maintenance_mode,
                        "model_confidence": model_confidence,
                        # Add all settings...
                    }
                }
                
                st.download_button(
                    label="📥 Download Config File",
                    data=json.dumps(config_data, indent=2),
                    file_name=f"nba_predictions_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key="download_config_btn"
                )
                st.success("✅ Configuration exported!")
        
        with col4:
            uploaded_config = st.file_uploader("📤 Import Config", type=['json'], key="import_config_uploader")
            if uploaded_config:
                if st.button("📥 Import Settings", use_container_width=True, key="import_settings"):
                    try:
                        import json
                        config_data = json.load(uploaded_config)
                        st.success("✅ Configuration imported successfully!")
                        st.info("🔄 Please save settings to apply changes.")
                    except Exception as e:
                        st.error(f"❌ Error importing config: {str(e)}")
        
        # Settings summary
        st.markdown("---")
        st.markdown("### 📋 Current Configuration Summary")
        
        summary_col1, summary_col2, summary_col3 = st.columns(3)
        
        with summary_col1:
            st.metric("🚦 Maintenance Mode", "Active" if maintenance_mode else "Inactive")
            st.metric("👥 User Registration", "Enabled" if new_registrations else "Disabled")
            st.metric("🔥 Hot Picks", "Enabled" if hot_picks else "Disabled")
        
        with summary_col2:
            st.metric("📊 Confidence Threshold", f"{model_confidence:.0%}")
            st.metric("📈 Max Daily Predictions", f"{max_predictions}")
            st.metric("💾 Data Retention", f"{retention_days} days")
        
        with summary_col3:
            st.metric("🔔 Notifications", "Enabled" if notifications else "Disabled")
            st.metric("💰 Profit Calculator", "Enabled" if profit_calculator else "Disabled")
            st.metric("💾 Backup Frequency", backup_frequency)
    
    with tab5:
        st.markdown("""
        <div class="admin-section">
            <h4>📈 Reports & Monitoring</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Report generation
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Generate Reports")
            
            report_type = st.selectbox("📋 Report Type", [
                "User Activity Report",
                "Prediction Performance Report", 
                "Revenue Report",
                "System Health Report",
                "Custom Report"
            ], key="report_type_select")
            
            date_range = st.date_input("📅 Date Range", 
                value=[date.today() - timedelta(days=7), date.today()], key="report_date_range")
            
            report_format = st.selectbox("📁 Format", ["PDF", "Excel", "CSV"], key="report_format_select")
            
            if st.button("📄 Generate Report", type="primary", use_container_width=True, key="generate_report_btn"):
                st.success(f"✅ {report_type} generated successfully!")
                st.download_button(
                    label="📥 Download Report",
                    data="Sample report data...",
                    file_name=f"nba_predictions_{report_type.lower().replace(' ', '_')}.{report_format.lower()}",
                    mime="application/octet-stream",
                    key="download_report_btn"
                )
        
        with col2:
            st.subheader("📋 Activity Logs")
            
            log_data = pd.DataFrame({
                'Timestamp': ['2025-08-10 09:30:25', '2025-08-10 09:25:10', '2025-08-10 09:20:45'],
                'User': ['admin', 'user1', 'demo_user'],
                'Action': ['Settings Updated', 'Login', 'Prediction Made'],
                'Details': ['Model threshold changed', 'Successful login', 'Lakers vs Warriors'],
                'IP': ['192.168.1.100', '192.168.1.105', '192.168.1.110']
            })
            
            st.dataframe(log_data, use_container_width=True)
            
            # Log filters
            st.subheader("🔍 Log Filters")
            log_level = st.selectbox("📊 Log Level", ["All", "Info", "Warning", "Error"])
            log_user = st.text_input("👤 Filter by User", placeholder="Username")
        
        # System monitoring alerts
        st.subheader("🚨 System Alerts")
        
        alert_col1, alert_col2, alert_col3 = st.columns(3)
        
        with alert_col1:
            st.info("ℹ️ **Info**: Daily backup completed successfully")
        
        with alert_col2:
            st.warning("⚠️ **Warning**: Cache usage at 89% - consider clearing")
        
        with alert_col3:
            st.error("🚨 **Error**: Failed login attempts detected (3x)")
    
    # Footer with admin quick actions
    st.markdown("---")
    st.markdown("### 🚀 Quick Actions")
    
    quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
    
    with quick_col1:
        if st.button("🔄 Restart Services", use_container_width=True, key="restart_services_btn"):
            with st.spinner("Restarting services..."):
                # Simulate service restart
                import time
                time.sleep(2)
                
                # Show progress
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                st.success("✅ All services restarted successfully!")
                st.balloons()
                
                # Log the action
                st.info(f"🕐 Action logged: Services restarted by {admin_name} at {datetime.now().strftime('%H:%M:%S')}")
    
    with quick_col2:
        if st.button("💾 Backup Database", use_container_width=True, key="backup_database_btn"):
            with st.spinner("Creating database backup..."):
                # Simulate backup process
                import time
                time.sleep(1.5)
                
                # Show backup progress
                backup_progress = st.progress(0)
                backup_status = st.empty()
                
                stages = [
                    "Connecting to database...",
                    "Analyzing data structure...", 
                    "Copying user data...",
                    "Copying prediction data...",
                    "Compressing backup file...",
                    "Verifying backup integrity...",
                    "Backup completed!"
                ]
                
                for i, stage in enumerate(stages):
                    backup_status.text(stage)
                    backup_progress.progress((i + 1) * 100 // len(stages))
                    time.sleep(0.3)
                
                backup_size = round(np.random.uniform(1.2, 3.8), 1)
                backup_filename = f"nba_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
                
                st.success(f"✅ Database backup completed!")
                st.info(f"📁 Backup file: {backup_filename} ({backup_size}GB)")
                st.info(f"🕐 Backup created by {admin_name} at {datetime.now().strftime('%H:%M:%S')}")
                
                # Provide download button (simulation)
                st.download_button(
                    label="📥 Download Backup",
                    data=f"-- NBA Predictions Database Backup\n-- Created: {datetime.now()}\n-- User: {user['name']}\n-- Size: {backup_size}GB",
                    file_name=backup_filename,
                    mime="application/sql",
                    key="download_backup_btn"
                )
    
    with quick_col3:
        if st.button("🧹 Clear Cache", use_container_width=True, key="clear_cache_btn"):
            # Cache clearing with confirmation
            cache_types = st.multiselect(
                "Select cache types to clear:",
                ["User Sessions", "Prediction Cache", "Model Cache", "Static Files", "Database Query Cache"],
                default=["User Sessions", "Prediction Cache"],
                key="cache_types_multiselect"
            )
            
            if cache_types:
                confirm_clear = st.checkbox("⚠️ I confirm I want to clear the selected caches", key="confirm_clear_cache")
                
                if confirm_clear:
                    with st.spinner("Clearing cache..."):
                        import time
                        
                        clear_progress = st.progress(0)
                        clear_status = st.empty()
                        
                        for i, cache_type in enumerate(cache_types):
                            clear_status.text(f"Clearing {cache_type}...")
                            clear_progress.progress((i + 1) * 100 // len(cache_types))
                            time.sleep(0.5)
                        
                        # Calculate freed space
                        freed_space = round(sum([np.random.uniform(50, 500) for _ in cache_types]), 1)
                        
                        st.success(f"✅ Cache cleared successfully!")
                        st.info(f"💾 Freed up {freed_space}MB of space")
                        st.info(f"🕐 Cache cleared by {admin_name} at {datetime.now().strftime('%H:%M:%S')}")
                        
                        # Show new cache status
                        new_cache_usage = max(20, np.random.randint(20, 60))
                        st.metric("📊 New Cache Usage", f"{new_cache_usage}%", f"-{100-new_cache_usage}%")
    
    with quick_col4:
        # Send Announcement - Phase 2 placeholder
        if st.button("📧 Send Announcement", use_container_width=True, key="send_announcement_btn"):
            st.info("📝 **Phase 2 Feature**")
            st.markdown("""
            The **Send Announcement** feature will be implemented in Phase 2 and will include:
            
            - 📧 **Email notifications** to all users
            - 📱 **In-app notifications** system
            - 🎯 **Targeted messaging** by user groups
            - 📊 **Delivery tracking** and analytics
            - 📝 **Template management** for common announcements
            
            *Coming soon in the next development phase!*
            """)
            
            # Show placeholder form
            with st.expander("📋 Preview - Announcement Form"):
                st.text_input("📧 Subject", placeholder="Important NBA Predictions Update", key="announcement_subject")
                st.text_area("📝 Message", placeholder="Dear users, we have an important update...", key="announcement_message")
                st.multiselect("👥 Send to", ["All Users", "Premium Users", "Admin Users", "New Users"], key="announcement_recipients")
                st.selectbox("📱 Delivery Method", ["Email + In-App", "Email Only", "In-App Only"], key="announcement_delivery_method")
                st.button("📤 Send Announcement (Phase 2)", disabled=True, key="send_announcement_phase2_btn")
    
    # System status summary
    st.markdown("---")
    st.markdown("### 📋 Quick System Summary")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.markdown("**🔧 System Status**")
        system_health = np.random.choice(["Excellent", "Good", "Fair"], p=[0.6, 0.3, 0.1])
        health_color = {"Excellent": "green", "Good": "orange", "Fair": "red"}[system_health]
        st.markdown(f"Health: <span style='color: {health_color}'>{system_health}</span>", unsafe_allow_html=True)
        st.markdown(f"Uptime: {round(np.random.uniform(99.5, 99.9), 1)}%")
        st.markdown(f"Active Users: {np.random.randint(800, 1200)}")
    
    with summary_col2:
        st.markdown("**⚡ Performance**")
        st.markdown(f"Response Time: {np.random.randint(100, 200)}ms")
        st.markdown(f"CPU Usage: {np.random.randint(20, 80)}%")
        st.markdown(f"Memory Usage: {np.random.randint(40, 85)}%")
    
    with summary_col3:
        st.markdown("**📊 Today's Stats**")
        st.markdown(f"New Users: +{np.random.randint(15, 35)}")
        st.markdown(f"Predictions: +{np.random.randint(120, 180)}")
        st.markdown(f"Model Accuracy: {round(np.random.uniform(70, 85), 1)}%")

def main():
    """Main application function with authentication and routing"""
    
    # Debug info (remove in production)
    st.sidebar.info(f"Enhanced Dashboard Available: {ENHANCED_DASHBOARD_AVAILABLE}")
    if ENHANCED_DASHBOARD_AVAILABLE:
        st.sidebar.success(f"Enhanced Dashboard Function: {enhanced_dashboard_main}")
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Check authentication status
    if not is_authenticated():
        show_login_form()
        return
    
    # User is authenticated, show header and appropriate dashboard
    show_user_header()
    
    user = get_current_user()
    if user:
        if user["role"] == "admin":
            show_admin_dashboard(user)
        else:
            show_user_dashboard(user)

if __name__ == "__main__":
    main()
