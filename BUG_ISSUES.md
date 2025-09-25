# Bug Issues - GitHub Issue Templates

## Issue 6: Critical Bug - Python Query Field Mapping Error

**Title:** [BUG] Critical bug in SearchQuery.to_dict() field name conversion

**Labels:** `bug`, `critical`, `python`

**Description:**
There's a critical bug in the Python SDK where field name conversion does nothing due to incorrect string replacement.

**Location:**
- File: `python/src/rocketreach/sdk/models/queries.py`
- Line: 58

**Current Code:**
```python
# Convert field names to API parameter names
api_name = field_name.replace('_', '_')  # This does nothing!
data[api_name] = value
```

**Impact:**
- **Critical** - Field names are not being converted properly
- May cause API requests to fail
- Could lead to incorrect query parameter formatting

**Recommended Fix:**
```python
# Option 1: Remove if no conversion needed
api_name = field_name
data[api_name] = value

# Option 2: Implement proper conversion if needed
api_name = field_name  # or implement actual conversion logic
data[api_name] = value
```

**Steps to Reproduce:**
1. Create a SearchQuery instance
2. Set any field with underscore
3. Call `to_dict()`
4. Observe that field names are not converted

**Test Case Needed:**
```python
def test_field_name_conversion():
    query = SearchQuery()
    query.set_current_employer(["Google"])
    result = query.to_dict()
    # Verify field names are correct for API
```

---

## Issue 7: Medium Bug - HTTP Status Code Logic Inconsistency

**Title:** [BUG] Inconsistent HTTP status code handling logic

**Labels:** `bug`, `medium`, `python`

**Description:**
The HTTP client has inconsistent logic for handling success status codes. The code checks `!= 201` but the comment suggests 201 should also be success.

**Location:**
- File: `python/src/rocketreach/sdk/http/client.py`
- Line: 167

**Current Code:**
```python
# Handle other HTTP errors (201 is also success)
if not response.ok and response.status_code != 201:
    self._handle_error_response(response)
```

**Issue:**
- `response.ok` already includes 201 as success (2xx range)
- The additional check for 201 is redundant
- Logic is confusing and potentially incorrect

**Recommended Fix:**
```python
# Handle HTTP errors (2xx range is success)
if not response.ok:
    self._handle_error_response(response)
```

**Impact:**
- Potential incorrect error handling
- Code confusion and maintenance issues
- May mask actual API errors

---

## Issue 8: Low Bug - Assumptions About JSON Error Responses

**Title:** [BUG] Error handling assumes JSON format for all error responses

**Labels:** `bug`, `low`, `error-handling`

**Description:**
Both PHP and Python implementations assume error responses are always in JSON format, which may not be true for all API errors (network errors, proxy errors, etc.).

**Location:**
- File: `python/src/rocketreach/sdk/http/client.py`
- File: `php/src/Http/HttpClient.php`

**Current Code (Python):**
```python
def _handle_error_response(self, response: requests.Response) -> None:
    try:
        error_data = response.json()  # May fail for non-JSON responses
        message = error_data.get('message', 'Unknown error')
        details = error_data.get('details', {})
    except ValueError:
        message = response.text or 'Unknown error'
        details = {}
```

**Issue:**
- While there is a try/catch, the error handling could be more robust
- Content-Type header should be checked before attempting JSON parsing
- Different error formats should be handled appropriately

**Recommended Enhancement:**
```python
def _handle_error_response(self, response: requests.Response) -> None:
    content_type = response.headers.get('content-type', '').lower()
    
    if 'application/json' in content_type:
        try:
            error_data = response.json()
            message = error_data.get('message', 'Unknown error')
            details = error_data.get('details', {})
        except ValueError:
            message = response.text or 'Unknown error'
            details = {}
    else:
        message = response.text or f'HTTP {response.status_code} error'
        details = {'content_type': content_type}
```

---

## Issue 9: Medium Bug - Query State Persistence Between Requests

**Title:** [BUG] Query builders maintain state between requests leading to unexpected behavior

**Labels:** `bug`, `medium`, `state-management`

**Description:**
The endpoint query builders maintain state between requests, which can lead to unexpected behavior when reusing the same endpoint instance.

**Location:**
- File: `python/src/rocketreach/sdk/endpoints/people_search.py`
- File: `php/src/Endpoints/PeopleSearch.php`

**Example Problem:**
```python
client = RocketReachClient("api-key")
search = client.people_search()

# First search
search.name(["John Doe"]).search()

# Second search - still has "John Doe" from previous search!
search.current_employer(["Google"]).search()  # Searches for John Doe at Google
```

**Impact:**
- Unexpected search results
- Hard to debug issues
- Poor user experience

**Recommended Solutions:**

1. **Auto-reset after search:**
```python
def search(self) -> SearchResponse:
    query_data = self._query.to_dict()
    # ... make request ...
    self.reset()  # Clear state after search
    return SearchResponse(response_data)
```

2. **Immutable query building:**
```python
def name(self, names: Union[str, List[str]]) -> 'PeopleSearch':
    new_search = copy.deepcopy(self)
    new_search._query.set_name(names)
    return new_search
```

3. **Clear documentation and examples**

---

## Issue 10: Low Bug - Missing Query Parameter Validation

**Title:** [BUG] No validation for query parameters leading to potential API errors

**Labels:** `bug`, `enhancement`, `validation`

**Description:**
The SDK doesn't validate query parameters (like page size limits, valid field values) before sending requests to the API, leading to potential API errors that could be caught earlier.

**Examples of Missing Validation:**
- Page size limits (probably 1-100)
- Page number validation (positive integers)
- Email format validation for lookup queries
- URL format validation for LinkedIn URLs

**Recommended Enhancement:**
```python
def set_page_size(self, page_size: int) -> 'SearchQuery':
    if not isinstance(page_size, int) or page_size < 1 or page_size > 100:
        raise ValueError("Page size must be an integer between 1 and 100")
    self.page_size = page_size
    return self

def set_email(self, email: str) -> 'LookupQuery':
    import re
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        raise ValueError("Invalid email format")
    self.email = email
    return self
```

**Benefits:**
- Better error messages
- Reduced API calls with invalid parameters
- Better user experience
- Faster debugging