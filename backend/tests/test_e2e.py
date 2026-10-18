# File: backend/tests/test_e2e.py
import sys
import json
import os
import pathlib
import requests
import pytest
from dotenv import load_dotenv

def setup_test():
    """Configure environment for testing"""
    test_env_path = pathlib.Path(__file__).parent.parent / '.env'
    load_dotenv(test_env_path)

    # Verify required environment variables
    required_vars = [ 'GEMINI_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    assert not missing_vars, f"Missing required env vars: {missing_vars}"

def create_test_request():
    """Create a sample test request"""
    return json.dumps({
        "category": "bollywood",
        "difficulty": "easy",
        "exclude": ["Sholay", "Dangal"]
    })

def test_full_movie_selection_flow():
    setup_test()

    test_url = os.getenv("API_URL")
    assert test_url, "API_URL not set in environment"

    response = requests.post(
        f"{test_url}/movie",
        headers={"Content-Type": "application/json"},
        data=create_test_request()
    )

    assert response.status_code == 200
    data = json.loads(response.text)

    # Verify response structure
    assert "movie" in data
    assert "source" in data
    assert "category" in data

    # Verify fallback logic
    if data['source'] == "fallback":
        payload = json.loads(test_request)
        assert data['movie'] not in payload['exclude'], \
            "Fallback movie is in exclusion list"

    # Verify alternative source options
    if data['source'] == "gemini":
        assert isinstance(data['categories'], list)
    elif data['source'] == "fallback":
        assert isinstance(data.get('categories'), list)

    # Verify movie title characteristics
    assert isinstance(data['movie'], str)
    assert len(data['movie']) > 0
    assert isinstance(data['category'], str)

if __name__ == "__main__":
    pytest.main([__file__])