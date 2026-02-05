#!/usr/bin/env python3
"""
Clean up the FEDERAL-CONTRACTOR-MASTER-DATABASE.csv:
1. Fix source column - standardize names
2. Fix rows where addresses/NAICS ended up in wrong columns
3. Clean up SBLO names and emails with parsing artifacts
"""

import csv
import re

def is_valid_source(source):
    """Check if source value is a valid source name."""
    valid_sources = [
        'SBA Prime Directory FY24',
        'DHS Prime Contractors Page',
        'DoD CSP Prime Directory',
        'DOT Subcontracting Directory',
        'Tribal 8(a) SBA Certified',
        'SBA Prime Directory FY24 | Tribal 8(a)',
        'SBA Prime Directory FY24 | Tribal 8(a) SBA Certified'
    ]

    if not source:
        return False

    # Check if it matches known sources
    for valid in valid_sources:
        if valid.lower() in source.lower():
            return True

    # Check if it looks like an address, state, or NAICS code
    if re.match(r'^\d{6}', source):  # Starts with 6 digits (NAICS)
        return False
    if re.search(r'\d{5}"?$', source):  # Ends with zip code
        return False
    if re.search(r'(Alaska|Virginia|Texas|California|Florida|Colorado|Hawaii|Oklahoma|Alabama|Arizona|Maryland|Washington|Georgia|North Carolina|South Carolina|New Mexico|New Jersey|Nevada|Wisconsin|Montana|Oregon|Idaho|Utah|Kansas|Kentucky|Tennessee|Michigan|Ohio|Pennsylvania|Massachusetts|Connecticut|Rhode Island|Vermont|Maine|New Hampshire|New York|Illinois|Missouri|Nebraska|Iowa|Minnesota|North Dakota|South Dakota|Wyoming|Louisiana|Mississippi|Arkansas|Indiana|West Virginia|Delaware|District of Columbia|Puerto Rico)\s+\d{5}', source, re.IGNORECASE):
        return False
    if source.isupper() and len(source.split()) <= 2 and not any(c.isdigit() for c in source):
        # Looks like a city name
        return False
    if 'SUITE' in source or 'STE' in source:
        return False

    return True

def clean_source(source):
    """Standardize source name."""
    if not source:
        return 'SBA Prime Directory FY24'

    source_lower = source.lower()

    if 'tribal' in source_lower and '8(a)' in source_lower:
        return 'SBA Prime Directory FY24 | Tribal 8(a)'
    if 'dhs' in source_lower:
        return 'DHS Prime Contractors Page'
    if 'dod' in source_lower or 'defense' in source_lower:
        return 'DoD CSP Prime Directory'
    if 'dot' in source_lower or 'transportation' in source_lower:
        return 'DOT Subcontracting Directory'
    if 'sba' in source_lower:
        return 'SBA Prime Directory FY24'

    return 'SBA Prime Directory FY24'

def clean_sblo_name(name):
    """Clean up SBLO name - remove parsing artifacts."""
    if not name:
        return ''

    # Remove duplicate names (e.g., "John Smith John Smith")
    words = name.split()
    if len(words) >= 4:
        mid = len(words) // 2
        first_half = ' '.join(words[:mid])
        second_half = ' '.join(words[mid:])
        if first_half.lower() == second_half.lower():
            name = first_half

    # Remove email-like suffixes
    name = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}.*$', '', name)

    # Remove "Small", "Website", "SBLO" suffixes that got concatenated
    name = re.sub(r'(Small|Website|SBLO|smallbusinesscompliance|Burtonsmallbusinesscompliance)$', '', name, flags=re.IGNORECASE)

    # Remove role suffixes that got concatenated
    name = re.sub(r'(SBLO|Small Business|Liaison)$', '', name, flags=re.IGNORECASE)

    return name.strip()

def clean_email(email):
    """Clean up email - remove parsing artifacts."""
    if not email:
        return ''

    # If multiple emails, take the first valid one
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', email)
    if emails:
        # Return the first one that doesn't have artifacts
        for e in emails:
            if not any(artifact in e.lower() for artifact in ['website', 'small']):
                return e
        return emails[0]

    return ''

def main():
    print("Reading database...")

    rows = []
    with open('FEDERAL-CONTRACTOR-MASTER-DATABASE.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(dict(row))

    print(f"Loaded {len(rows)} rows")

    # Count issues before
    bad_sources = sum(1 for r in rows if not is_valid_source(r.get('source', '')))
    print(f"Rows with bad source values: {bad_sources}")

    # Clean up each row
    cleaned = 0
    for row in rows:
        original = dict(row)

        # Clean source
        source = row.get('source', '')
        if not is_valid_source(source):
            row['source'] = 'SBA Prime Directory FY24'
            cleaned += 1
        else:
            row['source'] = clean_source(source)

        # Clean SBLO name
        sblo_name = row.get('sblo_name', '')
        row['sblo_name'] = clean_sblo_name(sblo_name)

        # Clean email
        email = row.get('email', '')
        row['email'] = clean_email(email)

    print(f"Cleaned {cleaned} rows")

    # Count sources after
    source_counts = {}
    for row in rows:
        source = row.get('source', 'Unknown')
        source_counts[source] = source_counts.get(source, 0) + 1

    print("\nSource distribution after cleanup:")
    for source, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        print(f"  {source}: {count}")

    # Write cleaned data
    print("\nWriting cleaned database...")
    with open('FEDERAL-CONTRACTOR-MASTER-DATABASE.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Done!")

    # Show some examples of cleaned data
    print("\nSample cleaned rows:")
    for row in rows[:5]:
        print(f"  {row['company'][:40]}: source={row['source']}, sblo={row['sblo_name'][:30] if row['sblo_name'] else 'N/A'}")

if __name__ == '__main__':
    main()
