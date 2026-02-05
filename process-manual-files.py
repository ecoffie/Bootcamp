#!/usr/bin/env python3
"""
Process manually downloaded SBLO files
Place downloaded Excel/PDF files in sblo-data-downloads/ folder
"""

import pandas as pd
import PyPDF2
import csv
from pathlib import Path
import re

def process_excel_files():
    """Process all Excel files in the downloads folder"""
    downloads_dir = Path('sblo-data-downloads')
    contacts = []
    
    excel_files = list(downloads_dir.glob('*.xlsx')) + list(downloads_dir.glob('*.xls'))
    
    for excel_file in excel_files:
        print(f"\n📊 Processing Excel: {excel_file.name}")
        try:
            # Try reading with different engines
            try:
                df = pd.read_excel(excel_file, engine='openpyxl')
            except:
                df = pd.read_excel(excel_file, engine='xlrd')
            
            print(f"   Columns: {list(df.columns)}")
            print(f"   Rows: {len(df)}")
            
            # Find relevant columns
            name_cols = [col for col in df.columns if any(x in str(col).lower() for x in ['name', 'company', 'contractor', 'prime', 'firm'])]
            email_cols = [col for col in df.columns if 'email' in str(col).lower()]
            phone_cols = [col for col in df.columns if any(x in str(col).lower() for x in ['phone', 'tel', 'telephone'])]
            sblo_cols = [col for col in df.columns if 'sblo' in str(col).lower() or 'small business' in str(col).lower() or 'liaison' in str(col).lower()]
            address_cols = [col for col in df.columns if any(x in str(col).lower() for x in ['address', 'location', 'city', 'state'])]
            naics_cols = [col for col in df.columns if 'naics' in str(col).lower()]
            
            print(f"   Found: {len(name_cols)} name cols, {len(email_cols)} email cols, {len(phone_cols)} phone cols")
            
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
                
                # Extract company name
                if name_cols:
                    for col in name_cols:
                        val = row[col]
                        if pd.notna(val) and str(val).strip():
                            contact['company'] = str(val).strip()
                            break
                
                # Extract SBLO name
                if sblo_cols:
                    for col in sblo_cols:
                        val = row[col]
                        if pd.notna(val) and str(val).strip():
                            contact['sblo_name'] = str(val).strip()
                            break
                
                # Extract email
                if email_cols:
                    for col in email_cols:
                        val = row[col]
                        if pd.notna(val) and str(val).strip():
                            email = str(val).strip()
                            if '@' in email:
                                contact['email'] = email
                                break
                
                # Extract phone
                if phone_cols:
                    for col in phone_cols:
                        val = row[col]
                        if pd.notna(val) and str(val).strip():
                            contact['phone'] = str(val).strip()
                            break
                
                # Extract address
                if address_cols:
                    address_parts = []
                    for col in address_cols[:3]:  # Limit to first 3 address columns
                        val = row[col]
                        if pd.notna(val) and str(val).strip():
                            address_parts.append(str(val).strip())
                    contact['address'] = ', '.join(address_parts)
                
                # Extract NAICS
                if naics_cols:
                    for col in naics_cols:
                        val = row[col]
                        if pd.notna(val) and str(val).strip():
                            contact['naics'] = str(val).strip()
                            break
                
                if contact['company'] or contact['sblo_name'] or contact['email']:
                    contacts.append(contact)
            
            print(f"   ✅ Extracted {len([c for c in contacts if c['source'] == excel_file.name])} contacts")
            
        except Exception as e:
            print(f"   ❌ Error processing {excel_file.name}: {e}")
    
    return contacts

