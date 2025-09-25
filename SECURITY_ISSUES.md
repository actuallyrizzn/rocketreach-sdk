# Security Issues - GitHub Issue Templates

## Issue 1: Critical - API Key Exposure in Debug Output

**Title:** [SECURITY] API key partially exposed in client string representation

**Labels:** `security`, `critical`, `bug`

**Description:**
The RocketReachClient's `__repr__` method in Python exposes the first 8 characters of the API key, which could lead to sensitive information disclosure in logs, debug output, or error messages.

**Location:**
- File: `python/src/rocketreach/sdk/client.py`
- Line: 149

**Current Code:**
```python
def __repr__(self) -> str:
    return f"RocketReachClient(api_key='{self._api_key[:8]}...', base_url='{self._base_url}')"
```

**Recommended Fix:**
```python
def __repr__(self) -> str:
    return f"RocketReachClient(api_key='***', base_url='{self._base_url}')"
```

**Impact:**
- **High** - API keys could be exposed in production logs
- Could facilitate credential stuffing attacks if partial keys are leaked

**Steps to Reproduce:**
1. Create a RocketReachClient instance
2. Print or log the client object
3. Observe API key prefix in output

---

## Issue 2: High - Missing API Key Format Validation

**Title:** [SECURITY] No validation for API key format and structure

**Labels:** `security`, `enhancement`, `validation`

**Description:**
The SDK accepts any non-empty string as an API key without validating its format. This could lead to runtime errors and makes it harder to catch configuration mistakes early.

**Location:**
- File: `python/src/rocketreach/sdk/client.py`
- File: `php/src/RocketReachClient.php`

**Current Validation:**
```python
if not api_key or not api_key.strip():
    raise InvalidApiKeyException("API key cannot be empty")
```

**Recommended Enhancement:**
```python
import re

API_KEY_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{32,64}$')  # Adjust pattern as needed

def validate_api_key(api_key: str) -> bool:
    if not api_key or not api_key.strip():
        return False
    return bool(API_KEY_PATTERN.match(api_key.strip()))
```

**Impact:**
- Better error messages for invalid API keys
- Early detection of configuration issues
- Reduced support requests

---

## Issue 3: Medium - Sensitive Data in Exception Messages

**Title:** [SECURITY] Potential sensitive data exposure in exception messages

**Labels:** `security`, `medium`, `enhancement`

**Description:**
Exception classes include full response text and details, which might contain sensitive information that could be logged or displayed in error messages.

**Location:**
- File: `python/src/rocketreach/sdk/exceptions/base.py`
- File: `php/src/Http/HttpClient.php`

**Current Code (Python):**
```python
def __str__(self) -> str:
    parts = [self.message]
    if self.status_code is not None:
        parts.append(f"Status: {self.status_code}")
    if self.details:
        parts.append(f"Details: {self.details}")  # Potential sensitive data
    return " | ".join(parts)
```

**Recommended Fix:**
Add a sanitization method and production mode flag to control detail exposure.

**Impact:**
- Prevent accidental sensitive data leakage
- Maintain debugging capability in development
- Comply with security best practices

---

## Issue 4: Low - Basic User-Agent Header

**Title:** [SECURITY] Implement more descriptive User-Agent header

**Labels:** `security`, `enhancement`, `low`

**Description:**
The current User-Agent header is basic and doesn't include version information or other identifying details that could be useful for API monitoring and security.

**Current Headers:**
```python
'User-Agent': 'RocketReach-Python-SDK/1.0.0'
```

**Recommended Enhancement:**
```python
import platform
'User-Agent': f'RocketReach-Python-SDK/{VERSION} ({platform.system()} {platform.release()}; Python {platform.python_version()})'
```

**Benefits:**
- Better API usage analytics
- Easier debugging and support
- Standard practice for HTTP clients

---

## Issue 5: Medium - Timeout Configuration Security

**Title:** [SECURITY] Make timeout configurations environment-appropriate

**Labels:** `security`, `configuration`, `medium`

**Description:**
Fixed timeout values may not be appropriate for all environments and could lead to either security vulnerabilities (too long) or availability issues (too short).

**Current Implementation:**
```python
DEFAULT_TIMEOUT = 30
```

**Recommended Enhancement:**
- Add environment-based timeout configuration
- Implement minimum and maximum timeout bounds
- Add documentation on security implications of timeout values

**Security Implications:**
- Long timeouts can facilitate DoS attacks
- Short timeouts can cause legitimate requests to fail
- Different environments need different timeout strategies