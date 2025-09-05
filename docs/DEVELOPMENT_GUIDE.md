# Development Guide

Complete guide for developing with the RocketReach SDK.

## 🏗️ Project Structure

```
rocketreach-sdk/
├── php/                    # PHP SDK
│   ├── src/               # Source code
│   ├── tests/             # Test suite
│   ├── examples/          # Usage examples
│   ├── composer.json      # Dependencies
│   └── README.md          # PHP-specific docs
├── python/                # Python SDK
│   ├── src/               # Source code
│   ├── tests/             # Test suite
│   ├── examples/          # Usage examples
│   ├── setup.py           # Package configuration
│   └── README.md          # Python-specific docs
├── docs/                  # Documentation
└── README.md              # Main documentation
```

## 🚀 Getting Started

### Prerequisites

- **PHP**: 8.1 or higher
- **Python**: 3.8 or higher
- **Composer**: Latest version (for PHP)
- **pip**: Latest version (for Python)
- **Git**: For version control

### Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/actuallyrizzn/rocketreach-sdk.git
   cd rocketreach-sdk
   ```

2. **Choose your language**:
   - [PHP Development Setup](#php-development-setup)
   - [Python Development Setup](#python-development-setup)

## 🐘 PHP Development Setup

### Installation

```bash
cd php
composer install
```

### Development Dependencies

The project includes development dependencies for testing and code quality:

- **PHPUnit**: Testing framework
- **PHPStan**: Static analysis
- **PHP_CodeSniffer**: Code style checking

### Running Tests

```bash
# Run all tests
./vendor/bin/phpunit

# Run specific test suite
./vendor/bin/phpunit --testsuite Unit
./vendor/bin/phpunit --testsuite Integration
./vendor/bin/phpunit --testsuite E2E
./vendor/bin/phpunit --testsuite Live

# Run with coverage
./vendor/bin/phpunit --coverage-html coverage/
```

### Code Quality

```bash
# Static analysis
./vendor/bin/phpstan analyse src/

# Code style checking
./vendor/bin/phpcs src/
./vendor/bin/phpcbf src/  # Auto-fix
```

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow PSR-12 coding standards
   - Add tests for new functionality
   - Update documentation

3. **Run tests**:
   ```bash
   ./vendor/bin/phpunit
   ```

4. **Check code quality**:
   ```bash
   ./vendor/bin/phpstan analyse src/
   ./vendor/bin/phpcs src/
   ```

5. **Commit and push**:
   ```bash
   git add .
   git commit -m "Add your feature"
   git push origin feature/your-feature-name
   ```

## 🐍 Python Development Setup

### Installation

```bash
cd python

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt
```

### Development Dependencies

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
pytest tests/live/

# Run with coverage
pytest --cov=src/ --cov-report=html

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow PEP 8 style guidelines
   - Add type hints
   - Add tests for new functionality
   - Update documentation

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Check code quality**:
   ```bash
   black src/ tests/
   isort src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

5. **Commit and push**:
   ```bash
   git add .
   git commit -m "Add your feature"
   git push origin feature/your-feature-name
   ```

## 🧪 Testing

### Test Structure

Both SDKs follow the same testing structure:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete workflows
- **Live Tests**: Test against real API (use sparingly)

### Writing Tests

#### PHP (PHPUnit)

```php
<?php

use PHPUnit\Framework\TestCase;
use RocketReach\SDK\RocketReachClient;

class RocketReachClientTest extends TestCase
{
    public function testClientCreation()
    {
        $client = new RocketReachClient('test-key');
        $this->assertEquals('test-key', $client->getApiKey());
    }
}
```

#### Python (pytest)

```python
import pytest
from rocketreach.sdk import RocketReachClient

def test_client_creation():
    client = RocketReachClient('test-key')
    assert client.api_key == 'test-key'
```

### Test Data

Use the provided test fixtures:

- **PHP**: `tests/Fixtures/`
- **Python**: `tests/fixtures/`

### Mocking

#### PHP

```php
use PHPUnit\Framework\MockObject\MockObject;

$mockHttpClient = $this->createMock(HttpClient::class);
$mockHttpClient->method('post')
    ->willReturn(['profiles' => [], 'pagination' => []]);
```

#### Python

```python
from unittest.mock import Mock, patch

@patch('rocketreach.sdk.http.client.requests.post')
def test_search(mock_post):
    mock_post.return_value.json.return_value = {
        'profiles': [],
        'pagination': {}
    }
```

## 📝 Code Standards

### PHP (PSR-12)

- Use PSR-12 coding standards
- Follow PSR-4 autoloading
- Use strict types: `declare(strict_types=1);`
- Add proper docblocks
- Use type hints

### Python (PEP 8)

- Follow PEP 8 style guidelines
- Use type hints
- Add docstrings
- Use meaningful variable names
- Keep line length under 88 characters (Black default)

## 🔧 Configuration

### Environment Variables

Create a `.env` file for local development:

```bash
# .env
ROCKETREACH_API_KEY=your-api-key-here
ROCKETREACH_BASE_URL=https://api.rocketreach.co/api/v2
ROCKETREACH_TIMEOUT=30
ROCKETREACH_RETRY_ATTEMPTS=3
```

### IDE Configuration

#### VS Code

Create `.vscode/settings.json`:

```json
{
    "php.suggest.basic": false,
    "php.validate.enable": true,
    "php.validate.executablePath": "/usr/bin/php",
    "python.defaultInterpreterPath": "./python/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black"
}
```

## 🚀 Building and Packaging

### PHP

```bash
# Build for distribution
composer install --no-dev --optimize-autoloader

# Create PHAR (if configured)
php -d phar.readonly=0 build.php
```

### Python

```bash
# Build wheel
python -m build

# Build source distribution
python setup.py sdist

# Install in development mode
pip install -e .
```

## 📚 Documentation

### Updating Documentation

1. **API Documentation**: Update `docs/API_REFERENCE.md`
2. **Code Documentation**: Update inline docstrings
3. **README Files**: Update language-specific READMEs
4. **Examples**: Update example files

### Documentation Standards

- Use Markdown format
- Include code examples
- Add table of contents for long documents
- Keep language-specific docs in their respective directories

## 🐛 Debugging

### PHP

```php
// Enable error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Use Xdebug for debugging
// Install Xdebug and configure your IDE
```

### Python

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Use pdb for debugging
import pdb; pdb.set_trace()
```

## 🔄 Continuous Integration

### GitHub Actions

The project includes GitHub Actions workflows for:

- **PHP**: Run tests, static analysis, and code style checks
- **Python**: Run tests, linting, and type checking
- **Documentation**: Build and deploy documentation

### Local CI

```bash
# Run all checks locally
./scripts/ci-check.sh
```

## 🆘 Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure your API key is valid and has proper permissions
2. **Rate Limiting**: Implement proper retry logic with exponential backoff
3. **Network Issues**: Check your internet connection and firewall settings
4. **Dependency Issues**: Ensure all dependencies are properly installed

### Getting Help

- **Issues**: [GitHub Issues](https://github.com/actuallyrizzn/rocketreach-sdk/issues)
- **Documentation**: Check the relevant README files
- **RocketReach Support**: [RocketReach Support](https://rocketreach.co/support)

## 📋 Checklist

Before submitting a pull request:

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Examples work correctly
- [ ] No sensitive data in commits
- [ ] Proper commit messages
- [ ] Branch is up to date with main
