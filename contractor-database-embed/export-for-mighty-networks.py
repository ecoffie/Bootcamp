#!/usr/bin/env python3
"""
Export Vercel database to CSV format for Mighty Networks import
Converts data-extract.js to contractors-for-mighty-networks.csv
"""
import json
import csv
import re
import sys

def export_to_csv(input_file='data-extract.js', output_file='contractors-for-mighty-networks.csv', export_all=False):
    """Export companies from data-extract.js to CSV for Mighty Networks"""
    
    print("📥 Reading data-extract.js...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: {input_file} not found!")
        print("   Make sure you're in the contractor-database-embed directory")
        sys.exit(1)
    
    # Extract the JSON array from the JavaScript file
    match = re.search(r'const companies = (\[.*?\]);', content, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            companies = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
            sys.exit(1)
    else:
        print("❌ Could not extract companies array from data-extract.js")
        print("   Make sure the file contains: const companies = [...]")
        sys.exit(1)
    
    print(f"✅ Found {len(companies)} companies in database")
    
    # Convert to CSV format suitable for Mighty Networks
    fieldnames = [
        'email',           # Required for member invitation
        'name',            # Display name (company name or SBLO name)
        'company',         # Company name
        'sblo_name',       # SBLO contact name
        'phone',           # Phone number
        'naics',           # NAICS codes
        'contract_count',  # Contract count
        'contract_value',  # Total contract value
        'agencies',        # Agencies worked with
        'has_subcontract_plan'  # Has subcontract plan
    ]
    
    exported_count = 0
    skipped_count = 0
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for company in companies:
            email = company.get('email', '').strip() if company.get('email') else ''
            company_name = company.get('company', '').strip()
            sblo_name = company.get('sblo_name', '').strip()
            
            # Determine display name
            display_name = sblo_name if sblo_name else company_name
            
            # If export_all is False, only export companies with emails
            if not export_all and not email:
                skipped_count += 1
                continue
            
            # If no email but export_all is True, create placeholder
            if export_all and not email:
                # Create placeholder email (you'll need to update these)
                email = f"contact@{company_name.lower().replace(' ', '').replace('.', '').replace(',', '').replace('&', '').replace('-', '')[:50]}.example.com"
            
            writer.writerow({
                'email': email,
                'name': display_name,
                'company': company_name,
                'sblo_name': sblo_name,
                'phone': company.get('phone', '').strip() if company.get('phone') else '',
                'naics': company.get('naics', '').strip() if company.get('naics') else '',
                'contract_count': str(company.get('contract_count', '')).strip(),
                'contract_value': str(company.get('total_contract_value', '')).strip(),
                'agencies': company.get('agencies', '').strip() if company.get('agencies') else '',
                'has_subcontract_plan': str(company.get('has_subcontract_plan', '')).strip()
            })
            exported_count += 1
    
    print(f"\n✅ Export complete!")
    print(f"📊 Exported {exported_count} companies to {output_file}")
    if skipped_count > 0:
        print(f"⚠️  Skipped {skipped_count} companies (no email address)")
        print(f"   Use --export-all flag to include all companies")
    
    print(f"\n📋 Next steps:")
    print(f"   1. Review {output_file}")
    print(f"   2. Check Mighty Networks admin panel for bulk import")
    print(f"   3. Contact support@mightynetworks.com if needed")
    print(f"   4. See IMPORT_TO_MIGHTY_NETWORKS.md for import methods")

if __name__ == '__main__':
    export_all = '--export-all' in sys.argv
    export_to_csv(export_all=export_all)
