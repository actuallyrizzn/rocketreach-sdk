# RocketReach PHP SDK

Official PHP SDK for the RocketReach People Search API.

## 🚀 Features

- **Complete API Coverage**: People Search, Person Lookup, and Person Enrich endpoints
- **Fluent API**: Method chaining for intuitive usage
- **Type Safety**: Full type hints and validation
- **Error Handling**: Custom exceptions for different error types
- **Rate Limiting**: Built-in retry logic with exponential backoff
- **PSR-12 Compliant**: Follows PHP coding standards
- **100% Test Coverage**: Comprehensive test suite

## 📦 Installation

### Composer

```bash
composer require actuallyrizzn/rocketreach-sdk-php
```

### Manual Installation

1. Download the SDK files
2. Include the autoloader:
   ```php
   require_once 'path/to/rocketreach-sdk-php/vendor/autoload.php';
   ```

## 🔧 Requirements

- **PHP**: 8.1 or higher
- **Extensions**: mbstring, json, curl
- **Composer**: For dependency management

## 🚀 Quick Start

### Basic Usage

```php
<?php

require_once 'vendor/autoload.php';

use RocketReach\SDK\RocketReachClient;

// Initialize the client
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
    ->id(12345)
    ->lookup();

echo "Person: " . $person->getName() . "\n";

// Person Enrich
$enriched = $client->personEnrich()
    ->name('John Doe')
    ->currentEmployer('Google')
    ->enrich();

echo "Company: " . $enriched->getCompanyName() . "\n";
```

### Advanced Usage

```php
<?php

use RocketReach\SDK\RocketReachClient;
use RocketReach\SDK\Exceptions\ApiException;

try {
    $client = new RocketReachClient('your-api-key');
    
    // Complex search with multiple filters
    $results = $client->peopleSearch()
        ->name(['John Doe', 'Jane Smith'])
        ->currentEmployer(['Google', 'Microsoft'])
        ->currentTitle(['Software Engineer', 'Senior Developer'])
        ->location(['San Francisco', 'Seattle'])
        ->industry(['Technology'])
        ->companySize(['1000+'])
        ->seniority(['Director', 'Manager'])
        ->skills(['PHP', 'Python', 'JavaScript'])
        ->page(1)
        ->pageSize(50)
        ->orderBy('relevance')
        ->search();
    
    foreach ($results->getProfiles() as $profile) {
        echo "Name: " . $profile['name'] . "\n";
        echo "Title: " . $profile['current_title'] . "\n";
        echo "Company: " . $profile['current_employer'] . "\n";
        echo "LinkedIn: " . $profile['linkedin_url'] . "\n\n";
    }
    
} catch (ApiException $e) {
    echo "API Error: " . $e->getMessage() . "\n";
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
```

## 📚 API Reference

### RocketReachClient

Main client class for interacting with the RocketReach API.

```php
$client = new RocketReachClient(string $apiKey, ?string $baseUrl = null);
```

#### Methods

- `peopleSearch()`: Returns a PeopleSearch endpoint instance
- `personLookup()`: Returns a PersonLookup endpoint instance
- `personEnrich()`: Returns a PersonEnrich endpoint instance

### People Search

Search for professional profiles by various criteria.

```php
$results = $client->peopleSearch()
    ->name(['John Doe'])                    // Full name(s)
    ->currentEmployer(['Google'])           // Current company name(s)
    ->currentTitle(['Software Engineer'])   // Current job title(s)
    ->currentEmployerDomain(['google.com']) // Employer website domain(s)
    ->location(['San Francisco, CA'])       // Location keyword(s)
    ->linkedinUrl(['https://linkedin.com/in/johndoe']) // LinkedIn URL(s)
    ->contactMethod(['email', 'phone'])     // Contact availability
    ->industry(['Technology'])              // Industry sector(s)
    ->companySize(['1000+'])               // Company size (employees)
    ->companyFunding(['1000000+'])         // Company funding raised
    ->companyRevenue(['100M+'])            // Company annual revenue
    ->seniority(['Director', 'Manager'])   // Seniority level(s)
    ->skills(['PHP', 'Python'])            // Skills or keywords
    ->education(['Stanford University'])   // Education institution(s)
    ->page(1)                              // Page number (1-based)
    ->pageSize(10)                         // Results per page (max 100)
    ->orderBy('relevance')                 // Sort order
    ->search();                            // Execute search
```

#### Response

```php
$results->getCount();        // Total number of results
$results->getProfiles();     // Array of profile data
$results->getPagination();   // Pagination information
```

### Person Lookup

Retrieve detailed contact information for a specific person.

```php
$person = $client->personLookup()
    ->id(12345)                           // RocketReach profile ID
    ->linkedinUrl('https://linkedin.com/in/johndoe') // LinkedIn URL
    ->name('John Doe')                    // Full name (requires currentEmployer)
    ->currentEmployer('Google')           // Company name (required with name)
    ->title('Software Engineer')          // Job title
    ->email('john@google.com')            // Email address
    ->npiNumber(1234567890)               // NPI number (healthcare)
    ->lookup();                           // Execute lookup
```

