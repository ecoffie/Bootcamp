#!/usr/bin/env python3
"""
Find vendor registration/supplier portal links for companies in SBLO lists.
This script will search for vendor registration pages for each company.
"""

import csv
import time
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

def clean_company_name(company_name):
    """Clean company name for search queries"""
    # Remove common suffixes and special characters
    company = company_name.strip()
    company = re.sub(r',\s*(INC\.?|LLC\.?|CORPORATION|CORP\.?|LP|LLP)$', '', company, flags=re.IGNORECASE)
    return company.strip()

def search_vendor_portal(company_name):
    """
    Search for vendor registration/supplier portal for a company.
    Uses multiple search strategies.
    """
    clean_name = clean_company_name(company_name)

    # Common vendor portal keywords
    keywords = [
        "vendor registration",
        "supplier registration",
        "become a supplier",
        "supplier portal",
        "vendor portal",
        "small business portal",
        "subcontractor registration"
    ]

    results = {
        'company': company_name,
        'vendor_portal_url': '',
        'portal_type': '',
        'search_status': 'pending'
    }

    print(f"\nSearching for: {company_name}")

    # Strategy 1: Common vendor portal URL patterns
    common_patterns = [
        f"supplier.{clean_name.lower().replace(' ', '')}.com",
        f"vendors.{clean_name.lower().replace(' ', '')}.com",
        f"portal.{clean_name.lower().replace(' ', '')}.com",
        f"{clean_name.lower().replace(' ', '')}.com/suppliers",
        f"{clean_name.lower().replace(' ', '')}.com/vendors",
        f"{clean_name.lower().replace(' ', '')}.com/smallbusiness",
    ]

    # We'll need to use web search for this - marking for manual research
    results['search_status'] = 'needs_web_search'
    results['search_queries'] = [
        f'"{clean_name}" vendor registration portal',
        f'"{clean_name}" supplier registration',
        f'"{clean_name}" small business portal'
    ]

    return results

def process_sblo_list(input_file, output_file):
    """Process SBLO list and find vendor portals"""

    companies_data = []

    # Read the CSV file
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        # Add new field if not exists
        if 'vendor_registration_url' not in fieldnames:
            fieldnames = list(fieldnames) + ['vendor_registration_url', 'portal_type']

        for row in reader:
            companies_data.append(row)

    print(f"Found {len(companies_data)} companies to process")

    # For now, we'll create a research template
    # Actual web searches will need to be done via WebSearch tool
    research_file = output_file.replace('.csv', '-research-template.csv')

    with open(research_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['company', 'sblo_name', 'email',
                                                'vendor_registration_url', 'portal_type',
                                                'search_query', 'notes'])
        writer.writeheader()

        for company in companies_data:
            company_name = company.get('company', '')
            clean_name = clean_company_name(company_name)

            writer.writerow({
                'company': company_name,
                'sblo_name': company.get('sblo_name', ''),
                'email': company.get('email', ''),
                'vendor_registration_url': '',  # To be filled
                'portal_type': '',  # To be filled
                'search_query': f'"{clean_name}" vendor registration portal',
                'notes': ''
            })

    print(f"\nResearch template created: {research_file}")
    print(f"This file can be used to track vendor portal research progress")

    return research_file

if __name__ == '__main__':
    print("=" * 80)
    print("VENDOR REGISTRATION LINK FINDER")
    print("=" * 80)

    # Process Tier 1 list
    print("\n\nProcessing Tier 1 SBLO List...")
    tier1_research = process_sblo_list(
        'FINAL-SBLO-CONTACT-LIST.csv',
        'TIER-1-VENDOR-REGISTRATION-RESEARCH.csv'
    )

    # Process Tier 2 list
    print("\n\nProcessing Tier 2 SBLO List...")
    tier2_research = process_sblo_list(
        'TIER-2-FINAL-CONTACT-LIST-CLEAN.csv',
        'TIER-2-VENDOR-REGISTRATION-RESEARCH.csv'
    )

    print("\n" + "=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print("1. Research templates have been created")
    print("2. Use web search to find vendor portals for each company")
    print("3. Common portal names to look for:")
    print("   - Supplier Portal")
    print("   - Vendor Registration")
    print("   - Small Business Portal")
    print("   - Subcontractor Portal")
    print("   - Partner Portal")
    print("=" * 80)
