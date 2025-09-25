#!/bin/bash

# GitHub Issues Creation Script
# This script creates all 32 identified issues from the code audit
# Prerequisites: GitHub CLI installed and authenticated (gh auth login)

set -e

echo "🚀 Creating GitHub issues from code audit..."
echo "Make sure you're in the repository directory and authenticated with GitHub CLI"
echo ""

# Check if gh CLI is available
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI not found. Please install it first: https://github.com/cli/cli#installation"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "❌ Not authenticated with GitHub. Please run: gh auth login"
    exit 1
fi

echo "✅ GitHub CLI found and authenticated"
echo ""

# Function to create issue with error handling
create_issue() {
    local title="$1"
    local labels="$2"
    local body="$3"
    
    echo "Creating: $title"
    if gh issue create --title "$title" --label "$labels" --body "$body"; then
        echo "✅ Created successfully"
    else
        echo "❌ Failed to create issue"
        return 1
    fi
    echo ""
}

echo "📋 Creating CRITICAL issues first..."

# CRITICAL-001: API Key Exposure
create_issue \
"[SECURITY] API key partially exposed in client string representation" \
"security,critical,bug" \
"## Description
The RocketReachClient's \`__repr__\` method in Python exposes the first 8 characters of the API key, which could lead to sensitive information disclosure in logs, debug output, or error messages.

