#!/usr/bin/env python3
"""
Cross-reference top 20 SBA companies with existing compiled SBLO list
"""

import csv
from difflib import SequenceMatcher

def similar(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Top 20 SBA companies to check
top_20_companies = [
    "PANTEXAS DETERRENCE LLC",
    "OPTUM PUBLIC SECTOR SOLUTIONS INC",
    "TRIWEST HEALTHCARE ALLIANCE CORP",
    "SIERRA NEVADA COMPANY LLC",
    "BOOZ ALLEN HAMILTON INC",
    "HUNTINGTON INGALLS INC",
    "GENERAL DYNAMICS CORPORATION",
    "MCKESSON CORPORATION",
    "CACI INC - FEDERAL",
    "NORTHROP GRUMMAN SYSTEMS CORPORATION",
    "DELOITTE CONSULTING LLP",
    "GENERAL ATOMIC TECHNOLOGIES CORPORATION",
    "GENERAL DYNAMICS INFORMATION TECHNOLOGY INC",
    "TRIAD NATIONAL SECURITY LLC",
    "SCIENCE APPLICATIONS INTERNATIONAL CORPORATION",
    "LEIDOS INC",
    "INTUITIVE MACHINES LLC",
    "LOCKHEED MARTIN CORPORATION",
    "VERTEX AEROSPACE LLC",
    "OPTUM PUBLIC SECTOR SOLUTIONS INC"
]

# Read compiled SBLO list
compiled_file = '/Users/ericcoffie/Bootcamp/sblo-list-compiled.csv'
matches_found = {}
companies_with_contacts = {}

print("=" * 80)
print("CROSS-REFERENCE: Top 20 SBA Companies vs Existing SBLO Database")
print("=" * 80)

with open(compiled_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    all_rows = list(reader)

    for target_company in top_20_companies:
        print(f"\n🔍 Searching for: {target_company}")
        found_contacts = []

        for row in all_rows:
            company_name = row.get('company', '').strip()

            # Check for close match
            if similar(target_company, company_name) > 0.7 or \
               any(word in company_name.upper() for word in target_company.split() if len(word) > 3):

                email = row.get('email', '').strip()
                sblo_name = row.get('sblo_name', '').strip()

                if email:  # Only include if has email
                    found_contacts.append({
                        'company': company_name,
                        'sblo_name': sblo_name,
                        'email': email,
                        'phone': row.get('phone', '').strip(),
                        'source': row.get('source', '').strip()
                    })

        if found_contacts:
            print(f"   ✅ FOUND {len(found_contacts)} contact(s) in database:")
            companies_with_contacts[target_company] = found_contacts
            for contact in found_contacts:
                if contact['sblo_name']:
                    print(f"      • {contact['sblo_name']}: {contact['email']}")
                elif contact['email']:
                    print(f"      • {contact['email']}")
        else:
            print(f"   ❌ NOT FOUND - needs research")
            matches_found[target_company] = None

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"✅ Companies with contacts: {len(companies_with_contacts)}/20")
print(f"❌ Companies needing research: {20 - len(companies_with_contacts)}/20")

print("\n📋 COMPANIES ALREADY IN DATABASE:")
for company in sorted(companies_with_contacts.keys()):
    print(f"   ✅ {company}")

print("\n🔬 COMPANIES NEEDING RESEARCH:")
need_research = [c for c in top_20_companies if c not in companies_with_contacts]
for company in need_research:
    print(f"   ❌ {company}")

# Create output file with best contacts for each company
output_file = '/Users/ericcoffie/Bootcamp/top-20-existing-contacts.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    fieldnames = ['rank', 'target_company', 'matched_company', 'sblo_name', 'email', 'phone', 'source', 'status']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for i, company in enumerate(top_20_companies, 1):
        if company in companies_with_contacts:
            contacts = companies_with_contacts[company]
            # Write the best contact (first one with email and name)
            best_contact = next((c for c in contacts if c['sblo_name'] and c['email']), contacts[0])
            writer.writerow({
                'rank': i,
                'target_company': company,
                'matched_company': best_contact['company'],
                'sblo_name': best_contact['sblo_name'],
                'email': best_contact['email'],
                'phone': best_contact['phone'],
                'source': best_contact['source'],
                'status': 'FOUND'
            })
        else:
            writer.writerow({
                'rank': i,
                'target_company': company,
                'matched_company': '',
                'sblo_name': '',
                'email': '',
                'phone': '',
                'source': '',
                'status': 'NEEDS RESEARCH'
            })

print(f"\n📄 Output saved to: {output_file}")
