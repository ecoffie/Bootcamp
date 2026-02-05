#!/usr/bin/env python3
"""
Fix contact data issues in the master database:
1. Clean up emails with parsing artifacts
2. Clean up SBLO names with concatenated text
3. Fix any other data quality issues
"""

import csv
import re

def clean_email(email):
    """Extract valid email from potentially malformed string."""
    if not email:
        return ''

    # Common fixes
    email = email.replace('comSmall', 'com')
    email = email.replace('comWebsite', 'com')
    email = email.replace('comIn', 'com')

    # Extract just the email part
    match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', email)
    if match:
        return match.group(1)

    return email

def clean_sblo_name(name):
    """Clean SBLO name - remove artifacts and duplicates."""
    if not name:
        return ''

    # Remove common artifacts
    artifacts = [
        'smallbusinesscompliance', 'SmallBusiness', 'Small Business',
        'Website', 'SBLO', 'Contact', 'Manager', 'Director',
        'Burtonsmallbusinesscompliance', 'LoweSBLO', 'RalstonShawn',
        'RiveraIrene', 'AndersonHeidi', 'ThibodeauxSusan', 'Mackellen'
    ]

    for artifact in artifacts:
        if name.endswith(artifact):
            name = name[:-len(artifact)]

    # Remove duplicate names (e.g., "Ashley Burton Ashley Burton")
    words = name.split()
    if len(words) >= 4:
        mid = len(words) // 2
        first_half = ' '.join(words[:mid])
        second_half = ' '.join(words[mid:])
        if first_half.lower() == second_half.lower():
            name = first_half

    # Clean up extra semicolons and whitespace
    name = re.sub(r'\s*;\s*', '; ', name)
    name = re.sub(r'\s+', ' ', name)

    return name.strip()

def main():
    print("Reading database...")

    rows = []
    with open('FEDERAL-CONTRACTOR-MASTER-DATABASE.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(dict(row))

    print(f"Loaded {len(rows)} rows")

    # Fix issues
    fixed_emails = 0
    fixed_names = 0

    for row in rows:
        # Fix email
        original_email = row.get('email', '')
        cleaned_email = clean_email(original_email)
        if cleaned_email != original_email:
            print(f"  Fixed email: {original_email[:50]} -> {cleaned_email}")
            row['email'] = cleaned_email
            fixed_emails += 1

        # Fix SBLO name
        original_name = row.get('sblo_name', '')
        cleaned_name = clean_sblo_name(original_name)
        if cleaned_name != original_name and original_name:
            print(f"  Fixed name: {original_name[:50]} -> {cleaned_name}")
            row['sblo_name'] = cleaned_name
            fixed_names += 1

    print(f"\nFixed {fixed_emails} emails, {fixed_names} names")

    # Write cleaned data
    print("Writing cleaned database...")
    with open('FEDERAL-CONTRACTOR-MASTER-DATABASE.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Done!")

    # Summary stats
    with_email = sum(1 for r in rows if r.get('email'))
    with_phone = sum(1 for r in rows if r.get('phone'))
    with_sblo = sum(1 for r in rows if r.get('sblo_name'))
    with_portal = sum(1 for r in rows if r.get('vendor_registration_url'))

    print(f"\nDatabase summary:")
    print(f"  Total companies: {len(rows)}")
    print(f"  With SBLO name: {with_sblo}")
    print(f"  With email: {with_email}")
    print(f"  With phone: {with_phone}")
    print(f"  With portal URL: {with_portal}")

if __name__ == '__main__':
    main()
