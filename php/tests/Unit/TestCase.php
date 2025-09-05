<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit;

use PHPUnit\Framework\TestCase as BaseTestCase;
use RocketReach\SDK\Tests\Fixtures\TestData;

/**
 * Base test case for unit tests
 */
abstract class TestCase extends BaseTestCase
{
    protected function getValidApiKey(): string
    {
        return TestData::getValidApiKey();
    }

    protected function getInvalidApiKey(): string
    {
        return TestData::getInvalidApiKey();
    }

    protected function getTestConfig(): array
    {
        return TestData::getHttpClientConfig();
    }
}
