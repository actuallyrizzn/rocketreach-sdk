"""
RocketReach Client

Main client class for interacting with the RocketReach API.
"""

from typing import Optional, Dict, Any
import requests
from .exceptions import InvalidApiKeyException, ApiException
from .endpoints import PeopleSearch, PersonLookup, PersonEnrich
from .http import HttpClient


class RocketReachClient:
    """
    Main client for interacting with the RocketReach API.
    
    This client provides access to all RocketReach API endpoints through
    a simple, fluent interface.
    
    Args:
        api_key (str): Your RocketReach API key
        base_url (str, optional): Base URL for the API. Defaults to production URL.
        timeout (int, optional): Request timeout in seconds. Defaults to 30.
        retry_attempts (int, optional): Number of retry attempts for failed requests. Defaults to 3.
        retry_delay (float, optional): Delay between retry attempts in seconds. Defaults to 1.0.
    
    Example:
        >>> client = RocketReachClient("your-api-key")
        >>> results = client.people_search().name(["John Doe"]).search()
        >>> person = client.person_lookup().name("John Doe").lookup()
        >>> enriched = client.person_enrich().name("John Doe").enrich()
    """
    
    DEFAULT_BASE_URL = "https://api.rocketreach.co/api/v2"
    DEFAULT_TIMEOUT = 30
    DEFAULT_RETRY_ATTEMPTS = 3
    DEFAULT_RETRY_DELAY = 1.0
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        retry_attempts: int = DEFAULT_RETRY_ATTEMPTS,
        retry_delay: float = DEFAULT_RETRY_DELAY,
    ):
        if not api_key or not api_key.strip():
            raise InvalidApiKeyException("API key cannot be empty")
        
        self._api_key = api_key.strip()
        self._base_url = base_url or self.DEFAULT_BASE_URL
        self._timeout = timeout
        self._retry_attempts = retry_attempts
        self._retry_delay = retry_delay
        
        # Initialize HTTP client
        self._http_client = HttpClient(
            base_url=self._base_url,
            api_key=self._api_key,
            timeout=self._timeout,
            retry_attempts=self._retry_attempts,
            retry_delay=self._retry_delay,
        )
        
        # HTTP client is already stored in self._http_client
    
    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self._api_key
    
    @property
    def base_url(self) -> str:
        """Get the base URL."""
        return self._base_url
    
    @property
    def timeout(self) -> int:
        """Get the request timeout."""
        return self._timeout
    
    @property
    def retry_attempts(self) -> int:
        """Get the number of retry attempts."""
        return self._retry_attempts
    
    @property
    def retry_delay(self) -> float:
        """Get the retry delay."""
        return self._retry_delay
    
    def people_search(self) -> PeopleSearch:
        """
        Get the People Search endpoint client.
        
        Returns:
            PeopleSearch: The people search endpoint client
        """
        return PeopleSearch(self._http_client)
    
    def person_lookup(self) -> PersonLookup:
        """
        Get the Person Lookup endpoint client.
        
        Returns:
            PersonLookup: The person lookup endpoint client
        """
        return PersonLookup(self._http_client)
    
    def person_enrich(self) -> PersonEnrich:
        """
        Get the Person Enrich endpoint client.
        
        Returns:
            PersonEnrich: The person enrich endpoint client
        """
        return PersonEnrich(self._http_client)
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information and usage statistics.
        
        Returns:
            Dict[str, Any]: Account information including credits, usage, etc.
            
        Raises:
            ApiException: If the API request fails
        """
        return self._http_client.get("/account")
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Check the health status of the API.
        
        Returns:
            Dict[str, Any]: Health status information
            
        Raises:
            ApiException: If the API request fails
        """
        return self._http_client.get("/health")
    
    def __repr__(self) -> str:
        """String representation of the client."""
        return f"RocketReachClient(api_key='{self._api_key[:8]}...', base_url='{self._base_url}')"
    
    def __str__(self) -> str:
        """String representation of the client."""
        return self.__repr__()
