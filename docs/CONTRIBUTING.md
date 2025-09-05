# Contributing to RocketReach SDK

Thank you for your interest in contributing to the RocketReach SDK! This guide will help you get started with contributing to the project.

## 🤝 How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **Bug Reports**: Report issues you've found
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit bug fixes or new features
- **Documentation**: Improve or add documentation
- **Examples**: Add usage examples
- **Tests**: Improve test coverage

### Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Make your changes** following our guidelines
5. **Test your changes** thoroughly
6. **Submit a pull request**

## 🏗️ Development Setup

### Prerequisites

- **Git**: For version control
- **PHP**: 8.1+ (for PHP SDK contributions)
- **Python**: 3.8+ (for Python SDK contributions)
- **Composer**: For PHP dependencies
- **pip**: For Python dependencies

### Setup Instructions

1. **Fork and clone**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/rocketreach-sdk.git
   cd rocketreach-sdk
   ```

2. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/actuallyrizzn/rocketreach-sdk.git
   ```

3. **Choose your language**:
   - [PHP Development Setup](#php-development-setup)
   - [Python Development Setup](#python-development-setup)

### PHP Development Setup

```bash
cd php
composer install
```

### Python Development Setup

```bash
cd python
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
```

## 📝 Coding Standards

### General Guidelines

- **Follow existing patterns**: Maintain consistency with existing code
- **Write clear code**: Use descriptive variable and function names
- **Add documentation**: Include docstrings and comments
- **Write tests**: Add tests for new functionality
- **Keep commits small**: Make focused, atomic commits

### PHP Standards

- **PSR-12**: Follow PSR-12 coding standards
- **Type hints**: Use strict types and type hints
- **Docblocks**: Add proper PHPDoc comments
- **Naming**: Use camelCase for methods, PascalCase for classes

```php
<?php

declare(strict_types=1);

namespace RocketReach\SDK;

/**
 * Example class demonstrating coding standards
 */
class ExampleClass
{
    private string $property;

    public function __construct(string $property)
    {
        $this->property = $property;
    }

    /**
     * Example method with proper documentation
     *
     * @param string $input The input string
     * @return string The processed string
     */
    public function processInput(string $input): string
    {
        return strtoupper($input);
    }
}
```

### Python Standards

- **PEP 8**: Follow PEP 8 style guidelines
- **Type hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings
- **Naming**: Use snake_case for functions and variables

```python
from typing import List, Optional

class ExampleClass:
    """Example class demonstrating coding standards."""
    
    def __init__(self, property: str) -> None:
        """Initialize the class.
        
        Args:
            property: The property value
        """
        self.property = property
    
    def process_input(self, input_str: str) -> str:
        """Process the input string.
        
        Args:
            input_str: The input string to process
            
        Returns:
            The processed string
        """
        return input_str.upper()
```

## 🧪 Testing Requirements

### Test Coverage

- **Unit Tests**: 100% coverage for new code
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete workflows
- **Live Tests**: Test against real API (use sparingly)

### Running Tests

#### PHP

```bash
cd php

# Run all tests
./vendor/bin/phpunit

# Run with coverage
./vendor/bin/phpunit --coverage-html coverage/

# Run specific test
./vendor/bin/phpunit tests/Unit/YourTest.php
```

#### Python

```bash
cd python

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run all tests
pytest

# Run with coverage
pytest --cov=src/ --cov-report=html

# Run specific test
pytest tests/unit/test_your_test.py
```

### Writing Tests

#### Test Structure

- **Arrange**: Set up test data and mocks
- **Act**: Execute the code being tested
- **Assert**: Verify the expected outcome

#### Example Test

```php
<?php

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    public function testMethodReturnsExpectedValue()
    {
        // Arrange
        $input = 'test input';
        $expected = 'TEST INPUT';
        
        // Act
        $result = $this->subject->processInput($input);
        
        // Assert
        $this->assertEquals($expected, $result);
    }
}
```

## 📚 Documentation

### Documentation Standards

- **Markdown**: Use Markdown for all documentation
- **Clear structure**: Use headers and lists for organization
- **Code examples**: Include working code examples
- **Keep updated**: Update documentation with code changes

### Documentation Types

1. **API Documentation**: Update `docs/API_REFERENCE.md`
2. **Code Documentation**: Update inline docstrings
3. **README Files**: Update language-specific READMEs
4. **Examples**: Add or update example files

### Example Documentation

```markdown
## New Feature

This feature adds support for [description].

### Usage

```php
$client = new RocketReachClient('your-api-key');
$result = $client->newMethod()->execute();
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `param1` | string | Yes | Description of param1 |
| `param2` | int | No | Description of param2 |

### Response

Returns a `ResponseObject` containing the results.
```

## 🔄 Git Workflow

### Branch Naming

Use descriptive branch names:

- `feature/add-new-endpoint`
- `bugfix/fix-authentication-issue`
- `docs/update-api-reference`
- `test/add-coverage-for-models`

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add support for new API endpoint
fix: resolve authentication timeout issue
docs: update installation instructions
test: add unit tests for response models
refactor: improve error handling logic
```

### Pull Request Process

1. **Create a feature branch** from `main`
2. **Make your changes** following our guidelines
3. **Write tests** for your changes
4. **Update documentation** if needed
5. **Run all tests** to ensure they pass
6. **Submit a pull request** with a clear description

### Pull Request Template

```markdown
## Description

Brief description of the changes made.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Test improvement

## Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Live tests pass (if applicable)
- [ ] Manual testing completed

## Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented if necessary)
```

## 🐛 Bug Reports

### Before Reporting

1. **Check existing issues**: Search for similar issues
2. **Test latest version**: Ensure you're using the latest code
3. **Reproduce the issue**: Create a minimal reproduction case

### Bug Report Template

```markdown
## Bug Description

Clear description of the bug.

## Steps to Reproduce

1. Step one
2. Step two
3. Step three

## Expected Behavior

What should happen.

## Actual Behavior

What actually happens.

## Environment

- PHP Version: 8.1.0
- Python Version: 3.8.0
- SDK Version: 1.0.0
- Operating System: Ubuntu 20.04

## Additional Context

Any additional information that might be helpful.
```

## 💡 Feature Requests

### Before Requesting

1. **Check existing issues**: Search for similar requests
2. **Consider the scope**: Ensure it fits the project's goals
3. **Provide use cases**: Explain why this feature is needed

### Feature Request Template

```markdown
## Feature Description

Clear description of the requested feature.

## Use Case

Why is this feature needed? What problem does it solve?

## Proposed Solution

How would you like this feature to work?

## Alternatives Considered

What other solutions have you considered?

## Additional Context

Any additional information that might be helpful.
```

## 🔍 Code Review Process

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] No breaking changes (or documented)
- [ ] Performance implications considered
- [ ] Security implications considered

### Review Guidelines

- **Be constructive**: Provide helpful feedback
- **Be specific**: Point out exact issues
- **Be respectful**: Maintain a positive tone
- **Be thorough**: Check all aspects of the code

## 🚀 Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Changelog updated
- [ ] Version numbers updated
- [ ] Release notes prepared
- [ ] Tag created

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For general questions and discussions
- **Pull Requests**: For code contributions

### Response Times

- **Bug reports**: Within 48 hours
- **Feature requests**: Within 1 week
- **Pull requests**: Within 3 business days
- **General questions**: Within 1 week

## 📋 Contributor Checklist

Before submitting your contribution:

- [ ] Code follows style guidelines
- [ ] Tests are written and pass
- [ ] Documentation is updated
- [ ] No sensitive data in commits
- [ ] Commit messages are clear
- [ ] Pull request description is complete
- [ ] Branch is up to date with main
- [ ] All CI checks pass

## 🎉 Recognition

Contributors will be recognized in:

- **README**: Listed as contributors
- **Changelog**: Mentioned in release notes
- **GitHub**: Added to contributors list

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project:

- **Code**: GNU Affero General Public License v3.0
- **Documentation**: Creative Commons Attribution-ShareAlike 4.0 International

## 🆘 Questions?

If you have any questions about contributing, please:

1. **Check the documentation**: Review this guide and other docs
2. **Search issues**: Look for similar questions
3. **Open an issue**: Create a new issue with the `question` label
4. **Start a discussion**: Use GitHub Discussions for general questions

Thank you for contributing to the RocketReach SDK! 🚀
