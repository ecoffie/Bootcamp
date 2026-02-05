#!/usr/bin/env python3
"""
Merge Tribal 8(a) companies into the master database
"""

import csv

# Read existing master database
master_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
master_companies = []

print("=" * 80)
print("MERGING TRIBAL 8(a) COMPANIES INTO MASTER DATABASE")
print("=" * 80)

print("\n📊 Loading master database...")
with open(master_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        master_companies.append(row)

print(f"✅ Loaded {len(master_companies)} companies from master database")

# Read tribal data
tribal_file = '/Users/ericcoffie/Bootcamp/tribal-8a-research-template.csv'
tribal_companies = []

print("\n📊 Loading tribal 8(a) companies...")
with open(tribal_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tribal_companies.append(row)

print(f"✅ Loaded {len(tribal_companies)} tribal companies")

# Create a set of existing company names (uppercase for matching)
existing_companies = {c['company'].upper() for c in master_companies}

# Add tribal companies that aren't already in the database
new_companies_added = 0
already_exists = 0

for tribal in tribal_companies:
    company_name = tribal['company'].strip()
    company_upper = company_name.upper()

    if company_upper not in existing_companies:
        # Add as new company
        master_companies.append({
            'company': company_name,
            'sblo_name': tribal.get('sblo_contact', ''),
            'title': '',
            'email': tribal.get('email', ''),
            'phone': tribal.get('phone', ''),
            'address': '',
            'naics': tribal.get('naics', ''),
            'source': 'Tribal 8(a) Research',
            'contract_count': tribal.get('contract_count', ''),
            'total_contract_value': tribal.get('total_contract_value', ''),
            'agencies': tribal.get('agencies', ''),
            'has_subcontract_plan': 'True',  # Tribal 8(a) companies typically have plans
            'has_contact_info': 'Yes' if tribal.get('email') or tribal.get('phone') else 'No'
        })
        new_companies_added += 1
        existing_companies.add(company_upper)
    else:
        already_exists += 1

print(f"\n✅ Added {new_companies_added} new tribal companies")
print(f"ℹ️  {already_exists} tribal companies already in database")

# Sort by total contract value (descending)
master_companies.sort(
    key=lambda x: float(x['total_contract_value']) if x.get('total_contract_value') and x['total_contract_value'] else 0,
    reverse=True
)

# Write updated database
output_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-MASTER-DATABASE-WITH-TRIBAL.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = [
        'company', 'sblo_name', 'title', 'email', 'phone', 'address',
        'naics', 'source', 'contract_count', 'total_contract_value',
        'agencies', 'has_subcontract_plan', 'has_contact_info'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(master_companies)

# Calculate statistics
total_companies = len(master_companies)
email_count = sum(1 for c in master_companies if c.get('email'))
phone_count = sum(1 for c in master_companies if c.get('phone'))
both_count = sum(1 for c in master_companies if c.get('email') and c.get('phone'))
tribal_count = sum(1 for c in master_companies if c.get('source') == 'Tribal 8(a) Research')
total_value = sum(float(c['total_contract_value']) for c in master_companies if c.get('total_contract_value') and c['total_contract_value'])

print("\n" + "=" * 80)
print("UPDATED DATABASE STATISTICS")
print("=" * 80)
print(f"\n📊 Total companies: {total_companies:,}")
print(f"   • Original: {total_companies - new_companies_added:,}")
print(f"   • New tribal: {new_companies_added:,}")
print(f"   • Tribal 8(a) companies: {tribal_count:,}")
print(f"\n📧 Contact Information:")
print(f"   • With email: {email_count:,}")
print(f"   • With phone: {phone_count:,}")
print(f"   • With both: {both_count:,}")
print(f"\n💰 Total contract value: ${total_value:,.2f}")
print(f"\n📄 Saved to: {output_file}")
print("\n🎯 NEXT STEP: Regenerate searchable database")
print("=" * 80)
