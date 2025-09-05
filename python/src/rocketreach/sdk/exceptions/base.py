"""
Base Exception Classes

Base exception classes for the RocketReach SDK.
"""

from typing import Optional, Dict, Any


class RocketReachException(Exception):
    """
    Base exception class for all RocketReach SDK exceptions.
    """
    
    def __init__(self, message: str, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.message = message


class ApiException(RocketReachException):
    """
    Exception raised for API-related errors.
    
    This is the base class for all API-specific exceptions.
    """
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        *args,
        **kwargs
    ):
        super().__init__(message, *args, **kwargs)
        self.status_code = status_code
        self.response_text = response_text
        self.details = details or {}
    
    @property
    def is_client_error(self) -> bool:
        """Check if this is a client error (4xx status code)."""
        return self.status_code is not None and 400 <= self.status_code < 500
    
    @property
    def is_server_error(self) -> bool:
        """Check if this is a server error (5xx status code)."""
        return self.status_code is not None and 500 <= self.status_code < 600
    
    def __str__(self) -> str:
        """String representation of the exception."""
        parts = [self.message]
        
        if self.status_code is not None:
            parts.append(f"Status: {self.status_code}")
        
        if self.details:
            parts.append(f"Details: {self.details}")
        
        return " | ".join(parts)
