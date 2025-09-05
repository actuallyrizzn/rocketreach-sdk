<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Live;

use RocketReach\SDK\RocketReachClient;
use RocketReach\SDK\Exceptions\ApiException;
use RocketReach\SDK\Exceptions\RateLimitException;
use RocketReach\SDK\Exceptions\NetworkException;

/**
 * Live API tests - use with caution to avoid consuming credits
 */
class ApiTest extends TestCase
{
    private RocketReachClient $client;

    protected function setUp(): void
    {
        parent::setUp();
        $this->client = new RocketReachClient($this->getValidApiKey());
    }

    public function testPeopleSearchWithMinimalQuery(): void
    {
        $this->markTestSkipped('Live API test - uncomment to run with real API');
        
        try {
            $results = $this->client->peopleSearch()
                ->name(['John'])
                ->currentEmployer(['Google'])
                ->pageSize(1)
                ->search();

            $this->assertInstanceOf(\RocketReach\SDK\Models\SearchResponse::class, $results);
            $this->assertGreaterThanOrEqual(0, $results->getCount());
            
        } catch (RateLimitException $e) {
            $this->markTestSkipped('Rate limit exceeded: ' . $e->getMessage());
        } catch (ApiException $e) {
            $this->markTestSkipped('API error: ' . $e->getMessage());
        } catch (NetworkException $e) {
            $this->markTestSkipped('Network error: ' . $e->getMessage());
        }
    }

    public function testPersonLookupWithMinimalQuery(): void
    {
        $this->markTestSkipped('Live API test - uncomment to run with real API');
        
        try {
            $person = $this->client->personLookup()
                ->name('John Doe')
                ->currentEmployer('Google')
                ->lookup();

            $this->assertInstanceOf(\RocketReach\SDK\Models\PersonResponse::class, $person);
            
        } catch (RateLimitException $e) {
            $this->markTestSkipped('Rate limit exceeded: ' . $e->getMessage());
        } catch (ApiException $e) {
            $this->markTestSkipped('API error: ' . $e->getMessage());
        } catch (NetworkException $e) {
            $this->markTestSkipped('Network error: ' . $e->getMessage());
        }
    }

    public function testPersonEnrichWithMinimalQuery(): void
    {
        $this->markTestSkipped('Live API test - uncomment to run with real API');
        
        try {
            $enriched = $this->client->personEnrich()
                ->name('John Doe')
                ->currentEmployer('Google')
                ->enrich();

            $this->assertInstanceOf(\RocketReach\SDK\Models\EnrichResponse::class, $enriched);
            
        } catch (RateLimitException $e) {
            $this->markTestSkipped('Rate limit exceeded: ' . $e->getMessage());
        } catch (ApiException $e) {
            $this->markTestSkipped('API error: ' . $e->getMessage());
        } catch (NetworkException $e) {
            $this->markTestSkipped('Network error: ' . $e->getMessage());
        }
    }

    public function testRateLimitHandling(): void
    {
        $this->markTestSkipped('Live API test - uncomment to run with real API');
        
        try {
            // Make multiple requests quickly to test rate limiting
            for ($i = 0; $i < 5; $i++) {
                $this->client->peopleSearch()
                    ->name(['Test'])
                    ->pageSize(1)
                    ->search();
            }
            
            $this->fail('Expected rate limit exception');
            
        } catch (RateLimitException $e) {
            $this->assertGreaterThan(0, $e->getRetryAfter());
        } catch (ApiException $e) {
            $this->markTestSkipped('API error: ' . $e->getMessage());
        } catch (NetworkException $e) {
            $this->markTestSkipped('Network error: ' . $e->getMessage());
        }
    }

    public function testErrorHandling(): void
    {
        $this->markTestSkipped('Live API test - uncomment to run with real API');
        
        try {
            // Test with invalid API key
            $invalidClient = new RocketReachClient('invalid-key');
            $invalidClient->peopleSearch()->search();
            
            $this->fail('Expected API exception for invalid key');
            
        } catch (ApiException $e) {
            $this->assertEquals(401, $e->getCode());
        } catch (RateLimitException $e) {
            $this->markTestSkipped('Rate limit exceeded: ' . $e->getMessage());
        } catch (NetworkException $e) {
            $this->markTestSkipped('Network error: ' . $e->getMessage());
        }
    }
}
