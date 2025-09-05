# Testing Guide

Comprehensive guide for testing the RocketReach SDK.

## 🧪 Testing Philosophy

The RocketReach SDK follows a comprehensive testing strategy with multiple layers:

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test component interactions
3. **End-to-End (E2E) Tests**: Test complete workflows
4. **Live Tests**: Test against real API (conservative usage)

## 📊 Test Coverage Goals

- **Unit Tests**: 100% code coverage
- **Integration Tests**: Critical path coverage
- **E2E Tests**: Complete workflow coverage
- **Live Tests**: API compatibility validation

## 🏗️ Test Structure

### PHP Test Structure

```
php/tests/
├── Unit/                    # Unit tests
│   ├── RocketReachClientTest.php
│   ├── Http/
│   ├── Exceptions/
│   ├── Models/
│   └── Endpoints/
├── Integration/             # Integration tests
│   ├── HttpClientIntegrationTest.php
│   └── TestCase.php
├── E2E/                     # End-to-end tests
│   ├── WorkflowTest.php
│   └── TestCase.php
├── Live/                    # Live API tests
│   ├── ApiTest.php
│   └── TestCase.php
├── Fixtures/                # Test data
│   ├── ApiResponses.php
│   └── TestData.php
└── bootstrap.php            # Test bootstrap
```

### Python Test Structure

```
python/tests/
├── unit/                    # Unit tests
│   ├── test_client.py
│   ├── test_http_client.py
│   └── test_models.py
├── integration/             # Integration tests
├── e2e/                     # End-to-end tests
├── live/                    # Live API tests
│   └── test_live_api.py
├── fixtures/                # Test data
│   ├── api_responses.py
│   └── test_data.py
└── conftest.py              # Pytest configuration
```

## 🚀 Running Tests

### PHP Tests

```bash
cd php

# Run all tests
./vendor/bin/phpunit

# Run specific test suite
./vendor/bin/phpunit --testsuite Unit
./vendor/bin/phpunit --testsuite Integration
./vendor/bin/phpunit --testsuite E2E
./vendor/bin/phpunit --testsuite Live

# Run with coverage
./vendor/bin/phpunit --coverage-html coverage/

# Run specific test
./vendor/bin/phpunit tests/Unit/RocketReachClientTest.php

# Run with verbose output
./vendor/bin/phpunit --verbose
```

### Python Tests

```bash
cd python

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
pytest tests/live/

# Run with coverage
pytest --cov=src/ --cov-report=html

# Run specific test
pytest tests/unit/test_client.py

# Run with verbose output
pytest -v
```

## 🔧 Test Configuration

### PHP (phpunit.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="tests/bootstrap.php"
         colors="true">
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Integration">
            <directory>tests/Integration</directory>
        </testsuite>
        <testsuite name="E2E">
            <directory>tests/E2E</directory>
        </testsuite>
        <testsuite name="Live">
            <directory>tests/Live</directory>
        </testsuite>
    </testsuites>
    <coverage>
        <include>
            <directory suffix=".php">src</directory>
        </include>
        <report>
            <html outputDirectory="coverage"/>
        </report>
    </coverage>
</phpunit>
```

### Python (pytest.ini)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    live: Live API tests
    slow: Slow running tests
```

## 📝 Writing Tests

### Unit Tests

Test individual components in isolation with mocked dependencies.

#### PHP Example

```php
<?php

use PHPUnit\Framework\TestCase;
use RocketReach\SDK\RocketReachClient;
use RocketReach\SDK\Http\HttpClient;

class RocketReachClientTest extends TestCase
{
    private HttpClient $mockHttpClient;
    private RocketReachClient $client;

    protected function setUp(): void
    {
        $this->mockHttpClient = $this->createMock(HttpClient::class);
        $this->client = new RocketReachClient('test-key');
    }

    public function testClientCreation()
    {
        $this->assertEquals('test-key', $this->client->getApiKey());
    }

    public function testPeopleSearch()
    {
        $this->mockHttpClient->expects($this->once())
            ->method('post')
            ->with('/person/search', $this->isType('array'))
            ->willReturn(['profiles' => [], 'pagination' => []]);

        $result = $this->client->peopleSearch()
            ->name(['John Doe'])
            ->search();

        $this->assertInstanceOf(SearchResponse::class, $result);
    }
}
```

#### Python Example

```python
import pytest
from unittest.mock import Mock, patch
from rocketreach.sdk import RocketReachClient

class TestRocketReachClient:
    def setup_method(self):
        self.client = RocketReachClient('test-key')

    def test_client_creation(self):
        assert self.client.api_key == 'test-key'

    @patch('rocketreach.sdk.http.client.requests.post')
    def test_people_search(self, mock_post):
        mock_post.return_value.json.return_value = {
            'profiles': [],
            'pagination': {}
        }
        mock_post.return_value.status_code = 201

        result = (self.client.people_search()
                 .name(['John Doe'])
                 .search())

        assert hasattr(result, 'profiles')
        assert hasattr(result, 'pagination')
```

