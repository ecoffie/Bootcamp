#!/usr/bin/env python3
"""
Update all Tier 2 batch CSV files with vendor portal information.
Based on research findings: Most Tier 2 companies require direct SBLO contact.
"""

import csv
import os

# Vendor portal data - specific companies that have portals or are subsidiaries
PORTAL_DATA = {
    # Batch 3
    "KPMG": {
        "vendor_registration_url": "https://kpmg.supplierone.co/",
        "portal_type": "Full Portal",
        "notes": "Uses Coupa Supplier Portal (CSP) for transactions. Supplier diversity registration at kpmg.supplierone.co. Invitation-based system."
    },
    "G4S Secure Solutions (USA) Inc.": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Note: G4S was acquired by Allied Universal. May use Allied Universal supplier portal - check with SBLO."
    },
    "GE Power": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "General Electric Power division. May use GE corporate supplier portal - contact SBLO for access."
    },
    "Grant Thornton, LLP": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Professional services firm. No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Grunley Construction Company, Inc.": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Construction services. No public vendor portal found. Contact SBLO for subcontractor registration."
    },
    "ICF International": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Consulting and technology services. No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Insitu": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Note: Insitu is a Boeing subsidiary. May use Boeing supplier portal (boeing.suppliergateway.com) or have separate system - contact SBLO."
    },
    "Leo A Daly": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Architecture and engineering. No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Loyal Source": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Healthcare and government services. No public vendor portal found. Contact SBLO for supplier registration."
    },
    "M V M, Inc.": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for vendor registration."
    },
    # Batch 4
    "Maximus Federal": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Government services. No public vendor portal found. Contact SBLO for supplier registration."
    },
    "McDean": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Michael Baker Jr., Inc.": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Engineering and consulting. No public vendor portal found. Contact SBLO for supplier registration."
    },
    "Monster Government Solutions LLC": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Mortenson": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Construction services. No public vendor portal found. Contact SBLO for subcontractor registration."
    },
    "Motorola Solutions, Inc.": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Technology and communications. Large company but no public vendor portal found. Contact SBLO for supplier registration."
    },
    "Neopost Inc.": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Note: Neopost rebranded to Quadient. Check quadient.com for supplier portal or contact SBLO."
    },
    "Noblis": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Science and technology consulting. No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Noresco LLC": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Energy services. No public vendor portal found. Contact SBLO for supplier registration."
    },
    "NTTData Federal": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "IT services. No public vendor portal found. Contact SBLO for supplier registration."
    },
    # Batch 5
    "Paragon Systems": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Security services. No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Rapiscan": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Security screening equipment. No public vendor portal found. Contact SBLO for supplier registration."
    },
    "ReadyAmerica": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Salient": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Note: Likely Salient CRGT. No public vendor portal found. Contact SBLO for supplier registration."
    },
    "THE GEO GROUP": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Corrections and detention services. No public vendor portal found. Contact SBLO for vendor registration."
    },
    "The Haskell Company": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Construction and engineering. No public vendor portal found. Contact SBLO for subcontractor registration."
    },
    "The Rand Company": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Note: Likely RAND Corporation. Research and analysis. No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Triple Canopy": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Note: Triple Canopy is part of Constellis. Check constellis.com for supplier portal or contact SBLO."
    },
}

def clean_company_name(name):
    """Clean company name for matching."""
    return name.strip().strip('"')

def update_batch_file(batch_file):
    """Update a batch CSV file with portal information."""
    if not os.path.exists(batch_file):
        print(f"File not found: {batch_file}")
        return 0
    
    rows = []
    updated_count = 0
    missing_companies = []
    
    with open(batch_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            company = clean_company_name(row.get('company', ''))
            clean_name = clean_company_name(row.get('clean_name', ''))
            
            # Skip invalid entries
            if company in ['Contract', 'In Search Of:', 'https://', 'Lavenia Kitchen', 
                          'Manager/ SBLO Sikorksy', 'Maranda Sterling', 'Officer GEA',
                          'Pasquele DeSanto', 'Small Business', 'Susan Turley', 'Virginia Foley',
                          'Amanda Bennett', 'Ariel Hooker']:
                rows.append(row)
                continue
            
            # Try to match company name or clean_name
            match_key = None
            for key in PORTAL_DATA.keys():
                if company == key or clean_name == key:
                    match_key = key
                    break
                # Also check partial matches for subsidiaries
                if key.lower() in company.lower() or key.lower() in clean_name.lower():
                    match_key = key
                    break
            
            if match_key and PORTAL_DATA[match_key]:
                portal_info = PORTAL_DATA[match_key]
                # Only update if fields are empty
                if not row.get('vendor_registration_url', '').strip():
                    row['vendor_registration_url'] = portal_info.get('vendor_registration_url', '')
                    row['portal_type'] = portal_info.get('portal_type', '')
                    row['notes'] = portal_info.get('notes', '')
                    updated_count += 1
            elif company and company not in ['', 'Contract', 'In Search Of:', 'https://']:
                # Default to contact SBLO if not found
                if not row.get('vendor_registration_url', '').strip():
                    row['vendor_registration_url'] = "Contact SBLO directly"
                    row['portal_type'] = "Email Registration"
                    row['notes'] = "No public vendor portal found. Contact SBLO for vendor registration."
                    updated_count += 1
                    missing_companies.append(company)
            
            rows.append(row)
    
    # Write back to file
    with open(batch_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Updated {batch_file}: {updated_count} companies updated")
    if missing_companies:
        print(f"  Companies marked for SBLO contact: {', '.join(missing_companies[:5])}")
        if len(missing_companies) > 5:
            print(f"  ... and {len(missing_companies) - 5} more")
    
    return updated_count

def main():
    """Update all Tier 2 batch files."""
    batch_files = [
        'tier2-priority-batch-01.csv',
        'tier2-priority-batch-02.csv',
        'tier2-priority-batch-03.csv',
        'tier2-priority-batch-04.csv',
        'tier2-priority-batch-05.csv',
        'tier2-priority-batch-06.csv',
    ]
    
    total_updated = 0
    for batch_file in batch_files:
        count = update_batch_file(batch_file)
        total_updated += count
    
    print(f"\n✅ All batch files updated! Total: {total_updated} companies")

if __name__ == '__main__':
    main()

