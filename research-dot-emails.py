#!/usr/bin/env python3
"""
Research email addresses for DOT contacts
Uses company websites and common email patterns to find SBLO emails
"""

import csv
import re
import requests
from pathlib import Path
from urllib.parse import urlparse
import time

def find_company_website(company_name):
    """Try to find company website from name"""
    # Common patterns
    company_clean = company_name.lower()
    company_clean = re.sub(r'\s+(inc|llc|corp|corporation|lp|incorporated)$', '', company_clean)
    company_clean = re.sub(r'[^a-z0-9]', '', company_clean)
    
    # Try common domain patterns
    possible_domains = [
        f"www.{company_clean}.com",
        f"{company_clean}.com",
        f"www.{company_clean.replace(' ', '')}.com",
    ]
    
    return None  # Will need manual research or web search

def generate_email_patterns(company_name, sblo_name):
    """Generate possible email patterns"""
    patterns = []
    
    # Clean company name for domain
    company_clean = company_name.lower()
    company_clean = re.sub(r'\s+(inc|llc|corp|corporation|lp|incorporated)$', '', company_clean)
    company_clean = re.sub(r'[^a-z0-9]', '', company_clean)
    
    # Common SBLO email patterns
    if sblo_name:
        name_parts = sblo_name.lower().split()
        if len(name_parts) >= 2:
            first = name_parts[0]
            last = name_parts[-1]
            
            patterns.extend([
                f"{first}.{last}@{company_clean}.com",
                f"{first}{last}@{company_clean}.com",
                f"{first}_{last}@{company_clean}.com",
                f"{first[0]}{last}@{company_clean}.com",
            ])
    
    # Generic SBLO patterns
    patterns.extend([
        f"smallbusiness@{company_clean}.com",
        f"sblo@{company_clean}.com",
        f"small.business@{company_clean}.com",
        f"supplier.diversity@{company_clean}.com",
        f"osdbu@{company_clean}.com",
    ])
    
    return patterns

def research_dot_emails():
    """Research email addresses for DOT contacts"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Research Email Addresses for DOT Contacts         ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    input_file = Path('dot-contacts.csv')
    
    if not input_file.exists():
        print(f"❌ File not found: {input_file}")
        return
    
    contacts = []
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        contacts = list(reader)
    
    print(f"📊 Processing {len(contacts)} DOT contacts...")
    print("🔍 Researching email addresses...\n")
    
    # For now, we'll create a template with email patterns
    # Actual email verification would require API access or manual research
    enhanced_contacts = []
    
    for i, contact in enumerate(contacts, 1):
        company = contact['company']
        sblo_name = contact['sblo_name']
        
        # Generate possible email patterns
        email_patterns = generate_email_patterns(company, sblo_name)
        
        # For now, mark as needs research
        contact['email'] = '[NEEDS RESEARCH]'
        contact['email_patterns'] = '; '.join(email_patterns[:5])  # Top 5 patterns
        contact['research_status'] = 'PENDING'
        
        enhanced_contacts.append(contact)
        
        if i % 20 == 0:
            print(f"   Processed {i}/{len(contacts)}...")
    
    # Save enhanced list
    output_file = Path('dot-contacts-with-email-research.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'naics', 'address', 'source', 'email_patterns', 'research_status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enhanced_contacts)
    
    print(f"\n💾 Saved to: {output_file}")
    print(f"📊 Enhanced {len(enhanced_contacts)} contacts with email research patterns")
    
    print("\n📋 Next steps for email research:")
    print("   1. Visit each company's website")
    print("   2. Look for 'Small Business' or 'Supplier Diversity' pages")
    print("   3. Check contact pages for SBLO email")
    print("   4. Use email patterns generated above")
    print("   5. Update the CSV with verified emails")
    
    return enhanced_contacts

if __name__ == '__main__':
    research_dot_emails()




