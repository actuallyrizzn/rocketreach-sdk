# Python Virtual Environment Setup

## Overview
This document describes how to set up and use the Python virtual environment for the RocketReach Python SDK development.

## Quick Setup

### Windows (PowerShell)
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\activate_env.ps1

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Test the setup
python -c "import sys; sys.path.insert(0, 'src'); from rocketreach.sdk import RocketReachClient; print('✅ SDK imported successfully!')"
```

### Windows (Command Prompt)
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
activate_env.bat

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### macOS/Linux
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Virtual Environment Structure

```
python/
├── venv/                    # Virtual environment directory
│   ├── Scripts/            # Windows activation scripts
│   ├── bin/                # Unix activation scripts
│   └── lib/                # Installed packages
├── activate_env.ps1        # PowerShell activation script
├── activate_env.bat        # Command Prompt activation script
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
└── src/                    # SDK source code
```

## Dependencies

### Production Dependencies (`requirements.txt`)
- `requests>=2.28.0` - HTTP client
- `urllib3>=1.26.0` - HTTP library
- `typing-extensions>=4.0.0` - Type hints support
- `orjson>=3.8.0` - Fast JSON handling
- `httpx>=0.24.0` - Modern HTTP client

### Development Dependencies (`requirements-dev.txt`)
- `pytest>=7.0.0` - Testing framework
- `pytest-cov>=4.0.0` - Coverage reporting
- `pytest-mock>=3.10.0` - Mocking utilities
- `black>=23.0.0` - Code formatting
- `isort>=5.12.0` - Import sorting
- `mypy>=1.0.0` - Type checking
- `flake8>=6.0.0` - Linting
- `bandit>=1.7.0` - Security analysis
- `sphinx>=6.0.0` - Documentation generation
- `pre-commit>=3.0.0` - Git hooks
- `tox>=4.0.0` - Testing automation

## Usage

### Activating the Environment
```bash
# Windows PowerShell
.\activate_env.ps1

# Windows Command Prompt
activate_env.bat

# macOS/Linux
source venv/bin/activate
```

### Deactivating the Environment
```bash
deactivate
```

### Running Tests
```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --category unit

# Run tests in loop
python run_tests.py --loop
```

### Development Commands
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

## Troubleshooting

### Common Issues

1. **Virtual environment not activating**
   - Ensure Python is installed and in PATH
   - Try using full path to activation script
   - Check PowerShell execution policy: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

2. **Package installation fails**
   - Update pip: `python -m pip install --upgrade pip`
   - Clear pip cache: `pip cache purge`
   - Check internet connection

3. **Import errors**
   - Ensure virtual environment is activated
   - Check that src/ directory is in Python path
   - Verify all dependencies are installed

### Verification

To verify the setup is working correctly:

```bash
# Test SDK import
python -c "import sys; sys.path.insert(0, 'src'); from rocketreach.sdk import RocketReachClient; print('✅ SDK imported successfully!')"

# Test basic functionality
python -c "import sys; sys.path.insert(0, 'src'); from rocketreach.sdk import RocketReachClient; client = RocketReachClient('test-key'); print('✅ Client created successfully!')"

# Run basic tests
python -c "import sys; sys.path.insert(0, 'src'); from rocketreach.sdk.models import SearchQuery; query = SearchQuery().set_name(['John']); print('✅ Models working!')"
```

## Best Practices

1. **Always activate the virtual environment** before working on the project
2. **Install dependencies** after creating a new virtual environment
3. **Use the provided scripts** for easy activation
4. **Keep requirements.txt updated** when adding new dependencies
5. **Test the setup** after any changes to the environment

## Notes

- The virtual environment is excluded from version control (see `.gitignore`)
- Dependencies are pinned to specific versions for reproducibility
- The SDK source code is in the `src/` directory
- All test files are in the `tests/` directory
