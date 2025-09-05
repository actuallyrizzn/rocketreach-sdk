"""
Unit tests for the RocketReachClient class.
"""

import pytest
from unittest.mock import Mock, patch
from rocketreach.sdk.client import RocketReachClient
from rocketreach.sdk.exceptions import InvalidApiKeyException


class TestRocketReachClient:
    """Test cases for RocketReachClient."""
    
    def test_init_with_valid_api_key(self, valid_api_key):
        """Test client initialization with valid API key."""
        with patch('rocketreach.sdk.client.HttpClient'):
            client = RocketReachClient(valid_api_key)
            assert client.api_key == valid_api_key
            assert client.base_url == "https://api.rocketreach.co/api/v2"
            assert client.timeout == 30
            assert client.retry_attempts == 3
            assert client.retry_delay == 1.0
    
    def test_init_with_empty_api_key(self, empty_api_key):
        """Test client initialization with empty API key raises exception."""
        with pytest.raises(InvalidApiKeyException, match="API key cannot be empty"):
            RocketReachClient(empty_api_key)
    
    def test_init_with_none_api_key(self):
        """Test client initialization with None API key raises exception."""
        with pytest.raises(InvalidApiKeyException, match="API key cannot be empty"):
            RocketReachClient(None)
    
    def test_init_with_whitespace_api_key(self):
        """Test client initialization with whitespace-only API key raises exception."""
        with pytest.raises(InvalidApiKeyException, match="API key cannot be empty"):
            RocketReachClient("   ")
    
    def test_init_with_custom_parameters(self, valid_api_key):
        """Test client initialization with custom parameters."""
        with patch('rocketreach.sdk.client.HttpClient') as mock_http:
            client = RocketReachClient(
                api_key=valid_api_key,
                base_url="https://custom-api.example.com/v2",
                timeout=60,
                retry_attempts=5,
                retry_delay=2.0
            )
            
            assert client.api_key == valid_api_key
            assert client.base_url == "https://custom-api.example.com/v2"
            assert client.timeout == 60
            assert client.retry_attempts == 5
            assert client.retry_delay == 2.0
            
            # Verify HttpClient was called with correct parameters
            mock_http.assert_called_once_with(
                base_url="https://custom-api.example.com/v2",
                api_key=valid_api_key,
                timeout=60,
                retry_attempts=5,
                retry_delay=2.0
            )
    
    def test_api_key_property(self, valid_api_key):
        """Test API key property."""
        with patch('rocketreach.sdk.client.HttpClient'):
            client = RocketReachClient(valid_api_key)
            assert client.api_key == valid_api_key
    
    def test_base_url_property(self, valid_api_key):
        """Test base URL property."""
        with patch('rocketreach.sdk.client.HttpClient'):
            client = RocketReachClient(valid_api_key)
            assert client.base_url == "https://api.rocketreach.co/api/v2"
    
    def test_timeout_property(self, valid_api_key):
        """Test timeout property."""
        with patch('rocketreach.sdk.client.HttpClient'):
            client = RocketReachClient(valid_api_key)
            assert client.timeout == 30
    
    def test_retry_attempts_property(self, valid_api_key):
        """Test retry attempts property."""
        with patch('rocketreach.sdk.client.HttpClient'):
            client = RocketReachClient(valid_api_key)
            assert client.retry_attempts == 3
    
    def test_retry_delay_property(self, valid_api_key):
        """Test retry delay property."""
        with patch('rocketreach.sdk.client.HttpClient'):
            client = RocketReachClient(valid_api_key)
            assert client.retry_delay == 1.0
    
    def test_people_search_endpoint(self, rocketreach_client):
        """Test people search endpoint access."""
        endpoint = rocketreach_client.people_search()
        assert endpoint is not None
        assert hasattr(endpoint, 'search')
    
    def test_person_lookup_endpoint(self, rocketreach_client):
        """Test person lookup endpoint access."""
        endpoint = rocketreach_client.person_lookup()
        assert endpoint is not None
        assert hasattr(endpoint, 'lookup')
    
    def test_person_enrich_endpoint(self, rocketreach_client):
        """Test person enrich endpoint access."""
        endpoint = rocketreach_client.person_enrich()
        assert endpoint is not None
        assert hasattr(endpoint, 'enrich')
    
    def test_get_account_info(self, rocketreach_client, account_response_data):
        """Test get account info method."""
        rocketreach_client._http_client.get.return_value = account_response_data
        
        result = rocketreach_client.get_account_info()
        
        assert result == account_response_data
        rocketreach_client._http_client.get.assert_called_once_with("/account")
    
    def test_get_health_status(self, rocketreach_client, health_response_data):
        """Test get health status method."""
        rocketreach_client._http_client.get.return_value = health_response_data
        
        result = rocketreach_client.get_health_status()
        
        assert result == health_response_data
        rocketreach_client._http_client.get.assert_called_once_with("/health")
    
    def test_repr(self, valid_api_key):
        """Test string representation."""
        with patch('rocketreach.sdk.client.HttpClient'):
            client = RocketReachClient(valid_api_key)
            repr_str = repr(client)
            assert "RocketReachClient" in repr_str
            assert valid_api_key[:8] in repr_str
            assert "https://api.rocketreach.co/api/v2" in repr_str
    
    def test_str(self, valid_api_key):
        """Test string conversion."""
        with patch('rocketreach.sdk.client.HttpClient'):
            client = RocketReachClient(valid_api_key)
            str_repr = str(client)
            assert "RocketReachClient" in str_repr
            assert valid_api_key[:8] in str_repr
            assert "https://api.rocketreach.co/api/v2" in str_repr
    
    def test_api_key_stripping(self):
        """Test that API key is stripped of whitespace."""
        with patch('rocketreach.sdk.client.HttpClient') as mock_http:
            client = RocketReachClient("  test-key  ")
            assert client.api_key == "test-key"
            mock_http.assert_called_once()
            call_args = mock_http.call_args
            assert call_args[1]['api_key'] == "test-key"
    
    def test_default_values(self, valid_api_key):
        """Test default values are set correctly."""
        with patch('rocketreach.sdk.client.HttpClient') as mock_http:
            client = RocketReachClient(valid_api_key)
            
            # Check that HttpClient was called with default values
            call_args = mock_http.call_args
            assert call_args[1]['base_url'] == "https://api.rocketreach.co/api/v2"
            assert call_args[1]['timeout'] == 30
            assert call_args[1]['retry_attempts'] == 3
            assert call_args[1]['retry_delay'] == 1.0
    
    def test_endpoint_independence(self, rocketreach_client):
        """Test that different endpoint calls return different instances."""
        search1 = rocketreach_client.people_search()
        search2 = rocketreach_client.people_search()
        
        # Should be different instances
        assert search1 is not search2
        
        # But should be the same type
        assert type(search1) == type(search2)
    
    def test_endpoint_persistence(self, rocketreach_client):
        """Test that endpoint instances persist their state."""
        search = rocketreach_client.people_search()
        search.name(["John Doe"])
        
        # Get another instance - should be independent
        search2 = rocketreach_client.people_search()
        
        # Original should still have the name set
        assert search._query.name == ["John Doe"]
        
        # New instance should not have the name set
        assert search2._query.name is None
