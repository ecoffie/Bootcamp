#!/usr/bin/env python3
"""
Final DHS Scraper - Extract ALL companies including Lockheed Martin
Extract multiple SBLO contacts per company where applicable
"""

import csv
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

def scrape_all_dhs_contacts():
    """Scrape ALL companies and ALL contacts from DHS page"""
    url = "https://www.dhs.gov/osdbu/prime-contractors"
    
    print(f"🌐 Fetching: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Failed: Status {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        all_contacts = []
        
        # Find all h2 tags (company names)
        h2_tags = soup.find_all('h2')
        
        print(f"📋 Processing {len(h2_tags)} company sections...")
        
        for h2 in h2_tags:
            company_name = h2.get_text().strip()
            
            # Skip headers
            if company_name.lower() in ['topics', 'keywords', 'prime contractors']:
                continue
            
            # Get all content until next h2
            content_elements = []
            current = h2.find_next_sibling()
            count = 0
            while current and count < 50:
                if current.name == 'h2':
                    break
                if current.name in ['p', 'div', 'ul', 'li', 'strong']:
                    content_elements.append(current)
                current = current.find_next_sibling()
                count += 1
            
            # Extract text from all elements
            full_text = ' '.join([elem.get_text() for elem in content_elements])
            
            # Find ALL "Small Business Liaison" sections
            # Pattern: "Small Business Liaison: Name" followed by email/phone
            
            # Extract all SBLO names with their associated info
            sblo_sections = []
            
            # Look for patterns like "Small Business Liaison: Name" or "Small Business Liaison Officer: Name"
            sblo_pattern = r'(?:Small Business Liaison|Small Business Liaison Officer|Supplier Diversity Manager|Deputy Small Business Liaison)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)'
            
            sblo_matches = list(re.finditer(sblo_pattern, full_text, re.IGNORECASE))
            
            # Extract all emails
            email_pattern = r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'
            emails = re.findall(email_pattern, full_text)
            
            # Extract all phones
            phone_pattern = r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})'
            phones = re.findall(phone_pattern, full_text)
            
            # Extract websites
            website_pattern = r'(https?://[^\s<>"]+|www\.[^\s<>"]+)'
            websites = re.findall(website_pattern, full_text)
            
            # Extract NAICS codes
            naics_codes = re.findall(r'\b(\d{6})\b', full_text)
            naics = ', '.join(set(naics_codes)) if naics_codes else ''
            
            # Create contacts - one per email, or one per SBLO name
            if emails:
                # If we have SBLO names, match them to emails
                if sblo_matches:
                    for i, email in enumerate(emails):
                        sblo_name = ''
                        if i < len(sblo_matches):
                            sblo_name = sblo_matches[i].group(1).strip()
                        elif len(sblo_matches) == 1:
                            sblo_name = sblo_matches[0].group(1).strip()
                        
                        contact = {
                            'company': company_name,
                            'sblo_name': sblo_name,
                            'email': email,
                            'phone': phones[i] if i < len(phones) else '',
                            'website': websites[0] if websites else '',
                            'naics': naics,
                            'source': 'DHS Prime Contractors Page'
                        }
                        all_contacts.append(contact)
                else:
                    # No SBLO names found, create one contact per email
                    for i, email in enumerate(emails):
                        contact = {
                            'company': company_name,
                            'sblo_name': '',
                            'email': email,
                            'phone': phones[i] if i < len(phones) else '',
                            'website': websites[0] if websites else '',
                            'naics': naics,
                            'source': 'DHS Prime Contractors Page'
                        }
                        all_contacts.append(contact)
            elif company_name:
                # Company with no email but still valid
                sblo_name = sblo_matches[0].group(1).strip() if sblo_matches else ''
                contact = {
                    'company': company_name,
                    'sblo_name': sblo_name,
                    'email': '',
                    'phone': phones[0] if phones else '',
                    'website': websites[0] if websites else '',
                    'naics': naics,
                    'source': 'DHS Prime Contractors Page'
                }
                all_contacts.append(contact)
        
        print(f"✅ Extracted {len(all_contacts)} total contacts")
        return all_contacts
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   DHS Final Scrape - ALL Companies & Contacts       ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    contacts = scrape_all_dhs_contacts()
    
    if not contacts:
        print("⚠️  No contacts extracted")
        return
    
    # Remove duplicates based on company+email
    seen = set()
    unique_contacts = []
    for contact in contacts:
        key = (contact['company'].lower(), contact['email'].lower() if contact['email'] else '')
        if key not in seen:
            seen.add(key)
            unique_contacts.append(contact)
    
    print(f"📊 Unique contacts: {len(unique_contacts)}")
    
    # Count unique companies
    unique_companies = set(c['company'] for c in unique_contacts)
    print(f"📊 Unique companies: {len(unique_companies)}")
    
    # Save to CSV
    output_file = Path('dhs-contacts-final.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'naics', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for contact in unique_contacts:
            writer.writerow({
                'company': contact['company'],
                'sblo_name': contact['sblo_name'],
                'title': 'SBLO',
                'email': contact['email'],
                'phone': contact['phone'],
                'website': contact['website'],
                'naics': contact['naics'],
                'source': contact['source']
            })
    
    print(f"💾 Saved to: {output_file}")
    
    # Check if we have all 76 companies
    expected_companies = 76
    if len(unique_companies) == expected_companies:
        print(f"✅ Perfect! Found all {expected_companies} companies!")
    else:
        print(f"⚠️  Found {len(unique_companies)}/{expected_companies} companies")
    
    # Show companies with multiple contacts
    company_counts = {}
    for contact in unique_contacts:
        company = contact['company']
        company_counts[company] = company_counts.get(company, 0) + 1
    
    multi_contact_companies = {k: v for k, v in company_counts.items() if v > 1}
    if multi_contact_companies:
        print(f"\n📋 Companies with multiple contacts ({len(multi_contact_companies)}):")
        for company, count in sorted(multi_contact_companies.items(), key=lambda x: x[1], reverse=True):
            print(f"   {company}: {count} contacts")
    
    print("\n📋 Sample contacts:")
    for i, contact in enumerate(unique_contacts[:20]):
        email = contact['email'][:35] if contact['email'] else 'N/A'
        print(f"   {i+1:2d}. {contact['company'][:35]:35s} - {email}")

if __name__ == '__main__':
    main()




