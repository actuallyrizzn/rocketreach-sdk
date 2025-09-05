<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Http;

use GuzzleHttp\ClientInterface;
use GuzzleHttp\Exception\RequestException;
use GuzzleHttp\Psr7\Response;
use GuzzleHttp\Psr7\Stream;
use Psr\Http\Message\RequestInterface;
use RocketReach\SDK\Http\HttpClient;
use RocketReach\SDK\Exceptions\ApiException;
use RocketReach\SDK\Exceptions\RateLimitException;
use RocketReach\SDK\Exceptions\NetworkException;
use RocketReach\SDK\Tests\Unit\TestCase;

/**
 * Unit tests for HttpClient
 */
class HttpClientTest extends TestCase
{
    private ClientInterface $mockGuzzleClient;
    private HttpClient $httpClient;

    protected function setUp(): void
    {
        parent::setUp();
        $this->mockGuzzleClient = $this->createMock(ClientInterface::class);
        $this->httpClient = new HttpClient($this->mockGuzzleClient);
    }

    public function testGetRequestSuccess(): void
    {
        $responseData = ['success' => true, 'data' => 'test'];
        $response = new Response(200, [], json_encode($responseData));
        
        $this->mockGuzzleClient
            ->expects($this->once())
            ->method('request')
            ->with('GET', '/test', ['query' => ['param' => 'value']])
            ->willReturn($response);

        $result = $this->httpClient->get('/test', ['param' => 'value']);
        
        $this->assertEquals($responseData, $result);
    }

    public function testPostRequestSuccess(): void
    {
        $responseData = ['success' => true, 'data' => 'test'];
        $response = new Response(200, [], json_encode($responseData));
        
        $this->mockGuzzleClient
            ->expects($this->once())
            ->method('request')
            ->with('POST', '/test', ['json' => ['data' => 'test']])
            ->willReturn($response);

        $result = $this->httpClient->post('/test', ['data' => 'test']);
        
        $this->assertEquals($responseData, $result);
    }

    public function testGetRequestWithClientError(): void
    {
        $errorData = ['status' => 400, 'message' => 'Bad Request'];
        $response = new Response(400, [], json_encode($errorData));
        $request = $this->createMock(RequestInterface::class);
        
        $exception = new RequestException('Bad Request', $request, $response);
        
        $this->mockGuzzleClient
            ->expects($this->once())
            ->method('request')
            ->willThrowException($exception);

        $this->expectException(ApiException::class);
        $this->expectExceptionMessage('Bad Request');
        
        $this->httpClient->get('/test');
    }

    public function testGetRequestWithServerError(): void
    {
        $errorData = ['status' => 500, 'message' => 'Internal Server Error'];
        $response = new Response(500, [], json_encode($errorData));
        $request = $this->createMock(RequestInterface::class);
        
        $exception = new RequestException('Internal Server Error', $request, $response);
        
        $this->mockGuzzleClient
            ->expects($this->exactly(3))
            ->method('request')
            ->willThrowException($exception);

        $this->expectException(ApiException::class);
        $this->expectExceptionMessage('Internal Server Error');
        
        $this->httpClient->get('/test');
    }

    public function testGetRequestWithRateLimit(): void
    {
        $errorData = ['status' => 429, 'message' => 'Rate limit exceeded'];
        $response = new Response(429, ['Retry-After' => ['60']], json_encode($errorData));
        $request = $this->createMock(RequestInterface::class);
        
        $exception = new RequestException('Rate limit exceeded', $request, $response);
        
        $this->mockGuzzleClient
            ->expects($this->exactly(3))
            ->method('request')
            ->willThrowException($exception);

        $this->expectException(RateLimitException::class);
        $this->expectExceptionMessage('Rate limit exceeded');
        
        $this->httpClient->get('/test');
    }

    public function testGetRequestWithNetworkError(): void
    {
        $exception = new RequestException('Network error');
        
        $this->mockGuzzleClient
            ->expects($this->exactly(3))
            ->method('request')
            ->willThrowException($exception);

        $this->expectException(NetworkException::class);
        $this->expectExceptionMessage('Network request failed after all retries');
        
        $this->httpClient->get('/test');
    }

    public function testGetRequestWithEmptyResponse(): void
    {
        $response = new Response(200, [], '');
        
        $this->mockGuzzleClient
            ->expects($this->once())
            ->method('request')
            ->willReturn($response);

        $result = $this->httpClient->get('/test');
        
        $this->assertEquals([], $result);
    }

    public function testGetRequestWithInvalidJson(): void
    {
        $response = new Response(200, [], 'invalid json');
        
        $this->mockGuzzleClient
            ->expects($this->once())
            ->method('request')
            ->willReturn($response);

        $result = $this->httpClient->get('/test');
        
        $this->assertEquals([], $result);
    }

    public function testRetryAfterHeaderHandling(): void
    {
        $errorData = ['status' => 429, 'message' => 'Rate limit exceeded'];
        $response = new Response(429, ['Retry-After' => ['120']], json_encode($errorData));
        $request = $this->createMock(RequestInterface::class);
        
        $exception = new RequestException('Rate limit exceeded', $request, $response);
        
        $this->mockGuzzleClient
            ->expects($this->exactly(3))
            ->method('request')
            ->willThrowException($exception);

        $this->expectException(RateLimitException::class);
        
        try {
            $this->httpClient->get('/test');
        } catch (RateLimitException $e) {
            $this->assertEquals(120, $e->getRetryAfter());
            throw $e;
        }
    }

    public function testRetryAfterHeaderMissing(): void
    {
        $errorData = ['status' => 429, 'message' => 'Rate limit exceeded'];
        $response = new Response(429, [], json_encode($errorData));
        $request = $this->createMock(RequestInterface::class);
        
        $exception = new RequestException('Rate limit exceeded', $request, $response);
        
        $this->mockGuzzleClient
            ->expects($this->exactly(3))
            ->method('request')
            ->willThrowException($exception);

        $this->expectException(RateLimitException::class);
        
        try {
            $this->httpClient->get('/test');
        } catch (RateLimitException $e) {
            $this->assertEquals(60, $e->getRetryAfter()); // Default value
            throw $e;
        }
    }

    public function testCustomRetryAttempts(): void
    {
        $httpClient = new HttpClient($this->mockGuzzleClient, 2, 1000);
        
        $exception = new RequestException('Network error');
        
        $this->mockGuzzleClient
            ->expects($this->exactly(2))
            ->method('request')
            ->willThrowException($exception);

        $this->expectException(NetworkException::class);
        
        $httpClient->get('/test');
    }
}