### Integration Tests

Test component interactions with real implementations.

#### PHP Example

```php
<?php

use PHPUnit\Framework\TestCase;
use RocketReach\SDK\Http\HttpClient;

class HttpClientIntegrationTest extends TestCase
{
    public function testHttpClientWithMockServer()
    {
        $httpClient = new HttpClient('https://httpbin.org', 'test-key');
        
        $response = $httpClient->get('/get');
        
        $this->assertIsArray($response);
        $this->assertArrayHasKey('headers', $response);
    }
}
```

#### Python Example

```python
import pytest
from rocketreach.sdk.http import HttpClient

class TestHttpClientIntegration:
    def test_http_client_with_mock_server(self):
        http_client = HttpClient('https://httpbin.org', 'test-key')
        
        response = http_client.get('/get')
        
        assert isinstance(response, dict)
        assert 'headers' in response
```

### E2E Tests

Test complete workflows from start to finish.

#### PHP Example

```php
<?php

use PHPUnit\Framework\TestCase;
use RocketReach\SDK\RocketReachClient;

class WorkflowTest extends TestCase
{
    public function testSearchToLookupWorkflow()
    {
        $client = new RocketReachClient('test-key');
        
        // Mock the search response
        $this->mockHttpClient->expects($this->exactly(2))
            ->method('post')
            ->willReturnOnConsecutiveCalls(
                ['profiles' => [['id' => 12345, 'name' => 'John Doe']], 'pagination' => []],
                ['id' => 12345, 'name' => 'John Doe', 'emails' => []]
            );

        // Search for people
        $searchResults = $client->peopleSearch()
            ->name(['John Doe'])
            ->search();

        $this->assertCount(1, $searchResults->getProfiles());

        // Lookup specific person
        $person = $client->personLookup()
            ->id(12345)
            ->lookup();

        $this->assertEquals('John Doe', $person->getName());
    }
}
```

### Live Tests

Test against the real API (use sparingly).

#### PHP Example

```php
<?php

use PHPUnit\Framework\TestCase;
use RocketReach\SDK\RocketReachClient;

class ApiTest extends TestCase
{
    private RocketReachClient $client;

    protected function setUp(): void
    {
        $apiKey = getenv('ROCKETREACH_API_KEY');
        if (!$apiKey) {
            $this->markTestSkipped('API key not provided');
        }
        
        $this->client = new RocketReachClient($apiKey);
    }

    public function testPeopleSearch()
    {
        $results = $this->client->peopleSearch()
            ->name(['John Doe'])
            ->pageSize(1)
            ->search();

        $this->assertInstanceOf(SearchResponse::class, $results);
        $this->assertGreaterThanOrEqual(0, $results->getCount());
    }
}
```

#### Python Example

```python
import pytest
import os
from rocketreach.sdk import RocketReachClient

@pytest.mark.live
class TestLiveAPI:
    def setup_method(self):
        api_key = os.getenv('ROCKETREACH_API_KEY')
        if not api_key:
            pytest.skip('API key not provided')
        
        self.client = RocketReachClient(api_key)

    def test_people_search(self):
        results = (self.client.people_search()
                  .name(['John Doe'])
                  .page_size(1)
                  .search())

        assert hasattr(results, 'profiles')
        assert hasattr(results, 'pagination')
        assert results.count >= 0
```

## 🎯 Test Data

### Fixtures

Use consistent test data across all tests.

#### PHP Fixtures

```php
<?php

class ApiResponses
{
    public static function getSearchResponse(): array
    {
        return [
            'profiles' => [
                [
                    'id' => 12345,
                    'name' => 'John Doe',
                    'current_title' => 'Software Engineer',
                    'current_employer' => 'Google',
                    'linkedin_url' => 'https://www.linkedin.com/in/johndoe'
                ]
            ],
            'pagination' => [
                'start' => 1,
                'next' => 2,
                'total' => 100
            ]
        ];
    }

    public static function getPersonResponse(): array
    {
        return [
            'id' => 12345,
            'name' => 'John Doe',
            'current_title' => 'Software Engineer',
            'current_employer' => 'Google',
            'status' => 'complete',
            'emails' => [
                [
                    'email' => 'john@google.com',
                    'type' => 'professional',
                    'grade' => 'A'
                ]
            ]
        ];
    }
}
```

#### Python Fixtures

```python
class ApiResponses:
    @staticmethod
    def get_search_response():
        return {
            'profiles': [
                {
                    'id': 12345,
                    'name': 'John Doe',
                    'current_title': 'Software Engineer',
                    'current_employer': 'Google',
                    'linkedin_url': 'https://www.linkedin.com/in/johndoe'
                }
            ],
            'pagination': {
                'start': 1,
                'next': 2,
                'total': 100
            }
        }

    @staticmethod
    def get_person_response():
        return {
            'id': 12345,
            'name': 'John Doe',
            'current_title': 'Software Engineer',
            'current_employer': 'Google',
            'status': 'complete',
            'emails': [
                {
                    'email': 'john@google.com',
                    'type': 'professional',
                    'grade': 'A'
                }
            ]
        }
```