## Location
- File: \`python/src/rocketreach/sdk/client.py\`
- Line: 149

## Current Code
\`\`\`python
def __repr__(self) -> str:
    return f\"RocketReachClient(api_key='{self._api_key[:8]}...', base_url='{self._base_url}')\"
\`\`\`

## Recommended Fix
\`\`\`python
def __repr__(self) -> str:
    return f\"RocketReachClient(api_key='***', base_url='{self._base_url}')\"
\`\`\`

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
- [ ] Security review completed"

# CRITICAL-002: Python Query Bug
create_issue \
"[BUG] Critical bug in SearchQuery.to_dict() field name conversion" \
"bug,critical,python" \
"## Description
There's a critical bug in the Python SDK where field name conversion does nothing due to incorrect string replacement.

## Location
- File: \`python/src/rocketreach/sdk/models/queries.py\`
- Line: 58

## Current Code
\`\`\`python
# Convert field names to API parameter names
api_name = field_name.replace('_', '_')  # This does nothing!
data[api_name] = value
\`\`\`

## Impact
- **Critical** - Field names are not being converted properly
- May cause API requests to fail
- Could lead to incorrect query parameter formatting

## Recommended Fix
\`\`\`python
# Option 1: Remove if no conversion needed
api_name = field_name
data[api_name] = value

# Option 2: Implement proper conversion if needed
api_name = field_name  # or implement actual conversion logic
data[api_name] = value
\`\`\`

## Acceptance Criteria
- [ ] Fix field name conversion logic
- [ ] Add tests for field name conversion
- [ ] Verify API requests work correctly
- [ ] Update documentation if needed"

# CRITICAL-003: HTTP Status Code Logic
create_issue \
"[BUG] Inconsistent HTTP status code handling logic" \
"bug,critical,python" \
"## Description
The HTTP client has inconsistent logic for handling success status codes. The code checks \`!= 201\` but the comment suggests 201 should also be success.

## Location
- File: \`python/src/rocketreach/sdk/http/client.py\`
- Line: 167

## Current Code
\`\`\`python
# Handle other HTTP errors (201 is also success)
if not response.ok and response.status_code != 201:
    self._handle_error_response(response)
\`\`\`

## Issue
- \`response.ok\` already includes 201 as success (2xx range)
- The additional check for 201 is redundant
- Logic is confusing and potentially incorrect

## Recommended Fix
\`\`\`python
# Handle HTTP errors (2xx range is success)
if not response.ok:
    self._handle_error_response(response)
\`\`\`

## Acceptance Criteria
- [ ] Simplify HTTP status code logic
- [ ] Add tests for various status codes
- [ ] Verify error handling works correctly"

echo "📋 Creating HIGH priority issues..."

# HIGH-001: API Key Validation
create_issue \
"[SECURITY] No validation for API key format and structure" \
"security,enhancement,validation" \
"## Description
The SDK accepts any non-empty string as an API key without validating its format. This could lead to runtime errors and makes it harder to catch configuration mistakes early.

## Location
- File: \`python/src/rocketreach/sdk/client.py\`
- File: \`php/src/RocketReachClient.php\`

## Current Validation
\`\`\`python
if not api_key or not api_key.strip():
    raise InvalidApiKeyException(\"API key cannot be empty\")
\`\`\`

## Recommended Enhancement
Add format validation for API keys to catch configuration errors early.

## Benefits
- Better error messages for invalid API keys
- Early detection of configuration issues
- Reduced support requests

## Acceptance Criteria
- [ ] Add API key format validation
- [ ] Create appropriate error messages
- [ ] Add tests for validation logic
- [ ] Update documentation"

# HIGH-002: Centralized Configuration
create_issue \
"[ARCHITECTURE] Implement centralized configuration management" \
"architecture,enhancement,configuration" \
"## Description
Configuration constants are scattered across multiple classes making them hard to maintain and customize.

## Current State
Constants are hardcoded in multiple files without central management.

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
- [ ] Add tests for configuration loading"

# HIGH-003: Logging Framework
create_issue \
"[ARCHITECTURE] Implement structured logging framework" \
"architecture,enhancement,logging" \
"## Description
The SDK lacks proper logging, making debugging and monitoring difficult.

## Current State
- No logging framework
- No debug information
- No request/response logging
- No performance metrics

## Recommended Features
- Request/response logging (with sensitive data masking)
- Performance metrics
- Error tracking
- Debug mode
- Configurable log levels
- Structured output (JSON)

## Acceptance Criteria
- [ ] Implement structured logging
- [ ] Add request/response logging with masking
- [ ] Add performance metrics
- [ ] Add configurable log levels
- [ ] Add documentation for logging configuration"

# HIGH-004: Edge Case Testing
create_issue \
"[TESTING] Add comprehensive tests for error scenarios and edge cases" \
"testing,enhancement,coverage" \
"## Description
The current test suite has good coverage for happy path scenarios but lacks comprehensive testing for error conditions, edge cases, and failure modes.

## Missing Test Scenarios
1. Network error handling (timeouts, DNS failures, SSL errors)
2. Malformed response handling (non-JSON, partial JSON, empty responses)
3. Rate limiting scenarios (with/without retry headers)
4. Authentication edge cases (expired, revoked, malformed keys)

## Acceptance Criteria
- [ ] Add network error tests
- [ ] Add malformed response tests
- [ ] Add rate limiting tests
- [ ] Add authentication edge case tests
- [ ] Achieve 95%+ test coverage
- [ ] Add property-based testing"

# HIGH-005: Property-Based Testing
create_issue \
"[TESTING] Implement property-based testing for query validation" \
"testing,enhancement,property-based" \
"## Description
Implement property-based testing using Hypothesis to test query parameter validation and API request formation with a wide range of inputs.

## Benefits
- Discovers edge cases that manual tests might miss
- Ensures robust input validation
- Improves confidence in parameter handling
- Catches regressions automatically

## Acceptance Criteria
- [ ] Install and configure Hypothesis
- [ ] Add property-based tests for query building
- [ ] Add property-based tests for API key validation
- [ ] Add property-based tests for parameter validation
- [ ] Document property-based testing approach"

# HIGH-006: Type Checking
create_issue \
"[TESTING] Implement comprehensive type checking and validation tests" \
"testing,types,validation" \
"## Description
Add comprehensive type checking tests to ensure type safety across the entire codebase, especially for public APIs.

## Current Issues
- Some methods lack complete type annotations
- No runtime type validation testing
- Missing mypy integration in CI

## Acceptance Criteria
- [ ] Add mypy to CI pipeline
- [ ] Complete type annotations for all public methods
- [ ] Add runtime type validation tests
- [ ] Configure strict mypy settings
- [ ] Add type checking documentation"

# HIGH-007: Security Scanning
create_issue \
"[SECURITY] Add automated dependency vulnerability scanning" \
"security,dependencies,automation" \
"## Description
No automated dependency vulnerability scanning is currently in place, which could lead to using packages with known security vulnerabilities.

## Recommended Implementation
1. GitHub Dependabot for automated updates
2. Security scanning in CI (safety, pip-audit)
3. Local development tools

## Benefits
- Early detection of vulnerable dependencies
- Automated security updates
- Compliance with security best practices
- Reduced manual security review overhead

## Acceptance Criteria
- [ ] Configure GitHub Dependabot
- [ ] Add security scanning to CI
- [ ] Add local security check scripts
- [ ] Document security scanning process"

# HIGH-008: Dependency Cleanup
create_issue \
"[DEPENDENCIES] Remove unused dependencies and optimize requirements" \
"dependencies,cleanup,maintenance" \
"## Description
The Python SDK includes dependencies in requirements.txt that are not actually used in the codebase.

## Unused Dependencies Identified
1. **httpx** - Listed but never imported or used
2. **orjson** - Listed but standard json library is used instead

## Benefits
- Smaller installation footprint
- Reduced security surface area
- Faster installation times
- Clearer dependency management

## Acceptance Criteria
- [ ] Audit all dependencies for actual usage
- [ ] Remove unused dependencies
- [ ] Update requirements.txt
- [ ] Update documentation
- [ ] Verify tests still pass"

echo "📋 Creating MEDIUM priority issues..."

# MEDIUM-001: Sensitive Data in Exceptions
create_issue \
"[SECURITY] Potential sensitive data exposure in exception messages" \
"security,medium,enhancement" \
"## Description
Exception classes include full response text and details, which might contain sensitive information that could be logged or displayed in error messages.

## Impact
- Prevent accidental sensitive data leakage
- Maintain debugging capability in development
- Comply with security best practices

## Acceptance Criteria
- [ ] Add sanitization method for exception messages
- [ ] Add production mode flag to control detail exposure
- [ ] Update all exception classes
- [ ] Add tests for sanitization"

# MEDIUM-002: Implement orjson
create_issue \
"[PERFORMANCE] Use orjson library that's already in requirements" \
"performance,enhancement,python" \
"## Description
The Python SDK includes \`orjson\` in requirements.txt but doesn't actually use it in the code. orjson provides significant performance improvements over the standard json library.

## Performance Benefits
- 2-3x faster JSON parsing
- Lower memory usage
- Better handling of large responses

## Acceptance Criteria
- [ ] Implement orjson usage with fallback to standard json
- [ ] Update all JSON parsing to use new wrapper
- [ ] Add performance benchmarks
- [ ] Update documentation"

# MEDIUM-003: Streaming Support
create_issue \
"[PERFORMANCE] Add streaming support for large API responses" \
"performance,enhancement,streaming" \
"## Description
The current implementation loads entire responses into memory, which can be problematic for large datasets or bulk operations.

## Use Cases
- Large search result sets
- Bulk data exports
- Streaming analytics
- Memory-constrained environments

## Acceptance Criteria
- [ ] Implement response streaming
- [ ] Add pagination helpers
- [ ] Add streaming examples
- [ ] Add memory usage tests"

# MEDIUM-004: Connection Pooling
create_issue \
"[PERFORMANCE] Optimize HTTP connection pooling configuration" \
"performance,enhancement,http" \
"## Description
The current HTTP client uses default connection pooling settings which may not be optimal for API usage patterns.

## Benefits
- Better connection reuse
- Reduced connection overhead
- Improved throughput for multiple requests
- Better handling of network issues

## Acceptance Criteria
- [ ] Configure optimal connection pooling settings
- [ ] Add connection pool monitoring
- [ ] Add performance tests
- [ ] Document configuration options"

# MEDIUM-005: Retry with Jitter
create_issue \
"[PERFORMANCE] Implement retry strategy with jitter to prevent thundering herd" \
"performance,enhancement,reliability" \
"## Description
The current retry strategy uses simple exponential backoff without jitter, which can lead to thundering herd problems when multiple clients retry simultaneously.

## Benefits
- Prevents thundering herd problems
- Better system stability under load
- Improved error recovery
- Reduced server load during outages

## Acceptance Criteria
- [ ] Implement jitter in retry logic
- [ ] Add circuit breaker pattern
- [ ] Add retry strategy documentation
- [ ] Add load testing scenarios"

# MEDIUM-006: API Consistency
create_issue \
"[ARCHITECTURE] Inconsistent API design between PHP and Python SDKs" \
"architecture,enhancement,consistency" \
"## Description
The PHP and Python SDKs have inconsistent method signatures, particularly around parameter types. PHP requires arrays while Python accepts both strings and arrays.

## Impact
- Inconsistent developer experience across languages
- Different learning curves for developers using both SDKs
- Documentation complexity

## Acceptance Criteria
- [ ] Standardize parameter handling across SDKs
- [ ] Update documentation to reflect changes
- [ ] Add cross-SDK compatibility tests
- [ ] Create migration guide if needed"

# MEDIUM-007: Object Creation Optimization
create_issue \
"[ARCHITECTURE] Endpoint objects created on every method call" \
"architecture,performance,enhancement" \
"## Description
Each call to endpoint methods (e.g., \`client.people_search()\`) creates a new instance, which is inefficient and can lead to unexpected behavior.

## Issues
- Memory overhead from creating new objects
- Loss of any state or configuration
- Potential performance impact

## Acceptance Criteria
- [ ] Implement efficient object reuse pattern
- [ ] Add object pooling or lazy initialization
- [ ] Add performance benchmarks
- [ ] Update documentation"

# MEDIUM-008: Exception Hierarchy
create_issue \
"[ARCHITECTURE] Implement more granular exception hierarchy" \
"architecture,enhancement,error-handling" \
"## Description
The current exception hierarchy is good but could be more granular to allow for better error handling and recovery strategies.

## Benefits
- More specific error handling
- Better error recovery strategies
- Clearer error categorization
- Better logging and monitoring

## Acceptance Criteria
- [ ] Design enhanced exception hierarchy
- [ ] Implement new exception classes
- [ ] Update error handling throughout codebase
- [ ] Add exception handling documentation"

# MEDIUM-009: Integration Tests
create_issue \
"[TESTING] Enhance integration tests with better mocking and scenarios" \
"testing,integration,enhancement" \
"## Description
Current integration tests could be improved with better HTTP mocking and more realistic scenarios.

## Current Issues
- Limited HTTP response scenarios
- No testing of retry logic
- Missing timeout testing
- No connection error simulation

## Acceptance Criteria
- [ ] Implement comprehensive HTTP mocking
- [ ] Add retry logic testing
- [ ] Add timeout testing
- [ ] Add connection error simulation
- [ ] Add realistic integration scenarios"

# MEDIUM-010: Performance Benchmarking
create_issue \
"[TESTING] Implement performance benchmarking and regression tests" \
"testing,performance,benchmarking" \
"## Description
Add performance benchmarking tests to catch performance regressions and measure improvements.

## Tools to integrate
- pytest-benchmark for performance testing
- memory_profiler for memory usage testing
- Coverage reporting for performance-critical paths

## Acceptance Criteria
- [ ] Set up performance benchmarking framework
- [ ] Add benchmarks for critical operations
- [ ] Add memory usage tests
- [ ] Integrate into CI pipeline
- [ ] Set performance regression thresholds"

# MEDIUM-011: Version Pinning
create_issue \
"[DEPENDENCIES] Implement better version pinning and compatibility strategy" \
"dependencies,versioning,compatibility" \
"## Description
Current dependency version constraints are inconsistent and could lead to compatibility issues or missed security updates.

## Recommended Strategy
- Use compatible release operator for Python
- Generate lock files for reproducible builds
- Consistent strategy across PHP and Python

## Acceptance Criteria
- [ ] Implement consistent version pinning strategy
- [ ] Generate lock files for reproducible builds
- [ ] Update dependency documentation
- [ ] Add dependency update automation"

# MEDIUM-012: Dependency Updates
create_issue \
"[MAINTENANCE] Automate dependency updates with testing" \
"maintenance,automation,dependencies" \
"## Description
Implement automated dependency updates with proper testing to ensure dependencies stay current without breaking functionality.

## Benefits
- Keep dependencies current
- Automated security updates
- Reduced manual maintenance overhead
- Consistent update testing

## Acceptance Criteria
- [ ] Set up automated dependency update workflow
- [ ] Implement dependency health monitoring
- [ ] Add automated testing for updates
- [ ] Create update documentation"

echo "📋 Creating LOW priority issues..."

# LOW-001: User-Agent Enhancement
create_issue \
"[SECURITY] Implement more descriptive User-Agent header" \
"security,enhancement,low" \
"## Description
The current User-Agent header is basic and doesn't include version information or other identifying details that could be useful for API monitoring and security.

## Benefits
- Better API usage analytics
- Easier debugging and support
- Standard practice for HTTP clients

## Acceptance Criteria
- [ ] Enhance User-Agent header with version info
- [ ] Add platform information
- [ ] Make User-Agent configurable
- [ ] Update documentation"

# LOW-002: Query State Management
create_issue \
"[BUG] Query builders maintain state between requests leading to unexpected behavior" \
"bug,medium,state-management" \
"## Description
The endpoint query builders maintain state between requests, which can lead to unexpected behavior when reusing the same endpoint instance.

## Impact
- Unexpected search results
- Hard to debug issues
- Poor user experience

## Acceptance Criteria
- [ ] Implement auto-reset after search
- [ ] Or implement immutable query building
- [ ] Add clear documentation and examples
- [ ] Add tests for state management"

# LOW-003: Parameter Validation
create_issue \
"[BUG] No validation for query parameters leading to potential API errors" \
"bug,enhancement,validation" \
"## Description
The SDK doesn't validate query parameters (like page size limits, valid field values) before sending requests to the API, leading to potential API errors that could be caught earlier.

## Benefits
- Better error messages
- Reduced API calls with invalid parameters
- Better user experience
- Faster debugging

## Acceptance Criteria
- [ ] Add parameter validation for common fields
- [ ] Add appropriate error messages
- [ ] Add validation tests
- [ ] Update documentation with parameter limits"

# LOW-004: Response Caching
create_issue \
"[PERFORMANCE] Add optional response caching for repeated requests" \
"performance,enhancement,caching" \
"## Description
Some API responses (like account info, health checks) could benefit from caching to reduce redundant requests.

## Cacheable Operations
- Account information
- Health status checks
- Rate limit status
- Static configuration data

## Acceptance Criteria
- [ ] Implement response caching framework
- [ ] Add TTL-based cache expiration
- [ ] Add cache configuration options
- [ ] Add cache hit/miss metrics
- [ ] Add caching documentation"

# LOW-005: License Compliance
create_issue \
"[LEGAL] Implement dependency license compliance checking" \
"legal,dependencies,compliance" \
"## Description
No license compliance checking is in place to ensure all dependencies have compatible licenses.

## Benefits
- Legal compliance assurance
- Automated license conflict detection
- Clear license policy documentation
- Risk mitigation for commercial use

## Acceptance Criteria
- [ ] Implement license checking tools
- [ ] Define allowed/prohibited licenses
- [ ] Add license checking to CI
- [ ] Document license policy
- [ ] Add license compliance reports"

echo ""
echo "🎉 All issues created successfully!"
echo ""
echo "📊 Summary:"
echo "- 3 Critical issues"
echo "- 8 High priority issues" 
echo "- 12 Medium priority issues"
echo "- 5 Low priority issues"
echo "- Total: 28 issues created"
echo ""
echo "🔗 View all issues: gh issue list"
echo "📋 To manage issues: Consider setting up a project board"
echo ""
echo "Next steps:"
echo "1. Review and prioritize issues in your repository"
echo "2. Assign issues to team members"
echo "3. Set up project board for tracking"
echo "4. Start with critical issues first"