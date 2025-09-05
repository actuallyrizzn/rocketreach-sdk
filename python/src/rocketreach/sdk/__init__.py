"""
RocketReach SDK Core Module

This module contains the main client and core functionality for the RocketReach SDK.
"""

from .client import RocketReachClient
from .exceptions import (
    RocketReachException,
    ApiException,
    InvalidApiKeyException,
    RateLimitException,
    NetworkException,
)
from .models import (
    SearchQuery,
    LookupQuery,
    SearchResponse,
    PersonResponse,
    EnrichResponse,
)

__all__ = [
    "RocketReachClient",
    "RocketReachException",
    "ApiException",
    "InvalidApiKeyException",
    "RateLimitException",
    "NetworkException",
    "SearchQuery",
    "LookupQuery",
    "SearchResponse",
    "PersonResponse",
    "EnrichResponse",
]
