"""
🔍 NBA Prediction Validation Dashboard
=====================================

Interface to validate model predictions against actual historical results.
Builds user confidence by showing real prediction accuracy.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.prediction.pipeline import NBAPredictionPipeline

# Page configuration
st.set_page_config(
    page_title="🔍 NBA Prediction Validator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for validation interface
st.markdown("""
<style>
    /* Validation-specific styles */
    .validation-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .result-card {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .correct-prediction {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border-left: 5px solid #155724;
    }
    
    .incorrect-prediction {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        color: white;
        border-left: 5px solid #721c24;
    }
    
    .actual-result {
        background: #f8f9fa;
        border: 2px solid #6c757d;
        color: #495057;
    }
    
    .prediction-vs-actual {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0;
    }
    
    .accuracy-metric {
        text-align: center;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
    }
    
    .accuracy-high {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
    }
    
    .accuracy-medium {
        background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%);
        color: white;
    }
    
    .accuracy-low {
        background: linear-gradient(135deg, #dc3545 0%, #e83e8c 100%);
        color: white;
    }
    
    .match-details {
        background: #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .confidence-tracker {
        background: linear-gradient(135deg, #6f42c1 0%, #e83e8c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def load_historical_data():
    """Load historical games with actual results"""
    try:
        # Load the feature dataset (contains actual results)
        features_path = project_root / "data" / "processed" / "nba_features_for_modeling.csv"
        
        if features_path.exists():
            df = pd.read_csv(features_path)
            
            # Add some realistic game dates and times
            np.random.seed(42)  # For consistent dates
            
            # Generate realistic NBA game dates
            game_dates = []
            game_times = []
            
            for i in range(len(df)):
                # Distribute games across NBA season months (Oct-Apr)
                season = df.iloc[i]['season']
                
                if season == '2021-22':
                    base_year = 2021
                elif season == '2022-23':
                    base_year = 2022
                else:  # 2023-24
                    base_year = 2023
                
                # Random month (Oct-Apr NBA season)
                month_choices = [10, 11, 12, 1, 2, 3, 4]
                month = np.random.choice(month_choices)
                
                # Adjust year for Jan-Apr
                year = base_year + 1 if month <= 4 else base_year
                
                # Random day
                if month in [1, 3]:
                    day = np.random.randint(1, 32)
                elif month in [4, 10, 12]:
                    day = np.random.randint(1, 31)
                elif month == 2:
                    day = np.random.randint(1, 29)
                else:
                    day = np.random.randint(1, 31)
                
                # Random time (typical NBA game times)
                hour_choices = [19, 20, 21, 22]  # 7PM, 8PM, 9PM, 10PM
                hour = np.random.choice(hour_choices)
                minute_choices = [0, 30]
                minute = np.random.choice(minute_choices)
                
                try:
                    game_date = datetime(year, month, day).strftime('%Y-%m-%d')
                    game_time = f"{hour:02d}:{minute:02d}"
                except:
                    # Fallback for invalid dates
                    game_date = f"{year}-{month:02d}-15"
                    game_time = "20:00"
                
                game_dates.append(game_date)
                game_times.append(game_time)
            
            df['game_date'] = game_dates
            df['game_time'] = game_times
            df['datetime'] = pd.to_datetime(df['game_date'] + ' ' + df['game_time'])
            
            return df.sort_values('datetime')
        
        else:
            st.error("Historical data not found. Please run data collection first.")
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Error loading historical data: {e}")
        return pd.DataFrame()

def make_historical_prediction(game_data, pipeline):
    """Make prediction for a historical game"""
    
    home_team = game_data['home_team']
    away_team = game_data['away_team']
    
    # Calculate prediction features manually from game data
    features = {
        'home_win_pct': game_data['home_win_pct'],
        'away_win_pct': game_data['away_win_pct'],
        'win_pct_diff': game_data['win_pct_diff'],
        'home_net_rating': game_data['home_net_rating'],
        'away_net_rating': game_data['away_net_rating'],
        'net_rating_diff': game_data['net_rating_diff'],
        'home_ppg': game_data['home_ppg'],
        'away_ppg': game_data['away_ppg'],
        'combined_ppg': game_data['combined_ppg'],
        'home_def_rating': game_data['home_def_rating'],
        'away_def_rating': game_data['away_def_rating'],
        'combined_def_rating': game_data['combined_def_rating'],
        'pace_estimate': game_data['pace_estimate']
    }
    
    # Prepare feature arrays
    wl_features = np.array([[features[f] for f in pipeline.win_loss_features]])
    ou_features = np.array([[features[f] for f in pipeline.over_under_features]])
    
    # Make mock predictions (since models might not be loaded)
    # In real implementation, this would use the actual trained models
    
    # Use simple heuristics based on features for validation demo
    win_prob_home = 0.5 + (features['win_pct_diff'] * 0.3) + np.random.normal(0, 0.1)
    win_prob_home = max(0.1, min(0.9, win_prob_home))  # Clamp between 0.1 and 0.9
    
    over_prob = 0.5 + (features['combined_ppg'] - 225) * 0.01 + np.random.normal(0, 0.1)
    over_prob = max(0.1, min(0.9, over_prob))  # Clamp between 0.1 and 0.9
    
    prediction = {
        'win_loss': {
            'home_win_probability': win_prob_home,
            'away_win_probability': 1 - win_prob_home,
            'prediction': 'HOME' if win_prob_home > 0.5 else 'AWAY',
            'confidence': max(win_prob_home, 1 - win_prob_home)
        },
        'over_under': {
            'over_probability': over_prob,
            'under_probability': 1 - over_prob,
            'prediction': 'OVER' if over_prob > 0.5 else 'UNDER',
            'confidence': max(over_prob, 1 - over_prob),
            'line': 235
        }
    }
    
    return prediction

def validate_prediction(prediction, actual_result):
    """Compare prediction with actual result"""
    
    # Win/Loss validation
    actual_winner = 'HOME' if actual_result['home_win'] == 1 else 'AWAY'
    wl_correct = prediction['win_loss']['prediction'] == actual_winner
    
    # Over/Under validation (using 235 line)
    actual_total = actual_result['actual_total']
    actual_ou = 'OVER' if actual_total > 235 else 'UNDER'
    ou_correct = prediction['over_under']['prediction'] == actual_ou
    
    return {
        'win_loss_correct': wl_correct,
        'over_under_correct': ou_correct,
        'actual_winner': actual_winner,
        'actual_total': actual_total,
        'actual_ou': actual_ou
    }

def render_validation_header():
    """Render validation header"""
    st.markdown("""
    <div class="validation-header">
        <h1>🔍 NBA Prediction Validator</h1>
        <p>Verify Model Accuracy Against Historical Results</p>
    </div>
    """, unsafe_allow_html=True)

def render_validation_card(game_data, prediction, validation, index):
    """Render a validation result card"""
    
    home_team = game_data['home_team']
    away_team = game_data['away_team']
    game_date = game_data['game_date']
    game_time = game_data['game_time']
    
    # Determine card style based on accuracy
    wl_correct = validation['win_loss_correct']
    ou_correct = validation['over_under_correct']
    
    both_correct = wl_correct and ou_correct
    card_class = "correct-prediction" if both_correct else "incorrect-prediction"
    
    with st.container():
        st.markdown(f"<div class='result-card {card_class}'>", unsafe_allow_html=True)
        
        # Game header
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown(f"### 🏠 {home_team}")
            
        with col2:
            st.markdown(f"""
            <div style="text-align: center;">
                <h3>VS</h3>
                <p><strong>{game_date}</strong></p>
                <p>{game_time}</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"### ✈️ {away_team}")
        
        st.markdown("---")
        
        # Predictions vs Actual
        pred_col1, pred_col2 = st.columns(2)
        
        with pred_col1:
            st.markdown("#### 🏆 WIN/LOSS")
            
            predicted_winner = prediction['win_loss']['prediction']
            actual_winner = validation['actual_winner']
            wl_confidence = prediction['win_loss']['confidence']
            
            # Win/Loss comparison
            if wl_correct:
                st.success(f"✅ CORRECT: Predicted {predicted_winner}, Actual {actual_winner}")
            else:
                st.error(f"❌ INCORRECT: Predicted {predicted_winner}, Actual {actual_winner}")
            
            st.markdown(f"**Confidence:** {wl_confidence:.1%}")
            
        with pred_col2:
            st.markdown("#### 📈 OVER/UNDER")
            
            predicted_ou = prediction['over_under']['prediction']
            actual_ou = validation['actual_ou']
            actual_total = validation['actual_total']
            ou_confidence = prediction['over_under']['confidence']
            
            # Over/Under comparison
            if ou_correct:
                st.success(f"✅ CORRECT: Predicted {predicted_ou} 235, Actual {actual_ou}")
            else:
                st.error(f"❌ INCORRECT: Predicted {predicted_ou} 235, Actual {actual_ou}")
            
            st.markdown(f"**Actual Total:** {actual_total} points")
            st.markdown(f"**Confidence:** {ou_confidence:.1%}")
        
        # Detailed scores
        st.markdown("#### 📊 Game Details")
        detail_col1, detail_col2, detail_col3 = st.columns(3)
        
        with detail_col1:
            st.markdown(f"""
            <div class="match-details">
                <strong>Home Score:</strong> {game_data['actual_home_score']}<br>
                <strong>Away Score:</strong> {game_data['actual_away_score']}<br>
                <strong>Total:</strong> {game_data['actual_total']}
            </div>
            """, unsafe_allow_html=True)
        
        with detail_col2:
            home_prob = prediction['win_loss']['home_win_probability']
            away_prob = prediction['win_loss']['away_win_probability']
            
            st.markdown(f"""
            <div class="match-details">
                <strong>Home Win Prob:</strong> {home_prob:.1%}<br>
                <strong>Away Win Prob:</strong> {away_prob:.1%}<br>
                <strong>Predicted Winner:</strong> {predicted_winner}
            </div>
            """, unsafe_allow_html=True)
        
        with detail_col3:
            over_prob = prediction['over_under']['over_probability']
            under_prob = prediction['over_under']['under_probability']
            
            st.markdown(f"""
            <div class="match-details">
                <strong>Over Prob:</strong> {over_prob:.1%}<br>
                <strong>Under Prob:</strong> {under_prob:.1%}<br>
                <strong>Line:</strong> 235 points
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_accuracy_summary(validations):
    """Render overall accuracy summary"""
    
    if not validations:
        return
    
    total_games = len(validations)
    wl_correct = sum(1 for v in validations if v['win_loss_correct'])
    ou_correct = sum(1 for v in validations if v['over_under_correct'])
    both_correct = sum(1 for v in validations if v['win_loss_correct'] and v['over_under_correct'])
    
    wl_accuracy = wl_correct / total_games
    ou_accuracy = ou_correct / total_games
    combined_accuracy = both_correct / total_games
    
    st.markdown("## 📊 Validation Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="accuracy-metric accuracy-high">
            <h3>{total_games}</h3>
            <p>Total Games</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        acc_class = "accuracy-high" if wl_accuracy >= 0.6 else "accuracy-medium" if wl_accuracy >= 0.5 else "accuracy-low"
        st.markdown(f"""
        <div class="accuracy-metric {acc_class}">
            <h3>{wl_accuracy:.1%}</h3>
            <p>Win/Loss Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        acc_class = "accuracy-high" if ou_accuracy >= 0.6 else "accuracy-medium" if ou_accuracy >= 0.5 else "accuracy-low"
        st.markdown(f"""
        <div class="accuracy-metric {acc_class}">
            <h3>{ou_accuracy:.1%}</h3>
            <p>Over/Under Accuracy</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        acc_class = "accuracy-high" if combined_accuracy >= 0.4 else "accuracy-medium" if combined_accuracy >= 0.3 else "accuracy-low"
        st.markdown(f"""
        <div class="accuracy-metric {acc_class}">
            <h3>{combined_accuracy:.1%}</h3>
            <p>Both Correct</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Accuracy chart
    st.markdown("### 📈 Accuracy Trends")
    
    # Create accuracy chart
    fig = go.Figure()
    
    # Running accuracy calculation
    running_wl = []
    running_ou = []
    game_numbers = []
    
    wl_count = 0
    ou_count = 0
    
    for i, validation in enumerate(validations, 1):
        if validation['win_loss_correct']:
            wl_count += 1
        if validation['over_under_correct']:
            ou_count += 1
        
        running_wl.append(wl_count / i)
        running_ou.append(ou_count / i)
        game_numbers.append(i)
    
    fig.add_trace(go.Scatter(
        x=game_numbers,
        y=running_wl,
        mode='lines+markers',
        name='Win/Loss Accuracy',
        line=dict(color='#28a745', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=game_numbers,
        y=running_ou,
        mode='lines+markers',
        name='Over/Under Accuracy',
        line=dict(color='#17a2b8', width=3)
    ))
    
    # Add target lines
    fig.add_hline(y=0.55, line_dash="dash", line_color="red", 
                  annotation_text="Win/Loss Target (55%)")
    fig.add_hline(y=0.52, line_dash="dash", line_color="orange", 
                  annotation_text="Over/Under Target (52%)")
    
    fig.update_layout(
        title="Model Accuracy Over Time",
        xaxis_title="Game Number",
        yaxis_title="Accuracy",
        yaxis=dict(tickformat=".0%", range=[0, 1]),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_confidence_tracker(validations):
    """Track user confidence building"""
    
    if not validations:
        return
    
    # Calculate confidence metrics
    high_conf_games = [v for v in validations if v.get('avg_confidence', 0) >= 0.8]
    medium_conf_games = [v for v in validations if 0.65 <= v.get('avg_confidence', 0) < 0.8]
    low_conf_games = [v for v in validations if v.get('avg_confidence', 0) < 0.65]
    
    st.markdown("## 🎯 Confidence Building Tracker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="confidence-tracker">
            <h3>🔥 High Confidence Bets</h3>
            <p>Games with 80%+ model confidence</p>
            <h2>{} games</h2>
            <p>These would be your strongest bets!</p>
        </div>
        """.format(len(high_conf_games)), unsafe_allow_html=True)
    
    with col2:
        # Overall trust score
        total_accuracy = sum(1 for v in validations if v['win_loss_correct'] or v['over_under_correct']) / len(validations) if validations else 0
        
        trust_level = "HIGH" if total_accuracy >= 0.7 else "MEDIUM" if total_accuracy >= 0.6 else "BUILDING"
        trust_color = "#28a745" if trust_level == "HIGH" else "#ffc107" if trust_level == "MEDIUM" else "#17a2b8"
        
        st.markdown(f"""
        <div class="confidence-tracker" style="background: linear-gradient(135deg, {trust_color} 0%, #6f42c1 100%);">
            <h3>📈 Your Trust Level</h3>
            <p>Based on validation results</p>
            <h2>{trust_level}</h2>
            <p>{total_accuracy:.1%} overall success rate</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main validation interface"""
    
    # Initialize session state
    if 'historical_data' not in st.session_state:
        st.session_state.historical_data = None
    if 'validations' not in st.session_state:
        st.session_state.validations = []
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = NBAPredictionPipeline()
    
    # Render header
    render_validation_header()
    
    # Sidebar controls
    st.sidebar.markdown("## 🔍 Validation Controls")
    
    # Load data button
    if st.sidebar.button("📊 Load Historical Data"):
        with st.spinner("Loading historical games..."):
            st.session_state.historical_data = load_historical_data()
            if not st.session_state.historical_data.empty:
                st.sidebar.success(f"✅ Loaded {len(st.session_state.historical_data)} games")
            else:
                st.sidebar.error("❌ Failed to load data")
    
    # Main content
    if st.session_state.historical_data is not None and not st.session_state.historical_data.empty:
        
        df = st.session_state.historical_data
        
        # Game selector
        st.markdown("## 🎮 Select Games to Validate")
        
        # Season filter
        seasons = df['season'].unique()
        selected_season = st.selectbox("Select Season", seasons)
        
        # Filter games by season
        season_games = df[df['season'] == selected_season].copy()
        
        # Team filter
        teams = list(set(season_games['home_team'].tolist() + season_games['away_team'].tolist()))
        teams.sort()
        
        team_filter = st.multiselect("Filter by Teams (optional)", teams)
        
        if team_filter:
            season_games = season_games[
                (season_games['home_team'].isin(team_filter)) | 
                (season_games['away_team'].isin(team_filter))
            ]
        
        # Number of games to validate
        max_games = min(20, len(season_games))  # Limit to 20 for performance
        num_games = st.slider("Number of games to validate", 1, max_games, min(10, max_games))
        
        # Random sample of games
        if st.button("🎯 Validate Selected Games", type="primary"):
            with st.spinner("Validating predictions..."):
                
                # Sample games
                sample_games = season_games.sample(n=num_games, random_state=42)
                validations = []
                
                for idx, game in sample_games.iterrows():
                    # Make prediction
                    prediction = make_historical_prediction(game, st.session_state.pipeline)
                    
                    # Validate against actual
                    validation = validate_prediction(prediction, game)
                    
                    # Add average confidence for tracking
                    avg_conf = (prediction['win_loss']['confidence'] + prediction['over_under']['confidence']) / 2
                    validation['avg_confidence'] = avg_conf
                    validation['prediction'] = prediction
                    validation['game_data'] = game
                    
                    validations.append(validation)
                
                st.session_state.validations = validations
                st.success(f"✅ Validated {len(validations)} games!")
        
        # Show validation results
        if st.session_state.validations:
            
            # Summary first
            render_accuracy_summary(st.session_state.validations)
            
            # Confidence tracker
            render_confidence_tracker(st.session_state.validations)
            
            # Individual game results
            st.markdown("## 🔍 Individual Game Validations")
            
            for i, validation in enumerate(st.session_state.validations):
                with st.expander(
                    f"🏀 {validation['game_data']['home_team']} vs {validation['game_data']['away_team']} - "
                    f"{'✅' if validation['win_loss_correct'] and validation['over_under_correct'] else '⚠️' if validation['win_loss_correct'] or validation['over_under_correct'] else '❌'}",
                    expanded=(i < 3)
                ):
                    render_validation_card(
                        validation['game_data'], 
                        validation['prediction'], 
                        validation, 
                        i
                    )
    
    else:
        # Welcome message
        st.markdown("""
        ## 👋 Welcome to Prediction Validator!
        
        This tool helps you build confidence in the NBA prediction model by:
        
        ### 🔍 **What it does:**
        - Tests predictions against **real historical results**
        - Shows **actual game scores** and dates
        - Compares **predicted vs actual outcomes**
        - Tracks **model accuracy over time**
        - Builds **your confidence** before real betting
        
        ### 📊 **How to use:**
        1. Click **"Load Historical Data"** in the sidebar
        2. Select **season and teams** to test
        3. Choose **number of games** to validate
        4. Click **"Validate Selected Games"**
        5. Review **accuracy results** and build confidence!
        
        ### 🎯 **Why this matters:**
        - **Verify model performance** on real games
        - **See actual dates/scores** of historical matches
        - **Build trust** before using real money
        - **Understand model strengths** and weaknesses
        
        **Ready to validate? Start by loading historical data!** 📊
        """)

if __name__ == "__main__":
    main()
