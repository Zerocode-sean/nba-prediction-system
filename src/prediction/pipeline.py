"""
NBA Prediction Pipeline
======================

This module provides a clean interface for making NBA game predictions
using the trained models. Designed for easy integration with web interfaces.
"""

import pandas as pd
import numpy as np
import pickle
import joblib
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, List, Optional
import warnings
warnings.filterwarnings('ignore')

class NBAPredictionPipeline:
    """
    NBA Prediction Pipeline for Win/Loss and Over/Under predictions
    """
    
    def __init__(self, models_dir: Optional[Path] = None):
        """Initialize the prediction pipeline"""
        self.project_root = Path(__file__).parent.parent.parent
        self.models_dir = models_dir or self.project_root / "models"
        self.data_dir = self.project_root / "data"
        
        # Create models directory if it doesn't exist
        self.models_dir.mkdir(exist_ok=True)
        
        # Model placeholders
        self.win_loss_model = None
        self.over_under_model = None
        self.wl_scaler = None
        self.ou_scaler = None
        
        # Feature definitions
        self.win_loss_features = [
            'home_win_pct', 'away_win_pct', 'win_pct_diff',
            'home_net_rating', 'away_net_rating', 'net_rating_diff'
        ]
        
        self.over_under_features = [
            'home_ppg', 'away_ppg', 'combined_ppg',
            'home_def_rating', 'away_def_rating', 'combined_def_rating',
            'pace_estimate'
        ]
        
        # NBA team mappings for user-friendly display
        self.team_info = {
            'Atlanta Hawks': {'city': 'Atlanta', 'name': 'Hawks', 'color': '#E03A3E'},
            'Boston Celtics': {'city': 'Boston', 'name': 'Celtics', 'color': '#007A33'},
            'Brooklyn Nets': {'city': 'Brooklyn', 'name': 'Nets', 'color': '#000000'},
            'Charlotte Hornets': {'city': 'Charlotte', 'name': 'Hornets', 'color': '#1D1160'},
            'Chicago Bulls': {'city': 'Chicago', 'name': 'Bulls', 'color': '#CE1141'},
            'Cleveland Cavaliers': {'city': 'Cleveland', 'name': 'Cavaliers', 'color': '#860038'},
            'Dallas Mavericks': {'city': 'Dallas', 'name': 'Mavericks', 'color': '#00538C'},
            'Denver Nuggets': {'city': 'Denver', 'name': 'Nuggets', 'color': '#0E2240'},
            'Detroit Pistons': {'city': 'Detroit', 'name': 'Pistons', 'color': '#C8102E'},
            'Golden State Warriors': {'city': 'Golden State', 'name': 'Warriors', 'color': '#1D428A'},
            'Houston Rockets': {'city': 'Houston', 'name': 'Rockets', 'color': '#CE1141'},
            'Indiana Pacers': {'city': 'Indiana', 'name': 'Pacers', 'color': '#002D62'},
            'LA Clippers': {'city': 'LA', 'name': 'Clippers', 'color': '#C8102E'},
            'Los Angeles Lakers': {'city': 'Los Angeles', 'name': 'Lakers', 'color': '#552583'},
            'Memphis Grizzlies': {'city': 'Memphis', 'name': 'Grizzlies', 'color': '#5D76A9'},
            'Miami Heat': {'city': 'Miami', 'name': 'Heat', 'color': '#98002E'},
            'Milwaukee Bucks': {'city': 'Milwaukee', 'name': 'Bucks', 'color': '#00471B'},
            'Minnesota Timberwolves': {'city': 'Minnesota', 'name': 'Timberwolves', 'color': '#0C2340'},
            'New Orleans Pelicans': {'city': 'New Orleans', 'name': 'Pelicans', 'color': '#0C2340'},
            'New York Knicks': {'city': 'New York', 'name': 'Knicks', 'color': '#006BB6'},
            'Oklahoma City Thunder': {'city': 'Oklahoma City', 'name': 'Thunder', 'color': '#007AC1'},
            'Orlando Magic': {'city': 'Orlando', 'name': 'Magic', 'color': '#0077C0'},
            'Philadelphia 76ers': {'city': 'Philadelphia', 'name': '76ers', 'color': '#006BB6'},
            'Phoenix Suns': {'city': 'Phoenix', 'name': 'Suns', 'color': '#1D1160'},
            'Portland Trail Blazers': {'city': 'Portland', 'name': 'Trail Blazers', 'color': '#E03A3E'},
            'Sacramento Kings': {'city': 'Sacramento', 'name': 'Kings', 'color': '#5A2D81'},
            'San Antonio Spurs': {'city': 'San Antonio', 'name': 'Spurs', 'color': '#C4CED4'},
            'Toronto Raptors': {'city': 'Toronto', 'name': 'Raptors', 'color': '#CE1141'},
            'Utah Jazz': {'city': 'Utah', 'name': 'Jazz', 'color': '#002B5C'},
            'Washington Wizards': {'city': 'Washington', 'name': 'Wizards', 'color': '#002B5C'}
        }
        
    def load_models(self):
        """Load trained models and scalers"""
        try:
            # Try to load saved models
            model_files = {
                'win_loss_model': 'nba_win_loss_model.pkl',
                'over_under_model': 'nba_over_under_model.pkl',
                'wl_scaler': 'win_loss_scaler.pkl',
                'ou_scaler': 'over_under_scaler.pkl'
            }
            
            for attr, filename in model_files.items():
                filepath = self.models_dir / filename
                if filepath.exists():
                    setattr(self, attr, joblib.load(filepath))
                    print(f"✅ Loaded {attr}")
                else:
                    print(f"⚠️ {filename} not found - will need to train models")
                    
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False
            
        return all([self.win_loss_model, self.over_under_model, self.wl_scaler, self.ou_scaler])
    
    def save_models(self, win_loss_model, over_under_model, wl_scaler, ou_scaler):
        """Save trained models and scalers"""
        try:
            # Save models
            joblib.dump(win_loss_model, self.models_dir / 'nba_win_loss_model.pkl')
            joblib.dump(over_under_model, self.models_dir / 'nba_over_under_model.pkl')
            joblib.dump(wl_scaler, self.models_dir / 'win_loss_scaler.pkl')
            joblib.dump(ou_scaler, self.models_dir / 'over_under_scaler.pkl')
            
            # Update instance variables
            self.win_loss_model = win_loss_model
            self.over_under_model = over_under_model
            self.wl_scaler = wl_scaler
            self.ou_scaler = ou_scaler
            
            print("✅ Models saved successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error saving models: {e}")
            return False
    
    def get_team_stats(self) -> pd.DataFrame:
        """Load team statistics for feature calculation"""
        try:
            teams_path = self.data_dir / "processed" / "nba_teams_combined.csv"
            if teams_path.exists():
                return pd.read_csv(teams_path)
            else:
                print(f"⚠️ Team stats not found at {teams_path}")
                return pd.DataFrame()
        except Exception as e:
            print(f"❌ Error loading team stats: {e}")
            return pd.DataFrame()
    
    def calculate_features(self, home_team: str, away_team: str, 
                          team_stats: pd.DataFrame) -> Dict:
        """Calculate features for prediction"""
        
        # Get latest stats for each team
        latest_season = team_stats['SEASON'].max()
        current_stats = team_stats[team_stats['SEASON'] == latest_season]
        
        home_stats = current_stats[current_stats['TEAM_NAME'] == home_team]
        away_stats = current_stats[current_stats['TEAM_NAME'] == away_team]
        
        if home_stats.empty or away_stats.empty:
            raise ValueError(f"Team stats not found for {home_team} or {away_team}")
        
        home_stats = home_stats.iloc[0]
        away_stats = away_stats.iloc[0]
        
        # Calculate features
        features = {
            # Win/Loss features
            'home_win_pct': home_stats['WIN_PCT'],
            'away_win_pct': away_stats['WIN_PCT'],
            'win_pct_diff': home_stats['WIN_PCT'] - away_stats['WIN_PCT'],
            'home_net_rating': home_stats['NET_RATING'],
            'away_net_rating': away_stats['NET_RATING'],
            'net_rating_diff': home_stats['NET_RATING'] - away_stats['NET_RATING'],
            
            # Over/Under features
            'home_ppg': home_stats['PTS'],
            'away_ppg': away_stats['PTS'],
            'combined_ppg': home_stats['PTS'] + away_stats['PTS'],
            'home_def_rating': away_stats['OPP_PTS'],
            'away_def_rating': home_stats['OPP_PTS'],
            'combined_def_rating': home_stats['OPP_PTS'] + away_stats['OPP_PTS'],
            'pace_estimate': (home_stats.get('PACE', 100) + away_stats.get('PACE', 100)) / 2
        }
        
        return features
    
    def predict_game(self, home_team: str, away_team: str) -> Dict:
        """Make predictions for a single game"""
        
        if not all([self.win_loss_model, self.over_under_model]):
            raise ValueError("Models not loaded. Please load models first.")
        
        # Load team stats
        team_stats = self.get_team_stats()
        if team_stats.empty:
            raise ValueError("Team statistics not available")
        
        # Calculate features
        features = self.calculate_features(home_team, away_team, team_stats)
        
        # Prepare feature arrays
        wl_features = np.array([[features[f] for f in self.win_loss_features]])
        ou_features = np.array([[features[f] for f in self.over_under_features]])
        
        # Scale features
        wl_features_scaled = self.wl_scaler.transform(wl_features)
        ou_features_scaled = self.ou_scaler.transform(ou_features)
        
        # Make predictions
        win_loss_prob = self.win_loss_model.predict_proba(wl_features_scaled)[0]
        over_under_prob = self.over_under_model.predict_proba(ou_features_scaled)[0]
        
        # Format results
        prediction = {
            'matchup': {
                'home_team': home_team,
                'away_team': away_team,
                'home_info': self.team_info.get(home_team, {}),
                'away_info': self.team_info.get(away_team, {})
            },
            'win_loss': {
                'home_win_probability': float(win_loss_prob[1]),
                'away_win_probability': float(win_loss_prob[0]),
                'prediction': 'HOME' if win_loss_prob[1] > 0.5 else 'AWAY',
                'confidence': float(max(win_loss_prob))
            },
            'over_under': {
                'over_probability': float(over_under_prob[1]),
                'under_probability': float(over_under_prob[0]),
                'prediction': 'OVER' if over_under_prob[1] > 0.5 else 'UNDER',
                'confidence': float(max(over_under_prob)),
                'line': 235  # Default line
            },
            'features': features,
            'timestamp': datetime.now().isoformat()
        }
        
        return prediction
    
    def predict_multiple_games(self, games: List[Tuple[str, str]]) -> List[Dict]:
        """Make predictions for multiple games"""
        predictions = []
        
        for home_team, away_team in games:
            try:
                prediction = self.predict_game(home_team, away_team)
                predictions.append(prediction)
            except Exception as e:
                print(f"❌ Error predicting {home_team} vs {away_team}: {e}")
                
        return predictions
    
    def get_confidence_level(self, confidence: float) -> str:
        """Convert confidence score to readable level"""
        if confidence >= 0.8:
            return "Very High"
        elif confidence >= 0.7:
            return "High"
        elif confidence >= 0.6:
            return "Medium"
        else:
            return "Low"
    
    def get_available_teams(self) -> List[str]:
        """Get list of available teams"""
        return list(self.team_info.keys())


