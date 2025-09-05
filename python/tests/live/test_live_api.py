"""
Live API Tests

Tests that interact with the actual RocketReach API.
These tests require a valid API key and will make real API calls.
"""

import pytest
import os
import sys
from unittest.mock import patch, Mock

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

from rocketreach.sdk import RocketReachClient
from rocketreach.sdk.exceptions import ApiException, InvalidApiKeyException, RateLimitException


@pytest.mark.live
class TestLiveAPI:
    """Live API tests that make real requests to RocketReach API."""
    
    @pytest.fixture
    def api_key(self):
        """Get API key from environment or use test key."""
        return os.getenv('ROCKETREACH_API_KEY', '15317c3ka7e3b49defc53ce3fe874baacad0b742')
    
    @pytest.fixture
    def client(self, api_key):
        """Create client with live API key."""
        return RocketReachClient(api_key)
    
    def test_client_creation_with_live_key(self, api_key):
        """Test client creation with live API key."""
        client = RocketReachClient(api_key)
        assert client.api_key == api_key
        assert client.base_url == "https://api.rocketreach.co/api/v2"
    
    def test_account_info(self, client):
        """Test getting account information."""
        try:
            account_info = client.get_account_info()
            assert isinstance(account_info, dict)
            # Account info should contain credits or similar information
            print(f"Account info: {account_info}")
        except ApiException as e:
            # If API key is invalid, that's expected for test key
            if e.status_code == 401:
                pytest.skip("Invalid API key for live testing")
            else:
                raise
    
    def test_health_status(self, client):
        """Test health status endpoint."""
        try:
            health = client.get_health_status()
            assert isinstance(health, dict)
            print(f"Health status: {health}")
        except ApiException as e:
            if e.status_code == 401:
                pytest.skip("Invalid API key for live testing")
            else:
                raise
    
    def test_people_search_basic(self, client):
        """Test basic people search."""
        try:
            results = (client.people_search()
                      .name(["John Doe"])
                      .page(1)
                      .page_size(5)
                      .search())
            
            assert hasattr(results, 'profiles')
            assert hasattr(results, 'pagination')
            assert isinstance(results.profiles, list)
            print(f"Search results: {results.count} profiles found")
            
        except ApiException as e:
            if e.status_code == 401:
                pytest.skip("Invalid API key for live testing")
            elif e.status_code == 429:
                pytest.skip("Rate limited - skipping live test")
            else:
                raise
    
    def test_people_search_with_employer(self, client):
        """Test people search with employer filter."""
        try:
            results = (client.people_search()
                      .name(["John"])
                      .current_employer(["Google"])
                      .page(1)
                      .page_size(3)
                      .search())
            
            assert hasattr(results, 'profiles')
            assert isinstance(results.profiles, list)
            print(f"Employer search results: {results.count} profiles found")
            
        except ApiException as e:
            if e.status_code == 401:
                pytest.skip("Invalid API key for live testing")
            elif e.status_code == 429:
                pytest.skip("Rate limited - skipping live test")
            else:
                raise
    
    def test_person_lookup_basic(self, client):
        """Test basic person lookup."""
        try:
            # Try to lookup a person (this might not find anything with test data)
            person = (client.person_lookup()
                     .name("John Doe")
                     .current_employer("Google")
                     .lookup())
            
            assert hasattr(person, 'id')
            assert hasattr(person, 'name')
            print(f"Person lookup result: {person.name if person.name else 'No person found'}")
            
        except ApiException as e:
            if e.status_code == 401:
                pytest.skip("Invalid API key for live testing")
            elif e.status_code == 404:
                pytest.skip("No person found - expected for test data")
            elif e.status_code == 429:
                pytest.skip("Rate limited - skipping live test")
            else:
                raise
    
    def test_person_enrich_basic(self, client):
        """Test basic person enrichment."""
        try:
            # Try to enrich a person (this might not find anything with test data)
            enriched = (client.person_enrich()
                       .name("John Doe")
                       .current_employer("Google")
                       .enrich())
            
            assert hasattr(enriched, 'person_id')
            assert hasattr(enriched, 'company_id')
            print(f"Enrich result: Person {enriched.person_name}, Company {enriched.company_name}")
            
        except ApiException as e:
            if e.status_code == 401:
                pytest.skip("Invalid API key for live testing")
            elif e.status_code == 404:
                pytest.skip("No person found - expected for test data")
            elif e.status_code == 429:
                pytest.skip("Rate limited - skipping live test")
            else:
                raise
    
    def test_rate_limiting_handling(self, client):
        """Test that rate limiting is handled properly."""
        try:
            # Make multiple requests quickly to potentially trigger rate limiting
            for i in range(3):
                results = (client.people_search()
                          .name([f"Test User {i}"])
                          .page(1)
                          .page_size(1)
                          .search())
                print(f"Request {i+1}: {results.count} results")
                
        except RateLimitException as e:
            print(f"Rate limited as expected: {e}")
            assert e.retry_after is not None
        except ApiException as e:
            if e.status_code == 401:
                pytest.skip("Invalid API key for live testing")
            else:
                raise
    
    def test_error_handling_invalid_key(self):
        """Test error handling with invalid API key."""
        with pytest.raises(InvalidApiKeyException):
            RocketReachClient("")
        
        with pytest.raises(InvalidApiKeyException):
            RocketReachClient("invalid-key")
    
    def test_network_error_handling(self, client):
        """Test network error handling by using invalid base URL."""
        # Create client with invalid base URL to test network error handling
        invalid_client = RocketReachClient(
            api_key=client.api_key,
            base_url="https://invalid-url-that-does-not-exist.com/api/v2"
        )
        
        try:
            invalid_client.get_account_info()
            pytest.fail("Expected network error")
        except Exception as e:
            # Should get some kind of network error
            assert "network" in str(e).lower() or "connection" in str(e).lower() or "timeout" in str(e).lower()
            print(f"Network error handled correctly: {e}")


@pytest.mark.live
class TestLiveAPIWithMock:
    """Live API tests with mocked responses for testing error handling."""
    
    def test_api_exception_handling(self):
        """Test API exception handling with mocked responses."""
        with patch('requests.Session.request') as mock_request:
            # Mock a 400 error response
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.ok = False
            mock_response.json.return_value = {
                "error": "Bad Request",
                "message": "Invalid parameters"
            }
            mock_response.text = '{"error": "Bad Request"}'
            mock_request.return_value = mock_response
            
            client = RocketReachClient("test-key")
            
            with pytest.raises(ApiException) as exc_info:
                client.get_account_info()
            
            assert exc_info.value.status_code == 400
            assert exc_info.value.is_client_error is True
            assert exc_info.value.is_server_error is False
    
    def test_rate_limit_exception_handling(self):
        """Test rate limit exception handling with mocked responses."""
        with patch('requests.Session.request') as mock_request:
            # Mock a 429 rate limit response
            mock_response = Mock()
            mock_response.status_code = 429
            mock_response.ok = False
            mock_response.headers = {'Retry-After': '60'}
            mock_response.text = "Rate limit exceeded"
            mock_request.return_value = mock_response
            
            client = RocketReachClient("test-key", retry_attempts=0)
            
            with pytest.raises(RateLimitException) as exc_info:
                client.get_account_info()
            
            assert exc_info.value.status_code == 429
            assert exc_info.value.retry_after == 60
