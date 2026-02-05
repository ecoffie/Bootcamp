#!/usr/bin/env python3
"""
Process DoD CSP Prime Contractor Directory PDF
Extract SBLO contacts from the May 2025 directory
"""

import PyPDF2
import csv
import re
from pathlib import Path
from collections import defaultdict

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF"""
    print(f"📄 Reading PDF: {pdf_path}")
    
    try:
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            total_pages = len(pdf_reader.pages)
            print(f"   Pages: {total_pages}")
            
            full_text = ''
            for page_num, page in enumerate(pdf_reader.pages):
                if page_num % 10 == 0:
                    print(f"   Processing page {page_num + 1}/{total_pages}...", end='\r')
                full_text += page.extract_text() + '\n'
            
            print(f"   ✅ Extracted text from {total_pages} pages")
            return full_text
            
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

def parse_dod_contacts(text):
    """Parse SBLO contacts from PDF text"""
    print("\n🔍 Parsing contacts from PDF text...")
    
    contacts = []
    lines = text.split('\n')
    
    # Patterns to look for
    current_company = ''
    current_sblo = ''
    current_email = ''
    current_phone = ''
    current_website = ''
    
    # Common patterns in DoD directories:
    # Company Name (often in caps or bold)
    # Small Business Liaison: Name
    # Email: email@company.com
    # Phone: (xxx) xxx-xxxx
    # Website: www.company.com
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        
        # Skip empty lines
        if not line_clean:
            continue
        
        # Detect company names (usually longer, title case or all caps)
        # Company names are often followed by SBLO info
        if len(line_clean) > 5 and len(line_clean) < 100:
            # Check if it looks like a company name
            # Not a phone, email, or common words
            if not re.match(r'[\d\(\)\-\.\s]+$', line_clean):  # Not just numbers/punctuation
                if not '@' in line_clean:  # Not an email
                    if not any(word in line_clean.lower() for word in ['page', 'directory', 'table', 'of contents']):
                        # Could be a company name
                        # Save previous contact if we have one
                        if current_company and current_email:
                            contacts.append({
                                'company': current_company,
                                'sblo_name': current_sblo,
                                'email': current_email,
                                'phone': current_phone,
                                'website': current_website,
                                'source': 'DoD CSP Prime Directory May 2025'
                            })
                        
                        # Start new company
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
            r'(\d{3})\.(\d{3})\.(\d{4})',
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, line_clean)
            if match:
                if len(match.groups()) == 3:
                    current_phone = f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
                else:
                    current_phone = match.group(0)
                break
        
        # Extract website
        website_match = re.search(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', line_clean)
        if website_match:
            current_website = website_match.group(1).strip()
    
    # Don't forget the last contact
    if current_company and current_email:
        contacts.append({
            'company': current_company,
            'sblo_name': current_sblo,
            'email': current_email,
            'phone': current_phone,
            'website': current_website,
            'source': 'DoD CSP Prime Directory May 2025'
        })
    
    print(f"✅ Found {len(contacts)} contacts")
    return contacts

def improved_parse_dod_contacts(text):
    """Improved parsing using section detection"""
    print("\n🔍 Improved parsing with section detection...")
    
    contacts = []
    lines = text.split('\n')
    
    # Look for patterns that indicate a new company entry
    # Companies are often separated by blank lines or headers
    
    current_entry = {}
    in_company_section = False
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        
        # Skip empty lines (but they might separate entries)
        if not line_clean:
            if current_entry.get('company') and current_entry.get('email'):
                contacts.append(current_entry.copy())
                current_entry = {}
            continue
        
        # Look for company name indicators
        # Usually longer lines, title case, not emails/phones
        if len(line_clean) > 10 and len(line_clean) < 80:
            # Check if it's likely a company name
            has_numbers = bool(re.search(r'\d', line_clean))
            has_email = '@' in line_clean
            has_phone = bool(re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', line_clean))
            
            if not has_numbers and not has_email and not has_phone:
                # Could be company name
                # Save previous entry
                if current_entry.get('company') and current_entry.get('email'):
                    contacts.append(current_entry.copy())
                
                # Start new entry
                current_entry = {
                    'company': line_clean,
                    'sblo_name': '',
                    'email': '',
                    'phone': '',
                    'website': '',
                    'source': 'DoD CSP Prime Directory May 2025'
                }
                in_company_section = True
                continue
        
        # If we're in a company section, look for contact info
        if in_company_section and current_entry.get('company'):
            # SBLO name
            sblo_match = re.search(r'(?:Small Business Liaison|SBLO)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', line_clean, re.IGNORECASE)
            if sblo_match:
                current_entry['sblo_name'] = sblo_match.group(1).strip()
            
            # Email
            email_match = re.search(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b', line_clean)
            if email_match and not current_entry['email']:
                current_entry['email'] = email_match.group(1).strip()
            
            # Phone
            if not current_entry['phone']:
                phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', line_clean)
                if phone_match:
                    current_entry['phone'] = phone_match.group(1).strip()
            
            # Website
            if not current_entry['website']:
                website_match = re.search(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', line_clean)
                if website_match:
                    current_entry['website'] = website_match.group(1).strip()
    
    # Don't forget last entry
    if current_entry.get('company') and current_entry.get('email'):
        contacts.append(current_entry)
    
    print(f"✅ Found {len(contacts)} contacts")
    return contacts

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Process DoD CSP Prime Contractor Directory        ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    pdf_path = Path('./SBLO List /Dod CSP Prime Contractor Directory_May 2025.pdf')
    
    if not pdf_path.exists():
        print(f"❌ PDF not found at: {pdf_path}")
        print("   Looking for alternative paths...")
        # Try to find it
        for root, dirs, files in os.walk('.'):
            for file in files:
                if 'dod' in file.lower() and 'csp' in file.lower() and file.endswith('.pdf'):
                    pdf_path = Path(root) / file
                    print(f"   Found: {pdf_path}")
                    break
    
    # Extract text
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("❌ Could not extract text from PDF")
        return
    
    # Try improved parsing
    contacts = improved_parse_dod_contacts(text)
    
    # Remove duplicates
    seen = set()
    unique_contacts = []
    for contact in contacts:
        key = (contact['company'].lower().strip(), contact['email'].lower().strip() if contact['email'] else '')
        if key not in seen and contact['email']:
            seen.add(key)
            unique_contacts.append(contact)
    
    print(f"\n📊 Unique contacts with email: {len(unique_contacts)}")
    
    # Save results
    output_file = Path('dod-csp-contacts.csv')
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
    import os
    main()




