#!/usr/bin/env python3
"""
Cross-reference SBA companies with existing SBLO contacts
Match companies we already have contacts for
"""

import csv
from pathlib import Path

def normalize_company_name(name):
    """Normalize company name for matching"""
    if not name:
        return ''
    name = str(name).strip().lower()
    # Remove common suffixes
    name = re.sub(r'\s+(inc|llc|corp|corporation|lp|incorporated|company|co)$', '', name)
    # Remove punctuation
    name = re.sub(r'[^a-z0-9]', '', name)
    return name

def cross_reference_sba_with_existing():
    """Cross-reference SBA companies with existing SBLO contacts"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Cross-Reference SBA with Existing Contacts        ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Load existing contacts
    existing_files = [
        'dhs-contacts-all-76-companies.csv',
        'dod-csp-contacts-cleaned.csv',
        'dot-contacts.csv'
    ]
    
    existing_contacts = {}
    for file_path in existing_files:
        file = Path(file_path)
        if file.exists():
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    company = row.get('company', '').strip()
                    if company:
                        normalized = normalize_company_name(company)
                        if normalized not in existing_contacts:
                            existing_contacts[normalized] = row
    
    print(f"📊 Existing contacts: {len(existing_contacts)} companies")
    
    # Load SBA companies
    sba_file = Path('sba-new-companies-need-sblo.csv')
    if not sba_file.exists():
        print(f"❌ File not found: {sba_file}")
        return
    
    sba_companies = []
    with open(sba_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        sba_companies = list(reader)
    
    print(f"📊 SBA companies needing contacts: {len(sba_companies)}")
    
    # Match SBA companies with existing contacts
    matched = []
    unmatched = []
    
    for sba_company in sba_companies:
        company_name = sba_company['company']
        normalized = normalize_company_name(company_name)
        
        if normalized in existing_contacts:
            # Found a match!
            existing = existing_contacts[normalized]
            matched.append({
                'sba_company': company_name,
                'sba_contract_value': sba_company.get('total_contract_value', ''),
                'sba_contract_count': sba_company.get('contract_count', ''),
                'existing_sblo_name': existing.get('sblo_name', ''),
                'existing_email': existing.get('email', ''),
                'existing_phone': existing.get('phone', ''),
                'existing_source': existing.get('source', ''),
                'match_confidence': 'HIGH'
            })
        else:
            unmatched.append(sba_company)
    
    print(f"\n✅ Matched: {len(matched)} companies")
    print(f"🆕 Still need research: {len(unmatched)} companies")
    
    # Save matched companies
    if matched:
        matched_file = Path('sba-matched-with-existing-contacts.csv')
        with open(matched_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['sba_company', 'sba_contract_value', 'sba_contract_count', 
                         'existing_sblo_name', 'existing_email', 'existing_phone', 'existing_source', 'match_confidence']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(matched)
        
        print(f"💾 Saved matched companies to: {matched_file}")
        
        # Show top matches
        print("\n📋 Top Matched Companies:")
        matched_sorted = sorted(matched, key=lambda x: float(x.get('sba_contract_value', 0) or 0), reverse=True)
        for i, match in enumerate(matched_sorted[:10], 1):
            value = f"${float(match['sba_contract_value']):,.0f}" if match['sba_contract_value'] else 'N/A'
            email = match['existing_email'][:30] if match['existing_email'] else 'N/A'
            print(f"   {i:2d}. {match['sba_company'][:40]:40s} - {email} ({value})")
    
    # Save still-needed list (top 100)
    if unmatched:
        unmatched_sorted = sorted(unmatched, key=lambda x: float(x.get('total_contract_value', 0) or 0), reverse=True)
        still_needed_file = Path('sba-still-need-research-top-100.csv')
        with open(still_needed_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['company', 'contract_count', 'total_contract_value', 'agencies', 'naics', 'has_subcontract_plan']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unmatched_sorted[:100])
        
        print(f"\n💾 Saved top 100 still-needed companies to: {still_needed_file}")
    
    return matched, unmatched

def create_research_templates():
    """Create research templates for manual research"""
    print("\n" + "="*60)
    print("📝 Creating Research Templates")
    print("="*60)
    
    # DOT email research template
    dot_file = Path('dot-contacts.csv')
    if dot_file.exists():
        with open(dot_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            dot_contacts = list(reader)
        
        research_template = Path('DOT-EMAIL-RESEARCH-TEMPLATE.csv')
        with open(research_template, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['company', 'sblo_name', 'phone', 'website_to_check', 'email_found', 'research_status', 'notes']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for contact in dot_contacts:
                company = contact['company']
                # Generate website guess
                company_clean = company.lower().replace(' ', '').replace(',', '').replace('.', '')
                company_clean = re.sub(r'(inc|llc|corp|corporation|lp|incorporated)$', '', company_clean)
                
                writer.writerow({
                    'company': company,
                    'sblo_name': contact.get('sblo_name', ''),
                    'phone': contact.get('phone', ''),
                    'website_to_check': f"www.{company_clean}.com",
                    'email_found': '',
                    'research_status': 'PENDING',
                    'notes': ''
                })
        
        print(f"✅ Created: {research_template} ({len(dot_contacts)} contacts)")
    
    print("\n✨ Research templates created!")
    print("   Fill in email addresses as you research them")

if __name__ == '__main__':
    import re
    matched, unmatched = cross_reference_sba_with_existing()
    create_research_templates()




