"""
Unit tests for the model classes.
"""

import pytest
from rocketreach.sdk.models import SearchQuery, LookupQuery, SearchResponse, PersonResponse, EnrichResponse


class TestSearchQuery:
    """Test cases for SearchQuery model."""
    
    def test_init_default_values(self):
        """Test default initialization values."""
        query = SearchQuery()
        assert query.name is None
        assert query.current_title is None
        assert query.current_employer is None
        assert query.page == 1
        assert query.page_size == 10
        assert query.order_by == "relevance"
    
    def test_to_dict_empty(self):
        """Test to_dict with empty query."""
        query = SearchQuery()
        result = query.to_dict()
        assert result == {}
    
    def test_to_dict_with_values(self):
        """Test to_dict with values."""
        query = SearchQuery()
        query.name = ["John Doe"]
        query.current_employer = ["Google"]
        query.page = 2
        query.page_size = 25
        
        result = query.to_dict()
        assert result["name"] == ["John Doe"]
        assert result["current_employer"] == ["Google"]
        assert result["page"] == 2
        assert result["page_size"] == 25
    
    def test_set_name_string(self):
        """Test set_name with string input."""
        query = SearchQuery()
        result = query.set_name("John Doe")
        
        assert result is query  # Method chaining
        assert query.name == ["John Doe"]
    
    def test_set_name_list(self):
        """Test set_name with list input."""
        query = SearchQuery()
        result = query.set_name(["John Doe", "Jane Smith"])
        
        assert result is query
        assert query.name == ["John Doe", "Jane Smith"]
    
    def test_set_current_title(self):
        """Test set_current_title method."""
        query = SearchQuery()
        result = query.set_current_title("Software Engineer")
        
        assert result is query
        assert query.current_title == ["Software Engineer"]
    
    def test_set_current_employer(self):
        """Test set_current_employer method."""
        query = SearchQuery()
        result = query.set_current_employer("Google")
        
        assert result is query
        assert query.current_employer == ["Google"]
    
    def test_set_location(self):
        """Test set_location method."""
        query = SearchQuery()
        result = query.set_location("San Francisco")
        
        assert result is query
        assert query.location == ["San Francisco"]
    
    def test_set_page(self):
        """Test set_page method."""
        query = SearchQuery()
        result = query.set_page(5)
        
        assert result is query
        assert query.page == 5
    
    def test_set_page_size(self):
        """Test set_page_size method."""
        query = SearchQuery()
        result = query.set_page_size(50)
        
        assert result is query
        assert query.page_size == 50
    
    def test_method_chaining(self):
        """Test method chaining."""
        query = (SearchQuery()
                .set_name("John Doe")
                .set_current_employer("Google")
                .set_page(2)
                .set_page_size(25))
        
        assert query.name == ["John Doe"]
        assert query.current_employer == ["Google"]
        assert query.page == 2
        assert query.page_size == 25


class TestLookupQuery:
    """Test cases for LookupQuery model."""
    
    def test_init_default_values(self):
        """Test default initialization values."""
        query = LookupQuery()
        assert query.id is None
        assert query.linkedin_url is None
        assert query.name is None
        assert query.current_employer is None
        assert query.title is None
        assert query.email is None
        assert query.npi_number is None
    
    def test_to_dict_empty(self):
        """Test to_dict with empty query."""
        query = LookupQuery()
        result = query.to_dict()
        assert result == {}
    
    def test_to_dict_with_values(self):
        """Test to_dict with values."""
        query = LookupQuery()
        query.id = 12345
        query.name = "John Doe"
        query.current_employer = "Google"
        
        result = query.to_dict()
        assert result["id"] == 12345
        assert result["name"] == "John Doe"
        assert result["current_employer"] == "Google"
    
    def test_set_id(self):
        """Test set_id method."""
        query = LookupQuery()
        result = query.set_id(12345)
        
        assert result is query
        assert query.id == 12345
    
    def test_set_linkedin_url(self):
        """Test set_linkedin_url method."""
        query = LookupQuery()
        result = query.set_linkedin_url("https://linkedin.com/in/johndoe")
        
        assert result is query
        assert query.linkedin_url == "https://linkedin.com/in/johndoe"
    
    def test_set_name(self):
        """Test set_name method."""
        query = LookupQuery()
        result = query.set_name("John Doe")
        
        assert result is query
        assert query.name == "John Doe"
    
    def test_set_current_employer(self):
        """Test set_current_employer method."""
        query = LookupQuery()
        result = query.set_current_employer("Google")
        
        assert result is query
        assert query.current_employer == "Google"
    
    def test_set_title(self):
        """Test set_title method."""
        query = LookupQuery()
        result = query.set_title("Software Engineer")
        
        assert result is query
        assert query.title == "Software Engineer"
    
    def test_set_email(self):
        """Test set_email method."""
        query = LookupQuery()
        result = query.set_email("john@google.com")
        
        assert result is query
        assert query.email == "john@google.com"
    
    def test_set_npi_number(self):
        """Test set_npi_number method."""
        query = LookupQuery()
        result = query.set_npi_number(1234567890)
        
        assert result is query
        assert query.npi_number == 1234567890
    
    def test_method_chaining(self):
        """Test method chaining."""
        query = (LookupQuery()
                .set_name("John Doe")
                .set_current_employer("Google")
                .set_title("Software Engineer")
                .set_email("john@google.com"))
        
        assert query.name == "John Doe"
        assert query.current_employer == "Google"
        assert query.title == "Software Engineer"
        assert query.email == "john@google.com"


