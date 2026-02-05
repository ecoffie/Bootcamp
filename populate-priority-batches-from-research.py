#!/usr/bin/env python3
"""
Populate priority batch CSV files from PRIORITY-COMPANIES-VENDOR-PORTALS.md research
"""

import csv
import re

# Portal data extracted from PRIORITY-COMPANIES-VENDOR-PORTALS.md
PORTAL_DATA = {
    # Batch 1 (already complete)
    'Accenture': {
        'vendor_registration_url': 'https://supplierhub.accenture.com/',
        'portal_type': 'Full Portal',
        'notes': 'Accenture Supplier Hub for registration. Also has My Supplier Portal (MSP) at https://eme.mysupplierportal.com/ACC/Pages/UI/Login.aspx. Visit accenture.com/vendor to access registration link. Username and password provided after registration.'
    },
    'AECOM': {
        'vendor_registration_url': 'https://aecom.ayrus.com/wgint/',
        'portal_type': 'Full Portal',
        'notes': 'Uses Coupa Supplier Portal (CSP) for PO management and invoicing. Supplier/Subcontractor Registry available at https://aecom.ayrus.com/wgint/ for initial registration. First-time users receive email from do_not_reply@aecom.coupahost.com with registration link.'
    },
    'AECOM TECHNICAL SERVICES': {
        'vendor_registration_url': 'https://aecom.ayrus.com/wgint/',
        'portal_type': 'Full Portal',
        'notes': 'Same as AECOM parent company. Uses Coupa Supplier Portal (CSP). Supplier/Subcontractor Registry at https://aecom.ayrus.com/wgint/ for registration. Contact supplier@aecom.com if registration email not received.'
    },
    'Amentum': {
        'vendor_registration_url': 'https://supplier.amentum.com/SupplierRegistration',
        'portal_type': 'Full Portal',
        'notes': 'Supplier registration portal for small businesses and contractors. Also has Vendor Portal at https://vpconn.amentum.com/. Database accessible on Amentum intranet. Partners must comply with Amentum Business Partner Code of Conduct.'
    },
    'BAE Systems Intelligence & Security': {
        'vendor_registration_url': 'https://baesystems.hicx.net/bae/hicxesm-portal/app/discovery-login.html',
        'portal_type': 'Full Portal',
        'notes': 'Uses HICX supplier portal for registration. Suppliers can register and maintain information for future opportunities. Requires prequalification forms. Data routed to different groups within BAE Systems for review and validation.'
    },
    # Batch 2
    'BAE SYSTEMS SAN FRANCISCO SHIP REPAIR': {
        'vendor_registration_url': 'https://baesystems.hicx.net/bae/hicxesm-portal/app/discovery-login.html',
        'portal_type': 'Full Portal',
        'notes': 'New supplier registration portal using HiCX platform. Requires prequalification form completion including Health/Safety/Environmental questionnaire, OSHA logs, EMR certificates, and citation history.'
    },
    'BOEING COMPANY, THE': {
        'vendor_registration_url': 'https://boeing.suppliergateway.com/',
        'portal_type': 'Full Portal',
        'notes': 'Boeing Supplier Capability Assessment Database registration. Submission does not constitute approval or obligation to solicit RFQ. Existing suppliers use Boeing Portal via Exostar platform (requires email invitation). Only procurement agents can commit to purchase contracts.'
    },
    'Booz Allen Hamilton': {
        'vendor_registration_url': 'https://doingbusiness.bah.com/',
        'portal_type': 'Full Portal',
        'notes': 'Diverse Business Registration portal for small businesses and subcontractors. Secure portal for business registration, documentation sharing, contracts, and invoicing. Also has general supplier portal at supplier.bah.com. Strong focus on small business teaming - subcontracted over $1B in FY2020. Cybersecurity compliance required.'
    },
    'BOOZ ALLEN HAMILTON INCORPORATED': {
        'vendor_registration_url': 'https://doingbusiness.bah.com/',
        'portal_type': 'Full Portal',
        'notes': 'Same as above - Diverse Business Registration portal. Contact: smallbusinesscompliance@bah.com'
    },
    'CACI Federal': {
        'vendor_registration_url': 'https://supplier.caci.com/',
        'portal_type': 'Full Portal',
        'notes': 'CACI Supplier Network portal - requires email invitation from CACI with login credentials. Central repository for supplier profile information and required documents. Contact Small Business Advocacy Office: wpizer@caci.com'
    },
    # Batch 3
    'DELOITTE FINANCIAL ADVISORY SERVICES, LLP': {
        'vendor_registration_url': 'https://vendorportal.gps.deloitte.com/Register.html',
        'portal_type': 'Full Portal',
        'notes': 'GPS Vendor Portal - requires DUNS number, login required, must complete Prospective Vendor Questionnaire (PVQ), multi-factor authentication required.'
    },
    'Deloitte Services, LP': {
        'vendor_registration_url': 'https://vendorportal.gps.deloitte.com/Register.html',
        'portal_type': 'Full Portal',
        'notes': 'GPS Vendor Portal - requires DUNS number, login required, must complete Prospective Vendor Questionnaire (PVQ), multi-factor authentication required.'
    },
    'Fluor Government Group': {
        'vendor_registration_url': 'https://fggsupplierregistry.fluor.com/',
        'portal_type': 'Full Portal',
        'notes': 'FGG Supplier Registry - dedicated portal for supplier information and registration, uses Workday for B2B processes, registration does not constitute approval.'
    },
    'General Dynamics Information Technology': {
        'vendor_registration_url': 'https://suppliers.gendyn.com/',
        'portal_type': 'Full Portal',
        'notes': 'Enterprise Supplier Registration Portal (ESRP) - one registration provides visibility to all 10 GD business units, internal database for supplier capabilities, registration does not constitute approval.'
    },
    'IBM US Federal': {
        'vendor_registration_url': 'https://www.ibm.com/mysupport/s/topic/0TO500000002XcVGAU/supplier-portal',
        'portal_type': 'Full Portal',
        'notes': 'IBM Supplier Portal - requires IBMid creation for access, for tier-two technical services opportunities contact smallbusiness@us.ibm.com, evaluation process before network invitation.'
    },
    # Batch 4
    'JACOBS ENGINEERING GROUP INC.': {
        'vendor_registration_url': 'https://www.jacobs.com/contact/suppliers',
        'portal_type': 'Full Portal',
        'notes': 'Uses SAP Ariba Network for vendor registration. Official supplier contact page provides registration information and links to Ariba portal. No requirement to reach 100% profile completeness to conduct business.'
    },
    'Jacobs Engineering Group, Inc.': {
        'vendor_registration_url': 'https://www.jacobs.com/contact/suppliers',
        'portal_type': 'Full Portal',
        'notes': 'Uses SAP Ariba Network for vendor registration. Official supplier contact page provides registration information and links to Ariba portal. No requirement to reach 100% profile completeness to conduct business.'
    },
    'KPMG': {
        'vendor_registration_url': 'https://kpmg.supplierone.co/',
        'portal_type': 'Full Portal',
        'notes': 'Uses Coupa Supplier Portal (CSP) for transactions. Supplier diversity registration at kpmg.supplierone.co. Invitation-based system; no charge to use portal.'
    },
    'L3Harris': {
        'vendor_registration_url': 'https://suppliers.l3harris.com/supplier-info/supplier_registration.aspx',
        'portal_type': 'Email Registration',
        'notes': 'Submit Vendor Selection Form to SHR.VendorManagement.mas@L3Harris.com. Multiple division-specific portals available. Supplier Vetting Management (SVM) portal for qualification.'
    },
    'Leidos': {
        'vendor_registration_url': 'https://www.leidos.com/suppliers',
        'portal_type': 'Full Portal',
        'notes': 'Uses JAGGAER portal system. Invitation-based registration by Leidos team member required. Main portal: solutions.sciquest.com/apps/Router/SupplierLogin?CustOrg=Leidos. Support: Jaggaer@Leidos.com'
    },
    # Batch 5
    'LOCKHEED MARTIN CORPORATION': {
        'vendor_registration_url': 'https://www.myexostar.com/',
        'portal_type': 'Full Portal',
        'notes': 'Registration through Exostar MAG (Managed Access Gateway) required for LMP2P (Lockheed Martin Procure to Pay) portal access. Must establish company profile and user accounts. Also requires Avetta compliance program registration. Contact: Inquiries.supplier@lmco.com'
    },
    'Mantech': {
        'vendor_registration_url': 'https://myhub.mantech.com/psc/FMSPRDGST/SUPPLIER/ERP/c/SUP_OB_MENU.AUC_BIDDER_REGISTR.GBL',
        'portal_type': 'Full Portal',
        'notes': 'PeopleSoft-based supplier portal at myhub.mantech.com. Small businesses use GovWin/Deltek Supplier Portal for registration. Upload certifications (HUBZone, EDWOSB) to GovWin/Deltek portal.'
    },
    'Northrop Grumman (Information Technology)': {
        'vendor_registration_url': 'https://oasis-sbeforms.myngc.com/',
        'portal_type': 'Full Portal',
        'notes': 'Uses OASIS supplier portal and SAP Ariba Network for registration. Must complete Supplier Information Form then receive Ariba Network invitation. Note: Creating Ariba account alone does NOT register you as NG supplier - must complete full NG registration process.'
    },
    'PARSONS BRINCKERHOFF INC': {
        'vendor_registration_url': 'https://www.parsons.com/suppliers/',
        'portal_type': 'Full Portal',
        'notes': 'Note: Parsons Brinckerhoff rebranded to WSP in 2017. Current registration is through Parsons Corporation (separate company) which uses SAP Ariba for supplier management. Registration requires cybersecurity compliance, ESG factors, sustainability data and ethical conduct standards.'
    },
    'Peraton': {
        'vendor_registration_url': 'https://www.peraton.com/suppliers/prospective-supplier-intake-form',
        'portal_type': 'Contact Form',
        'notes': 'Prospective suppliers complete online Capability Form at supplier intake page. Peraton focuses on partnerships with small and large suppliers.'
    },
    # Batch 6
    'RAYTHEON COMPANY': {
        'vendor_registration_url': 'https://rtx.supplierone.co/',
        'portal_type': 'Full Portal',
        'notes': 'RTX SupplierOne platform for new vendor registration. Portal access at suppliers.utc.com is invitation-only for active suppliers. Note: Raytheon is now part of RTX. As of January 21, 2025, Raytheon suspended enforcement of diversity requirements except those required by federal regulations.'
    },
    'SAIC': {
        'vendor_registration_url': 'https://suppliers.saic.com/Register',
        'portal_type': 'Full Portal',
        'notes': 'Complete supplier form with required fields to gain portal access. Email verification required after submission. Information may be shared with government representatives.'
    },
    'SBLO Raytheon': {
        'vendor_registration_url': 'https://rtx.supplierone.co/',
        'portal_type': 'Full Portal',
        'notes': 'Same as Raytheon - use RTX SupplierOne platform. SBLO contact: Crystal L. King (crystal.l.king@rtx.com, 571-274-8407).'
    },
    'THE BOEING COMPANY': {
        'vendor_registration_url': 'https://boeing.suppliergateway.com/',
        'portal_type': 'Full Portal',
        'notes': 'Same as Boeing entry above. Updated provisions per EO 14173 (Jan 2025).'
    },
}

