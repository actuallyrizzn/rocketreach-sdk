#!/usr/bin/env python3
"""
Basic Usage Example

This example demonstrates how to use the RocketReach Python SDK
for common operations.
"""

from rocketreach import RocketReachClient


def main():
    """Main example function."""
    
    # Initialize the client
    client = RocketReachClient("your-api-key-here")
    
    print("=== RocketReach Python SDK Basic Usage ===\n")
    
    # Example 1: People Search
    print("1. People Search Example:")
    try:
        search_results = (client.people_search()
                         .name(["John Doe"])
                         .current_employer(["Google"])
                         .location(["San Francisco"])
                         .page(1)
                         .page_size(10)
                         .search())
        
        print(f"   Found {search_results.count} profiles")
        print(f"   Total available: {search_results.total}")
        print(f"   Current page: {search_results.current_page}")
        print(f"   Has next page: {search_results.has_next_page}")
        
        for profile in search_results.get_profiles():
            print(f"   - {profile.get('name', 'N/A')} at {profile.get('current_employer', 'N/A')}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 2: Person Lookup
    print("2. Person Lookup Example:")
    try:
        person = (client.person_lookup()
                  .name("John Doe")
                  .current_employer("Google")
                  .lookup())
        
        print(f"   Person ID: {person.id}")
        print(f"   Name: {person.name}")
        print(f"   Title: {person.current_title}")
        print(f"   Employer: {person.current_employer}")
        print(f"   Status: {person.status}")
        print(f"   Is Complete: {person.is_complete}")
        
        emails = person.get_emails()
        if emails:
            print(f"   Emails: {[email.get('email') for email in emails]}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 3: Person Enrichment
    print("3. Person Enrichment Example:")
    try:
        enriched = (client.person_enrich()
                    .name("John Doe")
                    .current_employer("Google")
                    .enrich())
        
        print(f"   Person: {enriched.person_name} (ID: {enriched.person_id})")
        print(f"   Company: {enriched.company_name} (ID: {enriched.company_id})")
        print(f"   Company Domain: {enriched.company_domain}")
        print(f"   Company Industry: {enriched.company_industry}")
        print(f"   Company Size: {enriched.company_employee_count}")
        
        person_emails = enriched.get_person_emails()
        if person_emails:
            print(f"   Person Emails: {[email.get('email') for email in person_emails]}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 4: Account Information
    print("4. Account Information Example:")
    try:
        account_info = client.get_account_info()
        print(f"   Account Info: {account_info}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print()
    
    # Example 5: Health Check
    print("5. Health Check Example:")
    try:
        health_status = client.get_health_status()
        print(f"   Health Status: {health_status}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
