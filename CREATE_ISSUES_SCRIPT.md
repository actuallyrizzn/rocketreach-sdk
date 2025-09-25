# GitHub Issues Creation Guide

This document contains templates for creating GitHub issues based on the comprehensive code audit. Each issue has been categorized by type and priority.

## How to Use These Templates

1. **Navigate to your GitHub repository**
2. **Click "Issues" → "New Issue"**
3. **Copy the appropriate template below**
4. **Customize as needed for your specific repository**

## Issues Summary

| Priority | Count | Categories |
|----------|--------|------------|
| Critical | 3 | Security (1), Bugs (2) |
| High | 8 | Security (1), Architecture (3), Testing (3), Dependencies (1) |
| Medium | 12 | Security (2), Architecture (3), Performance (4), Testing (2), Dependencies (1) |
| Low | 5 | Security (1), Bugs (2), Performance (1), Dependencies (1) |

---

## Quick Create Script

You can use the GitHub CLI to create all issues at once:

```bash
# Install GitHub CLI if not already installed
# https://github.com/cli/cli#installation

# Create all critical issues first
gh issue create --title "[SECURITY] API key partially exposed in client string representation" --label "security,critical,bug" --body-file SECURITY_ISSUE_1.md

gh issue create --title "[BUG] Critical bug in SearchQuery.to_dict() field name conversion" --label "bug,critical,python" --body-file BUG_ISSUE_1.md

# Continue with high priority issues...
# (See full script below)
```

## Individual Issue Templates

### Critical Priority Issues (Create First)

#### SECURITY-001: API Key Exposure
```
Title: [SECURITY] API key partially exposed in client string representation
Labels: security, critical, bug
Priority: Critical
Assignees: @security-team

## Description
The RocketReachClient's `__repr__` method in Python exposes the first 8 characters of the API key, which could lead to sensitive information disclosure in logs, debug output, or error messages.

## Location
- File: `python/src/rocketreach/sdk/client.py`
- Line: 149

## Current Code
```python
def __repr__(self) -> str:
    return f"RocketReachClient(api_key='{self._api_key[:8]}...', base_url='{self._base_url}')"
```

## Recommended Fix
```python
def __repr__(self) -> str:
    return f"RocketReachClient(api_key='***', base_url='{self._base_url}')"
```

## Impact
- **High** - API keys could be exposed in production logs
- Could facilitate credential stuffing attacks if partial keys are leaked

## Steps to Reproduce
1. Create a RocketReachClient instance
2. Print or log the client object
3. Observe API key prefix in output

## Acceptance Criteria
- [ ] API key is completely masked in string representations
- [ ] Tests added to verify masking
- [ ] Documentation updated
- [ ] Security review completed
```

#### BUG-001: Python Query Field Mapping
```
Title: [BUG] Critical bug in SearchQuery.to_dict() field name conversion
Labels: bug, critical, python
Priority: Critical

## Description
There's a critical bug in the Python SDK where field name conversion does nothing due to incorrect string replacement.

## Location
- File: `python/src/rocketreach/sdk/models/queries.py`
- Line: 58

## Current Code
```python
# Convert field names to API parameter names
api_name = field_name.replace('_', '_')  # This does nothing!
data[api_name] = value
```

## Impact
- **Critical** - Field names are not being converted properly
- May cause API requests to fail
- Could lead to incorrect query parameter formatting

## Recommended Fix
```python
# Option 1: Remove if no conversion needed
api_name = field_name
data[api_name] = value

# Option 2: Implement proper conversion if needed
api_name = field_name  # or implement actual conversion logic
data[api_name] = value
```

## Acceptance Criteria
- [ ] Fix field name conversion logic
- [ ] Add tests for field name conversion
- [ ] Verify API requests work correctly
- [ ] Update documentation if needed
```

### High Priority Issues

#### ARCHITECTURE-001: Centralized Configuration
```
Title: [ARCHITECTURE] Implement centralized configuration management
Labels: architecture, enhancement, configuration
Priority: High

## Description
Configuration constants are scattered across multiple classes making them hard to maintain and customize.

## Current State
```python
# In client.py
DEFAULT_BASE_URL = "https://api.rocketreach.co/api/v2"
DEFAULT_TIMEOUT = 30
DEFAULT_RETRY_ATTEMPTS = 3

# In http/client.py  
# Hardcoded retry logic

# In various files
# Magic numbers and hardcoded values
```

## Recommended Solution
Create centralized configuration classes with environment variable support.

## Benefits
- Single source of truth for configuration
- Environment-based configuration
- Easier testing with different configs
- Better documentation of configurable options

## Acceptance Criteria
- [ ] Create centralized config class
- [ ] Support environment variables
- [ ] Update all classes to use central config
- [ ] Add configuration documentation
- [ ] Add tests for configuration loading
```

Continue with remaining issues using similar templates...

## Bulk Creation Script

```bash
#!/bin/bash

# GitHub CLI bulk issue creation script
# Make sure you're in the repository directory and authenticated with gh

# Critical Issues
gh issue create \
  --title "[SECURITY] API key partially exposed in client string representation" \
  --label "security,critical,bug" \
  --body "$(cat <<'EOF'
The RocketReachClient's __repr__ method in Python exposes the first 8 characters of the API key.

**Location:** python/src/rocketreach/sdk/client.py:149

**Fix:** Completely mask API key in string representation

**Impact:** High - API keys could be exposed in production logs
EOF
)"

gh issue create \
  --title "[BUG] Critical bug in SearchQuery.to_dict() field name conversion" \
  --label "bug,critical,python" \
  --body "$(cat <<'EOF'
Critical bug where field_name.replace('_', '_') does nothing in queries.py:58

**Impact:** Field names not converted properly, may cause API failures

**Fix:** Remove redundant replacement or implement proper conversion
EOF
)"

# Continue with more issues...
```

## Priority Order for Creation

1. **Critical Issues (3)** - Create immediately
   - Security: API key exposure
   - Bug: Python query field mapping
   - Bug: HTTP status code logic

2. **High Priority Issues (8)** - Create within 1 week
   - Architecture: Centralized configuration
   - Testing: Edge case coverage
   - Dependencies: Security scanning

3. **Medium Priority Issues (12)** - Create within 1 month
   - Performance: orjson implementation
   - Architecture: Logging framework
   - Testing: Property-based testing

4. **Low Priority Issues (5)** - Create as time permits
   - Performance: Response caching
   - Dependencies: License compliance
   - Enhancement: User-agent improvements

## Labels to Use

### Priority Labels
- `critical` - Must fix immediately
- `high` - Important, fix soon
- `medium` - Moderate importance
- `low` - Nice to have

### Type Labels
- `security` - Security-related issues
- `bug` - Code defects
- `enhancement` - New features/improvements
- `architecture` - Design and structure
- `performance` - Speed/efficiency improvements
- `testing` - Test-related issues
- `dependencies` - Dependency management

### Component Labels
- `python` - Python SDK specific
- `php` - PHP SDK specific
- `documentation` - Documentation updates
- `ci-cd` - Continuous integration/deployment

## Project Board Setup

Consider creating a project board with columns:
- **Backlog** - All new issues
- **To Do** - Prioritized for current sprint
- **In Progress** - Currently being worked on
- **Review** - Ready for code review
- **Done** - Completed and deployed

This systematic approach will help you track and manage all identified improvements efficiently.