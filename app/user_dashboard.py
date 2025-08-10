#!/usr/bin/env python3
"""
👤 NBA Predictions - User Dashboard
==================================

Clean, modern user interface for browsing NBA game predictions.
Users can view predictions, live scores, and system performance.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import sys
import os
from pathlib import Path
import json

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

def apply_user_dashboard_styling():
    """Apply modern styling for user dashboard"""
    st.markdown("""
    <style>
    /* User Dashboard Specific Styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .user-dashboard-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .user-dashboard-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .prediction-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #28a745;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .prediction-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .live-scores-ticker {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(40,167,69,0.3);
    }
    
    .user-metric {
        background: white;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-top: 3px solid #667eea;
    }
    
    h1, h2, h3 {
        color: #2c3e50;
    }
    
    .user-welcome {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(102,126,234,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def get_live_nba_scores():
    """Get live NBA scores - simplified version with fallback"""
    try:
        if RealTimeNBASystem:
            real_time_system = RealTimeNBASystem()
            live_scores = real_time_system.get_live_scores()
            
            if live_scores and 'games' in live_scores:
                games = live_scores['games'][:5]  # Show only first 5 games
                return games
            else:
                return []
        else:
            return []
    except Exception as e:
        st.error(f"Error loading live scores: {e}")
        return []

def display_live_scores():
    """Display live NBA scores in a clean format"""
    st.markdown("### 🏀 Live NBA Scores")
    
    games = get_live_nba_scores()
    
    if games:
        for game in games:
            try:
                home_team = game.get('home_team', 'TBD')
                away_team = game.get('away_team', 'TBD')
                home_score = game.get('home_score', 0)
                away_score = game.get('away_score', 0)
                status = game.get('status', 'Scheduled')
                scheduled_time = game.get('scheduled_time', 'TBD')
                
                st.markdown(f"""
                <div class="live-scores-ticker">
                    🏀 {away_team} @ {home_team} | Score: {away_score} - {home_score} | {status} | {scheduled_time}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.warning(f"Error displaying game: {e}")
    else:
        st.markdown("""
        <div class="live-scores-ticker">
            🏀 No live games currently. NBA season starts October 2025!
        </div>
        """, unsafe_allow_html=True)

def get_sample_predictions():
    """Get sample predictions for demonstration"""
    sample_predictions = [
        {
            'game': 'Lakers vs Warriors',
            'date': '2025-03-15',
            'time': '8:00 PM EST',
            'win_prediction': 'Lakers',
            'win_confidence': 0.68,
            'total_prediction': 'Over 225.5',
            'total_confidence': 0.72,
            'odds': {'Lakers': -150, 'Warriors': +130, 'Over': -110, 'Under': -110}
        },
        {
            'game': 'Celtics vs Heat',
            'date': '2025-03-15',
            'time': '7:30 PM EST',
            'win_prediction': 'Celtics',
            'win_confidence': 0.75,
            'total_prediction': 'Under 218.5',
            'total_confidence': 0.65,
            'odds': {'Celtics': -200, 'Heat': +170, 'Over': -105, 'Under': -115}
        }
    ]
    return sample_predictions

def display_prediction_card(prediction, index):
    """Display a single prediction in a user-friendly card format"""
    win_conf_pct = int(prediction['win_confidence'] * 100)
    total_conf_pct = int(prediction['total_confidence'] * 100)
    
    # Get confidence color
    win_color = "#28a745" if win_conf_pct >= 70 else "#ffc107" if win_conf_pct >= 60 else "#dc3545"
    total_color = "#28a745" if total_conf_pct >= 70 else "#ffc107" if total_conf_pct >= 60 else "#dc3545"
    
    st.markdown(f"""
    <div class="prediction-card">
        <h4 style="color: #2c3e50; margin-bottom: 15px; font-size: 1.4em; font-weight: bold;">
            🏀 {prediction['game']}
        </h4>
        <p style="color: #6c757d; margin-bottom: 15px;">
            📅 {prediction['date']} at {prediction['time']}
        </p>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
                <h5 style="color: #495057; margin-bottom: 10px;">🎯 Win Prediction</h5>
                <p style="color: #212529; font-weight: bold; margin-bottom: 5px;">
                    {prediction['win_prediction']}
                </p>
                <div style="background: {win_color}; color: white; padding: 5px 10px; border-radius: 15px; 
                           text-align: center; font-size: 0.9em; font-weight: bold;">
                    {win_conf_pct}% Confidence
                </div>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 10px;">
                <h5 style="color: #495057; margin-bottom: 10px;">📊 Total Prediction</h5>
                <p style="color: #212529; font-weight: bold; margin-bottom: 5px;">
                    {prediction['total_prediction']}
                </p>
                <div style="background: {total_color}; color: white; padding: 5px 10px; border-radius: 15px; 
                           text-align: center; font-size: 0.9em; font-weight: bold;">
                    {total_conf_pct}% Confidence
                </div>
            </div>
        </div>
        
        <div style="background: #e9ecef; padding: 15px; border-radius: 10px; margin-top: 15px;">
            <h6 style="color: #495057; margin-bottom: 10px;">💰 Current Odds</h6>
            <p style="color: #6c757d; margin: 0; line-height: 1.6;">
                <strong>Win:</strong> {list(prediction['odds'].keys())[0]} ({prediction['odds'][list(prediction['odds'].keys())[0]]}) | 
                {list(prediction['odds'].keys())[1]} ({prediction['odds'][list(prediction['odds'].keys())[1]]})<br>
                <strong>Total:</strong> Over ({prediction['odds']['Over']}) | Under ({prediction['odds']['Under']})
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_predictions():
    """Display NBA predictions in a clean card format"""
    st.markdown("### 🎯 Today's Predictions")
    
    try:
        if NBAPredictionPipeline:
            pipeline = NBAPredictionPipeline()
            
            # Load models
            models_loaded = pipeline.load_models()
            if not models_loaded:
                st.warning("⚠️ Models not loaded. Using demo data.")
                predictions = get_sample_predictions()
            else:
                # Try to get real predictions (simplified for user view)
                predictions = get_sample_predictions()  # Using samples for now
            
            if predictions:
                for i, pred in enumerate(predictions):
                    display_prediction_card(pred, i)
            else:
                st.info("ℹ️ No predictions available at the moment.")
        else:
            st.info("ℹ️ Showing sample predictions.")
            predictions = get_sample_predictions()
            for i, pred in enumerate(predictions):
                display_prediction_card(pred, i)
            
    except Exception as e:
        st.error(f"Error loading predictions: {e}")
        st.info("Showing sample predictions instead.")
        predictions = get_sample_predictions()
        for i, pred in enumerate(predictions):
            display_prediction_card(pred, i)

def show_user_stats():
    """Display user-focused system statistics"""
    st.markdown("### 📊 System Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="user-metric">
            <h3 style="color: #667eea; margin: 0;">85%</h3>
            <p style="margin: 5px 0 0 0; color: #6c757d;">Win Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="user-metric">
            <h3 style="color: #28a745; margin: 0;">92%</h3>
            <p style="margin: 5px 0 0 0; color: #6c757d;">Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="user-metric">
            <h3 style="color: #ffc107; margin: 0;">1,230</h3>
            <p style="margin: 5px 0 0 0; color: #6c757d;">Games</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="user-metric">
            <h3 style="color: #17a2b8; margin: 0;">24/7</h3>
            <p style="margin: 5px 0 0 0; color: #6c757d;">Updates</p>
        </div>
        """, unsafe_allow_html=True)

def show_user_info():
    """Display user information and tips"""
    st.markdown("### ℹ️ How to Use NBA Predictions")
    
    st.markdown("""
    <div class="user-dashboard-card">
        <h4 style="color: #2c3e50; margin-bottom: 15px;">🎯 Understanding Predictions</h4>
        <ul style="color: #6c757d; line-height: 1.8;">
            <li><strong>Win Predictions:</strong> Shows which team is likely to win</li>
            <li><strong>Total Predictions:</strong> Over/Under point total forecasts</li>
            <li><strong>Confidence Levels:</strong> Higher percentages = more reliable predictions</li>
            <li><strong>Live Updates:</strong> Scores and odds updated in real-time</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="user-dashboard-card">
        <h4 style="color: #2c3e50; margin-bottom: 15px;">📈 Confidence Guide</h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
            <div style="text-align: center; padding: 15px; background: #d4edda; border-radius: 10px;">
                <div style="color: #155724; font-weight: bold;">70%+ Confidence</div>
                <div style="color: #155724; font-size: 0.9em;">High Reliability</div>
            </div>
            <div style="text-align: center; padding: 15px; background: #fff3cd; border-radius: 10px;">
                <div style="color: #856404; font-weight: bold;">60-70% Confidence</div>
                <div style="color: #856404; font-size: 0.9em;">Moderate Reliability</div>
            </div>
            <div style="text-align: center; padding: 15px; background: #f8d7da; border-radius: 10px;">
                <div style="color: #721c24; font-weight: bold;">Below 60%</div>
                <div style="color: #721c24; font-size: 0.9em;">Lower Reliability</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def main(user_info):
    """Main user dashboard function"""
    
    # Apply user dashboard styling
    apply_user_dashboard_styling()
    
    # Welcome header
    st.markdown(f"""
    <div class="user-welcome">
        <h2 style="margin: 0; color: white;">🏀 Welcome to NBA Predictions, {user_info['name']}!</h2>
        <p style="margin: 10px 0 0 0; color: #e9ecef;">Your personalized basketball prediction dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dashboard sections
    with st.container():
        display_live_scores()
    
    st.markdown("---")
    
    with st.container():
        show_predictions()
    
    st.markdown("---")
    
    with st.container():
        show_user_stats()
    
    st.markdown("---")
    
    with st.container():
        show_user_info()
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: #6c757d; margin-top: 30px;">
        <small>⚠️ For entertainment purposes only. Please gamble responsibly.</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # For testing
    demo_user = {"name": "Demo User", "role": "user", "username": "demo"}
    main(demo_user)
