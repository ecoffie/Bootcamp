#!/usr/bin/env python3
"""
Prepare Tier 2 list with proper contact_quality field
"""

import csv

input_file = '/Users/ericcoffie/Bootcamp/TIER-2-SUPPLIER-CONTACTS.csv'
output_file = '/Users/ericcoffie/Bootcamp/TIER-2-FINAL-CONTACT-LIST.csv'

tier2_contacts = []

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row.get('email', '').strip()
        phone = row.get('phone', '').strip()

        # Determine contact quality
        if email and phone:
            contact_quality = 'Email + Phone'
        elif email:
            contact_quality = 'Email Only'
        elif phone:
            contact_quality = 'Phone Only'
        else:
            continue  # Skip if no contact

        tier2_contacts.append({
            'company': row['company'],
            'sblo_name': row.get('sblo_name', ''),
            'email': email,
            'phone': phone,
            'contact_quality': contact_quality,
            'naics': row.get('naics', ''),
            'source': row.get('source', ''),
            'tier_classification': 'Tier 2 Subcontractor'
        })

# Sort alphabetically
tier2_contacts.sort(key=lambda x: x['company'].upper())

# Write output
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    fieldnames = ['company', 'sblo_name', 'email', 'phone', 'contact_quality', 'naics', 'source', 'tier_classification']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(tier2_contacts)

# Stats
email_count = sum(1 for c in tier2_contacts if c['email'])
phone_count = sum(1 for c in tier2_contacts if c['phone'])
both_count = sum(1 for c in tier2_contacts if c['email'] and c['phone'])

print("=" * 80)
print("TIER 2 FINAL LIST PREPARED")
print("=" * 80)
print(f"\n✅ Total Tier 2 companies: {len(tier2_contacts)}")
print(f"   • With email: {email_count}")
print(f"   • With phone: {phone_count}")
print(f"   • With both: {both_count}")
print(f"\n📄 Saved to: {output_file}")
print("=" * 80)
