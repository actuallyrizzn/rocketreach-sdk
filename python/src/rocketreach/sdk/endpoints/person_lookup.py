"""
Person Lookup Endpoint

Handles person lookup operations.
"""

from typing import Optional, Union, Dict, Any
from ..models import LookupQuery, PersonResponse
from ..http import HttpClient


class PersonLookup:
    """
    Person Lookup endpoint client.
    
    Provides methods for looking up specific people in the RocketReach database
    using various identifiers.
    """
    
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
        self._query = LookupQuery()
    
    def id(self, person_id: int) -> 'PersonLookup':
        """
        Set the person ID for the lookup.
        
        Args:
            person_id: The person's ID in the RocketReach database
            
        Returns:
            Self for method chaining
        """
        self._query.set_id(person_id)
        return self
    
    def linkedin_url(self, url: str) -> 'PersonLookup':
        """
        Set the LinkedIn URL for the lookup.
        
        Args:
            url: The person's LinkedIn profile URL
            
        Returns:
            Self for method chaining
        """
        self._query.set_linkedin_url(url)
        return self
    
    def name(self, name: str) -> 'PersonLookup':
        """
        Set the name for the lookup.
        
        Args:
            name: The person's name
            
        Returns:
            Self for method chaining
        """
        self._query.set_name(name)
        return self
    
    def current_employer(self, employer: str) -> 'PersonLookup':
        """
        Set the current employer for the lookup.
        
        Args:
            employer: The person's current employer
            
        Returns:
            Self for method chaining
        """
        self._query.set_current_employer(employer)
        return self
    
    def title(self, title: str) -> 'PersonLookup':
        """
        Set the title for the lookup.
        
        Args:
            title: The person's current title
            
        Returns:
            Self for method chaining
        """
        self._query.set_title(title)
        return self
    
    def email(self, email: str) -> 'PersonLookup':
        """
        Set the email for the lookup.
        
        Args:
            email: The person's email address
            
        Returns:
            Self for method chaining
        """
        self._query.set_email(email)
        return self
    
    def npi_number(self, npi: int) -> 'PersonLookup':
        """
        Set the NPI number for the lookup.
        
        Args:
            npi: The person's National Provider Identifier number
            
        Returns:
            Self for method chaining
        """
        self._query.set_npi_number(npi)
        return self
    
    def lookup(self) -> PersonResponse:
        """
        Execute the lookup with the current query parameters.
        
        Returns:
            PersonResponse containing the person data
            
        Raises:
            ApiException: If the API request fails
        """
        params = self._query.to_dict()
        response_data = self._http_client.get('/person/lookup', params=params)
        return PersonResponse(response_data)
    
    def reset(self) -> 'PersonLookup':
        """
        Reset the query parameters to defaults.
        
        Returns:
            Self for method chaining
        """
        self._query = LookupQuery()
        return self
