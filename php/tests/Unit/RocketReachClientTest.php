<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit;

use GuzzleHttp\Client as GuzzleClient;
use GuzzleHttp\ClientInterface;
use RocketReach\SDK\RocketReachClient;
use RocketReach\SDK\Exceptions\InvalidApiKeyException;
use RocketReach\SDK\Endpoints\PeopleSearch;
use RocketReach\SDK\Endpoints\PersonLookup;
use RocketReach\SDK\Endpoints\PersonEnrich;
use RocketReach\SDK\Http\HttpClient;

/**
 * Unit tests for RocketReachClient
 */
class RocketReachClientTest extends TestCase
{
    public function testConstructorWithValidApiKey(): void
    {
        $client = new RocketReachClient($this->getValidApiKey());
        
        $this->assertInstanceOf(RocketReachClient::class, $client);
        $this->assertEquals($this->getValidApiKey(), $client->getApiKey());
    }

    public function testConstructorWithEmptyApiKey(): void
    {
        $this->expectException(InvalidApiKeyException::class);
        $this->expectExceptionMessage('API key cannot be empty');
        
        new RocketReachClient('');
    }

    public function testConstructorWithCustomHttpClient(): void
    {
        $httpClient = $this->createMock(ClientInterface::class);
        $client = new RocketReachClient($this->getValidApiKey(), $httpClient);
        
        $this->assertInstanceOf(RocketReachClient::class, $client);
    }

    public function testConstructorWithCustomConfig(): void
    {
        $config = [
            'timeout' => 60,
            'custom_header' => 'custom_value'
        ];
        
        $client = new RocketReachClient($this->getValidApiKey(), null, $config);
        
        $this->assertInstanceOf(RocketReachClient::class, $client);
    }

    public function testPeopleSearchReturnsPeopleSearchInstance(): void
    {
        $client = new RocketReachClient($this->getValidApiKey());
        $peopleSearch = $client->peopleSearch();
        
        $this->assertInstanceOf(PeopleSearch::class, $peopleSearch);
    }

    public function testPersonLookupReturnsPersonLookupInstance(): void
    {
        $client = new RocketReachClient($this->getValidApiKey());
        $personLookup = $client->personLookup();
        
        $this->assertInstanceOf(PersonLookup::class, $personLookup);
    }

    public function testPersonEnrichReturnsPersonEnrichInstance(): void
    {
        $client = new RocketReachClient($this->getValidApiKey());
        $personEnrich = $client->personEnrich();
        
        $this->assertInstanceOf(PersonEnrich::class, $personEnrich);
    }

    public function testGetHttpClientReturnsHttpClientInstance(): void
    {
        $client = new RocketReachClient($this->getValidApiKey());
        $httpClient = $client->getHttpClient();
        
        $this->assertInstanceOf(HttpClient::class, $httpClient);
    }

    public function testGetApiKeyReturnsCorrectApiKey(): void
    {
        $apiKey = $this->getValidApiKey();
        $client = new RocketReachClient($apiKey);
        
        $this->assertEquals($apiKey, $client->getApiKey());
    }

    public function testMultipleEndpointInstancesAreDifferent(): void
    {
        $client = new RocketReachClient($this->getValidApiKey());
        
        $search1 = $client->peopleSearch();
        $search2 = $client->peopleSearch();
        
        $this->assertNotSame($search1, $search2);
    }

    public function testDefaultConfigurationValues(): void
    {
        $client = new RocketReachClient($this->getValidApiKey());
        
        // Test that client can be created without errors
        $this->assertInstanceOf(RocketReachClient::class, $client);
        
        // Test that endpoints can be created
        $this->assertInstanceOf(PeopleSearch::class, $client->peopleSearch());
        $this->assertInstanceOf(PersonLookup::class, $client->personLookup());
        $this->assertInstanceOf(PersonEnrich::class, $client->personEnrich());
    }
}
