<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Exceptions;

use RocketReach\SDK\Exceptions\InvalidApiKeyException;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for InvalidApiKeyException
 */
class InvalidApiKeyExceptionTest extends TestCase
{
    public function testConstructorWithDefaultMessage(): void
    {
        $exception = new InvalidApiKeyException();
        
        $this->assertInstanceOf(InvalidApiKeyException::class, $exception);
        $this->assertEquals('Invalid or missing API key', $exception->getMessage());
        $this->assertEquals(401, $exception->getCode());
    }

    public function testConstructorWithCustomMessage(): void
    {
        $message = 'Custom API key error';
        $exception = new InvalidApiKeyException($message);
        
        $this->assertEquals($message, $exception->getMessage());
        $this->assertEquals(401, $exception->getCode());
    }

    public function testInheritance(): void
    {
        $exception = new InvalidApiKeyException();
        
        $this->assertInstanceOf(\RocketReach\SDK\Exceptions\ApiException::class, $exception);
    }
}
