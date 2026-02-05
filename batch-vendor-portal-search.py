#!/usr/bin/env python3
"""
Batch vendor portal search - processes companies and prepares for web search
This creates structured data that can be used with Claude's WebSearch capability
"""

import csv
import json
import re

def clean_company_name(company_name):
    """Clean company name for search queries"""
    company = company_name.strip()
    company = re.sub(r',?\s*(INC\.?|LLC\.?|CORPORATION|CORP\.?|L\.P\.|LP|LLP|THE)$', '', company, flags=re.IGNORECASE)
    company = re.sub(r'^(THE)\s+', '', company, flags=re.IGNORECASE)
    return company.strip()

def create_search_batch(input_file, output_file, batch_size=10, batch_num=1):
    """Create a batch of companies to search"""

    companies = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)

    # Calculate batch
    start_idx = (batch_num - 1) * batch_size
    end_idx = start_idx + batch_size
    batch = companies[start_idx:end_idx]

    print(f"Batch {batch_num}: Companies {start_idx + 1} to {min(end_idx, len(companies))}")
    print(f"Total companies in file: {len(companies)}\n")

    # Create output with search instructions
    results = []
    for company in batch:
        company_name = company.get('company', '')
        clean_name = clean_company_name(company_name)

        results.append({
            'company': company_name,
            'clean_name': clean_name,
            'sblo_name': company.get('sblo_name', ''),
            'email': company.get('email', ''),
            'search_query': f'"{clean_name}" supplier portal vendor registration',
            'vendor_registration_url': '',
            'portal_type': '',
            'notes': ''
        })

    # Save batch
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'clean_name', 'sblo_name', 'email', 'search_query',
                     'vendor_registration_url', 'portal_type', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"✓ Batch file created: {output_file}")
    print(f"✓ Ready for web search\n")

    return results

def create_all_batches(input_file, prefix, batch_size=10):
    """Create all batches for a file"""

    # Count total companies
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        total = sum(1 for row in reader)

    num_batches = (total + batch_size - 1) // batch_size

    print(f"Creating {num_batches} batches of {batch_size} companies each")
    print(f"Total companies: {total}\n")
    print("=" * 80)

    for i in range(1, num_batches + 1):
        output_file = f"{prefix}-batch-{i:02d}.csv"
        create_search_batch(input_file, output_file, batch_size, i)

    print("=" * 80)
    print(f"✓ All {num_batches} batches created")
    print(f"\nNext steps:")
    print(f"1. Start with batch 01: {prefix}-batch-01.csv")
    print(f"2. Use web search for each company")
    print(f"3. Fill in vendor_registration_url, portal_type, and notes")
    print(f"4. Move to next batch")

if __name__ == '__main__':
    import sys

    print("=" * 80)
    print("BATCH VENDOR PORTAL SEARCH - BATCH CREATOR")
    print("=" * 80)
    print()

    # Check arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == 'priority':
            print("Creating batches for PRIORITY companies (5 companies per batch)...")
            create_all_batches('priority-vendor-portal-searches.csv', 'priority', batch_size=5)

        elif sys.argv[1] == 'tier1':
            print("Creating batches for TIER 1 companies (20 companies per batch)...")
            create_all_batches('tier1-vendor-portal-searches.csv', 'tier1', batch_size=20)

        elif sys.argv[1] == 'tier2':
            print("Creating batches for TIER 2 companies (20 companies per batch)...")
            create_all_batches('tier2-vendor-portal-searches.csv', 'tier2', batch_size=20)

        elif sys.argv[1] == 'all':
            print("Creating all batches...\n")
            print("\n1. PRIORITY COMPANIES (5 per batch)")
            print("-" * 80)
            create_all_batches('priority-vendor-portal-searches.csv', 'priority', batch_size=5)

            print("\n\n2. TIER 1 COMPANIES (20 per batch)")
            print("-" * 80)
            create_all_batches('tier1-vendor-portal-searches.csv', 'tier1', batch_size=20)

            print("\n\n3. TIER 2 COMPANIES (20 per batch)")
            print("-" * 80)
            create_all_batches('tier2-vendor-portal-searches.csv', 'tier2', batch_size=20)

        else:
            print("Usage: python3 batch-vendor-portal-search.py [priority|tier1|tier2|all]")

    else:
        print("Creating first batch of PRIORITY companies...")
        batch = create_search_batch('priority-vendor-portal-searches.csv',
                                    'priority-batch-01.csv', batch_size=5, batch_num=1)

        print("\nCompanies in this batch:")
        for i, company in enumerate(batch, 1):
            print(f"{i}. {company['company']}")

        print("\n" + "=" * 80)
        print("To create more batches, run:")
        print("  python3 batch-vendor-portal-search.py priority  # All priority batches")
        print("  python3 batch-vendor-portal-search.py tier1     # All tier 1 batches")
        print("  python3 batch-vendor-portal-search.py tier2     # All tier 2 batches")
        print("  python3 batch-vendor-portal-search.py all       # All batches")
        print("=" * 80)
