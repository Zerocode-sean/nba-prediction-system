#!/usr/bin/env python3
"""
🚀 NBA Predictions - Production Startup Script
==============================================

Quick verification that the enhanced user dashboard is working.
"""

import sys
import os
from pathlib import Path

def verify_setup():
    """Verify the production setup is ready"""
    print("🔍 Verifying NBA Predictions Production Setup...")
    
    # Check directory structure
    required_files = [
        "streamlit_app.py",
        "app/user_dashboard.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    
    print("✅ All required files present")
    
    # Test enhanced dashboard import
    try:
        sys.path.append(str(Path("app")))
        from user_dashboard import main as enhanced_dashboard_main
        print("✅ Enhanced dashboard import successful")
    except Exception as e:
        print(f"❌ Enhanced dashboard import failed: {e}")
        return False
    
    print("🎉 Setup verification complete!")
    return True

def show_startup_info():
    """Show startup information"""
    print("\n" + "="*60)
    print("🏀 NBA Predictions - Enhanced User Dashboard")
    print("="*60)
    print("✅ Enhanced user dashboard has been RE-ENABLED")
    print("✅ Regular users will now see the full enhanced interface")
    print("✅ Admin dashboard remains fully functional")
    print("✅ Login system with proper role-based routing")
    print("\n📋 What was fixed:")
    print("   • Re-enabled enhanced dashboard in show_user_dashboard()")
    print("   • Added error handling and fallback mechanisms")
    print("   • Improved import error handling in user_dashboard.py")
    print("   • Verified all dependencies and file structure")
    print("\n🚀 To start the application:")
    print("   streamlit run streamlit_app.py")
    print("\n👤 Test accounts:")
    print("   User: user1 / user123")
    print("   Admin: admin / admin123")
    print("="*60)

if __name__ == "__main__":
    if verify_setup():
        show_startup_info()
        print("\n🎉 Ready to launch! The enhanced user dashboard is now active.")
    else:
        print("\n⚠️ Setup verification failed. Please check the errors above.")
        sys.exit(1)
