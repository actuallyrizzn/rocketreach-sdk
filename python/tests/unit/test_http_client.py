"""
Unit tests for the HttpClient class.
"""

import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from rocketreach.sdk.http.client import HttpClient
from rocketreach.sdk.exceptions import ApiException, RateLimitException, NetworkException


class TestHttpClient:
    """Test cases for HttpClient."""
    
    def test_init(self, valid_api_key):
        """Test HTTP client initialization."""
        client = HttpClient(
            base_url="https://api.example.com",
            api_key=valid_api_key,
            timeout=30,
            retry_attempts=3,
            retry_delay=1.0
        )
        
        assert client.base_url == "https://api.example.com"
        assert client.api_key == valid_api_key
        assert client.timeout == 30
        assert client.retry_attempts == 3
        assert client.retry_delay == 1.0
        assert client.session is not None
        assert client.session.headers['Authorization'] == f'Bearer {valid_api_key}'
        assert client.session.headers['Content-Type'] == 'application/json'
        assert 'RocketReach-Python-SDK' in client.session.headers['User-Agent']
    
    def test_get_request_success(self, valid_api_key):
        """Test successful GET request."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.ok = True
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key)
            result = client.get("/test")
            
            assert result == {"success": True}
            mock_request.assert_called_once_with(
                method='GET',
                url='https://api.example.com/test',
                params=None,
                json=None,
                timeout=30
            )
    
    def test_post_request_success(self, valid_api_key):
        """Test successful POST request."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.ok = True
            mock_response.json.return_value = {"created": True}
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key)
            data = {"name": "John Doe"}
            result = client.post("/test", data)
            
            assert result == {"created": True}
            mock_request.assert_called_once_with(
                method='POST',
                url='https://api.example.com/test',
                params=None,
                json=data,
                timeout=30
            )
    
    def test_put_request_success(self, valid_api_key):
        """Test successful PUT request."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.ok = True
            mock_response.json.return_value = {"updated": True}
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key)
            data = {"name": "Jane Doe"}
            result = client.put("/test", data)
            
            assert result == {"updated": True}
            mock_request.assert_called_once_with(
                method='PUT',
                url='https://api.example.com/test',
                params=None,
                json=data,
                timeout=30
            )
    
    def test_delete_request_success(self, valid_api_key):
        """Test successful DELETE request."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.ok = True
            mock_response.json.return_value = {"deleted": True}
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key)
            result = client.delete("/test")
            
            assert result == {"deleted": True}
            mock_request.assert_called_once_with(
                method='DELETE',
                url='https://api.example.com/test',
                params=None,
                json=None,
                timeout=30
            )
    
    def test_rate_limit_exception(self, valid_api_key):
        """Test rate limit exception handling."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 429
            mock_response.ok = False
            mock_response.headers = {'Retry-After': '60'}
            mock_response.text = "Rate limit exceeded"
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=0)
            
            with pytest.raises(RateLimitException) as exc_info:
                client.get("/test")
            
            assert exc_info.value.status_code == 429
            assert exc_info.value.retry_after == 60
            assert "Rate limit exceeded" in str(exc_info.value)
    
    def test_rate_limit_with_retry(self, valid_api_key):
        """Test rate limit with retry logic."""
        with patch('requests.Session.request') as mock_request, \
             patch('time.sleep') as mock_sleep:
            
            # First call returns rate limit, second call succeeds
            rate_limit_response = Mock()
            rate_limit_response.status_code = 429
            rate_limit_response.ok = False
            rate_limit_response.headers = {'Retry-After': '1'}
            rate_limit_response.text = "Rate limit exceeded"
            
            success_response = Mock()
            success_response.status_code = 200
            success_response.ok = True
            success_response.json.return_value = {"success": True}
            
            mock_request.side_effect = [rate_limit_response, success_response]
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=1, retry_delay=0.1)
            result = client.get("/test")
            
            assert result == {"success": True}
            assert mock_request.call_count == 2
            mock_sleep.assert_called_once_with(1)  # Retry-After value
    
    def test_api_exception_4xx(self, valid_api_key):
        """Test API exception for 4xx errors."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.ok = False
            mock_response.json.return_value = {
                "error": "Bad Request",
                "message": "Invalid parameters",
                "details": {"field": "name"}
            }
            mock_response.text = '{"error": "Bad Request"}'
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=0)
            
            with pytest.raises(ApiException) as exc_info:
                client.get("/test")
            
            assert exc_info.value.status_code == 400
            assert exc_info.value.is_client_error is True
            assert exc_info.value.is_server_error is False
            assert exc_info.value.details == {"field": "name"}
    
    def test_api_exception_5xx(self, valid_api_key):
        """Test API exception for 5xx errors."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 500
            mock_response.ok = False
            mock_response.json.return_value = {
                "error": "Internal Server Error",
                "message": "Something went wrong"
            }
            mock_response.text = '{"error": "Internal Server Error"}'
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=0)
            
            with pytest.raises(ApiException) as exc_info:
                client.get("/test")
            
            assert exc_info.value.status_code == 500
            assert exc_info.value.is_client_error is False
            assert exc_info.value.is_server_error is True
    
    def test_network_exception_timeout(self, valid_api_key):
        """Test network exception for timeout."""
        with patch('requests.Session.request') as mock_request:
            mock_request.side_effect = requests.exceptions.Timeout("Request timeout")
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=0)
            
            with pytest.raises(NetworkException) as exc_info:
                client.get("/test")
            
            assert "Request timeout" in str(exc_info.value)
    
    def test_network_exception_connection_error(self, valid_api_key):
        """Test network exception for connection error."""
        with patch('requests.Session.request') as mock_request:
            mock_request.side_effect = requests.exceptions.ConnectionError("Connection error")
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=0)
            
            with pytest.raises(NetworkException) as exc_info:
                client.get("/test")
            
            assert "Connection error" in str(exc_info.value)
    
    def test_network_exception_general_request_error(self, valid_api_key):
        """Test network exception for general request error."""
        with patch('requests.Session.request') as mock_request:
            mock_request.side_effect = requests.exceptions.RequestException("General error")
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=0)
            
            with pytest.raises(NetworkException) as exc_info:
                client.get("/test")
            
            assert "General error" in str(exc_info.value)
    
    def test_retry_with_exponential_backoff(self, valid_api_key):
        """Test retry with exponential backoff."""
        with patch('requests.Session.request') as mock_request, \
             patch('time.sleep') as mock_sleep:
            
            # All calls fail with network error
            mock_request.side_effect = requests.exceptions.RequestException("Network error")
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=2, retry_delay=0.1)
            
            with pytest.raises(NetworkException):
                client.get("/test")
            
            # Should have made 3 calls (initial + 2 retries)
            assert mock_request.call_count == 3
            
            # Should have slept with exponential backoff: 0.1, 0.2
            expected_sleeps = [0.1, 0.2]
            actual_sleeps = [call[0][0] for call in mock_sleep.call_args_list]
            assert actual_sleeps == expected_sleeps
    
    def test_handle_error_response_with_json(self, valid_api_key):
        """Test error response handling with JSON."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.ok = False
            mock_response.json.return_value = {
                "message": "Custom error message",
                "details": {"field": "test"}
            }
            mock_response.text = '{"message": "Custom error message"}'
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=0)
            
            with pytest.raises(ApiException) as exc_info:
                client.get("/test")
            
            assert exc_info.value.message == "Custom error message"
            assert exc_info.value.details == {"field": "test"}
    
    def test_handle_error_response_without_json(self, valid_api_key):
        """Test error response handling without JSON."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 400
            mock_response.ok = False
            mock_response.json.side_effect = ValueError("Invalid JSON")
            mock_response.text = "Plain text error"
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key, retry_attempts=0)
            
            with pytest.raises(ApiException) as exc_info:
                client.get("/test")
            
            assert exc_info.value.message == "Plain text error"
            assert exc_info.value.details == {}
    
    def test_close_session(self, valid_api_key):
        """Test session closing."""
        with patch('requests.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value = mock_session
            
            client = HttpClient("https://api.example.com", valid_api_key)
            client.close()
            
            mock_session.close.assert_called_once()
    
    def test_context_manager(self, valid_api_key):
        """Test context manager functionality."""
        with patch('requests.Session') as mock_session_class:
            mock_session = Mock()
            mock_session_class.return_value = mock_session
            
            with HttpClient("https://api.example.com", valid_api_key) as client:
                assert client is not None
            
            mock_session.close.assert_called_once()
    
    def test_url_joining(self, valid_api_key):
        """Test URL joining functionality."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.ok = True
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com/", valid_api_key)
            client.get("/test")
            
            # Should join URLs correctly
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[1]['url'] == 'https://api.example.com/test'
    
    def test_url_joining_with_trailing_slash(self, valid_api_key):
        """Test URL joining with trailing slash in endpoint."""
        with patch('requests.Session.request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.ok = True
            mock_response.json.return_value = {"success": True}
            mock_request.return_value = mock_response
            
            client = HttpClient("https://api.example.com", valid_api_key)
            client.get("test/")
            
            # Should join URLs correctly
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[1]['url'] == 'https://api.example.com/test/'
