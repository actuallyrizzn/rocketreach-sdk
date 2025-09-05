<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Live;

use PHPUnit\Framework\TestCase as BaseTestCase;
use RocketReach\SDK\Tests\Fixtures\TestData;

/**
 * Base test case for live API tests
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

    protected function setUp(): void
    {
        parent::setUp();
        
        // Skip live tests if API key is not available
        if (empty($this->getValidApiKey()) || $this->getValidApiKey() === 'test-key') {
            $this->markTestSkipped('Live API tests require a valid API key');
        }
    }
}
