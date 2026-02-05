#!/usr/bin/env python3
"""
Search SBA DSBS for Tribal 8(a) Companies
Attempts to query SBA Dynamic Small Business Search for verified tribal 8(a) companies
"""

import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
import time
import re

def search_sba_dsbs_manual_instructions():
    """Provide instructions for manual SBA DSBS search"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   SBA DSBS Search Instructions                      ║
    ╚══════════════════════════════════════════════════════╝
    
    The SBA DSBS requires manual search through their web interface.
    Here's how to export Tribal 8(a) companies:
    
    STEP 1: Access SBA DSBS
    ------------------------
    URL: https://web.sba.gov/pro-net/search/dsp_dsbs.cfm
    
    STEP 2: Set Search Criteria
    ----------------------------
    1. Scroll to "Ownership and Self-Certifications"
    2. Check: ☑ Native American
    3. Scroll to "Government Certifications"
    4. Check: ☑ 8(a) Certified
    5. (Optional) Add NAICS codes or location filters
    
    STEP 3: Run Search
    ------------------
    Click "Search Using These Criteria"
    
    STEP 4: Export Results
    ----------------------
    1. On results page, look for "Export" or "Download" button
    2. Export to CSV or Excel
    3. Save file as: sba-dsbs-tribal-8a-export.csv
    
    STEP 5: Process Results
    -----------------------
    Run: python3 process-sba-dsbs-export.py
    
    """)

def create_dsbs_search_urls():
    """Create direct search URLs for common tribal 8(a) searches"""
    base_url = "https://web.sba.gov/pro-net/search/dsp_dsbs.cfm"
    
    searches = {
        'native_american_8a': {
            'name': 'Native American + 8(a)',
            'description': 'All Native American owned 8(a) companies',
            'url': base_url + '?certification=8A&ownership=NativeAmerican'
        },
        'alaska_native_8a': {
            'name': 'Alaska Native Corporation + 8(a)',
            'description': 'All ANC-owned 8(a) companies',
            'url': base_url + '?certification=8A&ownership=AlaskaNative'
        },
        'tribal_8a_by_naics': {
            'name': 'Tribal 8(a) by NAICS',
            'description': 'Search by specific NAICS codes',
            'url': base_url + '?certification=8A&ownership=NativeAmerican&naics='
        }
    }
    
    return searches

def process_dsbs_export(file_path):
    """Process exported SBA DSBS CSV file"""
    file = Path(file_path)
    
    if not file.exists():
        print(f"❌ File not found: {file_path}")
        print("   Please export from SBA DSBS first")
        return []
    
    print(f"📊 Processing SBA DSBS export: {file_path}")
    
    companies = []
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Extract key information
            company_name = row.get('Business Name', '') or row.get('Company Name', '') or row.get('Name', '')
            duns = row.get('DUNS', '') or row.get('DUNS Number', '')
            address = row.get('Address', '') or row.get('Business Address', '')
            city = row.get('City', '')
            state = row.get('State', '')
            zip_code = row.get('Zip', '') or row.get('ZIP Code', '')
            phone = row.get('Phone', '') or row.get('Business Phone', '')
            email = row.get('Email', '') or row.get('Business Email', '')
            website = row.get('Website', '') or row.get('Business Website', '')
            naics = row.get('Primary NAICS', '') or row.get('NAICS Code', '')
            
            # Check 8(a) status
            cert_status = row.get('8(a) Status', '') or row.get('Certification Status', '')
            ownership = row.get('Ownership Type', '') or row.get('Ownership', '')
            
            companies.append({
                'company': company_name,
                'duns': duns,
                'address': f"{address}, {city}, {state} {zip_code}".strip(', '),
                'phone': phone,
                'email': email,
                'website': website,
                'naics': naics,
                '8a_status': cert_status,
                'ownership_type': ownership,
                'source': 'SBA DSBS Export',
                'sblo_contact': '[NEEDS RESEARCH]',
                'sblo_email': '[NEEDS RESEARCH]',
                'sblo_phone': '[NEEDS RESEARCH]'
            })
    
    print(f"✅ Processed {len(companies)} companies")
    
    # Save processed list
    output_file = Path('sba-dsbs-tribal-8a-processed.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'duns', 'address', 'phone', 'email', 'website', 'naics',
                     '8a_status', 'ownership_type', 'source', 'sblo_contact', 'sblo_email', 'sblo_phone']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(companies)
    
    print(f"💾 Saved processed list: {output_file}")
    
    # Show top companies
    if companies:
        print("\n📋 Sample Companies Found:")
        for i, company in enumerate(companies[:10], 1):
            print(f"   {i:2d}. {company['company'][:50]:50s} - {company.get('8a_status', 'N/A')}")
    
    return companies

