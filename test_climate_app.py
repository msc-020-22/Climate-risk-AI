# This file is for local development testing only
# Run locally with: pytest test_climate_app.py -v
# 
# Note: pytest is NOT included in requirements.txt as it's only needed for development
# Streamlit Cloud will not execute this file

"""
Climate Risk Assessment - Testing Module
Unit tests for the climate risk assessment application
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from climate_app import (
    categorize_risk,
    get_risk_color,
    get_risk_recommendations,
    calculate_trend,
    validate_csv_columns
)


class TestRiskCategorization:
    """Test risk categorization logic"""
    
    def test_high_risk_rainfall(self):
        """Test high risk based on rainfall > 100mm"""
        assert categorize_risk(120.5, 30.0) == 'High'
    
    def test_high_risk_flood_depth(self):
        """Test high risk based on flood depth > 50cm"""
        assert categorize_risk(40.0, 65.3) == 'High'
    
    def test_high_risk_both(self):
        """Test high risk when both conditions met"""
        assert categorize_risk(120.5, 65.3) == 'High'
    
    def test_medium_risk_rainfall(self):
        """Test medium risk based on rainfall 50-100mm"""
        assert categorize_risk(75.0, 15.0) == 'Medium'
    
    def test_medium_risk_flood_depth(self):
        """Test medium risk based on flood depth 20-50cm"""
        assert categorize_risk(40.0, 35.0) == 'Medium'
    
    def test_low_risk(self):
        """Test low risk conditions"""
        assert categorize_risk(30.0, 10.0) == 'Low'
    
    def test_risk_with_nan(self):
        """Test handling of NaN values"""
        assert categorize_risk(np.nan, 30.0) == 'Unknown'
        assert categorize_risk(50.0, np.nan) == 'Unknown'


class TestRiskColors:
    """Test risk color assignment"""
    
    def test_high_risk_color(self):
        """Test high risk gets red color"""
        assert get_risk_color('High') == '#ef553b'
    
    def test_medium_risk_color(self):
        """Test medium risk gets yellow color"""
        assert get_risk_color('Medium') == '#ffa15a'
    
    def test_low_risk_color(self):
        """Test low risk gets green color"""
        assert get_risk_color('Low') == '#00cc96'


class TestRecommendations:
    """Test recommendation generation"""
    
    def test_high_risk_recommendations(self):
        """Test high risk returns appropriate recommendations"""
        recs = get_risk_recommendations('High')
        assert len(recs) == 5


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