## 🔄 Test Automation

### Continuous Integration

#### GitHub Actions (PHP)

```yaml
name: PHP Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.1'
        extensions: mbstring, xml, ctype, iconv, intl, pdo_sqlite
        coverage: xdebug
    
    - name: Install dependencies
      run: composer install --prefer-dist --no-progress
    
    - name: Run tests
      run: ./vendor/bin/phpunit --coverage-clover coverage.xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

#### GitHub Actions (Python)

```yaml
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: pytest --cov=src/ --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
```

### Local Test Scripts

#### PHP

```bash
#!/bin/bash
# scripts/test-php.sh

echo "Running PHP tests..."

# Run unit tests
./vendor/bin/phpunit --testsuite Unit

# Run integration tests
./vendor/bin/phpunit --testsuite Integration

# Run E2E tests
./vendor/bin/phpunit --testsuite E2E

# Run live tests (if API key provided)
if [ ! -z "$ROCKETREACH_API_KEY" ]; then
    ./vendor/bin/phpunit --testsuite Live
fi

echo "PHP tests completed!"
```

#### Python

```bash
#!/bin/bash
# scripts/test-python.sh

echo "Running Python tests..."

# Run unit tests
pytest tests/unit/ -v

# Run integration tests
pytest tests/integration/ -v

# Run E2E tests
pytest tests/e2e/ -v

# Run live tests (if API key provided)
if [ ! -z "$ROCKETREACH_API_KEY" ]; then
    pytest tests/live/ -v -m live
fi

echo "Python tests completed!"
```

## 🚨 Best Practices

### Test Organization

1. **One test per method**: Each test should verify one specific behavior
2. **Descriptive names**: Use clear, descriptive test method names
3. **Arrange-Act-Assert**: Structure tests with clear sections
4. **Independent tests**: Tests should not depend on each other
5. **Clean setup/teardown**: Use proper setup and teardown methods

### Mocking Guidelines

1. **Mock external dependencies**: Don't test external services in unit tests
2. **Use realistic data**: Mock responses should match real API responses
3. **Verify interactions**: Assert that mocked methods are called correctly
4. **Don't over-mock**: Only mock what's necessary for the test

### Live Testing

1. **Use sparingly**: Live tests consume API credits
2. **Environment variables**: Use environment variables for API keys
3. **Skip when unavailable**: Skip tests when API key is not provided
4. **Conservative usage**: Use minimal data and requests
5. **Rate limiting**: Implement proper delays between requests

### Performance Testing

1. **Timeout tests**: Test request timeouts
2. **Rate limiting**: Test rate limit handling
3. **Retry logic**: Test retry mechanisms
4. **Memory usage**: Monitor memory consumption
5. **Concurrent requests**: Test concurrent API calls

## 🐛 Debugging Tests

### PHP Debugging

```php
// Enable debug output
$this->expectOutputString('expected output');

// Debug variables
var_dump($variable);

// Use Xdebug for step debugging
// Set breakpoints in your IDE
```

### Python Debugging

```python
import pdb

# Set breakpoints
pdb.set_trace()

# Debug output
print(f"Debug: {variable}")

# Use pytest debugging
pytest --pdb  # Drop into debugger on failure
```

## 📊 Coverage Reports

### Generating Coverage

#### PHP

```bash
# HTML coverage report
./vendor/bin/phpunit --coverage-html coverage/

# Clover XML for CI
./vendor/bin/phpunit --coverage-clover coverage.xml
```

#### Python

```bash
# HTML coverage report
pytest --cov=src/ --cov-report=html

# XML coverage for CI
pytest --cov=src/ --cov-report=xml
```

### Coverage Goals

- **Unit Tests**: 100% line coverage
- **Integration Tests**: 90%+ coverage of critical paths
- **E2E Tests**: 80%+ coverage of user workflows
- **Overall**: 95%+ combined coverage

## 🆘 Troubleshooting

### Common Issues

1. **Test failures**: Check test data and assertions
2. **Mock issues**: Verify mock setup and expectations
3. **Environment issues**: Check dependencies and configuration
4. **API issues**: Verify API key and network connectivity

### Getting Help

- **Test failures**: Check the test output and error messages
- **Mock issues**: Review the mocking documentation
- **Environment issues**: Check the development guide
- **API issues**: Contact RocketReach support

## 📋 Test Checklist

Before submitting code:

- [ ] All unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Live tests pass (if applicable)
- [ ] Coverage meets requirements
- [ ] No test data leaks
- [ ] Proper error handling tested
- [ ] Edge cases covered
- [ ] Performance tests pass
- [ ] Documentation updated
