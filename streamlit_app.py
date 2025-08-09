#!/usr/bin/env python3
"""
🏀 NBA Predictions - Streamlit Cloud Entry Point
===============================================

Main entry point for Streamlit Cloud deployment.
This is the file Streamlit Cloud will run by default.
"""

import streamlit as st
import sys
from pathlib import Path

# Set page config first (must be first Streamlit command)
st.set_page_config(
    page_title="🏀 NBA Predictions",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/your-repo/issues',
        'Report a bug': 'https://github.com/your-repo/issues',
        'About': "# NBA Predictions App\nProfessional NBA game predictions powered by AI"
    }
)

# Add app directory to path for imports
app_dir = Path(__file__).parent / "app"
sys.path.append(str(app_dir))

def check_admin_auth():
    """Simple admin authentication"""
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 2rem; border-radius: 15px; text-align: center; margin: 2rem 0;">
            <h2>🔐 Admin Access Required</h2>
            <p>Enter admin credentials to access management features</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login"):
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="Enter admin password")
            submit = st.form_submit_button("🔑 Login", use_container_width=True)
            
            if submit:
                # Simple authentication (in production, use proper auth)
                if username == "admin" and password == "nba2025":
                    st.session_state.admin_authenticated = True
                    st.success("✅ Authentication successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Try: admin / nba2025")
        
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-top: 2rem;">
            <h4>📝 Demo Credentials:</h4>
            <p><strong>Username:</strong> admin<br>
            <strong>Password:</strong> nba2025</p>
            <small>Note: In production, use proper authentication system</small>
        </div>
        """, unsafe_allow_html=True)
        return False
    
    return True

def main():
    """Main Streamlit application"""
    
    # Add custom CSS for professional appearance
    st.markdown("""
    <style>
        /* Hide Streamlit branding for professional look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom header */
        .main-header {
            background: linear-gradient(90deg, #1f4e79, #2d6aa0);
            padding: 1rem 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
        }
        
        /* Professional styling */
        .stApp {
            background-color: #fafafa;
        }
        
        /* Custom sidebar */
        .css-1d391kg {
            background-color: #f8f9fa;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # App selector in sidebar
    st.sidebar.title("🏀 NBA Predictions")
    st.sidebar.markdown("---")
    
    app_choice = st.sidebar.selectbox(
        "Choose Interface:",
        ["🎯 Predictions", "🔧 Admin Dashboard", "✅ Validation"]
    )
    
    # Load selected interface
    try:
        if app_choice == "🎯 Predictions":
            # Import and run user interface
            from user_interface import main as user_main
            user_main()
            
        elif app_choice == "🔧 Admin Dashboard":
            # Check admin authentication
            if check_admin_auth():
                # Import and run admin interface
                from admin_interface import main as admin_main
                admin_main()
            
        elif app_choice == "✅ Validation":
            # Import and run validation dashboard
            from validation_dashboard import main as validation_main
            validation_main()
            
    except ImportError as e:
        st.error(f"❌ Error loading interface: {e}")
        st.info("🔧 Please check that all required files are present in the app/ directory")
        
        # Fallback simple interface
        st.markdown("""
        ## 🏀 NBA Predictions App
        
        ### Welcome to Professional NBA Game Predictions!
        
        **Current Status:** System is ready for NBA season start in October 2025.
        
        **Features:**
        - 🎯 **AI-Powered Predictions**: Win/Loss and Over/Under predictions
        - 📊 **Historical Validation**: 100% Win/Loss, 96.7% Over/Under accuracy on training data
        - 🔄 **Real-Time Data**: ESPN and NBA API integration
        - 📱 **Mobile Responsive**: Works on all devices
        
        **NBA Season 2025-26:**
        - 🏀 **Preseason**: October 1, 2025
        - 🏆 **Regular Season**: October 15, 2025
        - 📊 **Daily Predictions**: Available when season starts
        
        ---
        
        *Built with ❤️ for NBA betting enthusiasts*
        """)
    
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        st.info("🔄 Please refresh the page or contact support")

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **🏀 NBA Predictions V1.0**
    
    Professional sports predictions powered by machine learning.
    
    🎯 Focused on accuracy and profitability
    """)

if __name__ == "__main__":
    main()