def cross_reference_with_prime_list(tribal_companies_file='sba-dsbs-tribal-8a-processed.csv'):
    """Cross-reference tribal 8(a) companies with your prime list"""
    tribal_file = Path(tribal_companies_file)
    prime_file = Path('sba-prime-directory-companies.csv')
    
    if not tribal_file.exists():
        print(f"❌ Tribal companies file not found: {tribal_file}")
        return
    
    if not prime_file.exists():
        print(f"❌ Prime directory file not found: {prime_file}")
        return
    
    print("\n🔍 Cross-referencing with prime list...")
    
    # Load tribal companies
    tribal_companies = {}
    with open(tribal_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = row.get('company', '').strip().lower()
            if company:
                tribal_companies[company] = row
    
    # Load prime companies
    matches = []
    with open(prime_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = row.get('company', '').strip().lower()
            if company in tribal_companies:
                matches.append({
                    'company': row.get('company', ''),
                    'contract_value': row.get('total_contract_value', ''),
                    'contract_count': row.get('contract_count', ''),
                    '8a_status': tribal_companies[company].get('8a_status', ''),
                    'tribal_info': tribal_companies[company]
                })
    
    print(f"✅ Found {len(matches)} tribal 8(a) companies in your prime list")
    
    if matches:
        # Save matches
        matches_file = Path('tribal-8a-in-prime-list.csv')
        with open(matches_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['company', 'contract_value', 'contract_count', '8a_status', 'duns', 'email', 'phone']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for match in matches:
                tribal = match['tribal_info']
                writer.writerow({
                    'company': match['company'],
                    'contract_value': match['contract_value'],
                    'contract_count': match['contract_count'],
                    '8a_status': match['8a_status'],
                    'duns': tribal.get('duns', ''),
                    'email': tribal.get('email', ''),
                    'phone': tribal.get('phone', '')
                })
        
        print(f"💾 Saved matches: {matches_file}")
        
        # Show top matches
        print("\n📋 Top Tribal 8(a) Companies in Your Prime List:")
        matches_sorted = sorted(matches, key=lambda x: float(x.get('contract_value', 0) or 0), reverse=True)
        for i, match in enumerate(matches_sorted[:10], 1):
            value = match.get('contract_value', '')
            if value:
                try:
                    value_str = f"${float(value):,.0f}"
                except:
                    value_str = value
            else:
                value_str = 'N/A'
            print(f"   {i:2d}. {match['company'][:45]:45s} - {value_str}")
    
    return matches

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   SBA DSBS Tribal 8(a) Search Tool                  ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    print("""
    This tool helps you find and process Tribal 8(a) companies.
    
    OPTION 1: Manual Search (Recommended)
    -------------------------------------
    """)
    search_sba_dsbs_manual_instructions()
    
    print("""
    OPTION 2: Process Existing Export
    -----------------------------------
    If you've already exported from SBA DSBS, run:
    python3 search-sba-dsbs-tribal-8a.py process <filename.csv>
    """)
    
    # Check if user wants to process a file
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'process':
        filename = sys.argv[2] if len(sys.argv) > 2 else 'sba-dsbs-tribal-8a-export.csv'
        companies = process_dsbs_export(filename)
        if companies:
            cross_reference_with_prime_list('sba-dsbs-tribal-8a-processed.csv')

if __name__ == '__main__':
    main()




