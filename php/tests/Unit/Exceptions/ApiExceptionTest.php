<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Exceptions;

use RocketReach\SDK\Exceptions\ApiException;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for ApiException
 */
class ApiExceptionTest extends TestCase
{
    public function testConstructorWithDefaultValues(): void
    {
        $exception = new ApiException();
        
        $this->assertInstanceOf(ApiException::class, $exception);
        $this->assertEquals('', $exception->getMessage());
        $this->assertEquals(0, $exception->getCode());
        $this->assertNull($exception->getPrevious());
        $this->assertEquals([], $exception->getResponseData());
    }

    public function testConstructorWithCustomValues(): void
    {
        $message = 'Test error message';
        $code = 400;
        $previous = new \Exception('Previous exception');
        $responseData = ['error' => 'details'];
        
        $exception = new ApiException($message, $code, $previous, $responseData);
        
        $this->assertEquals($message, $exception->getMessage());
        $this->assertEquals($code, $exception->getCode());
        $this->assertSame($previous, $exception->getPrevious());
        $this->assertEquals($responseData, $exception->getResponseData());
    }

    public function testIsClientErrorWith4xxCode(): void
    {
        $exception = new ApiException('Bad Request', 400);
        
        $this->assertTrue($exception->isClientError());
        $this->assertFalse($exception->isServerError());
    }

    public function testIsClientErrorWith5xxCode(): void
    {
        $exception = new ApiException('Internal Server Error', 500);
        
        $this->assertFalse($exception->isClientError());
        $this->assertTrue($exception->isServerError());
    }

    public function testIsClientErrorWithOtherCode(): void
    {
        $exception = new ApiException('Other Error', 200);
        
        $this->assertFalse($exception->isClientError());
        $this->assertFalse($exception->isServerError());
    }

    public function testGetResponseData(): void
    {
        $responseData = [
            'status' => 400,
            'message' => 'Bad Request',
            'details' => 'Invalid parameters'
        ];
        
        $exception = new ApiException('Bad Request', 400, null, $responseData);
        
        $this->assertEquals($responseData, $exception->getResponseData());
    }
}
