#!/usr/bin/env python3
"""
Create priority batch files for Tier 2 companies
Focuses on high-priority companies for fastest go-to-market
"""

import csv
import re

def clean_company_name(company_name):
    """Clean company name for search queries"""
    company = company_name.strip()
    company = re.sub(r',?\s*(INC\.?|LLC\.?|CORPORATION|CORP\.?|L\.P\.|LP|LLP|THE)$', '', company, flags=re.IGNORECASE)
    company = re.sub(r'^(THE)\s+', '', company, flags=re.IGNORECASE)
    return company.strip()

def extract_priority_companies(input_file, output_file, priority_level='high'):
    """Extract companies by priority level"""
    
    priority_companies = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('priority', '').lower() == priority_level.lower():
                priority_companies.append({
                    'company': row.get('company', ''),
                    'search_query': row.get('search_query', ''),
                    'priority': row.get('priority', ''),
                    'sblo_name': '',  # Added for enrichment
                    'email': ''  # Added for enrichment
                })
    
    # Write to priority file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'search_query', 'priority', 'sblo_name', 'email']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(priority_companies)
    
    return priority_companies

def create_priority_batch(input_file, output_file, batch_size=10, batch_num=1):
    """Create a priority batch file with search-ready format"""
    
    companies = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)
    
    # Calculate batch
    start_idx = (batch_num - 1) * batch_size
    end_idx = start_idx + batch_size
    batch = companies[start_idx:end_idx]
    
    print(f"Priority Batch {batch_num}: Companies {start_idx + 1} to {min(end_idx, len(companies))}")
    print(f"Total priority companies: {len(companies)}\n")
    
    # Create output with search-ready format
    results = []
    for company in batch:
        company_name = company.get('company', '')
        clean_name = clean_company_name(company_name)
        
        results.append({
            'company': company_name,
            'clean_name': clean_name,
            'sblo_name': '',  # Will be filled from existing data
            'email': '',  # Will be filled from existing data
            'search_query': company.get('search_query', f'"{clean_name}" supplier portal vendor registration'),
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
    print(f"✓ Ready for vendor portal research\n")
    
    return results

def enrich_with_existing_contacts(priority_file, existing_contacts_file):
    """Enrich priority list with existing SBLO contacts"""
    
    # Load existing contacts
    contacts = {}
    try:
        with open(existing_contacts_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get('company', '').strip().upper()
                contacts[company] = {
                    'sblo_name': row.get('sblo_name', ''),
                    'email': row.get('email', '')
                }
    except FileNotFoundError:
        print(f"⚠ No existing contacts file found: {existing_contacts_file}")
        return False
    
    # Update priority file
    updated_rows = []
    with open(priority_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        
        for row in reader:
            company = row.get('company', '').strip().upper()
            
            # Try to match with existing contacts
            for contact_company, contact_data in contacts.items():
                if company in contact_company or contact_company in company:
                    row['sblo_name'] = contact_data.get('sblo_name', '')
                    row['email'] = contact_data.get('email', '')
                    break
            
            updated_rows.append(row)
    
    # Write updated file
    with open(priority_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)
    
    return True

def main():
    import sys
    
    print("=" * 80)
    print("TIER 2 PRIORITY BATCH CREATOR")
    print("Fastest Go-to-Market Strategy")
    print("=" * 80)
    print()
    
    # Step 1: Extract high-priority companies
    print("Step 1: Extracting high-priority Tier 2 companies...")
    priority_companies = extract_priority_companies(
        'tier2-vendor-portal-searches.csv',
        'tier2-high-priority-list.csv',
        'high'
    )
    
    print(f"✓ Found {len(priority_companies)} high-priority companies")
    print(f"✓ Saved to: tier2-high-priority-list.csv\n")
    
    if len(priority_companies) == 0:
        print("⚠ No high-priority companies found!")
        print("   Check tier2-vendor-portal-searches.csv for 'high' priority flag")
        return
    
    # Step 2: Enrich with existing contacts
    print("Step 2: Enriching with existing SBLO contacts...")
    if enrich_with_existing_contacts('tier2-high-priority-list.csv', 'TIER-2-FINAL-CONTACT-LIST.csv'):
        print("✓ Enriched with existing contacts\n")
    
    # Step 3: Create priority batches (10 companies each for fast research)
    print("Step 3: Creating priority batch files...")
    print("-" * 80)
    
    batch_size = 10
    num_batches = (len(priority_companies) + batch_size - 1) // batch_size
    
    for i in range(1, num_batches + 1):
        output_file = f"tier2-priority-batch-{i:02d}.csv"
        create_priority_batch(
            'tier2-high-priority-list.csv',
            output_file,
            batch_size=batch_size,
            batch_num=i
        )
    
    print("=" * 80)
    print(f"✓ Created {num_batches} priority batch files")
    print()
    print("🎯 NEXT STEPS:")
    print("1. Start with tier2-priority-batch-01.csv (top 10 companies)")
    print("2. Research vendor portals using search_query column")
    print("3. Fill in vendor_registration_url, portal_type, and notes")
    print("4. Register in portals and contact SBLOs immediately")
    print()
    print("💡 PRIORITY: Focus on Batch 01 first - these are your fastest path to revenue!")
    print("=" * 80)

if __name__ == '__main__':
    main()

