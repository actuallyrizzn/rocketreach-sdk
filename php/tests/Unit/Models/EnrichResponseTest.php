<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Models;

use RocketReach\SDK\Models\EnrichResponse;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for EnrichResponse
 */
class EnrichResponseTest extends TestCase
{
    public function testConstructorWithValidData(): void
    {
        $data = [
            'person' => [
                'id' => 12345,
                'name' => 'John Doe',
                'emails' => [['email' => 'john@google.com']],
                'phones' => [['number' => '+1-555-123-4567']]
            ],
            'company' => [
                'id' => 98765,
                'name' => 'Google',
                'domain' => 'google.com',
                'industry' => 'Internet',
                'employee_count' => '100000+',
                'location' => 'Mountain View, CA'
            ]
        ];
        
        $response = new EnrichResponse($data);
        
        $this->assertEquals($data['person'], $response->getPerson());
        $this->assertEquals($data['company'], $response->getCompany());
    }

    public function testConstructorWithEmptyData(): void
    {
        $response = new EnrichResponse([]);
        
        $this->assertEquals([], $response->getPerson());
        $this->assertEquals([], $response->getCompany());
    }

    public function testGetPerson(): void
    {
        $person = [
            'id' => 12345,
            'name' => 'John Doe',
            'emails' => [['email' => 'john@google.com']]
        ];
        
        $response = new EnrichResponse(['person' => $person]);
        
        $this->assertEquals($person, $response->getPerson());
    }

    public function testGetCompany(): void
    {
        $company = [
            'id' => 98765,
            'name' => 'Google',
            'domain' => 'google.com'
        ];
        
        $response = new EnrichResponse(['company' => $company]);
        
        $this->assertEquals($company, $response->getCompany());
    }

    public function testGetPersonId(): void
    {
        $response = new EnrichResponse(['person' => ['id' => 12345]]);
        
        $this->assertEquals(12345, $response->getPersonId());
    }

    public function testGetPersonIdWithMissingData(): void
    {
        $response = new EnrichResponse([]);
        
        $this->assertNull($response->getPersonId());
    }

    public function testGetPersonName(): void
    {
        $response = new EnrichResponse(['person' => ['name' => 'John Doe']]);
        
        $this->assertEquals('John Doe', $response->getPersonName());
    }

    public function testGetPersonEmails(): void
    {
        $emails = [
            ['email' => 'john@google.com', 'type' => 'professional'],
            ['email' => 'john@gmail.com', 'type' => 'personal']
        ];
        
        $response = new EnrichResponse(['person' => ['emails' => $emails]]);
        
        $this->assertEquals($emails, $response->getPersonEmails());
    }

    public function testGetPersonEmailsWithMissingData(): void
    {
        $response = new EnrichResponse([]);
        
        $this->assertEquals([], $response->getPersonEmails());
    }

    public function testGetPersonPhones(): void
    {
        $phones = [
            ['number' => '+1-555-123-4567', 'type' => 'mobile']
        ];
        
        $response = new EnrichResponse(['person' => ['phones' => $phones]]);
        
        $this->assertEquals($phones, $response->getPersonPhones());
    }

    public function testGetPersonPhonesWithMissingData(): void
    {
        $response = new EnrichResponse([]);
        
        $this->assertEquals([], $response->getPersonPhones());
    }

    public function testGetCompanyId(): void
    {
        $response = new EnrichResponse(['company' => ['id' => 98765]]);
        
        $this->assertEquals(98765, $response->getCompanyId());
    }

    public function testGetCompanyIdWithMissingData(): void
    {
        $response = new EnrichResponse([]);
        
        $this->assertNull($response->getCompanyId());
    }

    public function testGetCompanyName(): void
    {
        $response = new EnrichResponse(['company' => ['name' => 'Google']]);
        
        $this->assertEquals('Google', $response->getCompanyName());
    }

    public function testGetCompanyDomain(): void
    {
        $response = new EnrichResponse(['company' => ['domain' => 'google.com']]);
        
        $this->assertEquals('google.com', $response->getCompanyDomain());
    }

    public function testGetCompanyIndustry(): void
    {
        $response = new EnrichResponse(['company' => ['industry' => 'Internet']]);
        
        $this->assertEquals('Internet', $response->getCompanyIndustry());
    }

    public function testGetCompanyEmployeeCount(): void
    {
        $response = new EnrichResponse(['company' => ['employee_count' => '100000+']]);
        
        $this->assertEquals('100000+', $response->getCompanyEmployeeCount());
    }

    public function testGetCompanyLocation(): void
    {
        $response = new EnrichResponse(['company' => ['location' => 'Mountain View, CA']]);
        
        $this->assertEquals('Mountain View, CA', $response->getCompanyLocation());
    }

    public function testToArray(): void
    {
        $data = [
            'person' => ['id' => 12345, 'name' => 'John Doe'],
            'company' => ['id' => 98765, 'name' => 'Google']
        ];
        
        $response = new EnrichResponse($data);
        
        $this->assertEquals($data, $response->toArray());
    }
}
