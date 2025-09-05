<?php

require_once __DIR__ . '/../vendor/autoload.php';

use RocketReach\SDK\RocketReachClient;
use RocketReach\SDK\Exceptions\ApiException;
use RocketReach\SDK\Exceptions\RateLimitException;
use RocketReach\SDK\Exceptions\NetworkException;

// Initialize the client with your API key
$apiKey = '***REMOVED***';
$client = new RocketReachClient($apiKey);

try {
    echo "=== RocketReach PHP SDK Example ===\n\n";

    // Example 1: Search for people
    echo "1. Searching for people at Google...\n";
    $searchResults = $client->peopleSearch()
        ->name(['John Doe'])
        ->currentEmployer(['Google'])
        ->pageSize(5)
        ->search();

    echo "Found {$searchResults->getCount()} profiles\n";
    echo "Total available: {$searchResults->getTotal()}\n\n";

    // Display first few profiles
    foreach (array_slice($searchResults->getProfiles(), 0, 3) as $profile) {
        echo "- {$profile['name']} - {$profile['current_title']} at {$profile['current_employer']}\n";
    }

    // Example 2: Lookup contact details for a specific person
    echo "\n2. Looking up contact details...\n";
    $person = $client->personLookup()
        ->name('John Doe')
        ->currentEmployer('Google')
        ->lookup();

    if ($person->isComplete()) {
        echo "Person found: {$person->getName()}\n";
        echo "Title: {$person->getCurrentTitle()}\n";
        echo "Company: {$person->getCurrentEmployer()}\n";
        
        $emails = $person->getEmails();
        if (!empty($emails)) {
            echo "Emails:\n";
            foreach ($emails as $email) {
                echo "  - {$email['email']} ({$email['type']}, Grade: {$email['grade']})\n";
            }
        }
        
        $phones = $person->getPhones();
        if (!empty($phones)) {
            echo "Phones:\n";
            foreach ($phones as $phone) {
                echo "  - {$phone['number']} ({$phone['type']})\n";
            }
        }
    } else {
        echo "Lookup is still in progress...\n";
    }

    // Example 3: Enrich with company data
    echo "\n3. Enriching with company data...\n";
    $enriched = $client->personEnrich()
        ->name('John Doe')
        ->currentEmployer('Google')
        ->enrich();

    $personData = $enriched->getPerson();
    $companyData = $enriched->getCompany();

    echo "Person: {$enriched->getPersonName()}\n";
    echo "Company: {$enriched->getCompanyName()}\n";
    echo "Industry: {$enriched->getCompanyIndustry()}\n";
    echo "Size: {$enriched->getCompanyEmployeeCount()}\n";
    echo "Location: {$enriched->getCompanyLocation()}\n";

} catch (RateLimitException $e) {
    echo "Rate limit exceeded. Retry after {$e->getRetryAfter()} seconds.\n";
} catch (ApiException $e) {
    echo "API Error ({$e->getCode()}): {$e->getMessage()}\n";
    if ($e->getResponseData()) {
        echo "Response data: " . json_encode($e->getResponseData()) . "\n";
    }
} catch (NetworkException $e) {
    echo "Network Error: {$e->getMessage()}\n";
} catch (Exception $e) {
    echo "Unexpected Error: {$e->getMessage()}\n";
}

echo "\n=== Example Complete ===\n";
