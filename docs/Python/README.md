# RocketReach Python SDK

Official Python SDK for the RocketReach People Search API.

## 🚀 Features

- **Complete API Coverage**: People Search, Person Lookup, and Person Enrich endpoints
- **Fluent API**: Method chaining for intuitive usage
- **Type Safety**: Full type hints and validation
- **Error Handling**: Custom exceptions for different error types
- **Rate Limiting**: Built-in retry logic with exponential backoff
- **PEP 8 Compliant**: Follows Python coding standards
- **100% Test Coverage**: Comprehensive test suite

## 📦 Installation

### pip

```bash
pip install actuallyrizzn-rocketreach-sdk-python
```

### From Source

```bash
git clone https://github.com/actuallyrizzn/rocketreach-sdk.git
cd rocketreach-sdk/python
pip install -e .
```

### Development Installation

```bash
git clone https://github.com/actuallyrizzn/rocketreach-sdk.git
cd rocketreach-sdk/python
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
```

## 🔧 Requirements

- **Python**: 3.8 or higher
- **Dependencies**: requests, typing-extensions

## 🚀 Quick Start

### Basic Usage

```python
from rocketreach.sdk import RocketReachClient

# Initialize the client
client = RocketReachClient('your-api-key')

# People Search
results = (client.people_search()
          .name(['John Doe'])
          .current_employer(['Google'])
          .page(1)
          .page_size(10)
          .search())

print(f"Found {results.count} profiles")

# Person Lookup
person = (client.person_lookup()
         .id(12345)
         .lookup())

print(f"Person: {person.name}")

# Person Enrich
enriched = (client.person_enrich()
           .name('John Doe')
           .current_employer('Google')
           .enrich())

print(f"Company: {enriched.company_name}")
```

### Advanced Usage

```python
from rocketreach.sdk import RocketReachClient
from rocketreach.sdk.exceptions import ApiException

try:
    client = RocketReachClient('your-api-key')
    
    # Complex search with multiple filters
    results = (client.people_search()
              .name(['John Doe', 'Jane Smith'])
              .current_employer(['Google', 'Microsoft'])
              .current_title(['Software Engineer', 'Senior Developer'])
              .location(['San Francisco', 'Seattle'])
              .industry(['Technology'])
              .company_size(['1000+'])
              .seniority(['Director', 'Manager'])
              .skills(['Python', 'JavaScript', 'PHP'])
              .page(1)
              .page_size(50)
              .order_by('relevance')
              .search())
    
    for profile in results.profiles:
        print(f"Name: {profile['name']}")
        print(f"Title: {profile['current_title']}")
        print(f"Company: {profile['current_employer']}")
        print(f"LinkedIn: {profile['linkedin_url']}")
        print()
        
except ApiException as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## 📚 API Reference

### RocketReachClient

Main client class for interacting with the RocketReach API.

```python
client = RocketReachClient(api_key: str, base_url: Optional[str] = None)
```

#### Methods

- `people_search()`: Returns a PeopleSearch endpoint instance
- `person_lookup()`: Returns a PersonLookup endpoint instance
- `person_enrich()`: Returns a PersonEnrich endpoint instance

### People Search

Search for professional profiles by various criteria.

```python
results = (client.people_search()
          .name(['John Doe'])                    # Full name(s)
          .current_employer(['Google'])           # Current company name(s)
          .current_title(['Software Engineer'])   # Current job title(s)
          .current_employer_domain(['google.com']) # Employer website domain(s)
          .location(['San Francisco, CA'])        # Location keyword(s)
          .linkedin_url(['https://linkedin.com/in/johndoe']) # LinkedIn URL(s)
          .contact_method(['email', 'phone'])     # Contact availability
          .industry(['Technology'])               # Industry sector(s)
          .company_size(['1000+'])               # Company size (employees)
          .company_funding(['1000000+'])         # Company funding raised
          .company_revenue(['100M+'])            # Company annual revenue
          .seniority(['Director', 'Manager'])    # Seniority level(s)
          .skills(['Python', 'JavaScript'])      # Skills or keywords
          .education(['Stanford University'])    # Education institution(s)
          .page(1)                               # Page number (1-based)
          .page_size(10)                         # Results per page (max 100)
          .order_by('relevance')                 # Sort order
          .search())                             # Execute search
```

#### Response

```python
results.count          # Total number of results
results.profiles       # List of profile data
results.pagination     # Pagination information
```

### Person Lookup

Retrieve detailed contact information for a specific person.

```python
person = (client.person_lookup()
         .id(12345)                           # RocketReach profile ID
         .linkedin_url('https://linkedin.com/in/johndoe') # LinkedIn URL
         .name('John Doe')                    # Full name (requires current_employer)
         .current_employer('Google')          # Company name (required with name)
         .title('Software Engineer')          # Job title
         .email('john@google.com')            # Email address
         .npi_number(1234567890)              # NPI number (healthcare)
         .lookup())                           # Execute lookup
