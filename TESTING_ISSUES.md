# Testing & Quality Issues - GitHub Issue Templates

## Issue 23: High - Expand Test Coverage for Edge Cases

**Title:** [TESTING] Add comprehensive tests for error scenarios and edge cases

**Labels:** `testing`, `enhancement`, `coverage`

**Description:**
The current test suite has good coverage for happy path scenarios but lacks comprehensive testing for error conditions, edge cases, and failure modes.

**Missing Test Scenarios:**

1. **Network Error Handling:**
```python
def test_connection_timeout():
    """Test behavior when connection times out"""
    
def test_dns_resolution_failure():
    """Test behavior when DNS resolution fails"""
    
def test_ssl_certificate_error():
    """Test behavior with invalid SSL certificates"""
```

2. **Malformed Response Handling:**
```python
def test_non_json_error_response():
    """Test handling of non-JSON error responses"""
    
def test_partial_json_response():
    """Test handling of truncated JSON responses"""
    
def test_empty_response_body():
    """Test handling of empty response bodies"""
```

3. **Rate Limiting Scenarios:**
```python
def test_rate_limit_with_retry_after_header():
    """Test rate limit handling with Retry-After header"""
    
def test_rate_limit_without_retry_after():
    """Test rate limit handling without Retry-After header"""
    
def test_multiple_consecutive_rate_limits():
    """Test behavior with multiple consecutive rate limits"""
```

4. **Authentication Edge Cases:**
```python
def test_expired_api_key():
    """Test behavior with expired API key"""
    
def test_revoked_api_key():
    """Test behavior with revoked API key"""
    
def test_api_key_with_special_characters():
    """Test API key validation with special characters"""
```

**Recommended Test Structure:**
```python
@pytest.mark.parametrize("error_response", [
    {"status_code": 500, "content": "Internal Server Error", "headers": {}},
    {"status_code": 502, "content": "<html>Bad Gateway</html>", "headers": {"content-type": "text/html"}},
    {"status_code": 429, "content": "", "headers": {"retry-after": "60"}},
])
def test_error_response_handling(error_response):
    """Test various error response scenarios"""
```

**Priority:** High - Critical for production reliability

---

## Issue 24: Medium - Add Property-Based Testing

**Title:** [TESTING] Implement property-based testing for query validation

**Labels:** `testing`, `enhancement`, `property-based`

**Description:**
Implement property-based testing using Hypothesis to test query parameter validation and API request formation with a wide range of inputs.

**Recommended Implementation:**
```python
from hypothesis import given, strategies as st
import hypothesis.strategies as st

@given(
    names=st.lists(st.text(min_size=1, max_size=100), min_size=1, max_size=10),
    page=st.integers(min_value=1, max_value=1000),
    page_size=st.integers(min_value=1, max_value=100)
)
def test_search_query_properties(names, page, page_size):
    """Test that SearchQuery handles various input combinations correctly"""
    query = SearchQuery()
    query.set_name(names)
    query.set_page(page)
    query.set_page_size(page_size)
    
    result = query.to_dict()
    
    # Properties that should always hold
    assert result['name'] == names
    assert result['page'] == page
    assert result['page_size'] == page_size
    assert all(isinstance(name, str) for name in result['name'])

@given(st.text())
def test_api_key_validation_properties(api_key):
    """Test API key validation with various string inputs"""
    if api_key.strip():
        # Should not raise exception for non-empty strings
        client = RocketReachClient(api_key)
        assert client.api_key == api_key.strip()
    else:
        # Should raise exception for empty strings
        with pytest.raises(InvalidApiKeyException):
            RocketReachClient(api_key)
```

**Benefits:**
- Discovers edge cases that manual tests might miss
- Ensures robust input validation
- Improves confidence in parameter handling
- Catches regressions automatically

---

## Issue 25: Medium - Implement Integration Test Improvements

**Title:** [TESTING] Enhance integration tests with better mocking and scenarios

**Labels:** `testing`, `integration`, `enhancement`

**Description:**
Current integration tests could be improved with better HTTP mocking and more realistic scenarios.

**Current Issues:**
- Limited HTTP response scenarios
- No testing of retry logic
- Missing timeout testing
- No connection error simulation

**Recommended Enhancements:**

1. **Better HTTP Mocking:**
```python
import responses
from unittest.mock import patch
import time

@responses.activate
def test_retry_logic_with_transient_errors():
    """Test retry behavior with transient network errors"""
    
    # First two requests fail, third succeeds
    responses.add(responses.POST, 
                 "https://api.rocketreach.co/api/v2/person/search",
                 json={"error": "temporary failure"}, 
                 status=500)
    responses.add(responses.POST, 
                 "https://api.rocketreach.co/api/v2/person/search",
                 json={"error": "temporary failure"}, 
                 status=500)
    responses.add(responses.POST, 
                 "https://api.rocketreach.co/api/v2/person/search",
                 json={"results": [], "count": 0}, 
                 status=200)
    
    client = RocketReachClient("test-key")
    result = client.people_search().name(["John Doe"]).search()
    
    assert result.count == 0
    assert len(responses.calls) == 3  # Verify retries happened
```

