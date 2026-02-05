#!/usr/bin/env python3
"""
Update the Federal Contractor Master Database with vendor portal information
from PRIORITY-COMPANIES-VENDOR-PORTALS.md and Tier 2 batch files.
"""

import csv
import re
import os

# Vendor portal data from PRIORITY-COMPANIES-VENDOR-PORTALS.md
PRIORITY_PORTALS = {
    "Accenture": {
        "vendor_registration_url": "https://supplierhub.accenture.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Accenture Supplier Hub for registration. Also has My Supplier Portal (MSP) for existing suppliers."
    },
    "AECOM": {
        "vendor_registration_url": "https://aecom.ayrus.com/wgint/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Uses Coupa Supplier Portal (CSP). First-time users receive email invitation."
    },
    "AECOM TECHNICAL SERVICES": {
        "vendor_registration_url": "https://aecom.ayrus.com/wgint/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Same portal as AECOM parent company. Uses Coupa Supplier Portal system."
    },
    "Amentum": {
        "vendor_registration_url": "https://supplier.amentum.com/SupplierRegistration",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Dedicated supplier registration portal for small businesses and contractors."
    },
    "BAE Systems Intelligence & Security": {
        "vendor_registration_url": "https://baesystems.hicx.net/bae/hicxesm-portal/app/discovery-login.html",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Uses HICX supplier portal system. Requires prequalification forms."
    },
    "BAE SYSTEMS SAN FRANCISCO SHIP REPAIR": {
        "vendor_registration_url": "https://baesystems.hicx.net/bae/hicxesm-portal/app/discovery-login.html",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Uses HICX platform. Requires prequalification form completion."
    },
    "THE BOEING COMPANY": {
        "vendor_registration_url": "https://boeing.suppliergateway.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Boeing Supplier Capability Assessment Database registration."
    },
    "BOEING": {
        "vendor_registration_url": "https://boeing.suppliergateway.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Boeing Supplier Capability Assessment Database registration."
    },
    "Booz Allen Hamilton": {
        "vendor_registration_url": "https://doingbusiness.bah.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Diverse Business Registration portal for small businesses and subcontractors."
    },
    "BOOZ ALLEN HAMILTON INCORPORATED": {
        "vendor_registration_url": "https://doingbusiness.bah.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Diverse Business Registration portal. Contact: smallbusinesscompliance@bah.com"
    },
    "CACI Federal": {
        "vendor_registration_url": "https://supplier.caci.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "CACI Supplier Network portal - requires email invitation from CACI."
    },
    "Deloitte Financial Advisory Services, LLP": {
        "vendor_registration_url": "https://vendorportal.gps.deloitte.com/Register.html",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "GPS Vendor Portal - requires DUNS number, multi-factor authentication required."
    },
    "Deloitte Services, LP": {
        "vendor_registration_url": "https://vendorportal.gps.deloitte.com/Register.html",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "GPS Vendor Portal - requires DUNS number, multi-factor authentication required."
    },
    "Fluor Government Group": {
        "vendor_registration_url": "https://fggsupplierregistry.fluor.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "FGG Supplier Registry - dedicated portal for supplier information and registration."
    },
    "General Dynamics Information Technology": {
        "vendor_registration_url": "https://suppliers.gendyn.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Enterprise Supplier Registration Portal (ESRP) - one registration provides visibility to all 10 GD business units."
    },
    "GDIT": {
        "vendor_registration_url": "https://suppliers.gendyn.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Enterprise Supplier Registration Portal (ESRP)."
    },
    "IBM US Federal": {
        "vendor_registration_url": "https://www.ibm.com/mysupport/s/topic/0TO500000002XcVGAU/supplier-portal",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "IBM Supplier Portal - requires IBMid creation for access."
    },
    "Jacobs Engineering Group": {
        "vendor_registration_url": "https://www.jacobs.com/contact/suppliers",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Uses SAP Ariba Network for vendor registration."
    },
    "KPMG": {
        "vendor_registration_url": "https://kpmg.supplierone.co/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Uses Coupa Supplier Portal (CSP) for transactions. Invitation-based system."
    },
    "L3Harris": {
        "vendor_registration_url": "Contact SBLO directly",
        "vendor_portal_type": "Email Registration",
        "vendor_portal_notes": "Submit Vendor Selection Form to SHR.VendorManagement.mas@L3Harris.com."
    },
    "Leidos": {
        "vendor_registration_url": "https://www.leidos.com/suppliers",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Uses JAGGAER portal system. Invitation-based registration by Leidos team member required."
    },
    "Lockheed Martin": {
        "vendor_registration_url": "https://www.myexostar.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Registration through Exostar MAG (Managed Access Gateway) required for LMP2P portal access."
    },
    "ManTech": {
        "vendor_registration_url": "https://myhub.mantech.com/psc/FMSPRDGST/SUPPLIER/ERP/c/SUP_OB_MENU.AUC_BIDDER_REGISTR.GBL",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "PeopleSoft-based supplier portal. Small businesses use GovWin/Deltek Supplier Portal."
    },
    "Northrop Grumman": {
        "vendor_registration_url": "https://oasis-sbeforms.myngc.com/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Uses OASIS supplier portal and SAP Ariba Network for registration."
    },
    "Parsons Brinckerhoff": {
        "vendor_registration_url": "https://www.parsons.com/suppliers/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Note: Parsons Brinckerhoff rebranded to WSP in 2017. Current registration is through Parsons Corporation."
    },
    "Peraton": {
        "vendor_registration_url": "https://www.peraton.com/suppliers/prospective-supplier-intake-form",
        "vendor_portal_type": "Contact Form",
        "vendor_portal_notes": "Prospective suppliers complete online Capability Form at supplier intake page."
    },
    "Raytheon": {
        "vendor_registration_url": "https://rtx.supplierone.co/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "RTX SupplierOne platform for new vendor registration. Note: Raytheon is now part of RTX."
    },
    "SAIC": {
        "vendor_registration_url": "https://suppliers.saic.com/Register",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Complete supplier form with required fields to gain portal access."
    },
}