#### Response

```php
$person->getId();              // Profile ID
$person->getName();            // Full name
$person->getCurrentTitle();    // Current job title
$person->getCurrentEmployer(); // Current company
$person->getLinkedinUrl();     // LinkedIn profile URL
$person->getEmails();          // Array of email addresses
$person->getPhones();          // Array of phone numbers
$person->getStatus();          // Processing status
```

### Person Enrich

Get both person and company information in a single call.

```php
$enriched = $client->personEnrich()
    ->id(12345)                           // RocketReach profile ID
    ->linkedinUrl('https://linkedin.com/in/johndoe') // LinkedIn URL
    ->name('John Doe')                    // Full name (requires currentEmployer)
    ->currentEmployer('Google')           // Company name (required with name)
    ->title('Software Engineer')          // Job title
    ->email('john@google.com')            // Email address
    ->npiNumber(1234567890)               // NPI number (healthcare)
    ->enrich();                           // Execute enrichment
```

#### Response

```php
$enriched->getPerson();        // Person information
$enriched->getCompany();       // Company information
$enriched->getPersonName();    // Person's name
$enriched->getCompanyName();   // Company name
$enriched->getEmails();        // Email addresses
$enriched->getPhones();        // Phone numbers
```

## 🚨 Error Handling

The SDK provides custom exceptions for different error types:

```php
use RocketReach\SDK\Exceptions\{
    ApiException,
    InvalidApiKeyException,
    RateLimitException,
    NetworkException
};

try {
    $results = $client->peopleSearch()->search();
} catch (InvalidApiKeyException $e) {
    echo "Invalid API key: " . $e->getMessage();
} catch (RateLimitException $e) {
    echo "Rate limit exceeded: " . $e->getMessage();
} catch (NetworkException $e) {
    echo "Network error: " . $e->getMessage();
} catch (ApiException $e) {
    echo "API error: " . $e->getMessage();
}
```

### Exception Types

- **`ApiException`**: Base exception for API errors
- **`InvalidApiKeyException`**: Invalid or expired API key
- **`RateLimitException`**: Rate limit exceeded
- **`NetworkException`**: Network connectivity issues

## 🔄 Rate Limiting

The SDK automatically handles rate limiting with exponential backoff:

```php
$client = new RocketReachClient('your-api-key', [
    'retry_attempts' => 3,        // Number of retry attempts
    'retry_delay' => 1000,        // Initial delay in milliseconds
    'max_delay' => 30000,         // Maximum delay in milliseconds
    'timeout' => 30               // Request timeout in seconds
]);
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
./vendor/bin/phpunit

# Run with coverage
./vendor/bin/phpunit --coverage-html coverage/

# Run specific test suite
./vendor/bin/phpunit --testsuite Unit
./vendor/bin/phpunit --testsuite Integration
./vendor/bin/phpunit --testsuite E2E
./vendor/bin/phpunit --testsuite Live
```

### Test Configuration

The SDK includes comprehensive tests:

- **Unit Tests**: Test individual components
- **Integration Tests**: Test HTTP client integration
- **E2E Tests**: Test complete workflows
- **Live Tests**: Test against real API (use sparingly)

### Writing Tests

```php
<?php

use PHPUnit\Framework\TestCase;
use RocketReach\SDK\RocketReachClient;

class YourTest extends TestCase
{
    public function testYourFeature()
    {
        $client = new RocketReachClient('test-key');
        
        // Your test code here
        $this->assertTrue(true);
    }
}
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

```php
$client = new RocketReachClient('your-api-key', [
    'base_url' => 'https://api.rocketreach.co/api/v2',
    'timeout' => 30,
    'retry_attempts' => 3,
    'retry_delay' => 1000,
    'max_delay' => 30000,
    'user_agent' => 'RocketReach-PHP-SDK/1.0.0'
]);
```

## 🔧 Development

### Code Standards

- **PSR-12**: Follows PSR-12 coding standards
- **Type Hints**: Uses strict types and type hints
- **Docblocks**: Includes comprehensive PHPDoc comments
- **Static Analysis**: PHPStan level 8 compliance

### Static Analysis

```bash
# Run PHPStan
./vendor/bin/phpstan analyse src/

# Run with different levels
./vendor/bin/phpstan analyse src/ --level=8
```

### Code Style

```bash
# Check code style
./vendor/bin/phpcs src/

# Fix code style issues
./vendor/bin/phpcbf src/
```

## 📚 Examples

Check the `examples/` directory for complete working examples:

- **`basic_usage.php`**: Basic API usage examples
- **`advanced_search.php`**: Complex search scenarios
- **`error_handling.php`**: Error handling examples
- **`batch_processing.php`**: Batch processing examples

## 🆘 Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure your API key is valid and has proper permissions
2. **Rate Limiting**: The SDK handles rate limiting automatically
3. **Network Issues**: Check your internet connection and firewall settings
4. **Memory Issues**: Increase PHP memory limit if processing large datasets

### Debug Mode

```php
$client = new RocketReachClient('your-api-key', [
    'debug' => true,  // Enable debug logging
    'log_level' => 'debug'
]);
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
