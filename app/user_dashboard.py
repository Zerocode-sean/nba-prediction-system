#!/usr/bin/env python3
"""
👤 NBA Predictions - Simplified User Dashboard
==============================================

Clean, modern user interface using Streamlit native components.
Focuses on functionality and readability over complex HTML.
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
import time

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

# Try to import prediction modules (optional for enhanced features)
try:
    from src.prediction.pipeline import NBAPredictionPipeline
    from src.prediction.realtime_system import RealTimeNBASystem
    PREDICTION_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Prediction modules not available: {e}")
    NBAPredictionPipeline = None
    RealTimeNBASystem = None
    PREDICTION_MODULES_AVAILABLE = False

def apply_clean_styling():
    """Apply custom color scheme styling - Dark theme with bright accents"""
    st.markdown("""
    <style>
    /* Main App Background - Custom dark theme */
    .stApp {
        background: #0B0808;
        color: #ffffff;
    }
    
    /* Main Containers - Dark cards with enhanced visibility */
    .main-container {
        background: rgba(24, 24, 28, 0.95);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 16px 45px rgba(0,0,0,0.7), 0 0 0 2px rgba(223, 227, 29, 0.4);
        border: 3px solid #dfe31d;
        color: #ffffff;
    }
    
    /* Prediction Cards - Dark background with enhanced visibility */
    .prediction-container {
        background: #18181C;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        border-left: 6px solid #dfe31d;
        box-shadow: 0 12px 35px rgba(0,0,0,0.6), 0 0 0 2px rgba(223, 227, 29, 0.3);
        border: 3px solid rgba(223, 227, 29, 0.6);
        color: #ffffff;
    }
    
    /* Live Game Cards - Dark background with enhanced visibility and orange scores */
    .live-game-container {
        background: #18181C;
        border-radius: 12px;
        padding: 25px;
        margin: 15px 0;
        border-left: 6px solid #dfe31d;
        box-shadow: 0 12px 35px rgba(0,0,0,0.6), 0 0 0 2px rgba(223, 227, 29, 0.3);
        border: 3px solid rgba(223, 227, 29, 0.6);
        color: #ffffff;
    }
    
    /* Metric Cards - Dark theme with enhanced visibility */
    .metric-container {
        background: #18181C;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border-top: 5px solid #dfe31d;
        box-shadow: 0 12px 35px rgba(0,0,0,0.6), 0 0 0 2px rgba(223, 227, 29, 0.3);
        border: 3px solid rgba(223, 227, 29, 0.6);
        margin: 10px 0;
        color: #ffffff;
    }
    
    /* Typography - Custom colors for dark theme */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        font-weight: 600;
    }
    
    /* Text content in containers */
    .main-container h1, .main-container h2, .main-container h3,
    .prediction-container h1, .prediction-container h2, .prediction-container h3,
    .live-game-container h1, .live-game-container h2, .live-game-container h3,
    .metric-container h1, .metric-container h2, .metric-container h3 {
        color: #ffffff !important;
    }
    
    /* Subheaders with yellow accent */
    .main-container h4, .main-container h5, .main-container h6,
    .prediction-container h4, .prediction-container h5, .prediction-container h6,
    .live-game-container h4, .live-game-container h5, .live-game-container h6 {
        color: #dfe31d !important;
    }
    
    /* Confidence indicators with custom color scheme */
    .confidence-high {
        color: #000000 !important;
        background-color: #00FF88;
        padding: 6px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid #00FF88;
        text-transform: uppercase;
        font-size: 0.85em;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3);
        animation: pulse-green 2s infinite alternate;
    }
    
    @keyframes pulse-green {
        0% { box-shadow: 0 4px 12px rgba(0, 255, 136, 0.3); }
        100% { box-shadow: 0 6px 20px rgba(0, 255, 136, 0.5); }
    }
    
    .confidence-medium {
        color: #ffffff !important;
        background-color: rgba(223, 227, 29, 0.3);
        padding: 6px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid #dfe31d;
        text-transform: uppercase;
        font-size: 0.85em;
        letter-spacing: 0.5px;
    }
    
    .confidence-low {
        color: #dfe31d !important;
        background-color: transparent;
        padding: 6px 15px;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        border: 2px solid #dfe31d;
        text-transform: uppercase;
        font-size: 0.85em;
        letter-spacing: 0.5px;
    }
    
    /* Streamlit component overrides for dark theme */
    .stMetric {
        background: transparent;
        padding: 10px;
        border-radius: 8px;
    }
    
    .stMetric > div {
        color: #ffffff !important;
    }
    
    .stMetric > div > div {
        color: #dfe31d !important;
    }
    
    /* Score labels in orange */
    .stMetric > div > div[data-testid="metric-label"] {
        color: #FF7954 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Score values in orange for high visibility */
    .stMetric > div > div[data-testid="metric-value"] {
        color: #FF7954 !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        text-shadow: 0 2px 4px rgba(255, 121, 84, 0.3);
    }
    
    /* Specifically target live game score labels and values */
    .live-game-container .stMetric > div > div[data-testid="metric-label"] {
        color: #FF7954 !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        text-shadow: 0 1px 2px rgba(255, 121, 84, 0.2);
    }
    
    .live-game-container .stMetric > div > div[data-testid="metric-value"] {
        color: #FF7954 !important;
        font-weight: 800 !important;
        font-size: 2.8rem !important;
        text-shadow: 0 3px 6px rgba(255, 121, 84, 0.4);
        letter-spacing: 1px;
    }
    
    /* Additional targeting for Score labels - ensuring orange color visibility */
    .stMetric label {
        color: #FF7954 !important;
    }
    
    .stMetric [data-testid="metric-label"] {
        color: #FF7954 !important;
    }
    
    /* Force orange color for all metric labels containing "Score" */
    .stMetric div:contains("Score") {
        color: #FF7954 !important;
    }
    
    /* Alternative targeting for metric components */
    .live-game-container .stMetric label,
    .live-game-container .stMetric [role="text"]:first-child {
        color: #FF7954 !important;
        font-weight: 700 !important;
    }
    
    /* Ensure orange color for any text that says "Score" */
    .live-game-container *:contains("Score") {
        color: #FF7954 !important;
    }
    
    /* Success/Info/Warning boxes styling for dark theme */
    .stSuccess {
        background-color: rgba(0, 255, 136, 0.15) !important;
        border: 1px solid #00FF88 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    .stInfo {
        background-color: rgba(24, 24, 28, 0.8) !important;
        border: 1px solid #dfe31d !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    .stWarning {
        background-color: rgba(223, 227, 29, 0.1) !important;
        border: 1px solid #dfe31d !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    /* Tab styling for dark theme */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #18181C;
        border-radius: 8px;
        padding: 5px;
        border: 1px solid rgba(223, 227, 29, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 5px;
        color: #ffffff;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #dfe31d !important;
        color: #18181C !important;
        box-shadow: 0 2px 8px rgba(223, 227, 29, 0.3);
        font-weight: 600;
    }
    
    /* Divider styling */
    hr {
        border-color: rgba(223, 227, 29, 0.3) !important;
        margin: 2rem 0 !important;
    }
    
    /* Caption text */
    .stCaption {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Custom status badges with new color scheme */
    .status-live {
        background: #dfe31d;
        color: #18181C;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 700;
        display: inline-block;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 8px rgba(223, 227, 29, 0.3);
    }
    
    .status-upcoming {
        background: transparent;
        color: #ffffff;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 700;
        display: inline-block;
        border: 2px solid #dfe31d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-final {
        background: rgba(223, 227, 29, 0.2);
        color: #dfe31d;
        padding: 6px 15px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 700;
        display: inline-block;
        border: 2px solid #dfe31d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Override Streamlit's default text colors */
    .stMarkdown, .stText {
        color: #ffffff !important;
    }
    
    /* Sidebar styling with enhanced contrast */
    .css-1d391kg {
        background: linear-gradient(180deg, #18181C 0%, #0B0808 100%) !important;
        border-right: 2px solid #dfe31d !important;
        color: #ffffff !important;
    }
    
    /* Additional sidebar selectors for better coverage */
    .css-1aumxhk, .css-1d391kg, .css-1lcbmhc, .css-1y4p8pa {
        background: linear-gradient(180deg, #18181C 0%, #0B0808 100%) !important;
        color: #ffffff !important;
    }
    
    /* Sidebar container enhancements */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #18181C 0%, #0B0808 100%) !important;
        border-right: 3px solid #dfe31d !important;
    }
    
    /* Sidebar content wrapper */
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
        color: #ffffff !important;
    }
    
    /* Force sidebar text colors */
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Override for headers in sidebar */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4 {
        color: #dfe31d !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar markdown text */
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Sidebar markdown headers */
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown h4,
    section[data-testid="stSidebar"] .stMarkdown h5,
    section[data-testid="stSidebar"] .stMarkdown h6 {
        color: #dfe31d !important;
    }
    
    /* Sidebar metrics with enhanced visibility */
    .css-1d391kg .stMetric {
        background: rgba(223, 227, 29, 0.15) !important;
        border: 2px solid rgba(223, 227, 29, 0.4) !important;
        border-radius: 10px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Sidebar metric labels */
    .css-1d391kg .stMetric label,
    .css-1d391kg .stMetric > div > div:first-child {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }
    
    /* Sidebar metric values */
    .css-1d391kg .stMetric > div > div[data-testid="metric-value"] {
        color: #dfe31d !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
        text-shadow: 0 2px 4px rgba(223, 227, 29, 0.4);
    }
    
    /* Sidebar metric deltas */
    .css-1d391kg .stMetric > div > div:last-child {
        color: #00FF88 !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar buttons with enhanced styling */
    .css-1d391kg .stButton > button {
        background: linear-gradient(45deg, #dfe31d, #00FF88) !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 12px rgba(223, 227, 29, 0.3) !important;
        width: 100% !important;
        margin: 5px 0 !important;
    }
    
    .css-1d391kg .stButton > button:hover {
        background: linear-gradient(45deg, #00FF88, #dfe31d) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(223, 227, 29, 0.4) !important;
        color: #000000 !important;
    }
    
    /* Sidebar dividers */
    .css-1d391kg hr {
        border-color: rgba(223, 227, 29, 0.5) !important;
        margin: 20px 0 !important;
        border-width: 2px !important;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: #18181C;
        color: #ffffff;
        border-color: #dfe31d;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #dfe31d, #00FF88);
        color: #000000;
        border: none;
        font-weight: 700;
        border-radius: 10px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #00FF88, #dfe31d);
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(223, 227, 29, 0.4);
    }
    
    /* Profit calculator styling */
    .stNumberInput > div > div > input {
        background: #18181C;
        color: #dfe31d;
        border: 2px solid #dfe31d;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Auto-refresh indicator */
    .refresh-indicator {
        position: fixed;
        top: 10px;
        right: 10px;
        background: #00FF88;
        color: #000000;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8em;
        font-weight: 700;
        z-index: 1000;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Hot Picks Styling */
    .hot-picks {
        background: linear-gradient(135deg, #FF7954, #dfe31d);
        border: 3px solid #FF7954;
        animation: hot-glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes hot-glow {
        0% { box-shadow: 0 16px 45px rgba(0,0,0,0.7), 0 0 0 2px rgba(255, 121, 84, 0.4); }
        100% { box-shadow: 0 16px 45px rgba(0,0,0,0.7), 0 0 0 4px rgba(255, 121, 84, 0.6); }
    }
    
    /* Notification styling */
    .stAlert {
        border-radius: 10px !important;
        border-left: 5px solid !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_sample_nba_data():
    """Get sample NBA data"""
    return [
        {
            'home_team': 'Lakers',
            'away_team': 'Warriors',
            'home_score': 98,
            'away_score': 105,
            'status': 'Live - Q4 2:45',
            'scheduled_time': '8:00 PM EST',
            'home_record': '45-20',
            'away_record': '42-23'
        },
        {
            'home_team': 'Celtics',
            'away_team': 'Heat',
            'home_score': 0,
            'away_score': 0,
            'status': 'Upcoming',
            'scheduled_time': '7:30 PM EST',
            'home_record': '48-17',
            'away_record': '39-26'
        }
    ]

def get_sample_predictions():
    """Get sample predictions"""
    return [
        {
            'game': 'Lakers vs Warriors',
            'date': '2025-03-15',
            'time': '8:00 PM EST',
            'win_prediction': 'Lakers',
            'win_confidence': 0.73,
            'total_prediction': 'Over 225.5',
            'total_confidence': 0.68,
            'spread': 'Lakers -4.5',
            'spread_confidence': 0.71,
            'key_factors': [
                'Lakers home court advantage',
                'Warriors on back-to-back games',
                'LeBron James questionable (knee)'
            ]
        },
        {
            'game': 'Celtics vs Heat',
            'date': '2025-03-15',
            'time': '7:30 PM EST',
            'win_prediction': 'Celtics',
            'win_confidence': 0.79,
            'total_prediction': 'Under 218.5',
            'total_confidence': 0.65,
            'spread': 'Celtics -7.5',
            'spread_confidence': 0.74,
            'key_factors': [
                'Celtics strong home record (28-5)',
                'Heat missing key rotation players',
                'Playoff implications for seeding'
            ]
        }
    ]

def display_live_scores():
    """Display live scores using Streamlit components"""
    st.header("🏀 Live NBA Games")
    
    games = get_sample_nba_data()
    
    for game in games:
        with st.container():
            st.markdown('<div class="live-game-container">', unsafe_allow_html=True)
            
            # Add status indicator
            status = game['status']
            if 'Live' in status:
                status_class = 'status-live'
            elif status == 'Upcoming':
                status_class = 'status-upcoming'
            else:
                status_class = 'status-final'
            
            st.markdown(f'<div class="{status_class}">{status}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                st.subheader(f"🏃 {game['away_team']}")
                st.metric("Score", game['away_score'])
                st.caption(f"Record: {game['away_record']}")
            
            with col2:
                st.markdown("### @")
                st.caption(game['scheduled_time'])
            
            with col3:
                st.subheader(f"🏠 {game['home_team']}")
                st.metric("Score", game['home_score'])
                st.caption(f"Record: {game['home_record']}")
            
            st.markdown('</div>', unsafe_allow_html=True)

def get_confidence_class(confidence):
    """Get confidence CSS class"""
    if confidence >= 0.7:
        return "confidence-high"
    elif confidence >= 0.6:
        return "confidence-medium"
    else:
        return "confidence-low"

def display_predictions():
    """Display predictions using Streamlit components"""
    st.header("🎯 Today's Predictions")
    
    predictions = get_sample_predictions()
    
    for pred in predictions:
        with st.container():
            # Check if any prediction has high confidence
            has_high_confidence = any([
                pred['win_confidence'] >= 0.7,
                pred['total_confidence'] >= 0.7,
                pred['spread_confidence'] >= 0.7
            ])
            
            # Add special class for high-confidence predictions
            container_class = "prediction-container high-confidence" if has_high_confidence else "prediction-container"
            st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
            
            # Game header
            st.subheader(f"🏀 {pred['game']}")
            st.caption(f"📅 {pred['date']} at {pred['time']}")
            
            # Predictions in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**🎯 Win Prediction**")
                st.success(pred['win_prediction'])
                conf_class = get_confidence_class(pred['win_confidence'])
                conf_pct = int(pred['win_confidence'] * 100)
                st.markdown(f'<span class="{conf_class}">{conf_pct}% Confidence</span>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("**📊 Total Points**")
                st.info(pred['total_prediction'])
                conf_class = get_confidence_class(pred['total_confidence'])
                conf_pct = int(pred['total_confidence'] * 100)
                st.markdown(f'<span class="{conf_class}">{conf_pct}% Confidence</span>', unsafe_allow_html=True)
            
            with col3:
                st.markdown("**📈 Spread**")
                st.warning(pred['spread'])
                conf_class = get_confidence_class(pred['spread_confidence'])
                conf_pct = int(pred['spread_confidence'] * 100)
                st.markdown(f'<span class="{conf_class}">{conf_pct}% Confidence</span>', unsafe_allow_html=True)
            
            # Key factors
            st.markdown("**🔍 Key Factors:**")
            for factor in pred['key_factors']:
                st.markdown(f"• {factor}")
            
            st.markdown('</div>', unsafe_allow_html=True)

def display_performance_metrics():
    """Display performance metrics"""
    st.header("📊 Model Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Win Rate", "87%", "3.2%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Accuracy", "91%", "1.8%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("Games Analyzed", "2,400", "127")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-container">', unsafe_allow_html=True)
        st.metric("ROI", "+12%", "2.1%")
        st.markdown('</div>', unsafe_allow_html=True)

def display_chart():
    """Display performance chart with custom dark theme styling"""
    st.subheader("📈 Performance Trends")
    
    # Sample data
    dates = pd.date_range(start='2025-01-01', end='2025-03-15', freq='D')
    np.random.seed(42)
    accuracy = 85 + np.cumsum(np.random.randn(len(dates)) * 0.5)
    accuracy = np.clip(accuracy, 75, 95)
    
    fig = px.line(
        x=dates, y=accuracy,
        title="Model Accuracy Over Time",
        labels={'x': 'Date', 'y': 'Accuracy (%)'},
        template='plotly_dark'
    )
    
    # Custom styling for dark theme with yellow accent
    fig.update_traces(
        line_color='#dfe31d', 
        line_width=3,
        hovertemplate='<b>Date:</b> %{x}<br><b>Accuracy:</b> %{y:.1f}%<extra></extra>'
    )
    
    fig.update_layout(
        plot_bgcolor='#18181C',
        paper_bgcolor='#18181C',
        font=dict(color='#ffffff'),
        title_font=dict(size=16, color='#dfe31d', family="Arial Black"),
        xaxis=dict(
            gridcolor='rgba(223, 227, 29, 0.2)',
            linecolor='#dfe31d',
            tickfont=dict(color='#ffffff')
        ),
        yaxis=dict(
            gridcolor='rgba(223, 227, 29, 0.2)',
            linecolor='#dfe31d',
            tickfont=dict(color='#ffffff')
        ),
        hoverlabel=dict(
            bgcolor='#0B0808',
            bordercolor='#dfe31d',
            font_color='#ffffff'
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

def display_education():
    """Display educational content"""
    st.header("ℹ️ Understanding Predictions")
    
    tab1, tab2, tab3 = st.tabs(["🎯 How It Works", "📊 Confidence Levels", "⚠️ Disclaimers"])
    
    with tab1:
        st.markdown("""
        ### How Our Predictions Work
        
        **🏆 Win Predictions**
        - Analyzes team performance, player stats, injuries
        - Considers home/away records and head-to-head matchups
        - Uses machine learning models trained on historical data
        
        **📊 Total Points**
        - Evaluates offensive/defensive efficiency
        - Considers pace of play and recent scoring trends
        - Factors in weather and venue conditions
        
        **📈 Spread Predictions**
        - Assesses point differential expectations
        - Based on team strength and recent form
        - Incorporates market movements and betting patterns
        """)
    
    with tab2:
        st.markdown("""
        ### Confidence Level Guide
        
        **🟢 High Confidence (70%+)**
        - Strong data support
        - Clear statistical advantages
        - Recommended for consideration
        
        **🟡 Medium Confidence (60-70%)**
        - Moderate data support
        - Some uncertainty factors
        - Proceed with caution
        
        **🔴 Low Confidence (<60%)**
        - Limited data support
        - High uncertainty
        - Not recommended
        """)
    
    with tab3:
        st.warning("""
        **⚠️ Important Disclaimers**
        
        - Predictions are for entertainment purposes only
        - Past performance does not guarantee future results
        - Please gamble responsibly
        - Never bet more than you can afford to lose
        
        **🆘 Need Help?**
        National Problem Gambling Helpline: 1-800-522-4700
        """)

def display_hot_picks():
    """Display hot picks - top recommendations"""
    st.header("🔥 Today's Hot Picks")
    st.markdown("*High-confidence predictions with the best value*")
    
    # Hot picks container
    st.markdown('<div class="main-container hot-picks">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="prediction-container high-confidence">', unsafe_allow_html=True)
        st.markdown("### 🏆 LOCK OF THE DAY")
        st.markdown("**Celtics vs Heat**")
        st.success("Celtics -7.5")
        st.markdown('<span class="confidence-high">79% Confidence</span>', unsafe_allow_html=True)
        st.markdown("💰 **Expected Value: +15%**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="prediction-container high-confidence">', unsafe_allow_html=True)
        st.markdown("### ⭐ BEST VALUE")
        st.markdown("**Lakers vs Warriors**")
        st.info("Over 225.5")
        st.markdown('<span class="confidence-high">73% Confidence</span>', unsafe_allow_html=True)
        st.markdown("💰 **Expected Value: +12%**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="prediction-container">', unsafe_allow_html=True)
        st.markdown("### 🎯 UPSET SPECIAL")
        st.markdown("**Pacers vs Bucks**")
        st.warning("Pacers +8.5")
        st.markdown('<span class="confidence-medium">68% Confidence</span>', unsafe_allow_html=True)
        st.markdown("💰 **Expected Value: +8%**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_sidebar_navigation():
    """Display sidebar navigation"""
    with st.sidebar:
        st.markdown("### 🏀 Navigation")
        
        # Quick stats
        st.markdown("#### Today's Summary")
        st.metric("Games", "5", "2")
        st.metric("Hot Picks", "3", "1")
        st.metric("Live Games", "2", "0")
        
        st.divider()
        
        # Quick actions
        st.markdown("#### Quick Actions")
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        if st.button("📧 Get Alerts", use_container_width=True):
            st.success("Alert preferences updated!")
        
        st.divider()
        
        # Performance summary
        st.markdown("#### Your Performance")
        st.metric("Win Rate", "87%", "3%")
        st.metric("Total Bets", "127", "12")
        st.metric("Profit", "+$2,470", "+$340")

def display_notification_system():
    """Display notification system"""
    # Check for important notifications
    notifications = [
        {"type": "success", "message": "🎉 Your prediction for Lakers -4.5 won!", "time": "2 minutes ago"},
        {"type": "info", "message": "ℹ️ Game postponed: Nuggets vs Thunder", "time": "15 minutes ago"},
        {"type": "warning", "message": "⚠️ Key player injury: LeBron James (questionable)", "time": "1 hour ago"}
    ]
    
    if notifications:
        st.markdown("### 🔔 Recent Notifications")
        for notif in notifications:
            if notif["type"] == "success":
                st.success(f"{notif['message']} *{notif['time']}*")
            elif notif["type"] == "info":
                st.info(f"{notif['message']} *{notif['time']}*")
            elif notif["type"] == "warning":
                st.warning(f"{notif['message']} *{notif['time']}*")

def display_profit_calculator():
    """Display interactive profit/loss calculator"""
    st.header("💰 Profit Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Calculate Potential Returns")
        bet_amount = st.number_input("Bet Amount ($)", min_value=1, max_value=10000, value=100)
        odds = st.selectbox("Odds Format", ["American (-110)", "Decimal (1.91)", "Fractional (10/11)"])
        confidence = st.slider("Your Confidence", 50, 100, 75)
        
        # Calculate returns
        if odds == "American (-110)":
            potential_profit = bet_amount * 0.91
        else:
            potential_profit = bet_amount * 0.91
        
        risk_adjusted_value = potential_profit * (confidence / 100)
        
    with col2:
        st.markdown("#### Expected Returns")
        st.metric("Potential Profit", f"${potential_profit:.2f}")
        st.metric("Risk-Adjusted Value", f"${risk_adjusted_value:.2f}")
        
        if risk_adjusted_value > bet_amount * 0.1:
            st.success("✅ Good value bet!")
        elif risk_adjusted_value > 0:
            st.warning("⚠️ Marginal value")
        else:
            st.error("❌ Poor value - avoid")

def add_auto_refresh():
    """Add auto-refresh functionality"""
    # Create a placeholder for the refresh timer
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = time.time()
    
    # Auto-refresh every 30 seconds for live data
    current_time = time.time()
    if current_time - st.session_state.last_refresh > 30:
        st.session_state.last_refresh = current_time
        st.rerun()

def main(user_info):
    """Main enhanced user dashboard with new features"""
    
    # Apply styling
    apply_clean_styling()
    
    # Sidebar navigation
    display_sidebar_navigation()
    
    # Auto-refresh indicator
    st.markdown('<div class="refresh-indicator">🔄 Live</div>', unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.title(f"🏀 Welcome, {user_info['name']}!")
    st.markdown("Your personalized NBA predictions dashboard")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Notifications
    display_notification_system()
    
    st.divider()
    
    # Hot Picks - NEW!
    display_hot_picks()
    
    st.divider()
    
    # Live scores
    display_live_scores()
    
    st.divider()
    
    # Predictions
    display_predictions()
    
    st.divider()
    
    # Performance metrics
    display_performance_metrics()
    
    # Profit Calculator - NEW!
    display_profit_calculator()
    
    st.divider()
    
    # Chart
    display_chart()
    
    st.divider()
    
    # Educational content
    display_education()
    
    # Footer with enhanced info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("📅 Last updated: " + datetime.now().strftime("%H:%M:%S"))
    with col2:
        st.caption("🎯 Model v2.1.0")
    with col3:
        st.caption("⚡ Real-time data")

def show_user_dashboard_main(user):
    """Main user dashboard function for integration with streamlit_app.py"""
    apply_clean_styling()
    
    st.title("🏀 NBA Predictions Dashboard")
    st.markdown(f"Welcome back, **{user['name']}**! Here are today's predictions.")
    
    # Use our customized dashboard components
    main(user)

if __name__ == "__main__":
    # Test user
    demo_user = {
        "name": "Demo User",
        "role": "user",
        "username": "demo"
    }
    main(demo_user)