# Tier 2 vendor portals (from batch files)
TIER2_PORTALS = {
    "KPMG": {
        "vendor_registration_url": "https://kpmg.supplierone.co/",
        "vendor_portal_type": "Full Portal",
        "vendor_portal_notes": "Uses Coupa Supplier Portal (CSP) for transactions. Invitation-based system."
    },
    # Add more Tier 2 companies as needed - most require SBLO contact
}

def clean_company_name(name):
    """Clean and normalize company name for matching."""
    if not name:
        return ""
    # Remove extra whitespace
    name = " ".join(name.split())
    # Remove common suffixes/prefixes for better matching
    name = re.sub(r'\s+(INC|LLC|CORP|CORPORATION|LTD|LIMITED)$', '', name, flags=re.IGNORECASE)
    return name.strip().upper()

def match_company_name(db_company, portal_company):
    """Check if database company name matches portal company name."""
    db_clean = clean_company_name(db_company)
    portal_clean = clean_company_name(portal_company)
    
    # Exact match
    if db_clean == portal_clean:
        return True
    
    # Check if one contains the other
    if db_clean in portal_clean or portal_clean in db_clean:
        return True
    
    # Check for partial matches (at least 5 characters)
    if len(db_clean) >= 5 and len(portal_clean) >= 5:
        # Remove common words and check
        db_words = set(re.findall(r'\b\w{4,}\b', db_clean))
        portal_words = set(re.findall(r'\b\w{4,}\b', portal_clean))
        if db_words and portal_words and len(db_words.intersection(portal_words)) >= 2:
            return True
    
    return False

def find_portal_info(company_name):
    """Find vendor portal information for a company."""
    # Check priority portals first
    for portal_company, portal_info in PRIORITY_PORTALS.items():
        if match_company_name(company_name, portal_company):
            return portal_info
    
    # Check Tier 2 portals
    for portal_company, portal_info in TIER2_PORTALS.items():
        if match_company_name(company_name, portal_company):
            return portal_info
    
    return None

def update_database(input_file, output_file):
    """Update database CSV with vendor portal information."""
    rows = []
    updated_count = 0
    matched_companies = []
    
    # Read existing database
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        # Add vendor portal columns if they don't exist
        new_columns = ['vendor_registration_url', 'vendor_portal_type', 'vendor_portal_notes']
        for col in new_columns:
            if col not in fieldnames:
                fieldnames = list(fieldnames) + [col]
        
        for row in reader:
            company = row.get('company', '').strip()
            
            # Skip if already has vendor portal info (unless empty)
            if row.get('vendor_registration_url', '').strip():
                rows.append(row)
                continue
            
            # Find portal information
            portal_info = find_portal_info(company)
            
            if portal_info:
                row['vendor_registration_url'] = portal_info.get('vendor_registration_url', '')
                row['vendor_portal_type'] = portal_info.get('vendor_portal_type', '')
                row['vendor_portal_notes'] = portal_info.get('vendor_portal_notes', '')
                updated_count += 1
                matched_companies.append(company)
            
            # Ensure all new columns exist in row
            for col in new_columns:
                if col not in row:
                    row[col] = ''
            
            rows.append(row)
    
    # Write updated database
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ Updated {updated_count} companies with vendor portal information")
    if matched_companies:
        print(f"\nTop 10 matched companies:")
        for company in matched_companies[:10]:
            print(f"  - {company}")
        if len(matched_companies) > 10:
            print(f"  ... and {len(matched_companies) - 10} more")
    
    return updated_count

def main():
    """Main function."""
    input_file = 'FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
    output_file = 'FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
    
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found")
        return
    
    print(f"Updating {input_file} with vendor portal information...")
    print("=" * 60)
    
    count = update_database(input_file, output_file)
    
    print("=" * 60)
    print(f"\n✅ Database update complete!")
    print(f"   Total companies updated: {count}")
    print(f"   Output file: {output_file}")

if __name__ == '__main__':
    main()