def process_pdf_files():
    """Process all PDF files in the downloads folder"""
    downloads_dir = Path('sblo-data-downloads')
    contacts = []
    
    pdf_files = list(downloads_dir.glob('*.pdf'))
    
    for pdf_file in pdf_files:
        print(f"\n📄 Processing PDF: {pdf_file.name}")
        try:
            with open(pdf_file, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                print(f"   Pages: {len(pdf_reader.pages)}")
                
                full_text = ''
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    full_text += text + '\n'
                
                # Look for patterns
                lines = full_text.split('\n')
                current_company = ''
                
                # Pattern 1: Company name followed by SBLO info
                for i, line in enumerate(lines):
                    line_clean = line.strip()
                    
                    # Detect company names (usually all caps or title case, 3+ words)
                    if len(line_clean) > 5 and (line_clean.isupper() or (line_clean.istitle() and len(line_clean.split()) <= 5)):
                        # Check if it's likely a company name (not a header)
                        if not any(word in line_clean.lower() for word in ['page', 'table', 'directory', 'list']):
                            current_company = line_clean
                    
                    # Look for SBLO patterns
                    if 'sblo' in line_clean.lower() or 'small business liaison' in line_clean.lower():
                        # Extract name (usually before SBLO)
                        name_match = re.search(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', line_clean)
                        # Extract phone
                        phone_match = re.search(r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})', line_clean)
                        # Extract email
                        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', line_clean)
                        
                        contact = {
                            'company': current_company,
                            'sblo_name': name_match.group(1) if name_match else '',
                            'title': 'SBLO',
                            'email': email_match.group(1) if email_match else '',
                            'phone': phone_match.group(1) if phone_match else '',
                            'address': '',
                            'naics': '',
                            'source': pdf_file.name
                        }
                        
                        if contact['company'] or contact['sblo_name'] or contact['email']:
                            contacts.append(contact)
                
                print(f"   ✅ Extracted {len([c for c in contacts if c['source'] == pdf_file.name])} contacts")
                
        except Exception as e:
            print(f"   ❌ Error processing {pdf_file.name}: {e}")
    
    return contacts

def main():
    print("""
    ╔══════════════════════════════════════════════════╗
    ║   Process Manually Downloaded SBLO Files       ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    downloads_dir = Path('sblo-data-downloads')
    downloads_dir.mkdir(exist_ok=True)
    
    # Check for files
    excel_files = list(downloads_dir.glob('*.xlsx')) + list(downloads_dir.glob('*.xls'))
    pdf_files = list(downloads_dir.glob('*.pdf'))
    
    print(f"\n📁 Found {len(excel_files)} Excel file(s) and {len(pdf_files)} PDF file(s)")
    
    if not excel_files and not pdf_files:
        print("\n⚠️  No files found in sblo-data-downloads/")
        print("\nTo use this script:")
        print("1. Download files from:")
        print("   - SBA Prime Directory: https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans")
        print("   - DoD CSP Directory: https://business.defense.gov/Portals/57/Documents/Dod%20CSP%20Prime%20Contractor%20Directory_May%202025.pdf")
        print("   - DOT Directory: https://www.transportation.gov/osdbu/procurement-assistance/dot-subcontracting-directory")
        print("2. Save them to: sblo-data-downloads/")
        print("3. Run this script again")
        return
    
    all_contacts = []
    
    # Process Excel files
    if excel_files:
        excel_contacts = process_excel_files()
        all_contacts.extend(excel_contacts)
    
    # Process PDF files
    if pdf_files:
        pdf_contacts = process_pdf_files()
        all_contacts.extend(pdf_contacts)
    
    # Remove duplicates
    seen = set()
    unique_contacts = []
    for contact in all_contacts:
        key = (contact.get('company', ''), contact.get('email', ''))
        if key not in seen and (contact.get('company') or contact.get('email')):
            seen.add(key)
            unique_contacts.append(contact)
    
    print(f"\n✅ Total unique contacts: {len(unique_contacts)}")
    
    # Save compiled list
    output_file = Path('sblo-list-compiled.csv')
    if unique_contacts:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = unique_contacts[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(unique_contacts)
        print(f"💾 Saved to: {output_file}")
        
        # Show sample
        print("\n📋 Sample contacts:")
        for i, contact in enumerate(unique_contacts[:5]):
            print(f"   {i+1}. {contact.get('company', 'N/A')} - {contact.get('email', 'N/A')}")
    else:
        print("⚠️  No contacts extracted. Check file formats.")
    
    print("\n✨ Processing complete!")

if __name__ == '__main__':
    main()




