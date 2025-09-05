<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Endpoints;

use RocketReach\SDK\Endpoints\PeopleSearch;
use RocketReach\SDK\Http\HttpClient;
use RocketReach\SDK\Models\SearchResponse;
use RocketReach\SDK\Tests\Fixtures\ApiResponses;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for PeopleSearch endpoint
 */
class PeopleSearchTest extends TestCase
{
    private HttpClient $mockHttpClient;
    private PeopleSearch $peopleSearch;

    protected function setUp(): void
    {
        parent::setUp();
        $this->mockHttpClient = $this->createMock(HttpClient::class);
        $this->peopleSearch = new PeopleSearch($this->mockHttpClient);
    }

    public function testName(): void
    {
        $names = ['John Doe', 'Jane Smith'];
        $result = $this->peopleSearch->name($names);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testCurrentTitle(): void
    {
        $titles = ['Software Engineer', 'Product Manager'];
        $result = $this->peopleSearch->currentTitle($titles);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testCurrentEmployer(): void
    {
        $employers = ['Google', 'Microsoft'];
        $result = $this->peopleSearch->currentEmployer($employers);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testCurrentEmployerDomain(): void
    {
        $domains = ['google.com', 'microsoft.com'];
        $result = $this->peopleSearch->currentEmployerDomain($domains);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testLocation(): void
    {
        $locations = ['San Francisco', 'New York'];
        $result = $this->peopleSearch->location($locations);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testLinkedinUrl(): void
    {
        $urls = ['https://linkedin.com/in/johndoe'];
        $result = $this->peopleSearch->linkedinUrl($urls);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testContactMethod(): void
    {
        $methods = ['email', 'phone'];
        $result = $this->peopleSearch->contactMethod($methods);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testIndustry(): void
    {
        $industries = ['Technology', 'Healthcare'];
        $result = $this->peopleSearch->industry($industries);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testCompanySize(): void
    {
        $sizes = ['51-200', '500+'];
        $result = $this->peopleSearch->companySize($sizes);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testCompanyFunding(): void
    {
        $funding = ['1000000+', '<50000000'];
        $result = $this->peopleSearch->companyFunding($funding);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testCompanyRevenue(): void
    {
        $revenue = ['100M+', '10M-50M'];
        $result = $this->peopleSearch->companyRevenue($revenue);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testSeniority(): void
    {
        $seniority = ['CXO', 'Vice President'];
        $result = $this->peopleSearch->seniority($seniority);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testSkills(): void
    {
        $skills = ['Machine Learning', 'Salesforce'];
        $result = $this->peopleSearch->skills($skills);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testEducation(): void
    {
        $education = ['Stanford University', 'MIT'];
        $result = $this->peopleSearch->education($education);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testOrderBy(): void
    {
        $orderBy = 'relevance';
        $result = $this->peopleSearch->orderBy($orderBy);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testPage(): void
    {
        $page = 2;
        $result = $this->peopleSearch->page($page);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testPageSize(): void
    {
        $pageSize = 50;
        $result = $this->peopleSearch->pageSize($pageSize);
        
        $this->assertSame($this->peopleSearch, $result);
    }

    public function testSearch(): void
    {
        $responseData = ApiResponses::getSearchResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('post')
            ->with('/person/search', $this->callback(function ($data) {
                return isset($data['query']) && is_array($data['query']);
            }))
            ->willReturn($responseData);

        $result = $this->peopleSearch->search();
        
        $this->assertInstanceOf(SearchResponse::class, $result);
    }

    public function testMethodChaining(): void
    {
        $responseData = ApiResponses::getSearchResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('post')
            ->willReturn($responseData);

        $result = $this->peopleSearch
            ->name(['John Doe'])
            ->currentEmployer(['Google'])
            ->page(1)
            ->pageSize(10)
            ->search();
        
        $this->assertInstanceOf(SearchResponse::class, $result);
    }

    public function testSearchWithAllParameters(): void
    {
        $responseData = ApiResponses::getSearchResponse();
        
        $this->mockHttpClient
            ->expects($this->once())
            ->method('post')
            ->with('/person/search', $this->callback(function ($data) {
                $query = $data['query'];
                return isset($query['name']) &&
                       isset($query['current_employer']) &&
                       isset($query['current_title']) &&
                       isset($query['location']) &&
                       isset($query['linkedin_url']) &&
                       isset($query['contact_method']) &&
                       isset($query['industry']) &&
                       isset($query['company_size']) &&
                       isset($query['company_funding']) &&
                       isset($query['company_revenue']) &&
                       isset($query['seniority']) &&
                       isset($query['skills']) &&
                       isset($query['education']) &&
                       isset($query['order_by']) &&
                       isset($query['page']) &&
                       isset($query['page_size']);
            }))
            ->willReturn($responseData);

        $this->peopleSearch
            ->name(['John Doe'])
            ->currentEmployer(['Google'])
            ->currentTitle(['Software Engineer'])
            ->location(['San Francisco'])
            ->linkedinUrl(['https://linkedin.com/in/johndoe'])
            ->contactMethod(['email'])
            ->industry(['Technology'])
            ->companySize(['1000+'])
            ->companyFunding(['1000000+'])
            ->companyRevenue(['100M+'])
            ->seniority(['Manager'])
            ->skills(['PHP'])
            ->education(['Stanford'])
            ->orderBy('relevance')
            ->page(1)
            ->pageSize(10)
            ->search();
    }
}
