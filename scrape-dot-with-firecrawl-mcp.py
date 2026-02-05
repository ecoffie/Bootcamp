#!/usr/bin/env python3
"""
Scrape DOT Directory using Firecrawl MCP
This script interfaces with Firecrawl MCP server to scrape JavaScript-rendered pages
"""

import csv
import re
import json
import subprocess
import sys
from pathlib import Path

def scrape_with_firecrawl_mcp(url):
    """
    Scrape using Firecrawl MCP server
    Firecrawl MCP can be accessed via:
    1. MCP protocol (if MCP server is running)
    2. Firecrawl API (if API key is configured)
    3. Firecrawl CLI (if installed)
    """
    print(f"🌐 Scraping with Firecrawl MCP: {url}")
    
    # Method 1: Try MCP protocol via stdio
    # If Firecrawl MCP server is configured, it might be accessible via stdio
    try:
        # Firecrawl MCP typically uses JSON-RPC over stdio
        # This would require the MCP server to be running
        print("   Attempting MCP protocol connection...")
        # Note: This would need to be configured based on your MCP setup
        pass
    except Exception as e:
        print(f"   MCP protocol not available: {e}")
    
    # Method 2: Try Firecrawl Python SDK with API key from env
    try:
        import os
        from firecrawl import FirecrawlApp
        
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if api_key:
            print("   Using Firecrawl SDK with API key...")
            app = FirecrawlApp(api_key=api_key)
            result = app.scrape(url)
            
            # Extract content from Document object
            if hasattr(result, 'markdown') and result.markdown:
                content = result.markdown
                print(f"   ✅ Successfully scraped {len(content)} characters")
                return content
            elif hasattr(result, 'html') and result.html:
                content = result.html
                print(f"   ✅ Successfully scraped HTML {len(content)} characters")
                return content
            elif hasattr(result, 'content') and result.content:
                content = result.content
                print(f"   ✅ Successfully scraped {len(content)} characters")
                return content
        else:
            print("   ⚠️  FIRECRAWL_API_KEY not set in environment")
    except ImportError:
        print("   ⚠️  Firecrawl SDK not installed (pip install firecrawl-py)")
    except Exception as e:
        print(f"   ⚠️  Firecrawl SDK error: {e}")
    
    # Method 3: Try Firecrawl CLI
    try:
        print("   Attempting Firecrawl CLI...")
        result = subprocess.run(
            ['firecrawl', 'scrape', url, '--format', 'markdown'],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0 and result.stdout:
            print(f"   ✅ Successfully scraped via CLI")
            return result.stdout
    except FileNotFoundError:
        print("   ⚠️  Firecrawl CLI not found")
    except Exception as e:
        print(f"   ⚠️  Firecrawl CLI error: {e}")
    
    # Method 4: Instructions for manual setup
    print("\n" + "="*60)
    print("📋 Firecrawl MCP Setup Instructions")
    print("="*60)
    print("""
To use Firecrawl MCP, you need to:

1. Install Firecrawl SDK:
   pip install firecrawl-py

2. Set API key (get from https://firecrawl.dev):
   export FIRECRAWL_API_KEY='your-api-key-here'

3. Or configure Firecrawl MCP server if using Model Context Protocol

4. Then run this script again

Alternatively, you can manually:
- Visit: https://www.transportation.gov/osdbu/procurement-assistance/dot-subcontracting-directory
- Copy the page content
- Save to: dot-directory-manual.html
- Run: python3 parse-dot-manual.py
    """)
    
    return None

def parse_dot_directory(text):
    """Parse DOT directory content for SBLO contacts"""
    if not text:
        return []
    
    print("\n🔍 Parsing DOT directory content...")
    
    contacts = []
    
    # The DOT directory likely has a table or list structure
    # Look for patterns like:
    # Company Name | SBLO Name | Email | Phone
    
    # Extract all emails first
    emails = re.findall(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', text)
    
    # Extract company names (usually near emails)
    lines = text.split('\n')
    
    current_company = ''
    current_sblo = ''
    current_email = ''
    current_phone = ''
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        
        # Look for company names (usually in headings or table rows)
        # Company names are often followed by contact info
        
        # Check if line contains an email
        email_match = re.search(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', line_clean)
        if email_match:
            current_email = email_match.group(1)
            
            # Look backwards for company name
            for j in range(max(0, i-5), i):
                prev_line = lines[j].strip()
                if len(prev_line) > 5 and len(prev_line) < 80:
                    if not '@' in prev_line and not re.match(r'^[\d\s\-\(\)\.]+$', prev_line):
                        if not any(word in prev_line.lower() for word in ['email', 'phone', 'contact', 'sblo']):
                            current_company = prev_line
                            break
            
            # Look for SBLO name in same line or nearby
            sblo_match = re.search(r'(?:Small Business Liaison|SBLO|Contact)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', line_clean, re.IGNORECASE)
            if sblo_match:
                current_sblo = sblo_match.group(1).strip()
            
            # Extract phone
            phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', line_clean)
            if phone_match:
                current_phone = phone_match.group(1).strip()
            
            # Save contact if we have company and email
            if current_company and current_email:
                contacts.append({
                    'company': current_company,
                    'sblo_name': current_sblo,
                    'email': current_email,
                    'phone': current_phone,
                    'website': '',
                    'source': 'DOT Subcontracting Directory'
                })
            
            # Reset for next contact
            current_company = ''
            current_sblo = ''
            current_phone = ''
    
    print(f"✅ Found {len(contacts)} contacts")
    return contacts

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   DOT Directory Scraper - Firecrawl MCP              ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    url = "https://www.transportation.gov/osdbu/procurement-assistance/dot-subcontracting-directory"
    
    # Scrape with Firecrawl MCP
    content = scrape_with_firecrawl_mcp(url)
    
    if not content:
        print("\n⚠️  Could not scrape with Firecrawl MCP")
        print("   Please set up Firecrawl MCP or provide manual content")
        return
    
    # Parse contacts
    contacts = parse_dot_directory(content)
    
    if not contacts:
        print("⚠️  No contacts found. Saving raw content for review...")
        with open('dot-directory-firecrawl-output.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        print("   Saved to: dot-directory-firecrawl-output.txt")
        return
    
    # Remove duplicates
    seen = set()
    unique_contacts = []
    for contact in contacts:
        key = (contact['company'].lower().strip(), contact['email'].lower().strip())
        if key not in seen:
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
    
    print(f"\n✅ Added {new_count} new contacts to compiled list")
    print(f"📊 Total in compiled list: {len(existing_emails)}")
    
    print("\n" + "="*60)
    print("✨ Processing Complete!")
    print("="*60)

if __name__ == '__main__':
    main()

