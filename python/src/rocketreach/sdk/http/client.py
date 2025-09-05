"""
HTTP Client

Handles HTTP requests to the RocketReach API with retry logic and error handling.
"""

import time
import requests
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin
from ..exceptions import ApiException, RateLimitException, NetworkException


class HttpClient:
    """
    HTTP client for making requests to the RocketReach API.
    
    Handles authentication, retries, rate limiting, and error responses.
    """
    
    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
        retry_attempts: int = 3,
        retry_delay: float = 1.0,
    ):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        
        # Create session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'Api-Key': api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'RocketReach-Python-SDK/1.0.0',
        })
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Dict containing the response data
            
        Raises:
            ApiException: If the API returns an error
            RateLimitException: If rate limit is exceeded
            NetworkException: If there's a network error
        """
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Dict containing the response data
            
        Raises:
            ApiException: If the API returns an error
            RateLimitException: If rate limit is exceeded
            NetworkException: If there's a network error
        """
        return self._make_request('POST', endpoint, json=data)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a PUT request to the API.
        
        Args:
            endpoint: API endpoint path
            data: Request body data
            
        Returns:
            Dict containing the response data
            
        Raises:
            ApiException: If the API returns an error
            RateLimitException: If rate limit is exceeded
            NetworkException: If there's a network error
        """
        return self._make_request('PUT', endpoint, json=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Make a DELETE request to the API.
        
        Args:
            endpoint: API endpoint path
            
        Returns:
            Dict containing the response data
            
        Raises:
            ApiException: If the API returns an error
            RateLimitException: If rate limit is exceeded
            NetworkException: If there's a network error
        """
        return self._make_request('DELETE', endpoint)
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with retry logic.
        
        Args:
            method: HTTP method
            endpoint: API endpoint path
            params: Query parameters
            json: JSON body data
            
        Returns:
            Dict containing the response data
            
        Raises:
            ApiException: If the API returns an error
            RateLimitException: If rate limit is exceeded
            NetworkException: If there's a network error
        """
        url = urljoin(self.base_url, endpoint.lstrip('/'))
        
        last_exception = None
        
        for attempt in range(self.retry_attempts + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json,
                    timeout=self.timeout,
                )
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    if attempt < self.retry_attempts:
                        time.sleep(retry_after)
                        continue
                    else:
                        raise RateLimitException(
                            "Rate limit exceeded",
                            response.status_code,
                            response.text,
                            retry_after
                        )
                
                # Handle other HTTP errors (201 is also success)
                if not response.ok and response.status_code != 201:
                    self._handle_error_response(response)
                
                return response.json()
                
            except requests.exceptions.Timeout:
                last_exception = NetworkException("Request timeout")
            except requests.exceptions.ConnectionError:
                last_exception = NetworkException("Connection error")
            except requests.exceptions.RequestException as e:
                last_exception = NetworkException(f"Request failed: {str(e)}")
            
            # If this isn't the last attempt, wait before retrying
            if attempt < self.retry_attempts:
                time.sleep(self.retry_delay * (2 ** attempt))  # Exponential backoff
        
        # If we've exhausted all retry attempts, raise the last exception
        if last_exception:
            raise last_exception
        
        # This should never be reached, but just in case
        raise NetworkException("Request failed after all retry attempts")
    
    def _handle_error_response(self, response: requests.Response) -> None:
        """
        Handle error responses from the API.
        
        Args:
            response: The HTTP response object
            
        Raises:
            ApiException: For API errors
        """
        try:
            error_data = response.json()
            message = error_data.get('message', 'Unknown error')
            details = error_data.get('details', {})
        except ValueError:
            message = response.text or 'Unknown error'
            details = {}
        
        raise ApiException(
            message,
            response.status_code,
            response.text,
            details
        )
    
    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
