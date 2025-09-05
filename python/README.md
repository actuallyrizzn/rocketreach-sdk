# RocketReach Python SDK

A Python client library for the RocketReach People Search API.

## Features

- **People Search**: Search for people with advanced filtering options
- **Person Lookup**: Look up specific people by various identifiers
- **Person Enrichment**: Enrich person data with contact and company information
- **Fluent API**: Easy-to-use method chaining interface
- **Error Handling**: Comprehensive exception handling with retry logic
- **Type Hints**: Full type annotation support
- **Async Support**: Asynchronous operations support

## Installation

### Virtual Environment Setup (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# Or use the provided script:
.\activate_env.ps1

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### From PyPI (when published)
```bash
pip install rocketreach-sdk
```

### From Source
```bash
git clone https://github.com/rocketreach/sdk-python.git
cd sdk-python
pip install -e .
```

## Quick Start

```python
from rocketreach import RocketReachClient

# Initialize the client
client = RocketReachClient("your-api-key-here")

# Search for people
results = (client.people_search()
           .name(["John Doe"])
           .current_employer(["Google"])
           .location(["San Francisco"])
           .search())

print(f"Found {results.count} profiles")

# Look up a specific person
person = (client.person_lookup()
          .name("John Doe")
          .current_employer("Google")
          .lookup())

print(f"Person: {person.name} at {person.current_employer}")

# Enrich person data
enriched = (client.person_enrich()
            .name("John Doe")
            .current_employer("Google")
            .enrich())

print(f"Company: {enriched.company_name} ({enriched.company_domain})")
```

## API Reference

### RocketReachClient

The main client class for interacting with the RocketReach API.

```python
client = RocketReachClient(
    api_key="your-api-key",
    base_url="https://api.rocketreach.co/api/v2",  # Optional
    timeout=30,  # Optional
    retry_attempts=3,  # Optional
    retry_delay=1.0,  # Optional
)
```

### People Search

Search for people with various filters:

```python
results = (client.people_search()
           .name(["John Doe", "Jane Smith"])
           .current_title(["Software Engineer"])
           .current_employer(["Google", "Microsoft"])
           .location(["San Francisco", "New York"])
           .industry(["Technology"])
           .company_size(["1000+"])
           .page(1)
           .page_size(10)
           .search())
```

### Person Lookup

Look up a specific person:

```python
person = (client.person_lookup()
          .id(12345)  # or .linkedin_url("...") or .name("...")
          .lookup())
```

### Person Enrichment

Enrich person data with additional information:

```python
enriched = (client.person_enrich()
            .name("John Doe")
            .current_employer("Google")
            .enrich())
```

## Response Models

### SearchResponse

```python
response = client.people_search().name(["John Doe"]).search()

print(f"Count: {response.count}")
print(f"Total: {response.total}")
print(f"Current Page: {response.current_page}")
print(f"Has Next Page: {response.has_next_page}")

for profile in response.get_profiles():
    print(profile)
```

### PersonResponse

```python
person = client.person_lookup().name("John Doe").lookup()

print(f"ID: {person.id}")
print(f"Name: {person.name}")
print(f"Title: {person.current_title}")
print(f"Employer: {person.current_employer}")
print(f"Status: {person.status}")
print(f"Is Complete: {person.is_complete}")

emails = person.get_emails()
phones = person.get_phones()
```

### EnrichResponse

```python
enriched = client.person_enrich().name("John Doe").enrich()

print(f"Person: {enriched.person_name}")
print(f"Company: {enriched.company_name}")
print(f"Domain: {enriched.company_domain}")
print(f"Industry: {enriched.company_industry}")
```

## Error Handling

The SDK provides comprehensive error handling:

```python
from rocketreach import RocketReachClient, ApiException, RateLimitException, NetworkException

try:
    client = RocketReachClient("invalid-key")
    results = client.people_search().name(["John Doe"]).search()
except InvalidApiKeyException as e:
    print(f"Invalid API key: {e}")
except RateLimitException as e:
    print(f"Rate limit exceeded. Retry after: {e.retry_after} seconds")
except NetworkException as e:
    print(f"Network error: {e}")
except ApiException as e:
    print(f"API error: {e}")
```

## Configuration

### Environment Variables

You can set your API key as an environment variable:

```bash
export ROCKETREACH_API_KEY="your-api-key-here"
```

Then initialize the client without specifying the API key:

```python
import os
from rocketreach import RocketReachClient

client = RocketReachClient(os.getenv("ROCKETREACH_API_KEY"))
```

### Custom Configuration

```python
client = RocketReachClient(
    api_key="your-api-key",
    base_url="https://api.rocketreach.co/api/v2",
    timeout=60,  # 60 seconds
    retry_attempts=5,  # 5 retry attempts
    retry_delay=2.0,  # 2 seconds between retries
)
```

## Development

### Setup Development Environment

```bash
# Create and activate virtual environment
python -m venv venv
.\activate_env.ps1  # Windows PowerShell
# or source venv/bin/activate  # macOS/Linux

# Install development dependencies
pip install -r requirements-dev.txt

# Install the package in development mode
pip install -e .
```

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --category unit
python run_tests.py --category integration
python run_tests.py --category e2e
python run_tests.py --category live

# Run tests in loop until all pass
python run_tests.py --loop

# Run with pytest directly
pytest
pytest --cov=rocketreach
pytest tests/unit/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
flake8 src/ tests/

# Security check
bandit -r src/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [https://docs.rocketreach.co/python-sdk](https://docs.rocketreach.co/python-sdk)
- **Issues**: [https://github.com/rocketreach/sdk-python/issues](https://github.com/rocketreach/sdk-python/issues)
- **Email**: [sdk@rocketreach.co](mailto:sdk@rocketreach.co)