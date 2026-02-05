#!/usr/bin/env python3
"""
Update Tier 2 batch CSV files with vendor portal information from research.
This script populates vendor_registration_url, portal_type, and notes columns.
"""

import csv
import os

# Vendor portal data from research
PORTAL_DATA = {
    # Batch 2
    "CleanHarbors": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for vendor registration process."
    },
    "Composite Analysis Group": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Small company - no formal portal. Contact SBLO directly for subcontracting opportunities."
    },
    "CoreCivic": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Covenant Aviation Security, LLC": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for supplier registration."
    },
    "Deployed Resources": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Dewberry": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for subcontractor registration."
    },
    "Environmental Chemical Corporation (ECC)": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for vendor registration."
    },
    "Ernst & Young LLP": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "Large firm but no public vendor portal found. Contact SBLO for vendor registration process."
    },
    "FJC Security Services, Inc.": {
        "vendor_registration_url": "Contact SBLO directly",
        "portal_type": "Email Registration",
        "notes": "No public vendor portal found. Contact SBLO for supplier registration."
    },
    # Batch 3 - KPMG (already researched from Tier 1)
    "KPMG": {
        "vendor_registration_url": "https://kpmg.supplierone.co/",
        "portal_type": "Full Portal",
        "notes": "Uses Coupa Supplier Portal (CSP) for transactions. Supplier diversity registration at kpmg.supplierone.co. Invitation-based system."
    },
}

def update_batch_file(batch_file):
    """Update a batch CSV file with portal information."""
    if not os.path.exists(batch_file):
        print(f"File not found: {batch_file}")
        return
    
    rows = []
    updated_count = 0
    
    with open(batch_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            company = row.get('company', '').strip()
            clean_name = row.get('clean_name', '').strip()
            
            # Try to match company name or clean_name
            match_key = None
            for key in PORTAL_DATA.keys():
                if company == key or clean_name == key:
                    match_key = key
                    break
                # Also check if company name contains the key
                if key.lower() in company.lower() or key.lower() in clean_name.lower():
                    match_key = key
                    break
            
            if match_key and PORTAL_DATA[match_key]:
                portal_info = PORTAL_DATA[match_key]
                row['vendor_registration_url'] = portal_info.get('vendor_registration_url', '')
                row['portal_type'] = portal_info.get('portal_type', '')
                row['notes'] = portal_info.get('notes', '')
                updated_count += 1
            
            rows.append(row)
    
    # Write back to file
    with open(batch_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Updated {batch_file}: {updated_count} companies updated")

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
    
    for batch_file in batch_files:
        update_batch_file(batch_file)
    
    print("\n✅ All batch files updated!")

if __name__ == '__main__':
    main()

