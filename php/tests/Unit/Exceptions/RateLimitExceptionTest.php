<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Exceptions;

use RocketReach\SDK\Exceptions\RateLimitException;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for RateLimitException
 */
class RateLimitExceptionTest extends TestCase
{
    public function testConstructorWithDefaultValues(): void
    {
        $exception = new RateLimitException();
        
        $this->assertInstanceOf(RateLimitException::class, $exception);
        $this->assertEquals('Rate limit exceeded', $exception->getMessage());
        $this->assertEquals(429, $exception->getCode());
        $this->assertEquals(60, $exception->getRetryAfter());
    }

    public function testConstructorWithCustomValues(): void
    {
        $message = 'Custom rate limit message';
        $code = 429;
        $previous = new \Exception('Previous exception');
        $retryAfter = 120;
        
        $exception = new RateLimitException($message, $code, $previous, $retryAfter);
        
        $this->assertEquals($message, $exception->getMessage());
        $this->assertEquals($code, $exception->getCode());
        $this->assertSame($previous, $exception->getPrevious());
        $this->assertEquals($retryAfter, $exception->getRetryAfter());
    }

    public function testGetRetryAfter(): void
    {
        $retryAfter = 300;
        $exception = new RateLimitException('Rate limit exceeded', 429, null, $retryAfter);
        
        $this->assertEquals($retryAfter, $exception->getRetryAfter());
    }

    public function testInheritance(): void
    {
        $exception = new RateLimitException();
        
        $this->assertInstanceOf(\RocketReach\SDK\Exceptions\ApiException::class, $exception);
    }
}
