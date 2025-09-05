# RocketReach People Data API – Person Lookup & Person Enrich Endpoints
## Person Lookup API (GET /person/lookup)
Description: The Person Lookup API provides person enrichment – given one or more identifiers for an individual (such as name + company, LinkedIn URL, or a RocketReach profile ID), this endpoint returns that person’s verified contact details and profile information[1][2]. It’s commonly used to retrieve emails, phone numbers, job titles, and social profile links for a professional contact based on identifying information[1]. Lookup requests may sometimes be processed asynchronously if data isn’t immediately available – in such cases, the response will indicate a pending status and you may need to check the lookup’s status before getting final results[3][4].
Authentication: Requires your RocketReach API key in the header of the request. Include Api-Key: YOUR_API_KEY in the HTTP headers for every call[5]. (API keys can be obtained from your RocketReach account’s API Settings page.) No other authentication (like OAuth) is needed. Ensure the API key is kept confidential.
Endpoint: GET https://api.rocketreach.co/api/v2/person/lookup
Usage Example (cURL): Lookup a person by full name and company name. In this example, we search for “John Doe” who currently works at Google:
curl --request GET "https://api.rocketreach.co/api/v2/person/lookup" \
     --header "Api-Key: YOUR_API_KEY" \
     --data-urlencode "name=John Doe" \
     --data-urlencode "current_employer=Google"
If a matching profile is found, the API will return the person’s contact details (emails, phones, etc.)[6]. If no profile matches, the response will indicate not found and no lookup credit will be deducted[6].
Parameters: The following query parameters can be provided in the GET request. At least one form of identifier must be supplied to perform a lookup. You can identify a person by a unique ID, a LinkedIn URL, or a name plus company. Additional optional fields can improve matching accuracy.
Notes:
- † Name and Company: When using name, the current_employer is also required. A name by itself is not sufficient – the API needs a company context or another identifier to find a unique match[12][13]. Conversely, don’t supply current_employer alone without a name.
- You can combine multiple parameters for better accuracy. For instance, you might provide name, current_employer, and title together to pinpoint the person. If you have a LinkedIn URL or ID, those alone usually suffice (other fields will be ignored in that case).
- The lookup will deduct 1 lookup credit from your RocketReach account only if contact information is found and returned[14]. Failed lookups (no match) do not consume credits.
Example Response: A successful response returns a JSON object with the person’s profile data. This includes basic professional info and arrays of contact details (emails, phones, social links). For example:
{
  "id": 12345,
  "status": "complete",
  "name": "John Doe",
  "current_title": "Software Engineer",
  "current_employer": "Google",
  "linkedin_url": "https://www.linkedin.com/in/johndoe",
  "emails": [
    {
      "email": "[email protected]",
      "type": "professional",
      "grade": "A",
      "last_validation_check": "2024-02-01"
    },
    {
      "email": "johndoe@gmail.com",
      "type": "personal",
      "grade": "A",
      "last_validation_check": "2024-02-01"
    }
  ],
  "phones": [
    {
      "number": "+1-555-123-4567",
      "type": "mobile"
    }
  ]
}
In this example, the lookup found John Doe’s professional and personal emails (with validity grades), as well as a phone number[15][16]. The status: "complete" indicates the lookup finished successfully. (If the status were "searching", it would mean the lookup is still in progress and you’d need to poll for results later.)
Checking Lookup Status: If a lookup is taking some time (i.e. the initial response has status: "searching"), you can use the People Lookup Status API to check when it completes. This is a separate GET endpoint /person/checkStatus where you provide the id of the lookup job[17]. The status check will return "complete" once the data is ready, at which point you can call the /person/lookup again (with the same parameters or ID) to get the full details.
Error Codes and Responses: The Person Lookup API returns standard HTTP status codes to indicate success or error conditions. Common response codes include:
200 OK – The request was successful. The response body will contain the person data (or a status indicating a search in progress).
400 Bad Request – The request was invalid or missing required parameters. For example, if you only supplied a name without a current_employer, you will get a 400 error indicating a malformed request[18].
401 Unauthorized – Your API key is missing or invalid. The request did not include a proper Api-Key header, or the key is incorrect[19]. Ensure the API key is provided exactly as given by RocketReach.
403 Forbidden – The API key provided is valid but not authorized to use this endpoint. This can happen if your key lacks the necessary permissions or your account has restrictions[20]. (For example, if using an endpoint not included in your plan.)
404 Not Found – No matching person profile was found for the given criteria[21]. This means RocketReach could not identify any profile with the provided name/company or other identifiers. No lookup credit is charged in this case[6].
429 Too Many Requests – You have exceeded the rate limit for API calls[22]. RocketReach imposes rate limits per your plan (e.g. X requests per minute). If this occurs, the response may include a Retry-After header indicating when to retry[23][24]. You should slow down your request rate or upgrade your plan if needed.
500 Internal Server Error – A server-side error occurred at RocketReach[22]. This is uncommon but indicates an unexpected problem with the API. You can retry the request after a brief delay if you encounter a 5xx error.

