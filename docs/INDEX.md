# RocketReach SDK Documentation Index

Complete documentation for the RocketReach SDK project.

## 📚 Quick Navigation

### Getting Started
- [Main README](../../README.md) - Project overview and quick start
- [API Key Setup](#api-key-setup) - How to get and configure your API key
- [Installation](#installation) - Installation instructions for both languages

### Language-Specific Documentation
- [PHP SDK Documentation](PHP/README.md) - Complete PHP SDK guide
- [Python SDK Documentation](Python/README.md) - Complete Python SDK guide

### API Reference
- [API Reference](API_REFERENCE.md) - Complete API endpoint documentation
- [People Search API](Build%20SDK%20for%20API.md) - People Search endpoint details
- [Person Lookup & Enrich API](RocketReach%20People%20Data%20API%20%E2%80%93%20Person%20Lookup%20&%20Person%20Enrich%20Endpoints.md) - Person Lookup and Enrich endpoints

### Development
- [Development Guide](DEVELOPMENT_GUIDE.md) - Development setup and guidelines
- [Testing Guide](TESTING_GUIDE.md) - Testing strategies and procedures
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to the project
- [Project Plan](PROJECT_PLAN.md) - Complete project development plan

### Project Information
- [Changelog](CHANGELOG.md) - Version history and changes
- [License Information](#license-information) - Licensing details

## 🔑 API Key Setup

### Getting Your API Key

1. Visit the [RocketReach Dashboard](https://rocketreach.co/api)
2. Sign up for an account or log in
3. Navigate to the API section
4. Generate a new API key
5. Copy the API key for use in your application

### Security Best Practices

- **Never commit API keys** to version control
- **Use environment variables** for API key storage
- **Rotate API keys** regularly
- **Monitor API usage** to prevent overuse
- **Use different keys** for development and production

### Environment Variable Setup

#### PHP
```bash
export ROCKETREACH_API_KEY="your-api-key-here"
```

#### Python
```bash
export ROCKETREACH_API_KEY="your-api-key-here"
```

#### Windows
```cmd
set ROCKETREACH_API_KEY=your-api-key-here
```

## 📦 Installation

### PHP SDK

```bash
# Using Composer
composer require actuallyrizzn/rocketreach-sdk-php

# Manual installation
git clone https://github.com/actuallyrizzn/rocketreach-sdk.git
cd rocketreach-sdk/php
composer install
```

### Python SDK

```bash
# Using pip
pip install actuallyrizzn-rocketreach-sdk-python

# From source
git clone https://github.com/actuallyrizzn/rocketreach-sdk.git
cd rocketreach-sdk/python
pip install -e .
```

## 🚀 Quick Start Examples

### PHP Quick Start

```php
<?php
require_once 'vendor/autoload.php';

use RocketReach\SDK\RocketReachClient;

$client = new RocketReachClient('your-api-key');

// Search for people
$results = $client->peopleSearch()
    ->name(['John Doe'])
    ->currentEmployer(['Google'])
    ->search();

echo "Found " . $results->getCount() . " profiles\n";
```

### Python Quick Start

```python
from rocketreach.sdk import RocketReachClient

client = RocketReachClient('your-api-key')

# Search for people
results = (client.people_search()
          .name(['John Doe'])
          .current_employer(['Google'])
          .search())

print(f"Found {results.count} profiles")
```

## 📋 API Endpoints

### People Search
- **Endpoint**: `POST /api/v2/person/search`
- **Purpose**: Search for professional profiles
- **Documentation**: [People Search API](Build%20SDK%20for%20API.md)

### Person Lookup
- **Endpoint**: `GET /api/v2/person/lookup`
- **Purpose**: Get detailed contact information
- **Documentation**: [Person Lookup API](RocketReach%20People%20Data%20API%20%E2%80%93%20Person%20Lookup%20&%20Person%20Enrich%20Endpoints.md)

### Person Enrich
- **Endpoint**: `GET /api/v2/profile-company/lookup`
- **Purpose**: Get person and company information
- **Documentation**: [Person Enrich API](RocketReach%20People%20Data%20API%20%E2%80%93%20Person%20Lookup%20&%20Person%20Enrich%20Endpoints.md)

## 🧪 Testing

### Running Tests

#### PHP
```bash
cd php
./vendor/bin/phpunit
```

#### Python
```bash
cd python
pytest
```

### Test Coverage
- **Unit Tests**: 100% code coverage
- **Integration Tests**: Critical path coverage
- **E2E Tests**: Complete workflow coverage
- **Live Tests**: API compatibility validation

## 🔧 Development

### Prerequisites
- **PHP**: 8.1+ (for PHP development)
- **Python**: 3.8+ (for Python development)
- **Git**: For version control
- **Composer**: For PHP dependencies
- **pip**: For Python dependencies

### Development Setup
1. Fork the repository
2. Clone your fork
3. Set up development environment
4. Create a feature branch
5. Make your changes
6. Run tests
7. Submit a pull request

## 📄 License Information

### Code License
- **License**: GNU Affero General Public License v3.0
- **File**: [LICENSE](../../LICENSE)
- **Description**: Copyleft license requiring source code disclosure

### Documentation License
- **License**: Creative Commons Attribution-ShareAlike 4.0 International
- **File**: [LICENSE-DOCS](../../LICENSE-DOCS)
- **Description**: Share-alike license for documentation

## 🆘 Support

### Getting Help
- **Documentation**: Check the relevant documentation files
- **GitHub Issues**: [Report bugs or request features](https://github.com/actuallyrizzn/rocketreach-sdk/issues)
- **RocketReach Support**: [Official RocketReach support](https://rocketreach.co/support)

### Common Issues
1. **API Key Issues**: Ensure your API key is valid and has proper permissions
2. **Rate Limiting**: The SDK handles rate limiting automatically
3. **Network Issues**: Check your internet connection and firewall settings
4. **Installation Issues**: Check the installation requirements

## 📊 Project Status

- **PHP SDK**: ✅ Production Ready
- **Python SDK**: ✅ Production Ready
- **Documentation**: ✅ Complete
- **Tests**: ✅ 100% Coverage
- **Live API Integration**: ✅ Validated

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code standards and guidelines
- Testing requirements
- Documentation standards
- Pull request process
- Issue reporting

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a complete list of changes and version history.

## 🔗 External Links

- [RocketReach Website](https://rocketreach.co)
- [RocketReach API Documentation](https://rocketreach.co/api)
- [RocketReach Support](https://rocketreach.co/support)
- [GitHub Repository](https://github.com/actuallyrizzn/rocketreach-sdk)

---

**Last Updated**: February 2024  
**Version**: 1.0.0  
**Maintainer**: RocketReach SDK Team
