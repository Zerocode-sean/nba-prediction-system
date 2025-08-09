"""
🔴 Real-Time NBA Prediction Interface
===================================

Live NBA predictions using real data when available.
This is where the model faces the real world!
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.prediction.realtime_system import RealTimeNBASystem, RealTimeValidation

# Page configuration
st.set_page_config(
    page_title="🔴 Real-Time NBA Predictions",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .live-indicator {
        background: linear-gradient(90deg, #ff4444 0%, #ff6666 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        text-align: center;
        font-weight: bold;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .real-game-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #ff4444;
    }
    
    .accuracy-high {
        color: #2ca02c;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .accuracy-medium {
        color: #ff9800;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .accuracy-low {
        color: #d62728;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .season-status {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def init_real_time_session():
    """Initialize real-time session state"""
    if 'real_time_system' not in st.session_state:
        st.session_state.real_time_system = RealTimeNBASystem()
    if 'real_time_validator' not in st.session_state:
        st.session_state.real_time_validator = RealTimeValidation()
    if 'todays_predictions' not in st.session_state:
        st.session_state.todays_predictions = []
    if 'validation_results' not in st.session_state:
        st.session_state.validation_results = {}

def render_real_time_header():
    """Render real-time header with live indicators"""
    st.markdown("""
    <div class="live-indicator">
        🔴 REAL-TIME NBA PREDICTIONS - LIVE DATA MODE
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

def render_season_status():
    """Display current NBA season status"""
    system = st.session_state.real_time_system
    status = system.get_season_status()
    
    st.markdown("## 📅 NBA Season Status")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Current Season",
            value=status['current_season']
        )
    
    with col2:
        season_emoji = "🔴" if status['is_season_active'] else "🏖️"
        season_text = "Active" if status['is_season_active'] else "Off-Season"
        st.metric(
            label="Season Status",
            value=f"{season_emoji} {season_text}"
        )
    
    with col3:
        st.metric(
            label="Games Today",
            value=status['todays_games_count']
        )
    
    with col4:
        st.metric(
            label="Current Date",
            value=status['current_date']
        )
    
    # Status message
    st.markdown(f"""
    <div class="season-status">
        <h4>{status['status_message']}</h4>
    </div>
    """, unsafe_allow_html=True)

def render_todays_games():
    """Display today's games and predictions"""
    st.markdown("## 🎯 Today's NBA Games & Predictions")
    
    system = st.session_state.real_time_system
    
    # Get today's games
    with st.spinner("🔄 Loading today's games..."):
        todays_games = system.get_todays_games()
    
    if not todays_games:
        st.info("📅 No NBA games scheduled for today")
        return
    
    # Create predictions for today's games
    if st.button("🎯 Generate Real-Time Predictions", type="primary"):
        with st.spinner("🤖 Analyzing today's matchups with real data..."):
            predictions = system.create_real_time_predictions(todays_games)
            st.session_state.todays_predictions = predictions
            st.success(f"✅ Generated predictions for {len(predictions)} games!")
            st.rerun()
    
    # Display predictions
    if st.session_state.todays_predictions:
        for prediction in st.session_state.todays_predictions:
            render_real_time_prediction_card(prediction)
    else:
        st.info("Click the button above to generate predictions for today's games")

