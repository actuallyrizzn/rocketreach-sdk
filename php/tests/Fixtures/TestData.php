<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Fixtures;

/**
 * Test data fixtures
 */
class TestData
{
    public static function getValidApiKey(): string
    {
        return '***REMOVED***';
    }

    public static function getInvalidApiKey(): string
    {
        return '';
    }

    public static function getSearchQueryData(): array
    {
        return [
            'name' => ['John Doe'],
            'current_employer' => ['Google'],
            'current_title' => ['Software Engineer'],
            'location' => ['San Francisco'],
            'page' => 1,
            'page_size' => 10
        ];
    }

    public static function getLookupQueryData(): array
    {
        return [
            'name' => 'John Doe',
            'current_employer' => 'Google',
            'title' => 'Software Engineer'
        ];
    }

    public static function getEnrichQueryData(): array
    {
        return [
            'name' => 'John Doe',
            'current_employer' => 'Google'
        ];
    }

    public static function getHttpClientConfig(): array
    {
        return [
            'base_uri' => 'https://api.rocketreach.co/api/v2',
            'timeout' => 30,
            'headers' => [
                'Api-Key' => self::getValidApiKey(),
                'Content-Type' => 'application/json',
                'User-Agent' => 'RocketReach-PHP-SDK/1.0.0'
            ]
        ];
    }
}
