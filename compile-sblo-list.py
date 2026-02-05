#!/usr/bin/env python3
"""
SBLO List Compiler
Automatically downloads and compiles SBLO contacts from public sources
"""

import csv
import json
import requests
import sys
from pathlib import Path
from urllib.parse import urlparse
import re

# Try to import optional libraries
try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    print("⚠️  pandas not installed. Install with: pip install pandas openpyxl")

try:
    import PyPDF2
    HAS_PDF = True
except ImportError:
    HAS_PDF = False
    print("⚠️  PyPDF2 not installed. Install with: pip install PyPDF2")

# Data sources
SOURCES = {
    'sba_prime': {
        'url': 'https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans',
        'type': 'excel',
        'description': 'SBA Prime Directory (300+ primes)'
    },
    'dod_csp': {
        'url': 'https://business.defense.gov/Portals/57/Documents/Dod%20CSP%20Prime%20Contractor%20Directory_May%202025.pdf',
        'type': 'pdf',
        'description': 'DoD CSP Prime Directory (100+ primes)'
    },
    'dhs_primes': {
        'url': 'https://www.dhs.gov/osdbu/prime-contractors',
        'type': 'web',
        'description': 'DHS Prime Contractors List (50+ primes)'
    }
}

def download_file(url, filename):
    """Download a file from URL"""
    try:
        print(f"📥 Downloading {filename}...")
        response = requests.get(url, timeout=30, allow_redirects=True)
        if response.status_code == 200:
            filepath = Path('sblo-data-downloads') / filename
            filepath.parent.mkdir(exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✅ Downloaded: {filepath}")
            return filepath
        else:
            print(f"❌ Failed to download {url}: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")
        return None

def parse_excel(filepath):
    """Parse Excel file and extract SBLO contacts"""
    if not HAS_PANDAS:
        return []
    
    contacts = []
    try:
        # Try to read Excel file
        df = pd.read_excel(filepath, engine='openpyxl')
        
        # Look for common column names
        name_cols = [col for col in df.columns if any(x in col.lower() for x in ['name', 'company', 'contractor', 'prime'])]
        email_cols = [col for col in df.columns if 'email' in col.lower()]
        phone_cols = [col for col in df.columns if any(x in col.lower() for x in ['phone', 'tel'])]
        sblo_cols = [col for col in df.columns if 'sblo' in col.lower() or 'small business' in col.lower()]
        
        print(f"📊 Found columns: {list(df.columns)}")
        
        for idx, row in df.iterrows():
            contact = {
                'company': '',
                'sblo_name': '',
                'email': '',
                'phone': '',
                'source': filepath.name
            }
            
            # Extract company name
            if name_cols:
                contact['company'] = str(row[name_cols[0]]) if pd.notna(row[name_cols[0]]) else ''
            
            # Extract SBLO name
            if sblo_cols:
                contact['sblo_name'] = str(row[sblo_cols[0]]) if pd.notna(row[sblo_cols[0]]) else ''
            
            # Extract email
            if email_cols:
                contact['email'] = str(row[email_cols[0]]) if pd.notna(row[email_cols[0]]) else ''
            
            # Extract phone
            if phone_cols:
                contact['phone'] = str(row[phone_cols[0]]) if pd.notna(row[phone_cols[0]]) else ''
            
            if contact['company'] or contact['sblo_name']:
                contacts.append(contact)
        
        print(f"✅ Extracted {len(contacts)} contacts from Excel")
        return contacts
        
    except Exception as e:
        print(f"❌ Error parsing Excel: {e}")
        return []

def parse_pdf(filepath):
    """Extract text from PDF and find SBLO contacts"""
    if not HAS_PDF:
        return []
    
    contacts = []
    try:
        with open(filepath, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
        
        # Look for patterns like "Company Name: ... SBLO: ... Phone: ..."
        # This is a simple pattern - you may need to adjust based on actual PDF format
        lines = text.split('\n')
        current_company = ''
        
        for line in lines:
            # Look for company names (usually in caps or bold)
            if len(line) > 5 and line.isupper():
                current_company = line.strip()
            
            # Look for SBLO patterns
            if 'sblo' in line.lower() or 'small business' in line.lower():
                # Try to extract name and phone
                name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', line)
                phone_match = re.search(r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})', line)
                email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
                
                if name_match or current_company:
                    contacts.append({
                        'company': current_company,
                        'sblo_name': name_match.group(1) if name_match else '',
                        'email': email_match.group(1) if email_match else '',
                        'phone': phone_match.group(1) if phone_match else '',
                        'source': filepath.name
                    })
        
        print(f"✅ Extracted {len(contacts)} contacts from PDF")
        return contacts
        
    except Exception as e:
        print(f"❌ Error parsing PDF: {e}")
        return []

def scrape_dhs_page():
    """Scrape DHS prime contractors page"""
    contacts = []
    try:
        url = 'https://www.dhs.gov/osdbu/prime-contractors'
        print(f"🌐 Scraping {url}...")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=30, headers=headers)
        
        if response.status_code == 200:
            html = response.text
            
            # Look for email patterns
            emails = re.findall(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', html)
            
            # Look for company names - try multiple patterns
            # Pattern 1: Links with company names
            company_links = re.findall(r'<a[^>]*>([A-Z][^<]{3,50})</a>', html)
            # Pattern 2: Strong/bold text (often company names)
            company_bold = re.findall(r'<strong>([^<]{3,50})</strong>', html)
            # Pattern 3: Headings
            company_headings = re.findall(r'<h[23][^>]*>([^<]{3,50})</h[23]>', html)
            
            all_companies = list(set(company_links + company_bold + company_headings))
            
            # Map emails to companies (simple heuristic)
            email_to_company = {}
            lines = html.split('\n')
            for i, line in enumerate(lines):
                for email in emails:
                    if email in line.lower():
                        # Look for company name nearby
                        for j in range(max(0, i-5), min(len(lines), i+5)):
                            for company in all_companies:
                                if company.lower() in lines[j].lower() and len(company) > 3:
                                    email_to_company[email] = company.strip()
                                    break
                            if email in email_to_company:
                                break
            
            for email in set(emails):
                if any(keyword in email.lower() for keyword in ['smallbusiness', 'sblo', 'osdbu', 'small.business', 'supplier']):
                    company = email_to_company.get(email, '')
                    # Try to extract company from email domain
                    if not company:
                        domain = email.split('@')[1] if '@' in email else ''
                        # Remove common suffixes
                        domain = domain.replace('.com', '').replace('.gov', '').replace('.org', '')
                        # Capitalize
                        company = domain.replace('.', ' ').title() if domain else 'Unknown'
                    
                    contacts.append({
                        'company': company,
                        'sblo_name': '',
                        'email': email,
                        'phone': '',
                        'source': 'DHS Web Scrape'
                    })
            
            print(f"✅ Found {len(contacts)} contacts from DHS page")
        else:
            print(f"❌ Failed to scrape DHS page: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error scraping DHS page: {e}")
    
    return contacts

def compile_contacts():
    """Main function to compile all contacts"""
    all_contacts = []
    
    print("🚀 Starting SBLO List Compilation...")
    print("=" * 50)
    
    # Download and parse each source
    for source_id, source_info in SOURCES.items():
        print(f"\n📋 Processing: {source_info['description']}")
        
        if source_info['type'] == 'excel':
            # For Excel, we'll need the actual download URL
            # The SBA page might redirect or require clicking a download button
            print("⚠️  Excel files may need manual download from the website")
            print(f"   URL: {source_info['url']}")
            
        elif source_info['type'] == 'pdf':
            filename = f"{source_id}.pdf"
            filepath = download_file(source_info['url'], filename)
            if filepath and filepath.exists():
                contacts = parse_pdf(filepath)
                all_contacts.extend(contacts)
                
        elif source_info['type'] == 'web':
            contacts = scrape_dhs_page()
            all_contacts.extend(contacts)
    
    # Remove duplicates
    seen = set()
    unique_contacts = []
    for contact in all_contacts:
        key = (contact['company'], contact['email'])
        if key not in seen and contact['company']:
            seen.add(key)
            unique_contacts.append(contact)
    
    print(f"\n✅ Compiled {len(unique_contacts)} unique contacts")
    
    # Save to CSV
    output_file = Path('sblo-list-compiled.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        if unique_contacts:
            writer = csv.DictWriter(f, fieldnames=unique_contacts[0].keys())
            writer.writeheader()
            writer.writerows(unique_contacts)
        else:
            # Create empty file with headers
            writer = csv.DictWriter(f, fieldnames=['company', 'sblo_name', 'email', 'phone', 'source'])
            writer.writeheader()
    
    print(f"💾 Saved to: {output_file}")
    
    # Also update the main CSV
    update_main_csv(unique_contacts)
    
    return unique_contacts

def update_main_csv(new_contacts):
    """Update the main sblo-list.csv with new contacts"""
    try:
        main_csv = Path('sblo-list.csv')
        if main_csv.exists():
            print(f"\n📝 Updating {main_csv}...")
            # Read existing
            with open(main_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                existing = list(reader)
            
            # Add new contacts (avoid duplicates)
            existing_companies = {row.get('Agency', '') + row.get('Company Name', '') for row in existing}
            
            for contact in new_contacts:
                company_key = contact['company']
                if company_key not in existing_companies:
                    existing.append({
                        'Agency': 'Prime Contractor',
                        'Office/Program': 'Small Business',
                        'Contact Name': contact['sblo_name'],
                        'Title': 'SBLO',
                        'Email': contact['email'],
                        'Phone': contact['phone'],
                        'Website': '',
                        'Address': '',
                        'City': '',
                        'State': '',
                        'Notes': f"From {contact['source']}",
                        'Unobligated Balance (Dec 2025)': '',
                        'Key NAICS': ''
                    })
            
            # Write back
            if existing:
                with open(main_csv, 'w', newline='', encoding='utf-8') as f:
                    fieldnames = existing[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(existing)
            
            print(f"✅ Updated {main_csv} with {len(new_contacts)} new contacts")
    except Exception as e:
        print(f"⚠️  Could not update main CSV: {e}")

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════╗
    ║      SBLO List Compiler - Automated Tool        ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    # Check dependencies
    if not HAS_PANDAS:
        print("\n⚠️  WARNING: pandas not installed")
        print("   Install with: pip install pandas openpyxl")
        print("   Continuing with limited functionality...\n")
    
    contacts = compile_contacts()
    
    print("\n" + "=" * 50)
    print("✨ Compilation Complete!")
    print("\nNext steps:")
    print("1. Review sblo-list-compiled.csv")
    print("2. Manually download Excel files if needed")
    print("3. Verify and clean up contacts")
    print("4. Update sblo-list.html with verified contacts")

