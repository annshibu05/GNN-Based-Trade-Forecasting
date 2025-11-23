"""
API Tests - Run with: pytest tests/test_api.py
"""
import pytest
import requests
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data

def test_get_countries():
    """Test countries endpoint"""
    response = client.get("/countries")
    assert response.status_code == 200
    data = response.json()
    assert "countries" in data
    assert len(data["countries"]) > 0

def test_predict_valid():
    """Test valid prediction"""
    response = client.post("/predict", json={
        "source_country": "USA",
        "target_country": "CHN",
        "sector": "Pharmaceuticals",
        "year": 2024,
        "month": 12
    })
    
    if response.status_code == 200:
        data = response.json()
        assert "predicted_value_usd" in data
        assert data["predicted_value_usd"] > 0

def test_predict_invalid_country():
    """Test prediction with invalid country"""
    response = client.post("/predict", json={
        "source_country": "INVALID",
        "target_country": "CHN",
        "sector": "Pharmaceuticals"
    })
    assert response.status_code == 400

def test_predict_invalid_sector():
    """Test prediction with invalid sector"""
    response = client.post("/predict", json={
        "source_country": "USA",
        "target_country": "CHN",
        "sector": "InvalidSector"
    })
    assert response.status_code == 400

if __name__ == "__main__":
    pytest.main([__file__, "-v"])