#!/usr/bin/env python3
"""
Merge SBA Prime Directory (2,700+ companies) with SBLO Contact Database (893 companies)
Creates comprehensive searchable database
"""

import csv
from difflib import SequenceMatcher

def similar(a, b):
    """Calculate similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def normalize_company_name(name):
    """Normalize company name for matching"""
    # Remove common suffixes
    name = name.upper()
    suffixes = [
        ' LLC', ' INC', ' INCORPORATED', ' CORP', ' CORPORATION',
        ' LTD', ' LIMITED', ' CO', ' COMPANY', ' LP', ' L.P.',
        ' THE', ',', '.'
    ]
    for suffix in suffixes:
        name = name.replace(suffix, '')
    return name.strip()

# Load SBLO contact database
print("=" * 80)
print("MERGING SBA PRIME DIRECTORY WITH SBLO CONTACT DATABASE")
print("=" * 80)

sblo_file = '/Users/ericcoffie/Bootcamp/sblo-list-compiled.csv'
sblo_contacts = {}

print("\n📊 Loading SBLO contact database...")
with open(sblo_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = row.get('company', '').strip()
        if not company or company in ['In Search Of:', 'Contract', 'https://']:
            continue

        normalized = normalize_company_name(company)
        if normalized not in sblo_contacts:
            sblo_contacts[normalized] = []
        sblo_contacts[normalized].append({
            'company': company,
            'sblo_name': row.get('sblo_name', '').strip(),
            'title': row.get('title', '').strip(),
            'email': row.get('email', '').strip(),
            'phone': row.get('phone', '').strip(),
            'address': row.get('address', '').strip(),
            'naics': row.get('naics', '').strip(),
            'source': row.get('source', '').strip()
        })

print(f"✅ Loaded {len(sblo_contacts)} unique companies from SBLO database")

# Load SBA Prime Directory
sba_file = '/Users/ericcoffie/Bootcamp/sba-prime-directory-companies.csv'
sba_companies = []

print("\n📊 Loading SBA Prime Directory...")
with open(sba_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = row.get('company', '').strip()
        if company:
            sba_companies.append({
                'company': company,
                'contract_count': row.get('contract_count', ''),
                'total_contract_value': row.get('total_contract_value', ''),
                'agencies': row.get('agencies', '').strip(),
                'naics': row.get('naics', '').strip(),
                'has_subcontract_plan': row.get('has_subcontract_plan', '')
            })

print(f"✅ Loaded {len(sba_companies)} companies from SBA Prime Directory")

# Merge data
print("\n🔄 Merging datasets...")
merged_companies = []
matches_found = 0
no_match = 0

for sba_company in sba_companies:
    sba_name = sba_company['company']
    sba_normalized = normalize_company_name(sba_name)

    # Try exact match first
    matched_contact = None
    if sba_normalized in sblo_contacts:
        matched_contact = sblo_contacts[sba_normalized][0]
        matches_found += 1
    else:
        # Try fuzzy matching for close matches
        best_match = None
        best_ratio = 0
        for sblo_normalized, contacts in sblo_contacts.items():
            ratio = similar(sba_normalized, sblo_normalized)
            if ratio > best_ratio and ratio > 0.85:  # 85% similarity threshold
                best_ratio = ratio
                best_match = contacts[0]

        if best_match:
            matched_contact = best_match
            matches_found += 1
        else:
            no_match += 1

    # Build merged record
    merged = {
        'company': sba_name,
        'sblo_name': matched_contact['sblo_name'] if matched_contact else '',
        'title': matched_contact['title'] if matched_contact else '',
        'email': matched_contact['email'] if matched_contact else '',
        'phone': matched_contact['phone'] if matched_contact else '',
        'address': matched_contact['address'] if matched_contact else '',
        'naics': sba_company['naics'],  # Prefer SBA NAICS (more comprehensive)
        'source': matched_contact['source'] if matched_contact else 'SBA Prime Directory FY24',
        'contract_count': sba_company['contract_count'],
        'total_contract_value': sba_company['total_contract_value'],
        'agencies': sba_company['agencies'],
        'has_subcontract_plan': sba_company['has_subcontract_plan'],
        'has_contact_info': 'Yes' if matched_contact else 'No'
    }

    merged_companies.append(merged)

print(f"✅ Merged {matches_found} companies with SBLO contacts")
print(f"📊 {no_match} companies without contact info (yet)")

# Sort by total contract value (descending)
merged_companies.sort(key=lambda x: float(x['total_contract_value']) if x['total_contract_value'] else 0, reverse=True)

# Write merged database
output_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = [
        'company', 'sblo_name', 'title', 'email', 'phone', 'address',
        'naics', 'source', 'contract_count', 'total_contract_value',
        'agencies', 'has_subcontract_plan', 'has_contact_info'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(merged_companies)

# Calculate statistics
email_count = sum(1 for c in merged_companies if c['email'])
phone_count = sum(1 for c in merged_companies if c['phone'])
both_count = sum(1 for c in merged_companies if c['email'] and c['phone'])
total_value = sum(float(c['total_contract_value']) for c in merged_companies if c['total_contract_value'])

print("\n" + "=" * 80)
print("MASTER DATABASE CREATED")
print("=" * 80)
print(f"\n📊 STATISTICS:")
print(f"   • Total companies: {len(merged_companies):,}")
print(f"   • With email: {email_count:,}")
print(f"   • With phone: {phone_count:,}")
print(f"   • With both: {both_count:,}")
print(f"   • Total contract value: ${total_value:,.2f}")
print(f"\n📄 Saved to: {output_file}")
print("\n🎯 NEXT STEP: Generate searchable web database")
print("=" * 80)
