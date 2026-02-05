#!/usr/bin/env python3
"""
Clean and improve DoD CSP contacts
Fix company names and SBLO assignments
"""

import csv
from pathlib import Path

def clean_dod_contacts():
    """Clean the extracted DoD contacts"""
    
    input_file = Path('dod-csp-contacts.csv')
    
    # Known company mappings from the extracted data
    company_mappings = {
        'Systems, Inc BAE': 'BAE Systems',
        'Amanda Bennett': 'BAE Systems',
        'Virginia Foley': 'General Dynamics Information Technology',
        'Officer GEA': 'GE Power',
        'Maranda Sterling': 'GE Power',
        'SBLO Honeywell Aerospace Technologies': 'Honeywell Aerospace Technologies',
        'Small Business': 'L3Harris',
        'Susan Turley': 'L3Harris',
        'Procurement/SBLO Pratt & Whitney': 'Pratt & Whitney',
        'Ariel Hooker': 'Pratt & Whitney',
        'Senior Manager Lockheed  Martin Corporat': 'Lockheed Martin Corporation',
        'Senior Manager Lockheed  Martin Corporation': 'Lockheed Martin Corporation',
        'Pasquele DeSanto': 'Lockheed Martin Corporation',
        'SBLO Raytheon': 'Raytheon',
        'Manager/ SBLO Sikorksy': 'Sikorsky',
        'Lavenia Kitchen': 'Lockheed Martin Corporation'
    }
    
    # SBLO name mappings
    sblo_mappings = {
        'Systems, Inc BAE': 'Marianne Tenore',
        'Amanda Bennett': 'Amanda Bennett',
        'Virginia Foley': 'Virginia Foley',
        'Officer GEA': 'Bethani Clever',
        'Maranda Sterling': 'Maranda Sterling',
        'SBLO Honeywell Aerospace Technologies': 'Melissa Audain',
        'Small Business': 'Thosie Varga',
        'Susan Turley': 'Susan Turley',
        'Procurement/SBLO Pratt & Whitney': 'Francisco Vasquez',
        'Ariel Hooker': 'Ariel Hooker',
        'Senior Manager Lockheed  Martin Corporat': 'Sefnee A. Manzanares',
        'Pasquele DeSanto': 'Pasquale M. DeSanto',
        'SBLO Raytheon': 'Crystal L. King',
        'Manager/ SBLO Sikorksy': 'Martha Crawford',
        'Lavenia Kitchen': 'Lavenia M. Kitchen'
    }
    
    contacts = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = row['company'].strip()
            
            # Map to correct company name
            if company in company_mappings:
                company = company_mappings[company]
            
            # Get SBLO name from mappings
            original_company = row['company'].strip()
            sblo_name = sblo_mappings.get(original_company, row['sblo_name'].strip())
            
            # If still no SBLO name, try to extract from email
            if not sblo_name:
                email = row['email'].strip()
                if email:
                    # Extract name from email (first.last@company.com -> First Last)
                    email_part = email.split('@')[0]
                    if '.' in email_part:
                        parts = email_part.split('.')
                        sblo_name = ' '.join([p.capitalize() for p in parts[:2]])
            
            contacts.append({
                'company': company,
                'sblo_name': sblo_name,
                'title': 'SBLO',
                'email': row['email'].strip(),
                'phone': row['phone'].strip(),
                'website': row['website'].strip(),
                'source': row['source']
            })
    
    # Group by company to handle duplicates
    company_contacts = {}
    for contact in contacts:
        company = contact['company']
        email = contact['email'].lower()
        
        if company not in company_contacts:
            company_contacts[company] = []
        
        # Check if email already exists for this company
        existing_emails = [c['email'].lower() for c in company_contacts[company]]
        if email not in existing_emails:
            company_contacts[company].append(contact)
    
    # Flatten back to list
    cleaned_contacts = []
    for company, contact_list in company_contacts.items():
        cleaned_contacts.extend(contact_list)
    
    # Save cleaned version
    output_file = Path('dod-csp-contacts-cleaned.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_contacts)
    
    print(f"✅ Cleaned contacts saved to: {output_file}")
    print(f"📊 Total contacts: {len(cleaned_contacts)}")
    print(f"📊 Unique companies: {len(company_contacts)}")
    
    print("\n📋 Cleaned contacts:")
    for i, contact in enumerate(cleaned_contacts, 1):
        print(f"   {i:2d}. {contact['company'][:45]:45s} - {contact['sblo_name'][:25]:25s} - {contact['email']}")
    
    return cleaned_contacts

if __name__ == '__main__':
    clean_dod_contacts()

