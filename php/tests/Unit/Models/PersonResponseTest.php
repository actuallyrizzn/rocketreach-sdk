<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Models;

use RocketReach\SDK\Models\PersonResponse;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for PersonResponse
 */
class PersonResponseTest extends TestCase
{
    public function testConstructorWithValidData(): void
    {
        $data = [
            'id' => 12345,
            'name' => 'John Doe',
            'current_title' => 'Software Engineer',
            'current_employer' => 'Google',
            'linkedin_url' => 'https://linkedin.com/in/johndoe',
            'location' => 'San Francisco, CA',
            'emails' => [
                ['email' => 'john@google.com', 'type' => 'professional']
            ],
            'phones' => [
                ['number' => '+1-555-123-4567', 'type' => 'mobile']
            ],
            'status' => 'complete'
        ];
        
        $response = new PersonResponse($data);
        
        $this->assertEquals(12345, $response->getId());
        $this->assertEquals('John Doe', $response->getName());
        $this->assertEquals('Software Engineer', $response->getCurrentTitle());
        $this->assertEquals('Google', $response->getCurrentEmployer());
        $this->assertEquals('https://linkedin.com/in/johndoe', $response->getLinkedinUrl());
        $this->assertEquals('San Francisco, CA', $response->getLocation());
        $this->assertEquals($data['emails'], $response->getEmails());
        $this->assertEquals($data['phones'], $response->getPhones());
        $this->assertEquals('complete', $response->getStatus());
    }

    public function testGetId(): void
    {
        $response = new PersonResponse(['id' => 12345]);
        
        $this->assertEquals(12345, $response->getId());
    }

    public function testGetIdWithMissingData(): void
    {
        $response = new PersonResponse([]);
        
        $this->assertNull($response->getId());
    }

    public function testGetName(): void
    {
        $response = new PersonResponse(['name' => 'John Doe']);
        
        $this->assertEquals('John Doe', $response->getName());
    }

    public function testGetCurrentTitle(): void
    {
        $response = new PersonResponse(['current_title' => 'Software Engineer']);
        
        $this->assertEquals('Software Engineer', $response->getCurrentTitle());
    }

    public function testGetCurrentEmployer(): void
    {
        $response = new PersonResponse(['current_employer' => 'Google']);
        
        $this->assertEquals('Google', $response->getCurrentEmployer());
    }

    public function testGetLinkedinUrl(): void
    {
        $response = new PersonResponse(['linkedin_url' => 'https://linkedin.com/in/johndoe']);
        
        $this->assertEquals('https://linkedin.com/in/johndoe', $response->getLinkedinUrl());
    }

    public function testGetLocation(): void
    {
        $response = new PersonResponse(['location' => 'San Francisco, CA']);
        
        $this->assertEquals('San Francisco, CA', $response->getLocation());
    }

    public function testGetEmails(): void
    {
        $emails = [
            ['email' => 'john@google.com', 'type' => 'professional'],
            ['email' => 'john@gmail.com', 'type' => 'personal']
        ];
        
        $response = new PersonResponse(['emails' => $emails]);
        
        $this->assertEquals($emails, $response->getEmails());
    }

    public function testGetEmailsWithMissingData(): void
    {
        $response = new PersonResponse([]);
        
        $this->assertEquals([], $response->getEmails());
    }

    public function testGetPhones(): void
    {
        $phones = [
            ['number' => '+1-555-123-4567', 'type' => 'mobile'],
            ['number' => '+1-555-987-6543', 'type' => 'work']
        ];
        
        $response = new PersonResponse(['phones' => $phones]);
        
        $this->assertEquals($phones, $response->getPhones());
    }

    public function testGetPhonesWithMissingData(): void
    {
        $response = new PersonResponse([]);
        
        $this->assertEquals([], $response->getPhones());
    }

    public function testGetStatus(): void
    {
        $response = new PersonResponse(['status' => 'complete']);
        
        $this->assertEquals('complete', $response->getStatus());
    }

    public function testIsComplete(): void
    {
        $response = new PersonResponse(['status' => 'complete']);
        
        $this->assertTrue($response->isComplete());
    }

    public function testIsCompleteWithOtherStatus(): void
    {
        $response = new PersonResponse(['status' => 'searching']);
        
        $this->assertFalse($response->isComplete());
    }

    public function testIsSearching(): void
    {
        $response = new PersonResponse(['status' => 'searching']);
        
        $this->assertTrue($response->isSearching());
    }

    public function testIsSearchingWithOtherStatus(): void
    {
        $response = new PersonResponse(['status' => 'complete']);
        
        $this->assertFalse($response->isSearching());
    }

    public function testToArray(): void
    {
        $data = [
            'id' => 12345,
            'name' => 'John Doe',
            'status' => 'complete'
        ];
        
        $response = new PersonResponse($data);
        
        $this->assertEquals($data, $response->toArray());
    }
}