def create_sample_predictions():
    """Create sample predictions for testing the web interface"""
    
    sample_games = [
        ("Los Angeles Lakers", "Boston Celtics"),
        ("Golden State Warriors", "Miami Heat"),
        ("Phoenix Suns", "Milwaukee Bucks"),
        ("Denver Nuggets", "Philadelphia 76ers")
    ]
    
    # Create sample prediction results
    sample_predictions = []
    
    for home, away in sample_games:
        pipeline = NBAPredictionPipeline()
        
        # Mock prediction data for demo
        prediction = {
            'matchup': {
                'home_team': home,
                'away_team': away,
                'home_info': pipeline.team_info.get(home, {}),
                'away_info': pipeline.team_info.get(away, {})
            },
            'win_loss': {
                'home_win_probability': np.random.uniform(0.4, 0.8),
                'away_win_probability': np.random.uniform(0.2, 0.6),
                'prediction': np.random.choice(['HOME', 'AWAY']),
                'confidence': np.random.uniform(0.6, 0.9)
            },
            'over_under': {
                'over_probability': np.random.uniform(0.3, 0.7),
                'under_probability': np.random.uniform(0.3, 0.7),
                'prediction': np.random.choice(['OVER', 'UNDER']),
                'confidence': np.random.uniform(0.6, 0.85),
                'line': 235
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Normalize probabilities
        prediction['win_loss']['away_win_probability'] = 1 - prediction['win_loss']['home_win_probability']
        prediction['over_under']['under_probability'] = 1 - prediction['over_under']['over_probability']
        
        sample_predictions.append(prediction)
    
    return sample_predictions


if __name__ == "__main__":
    # Test the pipeline
    pipeline = NBAPredictionPipeline()
    
    # Test with sample data
    sample_preds = create_sample_predictions()
    print("🏀 Sample predictions created for testing")
    print(f"Generated {len(sample_preds)} predictions")
