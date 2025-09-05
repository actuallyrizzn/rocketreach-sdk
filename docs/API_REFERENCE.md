# RocketReach API Reference

Complete reference for the RocketReach People Search API.

## 🔑 Authentication

All API requests require authentication using your API key.

```http
Api-Key: YOUR_API_KEY
Content-Type: application/json
```

Get your API key from the [RocketReach Dashboard](https://rocketreach.co/api).

## 🌐 Base URL

```
https://api.rocketreach.co/api/v2
```

## 📋 Endpoints

### People Search

Search for professional profiles by various criteria.

**Endpoint**: `POST /person/search`

#### Request Body

```json
{
  "query": {
    "name": ["John Doe"],
    "current_employer": ["Google"],
    "current_title": ["Software Engineer"],
    "location": ["San Francisco, CA"],
    "linkedin_url": ["https://www.linkedin.com/in/johndoe"],
    "contact_method": ["email", "phone"],
    "industry": ["Technology"],
    "company_size": ["1000+"],
    "company_funding": ["1000000+"],
    "company_revenue": ["100M+"],
    "seniority": ["Director", "Manager"],
    "skills": ["Python", "JavaScript"],
    "education": ["Stanford University"]
  },
  "page": 1,
  "page_size": 10,
  "order_by": "relevance"
}
```

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | array | No | Full name(s) to match |
| `current_employer` | array | No | Current company name(s) |
| `current_title` | array | No | Current job title(s) |
| `current_employer_domain` | array | No | Employer website domain(s) |
| `location` | array | No | Location keyword(s) |
| `linkedin_url` | array | No | LinkedIn profile URL(s) |
| `contact_method` | array | No | Filter by contact availability |
| `industry` | array | No | Industry sector(s) |
| `company_size` | array | No | Company size (employees) |
| `company_funding` | array | No | Company funding raised |
| `company_revenue` | array | No | Company annual revenue |
| `seniority` | array | No | Seniority level(s) |
| `skills` | array | No | Skills or keywords |
| `education` | array | No | Education institution(s) |

#### Pagination Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | integer | 1 | Page number (1-based) |
| `page_size` | integer | 10 | Results per page (max 100) |
| `order_by` | string | "relevance" | Sort order ("relevance" or "popularity") |

#### Response

```json
{
  "profiles": [
    {
      "id": 12345,
      "name": "John Doe",
      "current_title": "Software Engineer",
      "current_employer": "Google",
      "linkedin_url": "https://www.linkedin.com/in/johndoe",
      "location": "San Francisco, CA"
    }
  ],
  "pagination": {
    "start": 1,
    "next": 2,
    "total": 100
  }
}
```

### Person Lookup

Retrieve detailed contact information for a specific person.

**Endpoint**: `GET /person/lookup`

#### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | integer | No | RocketReach profile ID |
| `linkedin_url` | string | No | LinkedIn profile URL |
| `name` | string | No† | Full name (requires current_employer) |
| `current_employer` | string | No† | Company name (required with name) |
| `title` | string | No | Job title |
| `email` | string | No | Email address |
| `npi_number` | integer | No | NPI number (healthcare) |

† At least one identifier must be provided.

#### Response

```json
{
  "id": 12345,
  "status": "complete",
  "name": "John Doe",
  "current_title": "Software Engineer",
  "current_employer": "Google",
  "linkedin_url": "https://www.linkedin.com/in/johndoe",
  "emails": [
    {
      "email": "john@google.com",
      "type": "professional",
      "grade": "A",
      "last_validation_check": "2024-02-01"
    }
  ],
  "phones": [
    {
      "number": "+1-555-123-4567",
      "type": "mobile"
    }
  ]
}
```

### Person Enrich

Get both person and company information in a single call.

**Endpoint**: `GET /profile-company/lookup`

#### Query Parameters

Same as Person Lookup.

#### Response

```json
{
  "id": 12345,
  "name": "John Doe",
  "current_title": "Software Engineer",
  "current_employer": "Google",
  "current_employer_id": 98765,
  "current_employer_domain": "google.com",
  "current_employer_website": "https://www.google.com",
  "current_employer_linkedin_url": "https://www.linkedin.com/company/google",
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
}
```

## 🚨 Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created (People Search) |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid API key |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

### Error Response Format

```json
{
  "error": "Invalid API key",
  "message": "The provided API key is invalid or expired",
  "status": 401
}
```

## 🔄 Rate Limiting

The API implements rate limiting based on your plan. When rate limited:

- HTTP status: `429`
- Header: `Retry-After: 60` (seconds)
- Implement exponential backoff for retries

## 📊 Response Status

### People Search
- Always returns `201 Created` on success
- Includes pagination information
- No contact details in search results

### Person Lookup/Enrich
- Returns `200 OK` on success
- `status` field indicates completion:
  - `"complete"` - Data is ready
  - `"searching"` - Still processing (check status later)

## 🔍 Advanced Features

### Exclusion Syntax
Use `-` prefix to exclude terms:

```json
{
  "query": {
    "current_title": ["Software Engineer", "-Senior"]
  }
}
```

### Location Radius
Specify radius for location searches:

```json
{
  "query": {
    "location": ["\"San Francisco\"::~50mi"]
  }
}
```

### Exact Matching
Use quotes for exact matches:

```json
{
  "query": {
    "name": ["\"John Doe\""]
  }
}
```

## 📝 Best Practices

1. **Use appropriate page sizes** (10-50 for most use cases)
2. **Implement retry logic** with exponential backoff
3. **Cache results** when appropriate
4. **Handle rate limits** gracefully
5. **Validate input** before making requests
6. **Use specific filters** to improve relevance
7. **Monitor API usage** to stay within limits

## 🆘 Support

- **Documentation**: [RocketReach Knowledge Base](https://knowledgebase.rocketreach.co)
- **Support**: [RocketReach Support](https://rocketreach.co/support)
- **API Status**: [RocketReach Status Page](https://status.rocketreach.co)
