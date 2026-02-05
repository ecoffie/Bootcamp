#!/usr/bin/env python3
"""
Scrape DOT Subcontracting Directory using Firecrawl MCP
Extract SBLO contacts and add to compiled list
"""

import csv
import re
import json
from pathlib import Path
import subprocess
import sys

def scrape_with_firecrawl(url):
    """Scrape URL using Firecrawl MCP"""
    print(f"🌐 Scraping with Firecrawl MCP: {url}")
    
    try:
        # Try to use Firecrawl MCP via command line or API
        # Firecrawl MCP might be available as a CLI tool or API
        
        # Method 1: Try Firecrawl CLI if available
        try:
            result = subprocess.run(
                ['firecrawl', 'scrape', url],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get('markdown', '') or data.get('html', '') or data.get('content', '')
        except FileNotFoundError:
            pass
        
        # Method 2: Try Firecrawl Python SDK if installed
        try:
            from firecrawl import FirecrawlApp
            app = FirecrawlApp(api_key=None)  # May need API key
            result = app.scrape_url(url)
            return result.get('markdown', '') or result.get('html', '') or result.get('content', '')
        except ImportError:
            pass
        except Exception as e:
            print(f"⚠️  Firecrawl SDK error: {e}")
        
        # Method 3: Try MCP client if available
        try:
            # Firecrawl MCP might be accessible via MCP protocol
            # This would depend on your MCP setup
            print("⚠️  Firecrawl MCP not directly accessible")
            print("   Falling back to regular web scraping...")
            return None
        except:
            pass
        
        return None
        
    except Exception as e:
        print(f"❌ Error with Firecrawl: {e}")
        return None

def scrape_with_requests(url):
    """Fallback: Scrape using requests and BeautifulSoup"""
    print(f"🌐 Scraping with requests: {url}")
    
    try:
        import requests
        from bs4 import BeautifulSoup
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()
        else:
            print(f"❌ Failed to fetch: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error scraping: {e}")
        return None

def parse_dot_contacts(text):
    """Parse SBLO contacts from DOT directory text"""
    print("\n🔍 Parsing contacts from DOT directory...")
    
    if not text:
        return []
    
    contacts = []
    lines = text.split('\n')
    
    current_company = ''
    current_sblo = ''
    current_email = ''
    current_phone = ''
    current_website = ''
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        
        if not line_clean:
            # Save contact if we have company and email
            if current_company and current_email:
                contacts.append({
                    'company': current_company,
                    'sblo_name': current_sblo,
                    'email': current_email,
                    'phone': current_phone,
                    'website': current_website,
                    'source': 'DOT Subcontracting Directory'
                })
                # Reset
                current_company = ''
                current_sblo = ''
                current_email = ''
                current_phone = ''
                current_website = ''
            continue
        
        # Detect company names (usually longer, title case)
        if len(line_clean) > 5 and len(line_clean) < 100:
            # Check if it looks like a company name
            has_email = '@' in line_clean
            has_phone = bool(re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line_clean))
            has_numbers_only = bool(re.match(r'^[\d\s\-\(\)\.]+$', line_clean))
            
            if not has_email and not has_phone and not has_numbers_only:
                # Could be company name
                if current_company and current_email:
                    contacts.append({
                        'company': current_company,
                        'sblo_name': current_sblo,
                        'email': current_email,
                        'phone': current_phone,
                        'website': current_website,
                        'source': 'DOT Subcontracting Directory'
                    })
                
                current_company = line_clean
                current_sblo = ''
                current_email = ''
                current_phone = ''
                current_website = ''
                continue
        
        # Look for SBLO name patterns
        sblo_patterns = [
            r'Small Business Liaison[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'SBLO[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Small Business[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
            r'Contact[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)',
        ]
        
        for pattern in sblo_patterns:
            match = re.search(pattern, line_clean, re.IGNORECASE)
            if match:
                current_sblo = match.group(1).strip()
                break
        
        # Extract email
        email_match = re.search(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', line_clean)
        if email_match:
            current_email = email_match.group(1).strip()
        
        # Extract phone
        phone_patterns = [
            r'\((\d{3})\)\s*(\d{3})[-.\s]?(\d{4})',
            r'(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4})',
            r'Phone[:\s]+([\d\-\(\)\s]+)',
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, line_clean)
            if match:
                if len(match.groups()) == 3:
                    current_phone = f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
                else:
                    current_phone = match.group(0).strip()
                break
        
        # Extract website
        website_match = re.search(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', line_clean)
        if website_match:
            current_website = website_match.group(1).strip()
    
    # Don't forget last contact
    if current_company and current_email:
        contacts.append({
            'company': current_company,
            'sblo_name': current_sblo,
            'email': current_email,
            'phone': current_phone,
            'website': current_website,
            'source': 'DOT Subcontracting Directory'
        })
    
    print(f"✅ Found {len(contacts)} contacts")
    return contacts

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Scrape DOT Subcontracting Directory              ║
    ║   Using Firecrawl MCP                               ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    url = "https://www.transportation.gov/osdbu/procurement-assistance/dot-subcontracting-directory"
    
    # Try Firecrawl MCP first
    text = scrape_with_firecrawl(url)
    
    # Fallback to regular scraping
    if not text:
        text = scrape_with_requests(url)
    
    if not text:
        print("❌ Could not scrape DOT directory")
        print("\n💡 Alternative approaches:")
        print("   1. Install Firecrawl: pip install firecrawl-py")
        print("   2. Use Firecrawl MCP server if configured")
        print("   3. Manually download the directory and process")
        return
    
    # Parse contacts
    contacts = parse_dot_contacts(text)
    
    if not contacts:
        print("⚠️  No contacts extracted. The page structure may be different.")
        print("   Saving raw text for manual review...")
        with open('dot-directory-raw.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        print("   Saved to: dot-directory-raw.txt")
        return
    
    # Remove duplicates
    seen = set()
    unique_contacts = []
    for contact in contacts:
        key = (contact['company'].lower().strip(), contact['email'].lower().strip() if contact['email'] else '')
        if key not in seen and contact['email']:
            seen.add(key)
            unique_contacts.append(contact)
    
    print(f"\n📊 Unique contacts: {len(unique_contacts)}")
    
    # Save results
    output_file = Path('dot-contacts.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'source']
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
                'source': contact['source']
            })
    
    print(f"💾 Saved to: {output_file}")
    
    # Show sample
    print("\n📋 Sample contacts:")
    for i, contact in enumerate(unique_contacts[:15], 1):
        email = contact['email'][:35] if contact['email'] else 'N/A'
        print(f"   {i:2d}. {contact['company'][:40]:40s} - {email}")
    
    # Update compiled list
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
                    'naics': '',
                    'source': contact['source']
                })
                existing_emails.add(email_lower)
                new_count += 1
    
    print(f"\n✅ Added {new_count} new contacts to compiled list")
    print(f"📊 Total in compiled list: {len(existing_emails)}")
    
    print("\n" + "="*60)
    print("✨ Processing Complete!")
    print("="*60)

if __name__ == '__main__':
    main()




