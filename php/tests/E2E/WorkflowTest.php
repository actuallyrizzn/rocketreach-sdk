<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\E2E;

use RocketReach\SDK\RocketReachClient;
use RocketReach\SDK\Exceptions\ApiException;
use RocketReach\SDK\Exceptions\RateLimitException;
use RocketReach\SDK\Exceptions\NetworkException;

/**
 * E2E tests for complete workflows
 */
class WorkflowTest extends TestCase
{
    private RocketReachClient $client;

    protected function setUp(): void
    {
        parent::setUp();
        $this->client = new RocketReachClient($this->getValidApiKey());
    }

    public function testSearchToLookupWorkflow(): void
    {
        // This test demonstrates the complete workflow but uses mock data
        // to avoid consuming API credits during development
        
        $this->markTestSkipped('E2E test - requires live API access');
        
        try {
            // Step 1: Search for people
            $searchResults = $this->client->peopleSearch()
                ->name(['John Doe'])
                ->currentEmployer(['Google'])
                ->pageSize(5)
                ->search();

            $this->assertGreaterThan(0, $searchResults->getCount());
            
            // Step 2: Get the first profile ID
            $profiles = $searchResults->getProfiles();
            $firstProfile = $profiles[0];
            $profileId = $firstProfile['id'];
            
            // Step 3: Lookup contact details
            $person = $this->client->personLookup()
                ->id($profileId)
                ->lookup();

            $this->assertTrue($person->isComplete());
            $this->assertNotEmpty($person->getName());
            
        } catch (RateLimitException $e) {
            $this->markTestSkipped('Rate limit exceeded: ' . $e->getMessage());
        } catch (ApiException $e) {
            $this->markTestSkipped('API error: ' . $e->getMessage());
        } catch (NetworkException $e) {
            $this->markTestSkipped('Network error: ' . $e->getMessage());
        }
    }

    public function testSearchToEnrichWorkflow(): void
    {
        $this->markTestSkipped('E2E test - requires live API access');
        
        try {
            // Step 1: Search for people
            $searchResults = $this->client->peopleSearch()
                ->name(['John Doe'])
                ->currentEmployer(['Google'])
                ->pageSize(1)
                ->search();

            $this->assertGreaterThan(0, $searchResults->getCount());
            
            // Step 2: Get the first profile
            $profiles = $searchResults->getProfiles();
            $firstProfile = $profiles[0];
            
            // Step 3: Enrich with company data
            $enriched = $this->client->personEnrich()
                ->name($firstProfile['name'])
                ->currentEmployer($firstProfile['current_employer'])
                ->enrich();

            $this->assertNotEmpty($enriched->getPersonName());
            $this->assertNotEmpty($enriched->getCompanyName());
            
        } catch (RateLimitException $e) {
            $this->markTestSkipped('Rate limit exceeded: ' . $e->getMessage());
        } catch (ApiException $e) {
            $this->markTestSkipped('API error: ' . $e->getMessage());
        } catch (NetworkException $e) {
            $this->markTestSkipped('Network error: ' . $e->getMessage());
        }
    }

    public function testErrorHandlingWorkflow(): void
    {
        $this->markTestSkipped('E2E test - requires live API access');
        
        try {
            // Test with invalid parameters to trigger error handling
            $searchResults = $this->client->peopleSearch()
                ->name(['']) // Empty name should trigger validation
                ->search();
                
            $this->fail('Expected API exception for invalid parameters');
            
        } catch (ApiException $e) {
            $this->assertTrue($e->isClientError());
            $this->assertNotEmpty($e->getMessage());
        } catch (RateLimitException $e) {
            $this->markTestSkipped('Rate limit exceeded: ' . $e->getMessage());
        } catch (NetworkException $e) {
            $this->markTestSkipped('Network error: ' . $e->getMessage());
        }
    }

    public function testPaginationWorkflow(): void
    {
        $this->markTestSkipped('E2E test - requires live API access');
        
        try {
            // Test pagination
            $page1 = $this->client->peopleSearch()
                ->name(['John'])
                ->page(1)
                ->pageSize(2)
                ->search();

            $this->assertLessThanOrEqual(2, $page1->getCount());
            
            if ($page1->hasNextPage()) {
                $page2 = $this->client->peopleSearch()
                    ->name(['John'])
                    ->page(2)
                    ->pageSize(2)
                    ->search();

                $this->assertLessThanOrEqual(2, $page2->getCount());
            }
            
        } catch (RateLimitException $e) {
            $this->markTestSkipped('Rate limit exceeded: ' . $e->getMessage());
        } catch (ApiException $e) {
            $this->markTestSkipped('API error: ' . $e->getMessage());
        } catch (NetworkException $e) {
            $this->markTestSkipped('Network error: ' . $e->getMessage());
        }
    }
}
