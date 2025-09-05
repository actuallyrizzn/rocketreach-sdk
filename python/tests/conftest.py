"""
Pytest Configuration

Global pytest configuration and fixtures.
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch
from typing import Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from rocketreach.sdk import RocketReachClient
from rocketreach.sdk.http import HttpClient


@pytest.fixture
def mock_http_client():
    """Mock HTTP client for testing."""
    client = Mock(spec=HttpClient)
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.delete = Mock()
    return client


@pytest.fixture
def mock_requests_response():
    """Mock requests response object."""
    response = Mock()
    response.json = Mock()
    response.status_code = 200
    response.ok = True
    response.text = "{}"
    response.headers = {}
    return response


@pytest.fixture
def valid_api_key():
    """Valid API key for testing."""
    return "15317c3ka7e3b49defc53ce3fe874baacad0b742"


@pytest.fixture
def invalid_api_key():
    """Invalid API key for testing."""
    return "invalid-key"


@pytest.fixture
def empty_api_key():
    """Empty API key for testing."""
    return ""


@pytest.fixture
def rocketreach_client(valid_api_key, mock_http_client):
    """RocketReach client with mocked HTTP client."""
    with patch('rocketreach.sdk.client.HttpClient', return_value=mock_http_client):
        client = RocketReachClient(valid_api_key)
        client._http_client = mock_http_client
        return client


@pytest.fixture
def search_response_data():
    """Sample search response data."""
    return {
        "profiles": [
            {
                "id": 12345,
                "name": "John Doe",
                "current_employer": "Google",
                "status": "complete"
            }
        ],
        "pagination": {
            "start": 1,
            "next": 2,
            "total": 100
        }
    }


@pytest.fixture
def person_response_data():
    """Sample person response data."""
    return {
        "id": 12345,
        "name": "John Doe",
        "current_title": "Software Engineer",
        "current_employer": "Google",
        "status": "complete"
    }


@pytest.fixture
def enrich_response_data():
    """Sample enrich response data."""
    return {
        "person": {
            "id": 12345,
            "name": "John Doe"
        },
        "company": {
            "id": 98765,
            "name": "Google",
            "domain": "google.com"
        }
    }


@pytest.fixture
def account_response_data():
    """Sample account response data."""
    return {
        "credits": 1000,
        "used_credits": 150,
        "remaining_credits": 850
    }


@pytest.fixture
def health_response_data():
    """Sample health response data."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@pytest.fixture
def error_response_data():
    """Sample error response data."""
    return {
        "error": "Test error",
        "code": 400,
        "message": "Test error message"
    }


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks after each test."""
    yield
    # This will run after each test
    pass
