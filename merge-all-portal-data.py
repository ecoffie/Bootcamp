#!/usr/bin/env python3
"""
Merge all vendor portal data from batch files into the master database.
This script consolidates portal research from multiple sources.
"""

import csv
import os
import glob
from collections import defaultdict

def normalize_company_name(name):
    """Normalize company name for matching."""
    if not name:
        return ""
    # Remove quotes, extra spaces, standardize case
    name = name.strip().strip('"').strip("'").upper()
    # Remove common suffixes for matching
    for suffix in [' INC.', ' INC', ' LLC', ' LP', ' LLP', ' CORP.', ' CORP', ' CORPORATION', ' COMPANY', ' CO.', ' CO', ' L.P.', ' L.L.C.']:
        name = name.replace(suffix, '')
    # Remove extra spaces
    name = ' '.join(name.split())
    return name

def read_batch_files():
    """Read all batch files and extract portal data."""
    portal_data = {}

    # Find all batch files
    batch_patterns = [
        'priority-batch-*.csv',
        'tier1-batch-*.csv',
        'tier2-batch-*.csv',
        'tier2-priority-batch-*.csv'
    ]

    batch_files = []
    for pattern in batch_patterns:
        batch_files.extend(glob.glob(pattern))

    print(f"Found {len(batch_files)} batch files")

    for filepath in batch_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    company = row.get('company', '').strip()
                    url = row.get('vendor_registration_url', '').strip()
                    portal_type = row.get('portal_type', '').strip()
                    notes = row.get('notes', '').strip()

                    if company and url and url.startswith('http'):
                        norm_name = normalize_company_name(company)
                        if norm_name not in portal_data:
                            portal_data[norm_name] = {
                                'original_name': company,
                                'url': url,
                                'type': portal_type,
                                'notes': notes
                            }
                            print(f"  Found portal: {company} -> {url[:50]}...")
        except Exception as e:
            print(f"Error reading {filepath}: {e}")

    return portal_data

def read_sblo_portal_files():
    """Read SBLO contact list files with portal data."""
    portal_data = {}

    files = [
        'FINAL-SBLO-CONTACT-LIST-WITH-PORTALS.csv',
        'TIER-2-FINAL-CONTACT-LIST-WITH-PORTALS.csv'
    ]

    for filepath in files:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        company = row.get('company', '').strip()
                        url = row.get('vendor_registration_url', '').strip()
                        portal_type = row.get('portal_type', '').strip()
                        notes = row.get('portal_notes', row.get('notes', '')).strip()

                        if company and url and url.startswith('http'):
                            norm_name = normalize_company_name(company)
                            if norm_name not in portal_data:
                                portal_data[norm_name] = {
                                    'original_name': company,
                                    'url': url,
                                    'type': portal_type,
                                    'notes': notes
                                }
                                print(f"  Found portal (SBLO): {company} -> {url[:50]}...")
            except Exception as e:
                print(f"Error reading {filepath}: {e}")

    return portal_data

def read_master_database():
    """Read the master database."""
    companies = []
    with open('FEDERAL-CONTRACTOR-MASTER-DATABASE.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(dict(row))
    return companies

def merge_portal_data(companies, portal_data):
    """Merge portal data into companies."""
    matched = 0
    already_has = 0

    for company in companies:
        name = company.get('company', '')
        norm_name = normalize_company_name(name)

        # Check if already has portal
        existing_url = company.get('vendor_registration_url', '').strip()
        if existing_url and existing_url.startswith('http'):
            already_has += 1
            continue

        # Try to find a match
        if norm_name in portal_data:
            data = portal_data[norm_name]
            company['vendor_registration_url'] = data['url']
            company['vendor_portal_type'] = data['type']
            company['vendor_portal_notes'] = data['notes']
            matched += 1
            print(f"  Matched: {name} -> {data['url'][:50]}...")
        else:
            # Try partial matching
            for portal_norm, data in portal_data.items():
                if portal_norm in norm_name or norm_name in portal_norm:
                    company['vendor_registration_url'] = data['url']
                    company['vendor_portal_type'] = data['type']
                    company['vendor_portal_notes'] = data['notes']
                    matched += 1
                    print(f"  Partial match: {name} -> {data['url'][:50]}...")
                    break

    return matched, already_has

def write_master_database(companies):
    """Write the updated master database."""
    fieldnames = [
        'company', 'sblo_name', 'title', 'email', 'phone', 'address',
        'naics', 'source', 'contract_count', 'total_contract_value',
        'agencies', 'has_subcontract_plan', 'has_contact_info',
        'vendor_registration_url', 'vendor_portal_type', 'vendor_portal_notes'
    ]

    with open('FEDERAL-CONTRACTOR-MASTER-DATABASE.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(companies)

def main():
    print("=" * 60)
    print("MERGING VENDOR PORTAL DATA INTO MASTER DATABASE")
    print("=" * 60)

    # Read portal data from batch files
    print("\n1. Reading batch files...")
    batch_portals = read_batch_files()
    print(f"   Found {len(batch_portals)} unique portals in batch files")

    # Read portal data from SBLO files
    print("\n2. Reading SBLO portal files...")
    sblo_portals = read_sblo_portal_files()
    print(f"   Found {len(sblo_portals)} unique portals in SBLO files")

    # Merge all portal data
    all_portals = {**batch_portals, **sblo_portals}
    print(f"\n   Total unique portals: {len(all_portals)}")

    # Read master database
    print("\n3. Reading master database...")
    companies = read_master_database()
    print(f"   Total companies: {len(companies)}")

    # Merge portal data
    print("\n4. Merging portal data...")
    matched, already_has = merge_portal_data(companies, all_portals)

    # Count final portals
    final_portal_count = sum(1 for c in companies if c.get('vendor_registration_url', '').startswith('http'))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Companies already with portals: {already_has}")
    print(f"New portals added: {matched}")
    print(f"Total companies with portals: {final_portal_count}")

    # Write updated database
    print("\n5. Writing updated master database...")
    write_master_database(companies)
    print("   Done!")

    # List all companies with portals
    print("\n" + "=" * 60)
    print("COMPANIES WITH PORTAL LINKS")
    print("=" * 60)
    for c in companies:
        url = c.get('vendor_registration_url', '')
        if url and url.startswith('http'):
            print(f"  - {c['company']}: {url[:60]}...")

if __name__ == '__main__':
    main()
