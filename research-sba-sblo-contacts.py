#!/usr/bin/env python3
"""
Research SBLO contacts for top SBA companies
Focus on companies with highest contract values
"""

import csv
import re
from pathlib import Path

def research_top_sba_companies():
    """Research SBLO contacts for top SBA companies"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Research SBLO Contacts for Top SBA Companies     ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Load SBA companies that need SBLO contacts
    sba_file = Path('sba-new-companies-need-sblo.csv')
    
    if not sba_file.exists():
        print(f"❌ File not found: {sba_file}")
        return
    
    companies = []
    with open(sba_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        companies = list(reader)
    
    # Sort by contract value (highest first)
    companies_sorted = sorted(
        companies,
        key=lambda x: float(x.get('total_contract_value', 0) or 0),
        reverse=True
    )
    
    print(f"📊 Found {len(companies_sorted)} companies needing SBLO contacts")
    print(f"🎯 Focusing on top 100 by contract value\n")
    
    # Focus on top 100
    top_companies = companies_sorted[:100]
    
    # Generate research template
    research_list = []
    
    for i, company in enumerate(top_companies, 1):
        company_name = company['company']
        contract_value = company.get('total_contract_value', 0)
        naics = company.get('naics', '')
        agencies = company.get('agencies', '')
        
        # Generate possible email patterns
        company_clean = company_name.lower()
        company_clean = re.sub(r'\s+(inc|llc|corp|corporation|lp|incorporated)$', '', company_clean)
        company_clean = re.sub(r'[^a-z0-9]', '', company_clean)
        
        email_patterns = [
            f"smallbusiness@{company_clean}.com",
            f"sblo@{company_clean}.com",
            f"small.business@{company_clean}.com",
            f"supplier.diversity@{company_clean}.com",
            f"osdbu@{company_clean}.com",
            f"procurement@{company_clean}.com",
        ]
        
        research_list.append({
            'rank': i,
            'company': company_name,
            'contract_value': f"${float(contract_value):,.0f}" if contract_value else '',
            'contract_count': company.get('contract_count', ''),
            'naics': naics,
            'agencies': agencies[:100],  # Truncate long agency lists
            'sblo_name': '[NEEDS RESEARCH]',
            'email': '[NEEDS RESEARCH]',
            'phone': '[NEEDS RESEARCH]',
            'website': f"www.{company_clean}.com",
            'email_patterns': '; '.join(email_patterns),
            'research_status': 'PENDING',
            'research_notes': ''
        })
    
    # Save research list
    output_file = Path('sba-top-100-research-list.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['rank', 'company', 'contract_value', 'contract_count', 'naics', 'agencies', 
                     'sblo_name', 'email', 'phone', 'website', 'email_patterns', 'research_status', 'research_notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(research_list)
    
    print(f"💾 Saved research list to: {output_file}")
    
    # Show top 20
    print("\n📋 Top 20 Companies Needing SBLO Research:")
    print("=" * 80)
    for company in research_list[:20]:
        value = company['contract_value'] or 'N/A'
        print(f"   {company['rank']:2d}. {company['company'][:50]:50s} - {value}")
    
    print("\n📋 Research Strategy:")
    print("   1. Start with top 20 companies (highest contract values)")
    print("   2. Visit each company website")
    print("   3. Look for 'Small Business' or 'Supplier Diversity' sections")
    print("   4. Check 'Doing Business With Us' or 'Vendor' pages")
    print("   5. Use email patterns provided")
    print("   6. Update CSV with verified contacts")
    
    # Create a quick reference guide
    guide_file = Path('SBA-RESEARCH-GUIDE.md')
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write("# SBA Top Companies - SBLO Research Guide\n\n")
        f.write("## Top 100 Companies by Contract Value\n\n")
        f.write("Research SBLO contacts for these high-value companies:\n\n")
        f.write("| Rank | Company | Contract Value | Research Status |\n")
        f.write("|------|---------|----------------|-----------------|\n")
        for company in research_list[:50]:
            f.write(f"| {company['rank']} | {company['company']} | {company['contract_value']} | {company['research_status']} |\n")
        f.write("\n## Research Steps\n\n")
        f.write("1. Visit company website\n")
        f.write("2. Search for 'Small Business' or 'Supplier Diversity'\n")
        f.write("3. Look for SBLO contact information\n")
        f.write("4. Try email patterns: smallbusiness@company.com, sblo@company.com\n")
        f.write("5. Update the CSV file with verified contacts\n")
    
    print(f"\n📝 Created research guide: {guide_file}")
    
    return research_list

if __name__ == '__main__':
    research_top_sba_companies()




