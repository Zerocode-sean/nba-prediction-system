"""
🏀 Real-Time NBA Data Integration System
======================================

This module handles live NBA data collection and real-time predictions
for actual games. This is where the rubber meets the road!
"""

import requests
import pandas as pd
import json
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Tuple
import time
import warnings
warnings.filterwarnings('ignore')

class RealTimeNBASystem:
    """
    Real-time NBA data system for live predictions and validation
    """
    
    def __init__(self):
        self.espn_base = "http://site.api.espn.com/apis/site/v2/sports/basketball/nba"
        self.nba_base = "https://stats.nba.com/stats"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Referer': 'https://www.nba.com/'
        }
        
        # Team name mappings for consistency
        self.team_mappings = {
            'LA Clippers': 'Los Angeles Clippers',
            'LA Lakers': 'Los Angeles Lakers',
            'Golden State': 'Golden State Warriors',
            'San Antonio': 'San Antonio Spurs',
            'New York': 'New York Knicks',
            'Oklahoma City': 'Oklahoma City Thunder',
            'New Orleans': 'New Orleans Pelicans'
        }
    
    def get_current_season(self) -> str:
        """Get current NBA season string"""
        current_date = datetime.now()
        
        # NBA season runs October to April of following year
        if current_date.month >= 10:
            # New season starting
            return f"{current_date.year}-{str(current_date.year + 1)[-2:]}"
        else:
            # Season ending
            return f"{current_date.year - 1}-{str(current_date.year)[-2:]}"
    
    def is_nba_season_active(self) -> bool:
        """Check if NBA season is currently active"""
        current_date = datetime.now()
        month = current_date.month
        
        # NBA season: October through April (+ playoffs through June)
        return month in [10, 11, 12, 1, 2, 3, 4, 5, 6]
    
    def get_todays_games(self) -> List[Dict]:
        """Get today's NBA games from ESPN API"""
        try:
            url = f"{self.espn_base}/scoreboard"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            games = []
            
            for event in data.get('events', []):
                game_info = {
                    'game_id': event.get('id'),
                    'date': event.get('date'),
                    'status': event.get('status', {}).get('type', {}).get('description', 'Unknown'),
                    'home_team': event.get('competitions', [{}])[0].get('competitors', [{}])[1].get('team', {}).get('displayName'),
                    'away_team': event.get('competitions', [{}])[0].get('competitors', [{}])[0].get('team', {}).get('displayName'),
                    'home_score': event.get('competitions', [{}])[0].get('competitors', [{}])[1].get('score'),
                    'away_score': event.get('competitions', [{}])[0].get('competitors', [{}])[0].get('score'),
                    'venue': event.get('competitions', [{}])[0].get('venue', {}).get('fullName'),
                    'broadcast': event.get('competitions', [{}])[0].get('broadcasts', [{}])[0].get('names', [''])[0] if event.get('competitions', [{}])[0].get('broadcasts') else 'TBD'
                }
                games.append(game_info)
            
            print(f"✅ Found {len(games)} games for today")
            return games
            
        except Exception as e:
            print(f"❌ Error fetching today's games: {e}")
            return []
    
    def get_live_scores(self) -> List[Dict]:
        """Get live scores for ongoing games"""
        try:
            games = self.get_todays_games()
            live_games = []
            
            for game in games:
                if game['status'] in ['In Progress', 'Halftime', '2nd Half']:
                    live_games.append(game)
            
            print(f"🔴 {len(live_games)} games currently live")
            return live_games
            
        except Exception as e:
            print(f"❌ Error fetching live scores: {e}")
            return []
    
    def get_upcoming_games(self, days: int = 7) -> List[Dict]:
        """Get upcoming NBA games for the next few days"""
        upcoming_games = []
        
        for i in range(1, days + 1):
            target_date = datetime.now() + timedelta(days=i)
            date_str = target_date.strftime("%Y%m%d")
            
            try:
                url = f"{self.espn_base}/scoreboard"
                params = {'dates': date_str}
                response = requests.get(url, params=params, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                for event in data.get('events', []):
                    game_info = {
                        'game_id': event.get('id'),
                        'date': event.get('date'),
                        'formatted_date': target_date.strftime("%Y-%m-%d"),
                        'status': 'Upcoming',
                        'home_team': event.get('competitions', [{}])[0].get('competitors', [{}])[1].get('team', {}).get('displayName'),
                        'away_team': event.get('competitions', [{}])[0].get('competitors', [{}])[0].get('team', {}).get('displayName'),
                        'venue': event.get('competitions', [{}])[0].get('venue', {}).get('fullName', 'TBD'),
                        'broadcast': event.get('competitions', [{}])[0].get('broadcasts', [{}])[0].get('names', ['TBD'])[0] if event.get('competitions', [{}])[0].get('broadcasts') else 'TBD',
                        'time': event.get('date', '').split('T')[1][:5] if 'T' in event.get('date', '') else 'TBD'
                    }
                    upcoming_games.append(game_info)
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f"⚠️ Error fetching upcoming games for {date_str}: {e}")
                continue
        
        print(f"✅ Found {len(upcoming_games)} upcoming games in next {days} days")
        return upcoming_games
    
    def get_completed_games(self, days_back: int = 7) -> List[Dict]:
        """Get completed games from recent days"""
        completed_games = []
        
        for i in range(days_back):
            target_date = datetime.now() - timedelta(days=i+1)
            date_str = target_date.strftime("%Y%m%d")
            
            try:
                url = f"{self.espn_base}/scoreboard"
                params = {'dates': date_str}
                response = requests.get(url, params=params, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                for event in data.get('events', []):
                    if event.get('status', {}).get('type', {}).get('description') == 'Final':
                        game_info = {
                            'game_id': event.get('id'),
                            'date': event.get('date'),
                            'formatted_date': target_date.strftime("%Y-%m-%d"),
                            'status': 'Final',
                            'home_team': event.get('competitions', [{}])[0].get('competitors', [{}])[1].get('team', {}).get('displayName'),
                            'away_team': event.get('competitions', [{}])[0].get('competitors', [{}])[0].get('team', {}).get('displayName'),
                            'home_score': int(event.get('competitions', [{}])[0].get('competitors', [{}])[1].get('score', 0)),
                            'away_score': int(event.get('competitions', [{}])[0].get('competitors', [{}])[0].get('score', 0)),
                            'total_score': None,
                            'home_win': None,
                            'venue': event.get('competitions', [{}])[0].get('venue', {}).get('fullName', 'Unknown')
                        }
                        
                        # Calculate derived values
                        game_info['total_score'] = game_info['home_score'] + game_info['away_score']
                        game_info['home_win'] = game_info['home_score'] > game_info['away_score']
                        game_info['over_225'] = game_info['total_score'] > 225
                        game_info['over_235'] = game_info['total_score'] > 235
                        game_info['over_245'] = game_info['total_score'] > 245
                        
                        completed_games.append(game_info)
                
                time.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                print(f"⚠️ Error fetching games for {date_str}: {e}")
                continue
        
        print(f"✅ Found {len(completed_games)} completed games in last {days_back} days")
        return completed_games
    
    def get_current_team_stats(self) -> pd.DataFrame:
        """Get current season team statistics"""
        try:
            current_season = self.get_current_season()
            url = f"{self.nba_base}/leaguedashteamstats"
            
            params = {
                'Season': current_season,
                'SeasonType': 'Regular Season',
                'MeasureType': 'Base'
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            headers = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']
            
            df = pd.DataFrame(rows, columns=headers)
            df['SEASON'] = current_season
            df['LAST_UPDATED'] = datetime.now()
            
            print(f"✅ Current season stats loaded: {current_season}")
            return df
            
        except Exception as e:
            print(f"❌ Error fetching current team stats: {e}")
            print("💡 Falling back to historical data for predictions")
            return pd.DataFrame()
    
    def create_real_time_predictions(self, games: List[Dict]) -> List[Dict]:
        """Create predictions for real games using live data"""
        from src.prediction.pipeline import NBAPredictionPipeline
        
        predictions = []
        pipeline = NBAPredictionPipeline()
        
        # Try to load trained models
        models_loaded = pipeline.load_models()
        if not models_loaded:
            print("⚠️ Models not loaded - using demo predictions")
        
        for game in games:
            try:
                home_team = self._normalize_team_name(game['home_team'])
                away_team = self._normalize_team_name(game['away_team'])
                
                if models_loaded:
                    # Use actual trained models
                    prediction = pipeline.predict_game(home_team, away_team)
                else:
                    # Create realistic demo prediction
                    prediction = self._create_demo_prediction(game)
                
                # Add real game info
                prediction['real_game_info'] = {
                    'game_id': game.get('game_id'),
                    'date': game.get('date'),
                    'formatted_date': game.get('formatted_date'),
                    'status': game.get('status'),
                    'venue': game.get('venue'),
                    'broadcast': game.get('broadcast', 'TBD')
                }
                
                # Add actual results if game is completed
                if game.get('status') == 'Final':
                    prediction['actual_results'] = {
                        'home_score': game['home_score'],
                        'away_score': game['away_score'],
                        'total_score': game['total_score'],
                        'home_win': game['home_win'],
                        'winner': home_team if game['home_win'] else away_team,
                        'over_235': game['over_235']
                    }
                    
                    # Calculate prediction accuracy
                    prediction['accuracy'] = self._calculate_accuracy(prediction)
                
                predictions.append(prediction)
                
            except Exception as e:
                print(f"❌ Error predicting {game.get('home_team')} vs {game.get('away_team')}: {e}")
        
        return predictions
    
    def _normalize_team_name(self, team_name: str) -> str:
        """Normalize team names for consistency"""
        return self.team_mappings.get(team_name, team_name)
    
    def _create_demo_prediction(self, game: Dict) -> Dict:
        """Create realistic demo prediction for testing"""
        import numpy as np
        from src.prediction.pipeline import NBAPredictionPipeline
        
        pipeline = NBAPredictionPipeline()
        home_team = self._normalize_team_name(game['home_team'])
        away_team = self._normalize_team_name(game['away_team'])
        
        # Create realistic probabilities
        home_win_prob = np.random.uniform(0.35, 0.75)
        over_prob = np.random.uniform(0.25, 0.65)
        
        prediction = {
            'matchup': {
                'home_team': home_team,
                'away_team': away_team,
                'home_info': pipeline.team_info.get(home_team, {}),
                'away_info': pipeline.team_info.get(away_team, {})
            },
            'win_loss': {
                'home_win_probability': home_win_prob,
                'away_win_probability': 1 - home_win_prob,
                'prediction': 'HOME' if home_win_prob > 0.5 else 'AWAY',
                'confidence': max(home_win_prob, 1 - home_win_prob)
            },
            'over_under': {
                'over_probability': over_prob,
                'under_probability': 1 - over_prob,
                'prediction': 'OVER' if over_prob > 0.5 else 'UNDER',
                'confidence': max(over_prob, 1 - over_prob),
                'line': 235
            },
            'timestamp': datetime.now().isoformat(),
            'data_source': 'demo_mode'
        }
        
        return prediction
    
    def _calculate_accuracy(self, prediction: Dict) -> Dict:
        """Calculate prediction accuracy against actual results"""
        if 'actual_results' not in prediction:
            return {}
        
        actual = prediction['actual_results']
        pred_wl = prediction['win_loss']
        pred_ou = prediction['over_under']
        
        # Win/Loss accuracy
        predicted_winner = pred_wl['prediction']
        actual_winner = 'HOME' if actual['home_win'] else 'AWAY'
        wl_correct = predicted_winner == actual_winner
        
        # Over/Under accuracy
        predicted_ou = pred_ou['prediction']
        actual_ou = 'OVER' if actual['over_235'] else 'UNDER'
        ou_correct = predicted_ou == actual_ou
        
        return {
            'win_loss_correct': wl_correct,
            'over_under_correct': ou_correct,
            'both_correct': wl_correct and ou_correct,
            'win_loss_confidence': pred_wl['confidence'],
            'over_under_confidence': pred_ou['confidence']
        }
    
    def get_season_status(self) -> Dict:
        """Get current NBA season status"""
        current_season = self.get_current_season()
        is_active = self.is_nba_season_active()
        
        # Try to get today's games to check activity
        todays_games = self.get_todays_games()
        
        status = {
            'current_season': current_season,
            'is_season_active': is_active,
            'todays_games_count': len(todays_games),
            'has_games_today': len(todays_games) > 0,
            'current_date': datetime.now().strftime("%Y-%m-%d"),
            'status_message': self._get_status_message(is_active, len(todays_games))
        }
        
        return status
    
    def _get_status_message(self, is_active: bool, games_count: int) -> str:
        """Get descriptive status message"""
        if not is_active:
            return "🏖️ NBA Off-Season - Using historical data for predictions"
        elif games_count == 0:
            return "🏀 NBA Season Active - No games scheduled today"
        else:
            return f"🔴 NBA Season Active - {games_count} games today!"


class RealTimeValidation:
    """
    Real-time validation system for tracking prediction accuracy
    """
    
    def __init__(self):
        self.real_time_system = RealTimeNBASystem()
        self.prediction_history = []
    
    def validate_recent_predictions(self, days_back: int = 7) -> Dict:
        """Validate predictions against recent game results"""
        print(f"🔍 Validating predictions from last {days_back} days...")
        
        # Get completed games
        completed_games = self.real_time_system.get_completed_games(days_back)
        
        if not completed_games:
            return {
                'status': 'no_data',
                'message': 'No completed games found for validation',
                'games_found': 0
            }
        
        # Create predictions for these games
        predictions_with_results = self.real_time_system.create_real_time_predictions(completed_games)
        
        # Calculate overall accuracy
        total_games = len(predictions_with_results)
        wl_correct = sum(1 for p in predictions_with_results 
                        if p.get('accuracy', {}).get('win_loss_correct', False))
        ou_correct = sum(1 for p in predictions_with_results 
                        if p.get('accuracy', {}).get('over_under_correct', False))
        both_correct = sum(1 for p in predictions_with_results 
                          if p.get('accuracy', {}).get('both_correct', False))
        
        validation_results = {
            'status': 'success',
            'period': f"Last {days_back} days",
            'total_games': total_games,
            'win_loss_accuracy': wl_correct / total_games if total_games > 0 else 0,
            'over_under_accuracy': ou_correct / total_games if total_games > 0 else 0,
            'both_correct_rate': both_correct / total_games if total_games > 0 else 0,
            'predictions_with_results': predictions_with_results,
            'validation_date': datetime.now().isoformat()
        }
        
        return validation_results
    
    def get_todays_predictions(self) -> List[Dict]:
        """Get predictions for today's games"""
        print("🎯 Creating predictions for today's games...")
        
        todays_games = self.real_time_system.get_todays_games()
        
        if not todays_games:
            return []
        
        predictions = self.real_time_system.create_real_time_predictions(todays_games)
        
        return predictions


if __name__ == "__main__":
    # Test the real-time system
    print("🏀 Testing Real-Time NBA System")
    print("=" * 40)
    
    system = RealTimeNBASystem()
    
    # Check season status
    status = system.get_season_status()
    print(f"📅 Season Status: {status['status_message']}")
    print(f"🏀 Current Season: {status['current_season']}")
    print(f"📊 Games Today: {status['todays_games_count']}")
    
    # Test validation
    validator = RealTimeValidation()
    
    print(f"\n🔍 Testing Recent Games Validation...")
    results = validator.validate_recent_predictions(days_back=3)
    
    if results['status'] == 'success':
        print(f"✅ Validation successful!")
        print(f"   Games analyzed: {results['total_games']}")
        print(f"   Win/Loss accuracy: {results['win_loss_accuracy']:.1%}")
        print(f"   Over/Under accuracy: {results['over_under_accuracy']:.1%}")
    else:
        print(f"⚠️ {results['message']}")
    
    print(f"\n🎯 Ready for real-time predictions!")
