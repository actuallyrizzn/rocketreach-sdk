# RocketReach SDK

Official SDKs for the RocketReach API in PHP and Python.

## 🚀 Features

- **Complete API Coverage**: People Search, Person Lookup, and Person Enrich endpoints
- **Production Ready**: Comprehensive error handling, rate limiting, and retry logic
- **100% Test Coverage**: Unit, Integration, E2E, and Live tests
- **Fluent API**: Method chaining for intuitive usage
- **Type Safety**: Full type hints and validation
- **Documentation**: Complete examples and API documentation

## 📦 Installation

### PHP SDK

```bash
composer require actuallyrizzn/rocketreach-sdk-php
```

### Python SDK

```bash
pip install actuallyrizzn-rocketreach-sdk-python
```

## 🔧 Quick Start

### PHP

```php
<?php
require_once 'vendor/autoload.php';

use RocketReach\SDK\RocketReachClient;

$client = new RocketReachClient('your-api-key');

// People Search
$results = $client->peopleSearch()
    ->name(['John Doe'])
    ->currentEmployer(['Google'])
    ->page(1)
    ->pageSize(10)
    ->search();

echo "Found " . $results->getCount() . " profiles\n";

// Person Lookup
$person = $client->personLookup()
    ->name('John Doe')
    ->currentEmployer('Google')
    ->lookup();

echo "Person: " . $person->getName() . "\n";

// Person Enrich
$enriched = $client->personEnrich()
    ->name('John Doe')
    ->currentEmployer('Google')
    ->enrich();

echo "Company: " . $enriched->getCompanyName() . "\n";
```

### Python

```python
from rocketreach.sdk import RocketReachClient

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
         .name('John Doe')
         .current_employer('Google')
         .lookup())

print(f"Person: {person.name}")

# Person Enrich
enriched = (client.person_enrich()
           .name('John Doe')
           .current_employer('Google')
           .enrich())

print(f"Company: {enriched.company_name}")
```

## 📚 Documentation

- [PHP SDK Documentation](php/README.md)
- [Python SDK Documentation](python/README.md)
- [API Documentation](docs/)

## 🧪 Testing

Both SDKs include comprehensive test suites:

### PHP
```bash
cd php
composer install
./vendor/bin/phpunit
```

### Python
```bash
cd python
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
pytest
```

## 🔑 API Key

Get your API key from the [RocketReach Dashboard](https://rocketreach.co/api).

## 📋 Requirements

- **PHP**: 8.1+
- **Python**: 3.8+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

- [Documentation](docs/)
- [Issues](https://github.com/actuallyrizzn/rocketreach-sdk/issues)
- [RocketReach Support](https://rocketreach.co/support)

## 🏗️ Project Structure

```
rocketreach-sdk/
├── php/                    # PHP SDK
│   ├── src/               # Source code
│   ├── tests/             # Test suite
│   ├── examples/          # Usage examples
│   └── README.md          # PHP-specific docs
├── python/                # Python SDK
│   ├── src/               # Source code
│   ├── tests/             # Test suite
│   ├── examples/          # Usage examples
│   └── README.md          # Python-specific docs
├── docs/                  # API documentation
└── README.md              # This file
```

## ✅ Status

- ✅ PHP SDK: Production Ready
- ✅ Python SDK: Production Ready
- ✅ Live API Testing: Complete
- ✅ Documentation: Complete
- ✅ Examples: Complete
