#!/usr/bin/env python3
"""
Automated SBLO Research Tool
Uses web search and company websites to find SBLO contacts
"""

import csv
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
import time

def find_sblo_on_website(company_name, website_url=None):
    """Try to find SBLO contact on company website"""
    if not website_url:
        # Try to construct website URL
        company_clean = company_name.lower()
        company_clean = re.sub(r'\s+(inc|llc|corp|corporation|lp|incorporated)$', '', company_clean)
        company_clean = re.sub(r'[^a-z0-9]', '', company_clean)
        website_url = f"https://www.{company_clean}.com"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(website_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text().lower()
            
            # Look for SBLO-related pages
            sblo_keywords = ['small business', 'supplier diversity', 'sblo', 'subcontracting', 'doing business']
            if any(keyword in text for keyword in sblo_keywords):
                # Try to find email
                emails = re.findall(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', response.text)
                sblo_emails = [e for e in emails if any(kw in e.lower() for kw in ['small', 'business', 'sblo', 'supplier', 'diversity'])]
                
                if sblo_emails:
                    return {
                        'website': website_url,
                        'email': sblo_emails[0],
                        'found': True
                    }
        
        return {'website': website_url, 'email': None, 'found': False}
    except:
        return {'website': website_url, 'email': None, 'found': False}

def research_dot_emails_automated():
    """Automated research for DOT email addresses"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Automated DOT Email Research                      ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    input_file = Path('dot-contacts.csv')
    
    if not input_file.exists():
        print(f"❌ File not found: {input_file}")
        return
    
    contacts = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        contacts = list(reader)
    
    print(f"📊 Researching emails for {len(contacts)} DOT contacts...")
    print("⚠️  This will take time - checking company websites...\n")
    
    found_count = 0
    enhanced_contacts = []
    
    # Research first 20 as a test
    for i, contact in enumerate(contacts[:20], 1):
        company = contact['company']
        print(f"   {i:2d}. Researching {company[:50]:50s}...", end=' ')
        
        result = find_sblo_on_website(company)
        
        if result['email']:
            contact['email'] = result['email']
            contact['website'] = result['website']
            contact['research_status'] = 'FOUND'
            found_count += 1
            print(f"✅ Found: {result['email']}")
        else:
            contact['email'] = '[NEEDS RESEARCH]'
            contact['research_status'] = 'NOT_FOUND'
            print("❌ Not found")
        
        enhanced_contacts.append(contact)
        time.sleep(1)  # Be polite to servers
    
    print(f"\n✅ Found {found_count}/20 emails in test run")
    
    # Save results
    output_file = Path('dot-contacts-researched.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'naics', 'address', 'source', 'research_status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enhanced_contacts)
    
    print(f"💾 Saved to: {output_file}")
    print("\n💡 To research all 133 contacts, run with full=True")
    
    return enhanced_contacts

def research_top_sba_companies_automated():
    """Automated research for top SBA companies"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Automated SBA SBLO Research (Top 20)              ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    sba_file = Path('sba-new-companies-need-sblo.csv')
    
    if not sba_file.exists():
        print(f"❌ File not found: {sba_file}")
        return
    
    companies = []
    with open(sba_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        companies = list(reader)
    
    # Sort by contract value
    companies_sorted = sorted(
        companies,
        key=lambda x: float(x.get('total_contract_value', 0) or 0),
        reverse=True
    )
    
    top_20 = companies_sorted[:20]
    
    print(f"📊 Researching top 20 SBA companies...\n")
    
    found_contacts = []
    
    for i, company in enumerate(top_20, 1):
        company_name = company['company']
        contract_value = company.get('total_contract_value', 0)
        value_str = f"${float(contract_value):,.0f}" if contract_value else 'N/A'
        
        print(f"   {i:2d}. {company_name[:50]:50s} ({value_str})...", end=' ')
        
        result = find_sblo_on_website(company_name)
        
        if result['email']:
            found_contacts.append({
                'company': company_name,
                'sblo_name': '[FOUND ON WEBSITE]',
                'email': result['email'],
                'phone': '[NEEDS RESEARCH]',
                'website': result['website'],
                'contract_value': value_str,
                'source': 'SBA Directory + Website Research'
            })
            print(f"✅ Found: {result['email']}")
        else:
            print("❌ Not found")
        
        time.sleep(1)  # Be polite
    
    if found_contacts:
        # Save found contacts
        output_file = Path('sba-top-20-researched.csv')
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['company', 'sblo_name', 'email', 'phone', 'website', 'contract_value', 'source']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(found_contacts)
        
        print(f"\n💾 Saved {len(found_contacts)} found contacts to: {output_file}")
        
        # Add to compiled list
        compiled_file = Path('sblo-list-compiled.csv')
        existing_emails = set()
        
        if compiled_file.exists():
            with open(compiled_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    email = row.get('email', '').lower()
                    if email:
                        existing_emails.add(email)
        
        new_count = 0
        with open(compiled_file, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'address', 'naics', 'source']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            for contact in found_contacts:
                email_lower = contact['email'].lower()
                if email_lower not in existing_emails:
                    writer.writerow({
                        'company': contact['company'],
                        'sblo_name': contact['sblo_name'],
                        'title': 'SBLO',
                        'email': contact['email'],
                        'phone': contact['phone'],
                        'address': '',
                        'naics': '',
                        'source': contact['source']
                    })
                    existing_emails.add(email_lower)
                    new_count += 1
        
        print(f"✅ Added {new_count} new contacts to compiled list")
    else:
        print("\n⚠️  No contacts found automatically")
        print("   Manual research required - see research guides created")
    
    return found_contacts

def main():
    print("Starting automated research...\n")
    
    # Research DOT emails (test run - first 20)
    print("="*60)
    print("TASK 1: Research DOT Email Addresses")
    print("="*60)
    dot_results = research_dot_emails_automated()
    
    print("\n" + "="*60)
    print("TASK 2: Research Top SBA SBLO Contacts")
    print("="*60)
    sba_results = research_top_sba_companies_automated()
    
    print("\n" + "="*60)
    print("✨ Research Complete!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   DOT contacts researched: {len(dot_results)}")
    print(f"   SBA contacts researched: {len(sba_results)}")
    print(f"\n💡 Next steps:")
    print(f"   - Review research results")
    print(f"   - Manually verify and complete missing contacts")
    print(f"   - Update compiled list with verified contacts")

if __name__ == '__main__':
    main()




