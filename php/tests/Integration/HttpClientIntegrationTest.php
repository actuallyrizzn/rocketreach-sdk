<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Integration;

use GuzzleHttp\Client as GuzzleClient;
use RocketReach\SDK\Http\HttpClient;
use RocketReach\SDK\Exceptions\ApiException;
use RocketReach\SDK\Exceptions\RateLimitException;
use RocketReach\SDK\Exceptions\NetworkException;

/**
 * Integration tests for HttpClient
 */
class HttpClientIntegrationTest extends TestCase
{
    private HttpClient $httpClient;

    protected function setUp(): void
    {
        parent::setUp();
        
        $guzzleClient = new GuzzleClient([
            'base_uri' => 'https://httpbin.org/',
            'timeout' => 10
        ]);
        
        $this->httpClient = new HttpClient($guzzleClient);
    }

    public function testGetRequestSuccess(): void
    {
        $response = $this->httpClient->get('/get', ['test' => 'value']);
        
        $this->assertIsArray($response);
        $this->assertArrayHasKey('args', $response);
        $this->assertEquals('value', $response['args']['test']);
    }

    public function testPostRequestSuccess(): void
    {
        $data = ['test' => 'value', 'number' => 123];
        $response = $this->httpClient->post('/post', $data);
        
        $this->assertIsArray($response);
        $this->assertArrayHasKey('json', $response);
        $this->assertEquals($data, $response['json']);
    }

    public function testGetRequestWith404Error(): void
    {
        $this->expectException(ApiException::class);
        
        $this->httpClient->get('/status/404');
    }

    public function testGetRequestWith500Error(): void
    {
        $this->expectException(ApiException::class);
        
        $this->httpClient->get('/status/500');
    }

    public function testGetRequestWithRateLimit(): void
    {
        $this->expectException(RateLimitException::class);
        
        $this->httpClient->get('/status/429');
    }

    public function testGetRequestWithTimeout(): void
    {
        $this->expectException(NetworkException::class);
        
        // This will timeout due to the delay
        $this->httpClient->get('/delay/15');
    }

    public function testRetryMechanism(): void
    {
        // Test that retries work for server errors
        $httpClient = new HttpClient(
            new GuzzleClient(['base_uri' => 'https://httpbin.org/', 'timeout' => 5]),
            2, // Only 2 retries for faster test
            100 // 100ms delay
        );
        
        $this->expectException(ApiException::class);
        
        $httpClient->get('/status/500');
    }
}
