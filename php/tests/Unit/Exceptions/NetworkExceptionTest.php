<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Exceptions;

use RocketReach\SDK\Exceptions\NetworkException;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for NetworkException
 */
class NetworkExceptionTest extends TestCase
{
    public function testConstructorWithDefaultValues(): void
    {
        $exception = new NetworkException();
        
        $this->assertInstanceOf(NetworkException::class, $exception);
        $this->assertEquals('Network error occurred', $exception->getMessage());
        $this->assertEquals(0, $exception->getCode());
        $this->assertNull($exception->getPrevious());
    }

    public function testConstructorWithCustomValues(): void
    {
        $message = 'Custom network error';
        $code = 0;
        $previous = new \Exception('Previous exception');
        
        $exception = new NetworkException($message, $code, $previous);
        
        $this->assertEquals($message, $exception->getMessage());
        $this->assertEquals($code, $exception->getCode());
        $this->assertSame($previous, $exception->getPrevious());
    }

    public function testInheritance(): void
    {
        $exception = new NetworkException();
        
        $this->assertInstanceOf(\RocketReach\SDK\Exceptions\ApiException::class, $exception);
    }
}
