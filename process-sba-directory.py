#!/usr/bin/env python3
"""
Process SBA Prime Directory (Report Builder FY24)
Cross-reference with existing SBLO list and add new contacts
"""

import pandas as pd
import csv
from pathlib import Path
from collections import defaultdict

def normalize_company_name(name):
    """Normalize company name for matching"""
    if pd.isna(name) or not name:
        return ''
    name = str(name).strip()
    # Remove common suffixes and normalize
    name = name.replace(',', '').replace('.', '').replace('Inc', '').replace('LLC', '').replace('LP', '')
    name = name.replace('Incorporated', '').replace('Corporation', '').replace('Corp', '')
    return name.strip().lower()

def process_sba_directory():
    """Process the SBA Prime Directory Excel file"""
    file_path = './SBLO List /Report Builder FY24 Final rev2.xlsx'
    
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Process SBA Prime Directory FY24                  ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    print(f"📂 Reading: {file_path}")
    
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
        print(f"✅ Loaded {len(df):,} rows")
        
        # Get unique prime contractors
        print("\n📊 Analyzing data...")
        
        # Use Ultimate Parent if available, otherwise Legal Business Name
        df['Prime_Company'] = df['Ultimate Parent Legal Business Name'].fillna(df['Legal Business Name'])
        
        # Group by company to get aggregated info
        company_data = defaultdict(lambda: {
            'companies': set(),
            'agencies': set(),
            'naics': set(),
            'total_contract_value': 0,
            'contract_count': 0,
            'has_subcontract_plan': False
        })
        
        for _, row in df.iterrows():
            company = row['Prime_Company']
            if pd.notna(company) and str(company).strip():
                normalized = normalize_company_name(company)
                company_data[normalized]['companies'].add(str(company).strip())
                company_data[normalized]['contract_count'] += 1
                
                if pd.notna(row['Contracting Agency Name']):
                    company_data[normalized]['agencies'].add(str(row['Contracting Agency Name']).strip())
                
                if pd.notna(row['NAICS Code']):
                    company_data[normalized]['naics'].add(str(int(row['NAICS Code'])))
                
                if pd.notna(row['Base and All Options Value (Total Contract Value)']):
                    try:
                        value = float(row['Base and All Options Value (Total Contract Value)'])
                        company_data[normalized]['total_contract_value'] += value
                    except:
                        pass
                
                if pd.notna(row['Subcontract Plan']) and str(row['Subcontract Plan']).strip().upper() != 'NONE':
                    company_data[normalized]['has_subcontract_plan'] = True
        
        print(f"✅ Found {len(company_data):,} unique prime contractors")
        
        # Create list of companies
        companies_list = []
        for normalized, data in company_data.items():
            # Use the most common company name variant
            company_name = sorted(data['companies'], key=len, reverse=True)[0]
            
            companies_list.append({
                'company': company_name,
                'normalized': normalized,
                'contract_count': data['contract_count'],
                'total_contract_value': data['total_contract_value'],
                'agencies': ', '.join(sorted(list(data['agencies']))[:5]),  # Top 5 agencies
                'naics': ', '.join(sorted(list(data['naics']))[:10]),  # Top 10 NAICS
                'has_subcontract_plan': data['has_subcontract_plan']
            })
        
        # Sort by contract value (highest first)
        companies_list.sort(key=lambda x: x['total_contract_value'], reverse=True)
        
        print(f"\n📋 Top 10 companies by contract value:")
        for i, comp in enumerate(companies_list[:10], 1):
            value_str = f"${comp['total_contract_value']:,.0f}" if comp['total_contract_value'] > 0 else "N/A"
            print(f"   {i:2d}. {comp['company'][:50]:50s} - {value_str} ({comp['contract_count']} contracts)")
        
        return companies_list
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        import traceback
        traceback.print_exc()
        return []

def cross_reference_with_sblo_list(companies_list):
    """Cross-reference SBA companies with existing SBLO list"""
    print("\n" + "="*60)
    print("🔍 Cross-Referencing with Existing SBLO List")
    print("="*60)
    
    # Load existing SBLO contacts
    existing_files = [
        'dhs-contacts-all-76-companies.csv',
        'sblo-list-compiled.csv',
        'sblo-list.csv'
    ]
    
    existing_companies = set()
    existing_contacts = {}
    
    for file_path in existing_files:
        file = Path(file_path)
        if file.exists():
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        company = row.get('company', '').strip()
                        if company:
                            normalized = normalize_company_name(company)
                            existing_companies.add(normalized)
                            if normalized not in existing_contacts:
                                existing_contacts[normalized] = row
            except Exception as e:
                print(f"⚠️  Could not read {file_path}: {e}")
    
    print(f"📊 Existing SBLO contacts: {len(existing_companies)} companies")
    
    # Find matches and new companies
    matched_companies = []
    new_companies = []
    
    for company in companies_list:
        normalized = company['normalized']
        if normalized in existing_companies:
            matched_companies.append(company)
        else:
            new_companies.append(company)
    
    print(f"\n✅ Matched companies: {len(matched_companies)}")
    print(f"🆕 New companies: {len(new_companies)}")
    
    return matched_companies, new_companies, existing_contacts

