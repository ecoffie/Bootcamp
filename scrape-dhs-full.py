#!/usr/bin/env python3
"""
Comprehensive DHS Prime Contractors Scraper
Extracts ALL companies and contacts from the full HTML page
"""

import csv
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

def scrape_dhs_page_full():
    """Scrape the full DHS page and extract all contacts"""
    url = "https://www.dhs.gov/osdbu/prime-contractors"
    
    print(f"🌐 Fetching full page: {url}")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Failed to fetch page: Status {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        contacts = []
        
        # Find all h2 tags (company names)
        h2_tags = soup.find_all('h2')
        
        print(f"📋 Found {len(h2_tags)} potential company sections")
        
        for h2 in h2_tags:
            company_name = h2.get_text().strip()
            
            # Skip if it's not a company (like "Topics" or other headers)
            if company_name.lower() in ['topics', 'keywords', 'prime contractors']:
                continue
            
            # Get the content after this h2 tag
            next_sibling = h2.find_next_sibling()
            contact = {
                'company': company_name,
                'sblo_name': '',
                'email': '',
                'phone': '',
                'website': '',
                'naics': '',
                'source': 'DHS Prime Contractors Page'
            }
            
            # Parse the content section
            content_text = ''
            current = next_sibling
            count = 0
            while current and count < 20:  # Limit to next 20 siblings
                if current.name == 'h2':  # Stop at next company
                    break
                content_text += str(current)
                current = current.find_next_sibling()
                count += 1
            
            # Extract SBLO name
            sblo_patterns = [
                r'Small Business Liaison[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Small Business Liaison Officer[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Supplier Diversity Manager[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
                r'Deputy Small Business Liaison[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            ]
            
            for pattern in sblo_patterns:
                match = re.search(pattern, content_text, re.IGNORECASE)
                if match:
                    contact['sblo_name'] = match.group(1).strip()
                    break
            
            # Extract email
            email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', content_text)
            if email_match:
                contact['email'] = email_match.group(1)
            
            # Extract phone
            phone_patterns = [
                r'\((\d{3})\)\s*(\d{3})[-.\s]?(\d{4})',
                r'(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})',
            ]
            for pattern in phone_patterns:
                match = re.search(pattern, content_text)
                if match:
                    contact['phone'] = f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
                    break
            
            # Extract website
            website_match = re.search(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', content_text)
            if website_match:
                contact['website'] = website_match.group(1)
            
            # Extract NAICS codes
            naics_matches = re.findall(r'\b(\d{6})\b', content_text)
            if naics_matches:
                contact['naics'] = ', '.join(set(naics_matches))
            
            # Only add if we have at least company name and email
            if contact['company'] and contact['email']:
                contacts.append(contact)
        
        print(f"✅ Extracted {len(contacts)} contacts")
        return contacts
        
    except Exception as e:
        print(f"❌ Error scraping page: {e}")
        return []

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   DHS Prime Contractors - FULL Page Scraper          ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Check if BeautifulSoup is available
    try:
        import bs4
    except ImportError:
        print("❌ BeautifulSoup4 not installed")
        print("   Install with: pip3 install beautifulsoup4 --user")
        return
    
    contacts = scrape_dhs_page_full()
    
    if not contacts:
        print("\n⚠️  No contacts extracted. Trying alternative method...")
        # Fallback: use the manual extraction
        return
    
    # Save to CSV
    output_file = Path('dhs-contacts-full.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'naics', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for contact in contacts:
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
    
    print(f"\n💾 Saved {len(contacts)} contacts to: {output_file}")
    
    # Update compiled list
    compiled_file = Path('sblo-list-compiled.csv')
    if compiled_file.exists():
        with open(compiled_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing = list(reader)
            existing_emails = {row.get('email', '').lower() for row in existing}
    else:
        existing_emails = set()
    
    with open(compiled_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'address', 'naics', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        for contact in contacts:
            if contact['email'].lower() not in existing_emails:
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
                existing_emails.add(contact['email'].lower())
    
    print(f"✅ Updated {compiled_file}")
    print(f"\n📊 Total contacts now: {len(existing_emails) + len(contacts)}")
    
    print("\n📋 Sample contacts:")
    for i, contact in enumerate(contacts[:15]):
        print(f"   {i+1:2d}. {contact['company'][:40]:40s} - {contact['email']}")

if __name__ == '__main__':
    main()




