#!/usr/bin/env python3
"""
Consolidate vendor portal research from batches back into main SBLO lists
"""

import csv
import glob
import os
from collections import defaultdict

def read_batch_results(pattern):
    """Read all batch files matching pattern and extract vendor portal data"""

    vendor_data = {}

    batch_files = sorted(glob.glob(pattern))

    print(f"Found {len(batch_files)} batch files matching pattern: {pattern}")

    for batch_file in batch_files:
        print(f"  Reading: {batch_file}")

        with open(batch_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                company = row.get('company', '')
                if company and row.get('vendor_registration_url'):
                    vendor_data[company] = {
                        'vendor_registration_url': row.get('vendor_registration_url', ''),
                        'portal_type': row.get('portal_type', ''),
                        'portal_notes': row.get('notes', '')
                    }

    print(f"  Extracted data for {len(vendor_data)} companies\n")
    return vendor_data

def update_sblo_list(input_file, output_file, vendor_data):
    """Update SBLO list with vendor portal data"""

    print(f"Updating {input_file}...")

    companies = []
    updated_count = 0

    # Read original file
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)

        # Add new fields if they don't exist
        new_fields = ['vendor_registration_url', 'portal_type', 'portal_notes']
        for field in new_fields:
            if field not in fieldnames:
                fieldnames.append(field)

        for row in reader:
            company_name = row.get('company', '')

            # Check if we have vendor data for this company
            if company_name in vendor_data:
                row['vendor_registration_url'] = vendor_data[company_name]['vendor_registration_url']
                row['portal_type'] = vendor_data[company_name]['portal_type']
                row['portal_notes'] = vendor_data[company_name]['portal_notes']
                updated_count += 1
            else:
                # Keep existing data or leave blank
                if 'vendor_registration_url' not in row:
                    row['vendor_registration_url'] = ''
                if 'portal_type' not in row:
                    row['portal_type'] = ''
                if 'portal_notes' not in row:
                    row['portal_notes'] = ''

            companies.append(row)

    # Write updated file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(companies)

    print(f"  ✓ Updated {updated_count} companies")
    print(f"  ✓ Saved to: {output_file}\n")

    return updated_count

def generate_summary(tier1_file, tier2_file):
    """Generate summary report of vendor portal research"""

    def count_portals(filename):
        stats = {
            'total': 0,
            'with_portal': 0,
            'full_portal': 0,
            'email_registration': 0,
            'contact_form': 0,
            'pdf_form': 0,
            'none_found': 0,
            'not_researched': 0
        }

        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                stats['total'] += 1

                portal_url = row.get('vendor_registration_url', '')
                portal_type = row.get('portal_type', '')

                if portal_url:
                    stats['with_portal'] += 1

                    if portal_type == 'Full Portal':
                        stats['full_portal'] += 1
                    elif portal_type == 'Email Registration':
                        stats['email_registration'] += 1
                    elif portal_type == 'Contact Form':
                        stats['contact_form'] += 1
                    elif portal_type == 'PDF Form':
                        stats['pdf_form'] += 1
                    elif portal_type == 'None Found':
                        stats['none_found'] += 1
                else:
                    stats['not_researched'] += 1

        return stats

    print("\n" + "=" * 80)
    print("VENDOR PORTAL RESEARCH SUMMARY")
    print("=" * 80)

    # Tier 1 stats
    tier1_stats = count_portals(tier1_file)
    print(f"\nTIER 1 COMPANIES:")
    print(f"  Total companies: {tier1_stats['total']}")
    print(f"  With vendor portal URL: {tier1_stats['with_portal']} ({tier1_stats['with_portal']/tier1_stats['total']*100:.1f}%)")
    print(f"    - Full Portal: {tier1_stats['full_portal']}")
    print(f"    - Email Registration: {tier1_stats['email_registration']}")
    print(f"    - Contact Form: {tier1_stats['contact_form']}")
    print(f"    - PDF Form: {tier1_stats['pdf_form']}")
    print(f"    - None Found: {tier1_stats['none_found']}")
    print(f"  Not yet researched: {tier1_stats['not_researched']} ({tier1_stats['not_researched']/tier1_stats['total']*100:.1f}%)")

    # Tier 2 stats
    tier2_stats = count_portals(tier2_file)
    print(f"\nTIER 2 COMPANIES:")
    print(f"  Total companies: {tier2_stats['total']}")
    print(f"  With vendor portal URL: {tier2_stats['with_portal']} ({tier2_stats['with_portal']/tier2_stats['total']*100:.1f}%)")
    print(f"    - Full Portal: {tier2_stats['full_portal']}")
    print(f"    - Email Registration: {tier2_stats['email_registration']}")
    print(f"    - Contact Form: {tier2_stats['contact_form']}")
    print(f"    - PDF Form: {tier2_stats['pdf_form']}")
    print(f"    - None Found: {tier2_stats['none_found']}")
    print(f"  Not yet researched: {tier2_stats['not_researched']} ({tier2_stats['not_researched']/tier2_stats['total']*100:.1f}%)")

    # Overall stats
    total = tier1_stats['total'] + tier2_stats['total']
    with_portal = tier1_stats['with_portal'] + tier2_stats['with_portal']
    not_researched = tier1_stats['not_researched'] + tier2_stats['not_researched']

    print(f"\nOVERALL:")
    print(f"  Total companies: {total}")
    print(f"  With vendor portal URL: {with_portal} ({with_portal/total*100:.1f}%)")
    print(f"  Not yet researched: {not_researched} ({not_researched/total*100:.1f}%)")

    print("=" * 80)

def main():
    print("=" * 80)
    print("VENDOR PORTAL CONSOLIDATION SCRIPT")
    print("=" * 80)
    print()

    # Read all priority batch results
    print("STEP 1: Reading priority batch results...")
    priority_data = read_batch_results('priority-batch-*.csv')

    # Read all tier1 batch results
    print("STEP 2: Reading Tier 1 batch results...")
    tier1_data = read_batch_results('tier1-batch-*.csv')

    # Read all tier2 batch results
    print("STEP 3: Reading Tier 2 batch results...")
    tier2_data = read_batch_results('tier2-batch-*.csv')

    # Combine priority data with tier1 data (priority companies are subset of tier1)
    tier1_data.update(priority_data)

    # Update main SBLO lists
    print("STEP 4: Updating main SBLO lists...")
    tier1_updated = update_sblo_list(
        'FINAL-SBLO-CONTACT-LIST.csv',
        'FINAL-SBLO-CONTACT-LIST-WITH-PORTALS.csv',
        tier1_data
    )

    tier2_updated = update_sblo_list(
        'TIER-2-FINAL-CONTACT-LIST-CLEAN.csv',
        'TIER-2-FINAL-CONTACT-LIST-WITH-PORTALS.csv',
        tier2_data
    )

    # Generate summary
    generate_summary(
        'FINAL-SBLO-CONTACT-LIST-WITH-PORTALS.csv',
        'TIER-2-FINAL-CONTACT-LIST-WITH-PORTALS.csv'
    )

    print("\n✓ Consolidation complete!")
    print("\nNew files created:")
    print("  - FINAL-SBLO-CONTACT-LIST-WITH-PORTALS.csv")
    print("  - TIER-2-FINAL-CONTACT-LIST-WITH-PORTALS.csv")

if __name__ == '__main__':
    main()
