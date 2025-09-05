<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Unit\Models;

use RocketReach\SDK\Models\SearchQuery;
use PHPUnit\Framework\TestCase;

/**
 * Unit tests for SearchQuery
 */
class SearchQueryTest extends TestCase
{
    private SearchQuery $query;

    protected function setUp(): void
    {
        parent::setUp();
        $this->query = new SearchQuery();
    }

    public function testSetName(): void
    {
        $names = ['John Doe', 'Jane Smith'];
        $this->query->setName($names);
        
        $this->assertEquals($names, $this->query->toArray()['name']);
    }

    public function testSetCurrentTitle(): void
    {
        $titles = ['Software Engineer', 'Product Manager'];
        $this->query->setCurrentTitle($titles);
        
        $this->assertEquals($titles, $this->query->toArray()['current_title']);
    }

    public function testSetCurrentEmployer(): void
    {
        $employers = ['Google', 'Microsoft'];
        $this->query->setCurrentEmployer($employers);
        
        $this->assertEquals($employers, $this->query->toArray()['current_employer']);
    }

    public function testSetCurrentEmployerDomain(): void
    {
        $domains = ['google.com', 'microsoft.com'];
        $this->query->setCurrentEmployerDomain($domains);
        
        $this->assertEquals($domains, $this->query->toArray()['current_employer_domain']);
    }

    public function testSetLocation(): void
    {
        $locations = ['San Francisco', 'New York'];
        $this->query->setLocation($locations);
        
        $this->assertEquals($locations, $this->query->toArray()['location']);
    }

    public function testSetLinkedinUrl(): void
    {
        $urls = ['https://linkedin.com/in/johndoe'];
        $this->query->setLinkedinUrl($urls);
        
        $this->assertEquals($urls, $this->query->toArray()['linkedin_url']);
    }

    public function testSetContactMethod(): void
    {
        $methods = ['email', 'phone'];
        $this->query->setContactMethod($methods);
        
        $this->assertEquals($methods, $this->query->toArray()['contact_method']);
    }

    public function testSetIndustry(): void
    {
        $industries = ['Technology', 'Healthcare'];
        $this->query->setIndustry($industries);
        
        $this->assertEquals($industries, $this->query->toArray()['industry']);
    }

    public function testSetCompanySize(): void
    {
        $sizes = ['51-200', '500+'];
        $this->query->setCompanySize($sizes);
        
        $this->assertEquals($sizes, $this->query->toArray()['company_size']);
    }

    public function testSetCompanyFunding(): void
    {
        $funding = ['1000000+', '<50000000'];
        $this->query->setCompanyFunding($funding);
        
        $this->assertEquals($funding, $this->query->toArray()['company_funding']);
    }

    public function testSetCompanyRevenue(): void
    {
        $revenue = ['100M+', '10M-50M'];
        $this->query->setCompanyRevenue($revenue);
        
        $this->assertEquals($revenue, $this->query->toArray()['company_revenue']);
    }

    public function testSetSeniority(): void
    {
        $seniority = ['CXO', 'Vice President'];
        $this->query->setSeniority($seniority);
        
        $this->assertEquals($seniority, $this->query->toArray()['seniority']);
    }

    public function testSetSkills(): void
    {
        $skills = ['Machine Learning', 'Salesforce'];
        $this->query->setSkills($skills);
        
        $this->assertEquals($skills, $this->query->toArray()['skills']);
    }

    public function testSetEducation(): void
    {
        $education = ['Stanford University', 'MIT'];
        $this->query->setEducation($education);
        
        $this->assertEquals($education, $this->query->toArray()['education']);
    }

    public function testSetOrderBy(): void
    {
        $orderBy = 'relevance';
        $this->query->setOrderBy($orderBy);
        
        $this->assertEquals($orderBy, $this->query->toArray()['order_by']);
    }

    public function testSetPage(): void
    {
        $page = 2;
        $this->query->setPage($page);
        
        $this->assertEquals($page, $this->query->toArray()['page']);
    }

    public function testSetPageSize(): void
    {
        $pageSize = 50;
        $this->query->setPageSize($pageSize);
        
        $this->assertEquals($pageSize, $this->query->toArray()['page_size']);
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
            ->setName(['John Doe'])
            ->setCurrentTitle(['Software Engineer'])
            ->setCurrentEmployer(['Google'])
            ->setCurrentEmployerDomain(['google.com'])
            ->setLocation(['San Francisco'])
            ->setLinkedinUrl(['https://linkedin.com/in/johndoe'])
            ->setContactMethod(['email'])
            ->setIndustry(['Technology'])
            ->setCompanySize(['1000+'])
            ->setCompanyFunding(['1000000+'])
            ->setCompanyRevenue(['100M+'])
            ->setSeniority(['Manager'])
            ->setSkills(['PHP'])
            ->setEducation(['Stanford'])
            ->setOrderBy('relevance')
            ->setPage(1)
            ->setPageSize(10);

        $result = $this->query->toArray();
        
        $this->assertArrayHasKey('name', $result);
        $this->assertArrayHasKey('current_title', $result);
        $this->assertArrayHasKey('current_employer', $result);
        $this->assertArrayHasKey('current_employer_domain', $result);
        $this->assertArrayHasKey('location', $result);
        $this->assertArrayHasKey('linkedin_url', $result);
        $this->assertArrayHasKey('contact_method', $result);
        $this->assertArrayHasKey('industry', $result);
        $this->assertArrayHasKey('company_size', $result);
        $this->assertArrayHasKey('company_funding', $result);
        $this->assertArrayHasKey('company_revenue', $result);
        $this->assertArrayHasKey('seniority', $result);
        $this->assertArrayHasKey('skills', $result);
        $this->assertArrayHasKey('education', $result);
        $this->assertArrayHasKey('order_by', $result);
        $this->assertArrayHasKey('page', $result);
        $this->assertArrayHasKey('page_size', $result);
    }

    public function testMethodChaining(): void
    {
        $result = $this->query
            ->setName(['John Doe'])
            ->setCurrentEmployer(['Google'])
            ->setPage(1)
            ->toArray();
        
        $this->assertArrayHasKey('name', $result);
        $this->assertArrayHasKey('current_employer', $result);
        $this->assertArrayHasKey('page', $result);
    }
}