## Person Enrich API (GET /profile-company/lookup)
Description: The Person Enrich API (also known as the People and Company Lookup API) returns a person’s contact details along with additional company information. It is similar to the standard Person Lookup, but in addition to the individual’s profile it also provides enriched data about their current employer (the company profile) in the same response[25]. This is useful when you need both the person’s info (emails, phones, etc.) and the firmographic details of their company (such as company size, industry, and website) in one call. For example, you can input a person’s name and company, and receive not only that person’s contact info but also the company’s background info in the response.
Authentication: Use your RocketReach API key via the Api-Key header, the same as with the standard lookup. Note: Access to company data through this endpoint may require that your account has Company data credits or an appropriate plan. RocketReach treats company lookups separately from person lookups[26]. If your API key/plan does not include company data (often called “Company Exports”), calls to this endpoint might be rejected with a 403 Forbidden error. Ensure your account has the necessary credits or plan for company enrichment.
Endpoint: GET https://api.rocketreach.co/api/v2/profile-company/lookup
Usage Example (cURL): Enrich a profile by name and company, retrieving both person and company details. For example, looking up John Doe at Google:
curl --request GET "https://api.rocketreach.co/api/v2/profile-company/lookup" \
     --header "Api-Key: YOUR_API_KEY" \
     --data-urlencode "name=John Doe" \
     --data-urlencode "current_employer=Google"
This request will search for John Doe at Google and, if found, return John’s contact info plus information about Google as a company. You could also perform an enrich lookup by other identifiers, such as a LinkedIn URL or RocketReach ID (using linkedin_url or id parameters instead of name/company, similar to the Person Lookup API).
Parameters: The input parameters for the Person Enrich API are the same as those for the Person Lookup endpoint. You must provide at least one identifying factor for the person, and you can use multiple for better accuracy. The following query parameters are accepted:
id (integer, optional): RocketReach person profile ID. If you have a specific profile ID, providing it will retrieve that person’s info and their company data directly.
linkedin_url (string, optional): LinkedIn profile URL of the person. This is an easy way to enrich a profile if you know their LinkedIn – the response will include both person and company details for that profile.
name (string, optional†): Full name of the person to lookup. Must be used with current_employer to pinpoint the person.
current_employer (string, optional†): Company name of the person’s current employer. Required when name is used, to specify which company the person works at.
title (string, optional): Job title of the person, to help disambiguate the person if needed (when used with name/company).
email (string, optional): Email address of the person, to assist in finding the correct profile.
npi_number (integer, optional): NPI number for a healthcare professional, if applicable for the lookup.
(The † notes are the same as for Person Lookup: name and current_employer must be paired.)
These parameters function just like in the Person Lookup API. For example, you can provide a LinkedIn URL alone, or a combination of name and company, etc. The difference is purely in the response content, which will be richer with company info.
Example Response: A successful response from the Enrich endpoint will include both a person object and a company object (or fields) in the JSON. The structure might look like this:
{
  "person": {
    "id": 12345,
    "name": "John Doe",
    "current_title": "Software Engineer",
    "current_employer": "Google",
    "linkedin_url": "https://www.linkedin.com/in/johndoe",
    "emails": [
      { "email": "[email protected]", "type": "professional", "grade": "A" },
      { "email": "johndoe@gmail.com", "type": "personal", "grade": "A" }
    ],
    "phones": [
      { "number": "+1-555-123-4567", "type": "mobile" }
    ],
    // ...other person fields...
  },
  "company": {
    "id": 98765,
    "name": "Google",
    "domain": "google.com",
    "linkedin_url": "https://www.linkedin.com/company/google",
    "industry": "Internet",
    "employee_count": "100000+",
    "location": "Mountain View, CA, USA"
    // ...other company fields...
  }
}
In this example, the person portion contains John Doe’s details (as in a normal lookup), and the company portion contains data about Google. The company data typically includes identifiers and firmographics such as the company’s domain/website, LinkedIn URL, industry category, size (employee count range), headquarters location, etc. By combining these, you get a full picture: for instance, you have John Doe’s contact info and also know the key facts about Google (useful for lead scoring, context, etc.).
How it Works: Under the hood, this endpoint essentially performs a person lookup and then also fetches the company’s profile. It saves you from having to call a separate Company Lookup endpoint. Do note that because of this, an enrich call may consume both a person lookup credit and a company lookup credit from your account (depending on RocketReach’s credit rules). Ensure your account has the necessary credits available.
Error Codes: The Person Enrich endpoint can return the same error codes as the regular lookup, plus errors related to company data access:
400 Bad Request – Missing or invalid parameters (e.g., name without company, etc.), just as with the standard lookup.
401 Unauthorized – API key missing or invalid.
403 Forbidden – Not allowed to use this endpoint. This can happen if your API key does not have company lookup privileges or if you’ve run out of company lookup credits. For example, if you try to enrich company info without a plan that supports it, you may get a 403 error[26].
404 Not Found – The person profile (or company) was not found. If no matching person is found, you’ll get a 404 (and no credits charged). It’s also possible (though less common) to get 404 if the person is found but the associated company profile is not found in RocketReach’s database.
429 Too Many Requests – Rate limit exceeded. This applies similarly – you may have a combined rate limit for lookups/enrich calls.
500 Internal Server Error – A server error on RocketReach’s side.
In general, error handling for Person Enrich is the same as for Person Lookup, with the additional consideration of plan eligibility for company data. Always check the response body for any error message details. For instance, a 403 might come with a message like “Access denied – company data not enabled” (in which case you’d need to contact RocketReach or upgrade your plan).
Using these two endpoints, developers can search for an individual’s contact info and enrich it with company context, enabling robust profile building for sales leads, marketing contacts, or recruiting candidates. Remember to respect RocketReach’s usage policies and rate limits when integrating these into your applications, and store the API responses securely as they contain personal contact data.

