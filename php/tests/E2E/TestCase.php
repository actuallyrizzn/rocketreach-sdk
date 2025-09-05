<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\E2E;

use PHPUnit\Framework\TestCase as BaseTestCase;
use RocketReach\SDK\Tests\Fixtures\TestData;

/**
 * Base test case for E2E tests
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
