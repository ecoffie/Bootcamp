#!/usr/bin/env python3
"""
Cross-reference user's complete company list with extracted contacts
Identify missing companies and verify completeness
"""

import csv
from pathlib import Path

# User's complete list
COMPLETE_COMPANY_LIST = [
    "AArete",
    "ABS Group Consulting",
    "Accenture",
    "Acuity International",
    "AECOM",
    "Akima Global Services",
    "Amentum",
    "APTIM",
    "BAE Systems Intelligence & Security",
    "Battelle National Biodefense Institute, LLC",
    "BI Incorporated",
    "Bollinger Shipyards",
    "Booz Allen Hamilton",
    "CACI Federal, Inc.",
    "CDM SMITH",
    "CGI Federal",
    "CH2M Hill",
    "Clark Construction",
    "CleanHarbors",
    "Composite Analysis Group",
    "CoreCivic",
    "Covenant Aviation Security, LLC",
    "Deloitte Services, LP",
    "Deployed Resources",
    "Dewberry",
    "Environmental Chemical Corporation (ECC)",
    "Ernst & Young LLP",
    "FJC Security Services, Inc.",
    "Fluor Government Group",
    "G4S Secure Solutions (USA) Inc.",
    "GE Power",
    "General Atomics Aeronautical Systems, Inc.",
    "Gilbane Building Company",
    "Grant Thornton, LLP",
    "Grunley Construction Company, Inc.",
    "The Haskell Company",
    "General Dynamics Information Technology",
    "IBM US Federal",
    "Insitu",
    "ICF International",
    "Huntington Ingalls Industries",
    "Jacobs Engineering Group, Inc.",
    "KPMG",
    "L3Harris",
    "Leidos",
    "Leo A Daly",
    "Lockheed Martin - Information Systems & Global Solutions",
    "Loyal Source",
    "Maximus Federal",
    "Mantech",
    "McDean",
    "Michael Baker Jr., Inc.",
    "Mitre",
    "Monster Government Solutions LLC",
    "Mortenson",
    "M V M, Inc.",
    "Motorola Solutions, Inc.",
    "Neopost Inc.",
    "Noblis",
    "Noresco LLC",
    "Northrop Grumman (Information Technology)",
    "NTTData Federal",
    "Paragon Systems",
    "Peraton",
    "Rapiscan",
    "ReadyAmerica",
    "SAIC",
    "Salient",
    "Serco, Inc.",
    "THE BOEING COMPANY",
    "THE GEO GROUP",
    "The Rand Company",
    "Triple Canopy",
    "Verizon",
    "Whiting-Turner",
    "WSP"
]

def normalize_company_name(name):
    """Normalize company name for comparison"""
    return name.strip().lower().replace(',', '').replace('.', '').replace('inc', '').replace('llc', '').replace('lp', '').strip()

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   DHS Companies - Cross-Reference & Verification   ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    print(f"📋 Total companies in user's list: {len(COMPLETE_COMPANY_LIST)}")
    
    # Load extracted contacts
    extracted_file = Path('dhs-contacts-full.csv')
    extracted_companies = set()
    extracted_contacts = []
    
    if extracted_file.exists():
        with open(extracted_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get('company', '').strip()
                if company:
                    extracted_companies.add(normalize_company_name(company))
                    extracted_contacts.append(row)
    
    print(f"📊 Companies in extracted file: {len(extracted_companies)}")
    
    # Normalize user's list
    user_companies_normalized = {normalize_company_name(name): name for name in COMPLETE_COMPANY_LIST}
    
    # Find missing companies
    missing_companies = []
    for normalized, original in user_companies_normalized.items():
        if normalized not in extracted_companies:
            missing_companies.append(original)
    
    print(f"\n❌ Missing companies: {len(missing_companies)}")
    
    if missing_companies:
        print("\n📋 Missing companies list:")
        for i, company in enumerate(missing_companies, 1):
            print(f"   {i:2d}. {company}")
    
    # Find companies we have
    found_companies = []
    for normalized, original in user_companies_normalized.items():
        if normalized in extracted_companies:
            found_companies.append(original)
    
    print(f"\n✅ Found companies: {len(found_companies)}/{len(COMPLETE_COMPANY_LIST)}")
    
    # Create complete list with missing companies marked
    complete_contacts = []
    
    # Add existing contacts
    for contact in extracted_contacts:
        complete_contacts.append({
            'company': contact.get('company', ''),
            'sblo_name': contact.get('sblo_name', ''),
            'title': contact.get('title', 'SBLO'),
            'email': contact.get('email', ''),
            'phone': contact.get('phone', ''),
            'website': contact.get('website', ''),
            'naics': contact.get('naics', ''),
            'source': contact.get('source', 'DHS Prime Contractors Page'),
            'status': 'EXTRACTED'
        })
    
    # Add missing companies as placeholders
    for company in missing_companies:
        complete_contacts.append({
            'company': company,
            'sblo_name': '[NEEDS EXTRACTION]',
            'title': 'SBLO',
            'email': '[NEEDS EXTRACTION]',
            'phone': '',
            'website': '',
            'naics': '',
            'source': 'DHS Prime Contractors Page',
            'status': 'MISSING'
        })
    
    # Save complete list
    output_file = Path('dhs-contacts-verified.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'naics', 'source', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(complete_contacts)
    
    print(f"\n💾 Saved complete verified list to: {output_file}")
    print(f"   Total entries: {len(complete_contacts)}")
    print(f"   Extracted: {len([c for c in complete_contacts if c['status'] == 'EXTRACTED'])}")
    print(f"   Missing: {len([c for c in complete_contacts if c['status'] == 'MISSING'])}")
    
    print("\n📊 Summary:")
    print(f"   User's list: {len(COMPLETE_COMPANY_LIST)} companies")
    print(f"   Extracted: {len(found_companies)} companies")
    print(f"   Missing: {len(missing_companies)} companies")
    print(f"   Coverage: {len(found_companies)/len(COMPLETE_COMPANY_LIST)*100:.1f}%")

if __name__ == '__main__':
    main()




