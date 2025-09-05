<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Endpoints;

use RocketReach\SDK\Endpoints\PersonEnrich;
use RocketReach\SDK\Http\HttpClient;
use RocketReach\SDK\Models\EnrichResponse;
use RocketReach\SDK\Tests\Fixtures\ApiResponses;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for PersonEnrich endpoint
 */
class PersonEnrichTest extends TestCase
{
    private HttpClient $mockHttpClient;
    private PersonEnrich $personEnrich;

    protected function setUp(): void
    {
        parent::setUp();
        $this->mockHttpClient = $this->createMock(HttpClient::class);
        $this->personEnrich = new PersonEnrich($this->mockHttpClient);
    }

    public function testId(): void
    {
        $id = 12345;
        $result = $this->personEnrich->id($id);
        
        $this->assertSame($this->personEnrich, $result);
    }

    public function testLinkedinUrl(): void
    {
        $url = 'https://linkedin.com/in/johndoe';
        $result = $this->personEnrich->linkedinUrl($url);
        
        $this->assertSame($this->personEnrich, $result);
    }

    public function testName(): void
    {
        $name = 'John Doe';
        $result = $this->personEnrich->name($name);
        
        $this->assertSame($this->personEnrich, $result);
    }

    public function testCurrentEmployer(): void
    {
        $employer = 'Google';
        $result = $this->personEnrich->currentEmployer($employer);
        
        $this->assertSame($this->personEnrich, $result);
    }

    public function testTitle(): void
    {
        $title = 'Software Engineer';
        $result = $this->personEnrich->title($title);
        
        $this->assertSame($this->personEnrich, $result);
    }

    public function testEmail(): void
    {
        $email = 'john@example.com';
        $result = $this->personEnrich->email($email);
        
        $this->assertSame($this->personEnrich, $result);
    }

    public function testNpiNumber(): void
    {
        $npiNumber = 1234567890;
        $result = $this->personEnrich->npiNumber($npiNumber);
        
        $this->assertSame($this->personEnrich, $result);
    }

    public function testEnrich(): void
    {
        $responseData = ApiResponses::getPersonEnrichResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->with('/profile-company/lookup', $this->callback(function ($data) {
                return is_array($data);
            }))
            ->willReturn($responseData);

        $result = $this->personEnrich->enrich();
        
        $this->assertInstanceOf(EnrichResponse::class, $result);
    }

    public function testMethodChaining(): void
    {
        $responseData = ApiResponses::getPersonEnrichResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->willReturn($responseData);

        $result = $this->personEnrich
            ->name('John Doe')
            ->currentEmployer('Google')
            ->title('Software Engineer')
            ->enrich();
        
        $this->assertInstanceOf(EnrichResponse::class, $result);
    }

    public function testEnrichWithAllParameters(): void
    {
        $responseData = ApiResponses::getPersonEnrichResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->with('/profile-company/lookup', $this->callback(function ($data) {
                return isset($data['id']) &&
                       isset($data['linkedin_url']) &&
                       isset($data['name']) &&
                       isset($data['current_employer']) &&
                       isset($data['title']) &&
                       isset($data['email']) &&
                       isset($data['npi_number']);
            }))
            ->willReturn($responseData);

        $this->personEnrich
            ->id(12345)
            ->linkedinUrl('https://linkedin.com/in/johndoe')
            ->name('John Doe')
            ->currentEmployer('Google')
            ->title('Software Engineer')
            ->email('john@example.com')
            ->npiNumber(1234567890)
            ->enrich();
    }

    public function testEnrichWithIdOnly(): void
    {
        $responseData = ApiResponses::getPersonEnrichResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->with('/profile-company/lookup', ['id' => 12345])
            ->willReturn($responseData);

        $this->personEnrich
            ->id(12345)
            ->enrich();
    }

    public function testEnrichWithLinkedinUrlOnly(): void
    {
        $responseData = ApiResponses::getPersonEnrichResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('get')
            ->with('/profile-company/lookup', ['linkedin_url' => 'https://linkedin.com/in/johndoe'])
            ->willReturn($responseData);

        $this->personEnrich
            ->linkedinUrl('https://linkedin.com/in/johndoe')
            ->enrich();
    }
}
