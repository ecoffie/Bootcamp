#!/usr/bin/env python3
"""
Create comprehensive final SBLO list with all companies that have email OR phone
Deduplicate, clean, and prepare for PDF export
"""

import csv
from collections import defaultdict

compiled_file = '/Users/ericcoffie/Bootcamp/sblo-list-compiled.csv'
output_csv = '/Users/ericcoffie/Bootcamp/FINAL-SBLO-CONTACT-LIST.csv'

print("=" * 80)
print("CREATING FINAL SBLO CONTACT LIST")
print("=" * 80)

# Read all contacts
contacts = []
with open(compiled_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = row.get('company', '').strip()
        email = row.get('email', '').strip()
        phone = row.get('phone', '').strip()

        # Only include if has email OR phone
        if (email or phone) and company:
            contacts.append({
                'company': company,
                'sblo_name': row.get('sblo_name', '').strip(),
                'title': row.get('title', '').strip(),
                'email': email,
                'phone': phone,
                'address': row.get('address', '').strip(),
                'naics': row.get('naics', '').strip(),
                'source': row.get('source', '').strip()
            })

print(f"\n📊 Extracted {len(contacts)} contacts with email or phone")

# Group by company to find best contact for each
company_contacts = defaultdict(list)
for contact in contacts:
    company_key = contact['company'].upper()
    company_contacts[company_key].append(contact)

print(f"📊 Found {len(company_contacts)} unique companies")

# Select best contact for each company
# Priority: 1) Has both email AND phone, 2) Has email, 3) Has phone only
final_contacts = []
for company_key, contact_list in company_contacts.items():
    # Sort by priority
    def priority_score(c):
        score = 0
        if c['email'] and c['phone']:
            score += 100
        elif c['email']:
            score += 50
        elif c['phone']:
            score += 25
        if c['sblo_name']:
            score += 10
        return score

    contact_list.sort(key=priority_score, reverse=True)
    best_contact = contact_list[0]

    # If multiple contacts have email, collect all unique emails
    all_emails = set()
    all_phones = set()
    all_sblo_names = set()

    for c in contact_list:
        if c['email']:
            all_emails.add(c['email'])
        if c['phone']:
            all_phones.add(c['phone'])
        if c['sblo_name']:
            all_sblo_names.add(c['sblo_name'])

    # Combine multiple contacts into one entry
    final_contact = {
        'company': best_contact['company'],
        'sblo_name': '; '.join(all_sblo_names) if all_sblo_names else '',
        'email': '; '.join(sorted(all_emails)) if all_emails else '',
        'phone': '; '.join(sorted(all_phones)) if all_phones else '',
        'naics': best_contact['naics'],
        'source': best_contact['source'],
        'contact_quality': 'Email + Phone' if all_emails and all_phones else 'Email Only' if all_emails else 'Phone Only'
    }

    final_contacts.append(final_contact)

# Sort alphabetically by company name
final_contacts.sort(key=lambda x: x['company'].upper())

# Write to CSV
with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
    fieldnames = ['company', 'sblo_name', 'email', 'phone', 'contact_quality', 'naics', 'source']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(final_contacts)

# Statistics
email_count = sum(1 for c in final_contacts if c['email'])
phone_count = sum(1 for c in final_contacts if c['phone'])
both_count = sum(1 for c in final_contacts if c['email'] and c['phone'])
email_only = email_count - both_count
phone_only = phone_count - both_count

print(f"\n✅ FINAL LIST CREATED:")
print(f"   • Total companies: {len(final_contacts)}")
print(f"   • With email: {email_count} ({email_count/len(final_contacts)*100:.1f}%)")
print(f"   • With phone: {phone_count} ({phone_count/len(final_contacts)*100:.1f}%)")
print(f"   • With both: {both_count} ({both_count/len(final_contacts)*100:.1f}%)")
print(f"   • Email only: {email_only}")
print(f"   • Phone only: {phone_only}")

print(f"\n📄 Saved to: {output_csv}")
print("=" * 80)
