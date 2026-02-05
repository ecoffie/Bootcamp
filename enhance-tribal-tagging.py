#!/usr/bin/env python3
"""
Enhance existing companies with Tribal 8(a) tags and information
"""

import csv

# Read existing master database
master_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
master_companies = {}

print("=" * 80)
print("ENHANCING DATABASE WITH TRIBAL 8(a) INFORMATION")
print("=" * 80)

print("\n📊 Loading master database...")
with open(master_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        master_companies[row['company'].upper()] = row

print(f"✅ Loaded {len(master_companies)} companies from master database")

# Read tribal data
tribal_file = '/Users/ericcoffie/Bootcamp/tribal-8a-research-template.csv'
tribal_info = {}

print("\n📊 Loading tribal 8(a) information...")
with open(tribal_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tribal_info[row['company'].upper()] = row

print(f"✅ Loaded {len(tribal_info)} tribal companies")

# Enhance master database with tribal tags
enhanced_count = 0
for company_upper, tribal_data in tribal_info.items():
    if company_upper in master_companies:
        # Update source to indicate tribal status
        current_source = master_companies[company_upper].get('source', '')
        if 'Tribal' not in current_source:
            master_companies[company_upper]['source'] = f"{current_source} | Tribal 8(a)" if current_source else "Tribal 8(a)"
        enhanced_count += 1

print(f"✅ Enhanced {enhanced_count} companies with Tribal 8(a) designation")

# Convert back to list and sort
enhanced_companies = list(master_companies.values())
enhanced_companies.sort(
    key=lambda x: float(x['total_contract_value']) if x.get('total_contract_value') and x['total_contract_value'] else 0,
    reverse=True
)

# Write enhanced database
output_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = [
        'company', 'sblo_name', 'title', 'email', 'phone', 'address',
        'naics', 'source', 'contract_count', 'total_contract_value',
        'agencies', 'has_subcontract_plan', 'has_contact_info'
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(enhanced_companies)

# Calculate statistics
tribal_tagged = sum(1 for c in enhanced_companies if 'Tribal' in c.get('source', ''))
total_value = sum(float(c['total_contract_value']) for c in enhanced_companies if c.get('total_contract_value') and c['total_contract_value'])

print("\n" + "=" * 80)
print("ENHANCED DATABASE STATISTICS")
print("=" * 80)
print(f"\n📊 Total companies: {len(enhanced_companies):,}")
print(f"   • Tribal 8(a) companies: {tribal_tagged:,}")
print(f"   • Total contract value: ${total_value:,.2f}")
print(f"\n📄 Updated: {output_file}")
print("\n🎯 Tribal companies now searchable with 'Tribal' keyword")
print("=" * 80)