[1] [2] [3] [4] [5] [6] [7] [8] [12] [14] [15] [16] [17] [19] [21] [22] How do I Perform a Person Lookup Using the RocketReach API? – RocketReach
https://knowledgebase.rocketreach.co/hc/en-us/articles/33990276843035-How-do-I-Perform-a-Person-Lookup-Using-the-RocketReach-API
[9] [10] [11] rocketreach-client.ts
https://github.com/transitive-bullshit/agentic/blob/767fa7e470134dd5c9c2939ffb946b781a37b4d4/legacy/packages/rocketreach/src/rocketreach-client.ts
[13] lookup profile - Pipedream
https://pipedream.com/apps/rocketreach/actions/lookup-profile
[18] [20] [23] [24] Responses & Errors
https://docs.rocketreach.co/reference/responses-and-errors
[25] People and Company Lookup API
https://docs.rocketreach.co/reference/create_person_and_company_lookup
[26] How do I Lookup Company Information Using the RocketReach API?
https://knowledgebase.rocketreach.co/hc/en-us/articles/33992106567963-How-do-I-Lookup-Company-Information-Using-the-RocketReach-API

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| id | integer | Optional | RocketReach Profile ID of the person. If you already have a RocketReach person id (e.g. from a previous search), you can provide it to retrieve that profile’s details[7]. This alone is sufficient to identify the person. |
| linkedin_url | string | Optional | LinkedIn profile URL of the person[8]. Providing the full URL (e.g. https://www.linkedin.com/in/johndoe) will directly lookup that profile. This is often the most accurate method for lookup. |
| name | string | Optional† | Full name of the person to lookup[5]. This parameter must be used in combination with current_employer (see below) to narrow down the person. |
| current_employer | string | Optional† | Company name of the person’s current employer[5]. Required when using name to ensure the lookup is specific to the right person (e.g. “John Doe” at “Google”). |
| title | string | Optional | Job title of the person. You may include a title to further improve match accuracy when searching by name and company. For example, if multiple people share the name at a company, the title can help identify the correct individual[9]. |
| email | string | Optional | An email address of the person. If you have a known email for the person, you can provide it to assist the lookup[10]. The API will attempt to find a profile matching that email and return enriched contact data. (This can be used alone or alongside other identifiers to improve confidence.) |
| npi_number | integer | Optional | NPI number (National Provider Identifier) for a person, if applicable. This is a unique identifier for US healthcare professionals. If provided, RocketReach will perform a specialized lookup for the medical professional associated with that NPI[11]. |
