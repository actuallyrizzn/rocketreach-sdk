<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Models;

use RocketReach\SDK\Models\SearchResponse;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for SearchResponse
 */
class SearchResponseTest extends TestCase
{
    public function testConstructorWithValidData(): void
    {
        $data = [
            'profiles' => [
                ['id' => 1, 'name' => 'John Doe'],
                ['id' => 2, 'name' => 'Jane Smith']
            ],
            'pagination' => [
                'start' => 1,
                'next' => 2,
                'total' => 10
            ]
        ];
        
        $response = new SearchResponse($data);
        
        $this->assertEquals($data['profiles'], $response->getProfiles());
        $this->assertEquals($data['pagination'], $response->getPagination());
    }

    public function testConstructorWithEmptyData(): void
    {
        $response = new SearchResponse([]);
        
        $this->assertEquals([], $response->getProfiles());
        $this->assertEquals([], $response->getPagination());
    }

    public function testGetProfiles(): void
    {
        $profiles = [
            ['id' => 1, 'name' => 'John Doe'],
            ['id' => 2, 'name' => 'Jane Smith']
        ];
        
        $response = new SearchResponse(['profiles' => $profiles]);
        
        $this->assertEquals($profiles, $response->getProfiles());
    }

    public function testGetPagination(): void
    {
        $pagination = [
            'start' => 1,
            'next' => 2,
            'total' => 10
        ];
        
        $response = new SearchResponse(['pagination' => $pagination]);
        
        $this->assertEquals($pagination, $response->getPagination());
    }

    public function testGetTotal(): void
    {
        $response = new SearchResponse(['pagination' => ['total' => 25]]);
        
        $this->assertEquals(25, $response->getTotal());
    }

    public function testGetTotalWithMissingData(): void
    {
        $response = new SearchResponse([]);
        
        $this->assertEquals(0, $response->getTotal());
    }

    public function testGetCurrentPage(): void
    {
        $response = new SearchResponse(['pagination' => ['start' => 3]]);
        
        $this->assertEquals(3, $response->getCurrentPage());
    }

    public function testGetCurrentPageWithMissingData(): void
    {
        $response = new SearchResponse([]);
        
        $this->assertEquals(1, $response->getCurrentPage());
    }

    public function testGetNextPage(): void
    {
        $response = new SearchResponse(['pagination' => ['next' => 2]]);
        
        $this->assertEquals(2, $response->getNextPage());
    }

    public function testGetNextPageWithNull(): void
    {
        $response = new SearchResponse(['pagination' => ['next' => null]]);
        
        $this->assertNull($response->getNextPage());
    }

    public function testGetNextPageWithMissingData(): void
    {
        $response = new SearchResponse([]);
        
        $this->assertNull($response->getNextPage());
    }

    public function testHasNextPage(): void
    {
        $response = new SearchResponse(['pagination' => ['next' => 2]]);
        
        $this->assertTrue($response->hasNextPage());
    }

    public function testHasNextPageWithNull(): void
    {
        $response = new SearchResponse(['pagination' => ['next' => null]]);
        
        $this->assertFalse($response->hasNextPage());
    }

    public function testGetCount(): void
    {
        $profiles = [
            ['id' => 1, 'name' => 'John Doe'],
            ['id' => 2, 'name' => 'Jane Smith'],
            ['id' => 3, 'name' => 'Bob Johnson']
        ];
        
        $response = new SearchResponse(['profiles' => $profiles]);
        
        $this->assertEquals(3, $response->getCount());
    }

    public function testGetCountWithEmptyProfiles(): void
    {
        $response = new SearchResponse(['profiles' => []]);
        
        $this->assertEquals(0, $response->getCount());
    }

    public function testIsEmpty(): void
    {
        $response = new SearchResponse(['profiles' => []]);
        
        $this->assertTrue($response->isEmpty());
    }

    public function testIsEmptyWithProfiles(): void
    {
        $response = new SearchResponse(['profiles' => [['id' => 1, 'name' => 'John Doe']]]);
        
        $this->assertFalse($response->isEmpty());
    }
}
