#!/usr/bin/env python3
"""
Enhanced DHS Scraper - Extracts ALL contacts including multiple SBLOs per company
"""

import csv
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

def scrape_dhs_all_contacts():
    """Scrape and extract ALL contacts, including multiple SBLOs per company"""
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
        contacts = []
        
        # Find all h2 tags (company names)
        h2_tags = soup.find_all('h2')
        
        print(f"📋 Processing {len(h2_tags)} company sections...")
        
        for h2 in h2_tags:
            company_name = h2.get_text().strip()
            
            # Skip headers
            if company_name.lower() in ['topics', 'keywords', 'prime contractors']:
                continue
            
            # Get content section
            content_section = []
            current = h2.find_next_sibling()
            count = 0
            while current and count < 30:
                if current.name == 'h2':
                    break
                if current.name in ['p', 'div', 'ul', 'li']:
                    content_section.append(current.get_text())
                current = current.find_next_sibling()
                count += 1
            
            content_text = ' '.join(content_section)
            
            # Extract ALL email addresses (more precise pattern)
            emails = []
            email_pattern = r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b'
            email_matches = re.finditer(email_pattern, content_text)
            for match in email_matches:
                email = match.group(1)
                # Clean up common prefixes/suffixes
                email = email.strip('.,;:')
                if email and '@' in email:
                    emails.append(email)
            
            # Extract ALL SBLO names (multiple patterns)
            sblo_names = []
            sblo_patterns = [
                r'Small Business Liaison[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Small Business Liaison Officer[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Supplier Diversity Manager[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Deputy Small Business Liaison[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            ]
            
            for pattern in sblo_patterns:
                matches = re.findall(pattern, content_text, re.IGNORECASE)
                sblo_names.extend(matches)
            
            # Extract phone numbers
            phones = re.findall(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', content_text)
            
            # Extract websites
            websites = re.findall(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', content_text)
            
            # Extract NAICS codes
            naics_codes = re.findall(r'\b(\d{6})\b', content_text)
            naics = ', '.join(set(naics_codes)) if naics_codes else ''
            
            # Create contact entries - one per email
            if emails:
                for i, email in enumerate(emails):
                    contact = {
                        'company': company_name,
                        'sblo_name': sblo_names[i] if i < len(sblo_names) else '',
                        'email': email,
                        'phone': phones[i] if i < len(phones) else '',
                        'website': websites[0] if websites else '',
                        'naics': naics,
                        'source': 'DHS Prime Contractors Page'
                    }
                    contacts.append(contact)
            elif company_name:  # Company with no email but still valid
                contact = {
                    'company': company_name,
                    'sblo_name': sblo_names[0] if sblo_names else '',
                    'email': '',
                    'phone': phones[0] if phones else '',
                    'website': websites[0] if websites else '',
                    'naics': naics,
                    'source': 'DHS Prime Contractors Page'
                }
                contacts.append(contact)
        
        print(f"✅ Extracted {len(contacts)} total contacts")
        return contacts
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   DHS - Extract ALL Contacts (Including Multi)      ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    contacts = scrape_dhs_all_contacts()
    
    if not contacts:
        print("⚠️  No contacts extracted")
        return
    
    # Remove duplicates based on email
    seen_emails = set()
    unique_contacts = []
    for contact in contacts:
        email = contact['email'].lower() if contact['email'] else ''
        key = (contact['company'].lower(), email)
        if key not in seen_emails:
            seen_emails.add(key)
            unique_contacts.append(contact)
    
    print(f"📊 Unique contacts: {len(unique_contacts)}")
    
    # Save to CSV
    output_file = Path('dhs-contacts-complete.csv')
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
    
    # Update compiled list
    compiled_file = Path('sblo-list-compiled.csv')
    existing_emails = set()
    
    if compiled_file.exists():
        with open(compiled_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_emails = {row.get('email', '').lower() for row in reader if row.get('email')}
    
    new_count = 0
    with open(compiled_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'address', 'naics', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        for contact in unique_contacts:
            email_lower = contact['email'].lower() if contact['email'] else ''
            if email_lower and email_lower not in existing_emails:
                writer.writerow({
                    'company': contact['company'],
                    'sblo_name': contact['sblo_name'],
                    'title': 'SBLO',
                    'email': contact['email'],
                    'phone': contact['phone'],
                    'address': '',
                    'naics': contact['naics'],
                    'source': contact['source']
                })
                existing_emails.add(email_lower)
                new_count += 1
    
    print(f"✅ Added {new_count} new contacts to compiled list")
    print(f"📊 Total in compiled list: {len(existing_emails)}")
    
    print("\n📋 Sample contacts:")
    for i, contact in enumerate(unique_contacts[:20]):
        email = contact['email'][:35] if contact['email'] else 'N/A'
        print(f"   {i+1:2d}. {contact['company'][:35]:35s} - {email}")

if __name__ == '__main__':
    main()

