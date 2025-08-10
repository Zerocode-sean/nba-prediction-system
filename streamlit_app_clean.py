#!/usr/bin/env python3
"""
🏀 NBA Predictions - Main Application Entry Point
===============================================

Streamlit Cloud entry point with authentication and role-based routing.
Routes users to appropriate dashboards based on their role.
"""

import streamlit as st
import sys
from pathlib import Path

# Set page config first (must be first Streamlit command)
st.set_page_config(
    page_title="🏀 NBA Predictions",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add app directory to path for imports
app_dir = Path(__file__).parent / "app"
sys.path.append(str(app_dir))

try:
    from auth_system import main as auth_main
    from user_dashboard import main as user_dashboard_main
    from admin_dashboard import main as admin_dashboard_main
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error("Please ensure all required files are present in the app directory")
    st.stop()

def main():
    """Main application function with authentication and routing"""
    
    # Handle authentication
    user = auth_main()
    
    if user is None:
        # User not authenticated, auth_main() handles the login form
        return
    
    # User is authenticated, route to appropriate dashboard
    if user["role"] == "admin":
        # Route to admin dashboard
        admin_dashboard_main(user)
    else:
        # Route to user dashboard
        user_dashboard_main(user)

if __name__ == "__main__":
    main()
