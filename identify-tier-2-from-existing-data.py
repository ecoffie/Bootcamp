#!/usr/bin/env python3
"""
Identify Tier 2 candidates from existing SBLO database
Strategy: Companies in our database that are NOT in the Top 100 are likely Tier 2 suppliers
"""

import csv

# Read Top 100 SBA companies
top_100_file = '/Users/ericcoffie/Bootcamp/sba-top-100-research-list.csv'
top_100_companies = set()

print("=" * 80)
print("IDENTIFYING TIER 2 SUPPLIERS FROM EXISTING DATABASE")
print("=" * 80)

with open(top_100_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = row['company'].upper().strip()
        top_100_companies.add(company)

print(f"\n📊 Loaded {len(top_100_companies)} Top 100 (Tier 1) companies")

# Read compiled SBLO list
compiled_file = '/Users/ericcoffie/Bootcamp/sblo-list-compiled.csv'
tier_2_candidates = []
tier_1_matches = []

with open(compiled_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = row.get('company', '').strip()
        email = row.get('email', '').strip()
        phone = row.get('phone', '').strip()

        if not company or (not email and not phone):
            continue

        # Check if this company is in Top 100
        company_upper = company.upper()
        is_tier_1 = False

        for top_100 in top_100_companies:
            # Check for partial matches (subsidiaries, divisions)
            top_100_words = set(top_100.split())
            company_words = set(company_upper.split())

            # If they share 2+ significant words, likely same company
            common_words = top_100_words & company_words
            significant_common = [w for w in common_words if len(w) > 4]

            if len(significant_common) >= 2:
                is_tier_1 = True
                break

        if is_tier_1:
            tier_1_matches.append(row)
        else:
            tier_2_candidates.append(row)

print(f"📊 Found {len(tier_1_matches)} Tier 1 (Top 100 primes) in database")
print(f"📊 Found {len(tier_2_candidates)} potential Tier 2 suppliers")

# Deduplicate Tier 2 by company name
tier_2_unique = {}
for candidate in tier_2_candidates:
    company = candidate['company'].upper()
    if company not in tier_2_unique:
        tier_2_unique[company] = candidate

print(f"📊 {len(tier_2_unique)} unique Tier 2 companies")

# Write Tier 2 list
output_file = '/Users/ericcoffie/Bootcamp/TIER-2-SUPPLIER-CONTACTS.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['company', 'sblo_name', 'email', 'phone', 'naics', 'source', 'tier_classification']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for company, data in sorted(tier_2_unique.items()):
        writer.writerow({
            'company': data['company'],
            'sblo_name': data.get('sblo_name', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'naics': data.get('naics', ''),
            'source': data.get('source', ''),
            'tier_classification': 'Tier 2 Subcontractor (Not in Top 100 Primes)'
        })

# Count with email vs phone
tier_2_with_email = sum(1 for d in tier_2_unique.values() if d.get('email'))
tier_2_with_phone = sum(1 for d in tier_2_unique.values() if d.get('phone'))
tier_2_with_both = sum(1 for d in tier_2_unique.values() if d.get('email') and d.get('phone'))

print(f"\n✅ TIER 2 STATISTICS:")
print(f"   • Total Tier 2 companies: {len(tier_2_unique)}")
print(f"   • With email: {tier_2_with_email} ({tier_2_with_email/len(tier_2_unique)*100:.1f}%)")
print(f"   • With phone: {tier_2_with_phone} ({tier_2_with_phone/len(tier_2_unique)*100:.1f}%)")
print(f"   • With both: {tier_2_with_both} ({tier_2_with_both/len(tier_2_unique)*100:.1f}%)")

print(f"\n📄 Saved to: {output_file}")
print("=" * 80)

# Show sample Tier 2 companies
print("\n📋 SAMPLE TIER 2 COMPANIES:")
count = 0
for company, data in sorted(tier_2_unique.items()):
    if data.get('email'):
        print(f"   • {data['company']}: {data.get('email', 'N/A')}")
        count += 1
        if count >= 10:
            break