2. **Timeout Testing:**
```python
@patch('requests.Session.request')
def test_request_timeout_handling(mock_request):
    """Test proper timeout handling"""
    mock_request.side_effect = requests.exceptions.Timeout()
    
    client = RocketReachClient("test-key", timeout=1)
    
    with pytest.raises(NetworkException, match="timeout"):
        client.people_search().name(["John Doe"]).search()
```

3. **Real API Integration Tests:**
```python
@pytest.mark.live
@pytest.mark.skipif(not os.getenv("ROCKETREACH_API_KEY"), 
                   reason="Live API key not available")
def test_live_api_integration():
    """Test against real API with live credentials"""
    client = RocketReachClient(os.getenv("ROCKETREACH_API_KEY"))
    
    # Test with known good query
    result = client.get_health_status()
    assert "status" in result
```

---

## Issue 26: Low - Add Performance Benchmarking Tests

**Title:** [TESTING] Implement performance benchmarking and regression tests

**Labels:** `testing`, `performance`, `benchmarking`

**Description:**
Add performance benchmarking tests to catch performance regressions and measure improvements.

**Recommended Implementation:**
```python
import pytest
import time
from unittest.mock import Mock

class TestPerformanceBenchmarks:
    
    @pytest.mark.benchmark
    def test_query_building_performance(self, benchmark):
        """Benchmark query building performance"""
        
        def build_complex_query():
            query = SearchQuery()
            query.set_name(["John Doe"] * 100)
            query.set_current_employer(["Google"] * 50)
            query.set_location(["San Francisco"] * 20)
            return query.to_dict()
        
        result = benchmark(build_complex_query)
        assert len(result['name']) == 100
    
    @pytest.mark.benchmark  
    def test_json_serialization_performance(self, benchmark):
        """Benchmark JSON serialization performance"""
        
        large_response = {
            "results": [
                {"name": f"Person {i}", "email": f"person{i}@example.com"}
                for i in range(1000)
            ],
            "count": 1000
        }
        
        def serialize_response():
            return SearchResponse(large_response)
        
        benchmark(serialize_response)
    
    @pytest.mark.performance
    def test_memory_usage_with_large_responses(self):
        """Test memory usage with large API responses"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Simulate large response
        large_data = {"results": [{"name": f"Person {i}"} for i in range(10000)]}
        response = SearchResponse(large_data)
        
        peak_memory = process.memory_info().rss
        memory_increase = peak_memory - initial_memory
        
        # Assert reasonable memory usage (adjust threshold as needed)
        assert memory_increase < 50 * 1024 * 1024  # 50MB limit
```

**Tools to integrate:**
- pytest-benchmark for performance testing
- memory_profiler for memory usage testing
- Coverage reporting for performance-critical paths

---

## Issue 27: High - Add Comprehensive Type Checking Tests

**Title:** [TESTING] Implement comprehensive type checking and validation tests

**Labels:** `testing`, `types`, `validation`

**Description:**
Add comprehensive type checking tests to ensure type safety across the entire codebase, especially for public APIs.

**Current Issues:**
- Some methods lack complete type annotations
- No runtime type validation testing
- Missing mypy integration in CI

**Recommended Implementation:**

1. **Type Checking in CI:**
```yaml
# .github/workflows/test.yml
- name: Type checking with mypy
  run: |
    mypy src/rocketreach --strict
    mypy tests --strict
```

2. **Runtime Type Validation Tests:**
```python
def test_client_initialization_type_validation():
    """Test that client initialization validates types properly"""
    
    # Test invalid API key types
    with pytest.raises(TypeError):
        RocketReachClient(123)  # Integer instead of string
    
    with pytest.raises(TypeError):
        RocketReachClient(None)  # None instead of string
    
    # Test invalid configuration types
    with pytest.raises(TypeError):
        RocketReachClient("valid-key", timeout="30")  # String instead of int

def test_query_parameter_type_validation():
    """Test that query parameters validate types"""
    query = SearchQuery()
    
    # Test invalid types for various parameters
    with pytest.raises(TypeError):
        query.set_page("1")  # String instead of int
    
    with pytest.raises(TypeError):
        query.set_page_size(10.5)  # Float instead of int
```

3. **Generic Type Testing:**
```python
from typing import get_type_hints

def test_all_public_methods_have_type_hints():
    """Ensure all public methods have proper type hints"""
    
    for cls in [RocketReachClient, PeopleSearch, PersonLookup, PersonEnrich]:
        for method_name in dir(cls):
            if not method_name.startswith('_'):  # Public methods only
                method = getattr(cls, method_name)
                if callable(method):
                    hints = get_type_hints(method)
                    assert 'return' in hints, f"{cls.__name__}.{method_name} missing return type"
```

**mypy Configuration:**
```ini
# mypy.ini
[mypy]
python_version = 3.8
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
```

**Priority:** High - Type safety is critical for SDK reliability