class TestSearchResponse:
    """Test cases for SearchResponse model."""
    
    def test_init_with_data(self, search_response_data):
        """Test initialization with data."""
        response = SearchResponse(search_response_data)
        
        assert len(response.profiles) == 2
        assert response.pagination["total"] == 100
        assert response.count == 2
        assert response.total == 100
        assert response.current_page == 1
        assert response.next_page == 2
        assert response.has_next_page is True
        assert response.is_empty is False
    
    def test_init_empty(self):
        """Test initialization with empty data."""
        response = SearchResponse({})
        
        assert response.profiles == []
        assert response.pagination == {}
        assert response.count == 0
        assert response.total == 0
        assert response.current_page == 1
        assert response.next_page is None
        assert response.has_next_page is False
        assert response.is_empty is True
    
    def test_get_profiles(self, search_response_data):
        """Test get_profiles method."""
        response = SearchResponse(search_response_data)
        profiles = response.get_profiles()
        
        assert profiles == search_response_data["profiles"]
        assert len(profiles) == 2
    
    def test_get_pagination(self, search_response_data):
        """Test get_pagination method."""
        response = SearchResponse(search_response_data)
        pagination = response.get_pagination()
        
        assert pagination == search_response_data["pagination"]
        assert pagination["total"] == 100


class TestPersonResponse:
    """Test cases for PersonResponse model."""
    
    def test_init_with_data(self, person_response_data):
        """Test initialization with data."""
        response = PersonResponse(person_response_data)
        
        assert response.id == 12345
        assert response.name == "John Doe"
        assert response.current_title == "Software Engineer"
        assert response.current_employer == "Google"
        assert response.status == "complete"
        assert response.is_complete is True
        assert response.is_searching is False
    
    def test_init_empty(self):
        """Test initialization with empty data."""
        response = PersonResponse({})
        
        assert response.id is None
        assert response.name is None
        assert response.current_title is None
        assert response.current_employer is None
        assert response.status is None
        assert response.is_complete is False
        assert response.is_searching is False
    
    def test_status_complete(self):
        """Test status when complete."""
        response = PersonResponse({"status": "complete"})
        assert response.is_complete is True
        assert response.is_searching is False
    
    def test_status_searching(self):
        """Test status when searching."""
        response = PersonResponse({"status": "searching"})
        assert response.is_complete is False
        assert response.is_searching is True
    
    def test_get_emails(self):
        """Test get_emails method."""
        data = {
            "emails": [
                {"email": "john@google.com", "type": "professional"},
                {"email": "johndoe@gmail.com", "type": "personal"}
            ]
        }
        response = PersonResponse(data)
        emails = response.get_emails()
        
        assert len(emails) == 2
        assert emails[0]["email"] == "john@google.com"
        assert emails[1]["email"] == "johndoe@gmail.com"
    
    def test_get_phones(self):
        """Test get_phones method."""
        data = {
            "phones": [
                {"number": "+1-555-123-4567", "type": "mobile"},
                {"number": "+1-555-987-6543", "type": "office"}
            ]
        }
        response = PersonResponse(data)
        phones = response.get_phones()
        
        assert len(phones) == 2
        assert phones[0]["number"] == "+1-555-123-4567"
        assert phones[1]["number"] == "+1-555-987-6543"
    
    def test_get_raw_data(self, person_response_data):
        """Test get_raw_data method."""
        response = PersonResponse(person_response_data)
        raw_data = response.get_raw_data()
        
        assert raw_data == person_response_data


class TestEnrichResponse:
    """Test cases for EnrichResponse model."""
    
    def test_init_with_data(self, enrich_response_data):
        """Test initialization with data."""
        response = EnrichResponse(enrich_response_data)
        
        assert response.person_id == 12345
        assert response.person_name == "John Doe"
        assert response.company_id == 98765
        assert response.company_name == "Google"
        assert response.company_domain == "google.com"
        assert response.company_industry == "Internet"
        assert response.company_employee_count == "100000+"
        assert response.company_location == "Mountain View, CA"
    
    def test_init_empty(self):
        """Test initialization with empty data."""
        response = EnrichResponse({})
        
        assert response.person_id is None
        assert response.person_name is None
        assert response.company_id is None
        assert response.company_name is None
        assert response.company_domain is None
        assert response.company_industry is None
        assert response.company_employee_count is None
        assert response.company_location is None
    
    def test_get_person_data(self, enrich_response_data):
        """Test get_person_data method."""
        response = EnrichResponse(enrich_response_data)
        person_data = response.get_person_data()
        
        assert person_data == enrich_response_data["person"]
    
    def test_get_company_data(self, enrich_response_data):
        """Test get_company_data method."""
        response = EnrichResponse(enrich_response_data)
        company_data = response.get_company_data()
        
        assert company_data == enrich_response_data["company"]
    
    def test_person_emails(self):
        """Test person_emails property."""
        data = {
            "person": {
                "emails": [
                    {"email": "john@google.com", "type": "professional"}
                ]
            }
        }
        response = EnrichResponse(data)
        emails = response.person_emails
        
        assert len(emails) == 1
        assert emails[0]["email"] == "john@google.com"
    
    def test_person_phones(self):
        """Test person_phones property."""
        data = {
            "person": {
                "phones": [
                    {"number": "+1-555-123-4567", "type": "mobile"}
                ]
            }
        }
        response = EnrichResponse(data)
        phones = response.person_phones
        
        assert len(phones) == 1
        assert phones[0]["number"] == "+1-555-123-4567"
