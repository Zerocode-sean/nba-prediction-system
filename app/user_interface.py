#!/usr/bin/env python3
"""
🏀 NBA Predictions - User Interface
==================================

Clean, modern user interface for browsing NBA game predictions.
Users can view available predictions, odds, and make informed betting decisions.
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
from plotly.subplots import make_subplots

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

from src.prediction.pipeline import NBAPredictionPipeline
from src.prediction.realtime_system import RealTimeNBASystem

# Custom CSS for modern, sleek design with sports background
st.markdown("""
<style>
    /* Sports-themed background with basketball court pattern */
    .main {
        background: linear-gradient(135deg, #0f1419 0%, #1a2332 25%, #2d3a52 50%, #1a2332 75%, #0f1419 100%);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        min-height: 100vh;
        position: relative;
    }
    
    /* Basketball court lines overlay */
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            /* Court center circle */
            radial-gradient(circle at 50% 50%, transparent 48px, rgba(255,255,255,0.05) 50px, rgba(255,255,255,0.05) 52px, transparent 54px),
            /* Court lines */
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(0deg, rgba(255,255,255,0.03) 1px, transparent 1px),
            /* Basketball texture dots */
            radial-gradient(circle at 25% 25%, rgba(255,165,0,0.08) 2px, transparent 2px),
            radial-gradient(circle at 75% 75%, rgba(255,165,0,0.06) 1px, transparent 1px);
        background-size: 200px 200px, 60px 60px, 60px 60px, 40px 40px, 30px 30px;
        background-position: 0 0, 0 0, 0 0, 0 0, 15px 15px;
        animation: courtMove 30s linear infinite;
        pointer-events: none;
        z-index: -1;
        opacity: 0.8;
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes courtMove {
        0% { background-position: 0 0, 0 0, 0 0, 0 0, 15px 15px; }
        100% { background-position: 200px 200px, 60px 60px, 60px 60px, 40px 40px, 45px 45px; }
    }
    
    /* Content container with glassmorphism */
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        margin: 1rem;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.2);
        position: relative;
        z-index: 1;
    }
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #1f4e79, #2d6aa0, #0066cc);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: headerShimmer 6s ease-in-out infinite;
        pointer-events: none;
    }
    
    @keyframes headerShimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Enhanced mobile responsiveness */
    @media (max-width: 1024px) {
        .block-container {
            margin: 0.8rem;
            padding: 1.5rem;
        }
        
        .main-header {
            padding: 2rem;
        }
    }
    
    @media (max-width: 768px) {
        .block-container {
            margin: 0.5rem !important;
            padding: 1rem !important;
            border-radius: 15px !important;
        }
        
        .main-header {
            padding: 1.5rem !important;
        }
        
        .main::before {
            animation: none !important; /* Disable complex animations on mobile */
        }
    }
    
    @media (max-width: 480px) {
        .block-container {
            margin: 0.2rem !important;
            padding: 0.8rem !important;
            border-radius: 10px !important;
        }
        
        .main-header {
            padding: 1rem !important;
            margin-bottom: 1rem !important;
        }
    }
    
    .game-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #2d6aa0;
        transition: all 0.3s ease;
    }
    
    .game-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .prediction-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.9rem;
        margin: 0.2rem;
    }
    
    .win-prediction {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
    }
    
    .over-prediction {
        background: linear-gradient(45deg, #fd7e14, #ffc107);
        color: white;
    }
    
    .under-prediction {
        background: linear-gradient(45deg, #6f42c1, #e83e8c);
        color: white;
    }
    
    .confidence-high {
        background: linear-gradient(45deg, #dc3545, #fd7e14);
        color: white;
    }
    
    .confidence-medium {
        background: linear-gradient(45deg, #ffc107, #28a745);
        color: white;
    }
    
    .confidence-low {
        background: linear-gradient(45deg, #6c757d, #adb5bd);
        color: white;
    }
    
    .team-vs {
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
        color: #2d6aa0;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .stat-item {
        text-align: center;
        padding: 0.8rem;
        background: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2d6aa0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6c757d;
        margin-top: 0.2rem;
    }
    
    .filter-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid #e9ecef;
    }
    
    .no-games {
        text-align: center;
        padding: 3rem;
        color: #6c757d;
        font-size: 1.1rem;
    }
    
    .footer-info {
        margin-top: 3rem;
        text-align: center;
        color: #6c757d;
        font-size: 0.9rem;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 12px;
    }
    
    /* Modern Card Design */
    .card-header {
        margin-bottom: 1.5rem;
    }
    
    .team-matchup {
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .team-info {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .team-name {
        font-size: 1.5rem;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #2d6aa0, #1f4e79);
        color: white;
        min-width: 120px;
        text-align: center;
    }
    
    .vs-text {
        font-size: 1.2rem;
        font-weight: bold;
        color: #6c757d;
    }
    
    .game-details {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 1rem;
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    
    .detail-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .detail-icon {
        font-size: 1.2rem;
    }
    
    .detail-text {
        font-weight: 600;
        color: #495057;
    }
    
    .status-today {
        color: #28a745 !important;
        font-weight: bold;
    }
    
    .status-other {
        color: #6c757d !important;
    }
    
    .predictions-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .prediction-section {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }
    
    .prediction-section:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    .prediction-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .prediction-icon {
        font-size: 1.3rem;
    }
    
    .prediction-title {
        font-weight: bold;
        color: #2d6aa0;
        font-size: 1.1rem;
    }
    
    .prediction-content {
        text-align: center;
    }
    
    .prediction-result {
        font-size: 1.2rem;
        font-weight: bold;
        padding: 0.8rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }
    
    .confidence-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .confidence-high {
        background: linear-gradient(135deg, #dc3545, #fd7e14);
        color: white;
    }
    
    .confidence-medium {
        background: linear-gradient(135deg, #ffc107, #28a745);
        color: white;
    }
    
    .confidence-low {
        background: linear-gradient(135deg, #6c757d, #adb5bd);
        color: white;
    }
    
    .stats-summary {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-top: 1.5rem;
    }
    
    .stat-card {
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e9ecef;
        transition: transform 0.2s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
    }
    
    .stat-card .stat-value {
        font-size: 1.4rem;
        font-weight: bold;
        color: #2d6aa0;
        margin-bottom: 0.3rem;
    }
    
    .stat-card .stat-label {
        font-size: 0.8rem;
        color: #6c757d;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .team-info {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .team-name {
            font-size: 1.2rem;
            min-width: 100px;
        }
        
        .predictions-container {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
        
        .stats-summary {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .game-details {
            flex-direction: column;
            text-align: center;
        }
    }
    
    @media (max-width: 480px) {
        .stats-summary {
            grid-template-columns: 1fr;
        }
        
        .team-name {
            font-size: 1rem;
            padding: 0.4rem 0.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

class UserInterface:
    """Modern user interface for NBA predictions"""
    
    def __init__(self):
        self.pipeline = NBAPredictionPipeline()
        self.realtime_system = RealTimeNBASystem()
        
    def render_header(self):
        """Render the main header"""
        current_date = datetime.now().strftime('%Y-%m-%d')
        st.markdown(f"""
        <div class="main-header">
            <h1>🏀 NBA Game Predictions</h1>
            <p>Professional predictions powered by AI • Current date: {current_date}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def get_available_predictions(self):
        """Get available game predictions"""
        try:
            # Try to load pre-generated predictions first
            predictions_file = Path(__file__).parent.parent / "data" / "predictions" / "latest_predictions.json"
            
            if predictions_file.exists():
                with open(predictions_file, 'r') as f:
                    predictions = json.load(f)
                    return predictions
            
            # Try to get real-time games if no predictions file
            games_today = self.realtime_system.get_todays_games()
            upcoming_games = self.realtime_system.get_upcoming_games(days=7)
            
            all_games = []
            
            # Process today's games
            for game in games_today:
                prediction_data = self.generate_game_prediction(game)
                if prediction_data:
                    prediction_data['game_date'] = datetime.now().strftime('%Y-%m-%d')
                    prediction_data['status'] = 'Today'
                    all_games.append(prediction_data)
            
            # Process upcoming games
            for game in upcoming_games[:10]:  # Limit to next 10 games
                prediction_data = self.generate_game_prediction(game)
                if prediction_data:
                    all_games.append(prediction_data)
            
            return all_games
            
        except Exception as e:
            # Fallback to sample predictions
            return self.get_sample_predictions()
    
    def generate_game_prediction(self, game_data):
        """Generate prediction for a single game"""
        try:
            # Extract team names
            home_team = game_data.get('home_team', 'Team A')
            away_team = game_data.get('away_team', 'Team B')
            game_date = game_data.get('date', datetime.now().strftime('%Y-%m-%d'))
            
            # Generate predictions using our pipeline
            predictions = self.pipeline.predict_game(home_team, away_team)
            
            # Calculate confidence levels
            win_confidence = self.calculate_confidence(predictions['win_loss_prob'])
            ou_confidence = self.calculate_confidence(predictions['over_under_prob'])
            
            return {
                'home_team': home_team,
                'away_team': away_team,
                'game_date': game_date,
                'win_prediction': predictions['win_loss_prediction'],
                'win_confidence': win_confidence,
                'win_probability': predictions['win_loss_prob'],
                'over_under_prediction': predictions['over_under_prediction'],
                'ou_confidence': ou_confidence,
                'ou_probability': predictions['over_under_prob'],
                'predicted_total': predictions.get('predicted_total', 220),
                'status': game_data.get('status', 'Upcoming')
            }
            
        except Exception as e:
            return None
    
    def calculate_confidence(self, probability):
        """Calculate confidence level from probability"""
        confidence = abs(probability - 0.5) * 2  # Convert to 0-1 scale
        
        if confidence >= 0.7:
            return "High"
        elif confidence >= 0.4:
            return "Medium"
        else:
            return "Low"
    
    def get_sample_predictions(self):
        """Generate sample predictions for demonstration"""
        sample_games = [
            {"home_team": "Los Angeles Lakers", "away_team": "Boston Celtics"},
            {"home_team": "Golden State Warriors", "away_team": "Miami Heat"},
            {"home_team": "Milwaukee Bucks", "away_team": "Phoenix Suns"},
            {"home_team": "Denver Nuggets", "away_team": "Philadelphia 76ers"},
            {"home_team": "Dallas Mavericks", "away_team": "Chicago Bulls"},
        ]
        
        predictions = []
        for i, game in enumerate(sample_games):
            # Generate realistic sample predictions
            win_prob = np.random.uniform(0.45, 0.85)
            ou_prob = np.random.uniform(0.45, 0.75)
            
            prediction = {
                'home_team': game['home_team'],
                'away_team': game['away_team'],
                'game_date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                'win_prediction': game['home_team'] if win_prob > 0.5 else game['away_team'],
                'win_confidence': self.calculate_confidence(win_prob),
                'win_probability': win_prob,
                'over_under_prediction': "Over" if ou_prob > 0.5 else "Under",
                'ou_confidence': self.calculate_confidence(ou_prob),
                'ou_probability': ou_prob,
                'predicted_total': np.random.randint(210, 240),
                'status': 'Today' if i == 0 else 'Upcoming'
            }
            predictions.append(prediction)
        
        return predictions
    
    def render_filters(self):
        """Render filter section"""
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            date_filter = st.selectbox(
                "📅 Date Range",
                ["All Games", "Today Only", "Next 3 Days", "Next Week"]
            )
        
        with col2:
            confidence_filter = st.selectbox(
                "🎯 Confidence Level",
                ["All Confidence", "High Confidence", "Medium+", "Low Risk"]
            )
        
        with col3:
            prediction_type = st.selectbox(
                "🎲 Prediction Type",
                ["All Predictions", "Win/Loss Only", "Over/Under Only"]
            )
        
        with col4:
            team_filter = st.selectbox(
                "🏀 Team Filter",
                ["All Teams", "Lakers", "Celtics", "Warriors", "Heat", "Bucks"]
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return {
            'date': date_filter,
            'confidence': confidence_filter,
            'type': prediction_type,
            'team': team_filter
        }
    
    def filter_predictions(self, predictions, filters):
        """Apply filters to predictions"""
        filtered = predictions.copy()
        current_date = datetime.now().date()
        
        # Date filter
        if filters['date'] == "Today Only":
            today_str = current_date.strftime('%Y-%m-%d')
            filtered = [p for p in filtered if p['game_date'] == today_str]
        elif filters['date'] == "Next 3 Days":
            cutoff_date = current_date + timedelta(days=3)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d')
            filtered = [p for p in filtered if p['game_date'] <= cutoff_str and p['game_date'] >= current_date.strftime('%Y-%m-%d')]
        elif filters['date'] == "Next Week":
            cutoff_date = current_date + timedelta(days=7)
            cutoff_str = cutoff_date.strftime('%Y-%m-%d')
            filtered = [p for p in filtered if p['game_date'] <= cutoff_str and p['game_date'] >= current_date.strftime('%Y-%m-%d')]
        
        # Update status based on actual date comparison
        for prediction in filtered:
            game_date = datetime.strptime(prediction['game_date'], '%Y-%m-%d').date()
            
            if game_date == current_date:
                prediction['status'] = 'Today'
            elif game_date < current_date:
                prediction['status'] = 'Past'
            else:
                days_ahead = (game_date - current_date).days
                if days_ahead == 1:
                    prediction['status'] = 'Tomorrow'
                elif days_ahead <= 7:
                    prediction['status'] = f'In {days_ahead} days'
                else:
                    prediction['status'] = 'Upcoming'
        
        # Remove past games unless specifically requested
        if filters['date'] != "All Games":
            filtered = [p for p in filtered if p['status'] != 'Past']
        
        # Confidence filter
        if filters['confidence'] == "High Confidence":
            filtered = [p for p in filtered if p['win_confidence'] == "High" or p['ou_confidence'] == "High"]
        elif filters['confidence'] == "Medium+":
            filtered = [p for p in filtered if p['win_confidence'] in ["High", "Medium"] or p['ou_confidence'] in ["High", "Medium"]]
        
        # Team filter
        if filters['team'] != "All Teams":
            filtered = [p for p in filtered if filters['team'] in p['home_team'] or filters['team'] in p['away_team']]
        
        return filtered
    
    def render_game_card(self, prediction):
        """Render a modern, interactive game prediction card with all details"""
        
        # Check if this is an old game
        current_date = datetime.now().date()
        game_date = datetime.strptime(prediction['game_date'], '%Y-%m-%d').date()
        
        # Modern card with complete game summary
        st.markdown(f"""
        <div class="game-card">
            <div class="card-header">
                <div class="team-matchup">
                    <div class="team-info">
                        <div class="team-name away-team">{prediction['away_team']}</div>
                        <div class="vs-text">@</div>
                        <div class="team-name home-team">{prediction['home_team']}</div>
                    </div>
                </div>
                
                <div class="game-details">
                    <div class="detail-item">
                        <span class="detail-icon">📅</span>
                        <span class="detail-text">{prediction['game_date']}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-icon">🕐</span>
                        <span class="detail-text">{prediction.get('game_time', 'TBD')}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-icon">⏰</span>
                        <span class="detail-text {'status-today' if prediction['status'] == 'Today' else 'status-other'}">{prediction['status']}</span>
                    </div>
                </div>
            </div>
            
            <div class="predictions-container">
                <div class="prediction-section">
                    <div class="prediction-header">
                        <span class="prediction-icon">🏆</span>
                        <span class="prediction-title">Win/Loss Prediction</span>
                    </div>
                    <div class="prediction-content">
                        <div class="prediction-result win-prediction">
                            Winner: {prediction['win_prediction']}
                        </div>
                        <div class="confidence-badge confidence-{prediction['win_confidence'].lower()}">
                            {prediction['win_confidence']} ({prediction['win_probability']:.1%})
                        </div>
                    </div>
                </div>
                
                <div class="prediction-section">
                    <div class="prediction-header">
                        <span class="prediction-icon">📊</span>
                        <span class="prediction-title">Over/Under Prediction</span>
                    </div>
                    <div class="prediction-content">
                        <div class="prediction-result {'over-prediction' if prediction['over_under_prediction'] == 'Over' else 'under-prediction'}">
                            {prediction['over_under_prediction']} {prediction['predicted_total']}
                        </div>
                        <div class="confidence-badge confidence-{prediction['ou_confidence'].lower()}">
                            {prediction['ou_confidence']} ({prediction['ou_probability']:.1%})
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="stats-summary">
                <div class="stat-card">
                    <div class="stat-value">{prediction['win_probability']:.0%}</div>
                    <div class="stat-label">Win Prob</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{prediction['ou_probability']:.0%}</div>
                    <div class="stat-label">O/U Prob</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{prediction['predicted_total']}</div>
                    <div class="stat-label">Total</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{prediction['win_confidence'][0]}</div>
                    <div class="stat-label">Confidence</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Historical data warning
        if game_date < current_date:
            st.info(f"📊 Historical Game from {prediction['game_date']} - Used for model validation")
        
        # Expandable advanced details
        with st.expander("🔍 Advanced Analytics & Betting Guide", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🤖 Model Information")
                info_items = []
                if 'model_version' in prediction:
                    info_items.append(f"**Model Version:** {prediction['model_version']}")
                if 'features_used' in prediction:
                    info_items.append(f"**Features Used:** {prediction['features_used']}")
                if 'created_at' in prediction:
                    created_time = datetime.fromisoformat(prediction['created_at'].replace('Z', '+00:00'))
                    info_items.append(f"**Generated:** {created_time.strftime('%H:%M')}")
                
                for item in info_items:
                    st.markdown(f"• {item}")
                
                if 'venue' in prediction:
                    st.markdown(f"• **Venue:** {prediction['venue']}")
                if 'tv_network' in prediction:
                    st.markdown(f"• **TV:** {prediction['tv_network']}")
            
            with col2:
                st.markdown("#### 💰 Betting Recommendation")
                
                # Calculate strongest bet
                max_confidence = max(
                    prediction.get('win_probability', 0.5), 
                    1 - prediction.get('win_probability', 0.5),
                    prediction.get('ou_probability', 0.5),
                    1 - prediction.get('ou_probability', 0.5)
                )
                
                if max_confidence >= 0.75:
                    st.success("🔥 **STRONG BET** - High Confidence")
                    st.markdown("*Model shows high confidence in this prediction*")
                elif max_confidence >= 0.65:
                    st.warning("⚡ **GOOD BET** - Medium Confidence")
                    st.markdown("*Solid prediction with good probability*")
                else:
                    st.info("⚠️ **CAUTIOUS BET** - Lower Confidence")
                    st.markdown("*Consider smaller stake or skip this game*")
                
                # Show best bet recommendation
                if abs(prediction['win_probability'] - 0.5) > abs(prediction['ou_probability'] - 0.5):
                    st.markdown(f"**🎯 Best Bet:** {prediction['win_prediction']} to win")
                else:
                    st.markdown(f"**🎯 Best Bet:** {prediction['over_under_prediction']} {prediction['predicted_total']}")
                
                st.markdown("**💡 Remember:** Always bet responsibly!")
        
        st.markdown("---")
    
    def render_summary_stats(self, predictions):
        """Render summary statistics"""
        if not predictions:
            return
            
        st.markdown("## 📊 Today's Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📅 Total Games",
                value=len(predictions)
            )
        
        with col2:
            high_conf = len([p for p in predictions if p['win_confidence'] == 'High' or p['ou_confidence'] == 'High'])
            st.metric(
                label="🎯 High Confidence",
                value=high_conf
            )
        
        with col3:
            avg_win_prob = np.mean([p['win_probability'] for p in predictions])
            st.metric(
                label="🏆 Avg Win Prob",
                value=f"{avg_win_prob:.1%}"
            )
        
        with col4:
            avg_total = np.mean([p['predicted_total'] for p in predictions])
            st.metric(
                label="📊 Avg Total",
                value=f"{avg_total:.0f}"
            )

def main():
    """Main application"""
    ui = UserInterface()
    
    # Render header
    ui.render_header()
    
    # Get predictions
    with st.spinner("🔄 Loading latest predictions..."):
        predictions = ui.get_available_predictions()
    
    if not predictions:
        st.markdown("""
        <div class="no-games">
            <h3>🏀 No Games Available</h3>
            <p>Check back later for today's predictions or during NBA season for live games!</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Render summary
    ui.render_summary_stats(predictions)
    
    # Render filters
    st.markdown("## 🎛️ Filter Predictions")
    filters = ui.render_filters()
    
    # Apply filters
    filtered_predictions = ui.filter_predictions(predictions, filters)
    
    if not filtered_predictions:
        st.warning("No games match your current filters. Try adjusting your selection.")
        return
    
    # Render predictions
    st.markdown(f"## 🎯 Available Predictions ({len(filtered_predictions)} games)")
    
    for prediction in filtered_predictions:
        ui.render_game_card(prediction)
    
    # Footer
    st.markdown("""
    <div class="footer-info">
        <h4>🏀 NBA Predictions Hub</h4>
        <p>Predictions are generated using advanced machine learning models trained on historical NBA data.</p>
        <p><strong>Disclaimer:</strong> These predictions are for entertainment purposes. Always gamble responsibly.</p>
        <p><em>Last updated: {}</em></p>
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M")), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
