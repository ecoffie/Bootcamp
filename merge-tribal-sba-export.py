#!/usr/bin/env python3
"""
Merge Tribal SBA Export (1,172 companies) into master database
"""

import csv
import re

def clean_hyperlink(text):
    """Remove Excel HYPERLINK formula and extract company name"""
    if not text:
        return text
    # Pattern: =HYPERLINK( "url", "Company Name" )
    match = re.search(r'HYPERLINK\([^,]+,\s*"([^"]+)"\s*\)', text)
    if match:
        return match.group(1).strip()
    return text.strip()

def normalize_company_name(name):
    """Normalize company name for matching"""
    name = name.upper()
    suffixes = [
        ' LLC', ' INC', ' INCORPORATED', ' CORP', ' CORPORATION',
        ' LTD', ' LIMITED', ' CO', ' COMPANY', ' LP', ' L.P.',
        ',', '.'
    ]
    for suffix in suffixes:
        name = name.replace(suffix, '')
    return name.strip()

# Read existing master database
master_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
master_companies = {}

print("=" * 80)
print("MERGING TRIBAL SBA EXPORT INTO MASTER DATABASE")
print("=" * 80)

print("\n📊 Loading master database...")
with open(master_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        normalized = normalize_company_name(row['company'])
        master_companies[normalized] = row

print(f"✅ Loaded {len(master_companies)} companies from master database")

# Read tribal SBA export
tribal_file = '/Users/ericcoffie/Bootcamp/SBLO List /Tribal SBS_export_[20251209].csv'
tribal_data = []

print("\n📊 Loading Tribal SBA export...")
with open(tribal_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Clean the business name (remove HYPERLINK formula)
        business_name = clean_hyperlink(row.get('Business name', ''))
        if business_name:
            tribal_data.append({
                'business_name': business_name,
                'contact_name': row.get("Contact person's name", '').strip(),
                'email': row.get("Contact person's email", '').strip(),
                'address_line1': row.get('Address line 1', '').strip(),
                'address_line2': row.get('Address line 2', '').strip(),
                'city': row.get('City', '').strip(),
                'state': row.get('State', '').strip(),
                'zipcode': row.get('Zipcode', '').strip(),
                'primary_naics': row.get('Primary NAICS code', '').strip(),
                'all_naics': row.get('All NAICS codes', '').strip(),
                'certifications': row.get('Active SBA certifications', '').strip(),
                'capabilities': row.get('Capabilities narrative', '').strip(),
            })

print(f"✅ Loaded {len(tribal_data)} tribal businesses from SBA export")

# Match and enhance existing companies, add new ones
matched = 0
new_added = 0
updated_list = list(master_companies.values())

for tribal in tribal_data:
    normalized = normalize_company_name(tribal['business_name'])

    if normalized in master_companies:
        # Update existing company with tribal information
        company = master_companies[normalized]

        # Add tribal tag to source if not already present
        if 'Tribal' not in company.get('source', ''):
            company['source'] = f"{company.get('source', '')} | Tribal 8(a) SBA Certified".strip(' |')

        # Update contact info if we have better data
        if tribal['email'] and not company.get('email'):
            company['email'] = tribal['email']
        if tribal['contact_name'] and not company.get('sblo_name'):
            company['sblo_name'] = tribal['contact_name']

        matched += 1
    else:
        # Add as new tribal company
        full_address = f"{tribal['address_line1']} {tribal['address_line2']}, {tribal['city']}, {tribal['state']} {tribal['zipcode']}".strip(', ')

        updated_list.append({
            'company': tribal['business_name'],
            'sblo_name': tribal['contact_name'],
            'title': 'Contact',
            'email': tribal['email'],
            'phone': '',
            'address': full_address,
            'naics': tribal['all_naics'],
            'source': 'Tribal 8(a) SBA Certified',
            'contract_count': '',
            'total_contract_value': '',
            'agencies': '',
            'has_subcontract_plan': 'True',
            'has_contact_info': 'Yes' if tribal['email'] else 'No'
        })
        new_added += 1

print(f"\n✅ Matched and enhanced: {matched} existing companies")
print(f"✅ Added new tribal companies: {new_added}")

# Sort by total contract value (descending), then by company name
updated_list.sort(
    key=lambda x: (
        -float(x['total_contract_value']) if x.get('total_contract_value') and x['total_contract_value'] else 0,
        x['company'].upper()
    )
)

# Write updated database
output_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = [
        'company', 'sblo_name', 'title', 'email', 'phone', 'address',
        'naics', 'source', 'contract_count', 'total_contract_value',
        'agencies', 'has_subcontract_plan', 'has_contact_info'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_list)

# Calculate statistics
total_companies = len(updated_list)
tribal_count = sum(1 for c in updated_list if 'Tribal' in c.get('source', ''))
email_count = sum(1 for c in updated_list if c.get('email'))
phone_count = sum(1 for c in updated_list if c.get('phone'))
both_count = sum(1 for c in updated_list if c.get('email') and c.get('phone'))
total_value = sum(float(c['total_contract_value']) for c in updated_list if c.get('total_contract_value') and c['total_contract_value'])

print("\n" + "=" * 80)
print("UPDATED DATABASE STATISTICS")
print("=" * 80)
print(f"\n📊 Total companies: {total_companies:,}")
print(f"   • Original database: {len(master_companies):,}")
print(f"   • New tribal companies added: {new_added:,}")
print(f"   • Total Tribal 8(a) companies: {tribal_count:,}")
print(f"\n📧 Contact Information:")
print(f"   • With email: {email_count:,}")
print(f"   • With phone: {phone_count:,}")
print(f"   • With both: {both_count:,}")
print(f"\n💰 Total contract value: ${total_value:,.2f}")
print(f"\n📄 Updated: {output_file}")
print("\n🎯 Search 'Tribal' to find all {tribal_count:,} tribal companies!")
print("=" * 80)
