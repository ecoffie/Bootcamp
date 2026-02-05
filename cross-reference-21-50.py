#!/usr/bin/env python3
"""
Cross-reference companies 21-50 with existing compiled SBLO list
"""

import csv
from difflib import SequenceMatcher

def similar(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Companies 21-50 to check
companies_21_50 = [
    ("21", "HONEYWELL INTERNATIONAL INC", "$4,067,873,163"),
    ("22", "ACCENTURE FEDERAL SERVICES LLC", "$3,916,762,889"),
    ("23", "BEYOND NEW HORIZONS LLC", "$3,788,828,058"),
    ("24", "LOCKHEED MARTIN CORP", "$3,438,185,262"),  # Duplicate of #19
    ("25", "SMARTRONIX LLC", "$3,437,888,078"),
    ("26", "SPACE EXPLORATION TECHNOLOGIES CORP", "$3,428,134,460"),  # SpaceX
    ("27", "SAN ANTONIO FAMILY ENDEAVORS INC", "$3,329,900,357"),
    ("28", "HII MISSION TECHNOLOGIES CORP", "$3,050,209,031"),
    ("29", "RAYTHEON COMPANY", "$2,978,919,610"),
    ("30", "PERATON CORP", "$2,971,989,197"),
    ("31", "THALLE CONSTRUCTION CO INC", "$2,903,365,914"),
    ("32", "HUNTINGTON INGALLS INDUSTRIES INC", "$2,877,924,806"),  # Variation of #7
    ("33", "JOHNS HOPKINS UNIVERSITY", "$2,816,866,089"),
    ("34", "BAE SYSTEMS LAND & ARMAMENTS LP", "$2,712,833,732"),
    ("35", "SALIENT CRGT INC", "$2,673,668,217"),
    ("36", "BECHTEL PLANT MACHINERY INC", "$2,308,047,737"),
    ("37", "NORTHROP GRUMMAN CORPORATION", "$2,271,796,813"),  # Variation of #11
    ("38", "TECHFLOW INC", "$2,157,348,169"),
    ("39", "KBR WYLE SERVICES LLC", "$2,121,041,705"),
    ("40", "AMENTUM GOVERNMENT SERVICES HOLDINGS LLC", "$1,999,225,539"),
    ("41", "L3HARRIS TECHNOLOGIES INC", "$1,992,158,813"),
    ("42", "MANTECH INTERNATIONAL CORPORATION", "$1,980,820,023"),
    ("43", "CALIFORNIA INSTITUTE OF TECHNOLOGY", "$1,977,598,972"),
    ("44", "RAYTHEON/LOCKHEED MARTIN JAVELIN JV", "$1,922,094,922"),
    ("45", "AM GENERAL LLC", "$1,786,267,768"),
    ("46", "RAYTHEON TECHNOLOGIES CORPORATION", "$1,779,497,841"),
    ("47", "QTC MEDICAL SERVICES INC", "$1,703,176,191"),
    ("48", "THE MITRE CORPORATION", "$1,698,933,474"),
    ("49", "CERNER CORPORATION", "$1,690,841,789"),
    ("50", "BATTELLE MEMORIAL INSTITUTE", "$1,665,819,076"),  # Need to add this one
]

# Read compiled SBLO list
compiled_file = '/Users/ericcoffie/Bootcamp/sblo-list-compiled.csv'
companies_with_contacts = {}
need_research = []

print("=" * 80)
print("CROSS-REFERENCE: Companies 21-50 vs Existing SBLO Database")
print("=" * 80)

with open(compiled_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    all_rows = list(reader)

    for rank, target_company, value in companies_21_50:
        print(f"\n🔍 #{rank} - {target_company} ({value})")
        found_contacts = []

        for row in all_rows:
            company_name = row.get('company', '').strip()

            # Check for close match
            if similar(target_company, company_name) > 0.6 or \
               any(word in company_name.upper() for word in target_company.split() if len(word) > 4):

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
            print(f"   ✅ FOUND {len(found_contacts)} contact(s) in database")
            companies_with_contacts[target_company] = {
                'rank': rank,
                'value': value,
                'contacts': found_contacts
            }
            # Show best contact
            best = next((c for c in found_contacts if c['sblo_name'] and c['email']), found_contacts[0])
            if best['sblo_name']:
                print(f"      • {best['sblo_name']}: {best['email']}")
            else:
                print(f"      • {best['email']}")
        else:
            print(f"   ❌ NOT FOUND - needs research")
            need_research.append((rank, target_company, value))

print("\n" + "=" * 80)
print("SUMMARY - Companies 21-50")
print("=" * 80)
print(f"✅ Companies with contacts: {len(companies_with_contacts)}/30")
print(f"❌ Companies needing research: {len(need_research)}/30")

if need_research:
    print("\n🔬 COMPANIES NEEDING RESEARCH:")
    for rank, company, value in need_research:
        print(f"   #{rank} - {company} ({value})")

# Create output file
output_file = '/Users/ericcoffie/Bootcamp/companies-21-50-existing-contacts.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    fieldnames = ['rank', 'target_company', 'contract_value', 'matched_company', 'sblo_name', 'email', 'phone', 'source', 'status']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for rank, company, value in companies_21_50:
        if company in companies_with_contacts:
            data = companies_with_contacts[company]
            contacts = data['contacts']
            best_contact = next((c for c in contacts if c['sblo_name'] and c['email']), contacts[0])
            writer.writerow({
                'rank': rank,
                'target_company': company,
                'contract_value': value,
                'matched_company': best_contact['company'],
                'sblo_name': best_contact['sblo_name'],
                'email': best_contact['email'],
                'phone': best_contact['phone'],
                'source': best_contact['source'],
                'status': 'FOUND'
            })
        else:
            writer.writerow({
                'rank': rank,
                'target_company': company,
                'contract_value': value,
                'matched_company': '',
                'sblo_name': '',
                'email': '',
                'phone': '',
                'source': '',
                'status': 'NEEDS RESEARCH'
            })

print(f"\n📄 Output saved to: {output_file}")
