"""
Query Models

Data models for API request parameters.
"""

from typing import List, Optional, Dict, Any, Union
from dataclasses import dataclass, field


@dataclass
class SearchQuery:
    """
    Query model for people search requests.
    
    This class represents the parameters for searching people in the RocketReach database.
    All parameters are optional and can be combined to create specific search criteria.
    """
    
    # Basic search parameters
    name: Optional[List[str]] = None
    current_title: Optional[List[str]] = None
    current_employer: Optional[List[str]] = None
    current_employer_domain: Optional[List[str]] = None
    location: Optional[List[str]] = None
    linkedin_url: Optional[List[str]] = None
    contact_method: Optional[List[str]] = None
    
    # Company filters
    industry: Optional[List[str]] = None
    company_size: Optional[List[str]] = None
    company_funding: Optional[List[str]] = None
    company_revenue: Optional[List[str]] = None
    
    # Professional filters
    seniority: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    education: Optional[List[str]] = None
    
    # Pagination
    page: int = 1
    page_size: int = 10
    order_by: str = "relevance"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary for API requests.
        
        Returns:
            Dict containing the query parameters
        """
        data = {}
        
        # Add parameters that are not None
        for field_name, value in self.__dict__.items():
            if value is not None:
                # Convert field names to API parameter names
                api_name = field_name.replace('_', '_')
                data[api_name] = value
        
        return data
    
    def set_name(self, names: Union[str, List[str]]) -> 'SearchQuery':
        """Set the name parameter."""
        if isinstance(names, str):
            names = [names]
        self.name = names
        return self
    
    def set_current_title(self, titles: Union[str, List[str]]) -> 'SearchQuery':
        """Set the current title parameter."""
        if isinstance(titles, str):
            titles = [titles]
        self.current_title = titles
        return self
    
    def set_current_employer(self, employers: Union[str, List[str]]) -> 'SearchQuery':
        """Set the current employer parameter."""
        if isinstance(employers, str):
            employers = [employers]
        self.current_employer = employers
        return self
    
    def set_current_employer_domain(self, domains: Union[str, List[str]]) -> 'SearchQuery':
        """Set the current employer domain parameter."""
        if isinstance(domains, str):
            domains = [domains]
        self.current_employer_domain = domains
        return self
    
    def set_location(self, locations: Union[str, List[str]]) -> 'SearchQuery':
        """Set the location parameter."""
        if isinstance(locations, str):
            locations = [locations]
        self.location = locations
        return self
    
    def set_linkedin_url(self, urls: Union[str, List[str]]) -> 'SearchQuery':
        """Set the LinkedIn URL parameter."""
        if isinstance(urls, str):
            urls = [urls]
        self.linkedin_url = urls
        return self
    
    def set_contact_method(self, methods: Union[str, List[str]]) -> 'SearchQuery':
        """Set the contact method parameter."""
        if isinstance(methods, str):
            methods = [methods]
        self.contact_method = methods
        return self
    
    def set_industry(self, industries: Union[str, List[str]]) -> 'SearchQuery':
        """Set the industry parameter."""
        if isinstance(industries, str):
            industries = [industries]
        self.industry = industries
        return self
    
    def set_company_size(self, sizes: Union[str, List[str]]) -> 'SearchQuery':
        """Set the company size parameter."""
        if isinstance(sizes, str):
            sizes = [sizes]
        self.company_size = sizes
        return self
    
    def set_company_funding(self, funding: Union[str, List[str]]) -> 'SearchQuery':
        """Set the company funding parameter."""
        if isinstance(funding, str):
            funding = [funding]
        self.company_funding = funding
        return self
    
    def set_company_revenue(self, revenue: Union[str, List[str]]) -> 'SearchQuery':
        """Set the company revenue parameter."""
        if isinstance(revenue, str):
            revenue = [revenue]
        self.company_revenue = revenue
        return self
    
    def set_seniority(self, seniorities: Union[str, List[str]]) -> 'SearchQuery':
        """Set the seniority parameter."""
        if isinstance(seniorities, str):
            seniorities = [seniorities]
        self.seniority = seniorities
        return self
    
    def set_skills(self, skills: Union[str, List[str]]) -> 'SearchQuery':
        """Set the skills parameter."""
        if isinstance(skills, str):
            skills = [skills]
        self.skills = skills
        return self
    
    def set_education(self, education: Union[str, List[str]]) -> 'SearchQuery':
        """Set the education parameter."""
        if isinstance(education, str):
            education = [education]
        self.education = education
        return self
    
    def set_page(self, page: int) -> 'SearchQuery':
        """Set the page parameter."""
        self.page = page
        return self
    
    def set_page_size(self, page_size: int) -> 'SearchQuery':
        """Set the page size parameter."""
        self.page_size = page_size
        return self
    
    def set_order_by(self, order_by: str) -> 'SearchQuery':
        """Set the order by parameter."""
        self.order_by = order_by
        return self


@dataclass
class LookupQuery:
    """
    Query model for person lookup requests.
    
    This class represents the parameters for looking up a specific person
    in the RocketReach database.
    """
    
    # Lookup parameters (at least one is required)
    id: Optional[int] = None
    linkedin_url: Optional[str] = None
    name: Optional[str] = None
    current_employer: Optional[str] = None
    title: Optional[str] = None
    email: Optional[str] = None
    npi_number: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the query to a dictionary for API requests.
        
        Returns:
            Dict containing the query parameters
        """
        data = {}
        
        # Add parameters that are not None
        for field_name, value in self.__dict__.items():
            if value is not None:
                # Convert field names to API parameter names
                api_name = field_name.replace('_', '_')
                data[api_name] = value
        
        return data
    
    def set_id(self, person_id: int) -> 'LookupQuery':
        """Set the person ID."""
        self.id = person_id
        return self
    
    def set_linkedin_url(self, url: str) -> 'LookupQuery':
        """Set the LinkedIn URL."""
        self.linkedin_url = url
        return self
    
    def set_name(self, name: str) -> 'LookupQuery':
        """Set the name."""
        self.name = name
        return self
    
    def set_current_employer(self, employer: str) -> 'LookupQuery':
        """Set the current employer."""
        self.current_employer = employer
        return self
    
    def set_title(self, title: str) -> 'LookupQuery':
        """Set the title."""
        self.title = title
        return self
    
    def set_email(self, email: str) -> 'LookupQuery':
        """Set the email."""
        self.email = email
        return self
    
    def set_npi_number(self, npi: int) -> 'LookupQuery':
        """Set the NPI number."""
        self.npi_number = npi
        return self
