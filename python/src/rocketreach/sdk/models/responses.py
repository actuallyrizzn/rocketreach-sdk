"""
Response Models

Data models for API responses.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field


@dataclass
class SearchResponse:
    """
    Response model for people search results.
    
    This class represents the response from a people search API call,
    including the profiles found and pagination information.
    """
    
    profiles: List[Dict[str, Any]] = field(default_factory=list)
    pagination: Dict[str, Any] = field(default_factory=dict)
    
    def __init__(self, data: Dict[str, Any]):
        """Initialize from API response data."""
        self.profiles = data.get('profiles', [])
        self.pagination = data.get('pagination', {})
    
    @property
    def count(self) -> int:
        """Get the number of profiles in this response."""
        return len(self.profiles)
    
    @property
    def total(self) -> int:
        """Get the total number of profiles available."""
        return self.pagination.get('total', 0)
    
    @property
    def current_page(self) -> int:
        """Get the current page number."""
        return self.pagination.get('start', 1)
    
    @property
    def next_page(self) -> Optional[int]:
        """Get the next page number, if available."""
        return self.pagination.get('next')
    
    @property
    def has_next_page(self) -> bool:
        """Check if there are more pages available."""
        return self.next_page is not None
    
    @property
    def is_empty(self) -> bool:
        """Check if the response is empty."""
        return self.count == 0
    
    def get_profiles(self) -> List[Dict[str, Any]]:
        """Get the list of profiles."""
        return self.profiles
    
    def get_pagination(self) -> Dict[str, Any]:
        """Get the pagination information."""
        return self.pagination


@dataclass
class PersonResponse:
    """
    Response model for person lookup results.
    
    This class represents the response from a person lookup API call,
    containing detailed information about a specific person.
    """
    
    data: Dict[str, Any] = field(default_factory=dict)
    
    def __init__(self, data: Dict[str, Any]):
        """Initialize from API response data."""
        self.data = data
    
    @property
    def id(self) -> Optional[int]:
        """Get the person ID."""
        return self.data.get('id')
    
    @property
    def name(self) -> Optional[str]:
        """Get the person's name."""
        return self.data.get('name')
    
    @property
    def current_title(self) -> Optional[str]:
        """Get the person's current title."""
        return self.data.get('current_title')
    
    @property
    def current_employer(self) -> Optional[str]:
        """Get the person's current employer."""
        return self.data.get('current_employer')
    
    @property
    def linkedin_url(self) -> Optional[str]:
        """Get the person's LinkedIn URL."""
        return self.data.get('linkedin_url')
    
    @property
    def location(self) -> Optional[str]:
        """Get the person's location."""
        return self.data.get('location')
    
    @property
    def status(self) -> Optional[str]:
        """Get the person's status."""
        return self.data.get('status')
    
    @property
    def is_complete(self) -> bool:
        """Check if the person data is complete."""
        return self.status == 'complete'
    
    @property
    def is_searching(self) -> bool:
        """Check if the person data is still being searched."""
        return self.status == 'searching'
    
    def get_emails(self) -> List[Dict[str, Any]]:
        """Get the person's email addresses."""
        return self.data.get('emails', [])
    
    def get_phones(self) -> List[Dict[str, Any]]:
        """Get the person's phone numbers."""
        return self.data.get('phones', [])
    
    def get_raw_data(self) -> Dict[str, Any]:
        """Get the raw response data."""
        return self.data


@dataclass
class EnrichResponse:
    """
    Response model for person enrichment results.
    
    This class represents the response from a person enrichment API call,
    containing both person and company information.
    """
    
    person: Dict[str, Any] = field(default_factory=dict)
    company: Dict[str, Any] = field(default_factory=dict)
    
    def __init__(self, data: Dict[str, Any]):
        """Initialize from API response data."""
        # The API returns a flat structure, not separate person/company objects
        self.person = data
        self.company = {
            'id': data.get('current_employer_id'),
            'name': data.get('current_employer'),
            'domain': data.get('current_employer_domain'),
            'website': data.get('current_employer_website'),
            'linkedin_url': data.get('current_employer_linkedin_url')
        }
    
    # Person properties
    @property
    def person_id(self) -> Optional[int]:
        """Get the person ID."""
        return self.person.get('id')
    
    @property
    def person_name(self) -> Optional[str]:
        """Get the person's name."""
        return self.person.get('name')
    
    @property
    def person_emails(self) -> List[Dict[str, Any]]:
        """Get the person's email addresses."""
        return self.person.get('emails', [])
    
    @property
    def person_phones(self) -> List[Dict[str, Any]]:
        """Get the person's phone numbers."""
        return self.person.get('phones', [])
    
    # Company properties
    @property
    def company_id(self) -> Optional[int]:
        """Get the company ID."""
        return self.company.get('id')
    
    @property
    def company_name(self) -> Optional[str]:
        """Get the company name."""
        return self.company.get('name')
    
    @property
    def company_domain(self) -> Optional[str]:
        """Get the company domain."""
        return self.company.get('domain')
    
    @property
    def company_industry(self) -> Optional[str]:
        """Get the company industry."""
        return self.company.get('industry')
    
    @property
    def company_employee_count(self) -> Optional[str]:
        """Get the company employee count."""
        return self.company.get('employee_count')
    
    @property
    def company_location(self) -> Optional[str]:
        """Get the company location."""
        return self.company.get('location')
    
    def get_person_data(self) -> Dict[str, Any]:
        """Get the person data."""
        return self.person
    
    def get_company_data(self) -> Dict[str, Any]:
        """Get the company data."""
        return self.company
