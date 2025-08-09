"""
Data collectors for various sports APIs and sources
"""
import requests
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from config.settings import NBA_API_BASE_URL, NBA_API_HEADERS
import time

class NBADataCollector:
    """Collect NBA data from various free sources"""
    
    def __init__(self):
        self.base_url = NBA_API_BASE_URL
        self.headers = NBA_API_HEADERS
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def get_team_stats(self, season: str = "2023-24") -> pd.DataFrame:
        """
        Get team statistics for a given season
        
        Args:
            season: NBA season (e.g., "2023-24")
            
        Returns:
            DataFrame with team statistics
        """
        url = f"{self.base_url}/leaguedashteamstats"
        params = {
            'Season': season,
            'SeasonType': 'Regular Season',
            'MeasureType': 'Base'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            headers = data['resultSets'][0]['headers']
            rows = data['resultSets'][0]['rowSet']
            
            df = pd.DataFrame(rows, columns=headers)
            df['SEASON'] = season
            df['LAST_UPDATED'] = datetime.now()
            
            return df
            
        except Exception as e:
            print(f"Error fetching team stats: {e}")
            return pd.DataFrame()
    
    def get_game_schedule(self, season: str = "2023-24") -> pd.DataFrame:
        """
        Get game schedule for a season
        
        Args:
            season: NBA season
            
        Returns:
            DataFrame with game schedule
        """
        # This would use NBA API to get schedule
        # For now, return empty DataFrame as placeholder
        print(f"Getting schedule for {season}...")
        return pd.DataFrame()
    
    def rate_limit_delay(self, delay: float = 1.0):
        """Add delay to respect API rate limits"""
        time.sleep(delay)


class DataCollectorFactory:
    """Factory to create appropriate data collectors"""
    
    @staticmethod
    def create_collector(sport: str):
        """Create a data collector for the specified sport"""
        if sport.lower() in ['nba', 'basketball']:
            return NBADataCollector()
        else:
            raise ValueError(f"Unsupported sport: {sport}")
