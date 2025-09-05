<?php

declare(strict_types=1);

// Set up autoloading
require_once __DIR__ . '/../vendor/autoload.php';

// Set up test environment
if (!defined('TEST_ENV')) {
    define('TEST_ENV', true);
}

// Set up error reporting for tests
error_reporting(E_ALL);
ini_set('display_errors', '1');

// Mock functions for testing
if (!function_exists('usleep')) {
    function usleep(int $microseconds): void
    {
        // Mock usleep for testing
    }
}