```

#### Response

```python
person.id               # Profile ID
person.name             # Full name
person.current_title    # Current job title
person.current_employer # Current company
person.linkedin_url     # LinkedIn profile URL
person.emails           # List of email addresses
person.phones           # List of phone numbers
person.status           # Processing status
```

### Person Enrich

Get both person and company information in a single call.

```python
enriched = (client.person_enrich()
           .id(12345)                           # RocketReach profile ID
           .linkedin_url('https://linkedin.com/in/johndoe') # LinkedIn URL
           .name('John Doe')                    # Full name (requires current_employer)
           .current_employer('Google')          # Company name (required with name)
           .title('Software Engineer')          # Job title
           .email('john@google.com')            # Email address
           .npi_number(1234567890)              # NPI number (healthcare)
           .enrich())                           # Execute enrichment
```

#### Response

```python
enriched.person         # Person information
enriched.company        # Company information
enriched.person_name    # Person's name
enriched.company_name   # Company name
enriched.emails         # Email addresses
enriched.phones         # Phone numbers
```

## 🚨 Error Handling

The SDK provides custom exceptions for different error types:

```python
from rocketreach.sdk.exceptions import (
    ApiException,
    InvalidApiKeyException,
    RateLimitException,
    NetworkException
)

try:
    results = client.people_search().search()
except InvalidApiKeyException as e:
    print(f"Invalid API key: {e}")
except RateLimitException as e:
    print(f"Rate limit exceeded: {e}")
except NetworkException as e:
    print(f"Network error: {e}")
except ApiException as e:
    print(f"API error: {e}")
```

### Exception Types

- **`ApiException`**: Base exception for API errors
- **`InvalidApiKeyException`**: Invalid or expired API key
- **`RateLimitException`**: Rate limit exceeded
- **`NetworkException`**: Network connectivity issues

## 🔄 Rate Limiting

The SDK automatically handles rate limiting with exponential backoff:

```python
client = RocketReachClient('your-api-key', {
    'retry_attempts': 3,        # Number of retry attempts
    'retry_delay': 1000,        # Initial delay in milliseconds
    'max_delay': 30000,         # Maximum delay in milliseconds
    'timeout': 30               # Request timeout in seconds
})
```

## 🧪 Testing

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest

# Run with coverage
pytest --cov=src/ --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
pytest tests/live/
```

### Test Configuration

The SDK includes comprehensive tests:

- **Unit Tests**: Test individual components
- **Integration Tests**: Test HTTP client integration
- **E2E Tests**: Test complete workflows
- **Live Tests**: Test against real API (use sparingly)

### Writing Tests

```python
import pytest
from rocketreach.sdk import RocketReachClient

def test_your_feature():
    client = RocketReachClient('test-key')
    
    # Your test code here
    assert True
```

## 📝 Configuration

### Environment Variables

```bash
# .env
ROCKETREACH_API_KEY=your-api-key-here
ROCKETREACH_BASE_URL=https://api.rocketreach.co/api/v2
ROCKETREACH_TIMEOUT=30
ROCKETREACH_RETRY_ATTEMPTS=3
```

### Configuration Options

```python
client = RocketReachClient('your-api-key', {
    'base_url': 'https://api.rocketreach.co/api/v2',
    'timeout': 30,
    'retry_attempts': 3,
    'retry_delay': 1000,
    'max_delay': 30000,
    'user_agent': 'RocketReach-Python-SDK/1.0.0'
})
```

## 🔧 Development

### Code Standards

- **PEP 8**: Follows PEP 8 coding standards
- **Type Hints**: Uses type hints for all functions
- **Docstrings**: Includes comprehensive docstrings
- **Static Analysis**: MyPy type checking

### Static Analysis

```bash
# Run MyPy
mypy src/

# Run with strict mode
mypy src/ --strict
```

### Code Style

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
```

## 📚 Examples

Check the `examples/` directory for complete working examples:

- **`basic_usage.py`**: Basic API usage examples
- **`advanced_search.py`**: Complex search scenarios
- **`error_handling.py`**: Error handling examples
- **`batch_processing.py`**: Batch processing examples

## 🆘 Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure your API key is valid and has proper permissions
2. **Rate Limiting**: The SDK handles rate limiting automatically
3. **Network Issues**: Check your internet connection and firewall settings
4. **Memory Issues**: Consider using generators for large datasets

### Debug Mode

```python
client = RocketReachClient('your-api-key', {
    'debug': True,      # Enable debug logging
    'log_level': 'debug'
})
```

### Getting Help

- **Documentation**: [Complete API Reference](../API_REFERENCE.md)
- **Issues**: [GitHub Issues](https://github.com/actuallyrizzn/rocketreach-sdk/issues)
- **RocketReach Support**: [RocketReach Support](https://rocketreach.co/support)

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](../../LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](../CONTRIBUTING.md) for details.

## 📋 Changelog

See [CHANGELOG.md](../CHANGELOG.md) for a list of changes and version history.
