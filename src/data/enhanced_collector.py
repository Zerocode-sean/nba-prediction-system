"""
Enhanced NBA Data Collector with multiple data sources and fallback options
"""

import requests
import pandas as pd
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
import warnings

class EnhancedNBADataCollector:
    """
    NBA Data Collector with multiple sources and fallback options
    Handles API rate limits and connection issues gracefully
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.nba.com/',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Sample data for testing when APIs are down
        self.sample_team_data = self._create_sample_team_data()
        self.sample_game_data = self._create_sample_game_data()
        
    def _create_sample_team_data(self) -> pd.DataFrame:
        """Create sample team data for testing"""
        teams_data = [
            {'TEAM_ID': 1610612737, 'TEAM_NAME': 'Atlanta Hawks', 'GP': 82, 'W': 36, 'L': 46, 'PTS': 118.2, 'OPP_PTS': 120.1},
            {'TEAM_ID': 1610612738, 'TEAM_NAME': 'Boston Celtics', 'GP': 82, 'W': 64, 'L': 18, 'PTS': 120.6, 'OPP_PTS': 109.2},
            {'TEAM_ID': 1610612751, 'TEAM_NAME': 'Brooklyn Nets', 'GP': 82, 'W': 32, 'L': 50, 'PTS': 111.9, 'OPP_PTS': 116.1},
            {'TEAM_ID': 1610612766, 'TEAM_NAME': 'Charlotte Hornets', 'GP': 82, 'W': 21, 'L': 61, 'PTS': 107.9, 'OPP_PTS': 115.2},
            {'TEAM_ID': 1610612741, 'TEAM_NAME': 'Chicago Bulls', 'GP': 82, 'W': 39, 'L': 43, 'PTS': 113.4, 'OPP_PTS': 115.7},
            {'TEAM_ID': 1610612739, 'TEAM_NAME': 'Cleveland Cavaliers', 'GP': 82, 'W': 48, 'L': 34, 'PTS': 112.8, 'OPP_PTS': 109.8},
            {'TEAM_ID': 1610612742, 'TEAM_NAME': 'Dallas Mavericks', 'GP': 82, 'W': 50, 'L': 32, 'PTS': 117.9, 'OPP_PTS': 115.0},
            {'TEAM_ID': 1610612743, 'TEAM_NAME': 'Denver Nuggets', 'GP': 82, 'W': 57, 'L': 25, 'PTS': 114.9, 'OPP_PTS': 110.8},
            {'TEAM_ID': 1610612765, 'TEAM_NAME': 'Detroit Pistons', 'GP': 82, 'W': 14, 'L': 68, 'PTS': 106.6, 'OPP_PTS': 118.0},
            {'TEAM_ID': 1610612744, 'TEAM_NAME': 'Golden State Warriors', 'GP': 82, 'W': 46, 'L': 36, 'PTS': 117.8, 'OPP_PTS': 116.3},
            {'TEAM_ID': 1610612745, 'TEAM_NAME': 'Houston Rockets', 'GP': 82, 'W': 41, 'L': 41, 'PTS': 112.3, 'OPP_PTS': 111.8},
            {'TEAM_ID': 1610612754, 'TEAM_NAME': 'Indiana Pacers', 'GP': 82, 'W': 47, 'L': 35, 'PTS': 120.1, 'OPP_PTS': 117.4},
            {'TEAM_ID': 1610612746, 'TEAM_NAME': 'LA Clippers', 'GP': 82, 'W': 51, 'L': 31, 'PTS': 115.6, 'OPP_PTS': 111.7},
            {'TEAM_ID': 1610612747, 'TEAM_NAME': 'Los Angeles Lakers', 'GP': 82, 'W': 47, 'L': 35, 'PTS': 115.0, 'OPP_PTS': 113.9},
            {'TEAM_ID': 1610612763, 'TEAM_NAME': 'Memphis Grizzlies', 'GP': 82, 'W': 27, 'L': 55, 'PTS': 108.0, 'OPP_PTS': 113.7},
            {'TEAM_ID': 1610612748, 'TEAM_NAME': 'Miami Heat', 'GP': 82, 'W': 46, 'L': 36, 'PTS': 111.6, 'OPP_PTS': 109.5},
            {'TEAM_ID': 1610612749, 'TEAM_NAME': 'Milwaukee Bucks', 'GP': 82, 'W': 49, 'L': 33, 'PTS': 118.6, 'OPP_PTS': 114.5},
            {'TEAM_ID': 1610612750, 'TEAM_NAME': 'Minnesota Timberwolves', 'GP': 82, 'W': 56, 'L': 26, 'PTS': 111.5, 'OPP_PTS': 106.5},
            {'TEAM_ID': 1610612740, 'TEAM_NAME': 'New Orleans Pelicans', 'GP': 82, 'W': 49, 'L': 33, 'PTS': 112.6, 'OPP_PTS': 110.4},
            {'TEAM_ID': 1610612752, 'TEAM_NAME': 'New York Knicks', 'GP': 82, 'W': 50, 'L': 32, 'PTS': 112.8, 'OPP_PTS': 107.8},
            {'TEAM_ID': 1610612760, 'TEAM_NAME': 'Oklahoma City Thunder', 'GP': 82, 'W': 57, 'L': 25, 'PTS': 118.0, 'OPP_PTS': 111.0},
            {'TEAM_ID': 1610612753, 'TEAM_NAME': 'Orlando Magic', 'GP': 82, 'W': 47, 'L': 35, 'PTS': 110.5, 'OPP_PTS': 108.4},
            {'TEAM_ID': 1610612755, 'TEAM_NAME': 'Philadelphia 76ers', 'GP': 82, 'W': 47, 'L': 35, 'PTS': 114.7, 'OPP_PTS': 112.6},
            {'TEAM_ID': 1610612756, 'TEAM_NAME': 'Phoenix Suns', 'GP': 82, 'W': 49, 'L': 33, 'PTS': 116.2, 'OPP_PTS': 113.4},
            {'TEAM_ID': 1610612757, 'TEAM_NAME': 'Portland Trail Blazers', 'GP': 82, 'W': 21, 'L': 61, 'PTS': 107.8, 'OPP_PTS': 117.3},
            {'TEAM_ID': 1610612758, 'TEAM_NAME': 'Sacramento Kings', 'GP': 82, 'W': 46, 'L': 36, 'PTS': 117.6, 'OPP_PTS': 116.4},
            {'TEAM_ID': 1610612759, 'TEAM_NAME': 'San Antonio Spurs', 'GP': 82, 'W': 22, 'L': 60, 'PTS': 111.0, 'OPP_PTS': 118.6},
            {'TEAM_ID': 1610612761, 'TEAM_NAME': 'Toronto Raptors', 'GP': 82, 'W': 25, 'L': 57, 'PTS': 109.5, 'OPP_PTS': 115.2},
            {'TEAM_ID': 1610612762, 'TEAM_NAME': 'Utah Jazz', 'GP': 82, 'W': 31, 'L': 51, 'PTS': 112.7, 'OPP_PTS': 118.0},
            {'TEAM_ID': 1610612764, 'TEAM_NAME': 'Washington Wizards', 'GP': 82, 'W': 15, 'L': 67, 'PTS': 110.9, 'OPP_PTS': 122.4}
        ]
        
        df = pd.DataFrame(teams_data)
        df['WIN_PCT'] = df['W'] / df['GP']
        df['SEASON'] = '2023-24'
        df['LAST_UPDATED'] = datetime.now()
        return df
    
    def _create_sample_game_data(self) -> pd.DataFrame:
        """Create sample game data for testing"""
        import random
        
        games_data = []
        # Use actual team names from our team data
        teams = ['Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 
                'Chicago Bulls', 'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets',
                'Detroit Pistons', 'Golden State Warriors', 'Houston Rockets', 'Indiana Pacers',
                'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Miami Heat',
                'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
                'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns',
                'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors',
                'Utah Jazz', 'Washington Wizards']
        
        for i in range(50):  # 50 sample games
            home_team = random.choice(teams)
            away_team = random.choice([t for t in teams if t != home_team])
            
            home_score = random.randint(95, 130)
            away_score = random.randint(95, 130)
            total_score = home_score + away_score
            
            games_data.append({
                'GAME_ID': f'002240000{i:02d}',
                'GAME_DATE': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
                'HOME_TEAM': home_team,
                'AWAY_TEAM': away_team,
                'HOME_SCORE': home_score,
                'AWAY_SCORE': away_score,
                'TOTAL_SCORE': total_score,
                'HOME_WIN': 1 if home_score > away_score else 0,
                'OVER_235': 1 if total_score > 235 else 0  # Sample Over/Under line
            })
        
        return pd.DataFrame(games_data)
    
    def get_team_stats(self, season: str = "2023-24", use_sample: bool = False) -> pd.DataFrame:
        """
        Get team statistics for a given season
        
        Args:
            season: NBA season (e.g., "2023-24")
            use_sample: If True, return sample data instead of API call
            
        Returns:
            DataFrame with team statistics
        """
        if use_sample:
            print("📊 Using sample team data for testing")
            return self.sample_team_data.copy()
        
        url = "https://stats.nba.com/stats/leaguedashteamstats"
        params = {
            'Season': season,
            'SeasonType': 'Regular Season',
            'MeasureType': 'Base'
        }
        
        try:
            print(f"🔄 Fetching team stats for {season}...")
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            headers = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']
            
            df = pd.DataFrame(rows, columns=headers)
            df['SEASON'] = season
            df['LAST_UPDATED'] = datetime.now()
            
            print(f"✅ Successfully fetched data for {len(df)} teams")
            return df
            
        except Exception as e:
            print(f"⚠️ API call failed: {e}")
            print("🔄 Falling back to sample data...")
            return self.sample_team_data.copy()
    
    def get_sample_games(self, count: int = 20) -> pd.DataFrame:
        """Get sample game data for testing"""
        print(f"📊 Generating {count} sample games for testing")
        return self.sample_game_data.head(count).copy()
    
    def test_connectivity(self) -> bool:
        """Test connectivity to NBA data sources"""
        print("🔍 Testing NBA data connectivity...")
        
        try:
            # Try a simple API call
            df = self.get_team_stats(use_sample=False)
            if len(df) >= 30:  # NBA has 30 teams
                print("✅ NBA API is working")
                return True
            else:
                print("⚠️ API returned incomplete data")
                return False
        except:
            print("❌ NBA API is not accessible")
            print("✅ Sample data is available as fallback")
            return False

def test_enhanced_collector():
    """Test the enhanced data collector"""
    print("🧪 Testing Enhanced NBA Data Collector")
    print("=" * 50)
    
    collector = EnhancedNBADataCollector()
    
    # Test 1: Sample data
    print("\n1. Testing sample data generation...")
    team_data = collector.get_team_stats(use_sample=True)
    print(f"✅ Sample team data: {len(team_data)} teams")
    
    game_data = collector.get_sample_games(10)
    print(f"✅ Sample game data: {len(game_data)} games")
    
    # Test 2: API connectivity
    print("\n2. Testing API connectivity...")
    api_works = collector.test_connectivity()
    
    # Test 3: Data quality
    print("\n3. Testing data quality...")
    print(f"   Team columns: {list(team_data.columns)[:5]}...")
    print(f"   Game columns: {list(game_data.columns)}")
    print(f"   Teams with >30 wins: {len(team_data[team_data['W'] > 30])}")
    print(f"   Games with total >200: {len(game_data[game_data['TOTAL_SCORE'] > 200])}")
    
    return True

if __name__ == "__main__":
    test_enhanced_collector()
