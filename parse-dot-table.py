#!/usr/bin/env python3
"""
Parse DOT directory from Firecrawl markdown output
Extract contacts from table format
"""

import csv
import re
from pathlib import Path

def parse_dot_markdown_table():
    """Parse the markdown table from Firecrawl output"""
    
    input_file = Path('dot-directory-firecrawl-output.txt')
    
    if not input_file.exists():
        print("❌ File not found: dot-directory-firecrawl-output.txt")
        return []
    
    print("📄 Reading Firecrawl output...")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"   File size: {len(content)} characters")
    
    # Find the table section
    # Table starts with: | Vendor Name | Vendor Physical Address | ...
    table_start = content.find('| Vendor Name |')
    if table_start == -1:
        print("❌ Could not find table in content")
        return []
    
    # Extract table content
    table_content = content[table_start:]
    
    # Parse markdown table rows
    contacts = []
    lines = table_content.split('\n')
    
    # Skip header row and separator row
    for line in lines[2:]:  # Skip header and separator
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
        
        # Parse table row: | Company | Address | NAICS | Services | Name Phone |
        parts = [p.strip() for p in line.split('|')]
        
        if len(parts) < 6:
            continue
        
        company = parts[1] if len(parts) > 1 else ''
        address = parts[2] if len(parts) > 2 else ''
        naics = parts[3] if len(parts) > 3 else ''
        services = parts[4] if len(parts) > 4 else ''
        name_phone = parts[5] if len(parts) > 5 else ''
        
        # Skip if it's the header row
        if 'Vendor Name' in company or '---' in company:
            continue
        
        # Parse name and phone from the last column
        # Format: "Name (phone)" or "Name<br>(phone)"
        name = ''
        phone = ''
        
        # Remove HTML tags
        name_phone_clean = re.sub(r'<br>', ' ', name_phone)
        name_phone_clean = re.sub(r'<[^>]+>', '', name_phone_clean)
        
        # Extract phone number
        phone_match = re.search(r'(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', name_phone_clean)
        if phone_match:
            phone = phone_match.group(1).strip()
            # Extract name (everything before phone)
            name = name_phone_clean[:phone_match.start()].strip()
        else:
            # No phone, use whole thing as name
            name = name_phone_clean.strip()
        
        # Clean up company name (remove HTML tags)
        company_clean = re.sub(r'<[^>]+>', '', company).strip()
        
        if company_clean:
            contacts.append({
                'company': company_clean,
                'sblo_name': name,
                'email': '',  # DOT directory doesn't have emails
                'phone': phone,
                'website': '',
                'naics': naics,
                'address': address,
                'source': 'DOT Subcontracting Directory FY2025'
            })
    
    print(f"✅ Parsed {len(contacts)} contacts from table")
    return contacts

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Parse DOT Directory Table                         ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    contacts = parse_dot_markdown_table()
    
    if not contacts:
        print("⚠️  No contacts parsed")
        return
    
    # Remove duplicates
    seen = set()
    unique_contacts = []
    for contact in contacts:
        key = (contact['company'].lower().strip(), contact['phone'].strip())
        if key not in seen:
            seen.add(key)
            unique_contacts.append(contact)
    
    print(f"📊 Unique contacts: {len(unique_contacts)}")
    
    # Save results
    output_file = Path('dot-contacts.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'naics', 'address', 'source']
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
                'address': contact['address'],
                'source': contact['source']
            })
    
    print(f"💾 Saved to: {output_file}")
    
    # Show sample
    print("\n📋 Sample contacts:")
    for i, contact in enumerate(unique_contacts[:15], 1):
        phone = contact['phone'][:20] if contact['phone'] else 'N/A'
        print(f"   {i:2d}. {contact['company'][:40]:40s} - {contact['sblo_name'][:25]:25s} - {phone}")
    
    # Update compiled list
    compiled_file = Path('sblo-list-compiled.csv')
    existing_companies = set()
    
    if compiled_file.exists():
        with open(compiled_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get('company', '').lower().strip()
                phone = row.get('phone', '').strip()
                if company:
                    existing_companies.add((company, phone))
    
    new_count = 0
    with open(compiled_file, 'a', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'address', 'naics', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        for contact in unique_contacts:
            key = (contact['company'].lower().strip(), contact['phone'].strip())
            if key not in existing_companies:
                writer.writerow({
                    'company': contact['company'],
                    'sblo_name': contact['sblo_name'],
                    'title': 'SBLO',
                    'email': contact['email'],
                    'phone': contact['phone'],
                    'address': contact['address'],
                    'naics': contact['naics'],
                    'source': contact['source']
                })
                existing_companies.add(key)
                new_count += 1
    
    print(f"\n✅ Added {new_count} new contacts to compiled list")
    print(f"📊 Total in compiled list: {len(existing_companies)}")
    
    print("\n" + "="*60)
    print("✨ Processing Complete!")
    print("="*60)
    print(f"\n📊 Summary:")
    print(f"   Total DOT contacts: {len(unique_contacts)}")
    print(f"   With phone numbers: {len([c for c in unique_contacts if c['phone']])}")
    print(f"   With SBLO names: {len([c for c in unique_contacts if c['sblo_name']])}")
    print(f"   Note: DOT directory doesn't include email addresses")

if __name__ == '__main__':
    main()




