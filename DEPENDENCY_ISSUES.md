# Dependency & Maintenance Issues - GitHub Issue Templates

## Issue 28: Medium - Clean Up Unused Dependencies

**Title:** [DEPENDENCIES] Remove unused dependencies and optimize requirements

**Labels:** `dependencies`, `cleanup`, `maintenance`

**Description:**
The Python SDK includes dependencies in requirements.txt that are not actually used in the codebase, leading to unnecessary bloat and potential security surface area.

**Unused Dependencies Identified:**

1. **httpx** - Listed but never imported or used
2. **orjson** - Listed but standard json library is used instead

**Current requirements.txt:**
```
requests>=2.28.0
urllib3>=1.26.0
typing-extensions>=4.0.0
orjson>=3.8.0      # Not used
httpx>=0.24.0      # Not used
```

**Recommended Actions:**

1. **Remove unused dependencies:**
```
# Core dependencies
requests>=2.28.0
urllib3>=1.26.0

# Type hints support
typing-extensions>=4.0.0; python_version<"3.10"
```

2. **Or implement orjson usage** (see Performance Issue #17)

3. **Audit all dependencies:**
```bash
pip-audit  # Check for known vulnerabilities
safety check  # Alternative security scanner
```

**Benefits:**
- Smaller installation footprint
- Reduced security surface area
- Faster installation times
- Clearer dependency management

**Priority:** Medium - affects installation and security posture

---

## Issue 29: High - Implement Automated Dependency Security Scanning

**Title:** [SECURITY] Add automated dependency vulnerability scanning

**Labels:** `security`, `dependencies`, `automation`

**Description:**
No automated dependency vulnerability scanning is currently in place, which could lead to using packages with known security vulnerabilities.

**Recommended Implementation:**

1. **GitHub Dependabot:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/python"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    
  - package-ecosystem: "composer"
    directory: "/php"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
```

2. **Security Scanning in CI:**
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  python-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          cd python
          pip install safety pip-audit
          
      - name: Run safety check
        run: |
          cd python
          safety check -r requirements.txt
          
      - name: Run pip-audit
        run: |
          cd python
          pip-audit -r requirements.txt

  php-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Security check
        run: |
          cd php
          composer audit
```

3. **Local Development Tools:**
```bash
# Add to package.json/composer.json scripts
"security-check": "safety check && pip-audit"
```

**Benefits:**
- Early detection of vulnerable dependencies
- Automated security updates
- Compliance with security best practices
- Reduced manual security review overhead

---

## Issue 30: Medium - Improve Version Pinning Strategy

**Title:** [DEPENDENCIES] Implement better version pinning and compatibility strategy

**Labels:** `dependencies`, `versioning`, `compatibility`

**Description:**
Current dependency version constraints are inconsistent and could lead to compatibility issues or missed security updates.

**Current Issues:**

1. **Loose version constraints:**
```
requests>=2.28.0  # Could pull in breaking changes
urllib3>=1.26.0   # Very loose constraint
```

2. **Missing upper bounds:**
```
# Could install incompatible future versions
requests>=2.28.0,<3.0.0  # Better
```

3. **Inconsistent patterns between Python and PHP**

**Recommended Version Strategy:**

1. **Python - Use compatible release operator:**
```
# requirements.txt - Production
requests~=2.28.0    # Allows 2.28.x, not 2.29.0
urllib3~=1.26.0     # Allows 1.26.x, not 1.27.0
typing-extensions~=4.0.0; python_version<"3.10"

# requirements-dev.txt - Development
pytest~=7.0.0
pytest-cov~=4.0.0
black~=23.0.0
mypy~=1.0.0
```

2. **Lock files for reproducible builds:**
```bash
# Generate lock files
pip-compile requirements.in
pip-compile requirements-dev.in
```

3. **PHP - Consistent with Python strategy:**
```json
{
  "require": {
    "php": "^8.1",
    "guzzlehttp/guzzle": "^7.0",
    "psr/http-message": "^1.0"
  }
}
```

**Benefits:**
- Predictable builds
- Security updates without breaking changes
- Better compatibility testing
- Easier dependency management

---

## Issue 31: Low - Add Dependency License Compliance Checking

**Title:** [LEGAL] Implement dependency license compliance checking

**Labels:** `legal`, `dependencies`, `compliance`

**Description:**
No license compliance checking is in place to ensure all dependencies have compatible licenses.

**Recommended Implementation:**

1. **Python License Checking:**
```bash
# Install license checker
pip install pip-licenses

# Check licenses
pip-licenses --with-license-file --no-license-path
```

2. **Automated License Checking:**
```yaml
# .github/workflows/license-check.yml
name: License Check
on: [push, pull_request]

jobs:
  license-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check Python licenses
        run: |
          cd python
          pip install pip-licenses
          pip-licenses --fail-on GPL --fail-on AGPL
```

3. **License Documentation:**
```markdown
# LICENSES.md
## Allowed Licenses
- MIT
- Apache 2.0
- BSD (2-clause, 3-clause)
- ISC

## Prohibited Licenses
- GPL (any version)
- AGPL (any version)
- SSPL
```

**Benefits:**
- Legal compliance assurance
- Automated license conflict detection
- Clear license policy documentation
- Risk mitigation for commercial use

---

## Issue 32: Medium - Implement Dependency Update Automation

**Title:** [MAINTENANCE] Automate dependency updates with testing

**Labels:** `maintenance`, `automation`, `dependencies`

**Description:**
Implement automated dependency updates with proper testing to ensure dependencies stay current without breaking functionality.

**Recommended Implementation:**

1. **Automated Update Workflow:**
```yaml
# .github/workflows/dependency-update.yml
name: Dependency Update
on:
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM
  workflow_dispatch:  # Manual trigger

jobs:
  update-dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Update Python dependencies
        run: |
          cd python
          pip install pip-tools
          pip-compile --upgrade requirements.in
          pip-compile --upgrade requirements-dev.in
          
      - name: Update PHP dependencies
        run: |
          cd php
          composer update
          
      - name: Run tests
        run: |
          # Run full test suite
          cd python && pytest
          cd php && ./vendor/bin/phpunit
          
      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v4
        with:
          title: 'chore: update dependencies'
          body: |
            Automated dependency update
            
            - Python dependencies updated
            - PHP dependencies updated
            - All tests passing
          branch: dependency-update
```

2. **Dependency Health Monitoring:**
```python
# scripts/check_dependency_health.py
import requests
import json

def check_dependency_health():
    """Check if dependencies have recent releases or security issues"""
    with open('requirements.txt') as f:
        deps = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    for dep in deps:
        package_name = dep.split('>=')[0].split('==')[0]
        
        # Check PyPI for latest version
        response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
        if response.status_code == 200:
            data = response.json()
            latest_version = data['info']['version']
            last_release = data['releases'][latest_version][0]['upload_time']
            print(f"{package_name}: Latest {latest_version}, Released {last_release}")
```

**Benefits:**
- Keep dependencies current
- Automated security updates
- Reduced manual maintenance overhead
- Consistent update testing