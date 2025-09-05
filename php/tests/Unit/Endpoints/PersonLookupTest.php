<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Endpoints;

use RocketReach\SDK\Endpoints\PersonLookup;
use RocketReach\SDK\Http\HttpClient;
use RocketReach\SDK\Models\PersonResponse;
use RocketReach\SDK\Tests\Fixtures\ApiResponses;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for PersonLookup endpoint
 */
class PersonLookupTest extends TestCase
{
    private HttpClient $mockHttpClient;
    private PersonLookup $personLookup;

    protected function setUp(): void
    {
        parent::setUp();
        $this->mockHttpClient = $this->createMock(HttpClient::class);
        $this->personLookup = new PersonLookup($this->mockHttpClient);
    }

    public function testId(): void
    {
        $id = 12345;
        $result = $this->personLookup->id($id);
        
        $this->assertSame($this->personLookup, $result);
    }

    public function testLinkedinUrl(): void
    {
        $url = 'https://linkedin.com/in/johndoe';
        $result = $this->personLookup->linkedinUrl($url);
        
        $this->assertSame($this->personLookup, $result);
    }

    public function testName(): void
    {
        $name = 'John Doe';
        $result = $this->personLookup->name($name);
        
        $this->assertSame($this->personLookup, $result);
    }

    public function testCurrentEmployer(): void
    {
        $employer = 'Google';
        $result = $this->personLookup->currentEmployer($employer);
        
        $this->assertSame($this->personLookup, $result);
    }

    public function testTitle(): void
    {
        $title = 'Software Engineer';
        $result = $this->personLookup->title($title);
        
        $this->assertSame($this->personLookup, $result);
    }

    public function testEmail(): void
    {
        $email = 'john@example.com';
        $result = $this->personLookup->email($email);
        
        $this->assertSame($this->personLookup, $result);
    }

    public function testNpiNumber(): void
    {
        $npiNumber = 1234567890;
        $result = $this->personLookup->npiNumber($npiNumber);
        
        $this->assertSame($this->personLookup, $result);
    }

    public function testLookup(): void
    {
        $responseData = ApiResponses::getPersonLookupResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->with('/person/lookup', $this->callback(function ($data) {
                return is_array($data);
            }))
            ->willReturn($responseData);

        $result = $this->personLookup->lookup();
        
        $this->assertInstanceOf(PersonResponse::class, $result);
    }

    public function testMethodChaining(): void
    {
        $responseData = ApiResponses::getPersonLookupResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->willReturn($responseData);

        $result = $this->personLookup
            ->name('John Doe')
            ->currentEmployer('Google')
            ->title('Software Engineer')
            ->lookup();
        
        $this->assertInstanceOf(PersonResponse::class, $result);
    }

    public function testLookupWithAllParameters(): void
    {
        $responseData = ApiResponses::getPersonLookupResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->with('/person/lookup', $this->callback(function ($data) {
                return isset($data['id']) &&
                       isset($data['linkedin_url']) &&
                       isset($data['name']) &&
                       isset($data['current_employer']) &&
                       isset($data['title']) &&
                       isset($data['email']) &&
                       isset($data['npi_number']);
            }))
            ->willReturn($responseData);

        $this->personLookup
            ->id(12345)
            ->linkedinUrl('https://linkedin.com/in/johndoe')
            ->name('John Doe')
            ->currentEmployer('Google')
            ->title('Software Engineer')
            ->email('john@example.com')
            ->npiNumber(1234567890)
            ->lookup();
    }

    public function testLookupWithIdOnly(): void
    {
        $responseData = ApiResponses::getPersonLookupResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->with('/person/lookup', ['id' => 12345])
            ->willReturn($responseData);

        $this->personLookup
            ->id(12345)
            ->lookup();
    }

    public function testLookupWithLinkedinUrlOnly(): void
    {
        $responseData = ApiResponses::getPersonLookupResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->with('/person/lookup', ['linkedin_url' => 'https://linkedin.com/in/johndoe'])
            ->willReturn($responseData);

        $this->personLookup
            ->linkedinUrl('https://linkedin.com/in/johndoe')
            ->lookup();
    }
}
