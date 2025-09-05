"""
Test Data Fixtures

Common test data for various test scenarios.
"""

# Search Query Test Data
SEARCH_QUERY_DATA = {
    "basic": {
        "name": ["John Doe"],
        "current_employer": ["Google"],
        "page": 1,
        "page_size": 10
    },
    "complex": {
        "name": ["John Doe", "Jane Smith"],
        "current_title": ["Software Engineer", "Product Manager"],
        "current_employer": ["Google", "Microsoft"],
        "location": ["San Francisco", "Seattle"],
        "industry": ["Technology"],
        "company_size": ["1000+"],
        "seniority": ["Senior"],
        "skills": ["Python", "JavaScript"],
        "education": ["Stanford", "MIT"],
        "page": 2,
        "page_size": 25,
        "order_by": "relevance"
    },
    "minimal": {
        "name": ["John Doe"]
    },
    "empty": {}
}

# Lookup Query Test Data
LOOKUP_QUERY_DATA = {
    "by_id": {
        "id": 12345
    },
    "by_linkedin": {
        "linkedin_url": "https://linkedin.com/in/johndoe"
    },
    "by_name_employer": {
        "name": "John Doe",
        "current_employer": "Google"
    },
    "by_email": {
        "email": "john@google.com"
    },
    "by_npi": {
        "npi_number": 1234567890
    },
    "complex": {
        "name": "John Doe",
        "current_employer": "Google",
        "title": "Software Engineer",
        "email": "john@google.com"
    }
}

# Edge Case Data
EDGE_CASE_DATA = {
    "empty_search_response": {
        "profiles": [],
        "pagination": {
            "start": 1,
            "next": None,
            "total": 0
        }
    },
    "empty_person_response": {},
    "empty_enrich_response": {
        "person": {},
        "company": {}
    },
    "partial_data": {
        "id": 12345,
        "name": "John Doe"
    },
    "missing_pagination": {
        "profiles": [{"id": 1, "name": "John Doe"}]
    }
}

# Error Test Data
ERROR_TEST_DATA = {
    "network_timeout": "Request timeout",
    "connection_error": "Connection error",
    "invalid_json": "Invalid JSON response",
    "empty_response": "",
    "malformed_response": "Not a valid JSON response"
}

# API Key Test Data
API_KEY_TEST_DATA = {
    "valid": "***REMOVED***",
    "invalid": "invalid-key",
    "empty": "",
    "none": None,
    "whitespace": "   ",
    "short": "abc",
    "long": "a" * 1000
}

# URL Test Data
URL_TEST_DATA = {
    "production": "https://api.rocketreach.co/api/v2",
    "staging": "https://staging-api.rocketreach.co/api/v2",
    "custom": "https://custom-api.example.com/v2",
    "invalid": "not-a-url",
    "http": "http://api.rocketreach.co/api/v2"
}
