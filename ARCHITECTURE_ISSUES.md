# Architecture & Design Issues - GitHub Issue Templates

## Issue 11: Medium - Inconsistent Method Signatures Between PHP and Python

**Title:** [ARCHITECTURE] Inconsistent API design between PHP and Python SDKs

**Labels:** `architecture`, `enhancement`, `consistency`

**Description:**
The PHP and Python SDKs have inconsistent method signatures, particularly around parameter types. PHP requires arrays while Python accepts both strings and arrays.

**Examples:**

**Python (flexible):**
```python
search.name("John Doe")  # Single string
search.name(["John Doe", "Jane Smith"])  # Array
```

**PHP (strict):**
```php
$search->name(["John Doe"]);  // Must be array
```

**Impact:**
- Inconsistent developer experience across languages
- Different learning curves for developers using both SDKs
- Documentation complexity

**Recommended Solutions:**

1. **Standardize on flexible approach** (preferred):
```php
public function name($names): self
{
    if (is_string($names)) {
        $names = [$names];
    }
    $this->query->setName($names);
    return $this;
}
```

2. **Or clearly document the differences**
3. **Create conversion utilities**

**Priority:** Medium - affects developer experience but doesn't break functionality

---

## Issue 12: High - Missing Centralized Configuration Management

**Title:** [ARCHITECTURE] Implement centralized configuration management

**Labels:** `architecture`, `enhancement`, `configuration`

**Description:**
Configuration constants are scattered across multiple classes making them hard to maintain and customize.

**Current State:**
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

**Recommended Solution:**
Create centralized configuration classes:

```python
# config.py
@dataclass
class RocketReachConfig:
    base_url: str = "https://api.rocketreach.co/api/v2"
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    max_page_size: int = 100
    min_page_size: int = 1
    user_agent_template: str = "RocketReach-Python-SDK/{version}"
    
    @classmethod
    def from_environment(cls) -> 'RocketReachConfig':
        """Load configuration from environment variables"""
        return cls(
            base_url=os.getenv('ROCKETREACH_BASE_URL', cls.base_url),
            timeout=int(os.getenv('ROCKETREACH_TIMEOUT', cls.timeout)),
            # ... etc
        )
```

**Benefits:**
- Single source of truth for configuration
- Environment-based configuration
- Easier testing with different configs
- Better documentation of configurable options

---

## Issue 13: Medium - Inefficient Object Creation Pattern

**Title:** [ARCHITECTURE] Endpoint objects created on every method call

**Labels:** `architecture`, `performance`, `enhancement`

**Description:**
Each call to endpoint methods (e.g., `client.people_search()`) creates a new instance, which is inefficient and can lead to unexpected behavior.

**Current Implementation:**
```python
def people_search(self) -> PeopleSearch:
    return PeopleSearch(self._http_client)  # New instance every time
```

**Issues:**
- Memory overhead from creating new objects
- Loss of any state or configuration
- Potential performance impact

**Recommended Solutions:**

1. **Lazy initialization with instance reuse:**
```python
def __init__(self, ...):
    # ...
    self._people_search = None

def people_search(self) -> PeopleSearch:
    if self._people_search is None:
        self._people_search = PeopleSearch(self._http_client)
    return self._people_search.reset()  # Reset state but reuse object
```

2. **Factory pattern with object pooling**

3. **Builder pattern that returns new configured instances**

**Priority:** Medium - affects performance and memory usage

---

## Issue 14: Low - Missing Context Manager Usage Promotion

**Title:** [ARCHITECTURE] HTTP client context manager not properly promoted

**Labels:** `architecture`, `documentation`, `best-practices`

**Description:**
The Python HTTP client implements context manager protocol but this isn't promoted in documentation or examples, leading to potential resource leaks.

**Current Usage:**
```python
client = RocketReachClient("api-key")
# ... use client ...
# No explicit cleanup
```

**Recommended Usage:**
```python
with RocketReachClient("api-key") as client:
    results = client.people_search().name(["John Doe"]).search()
# Automatic cleanup
```

**Required Changes:**
1. Implement context manager in main client:
```python
def __enter__(self):
    return self

def __exit__(self, exc_type, exc_val, exc_tb):
    self._http_client.close()
```

2. Update documentation and examples
3. Add deprecation warning for non-context-manager usage

---

## Issue 15: Medium - Exception Hierarchy Could Be More Granular

**Title:** [ARCHITECTURE] Implement more granular exception hierarchy

**Labels:** `architecture`, `enhancement`, `error-handling`

**Description:**
The current exception hierarchy is good but could be more granular to allow for better error handling and recovery strategies.

**Current Hierarchy:**
```
RocketReachException
├── ApiException
├── InvalidApiKeyException
├── RateLimitException
└── NetworkException
```

**Recommended Enhanced Hierarchy:**
```
RocketReachException
├── ConfigurationError
│   ├── InvalidApiKeyException
│   ├── InvalidUrlException
│   └── InvalidTimeoutException
├── RequestError
│   ├── ValidationError
│   ├── AuthenticationError
│   └── AuthorizationError
├── ResponseError
│   ├── ApiException
│   ├── RateLimitException
│   ├── ServerError
│   └── UnexpectedResponseError
└── NetworkError
    ├── TimeoutError
    ├── ConnectionError
    └── DNSError
```

**Benefits:**
- More specific error handling
- Better error recovery strategies
- Clearer error categorization
- Better logging and monitoring

---

## Issue 16: High - Missing Proper Logging Framework

**Title:** [ARCHITECTURE] Implement structured logging framework

**Labels:** `architecture`, `enhancement`, `logging`

**Description:**
The SDK lacks proper logging, making debugging and monitoring difficult.

**Current State:**
- No logging framework
- No debug information
- No request/response logging
- No performance metrics

**Recommended Implementation:**
```python
import logging
import structlog

# Configure structured logging
logger = structlog.get_logger(__name__)

class HttpClient:
    def _make_request(self, method, endpoint, **kwargs):
        logger.info("Making API request", 
                   method=method, 
                   endpoint=endpoint,
                   timeout=self.timeout)
        
        start_time = time.time()
        try:
            response = self.session.request(...)
            duration = time.time() - start_time
            
            logger.info("API request completed",
                       method=method,
                       endpoint=endpoint, 
                       status_code=response.status_code,
                       duration=duration)
                       
        except Exception as e:
            duration = time.time() - start_time
            logger.error("API request failed",
                        method=method,
                        endpoint=endpoint,
                        error=str(e),
                        duration=duration)
            raise
```

**Features to implement:**
- Request/response logging (with sensitive data masking)
- Performance metrics
- Error tracking
- Debug mode
- Configurable log levels
- Structured output (JSON)