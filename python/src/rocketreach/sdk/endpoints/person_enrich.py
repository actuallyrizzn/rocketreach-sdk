"""
Person Enrich Endpoint

Handles person enrichment operations.
"""

from typing import Optional, Union, Dict, Any
from ..models import LookupQuery, EnrichResponse
from ..http import HttpClient


class PersonEnrich:
    """
    Person Enrich endpoint client.
    
    Provides methods for enriching person data with additional information
    including contact details and company information.
    """
    
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
        self._query = LookupQuery()
    
    def id(self, person_id: int) -> 'PersonEnrich':
        """
        Set the person ID for the enrichment.
        
        Args:
            person_id: The person's ID in the RocketReach database
            
        Returns:
            Self for method chaining
        """
        self._query.set_id(person_id)
        return self
    
    def linkedin_url(self, url: str) -> 'PersonEnrich':
        """
        Set the LinkedIn URL for the enrichment.
        
        Args:
            url: The person's LinkedIn profile URL
            
        Returns:
            Self for method chaining
        """
        self._query.set_linkedin_url(url)
        return self
    
    def name(self, name: str) -> 'PersonEnrich':
        """
        Set the name for the enrichment.
        
        Args:
            name: The person's name
            
        Returns:
            Self for method chaining
        """
        self._query.set_name(name)
        return self
    
    def current_employer(self, employer: str) -> 'PersonEnrich':
        """
        Set the current employer for the enrichment.
        
        Args:
            employer: The person's current employer
            
        Returns:
            Self for method chaining
        """
        self._query.set_current_employer(employer)
        return self
    
    def title(self, title: str) -> 'PersonEnrich':
        """
        Set the title for the enrichment.
        
        Args:
            title: The person's current title
            
        Returns:
            Self for method chaining
        """
        self._query.set_title(title)
        return self
    
    def email(self, email: str) -> 'PersonEnrich':
        """
        Set the email for the enrichment.
        
        Args:
            email: The person's email address
            
        Returns:
            Self for method chaining
        """
        self._query.set_email(email)
        return self
    
    def npi_number(self, npi: int) -> 'PersonEnrich':
        """
        Set the NPI number for the enrichment.
        
        Args:
            npi: The person's National Provider Identifier number
            
        Returns:
            Self for method chaining
        """
        self._query.set_npi_number(npi)
        return self
    
    def enrich(self) -> EnrichResponse:
        """
        Execute the enrichment with the current query parameters.
        
        Returns:
            EnrichResponse containing the enriched person and company data
            
        Raises:
            ApiException: If the API request fails
        """
        params = self._query.to_dict()
        response_data = self._http_client.get('/profile-company/lookup', params=params)
        return EnrichResponse(response_data)
    
    def reset(self) -> 'PersonEnrich':
        """
        Reset the query parameters to defaults.
        
        Returns:
            Self for method chaining
        """
        self._query = LookupQuery()
        return self
