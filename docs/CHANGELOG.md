# Changelog

All notable changes to the RocketReach SDK project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial release of RocketReach SDK for PHP and Python
- Complete API integration for People Search, Person Lookup, and Person Enrich endpoints
- Comprehensive test coverage (Unit, Integration, E2E, Live tests)
- Fluent API design with method chaining
- Rate limiting and retry logic with exponential backoff
- Custom exception handling for API errors
- Complete documentation and examples
- Support for all RocketReach API parameters and filters
- Response models with proper data validation
- HTTP client with proper authentication and error handling

### Changed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Fixed
- N/A

### Security
- N/A

## [1.0.0] - 2024-02-01

### Added
- **PHP SDK**:
  - Complete RocketReach API client implementation
  - People Search endpoint with full parameter support
  - Person Lookup endpoint with multiple identifier support
  - Person Enrich endpoint with company information
  - HTTP client with Guzzle HTTP
  - Custom exception classes for API errors
  - Response models with data validation
  - Composer package configuration
  - PHPUnit test suite with 100% coverage
  - PSR-12 coding standards compliance
  - PHPStan static analysis integration

- **Python SDK**:
  - Complete RocketReach API client implementation
  - People Search endpoint with full parameter support
  - Person Lookup endpoint with multiple identifier support
  - Person Enrich endpoint with company information
  - HTTP client with requests library
  - Custom exception classes for API errors
  - Response models with data validation
  - setuptools package configuration
  - pytest test suite with 100% coverage
  - PEP 8 coding standards compliance
  - MyPy type checking integration

- **Documentation**:
  - Complete API reference documentation
  - Development guide with setup instructions
  - Testing guide with comprehensive examples
  - Contributing guidelines
  - Installation and usage examples
  - Code documentation with docstrings

- **Testing**:
  - Unit tests for all components
  - Integration tests for HTTP client
  - End-to-end tests for complete workflows
  - Live API tests for real API validation
  - Test fixtures with realistic data
  - Coverage reporting and CI integration

- **Project Structure**:
  - Organized codebase with clear separation
  - Language-specific directories (php/, python/)
  - Comprehensive documentation (docs/)
  - Example usage files
  - Configuration files for tools and CI

### Technical Details

#### API Integration
- **People Search**: `POST /api/v2/person/search`
- **Person Lookup**: `GET /api/v2/person/lookup`
- **Person Enrich**: `GET /api/v2/profile-company/lookup`
- **Authentication**: `Api-Key` header
- **Rate Limiting**: Exponential backoff with retry logic
- **Error Handling**: Custom exceptions for different error types

#### PHP SDK Features
- **PHP Version**: 8.1+
- **Dependencies**: Guzzle HTTP, PHPUnit
- **Autoloading**: PSR-4 compliant
- **Namespace**: `RocketReach\SDK`
- **Coding Standards**: PSR-12
- **Static Analysis**: PHPStan level 8

#### Python SDK Features
- **Python Version**: 3.8+
- **Dependencies**: requests, pytest
- **Package**: setuptools with wheel support
- **Namespace**: `rocketreach.sdk`
- **Coding Standards**: PEP 8
- **Type Checking**: MyPy with strict mode

#### Testing Coverage
- **Unit Tests**: 100% code coverage
- **Integration Tests**: HTTP client and API integration
- **E2E Tests**: Complete workflow testing
- **Live Tests**: Real API validation (conservative usage)
- **Test Frameworks**: PHPUnit (PHP), pytest (Python)

#### Documentation
- **API Reference**: Complete endpoint documentation
- **Development Guide**: Setup and contribution instructions
- **Testing Guide**: Comprehensive testing strategies
- **Contributing Guide**: Contribution guidelines and standards
- **Examples**: Working code examples for all features

### Performance
- **HTTP Client**: Optimized for concurrent requests
- **Rate Limiting**: Intelligent retry logic
- **Memory Usage**: Efficient data structures
- **Response Parsing**: Fast JSON processing
- **Error Handling**: Minimal overhead

### Security
- **API Key**: Secure storage and transmission
- **HTTPS**: All API calls use secure connections
- **Input Validation**: Proper parameter validation
- **Error Handling**: No sensitive data in error messages
- **Dependencies**: Regular security updates

### Compatibility
- **PHP**: 8.1, 8.2, 8.3
- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Operating Systems**: Windows, macOS, Linux
- **HTTP Libraries**: Guzzle (PHP), requests (Python)

### Dependencies

#### PHP Dependencies
- **guzzlehttp/guzzle**: ^7.0 (HTTP client)
- **phpunit/phpunit**: ^10.0 (Testing)
- **phpstan/phpstan**: ^1.0 (Static analysis)

#### Python Dependencies
- **requests**: ^2.28.0 (HTTP client)
- **pytest**: ^7.0.0 (Testing)
- **pytest-cov**: ^4.0.0 (Coverage)
- **mypy**: ^1.0.0 (Type checking)

### Installation

#### PHP
```bash
composer require actuallyrizzn/rocketreach-sdk-php
```

#### Python
```bash
pip install actuallyrizzn-rocketreach-sdk-python
```

### Usage Examples

#### PHP
```php
use RocketReach\SDK\RocketReachClient;

$client = new RocketReachClient('your-api-key');

// People Search
$results = $client->peopleSearch()
    ->name(['John Doe'])
    ->currentEmployer(['Google'])
    ->search();

// Person Lookup
$person = $client->personLookup()
    ->id(12345)
    ->lookup();

// Person Enrich
$enriched = $client->personEnrich()
    ->name('John Doe')
    ->currentEmployer('Google')
    ->enrich();
```

#### Python
```python
from rocketreach.sdk import RocketReachClient

client = RocketReachClient('your-api-key')

# People Search
results = (client.people_search()
          .name(['John Doe'])
          .current_employer(['Google'])
          .search())

# Person Lookup
person = (client.person_lookup()
         .id(12345)
         .lookup())

# Person Enrich
enriched = (client.person_enrich()
           .name('John Doe')
           .current_employer('Google')
           .enrich())
```

### Breaking Changes
- N/A (Initial release)

### Migration Guide
- N/A (Initial release)

### Known Issues
- None at release

### Contributors
- Initial development and implementation
- Complete test suite development
- Documentation creation
- API integration and validation

### Acknowledgments
- RocketReach team for API access and support
- Open source community for tools and libraries
- Contributors for feedback and testing

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0.0 | 2024-02-01 | Initial release with complete PHP and Python SDKs |

## Support

For support and questions:
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/actuallyrizzn/rocketreach-sdk/issues)
- **RocketReach Support**: [RocketReach Support](https://rocketreach.co/support)

## License

- **Code**: GNU Affero General Public License v3.0
- **Documentation**: Creative Commons Attribution-ShareAlike 4.0 International
