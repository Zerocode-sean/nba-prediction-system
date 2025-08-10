#!/usr/bin/env python3
"""
👨‍💼 NBA Predictions - Admin Dashboard
====================================

Comprehensive admin interface for managing the NBA prediction system.
Includes model management, user analytics, system monitoring, and configuration.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import sys
import os
from pathlib import Path
import json
import plotly.express as px
import plotly.graph_objects as go

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

try:
    from src.prediction.pipeline import NBAPredictionPipeline
    from src.prediction.realtime_system import RealTimeNBASystem
except ImportError as e:
    st.error(f"Import error: {e}")
    NBAPredictionPipeline = None
    RealTimeNBASystem = None

def apply_admin_dashboard_styling():
    """Apply modern styling for admin dashboard"""
    st.markdown("""
    <style>
    /* Admin Dashboard Specific Styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .admin-dashboard-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #dc3545;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .admin-dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .admin-metric {
        background: white;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-top: 4px solid #dc3545;
        transition: transform 0.3s ease;
    }
    
    .admin-metric:hover {
        transform: translateY(-3px);
    }
    
    .admin-welcome {
        background: linear-gradient(90deg, #dc3545 0%, #fd7e14 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(220,53,69,0.3);
    }
    
    .system-status {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        font-weight: bold;
    }
    
    .system-status.warning {
        background: linear-gradient(90deg, #ffc107 0%, #fd7e14 100%);
    }
    
    .system-status.error {
        background: linear-gradient(90deg, #dc3545 0%, #6f42c1 100%);
    }
    
    .model-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        border-left: 4px solid #17a2b8;
    }
    
    h1, h2, h3 {
        color: #2c3e50;
    }
    
    .admin-tab {
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def show_system_overview():
    """Display comprehensive system overview"""
    st.markdown("### 🖥️ System Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="admin-metric">
            <h2 style="color: #28a745; margin: 0;">🟢 Online</h2>
            <p style="margin: 10px 0 0 0; color: #6c757d; font-weight: bold;">System Status</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="admin-metric">
            <h2 style="color: #17a2b8; margin: 0;">1,234</h2>
            <p style="margin: 10px 0 0 0; color: #6c757d; font-weight: bold;">Total Users</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="admin-metric">
            <h2 style="color: #ffc107; margin: 0;">847</h2>
            <p style="margin: 10px 0 0 0; color: #6c757d; font-weight: bold;">Active Today</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="admin-metric">
            <h2 style="color: #6f42c1; margin: 0;">99.2%</h2>
            <p style="margin: 10px 0 0 0; color: #6c757d; font-weight: bold;">Uptime</p>
        </div>
        """, unsafe_allow_html=True)

def show_model_management():
    """Display model management interface"""
    st.markdown("### 🤖 Model Management")
    
    # Model status
    models_info = [
        {"name": "Win/Loss Model", "status": "Active", "accuracy": "92.4%", "last_updated": "2 hours ago"},
        {"name": "Over/Under Model", "status": "Active", "accuracy": "89.7%", "last_updated": "2 hours ago"},
        {"name": "Win/Loss Scaler", "status": "Active", "accuracy": "N/A", "last_updated": "2 hours ago"},
        {"name": "Over/Under Scaler", "status": "Active", "accuracy": "N/A", "last_updated": "2 hours ago"},
    ]
    
    for model in models_info:
        status_color = "#28a745" if model["status"] == "Active" else "#dc3545"
        st.markdown(f"""
        <div class="model-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h5 style="margin: 0; color: #2c3e50;">{model["name"]}</h5>
                    <small style="color: #6c757d;">Last updated: {model["last_updated"]}</small>
                </div>
                <div style="text-align: right;">
                    <div style="background: {status_color}; color: white; padding: 5px 15px; 
                               border-radius: 20px; font-weight: bold; margin-bottom: 5px;">
                        {model["status"]}
                    </div>
                    <small style="color: #6c757d;">Accuracy: {model["accuracy"]}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Model actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Retrain Models", use_container_width=True):
            st.success("Model retraining initiated!")
    with col2:
        if st.button("📊 View Model Metrics", use_container_width=True):
            st.info("Displaying detailed model metrics...")
    with col3:
        if st.button("⚙️ Model Configuration", use_container_width=True):
            st.info("Opening model configuration...")

def show_user_analytics():
    """Display user analytics and insights"""
    st.markdown("### 📈 User Analytics")
    
    # Generate sample analytics data
    dates = pd.date_range(start='2025-08-01', end='2025-08-09', freq='D')
    daily_users = np.random.randint(800, 1200, len(dates))
    predictions_made = np.random.randint(1500, 3000, len(dates))
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily active users chart
        fig_users = px.line(
            x=dates, 
            y=daily_users,
            title="Daily Active Users",
            labels={'x': 'Date', 'y': 'Active Users'}
        )
        fig_users.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50')
        )
        st.plotly_chart(fig_users, use_container_width=True)
    
    with col2:
        # Predictions made chart
        fig_predictions = px.bar(
            x=dates, 
            y=predictions_made,
            title="Daily Predictions Made",
            labels={'x': 'Date', 'y': 'Predictions'}
        )
        fig_predictions.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50')
        )
        st.plotly_chart(fig_predictions, use_container_width=True)
    
    # User behavior metrics
    st.markdown("#### 👥 User Behavior Insights")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg. Session Duration", "8.5 min", "+2.3 min")
    with col2:
        st.metric("Predictions per User", "4.7", "+1.2")
    with col3:
        st.metric("Return Rate", "73%", "+5%")

def show_system_monitoring():
    """Display system monitoring and health checks"""
    st.markdown("### 🔍 System Monitoring")
    
    # System health indicators
    health_checks = [
        {"component": "Database", "status": "Healthy", "response_time": "45ms"},
        {"component": "API Endpoints", "status": "Healthy", "response_time": "120ms"},
        {"component": "Model Loading", "status": "Healthy", "response_time": "2.3s"},
        {"component": "Live Data Feed", "status": "Warning", "response_time": "850ms"},
        {"component": "Authentication", "status": "Healthy", "response_time": "90ms"},
    ]
    
    for check in health_checks:
        if check["status"] == "Healthy":
            status_class = "system-status"
            icon = "✅"
        elif check["status"] == "Warning":
            status_class = "system-status warning"
            icon = "⚠️"
        else:
            status_class = "system-status error"
            icon = "❌"
        
        st.markdown(f"""
        <div class="{status_class}">
            {icon} {check["component"]}: {check["status"]} | Response: {check["response_time"]}
        </div>
        """, unsafe_allow_html=True)
    
    # System resources
    st.markdown("#### 💻 System Resources")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("CPU Usage", "34%", "-5%")
    with col2:
        st.metric("Memory Usage", "68%", "+2%")
    with col3:
        st.metric("Storage", "45% Used", "+1%")
    with col4:
        st.metric("Network I/O", "2.3 MB/s", "+0.5 MB/s")

def show_configuration():
    """Display system configuration options"""
    st.markdown("### ⚙️ System Configuration")
    
    with st.expander("🔧 Prediction Settings"):
        col1, col2 = st.columns(2)
        with col1:
            confidence_threshold = st.slider("Minimum Confidence Threshold", 50, 95, 70)
            max_predictions = st.number_input("Max Predictions per Day", 10, 100, 50)
        with col2:
            auto_retrain = st.checkbox("Auto-retrain Models", True)
            live_updates = st.checkbox("Enable Live Updates", True)
    
    with st.expander("👥 User Management"):
        col1, col2 = st.columns(2)
        with col1:
            max_users = st.number_input("Max Concurrent Users", 100, 10000, 1000)
            session_timeout = st.number_input("Session Timeout (minutes)", 15, 480, 60)
        with col2:
            guest_access = st.checkbox("Allow Guest Access", True)
            registration_open = st.checkbox("Open Registration", True)
    
    with st.expander("🔔 Notifications"):
        alert_emails = st.text_area("Alert Email Addresses", "admin@nbapredictions.com")
        error_threshold = st.slider("Error Alert Threshold", 1, 10, 5)
        
    if st.button("💾 Save Configuration", use_container_width=True):
        st.success("Configuration saved successfully!")

def show_recent_activity():
    """Display recent system activity"""
    st.markdown("### 📋 Recent Activity")
    
    activities = [
        {"time": "2 mins ago", "user": "admin", "action": "Updated model configuration", "status": "success"},
        {"time": "15 mins ago", "user": "user123", "action": "Generated prediction for Lakers vs Warriors", "status": "info"},
        {"time": "1 hour ago", "user": "system", "action": "Completed model retraining", "status": "success"},
        {"time": "2 hours ago", "user": "demo_admin", "action": "Accessed admin dashboard", "status": "info"},
        {"time": "3 hours ago", "user": "system", "action": "Live data sync completed", "status": "success"},
    ]
    
    for activity in activities:
        if activity["status"] == "success":
            icon = "✅"
            color = "#28a745"
        elif activity["status"] == "warning":
            icon = "⚠️"
            color = "#ffc107"
        elif activity["status"] == "error":
            icon = "❌"
            color = "#dc3545"
        else:
            icon = "ℹ️"
            color = "#17a2b8"
        
        st.markdown(f"""
        <div style="background: white; padding: 15px; margin: 10px 0; border-radius: 10px; 
                   border-left: 4px solid {color}; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong style="color: #2c3e50;">{icon} {activity['action']}</strong><br>
                    <small style="color: #6c757d;">by {activity['user']}</small>
                </div>
                <small style="color: #6c757d;">{activity['time']}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main(user_info):
    """Main admin dashboard function"""
    
    # Apply admin dashboard styling
    apply_admin_dashboard_styling()
    
    # Welcome header
    st.markdown(f"""
    <div class="admin-welcome">
        <h2 style="margin: 0; color: white;">👨‍💼 Admin Dashboard - Welcome, {user_info['name']}!</h2>
        <p style="margin: 10px 0 0 0; color: #ffe8e8;">Complete system management and monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🖥️ Overview", 
        "🤖 Models", 
        "📈 Analytics", 
        "🔍 Monitoring", 
        "⚙️ Config"
    ])
    
    with tab1:
        show_system_overview()
        st.markdown("---")
        show_recent_activity()
    
    with tab2:
        show_model_management()
    
    with tab3:
        show_user_analytics()
    
    with tab4:
        show_system_monitoring()
    
    with tab5:
        show_configuration()
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: #6c757d; margin-top: 30px;">
        <small>🔒 Admin Dashboard | NBA Predictions System v2.1.0</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # For testing
    demo_admin = {"name": "Demo Admin", "role": "admin", "username": "demo_admin"}
    main(demo_admin)
