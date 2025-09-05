<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Integration;

use PHPUnit\Framework\TestCase as BaseTestCase;
use RocketReach\SDK\Tests\Fixtures\TestData;

/**
 * Base test case for integration tests
 */
abstract class TestCase extends BaseTestCase
{
    protected function getValidApiKey(): string
    {
        return TestData::getValidApiKey();
    }

    protected function getTestConfig(): array
    {
        return TestData::getHttpClientConfig();
    }
}
