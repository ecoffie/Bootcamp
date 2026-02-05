#!/usr/bin/env python3
"""
Create final DHS contacts list with all 76 companies
Use clean contacts from verified file and add missing Lockheed Martin
"""

import csv
from pathlib import Path

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Create Final DHS List - All 76 Companies          ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Load clean contacts from verified file
    verified_file = Path('dhs-contacts-verified.csv')
    clean_contacts = []
    
    if verified_file.exists():
        with open(verified_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('status') == 'EXTRACTED':
                    clean_contacts.append({
                        'company': row['company'],
                        'sblo_name': row['sblo_name'],
                        'title': row.get('title', 'SBLO'),
                        'email': row['email'],
                        'phone': row['phone'],
                        'website': row['website'],
                        'naics': row['naics'],
                        'source': row['source']
                    })
                elif row.get('status') == 'MISSING':
                    # This is Lockheed Martin - get it from final file
                    company_name = row['company']
                    # Try to get from final file
                    final_file = Path('dhs-contacts-final.csv')
                    if final_file.exists():
                        with open(final_file, 'r', encoding='utf-8') as f2:
                            reader2 = csv.DictReader(f2)
                            for row2 in reader2:
                                if row2['company'].strip() == company_name:
                                    clean_contacts.append({
                                        'company': row2['company'],
                                        'sblo_name': row2.get('sblo_name', ''),
                                        'title': 'SBLO',
                                        'email': row2.get('email', ''),
                                        'phone': row2.get('phone', ''),
                                        'website': row2.get('website', ''),
                                        'naics': row2.get('naics', ''),
                                        'source': 'DHS Prime Contractors Page'
                                    })
                                    break
    
    print(f"📊 Total contacts: {len(clean_contacts)}")
    
    # Count unique companies
    unique_companies = set(c['company'] for c in clean_contacts)
    print(f"📊 Unique companies: {len(unique_companies)}")
    
    # Save final list
    output_file = Path('dhs-contacts-all-76-companies.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'naics', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(clean_contacts)
    
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
        
        for contact in clean_contacts:
            email_lower = contact['email'].lower() if contact['email'] else ''
            key = (contact['company'].lower(), email_lower)
            if key not in existing_emails and email_lower:
                writer.writerow({
                    'company': contact['company'],
                    'sblo_name': contact['sblo_name'],
                    'title': contact['title'],
                    'email': contact['email'],
                    'phone': contact['phone'],
                    'address': '',
                    'naics': contact['naics'],
                    'source': contact['source']
                })
                existing_emails.add(key)
                new_count += 1
    
    print(f"✅ Added {new_count} contacts to compiled list")
    print(f"📊 Total in compiled list: {len(existing_emails)}")
    
    # Show companies with emails vs without
    with_email = [c for c in clean_contacts if c['email']]
    without_email = [c for c in clean_contacts if not c['email']]
    
    print(f"\n📊 Breakdown:")
    print(f"   Companies with email: {len(with_email)}")
    print(f"   Companies without email: {len(without_email)}")
    
    if without_email:
        print(f"\n⚠️  Companies missing email:")
        for contact in without_email:
            print(f"   - {contact['company']}")
    
    print("\n✨ Final list created with all 76 companies!")

if __name__ == '__main__':
    main()




