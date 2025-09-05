RocketReach People Search API Reference[1]
Endpoint:
POST https://api.rocketreach.co/api/v2/person/search – Search for professional profiles by criteria (name, title, company, location, etc.). This returns a list of matching profiles, without contact details[1][2].
Authentication:
Include your API key in the request header: Api-Key: YOUR_API_KEY. Also set Content-Type: application/json. All requests and responses use JSON.
Example Request (cURL):[3]
curl --request POST 'https://api.rocketreach.co/api/v2/person/search' \
     --header 'Api-Key: YOUR_API_KEY' \
     --header 'Content-Type: application/json' \
     --data '{
       "query": {
         "name": ["John Doe"],
         "current_employer": ["Google"]
       }
     }'
This example searches for individuals named "John Doe" who currently work at Google[3].
Request Parameters:
- query (object, required): Search filters object. At least one filter field inside query must be provided. The following filter fields are supported (all are optional within query):
- name (array of string, optional) – Full name(s) to match. Supports partial matches and variations by default. Use quotes to force exact name matches (e.g. "\"John Doe\"" for exactly "John Doe")[4]. Multiple names can be provided to search for any of them.
- current_title (array of string, optional) – Current job title(s) to match. Partial titles are matched (e.g. "Engineer" matches "Software Engineer"). Use quotes for exact title matches[4]. You can include multiple titles (profiles matching any of the titles).
- current_employer (array of string, optional) – Current company name(s) to match. Provide one or more employer names. Partial matches are allowed; use quotes for exact company names.
- current_employer_domain (array of string, optional) – Employer website domain(s) to match. Use this to find people at a specific company by its domain (e.g. "example.com" for anyone working at Example.com).
- location (array of string, optional) – Location keyword(s) to match (such as city, state, or country). You can specify an optional radius for a location by appending ::~<distance><unit> to the location string. For example: "\"San Francisco\"::~50mi" will find people within a 50-mile radius of San Francisco[5] (use mi for miles or km for kilometers).
- linkedin_url (array of string, optional) – LinkedIn profile URL(s) to search for. Useful for finding a specific person by LinkedIn URL[6]. (Typically only one URL is used in this filter.)
- contact_method (array of string, optional) – Filter by availability of contact data. Allowed values: "email" and "phone". If provided, the search will only return profiles that have at least the specified contact info (e.g. if "email" is included, only profiles with an email address will be returned). Include both "email" and "phone" to require profiles that have either.
- industry (array of string, optional) – Industry sector(s) of the current employer to match. Accepts industry names or keywords (e.g. "Technology" or "Healthcare"). Profiles whose current company is classified in any of the given industries will be returned.
- company_size (array of string, optional) – Size of the current employer company (number of employees). Accepts ranges or thresholds as strings. Examples: "51-200" (company with 51 to 200 employees), "500+" (500 or more employees). You may also use comparison operators, e.g. "<=50" or ">=1000", to filter by company headcount size.
- company_funding (array of string, optional) – Funding raised by the current employer. Accepts numeric strings with operators or ranges. For example: "1000000+" (company with over $1,000,000 in funding), "<50000000" (under $50,000,000), or "1000000-90000000" (between $1M and $90M in funding)[7].
- company_revenue (array of string, optional) – Annual revenue of the current employer. Similar format to company_funding: can use ranges or comparison strings (e.g. "100M+" for revenue above $100M, or"10M-50M"for $10–50 million). - **seniority** (array of string, optional) – Seniority level of the person’s role. Examples:"CXO","Vice President","Director","Manager", etc. Only profiles with a matching seniority (based on title) will be returned. - **skills** (array of string, optional) – Skills or keywords to match in profiles. This searches the profiles’ skill set or summary for the given keywords (e.g."Machine Learning","Salesforce"). Use this to find people who have specific skills listed. - **education** (array of string, optional) – Education institution name(s) to filter by. Only profiles that attended the specified school(s) (college, university, etc.) will be returned. - **US diversity filters** (various, optional) – Special filters for U.S. diversity attributes (such as demographic information). **Note:** These fields are available only to approved customers and **must be used in combination with at least one other non-diversity filter.** (Contact RocketReach sales for access to diversity filters.) - **Exclusion syntax:** To exclude results containing certain terms, you can prepend a minus sign (-) to a value. Any filter term starting with-will be treated as an exclusion. For example,"current_title": ["Software Engineer", "-Senior"]finds software engineers **excluding** any with "Senior" in their title[8]. (Alternatively, fields support anexclude_<fieldname>` key with an array of terms to exclude[8].)
order_by (string, optional) – Sort order for results. Options are "relevance" (default) and "popularity". "relevance" returns the best matches first, while "popularity" prioritizes profiles who are key decision-makers or executives[9]. If not specified, results are sorted by relevance.
page (integer, optional) – Page number of results to retrieve, for pagination. Defaults to 1 (the first page). Use this to page through large result sets.
page_size (integer, optional) – Number of profiles to return per page. Defaults to 10 results per page. Maximum allowed is 100 profiles per page (any value above 100 will be capped).
Response Example:
A successful response returns a JSON object with a list of profile matches and pagination info. For example:
{
  "profiles": [
    {
      "id": 12345,
      "name": "John Doe",
      "current_title": "Software Engineer",
      "current_employer": "Google",
      "linkedin_url": "https://www.linkedin.com/in/johndoe",
      "location": "San Francisco, CA"
    },
    {
      "id": 67890,
      "name": "Jane Smith",
      "current_title": "Software Engineer",
      "current_employer": "Facebook",
      "linkedin_url": "https://www.linkedin.com/in/janesmith",
      "location": "Palo Alto, CA"
    }
  ],
  "pagination": {
    "start": 1,
    "next": null,
    "total": 2
  }
}
In this example, two profiles were found (John Doe and Jane Smith). The profiles array contains basic profile fields such as id, name, current title, current employer, LinkedIn URL, and location. Note: No emails or phone numbers are included in search results[2]. To get contact details, you must call the Person Lookup API on a specific profile ID from the results. The pagination object indicates this is the first page (start: 1), there is no next page (next: null), and a total of 2 results were available for the query.
Error Codes: The People Search endpoint can return standard API error status codes in its HTTP response. Possible codes include:
- 200 OK: Success – The request succeeded and the response contains data.
- 400 Bad Request: The request was invalid or missing required parameters (e.g. malformed JSON or no query provided)[10].
- 401 Unauthorized: Authentication failed – API key is missing or invalid[11].
- 403 Forbidden: The API key is valid but not authorized to use this endpoint or filter (for example, using a restricted field without permission)[11].
- 404 Not Found: The endpoint or resource was not found. (For instance, an incorrect URL path was used)[12].
- 429 Too Many Requests: Rate limit exceeded – Too many requests have been sent in a short time or daily limit reached[13]. The response will include a Retry-After header indicating how many seconds to wait before retrying.
- 500 Internal Server Error: An unexpected error occurred on the RocketReach server side[14]. This is rare; you can retry after some time if encountered.
Each error response typically includes a JSON body with more details (e.g. an error message). For example, a 401 Unauthorized may return {"status":401, "message":"Invalid API Key"}. When receiving an error, implement proper handling (check the status code and message) in your SDK. Always ensure required parameters are provided and respect rate limits to avoid errors.

[1] [2] [3] [4] [5] [6] [8] [9] How do I Search for People Using the RocketReach API? – RocketReach
https://knowledgebase.rocketreach.co/hc/en-us/articles/33989900093083-How-do-I-Search-for-People-Using-the-RocketReach-API
[7] People Search API
https://docs.rocketreach.co/reference/people-search-api
[10] [11] [12] [13] [14] Responses & Errors
https://docs.rocketreach.co/reference/responses-and-errors