def render_real_time_prediction_card(prediction):
    """Render prediction card with real game info"""
    
    matchup = prediction['matchup']
    win_loss = prediction['win_loss']
    over_under = prediction['over_under']
    real_info = prediction.get('real_game_info', {})
    actual_results = prediction.get('actual_results')
    accuracy = prediction.get('accuracy', {})
    
    with st.container():
        st.markdown('<div class="real-game-card">', unsafe_allow_html=True)
        
        # Game header with real info
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown(f"""
            ### 🏠 {matchup['home_team']}
            **HOME**
            """)
            
        with col2:
            game_time = real_info.get('date', 'TBD')
            status = real_info.get('status', 'Scheduled')
            
            st.markdown(f"""
            ### VS
            **{status}**
            *{game_time}*
            """)
            
        with col3:
            st.markdown(f"""
            ### ✈️ {matchup['away_team']}
            **AWAY**
            """)
        
        # Real game details
        if real_info:
            st.markdown("**📍 Game Details:**")
            detail_col1, detail_col2, detail_col3 = st.columns(3)
            
            with detail_col1:
                st.write(f"🏟️ **Venue:** {real_info.get('venue', 'TBD')}")
            
            with detail_col2:
                st.write(f"📺 **Broadcast:** {real_info.get('broadcast', 'TBD')}")
            
            with detail_col3:
                st.write(f"🆔 **Game ID:** {real_info.get('game_id', 'N/A')}")
        
        st.markdown("---")
        
        # Predictions vs Actual Results
        pred_col1, pred_col2 = st.columns(2)
        
        with pred_col1:
            st.markdown("### 🏆 WIN/LOSS PREDICTION")
            
            winner = "HOME" if win_loss['prediction'] == 'HOME' else "AWAY"
            winner_team = matchup['home_team'] if winner == "HOME" else matchup['away_team']
            confidence = win_loss['confidence']
            
            st.markdown(f"""
            **🎯 PREDICTED WINNER:** {winner_team}  
            **🎲 CONFIDENCE:** {confidence:.1%}
            """)
            
            # Show actual result if available
            if actual_results:
                actual_winner = matchup['home_team'] if actual_results['home_win'] else matchup['away_team']
                is_correct = accuracy.get('win_loss_correct', False)
                correct_emoji = "✅" if is_correct else "❌"
                
                st.markdown(f"""
                **🏆 ACTUAL WINNER:** {actual_winner} {correct_emoji}  
                **📊 FINAL SCORE:** {actual_results['home_score']} - {actual_results['away_score']}
                """)
        
        with pred_col2:
            st.markdown("### 📈 OVER/UNDER PREDICTION")
            
            ou_prediction = over_under['prediction']
            ou_confidence = over_under['confidence']
            line = over_under['line']
            
            st.markdown(f"""
            **🎯 PREDICTION:** {ou_prediction} {line}  
            **🎲 CONFIDENCE:** {ou_confidence:.1%}
            """)
            
            # Show actual result if available
            if actual_results:
                actual_total = actual_results['total_score']
                actual_ou = "OVER" if actual_results['over_235'] else "UNDER"
                is_correct = accuracy.get('over_under_correct', False)
                correct_emoji = "✅" if is_correct else "❌"
                
                st.markdown(f"""
                **📊 ACTUAL TOTAL:** {actual_total} points {correct_emoji}  
                **🎯 RESULT:** {actual_ou} {line}
                """)
        
        # Overall accuracy if game is complete
        if accuracy:
            st.markdown("---")
            st.markdown("### 🎯 PREDICTION ACCURACY")
            
            acc_col1, acc_col2, acc_col3 = st.columns(3)
            
            with acc_col1:
                wl_correct = accuracy.get('win_loss_correct', False)
                wl_emoji = "✅" if wl_correct else "❌"
                st.markdown(f"**🏆 Win/Loss:** {wl_emoji} {'Correct' if wl_correct else 'Incorrect'}")
            
            with acc_col2:
                ou_correct = accuracy.get('over_under_correct', False)
                ou_emoji = "✅" if ou_correct else "❌"
                st.markdown(f"**📈 Over/Under:** {ou_emoji} {'Correct' if ou_correct else 'Incorrect'}")
            
            with acc_col3:
                both_correct = accuracy.get('both_correct', False)
                both_emoji = "🎯" if both_correct else "⚠️"
                st.markdown(f"**🎪 Both Correct:** {both_emoji} {'Yes' if both_correct else 'No'}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_recent_validation():
    """Display recent prediction validation results"""
    st.markdown("## 🔍 Recent Prediction Validation")
    
    validator = st.session_state.real_time_validator
    
    # Validation controls
    days_back = st.selectbox("Validation Period", [3, 7, 14, 30], index=1)
    
    if st.button("🔍 Validate Recent Predictions", type="secondary"):
        with st.spinner(f"🔄 Analyzing predictions from last {days_back} days..."):
            results = validator.validate_recent_predictions(days_back)
            st.session_state.validation_results = results
            st.rerun()
    
    # Display validation results
    if st.session_state.validation_results:
        results = st.session_state.validation_results
        
        if results['status'] == 'success':
            # Overall accuracy metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="Games Analyzed",
                    value=results['total_games']
                )
            
            with col2:
                wl_acc = results['win_loss_accuracy']
                wl_class = "accuracy-high" if wl_acc >= 0.6 else "accuracy-medium" if wl_acc >= 0.5 else "accuracy-low"
                st.markdown(f"""
                <div class="{wl_class}">
                    Win/Loss Accuracy<br>
                    {wl_acc:.1%}
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                ou_acc = results['over_under_accuracy']
                ou_class = "accuracy-high" if ou_acc >= 0.55 else "accuracy-medium" if ou_acc >= 0.45 else "accuracy-low"
                st.markdown(f"""
                <div class="{ou_class}">
                    Over/Under Accuracy<br>
                    {ou_acc:.1%}
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                both_acc = results['both_correct_rate']
                both_class = "accuracy-high" if both_acc >= 0.4 else "accuracy-medium" if both_acc >= 0.25 else "accuracy-low"
                st.markdown(f"""
                <div class="{both_class}">
                    Both Correct<br>
                    {both_acc:.1%}
                </div>
                """, unsafe_allow_html=True)
            
            # Show detailed results
            st.markdown("### 📊 Detailed Validation Results")
            
            with st.expander("View Individual Game Results", expanded=False):
                for pred in results['predictions_with_results'][:10]:  # Show first 10
                    render_real_time_prediction_card(pred)
        
        else:
            st.warning(f"⚠️ {results['message']}")

def render_real_time_sidebar():
    """Render sidebar for real-time interface"""
    st.sidebar.markdown("## 🔴 Real-Time Mode")
    st.sidebar.markdown("---")
    
    # Data source indicator
    system = st.session_state.real_time_system
    status = system.get_season_status()
    
    if status['is_season_active']:
        st.sidebar.success("🔴 LIVE NBA DATA")
        st.sidebar.markdown("Using real NBA API data")
    else:
        st.sidebar.warning("🏖️ OFF-SEASON MODE")
        st.sidebar.markdown("Using recent historical data")
    
    st.sidebar.markdown("---")
    
    # Quick actions
    st.sidebar.markdown("### ⚡ Quick Actions")
    
    if st.sidebar.button("🔄 Refresh Data"):
        # Clear cached data
        for key in ['todays_predictions', 'validation_results']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    if st.sidebar.button("📊 Check Live Scores"):
        with st.spinner("Getting live scores..."):
            live_games = system.get_live_scores()
            if live_games:
                st.sidebar.success(f"🔴 {len(live_games)} games live now!")
            else:
                st.sidebar.info("No games currently in progress")
    
    st.sidebar.markdown("---")
    
    # Real-time stats
    st.sidebar.markdown("### 📈 Real-Time Stats")
    
    if st.session_state.validation_results:
        results = st.session_state.validation_results
        if results.get('status') == 'success':
            st.sidebar.metric("Recent Accuracy", f"{results['win_loss_accuracy']:.1%}")
            st.sidebar.metric("Games Analyzed", results['total_games'])
    
    st.sidebar.markdown("---")
    
    # About real-time mode
    st.sidebar.info("""
    **🔴 Real-Time Mode Features:**
    
    ✅ Live NBA game data  
    ✅ Real game predictions  
    ✅ Actual result validation  
    ✅ Performance tracking  
    ✅ Live score updates  
    
    **This is where your model faces the real world!**
    """)

def main():
    """Main real-time prediction interface"""
    
    # Initialize
    init_real_time_session()
    
    # Header
    render_real_time_header()
    
    # Sidebar
    render_real_time_sidebar()
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Today's Games", "🔍 Validation", "📊 Performance"])
    
    with tab1:
        render_season_status()
        render_todays_games()
    
    with tab2:
        render_recent_validation()
    
    with tab3:
        st.markdown("## 📊 Real-Time Performance Tracking")
        
        if st.session_state.validation_results:
            results = st.session_state.validation_results
            
            if results.get('status') == 'success':
                # Performance visualization
                games_data = []
                for pred in results['predictions_with_results']:
                    if 'accuracy' in pred:
                        games_data.append({
                            'Game': f"{pred['matchup']['away_team']} @ {pred['matchup']['home_team']}",
                            'Win/Loss Correct': pred['accuracy'].get('win_loss_correct', False),
                            'Over/Under Correct': pred['accuracy'].get('over_under_correct', False),
                            'WL Confidence': pred['accuracy'].get('win_loss_confidence', 0),
                            'OU Confidence': pred['accuracy'].get('over_under_confidence', 0)
                        })
                
                if games_data:
                    df = pd.DataFrame(games_data)
                    
                    # Accuracy by confidence level
                    fig = go.Figure()
                    
                    # Win/Loss accuracy
                    fig.add_trace(go.Scatter(
                        x=df['WL Confidence'],
                        y=df['Win/Loss Correct'].astype(int),
                        mode='markers',
                        name='Win/Loss Accuracy',
                        marker=dict(size=10, color='blue')
                    ))
                    
                    # Over/Under accuracy
                    fig.add_trace(go.Scatter(
                        x=df['OU Confidence'],
                        y=df['Over/Under Correct'].astype(int),
                        mode='markers',
                        name='Over/Under Accuracy',
                        marker=dict(size=10, color='orange')
                    ))
                    
                    fig.update_layout(
                        title="Prediction Accuracy vs Confidence Level",
                        xaxis_title="Confidence Level",
                        yaxis_title="Correct (1) / Incorrect (0)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("Run validation to see performance metrics")

if __name__ == "__main__":
    main()
