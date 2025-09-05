# RocketReach PHP SDK

A comprehensive PHP SDK for the RocketReach People Search API, providing easy access to search, lookup, and enrich functionality.

## Features

- **People Search** - Search for professional profiles by criteria
- **Person Lookup** - Get contact details for specific individuals
- **Person Enrich** - Get person data plus company information
- **Rate Limiting** - Built-in rate limiting and retry logic
- **Error Handling** - Comprehensive error handling with custom exceptions
- **PSR-12 Compliant** - Follows PHP coding standards

## Installation

```bash
composer require rocketreach/sdk
```

## Quick Start

```php
<?php

use RocketReach\SDK\RocketReachClient;

$client = new RocketReachClient('your-api-key');

// Search for people
$results = $client->peopleSearch()
    ->name(['John Doe'])
    ->currentEmployer(['Google'])
    ->search();

// Lookup contact details
$person = $client->personLookup()
    ->name('John Doe')
    ->currentEmployer('Google')
    ->lookup();

// Enrich with company data
$enriched = $client->personEnrich()
    ->name('John Doe')
    ->currentEmployer('Google')
    ->enrich();
```

## Documentation

- [API Reference](docs/api-reference.md)
- [Examples](examples/)
- [Error Handling](docs/error-handling.md)

## Requirements

- PHP 8.1+
- Guzzle HTTP 7.0+

## License

MIT
