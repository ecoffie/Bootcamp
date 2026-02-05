#!/usr/bin/env python3
"""
Merge new SBLO contacts into the master database.
Only updates companies that are missing email contacts.
"""

import csv

def normalize_company_name(name):
    """Normalize company name for matching."""
    if not name:
        return ""
    name = name.strip().upper()
    # Remove common suffixes
    for suffix in [' INC.', ' INC', ' LLC', ' LP', ' LLP', ' CORP.', ' CORP', ' CORPORATION', ' COMPANY', ' CO.', ' CO', ',']:
        name = name.replace(suffix, '')
    name = ' '.join(name.split())
    return name

def main():
    print("Reading new contacts...")
    new_contacts = {}
    with open('new-sblo-contacts.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = row.get('company', '').strip()
            norm_name = normalize_company_name(company)
            new_contacts[norm_name] = {
                'sblo_name': row.get('sblo_name', ''),
                'email': row.get('email', ''),
                'phone': row.get('phone', ''),
                'source': row.get('source', '')
            }
    print(f"  Loaded {len(new_contacts)} new contacts")

    print("\nReading master database...")
    rows = []
    with open('FEDERAL-CONTRACTOR-MASTER-DATABASE.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(dict(row))
    print(f"  Loaded {len(rows)} companies")

    # Count before
    before_emails = sum(1 for r in rows if r.get('email'))
    print(f"  Companies with email before: {before_emails}")

    # Merge contacts
    updated = 0
    for row in rows:
        company = row.get('company', '')
        norm_name = normalize_company_name(company)

        # Only update if missing email
        if not row.get('email') and norm_name in new_contacts:
            contact = new_contacts[norm_name]
            if contact['email']:
                row['email'] = contact['email']
                if contact['sblo_name'] and not row.get('sblo_name'):
                    row['sblo_name'] = contact['sblo_name']
                if contact['phone'] and not row.get('phone'):
                    row['phone'] = contact['phone']
                updated += 1
                print(f"  Updated: {company} -> {contact['email']}")

    # Count after
    after_emails = sum(1 for r in rows if r.get('email'))
    print(f"\nUpdated {updated} companies")
    print(f"Companies with email after: {after_emails}")

    # Write updated database
    print("\nWriting updated database...")
    with open('FEDERAL-CONTRACTOR-MASTER-DATABASE.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Done!")

if __name__ == '__main__':
    main()
