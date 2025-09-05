<?php

declare(strict_types=1);

namespace RocketReach\SDK\Tests\Fixtures;

/**
 * API Response fixtures for testing
 */
class ApiResponses
{
    public static function getSearchResponse(): array
    {
        return [
            'profiles' => [
                [
                    'id' => 12345,
                    'name' => 'John Doe',
                    'current_title' => 'Software Engineer',
                    'current_employer' => 'Google',
                    'linkedin_url' => 'https://www.linkedin.com/in/johndoe',
                    'location' => 'San Francisco, CA'
                ],
                [
                    'id' => 67890,
                    'name' => 'Jane Smith',
                    'current_title' => 'Software Engineer',
                    'current_employer' => 'Facebook',
                    'linkedin_url' => 'https://www.linkedin.com/in/janesmith',
                    'location' => 'Palo Alto, CA'
                ]
            ],
            'pagination' => [
                'start' => 1,
                'next' => null,
                'total' => 2
            ]
        ];
    }

    public static function getPersonLookupResponse(): array
    {
        return [
            'id' => 12345,
            'status' => 'complete',
            'name' => 'John Doe',
            'current_title' => 'Software Engineer',
            'current_employer' => 'Google',
            'linkedin_url' => 'https://www.linkedin.com/in/johndoe',
            'emails' => [
                [
                    'email' => 'john.doe@google.com',
                    'type' => 'professional',
                    'grade' => 'A',
                    'last_validation_check' => '2024-02-01'
                ],
                [
                    'email' => 'johndoe@gmail.com',
                    'type' => 'personal',
                    'grade' => 'A',
                    'last_validation_check' => '2024-02-01'
                ]
            ],
            'phones' => [
                [
                    'number' => '+1-555-123-4567',
                    'type' => 'mobile'
                ]
            ]
        ];
    }

    public static function getPersonEnrichResponse(): array
    {
        return [
            'person' => [
                'id' => 12345,
                'name' => 'John Doe',
                'current_title' => 'Software Engineer',
                'current_employer' => 'Google',
                'linkedin_url' => 'https://www.linkedin.com/in/johndoe',
                'emails' => [
                    [
                        'email' => 'john.doe@google.com',
                        'type' => 'professional',
                        'grade' => 'A'
                    ]
                ],
                'phones' => [
                    [
                        'number' => '+1-555-123-4567',
                        'type' => 'mobile'
                    ]
                ]
            ],
            'company' => [
                'id' => 98765,
                'name' => 'Google',
                'domain' => 'google.com',
                'linkedin_url' => 'https://www.linkedin.com/company/google',
                'industry' => 'Internet',
                'employee_count' => '100000+',
                'location' => 'Mountain View, CA, USA'
            ]
        ];
    }

    public static function getErrorResponse(int $statusCode = 400): array
    {
        $messages = [
            400 => 'Bad Request - Invalid parameters',
            401 => 'Unauthorized - Invalid API key',
            403 => 'Forbidden - Access denied',
            404 => 'Not Found - Resource not found',
            429 => 'Too Many Requests - Rate limit exceeded',
            500 => 'Internal Server Error'
        ];

        return [
            'status' => $statusCode,
            'message' => $messages[$statusCode] ?? 'Unknown error'
        ];
    }

    public static function getRateLimitResponse(): array
    {
        return [
            'status' => 429,
            'message' => 'Rate limit exceeded',
            'retry_after' => 60
        ];
    }
}
