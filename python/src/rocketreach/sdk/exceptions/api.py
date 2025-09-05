"""
API-Specific Exception Classes

Specific exception classes for different types of API errors.
"""

from typing import Optional, Dict, Any
from .base import ApiException


class InvalidApiKeyException(ApiException):
    """
    Exception raised when the API key is invalid or missing.
    """
    
    def __init__(
        self,
        message: str = "Invalid or missing API key",
        status_code: int = 401,
        response_text: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs
    ):
        super().__init__(message, status_code, response_text, details, *args, **kwargs)


class RateLimitException(ApiException):
    """
    Exception raised when the API rate limit is exceeded.
    """
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        status_code: int = 429,
        response_text: Optional[str] = None,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs
    ):
        super().__init__(message, status_code, response_text, details, *args, **kwargs)
        self.retry_after = retry_after
    
    def __str__(self) -> str:
        """String representation of the exception."""
        parts = [self.message]
        
        if self.retry_after is not None:
            parts.append(f"Retry after: {self.retry_after} seconds")
        
        if self.status_code is not None:
            parts.append(f"Status: {self.status_code}")
        
        return " | ".join(parts)


class NetworkException(ApiException):
    """
    Exception raised for network-related errors.
    """
    
    def __init__(
        self,
        message: str = "Network error",
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs
    ):
        super().__init__(message, status_code, response_text, details, *args, **kwargs)
