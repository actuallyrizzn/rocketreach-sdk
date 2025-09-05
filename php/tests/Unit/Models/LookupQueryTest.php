<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Models;

use RocketReach\SDK\Models\LookupQuery;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for LookupQuery
 */
class LookupQueryTest extends TestCase
{
    private LookupQuery $query;

    protected function setUp(): void
    {
        parent::setUp();
        $this->query = new LookupQuery();
    }

    public function testSetId(): void
    {
        $id = 12345;
        $this->query->setId($id);
        
        $this->assertEquals($id, $this->query->toArray()['id']);
    }

    public function testSetLinkedinUrl(): void
    {
        $url = 'https://linkedin.com/in/johndoe';
        $this->query->setLinkedinUrl($url);
        
        $this->assertEquals($url, $this->query->toArray()['linkedin_url']);
    }

    public function testSetName(): void
    {
        $name = 'John Doe';
        $this->query->setName($name);
        
        $this->assertEquals($name, $this->query->toArray()['name']);
    }

    public function testSetCurrentEmployer(): void
    {
        $employer = 'Google';
        $this->query->setCurrentEmployer($employer);
        
        $this->assertEquals($employer, $this->query->toArray()['current_employer']);
    }

    public function testSetTitle(): void
    {
        $title = 'Software Engineer';
        $this->query->setTitle($title);
        
        $this->assertEquals($title, $this->query->toArray()['title']);
    }

    public function testSetEmail(): void
    {
        $email = 'john@example.com';
        $this->query->setEmail($email);
        
        $this->assertEquals($email, $this->query->toArray()['email']);
    }

    public function testSetNpiNumber(): void
    {
        $npiNumber = 1234567890;
        $this->query->setNpiNumber($npiNumber);
        
        $this->assertEquals($npiNumber, $this->query->toArray()['npi_number']);
    }

    public function testToArrayWithEmptyQuery(): void
    {
        $result = $this->query->toArray();
        
        $this->assertIsArray($result);
        $this->assertEmpty($result);
    }

    public function testToArrayWithAllFields(): void
    {
        $this->query
            ->setId(12345)
            ->setLinkedinUrl('https://linkedin.com/in/johndoe')
            ->setName('John Doe')
            ->setCurrentEmployer('Google')
            ->setTitle('Software Engineer')
            ->setEmail('john@example.com')
            ->setNpiNumber(1234567890);

        $result = $this->query->toArray();
        
        $this->assertArrayHasKey('id', $result);
        $this->assertArrayHasKey('linkedin_url', $result);
        $this->assertArrayHasKey('name', $result);
        $this->assertArrayHasKey('current_employer', $result);
        $this->assertArrayHasKey('title', $result);
        $this->assertArrayHasKey('email', $result);
        $this->assertArrayHasKey('npi_number', $result);
    }

    public function testMethodChaining(): void
    {
        $result = $this->query
            ->setName('John Doe')
            ->setCurrentEmployer('Google')
            ->setTitle('Software Engineer')
            ->toArray();
        
        $this->assertArrayHasKey('name', $result);
        $this->assertArrayHasKey('current_employer', $result);
        $this->assertArrayHasKey('title', $result);
    }
}
