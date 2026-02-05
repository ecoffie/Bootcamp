#!/usr/bin/env python3
"""
Cross-reference companies 51-100 with existing compiled SBLO list
"""

import csv
from difflib import SequenceMatcher

def similar(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Companies 51-100 extracted from file
companies_51_100 = [
    ("50", "ALION SCIENCE AND TECHNOLOGY CORPORATION", "$1,631,620,204"),
    ("51", "UNITED LAUNCH ALLIANCE LLC", "$1,628,789,353"),
    ("52", "AT&T CORP", "$1,534,431,337"),
    ("53", "SERCO INC", "$1,477,534,032"),
    ("54", "UNITED CLEANUP OAK RIDGE LLC", "$1,469,539,175"),
    ("55", "IRON BOW TECHNOLOGIES LLC", "$1,466,670,357"),
    ("56", "AMENTUM SERVICES INC", "$1,338,389,028"),
    ("57", "INTERNATIONAL BUSINESS MACHINES CORPORATION", "$1,330,610,689"),  # IBM
    ("58", "BLUE CROSS AND BLUE SHIELD OF SOUTH CAROLINA", "$1,283,666,222"),
    ("59", "SALIENT CRGT INC", "$1,271,566,092"),  # Duplicate of #35
    ("60", "HENSEL PHELPS CONSTRUCTION CO", "$1,270,454,844"),
    ("61", "NAMMO PERRY INC", "$1,264,545,430"),
    ("62", "MEDLINE INDUSTRIES LP", "$1,186,990,806"),
    ("63", "ROCKWELL COLLINS INC", "$1,154,974,165"),
    ("64", "PERATON INC", "$1,143,793,955"),
    ("65", "APTIM FEDERAL SERVICES LLC", "$1,131,017,123"),
    ("66", "HONEYWELL FEDERAL MANUFACTURING & TECHNOLOGIES LLC", "$1,128,205,331"),
    ("67", "VALERO ENERGY CORPORATION", "$1,127,256,162"),
    ("68", "MANTECH TSG-2 JOINT VENTURE", "$1,105,581,667"),
    ("69", "OLIN CORPORATION", "$1,092,838,904"),
    ("70", "TEXTRON INC", "$1,023,393,431"),
    ("71", "CENTRAL PLATEAU CLEANUP COMPANY LLC", "$1,013,077,761"),
    ("72", "WESTAT INC", "$992,098,233"),
    ("73", "CGI INC", "$983,719,152"),
    ("74", "BLUEFORGE ALLIANCE", "$980,744,520"),
    ("75", "TRUMBULL CORPORATION AND BRAYMAN CONSTRUCTION", "$977,993,087"),
    ("76", "JACOBS TECHNOLOGY INC", "$975,601,066"),
    ("77", "GENERAL DYNAMICS LAND SYSTEMS INC", "$972,577,794"),
    ("78", "LAUREL TECHNOLOGIES PARTNERSHIP", "$941,992,783"),
    ("79", "OPTUMSERVE HEALTH SERVICES INC", "$922,213,299"),
    ("80", "AUSTAL LIMITED", "$912,985,894"),
    ("81", "BATH IRON WORKS CORPORATION", "$905,219,941"),
    ("82", "CREDENCE MANAGEMENT SOLUTIONS LLC", "$898,752,341"),
    ("83", "BALL CORPORATION", "$878,670,235"),
    ("84", "OSHKOSH CORPORATION", "$863,316,013"),
    ("85", "MVM INC", "$854,318,157"),
    ("86", "BAE SYSTEMS TECHNOLOGY SOLUTIONS & SERVICES INC", "$846,754,737"),
    ("87", "L3HARRIS GLOBAL COMMUNICATIONS INC", "$825,938,856"),
    ("88", "CLARK CONSTRUCTION GROUP LLC", "$824,649,091"),
    ("89", "BROOKHAVEN SCIENCE ASSOCIATES LLC", "$805,822,525"),
    ("90", "BELL BOEING JOINT PROJECT OFFICE", "$798,555,919"),
    ("91", "GREAT LAKES DREDGE & DOCK CORPORATION", "$793,515,717"),
    ("92", "LEIDOS BIOMEDICAL RESEARCH INC", "$779,690,864"),
    ("93", "FERMI RESEARCH ALLIANCE LLC", "$768,652,939"),
    ("94", "EXPRESS SCRIPTS INC", "$754,587,660"),
    ("95", "LEIDOS INC", "$753,753,275"),
    ("96", "CAE USA INC", "$753,523,215"),
    ("97", "ASGN INCORPORATED", "$752,921,910"),
    ("98", "CARAHSOFT TECHNOLOGY CORP", "$740,406,642"),
    ("99", "GEORGIA TECH RESEARCH CORPORATION", "$701,897,110"),
]

# Read compiled SBLO list
compiled_file = '/Users/ericcoffie/Bootcamp/sblo-list-compiled.csv'
companies_with_contacts = {}
need_research = []

print("=" * 80)
print("CROSS-REFERENCE: Companies 51-100 vs Existing SBLO Database")
print("=" * 80)

with open(compiled_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    all_rows = list(reader)

    for rank, target_company, value in companies_51_100:
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
            print(f"   ✅ FOUND {len(found_contacts)} contact(s)")
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
            print(f"   ❌ NOT FOUND")
            need_research.append((rank, target_company, value))

print("\n" + "=" * 80)
print("SUMMARY - Companies 51-100")
print("=" * 80)
print(f"✅ Companies with contacts: {len(companies_with_contacts)}/50")
print(f"❌ Companies needing research: {len(need_research)}/50")

if need_research:
    print(f"\n🔬 COMPANIES NEEDING RESEARCH ({len(need_research)}):")
    for rank, company, value in need_research:
        print(f"   #{rank} - {company} ({value})")

# Create output file
output_file = '/Users/ericcoffie/Bootcamp/companies-51-100-existing-contacts.csv'
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    fieldnames = ['rank', 'target_company', 'contract_value', 'matched_company', 'sblo_name', 'email', 'phone', 'source', 'status']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for rank, company, value in companies_51_100:
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
