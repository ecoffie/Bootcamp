#!/usr/bin/env python3
"""
Refine Tier 2 list by removing known Tier 1 companies
"""

import csv

# Expanded list of known Tier 1 companies (add more as we identify them)
TIER_1_KEYWORDS = [
    'LOCKHEED', 'BOEING', 'NORTHROP', 'GRUMMAN', 'RAYTHEON', 'RTX',
    'GENERAL DYNAMICS', 'LEIDOS', 'BOOZ ALLEN', 'SAIC', 'HUNTINGTON INGALLS',
    'CACI', 'DELOITTE', 'ACCENTURE', 'MANTECH', 'PERATON',
    'L3HARRIS', 'HARRIS', 'BAE SYSTEMS', 'AMENTUM', 'KBR',
    'HONEYWELL', 'TEXTRON', 'OSHKOSH', 'VERIZON', 'AT&T',
    'MCKESSON', 'OPTUM', 'TRIWEST', 'HUMANA', 'EXPRESS SCRIPTS',
    'BLUE CROSS', 'ANTHEM', 'UNITEDHEALTH', 'CIGNA',
    'IBM', 'MICROSOFT', 'ORACLE', 'GOOGLE', 'AMAZON', 'AWS',
    'DELL', 'HP', 'HPE', 'CISCO', 'INTEL',
    'LOCKHEED MARTIN', 'GENERAL ATOMICS', 'SIERRA NEVADA',
    'WHITING TURNER', 'WHITING-TURNER', 'BECHTEL', 'FLUOR', 'AECOM',
    'JACOBS', 'PARSONS', 'WSP', 'STANTEC', 'ARCADIS',
    'KIEWIT', 'SKANSKA', 'TURNER', 'CLARK CONSTRUCTION',
    'HENSEL PHELPS', 'SUFFOLK', 'GILBANE',
    'CGI', 'COGNIZANT', 'INFOSYS', 'WIPRO', 'TCS',
    'TATA CONSULTANCY', 'CAPGEMINI', 'DXC', 'UNISYS',
    'SERCO', 'MITRE', 'JOHNS HOPKINS', 'CALTECH', 'MIT',
    'BATTELLE', 'SRI', 'AEROSPACE CORPORATION',
    'UNITED LAUNCH', 'SPACEX', 'BLUE ORIGIN',
    'PFIZER', 'JOHNSON & JOHNSON', 'MERCK', 'ABBVIE',
    'CARDINAL HEALTH', 'AMERISOURCE', 'MCKESSON',
    'GENERAL ELECTRIC', 'GE AVIATION', 'PRATT & WHITNEY',
    'ROLLS ROYCE', 'SAFRAN', 'MTU',
    'BALL CORPORATION', 'ORBITAL ATK', 'AEROJET',
    'INTUITIVE MACHINES', 'AXIOM SPACE'
]

# Read current Tier 2 list
input_file = '/Users/ericcoffie/Bootcamp/TIER-2-FINAL-CONTACT-LIST.csv'
tier_1_found = []
tier_2_clean = []

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = row['company'].upper()

        # Check if company matches any Tier 1 keyword
        is_tier_1 = False
        for keyword in TIER_1_KEYWORDS:
            if keyword in company:
                is_tier_1 = True
                tier_1_found.append(row)
                break

        if not is_tier_1:
            tier_2_clean.append(row)

print("=" * 80)
print("REFINING TIER 2 LIST - REMOVING TIER 1 COMPANIES")
print("=" * 80)

print(f"\n❌ Found {len(tier_1_found)} Tier 1 companies in Tier 2 list:")
for company in sorted(tier_1_found, key=lambda x: x['company'])[:20]:
    print(f"   • {company['company']}")
if len(tier_1_found) > 20:
    print(f"   ... and {len(tier_1_found) - 20} more")

print(f"\n✅ Clean Tier 2 list: {len(tier_2_clean)} companies")

# Write cleaned Tier 2 list
output_file = '/Users/ericcoffie/Bootcamp/TIER-2-FINAL-CONTACT-LIST-CLEAN.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    if tier_2_clean:
        fieldnames = tier_2_clean[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tier_2_clean)

# Stats
email_count = sum(1 for c in tier_2_clean if c.get('email'))
phone_count = sum(1 for c in tier_2_clean if c.get('phone'))
both_count = sum(1 for c in tier_2_clean if c.get('email') and c.get('phone'))

print(f"\n📊 CLEAN TIER 2 STATISTICS:")
print(f"   • Total companies: {len(tier_2_clean)}")
print(f"   • With email: {email_count}")
print(f"   • With phone: {phone_count}")
print(f"   • With both: {both_count}")

print(f"\n📄 Saved to: {output_file}")

# Show sample of clean Tier 2
print(f"\n✅ SAMPLE CLEAN TIER 2 COMPANIES:")
count = 0
for company in sorted(tier_2_clean, key=lambda x: x['company'])[:15]:
    if company.get('email'):
        print(f"   • {company['company']}")
        count += 1

print("\n" + "=" * 80)

# Return counts for next step
print(f"\nREADY TO CREATE NEW PDF:")
print(f"  - {len(tier_2_clean)} companies")
print(f"  - {email_count} with email")
print(f"  - {phone_count} with phone")
