#!/usr/bin/env python3
"""
Aggressive SBLO Contact Downloader
Downloads and processes all available sources automatically
"""

import requests
import pandas as pd
import PyPDF2
import csv
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
import time

# Create downloads directory
downloads_dir = Path('sblo-data-downloads')
downloads_dir.mkdir(exist_ok=True)

def download_with_session(url, filename, headers=None):
    """Download file with proper headers"""
    if headers is None:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/pdf,text/html,*/*',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    
    try:
        print(f"📥 Downloading: {filename}")
        response = requests.get(url, headers=headers, timeout=60, allow_redirects=True, stream=True)
        
        if response.status_code == 200:
            filepath = downloads_dir / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Saved: {filepath} ({filepath.stat().st_size / 1024:.1f} KB)")
            return filepath
        else:
            print(f"❌ Failed: Status {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def find_download_link(base_url, session=None):
    """Try to find actual download link from a page"""
    if session is None:
        session = requests.Session()
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = session.get(base_url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            html = response.text
            # Look for download links
            patterns = [
                r'href=["\']([^"\']*\.(xlsx|xls|pdf))["\']',
                r'href=["\']([^"\']*download[^"\']*)["\']',
                r'data-url=["\']([^"\']*)["\']',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                for match in matches:
                    link = match if isinstance(match, str) else match[0]
                    if link.startswith('http'):
                        return link
                    elif link.startswith('/'):
                        return urljoin(base_url, link)
        return None
    except:
        return None

def download_sba_directory():
    """Download SBA Prime Directory"""
    print("\n" + "="*60)
    print("📋 SBA Prime Directory (300+ primes)")
    print("="*60)
    
    base_url = "https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans"
    
    # Try direct download URLs (common patterns)
    possible_urls = [
        "https://www.sba.gov/sites/default/files/2025-03/Prime%20Contractor%20Directory.xlsx",
        "https://www.sba.gov/sites/default/files/2025-03/Prime_Contractor_Directory.xlsx",
        "https://www.sba.gov/sites/default/files/2024/FY2024_Prime_Contractor_Directory.xlsx",
        base_url + "/download",
    ]
    
    for url in possible_urls:
        filepath = download_with_session(url, "sba-prime-directory.xlsx")
        if filepath and filepath.exists() and filepath.stat().st_size > 1000:
            return filepath
    
    print("⚠️  Could not auto-download. Manual download needed:")
    print(f"   {base_url}")
    return None

def download_dod_directory():
    """Download DoD CSP Directory"""
    print("\n" + "="*60)
    print("📋 DoD CSP Prime Directory (100+ primes)")
    print("="*60)
    
    url = "https://business.defense.gov/Portals/57/Documents/Dod%20CSP%20Prime%20Contractor%20Directory_May%202025.pdf"
    
    filepath = download_with_session(url, "dod-csp-directory.pdf")
    if filepath and filepath.exists():
        return filepath
    
    # Try alternative URL
    alt_url = "https://business.defense.gov/Portals/57/Documents/Dod_CSP_Prime_Contractor_Directory_May_2025.pdf"
    filepath = download_with_session(alt_url, "dod-csp-directory.pdf")
    
    if not filepath or not filepath.exists():
        print("⚠️  Could not auto-download. Manual download needed:")
        print(f"   https://business.defense.gov/Portals/57/Documents/Dod%20CSP%20Prime%20Contractor%20Directory_May%202025.pdf")
    
    return filepath

def scrape_dhs_contacts():
    """Scrape DHS prime contractors"""
    print("\n" + "="*60)
    print("📋 DHS Prime Contractors (50+ primes)")
    print("="*60)
    
    contacts = []
    url = "https://www.dhs.gov/osdbu/prime-contractors"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            html = response.text
            
            # Extract emails
            emails = re.findall(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', html)
            
            # Extract company names from various patterns
            company_patterns = [
                r'<h[23][^>]*>([^<]{3,80})</h[23]>',
                r'<strong>([^<]{3,80})</strong>',
                r'<li[^>]*>([^<]{3,80})</li>',
                r'<a[^>]*>([A-Z][^<]{3,80})</a>',
            ]
            
            companies = []
            for pattern in company_patterns:
                matches = re.findall(pattern, html)
                companies.extend([m.strip() for m in matches if 3 < len(m.strip()) < 80])
            
            # Match emails to companies
            for email in set(emails):
                if any(keyword in email.lower() for keyword in ['smallbusiness', 'sblo', 'osdbu', 'small.business', 'supplier', 'diversity']):
                    # Try to find company name
                    company = ''
                    email_domain = email.split('@')[1].split('.')[0] if '@' in email else ''
                    
                    # Look for company name near email in HTML
                    email_pos = html.lower().find(email.lower())
                    if email_pos > 0:
                        context = html[max(0, email_pos-500):email_pos+500]
                        for comp in companies:
                            if comp.lower() in context.lower():
                                company = comp
                                break
                    
                    # Fallback: use domain name
                    if not company and email_domain:
                        company = email_domain.replace('-', ' ').replace('_', ' ').title()
                    
                    contacts.append({
                        'company': company or 'Unknown',
                        'sblo_name': '',
                        'title': 'SBLO',
                        'email': email,
                        'phone': '',
                        'address': '',
                        'naics': '',
                        'source': 'DHS Web Scrape'
                    })
            
            print(f"✅ Found {len(contacts)} contacts")
            return contacts
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return contacts

def process_all_files():
    """Process all downloaded files"""
    print("\n" + "="*60)
    print("🔄 Processing Files")
    print("="*60)
    
    all_contacts = []
    
    # Process Excel files
    excel_files = list(downloads_dir.glob('*.xlsx')) + list(downloads_dir.glob('*.xls'))
    for excel_file in excel_files:
        print(f"\n📊 Processing: {excel_file.name}")
        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
            print(f"   Rows: {len(df)}, Columns: {len(df.columns)}")
            
            # Find columns
            name_cols = [col for col in df.columns if any(x in str(col).lower() for x in ['name', 'company', 'contractor', 'prime', 'firm'])]
            email_cols = [col for col in df.columns if 'email' in str(col).lower()]
            phone_cols = [col for col in df.columns if any(x in str(col).lower() for x in ['phone', 'tel'])]
            sblo_cols = [col for col in df.columns if any(x in str(col).lower() for x in ['sblo', 'small business', 'liaison'])]
            
            for idx, row in df.iterrows():
                contact = {
                    'company': '',
                    'sblo_name': '',
                    'title': 'SBLO',
                    'email': '',
                    'phone': '',
                    'address': '',
                    'naics': '',
                    'source': excel_file.name
                }
                
                if name_cols:
                    val = row[name_cols[0]]
                    if pd.notna(val):
                        contact['company'] = str(val).strip()
                
                if sblo_cols:
                    val = row[sblo_cols[0]]
                    if pd.notna(val):
                        contact['sblo_name'] = str(val).strip()
                
                if email_cols:
                    val = row[email_cols[0]]
                    if pd.notna(val) and '@' in str(val):
                        contact['email'] = str(val).strip()
                
                if phone_cols:
                    val = row[phone_cols[0]]
                    if pd.notna(val):
                        contact['phone'] = str(val).strip()
                
                if contact['company'] or contact['email']:
                    all_contacts.append(contact)
            
            print(f"   ✅ Extracted {len([c for c in all_contacts if c['source'] == excel_file.name])} contacts")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Process PDF files
    pdf_files = list(downloads_dir.glob('*.pdf'))
    for pdf_file in pdf_files:
        print(f"\n📄 Processing: {pdf_file.name}")
        try:
            with open(pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                text = ''
                for page in pdf_reader.pages[:50]:  # Limit to first 50 pages
                    text += page.extract_text() + '\n'
                
                # Extract contacts
                emails = re.findall(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
                phones = re.findall(r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})', text)
                names = re.findall(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
                
                # Simple extraction - look for patterns
                lines = text.split('\n')
                current_company = ''
                
                for line in lines:
                    if len(line.strip()) > 5 and (line.isupper() or line.istitle()):
                        if len(line.split()) <= 5:
                            current_company = line.strip()
                    
                    if 'sblo' in line.lower() or 'small business' in line.lower():
                        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line)
                        phone_match = re.search(r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})', line)
                        name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', line)
                        
                        all_contacts.append({
                            'company': current_company,
                            'sblo_name': name_match.group(1) if name_match else '',
                            'title': 'SBLO',
                            'email': email_match.group(1) if email_match else '',
                            'phone': phone_match.group(1) if phone_match else '',
                            'address': '',
                            'naics': '',
                            'source': pdf_file.name
                        })
                
                print(f"   ✅ Extracted {len([c for c in all_contacts if c['source'] == pdf_file.name])} contacts")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return all_contacts

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   SBLO Contact Downloader - All Sources in Minutes   ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    start_time = time.time()
    all_contacts = []
    
    # Download files
    print("\n🚀 Starting downloads...\n")
    download_sba_directory()
    download_dod_directory()
    
    # Scrape web pages
    dhs_contacts = scrape_dhs_contacts()
    all_contacts.extend(dhs_contacts)
    
    # Process downloaded files
    file_contacts = process_all_files()
    all_contacts.extend(file_contacts)
    
    # Remove duplicates
    seen = set()
    unique_contacts = []
    for contact in all_contacts:
        key = (contact.get('company', '').lower(), contact.get('email', '').lower())
        if key not in seen and (contact.get('company') or contact.get('email')):
            seen.add(key)
            unique_contacts.append(contact)
    
    # Save results
    output_file = Path('sblo-list-compiled.csv')
    if unique_contacts:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = unique_contacts[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_contacts)
        
        print("\n" + "="*60)
        print("✨ COMPILATION COMPLETE!")
        print("="*60)
        print(f"\n📊 Total unique contacts: {len(unique_contacts)}")
        print(f"⏱️  Time taken: {time.time() - start_time:.1f} seconds")
        print(f"💾 Saved to: {output_file}")
        
        # Show breakdown
        sources = {}
        for contact in unique_contacts:
            source = contact.get('source', 'Unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print("\n📋 Breakdown by source:")
        for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True):
            print(f"   {source}: {count} contacts")
        
        print("\n📋 Sample contacts:")
        for i, contact in enumerate(unique_contacts[:10]):
            company = contact.get('company', 'N/A')[:40]
            email = contact.get('email', 'N/A')[:30]
            print(f"   {i+1:2d}. {company:40s} - {email}")
        
        # Update main CSV
        try:
            main_csv = Path('sblo-list.csv')
            if main_csv.exists():
                with open(main_csv, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    existing = list(reader)
                
                existing_companies = {row.get('Agency', '') + row.get('Company Name', '') for row in existing}
                
                for contact in unique_contacts:
                    company_key = contact.get('company', '')
                    if company_key and company_key not in existing_companies:
                        existing.append({
                            'Agency': 'Prime Contractor',
                            'Office/Program': 'Small Business',
                            'Contact Name': contact.get('sblo_name', ''),
                            'Title': contact.get('title', 'SBLO'),
                            'Email': contact.get('email', ''),
                            'Phone': contact.get('phone', ''),
                            'Website': '',
                            'Address': contact.get('address', ''),
                            'City': '',
                            'State': '',
                            'Notes': f"From {contact.get('source', '')}",
                            'Unobligated Balance (Dec 2025)': '',
                            'Key NAICS': contact.get('naics', '')
                        })
                
                with open(main_csv, 'w', newline='', encoding='utf-8') as f:
                    if existing:
                        fieldnames = existing[0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(existing)
                
                print(f"\n✅ Updated sblo-list.csv with {len(unique_contacts)} new contacts")
        except Exception as e:
            print(f"⚠️  Could not update main CSV: {e}")
    else:
        print("\n⚠️  No contacts found. Check downloads and try manual processing.")
    
    print("\n" + "="*60)
    print("🎉 Done! Review sblo-list-compiled.csv")
    print("="*60)

if __name__ == '__main__':
    main()