def create_enhanced_list(matched_companies, new_companies, existing_contacts):
    """Create enhanced SBLO list with SBA data"""
    print("\n" + "="*60)
    print("📝 Creating Enhanced SBLO List")
    print("="*60)
    
    # Create output list
    enhanced_contacts = []
    
    # Add existing contacts with SBA data if matched
    for company in matched_companies:
        normalized = company['normalized']
        if normalized in existing_contacts:
            contact = existing_contacts[normalized].copy()
            # Add SBA data
            contact['sba_contract_count'] = company['contract_count']
            contact['sba_total_value'] = f"${company['total_contract_value']:,.0f}" if company['total_contract_value'] > 0 else ''
            contact['sba_agencies'] = company['agencies']
            contact['sba_naics'] = company['naics']
            contact['has_subcontract_plan'] = 'Yes' if company['has_subcontract_plan'] else 'No'
            enhanced_contacts.append(contact)
    
    # Add new companies (without SBLO contacts yet)
    for company in new_companies[:500]:  # Limit to top 500 by contract value
        enhanced_contacts.append({
            'company': company['company'],
            'sblo_name': '[NEEDS CONTACT]',
            'title': 'SBLO',
            'email': '[NEEDS CONTACT]',
            'phone': '',
            'website': '',
            'naics': company['naics'],
            'source': 'SBA Prime Directory FY24',
            'sba_contract_count': company['contract_count'],
            'sba_total_value': f"${company['total_contract_value']:,.0f}" if company['total_contract_value'] > 0 else '',
            'sba_agencies': company['agencies'],
            'has_subcontract_plan': 'Yes' if company['has_subcontract_plan'] else 'No'
        })
    
    return enhanced_contacts

def main():
    # Process SBA directory
    companies_list = process_sba_directory()
    
    if not companies_list:
        print("⚠️  No companies found in file")
        return
    
    # Cross-reference
    matched_companies, new_companies, existing_contacts = cross_reference_with_sblo_list(companies_list)
    
    # Create enhanced list
    enhanced_contacts = create_enhanced_list(matched_companies, new_companies, existing_contacts)
    
    # Save results
    print(f"\n💾 Saving results...")
    
    # Save full SBA company list
    sba_companies_file = Path('sba-prime-directory-companies.csv')
    with open(sba_companies_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'contract_count', 'total_contract_value', 'agencies', 'naics', 'has_subcontract_plan']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for company in companies_list:
            writer.writerow({
                'company': company['company'],
                'contract_count': company['contract_count'],
                'total_contract_value': company['total_contract_value'],
                'agencies': company['agencies'],
                'naics': company['naics'],
                'has_subcontract_plan': company['has_subcontract_plan']
            })
    print(f"✅ Saved SBA companies list: {sba_companies_file} ({len(companies_list):,} companies)")
    
    # Save new companies only
    new_companies_file = Path('sba-new-companies-need-sblo.csv')
    with open(new_companies_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'contract_count', 'total_contract_value', 'agencies', 'naics', 'has_subcontract_plan']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for company in new_companies[:1000]:  # Top 1000
            writer.writerow({
                'company': company['company'],
                'contract_count': company['contract_count'],
                'total_contract_value': company['total_contract_value'],
                'agencies': company['agencies'],
                'naics': company['naics'],
                'has_subcontract_plan': company['has_subcontract_plan']
            })
    print(f"✅ Saved new companies: {new_companies_file} ({len(new_companies):,} companies)")
    
    # Update compiled list with new companies
    compiled_file = Path('sblo-list-compiled.csv')
    existing_emails = set()
    
    if compiled_file.exists():
        with open(compiled_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                email = row.get('email', '').lower()
                if email and email != '[needs contact]':
                    existing_emails.add(email)
    
    # Add new companies to compiled list
    new_added = 0
    with open(compiled_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'address', 'naics', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        for company in new_companies[:500]:  # Top 500
            writer.writerow({
                'company': company['company'],
                'sblo_name': '',
                'title': 'SBLO',
                'email': '',
                'phone': '',
                'address': '',
                'naics': company['naics'],
                'source': 'SBA Prime Directory FY24'
            })
            new_added += 1
    
    print(f"✅ Added {new_added} new companies to compiled list")
    
    print("\n" + "="*60)
    print("✨ Processing Complete!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   Total SBA companies: {len(companies_list):,}")
    print(f"   Already have SBLO contacts: {len(matched_companies)}")
    print(f"   New companies (need SBLO): {len(new_companies):,}")
    print(f"   Added to compiled list: {new_added}")
    
    print(f"\n📁 Files created:")
    print(f"   - sba-prime-directory-companies.csv (all {len(companies_list):,} companies)")
    print(f"   - sba-new-companies-need-sblo.csv (top {min(1000, len(new_companies))} new companies)")
    print(f"   - Updated sblo-list-compiled.csv")

if __name__ == '__main__':
    main()




