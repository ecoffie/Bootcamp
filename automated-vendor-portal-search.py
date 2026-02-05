#!/usr/bin/env python3
"""
Automated vendor portal search using web search.
This script will search for vendor registration pages and extract URLs.
"""

import csv
import re
import time
import json

def clean_company_name(company_name):
    """Clean company name for search queries"""
    company = company_name.strip()
    # Remove common suffixes
    company = re.sub(r',?\s*(INC\.?|LLC\.?|CORPORATION|CORP\.?|L\.P\.|LP|LLP|THE)$', '', company, flags=re.IGNORECASE)
    company = re.sub(r'^(THE)\s+', '', company, flags=re.IGNORECASE)
    return company.strip()

def generate_search_queries(company_name):
    """Generate search queries for finding vendor portals"""
    clean_name = clean_company_name(company_name)

    queries = [
        f'"{clean_name}" supplier portal registration',
        f'"{clean_name}" vendor registration',
        f'"{clean_name}" small business subcontractor portal',
        f'site:{get_company_domain(clean_name)} vendor registration',
    ]

    return queries

def get_company_domain(company_name):
    """Guess company domain from name"""
    clean_name = clean_company_name(company_name)
    # Simple domain guess
    domain = clean_name.lower()
    domain = re.sub(r'[^a-z0-9\s]', '', domain)
    domain = domain.replace(' ', '')
    return f"{domain}.com"

def extract_vendor_portal_urls(search_results_text):
    """Extract likely vendor portal URLs from search results"""
    # Common patterns for vendor portals
    portal_keywords = [
        'supplier', 'vendor', 'portal', 'registration',
        'subcontractor', 'small-business', 'smallbusiness',
        'partner', 'sourcing', 'procurement'
    ]

    # URL pattern
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    urls = re.findall(url_pattern, search_results_text.lower())

    # Filter for vendor-related URLs
    vendor_urls = []
    for url in urls:
        for keyword in portal_keywords:
            if keyword in url:
                vendor_urls.append(url)
                break

    return list(set(vendor_urls))  # Remove duplicates

def read_companies_from_csv(filename):
    """Read company list from CSV"""
    companies = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('company'):
                companies.append({
                    'company': row['company'],
                    'sblo_name': row.get('sblo_name', ''),
                    'email': row.get('email', ''),
                })
    return companies

def save_results(results, output_file):
    """Save results to CSV"""
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'email', 'vendor_registration_url',
                      'additional_urls', 'search_query_used', 'needs_manual_review', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Results saved to: {output_file}")

def main():
    """Main function - creates search queries list"""

    print("=" * 80)
    print("VENDOR PORTAL AUTOMATED SEARCH SCRIPT")
    print("=" * 80)

    # This script will create a file with search queries
    # The actual web searching will be done via Claude's WebSearch capability

    tier1_companies = read_companies_from_csv('FINAL-SBLO-CONTACT-LIST.csv')
    tier2_companies = read_companies_from_csv('TIER-2-FINAL-CONTACT-LIST-CLEAN.csv')

    print(f"\nTier 1 Companies: {len(tier1_companies)}")
    print(f"Tier 2 Companies: {len(tier2_companies)}")

    # Create search query files
    def create_search_file(companies, output_file):
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['company', 'search_query', 'priority'])
            writer.writeheader()

            for company in companies:
                clean_name = clean_company_name(company['company'])
                # Primary search query
                writer.writerow({
                    'company': company['company'],
                    'search_query': f'"{clean_name}" supplier portal vendor registration',
                    'priority': 'high' if company.get('email') else 'medium'
                })

    create_search_file(tier1_companies, 'tier1-vendor-portal-searches.csv')
    create_search_file(tier2_companies, 'tier2-vendor-portal-searches.csv')

    print("\n✓ Search query files created:")
    print("  - tier1-vendor-portal-searches.csv")
    print("  - tier2-vendor-portal-searches.csv")

    # Create list of top priority companies (major primes)
    major_primes = [
        'Lockheed Martin', 'Raytheon', 'Boeing', 'Northrop Grumman',
        'General Dynamics', 'Booz Allen Hamilton', 'Leidos', 'SAIC',
        'BAE Systems', 'L3Harris', 'Accenture', 'Deloitte', 'KPMG',
        'IBM', 'Amentum', 'Jacobs Engineering', 'AECOM', 'Fluor',
        'Peraton', 'CACI', 'ManTech', 'Parsons'
    ]

    # Create priority list
    priority_companies = []
    for company in tier1_companies:
        for prime in major_primes:
            if prime.lower() in company['company'].lower():
                priority_companies.append(company)
                break

    print(f"\n✓ Identified {len(priority_companies)} high-priority companies for immediate search")

    # Save priority list
    with open('priority-vendor-portal-searches.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['company', 'sblo_name', 'email', 'search_query'])
        writer.writeheader()

        for company in priority_companies:
            clean_name = clean_company_name(company['company'])
            writer.writerow({
                'company': company['company'],
                'sblo_name': company['sblo_name'],
                'email': company['email'],
                'search_query': f'"{clean_name}" supplier portal vendor registration'
            })

    print("✓ Priority search file created: priority-vendor-portal-searches.csv")

    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Start with priority companies (major defense/IT primes)")
    print("2. Use web search to find vendor portals")
    print("3. Look for URLs containing: supplier, vendor, portal, subcontractor")
    print("4. Common portal locations:")
    print("   - https://supplier.company.com")
    print("   - https://company.com/suppliers")
    print("   - https://company.com/smallbusiness")
    print("   - https://portal.company.com/vendors")
    print("=" * 80)

if __name__ == '__main__':
    main()
