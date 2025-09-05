<?php

declare(strict_types=1);

namespace RocketReach\SDK\Http;

use GuzzleHttp\ClientInterface;
use GuzzleHttp\Exception\GuzzleException;
use GuzzleHttp\Exception\RequestException;
use Psr\Http\Message\ResponseInterface;
use RocketReach\SDK\Exceptions\ApiException;
use RocketReach\SDK\Exceptions\RateLimitException;
use RocketReach\SDK\Exceptions\NetworkException;

/**
 * HTTP Client wrapper for RocketReach API
 * 
 * Handles HTTP requests with retry logic, rate limiting,
 * and proper error handling.
 */
class HttpClient
{
    private ClientInterface $client;
    private int $retryAttempts;
    private int $retryDelay;

    public function __construct(
        ClientInterface $client,
        int $retryAttempts = 3,
        int $retryDelay = 1000
    ) {
        $this->client = $client;
        $this->retryAttempts = $retryAttempts;
        $this->retryDelay = $retryDelay;
    }

    /**
     * Make a GET request
     *
     * @param string $endpoint
     * @param array $query
     * @return array
     * @throws ApiException
     * @throws RateLimitException
     * @throws NetworkException
     */
    public function get(string $endpoint, array $query = []): array
    {
        return $this->makeRequest('GET', $endpoint, ['query' => $query]);
    }

    /**
     * Make a POST request
     *
     * @param string $endpoint
     * @param array $data
     * @return array
     * @throws ApiException
     * @throws RateLimitException
     * @throws NetworkException
     */
    public function post(string $endpoint, array $data = []): array
    {
        return $this->makeRequest('POST', $endpoint, ['json' => $data]);
    }

    /**
     * Make an HTTP request with retry logic
     *
     * @param string $method
     * @param string $endpoint
     * @param array $options
     * @return array
     * @throws ApiException
     * @throws RateLimitException
     * @throws NetworkException
     */
    private function makeRequest(string $method, string $endpoint, array $options = []): array
    {
        $lastException = null;
        
        for ($attempt = 1; $attempt <= $this->retryAttempts; $attempt++) {
            try {
                $response = $this->client->request($method, $endpoint, $options);
                return $this->handleResponse($response);
            } catch (RequestException $e) {
                $lastException = $e;
                
                if ($e->hasResponse()) {
                    $response = $e->getResponse();
                    $statusCode = $response->getStatusCode();
                    
                    // Don't retry on client errors (4xx) except 429
                    if ($statusCode >= 400 && $statusCode < 500 && $statusCode !== 429) {
                        throw $this->createApiException($e);
                    }
                    
                    // Handle rate limiting
                    if ($statusCode === 429) {
                        $retryAfter = $this->getRetryAfter($response);
                        if ($attempt < $this->retryAttempts) {
                            usleep($retryAfter * 1000000); // Convert to microseconds
                            continue;
                        }
                        throw new RateLimitException(
                            'Rate limit exceeded',
                            $statusCode,
                            $e,
                            $retryAfter
                        );
                    }
                }
                
                // For network errors, retry with exponential backoff
                if ($attempt < $this->retryAttempts) {
                    $delay = $this->retryDelay * pow(2, $attempt - 1);
                    usleep($delay * 1000); // Convert to microseconds
                    continue;
                }
            }
        }
        
        // If we get here, all retries failed
        if ($lastException instanceof RequestException) {
            throw $this->createApiException($lastException);
        }
        
        throw new NetworkException('Network request failed after all retries', 0, $lastException);
    }

    /**
     * Handle HTTP response
     *
     * @param ResponseInterface $response
     * @return array
     * @throws ApiException
     */
    private function handleResponse(ResponseInterface $response): array
    {
        $statusCode = $response->getStatusCode();
        $body = $response->getBody()->getContents();
        $data = json_decode($body, true);
        
        if ($statusCode >= 400) {
            throw new ApiException(
                $data['message'] ?? 'API request failed',
                $statusCode,
                null,
                $data
            );
        }
        
        return $data ?? [];
    }

    /**
     * Create appropriate API exception
     *
     * @param RequestException $e
     * @return ApiException
     */
    private function createApiException(RequestException $e): ApiException
    {
        $statusCode = 0;
        $responseData = [];
        
        if ($e->hasResponse()) {
            $response = $e->getResponse();
            $statusCode = $response->getStatusCode();
            $body = $response->getBody()->getContents();
            $responseData = json_decode($body, true) ?? [];
        }
        
        return new ApiException(
            $responseData['message'] ?? $e->getMessage(),
            $statusCode,
            $e,
            $responseData
        );
    }

    /**
     * Get retry-after header value
     *
     * @param ResponseInterface $response
     * @return int
     */
    private function getRetryAfter(ResponseInterface $response): int
    {
        $retryAfter = $response->getHeader('Retry-After');
        return !empty($retryAfter) ? (int) $retryAfter[0] : 60;
    }
}