def normalize_company_name(name):
    """Normalize company name for matching"""
    # Remove extra whitespace
    name = ' '.join(name.split())
    # Handle variations
    name = name.replace('"', '').strip()
    return name

def populate_batch_file(batch_file):
    """Populate a batch file with vendor portal data"""
    
    print(f"\nProcessing: {batch_file}")
    
    rows = []
    updated_count = 0
    
    # Read the batch file
    with open(batch_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        
        for row in reader:
            company = row.get('company', '').strip()
            normalized = normalize_company_name(company)
            
            # Try to find matching portal data
            matched = False
            for key, data in PORTAL_DATA.items():
                if normalize_company_name(key) == normalized or key in company or company in key:
                    row['vendor_registration_url'] = data['vendor_registration_url']
                    row['portal_type'] = data['portal_type']
                    row['notes'] = data['notes']
                    updated_count += 1
                    matched = True
                    print(f"  ✓ Matched: {company}")
                    break
            
            if not matched:
                print(f"  ⚠ No match found: {company}")
            
            rows.append(row)
    
    # Write updated file
    with open(batch_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"  Updated {updated_count}/{len(rows)} companies")
    return updated_count

def main():
    print("=" * 80)
    print("POPULATE PRIORITY BATCHES FROM RESEARCH")
    print("=" * 80)
    
    batch_files = [
        'priority-batch-02.csv',
        'priority-batch-03.csv',
        'priority-batch-04.csv',
        'priority-batch-05.csv',
        'priority-batch-06.csv',
    ]
    
    total_updated = 0
    
    for batch_file in batch_files:
        try:
            updated = populate_batch_file(batch_file)
            total_updated += updated
        except FileNotFoundError:
            print(f"  ❌ File not found: {batch_file}")
        except Exception as e:
            print(f"  ❌ Error processing {batch_file}: {e}")
    
    print("\n" + "=" * 80)
    print(f"✓ Total companies updated: {total_updated}")
    print("=" * 80)
    
    if total_updated > 0:
        print("\n✅ Batch files populated successfully!")
        print("Next step: Verify the data and run consolidate-vendor-portals.py")

if __name__ == '__main__':
    main()

