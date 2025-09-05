"""
API Response Fixtures

Mock API response data for testing.
"""

# Search API Response
SEARCH_RESPONSE = {
    "profiles": [
        {
            "id": 12345,
            "name": "John Doe",
            "current_title": "Software Engineer",
            "current_employer": "Google",
            "linkedin_url": "https://linkedin.com/in/johndoe",
            "location": "San Francisco, CA",
            "emails": [
                {
                    "email": "john@google.com",
                    "type": "professional",
                    "grade": "A"
                }
            ],
            "phones": [
                {
                    "number": "+1-555-123-4567",
                    "type": "mobile"
                }
            ],
            "status": "complete"
        },
        {
            "id": 67890,
            "name": "Jane Smith",
            "current_title": "Product Manager",
            "current_employer": "Microsoft",
            "linkedin_url": "https://linkedin.com/in/janesmith",
            "location": "Seattle, WA",
            "emails": [
                {
                    "email": "jane@microsoft.com",
                    "type": "professional",
                    "grade": "A"
                }
            ],
            "phones": [
                {
                    "number": "+1-555-987-6543",
                    "type": "mobile"
                }
            ],
            "status": "complete"
        }
    ],
    "pagination": {
        "start": 1,
        "next": 2,
        "total": 100
    }
}

# Person Lookup Response
PERSON_RESPONSE = {
    "id": 12345,
    "name": "John Doe",
    "current_title": "Software Engineer",
    "current_employer": "Google",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "location": "San Francisco, CA",
    "emails": [
        {
            "email": "john@google.com",
            "type": "professional",
            "grade": "A"
        }
    ],
    "phones": [
        {
            "number": "+1-555-123-4567",
            "type": "mobile"
        }
    ],
    "status": "complete"
}

# Person Enrich Response
ENRICH_RESPONSE = {
    "person": {
        "id": 12345,
        "name": "John Doe",
        "emails": [
            {
                "email": "john@google.com",
                "type": "professional",
                "grade": "A"
            }
        ],
        "phones": [
            {
                "number": "+1-555-123-4567",
                "type": "mobile"
            }
        ]
    },
    "company": {
        "id": 98765,
        "name": "Google",
        "domain": "google.com",
        "industry": "Internet",
        "employee_count": "100000+",
        "location": "Mountain View, CA"
    }
}

# Account Info Response
ACCOUNT_RESPONSE = {
    "credits": 1000,
    "used_credits": 150,
    "remaining_credits": 850,
    "plan": "professional",
    "expires_at": "2024-12-31T23:59:59Z"
}

# Health Status Response
HEALTH_RESPONSE = {
    "status": "healthy",
    "timestamp": "2024-01-01T00:00:00Z",
    "version": "v2.0.0"
}

# Error Responses
ERROR_RESPONSES = {
    "invalid_api_key": {
        "error": "Invalid API key",
        "code": 401,
        "message": "The provided API key is invalid or expired"
    },
    "rate_limit": {
        "error": "Rate limit exceeded",
        "code": 429,
        "message": "Too many requests",
        "retry_after": 60
    },
    "not_found": {
        "error": "Not found",
        "code": 404,
        "message": "The requested resource was not found"
    },
    "server_error": {
        "error": "Internal server error",
        "code": 500,
        "message": "An internal server error occurred"
    }
}
