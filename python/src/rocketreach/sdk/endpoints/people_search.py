"""
People Search Endpoint

Handles people search operations.
"""

from typing import List, Optional, Union, Dict, Any
from ..models import SearchQuery, SearchResponse
from ..http import HttpClient


class PeopleSearch:
    """
    People Search endpoint client.
    
    Provides methods for searching people in the RocketReach database
    with various filters and criteria.
    """
    
    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
        self._query = SearchQuery()
    
    def name(self, names: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the name filter for the search.
        
        Args:
            names: Name or list of names to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_name(names)
        return self
    
    def current_title(self, titles: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the current title filter for the search.
        
        Args:
            titles: Title or list of titles to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_current_title(titles)
        return self
    
    def current_employer(self, employers: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the current employer filter for the search.
        
        Args:
            employers: Employer or list of employers to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_current_employer(employers)
        return self
    
    def current_employer_domain(self, domains: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the current employer domain filter for the search.
        
        Args:
            domains: Domain or list of domains to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_current_employer_domain(domains)
        return self
    
    def location(self, locations: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the location filter for the search.
        
        Args:
            locations: Location or list of locations to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_location(locations)
        return self
    
    def linkedin_url(self, urls: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the LinkedIn URL filter for the search.
        
        Args:
            urls: LinkedIn URL or list of URLs to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_linkedin_url(urls)
        return self
    
    def contact_method(self, methods: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the contact method filter for the search.
        
        Args:
            methods: Contact method or list of methods to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_contact_method(methods)
        return self
    
    def industry(self, industries: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the industry filter for the search.
        
        Args:
            industries: Industry or list of industries to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_industry(industries)
        return self
    
    def company_size(self, sizes: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the company size filter for the search.
        
        Args:
            sizes: Company size or list of sizes to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_company_size(sizes)
        return self
    
    def company_funding(self, funding: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the company funding filter for the search.
        
        Args:
            funding: Company funding or list of funding levels to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_company_funding(funding)
        return self
    
    def company_revenue(self, revenue: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the company revenue filter for the search.
        
        Args:
            revenue: Company revenue or list of revenue levels to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_company_revenue(revenue)
        return self
    
    def seniority(self, seniorities: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the seniority filter for the search.
        
        Args:
            seniorities: Seniority level or list of levels to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_seniority(seniorities)
        return self
    
    def skills(self, skills: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the skills filter for the search.
        
        Args:
            skills: Skill or list of skills to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_skills(skills)
        return self
    
    def education(self, education: Union[str, List[str]]) -> 'PeopleSearch':
        """
        Set the education filter for the search.
        
        Args:
            education: Education or list of education levels to search for
            
        Returns:
            Self for method chaining
        """
        self._query.set_education(education)
        return self
    
    def page(self, page: int) -> 'PeopleSearch':
        """
        Set the page number for pagination.
        
        Args:
            page: Page number (1-based)
            
        Returns:
            Self for method chaining
        """
        self._query.set_page(page)
        return self
    
    def page_size(self, page_size: int) -> 'PeopleSearch':
        """
        Set the page size for pagination.
        
        Args:
            page_size: Number of results per page
            
        Returns:
            Self for method chaining
        """
        self._query.set_page_size(page_size)
        return self
    
    def order_by(self, order_by: str) -> 'PeopleSearch':
        """
        Set the ordering for the search results.
        
        Args:
            order_by: Field to order by (e.g., 'relevance', 'name')
            
        Returns:
            Self for method chaining
        """
        self._query.set_order_by(order_by)
        return self
    
    def search(self) -> SearchResponse:
        """
        Execute the search with the current query parameters.
        
        Returns:
            SearchResponse containing the search results
            
        Raises:
            ApiException: If the API request fails
        """
        query_data = self._query.to_dict()
        
        # Extract pagination and ordering parameters from query
        page = query_data.pop('page', 1)
        page_size = query_data.pop('page_size', 10)
        order_by = query_data.pop('order_by', 'relevance')
        
        # Create payload with query object and top-level pagination/ordering
        payload = {
            "query": query_data,
            "page": page,
            "page_size": page_size,
            "order_by": order_by
        }
        
        response_data = self._http_client.post('/person/search', data=payload)
        return SearchResponse(response_data)
    
    def reset(self) -> 'PeopleSearch':
        """
        Reset the query parameters to defaults.
        
        Returns:
            Self for method chaining
        """
        self._query = SearchQuery()
        return self
