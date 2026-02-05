#!/usr/bin/env python3
"""
Compare Tier 2 High-Priority List with Full Tier 2 Directory
Shows overlap, unique companies, and data completeness
"""

import csv
from collections import defaultdict

# Read the high-priority list (46 companies with portal research)
priority_companies = set()
priority_data = {}

with open('tier2-high-priority-list.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = row['company'].strip().upper()
        priority_companies.add(company)
        priority_data[company] = {
            'sblo_name': row['sblo_name'],
            'email': row['email']
        }

# Read the full Tier 2 directory (168 companies)
full_directory_companies = set()
full_directory_data = {}

with open('TIER-2-FINAL-CONTACT-LIST-CLEAN.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company = row['company'].strip().upper()
        full_directory_companies.add(company)
        full_directory_data[company] = {
            'sblo_name': row['sblo_name'],
            'email': row['email'],
            'phone': row.get('phone', ''),
            'contact_quality': row.get('contact_quality', ''),
            'naics': row.get('naics', ''),
            'source': row.get('source', '')
        }

# Calculate overlap and differences
overlap = priority_companies & full_directory_companies
priority_only = priority_companies - full_directory_companies
directory_only = full_directory_companies - priority_companies

print("=" * 80)
print("TIER 2 LIST COMPARISON")
print("=" * 80)
print()

print("📊 SUMMARY STATISTICS")
print("-" * 80)
print(f"High-Priority List (with portal research):  {len(priority_companies):3d} companies")
print(f"Full Tier 2 Directory:                       {len(full_directory_companies):3d} companies")
print(f"Companies in BOTH lists:                     {len(overlap):3d} companies")
print(f"Only in High-Priority:                       {len(priority_only):3d} companies")
print(f"Only in Full Directory:                      {len(directory_only):3d} companies")
print()

print("📈 OVERLAP ANALYSIS")
print("-" * 80)
overlap_percentage = (len(overlap) / len(priority_companies)) * 100
print(f"Overlap Rate: {overlap_percentage:.1f}% of high-priority companies are in full directory")
print()

if overlap:
    print(f"✅ Companies in BOTH lists ({len(overlap)} companies):")
    print("-" * 80)
    for idx, company in enumerate(sorted(overlap), 1):
        print(f"{idx:3d}. {company.title()}")
    print()

if priority_only:
    print(f"🆕 Companies ONLY in High-Priority List ({len(priority_only)} companies):")
    print("-" * 80)
    print("These are companies with portal research but not in the main directory:")
    for idx, company in enumerate(sorted(priority_only), 1):
        email = priority_data[company]['email']
        print(f"{idx:3d}. {company.title()}")
        print(f"      Email: {email}")
    print()

if directory_only:
    print(f"📋 Companies ONLY in Full Directory ({len(directory_only)} companies):")
    print("-" * 80)
    print("These companies could benefit from vendor portal research:")
    print()

    # Categorize by contact quality
    by_quality = defaultdict(list)
    for company in directory_only:
        quality = full_directory_data[company].get('contact_quality', 'Unknown')
        by_quality[quality].append(company)

    for quality in ['Email + Phone', 'Email Only', 'Phone Only', 'Unknown']:
        if quality in by_quality:
            companies = sorted(by_quality[quality])
            print(f"\n{quality}: {len(companies)} companies")
            print("-" * 40)
            for idx, company in enumerate(companies[:10], 1):  # Show first 10
                email = full_directory_data[company]['email']
                source = full_directory_data[company]['source']
                print(f"{idx:3d}. {company.title()}")
                if email:
                    print(f"      Email: {email}")
                print(f"      Source: {source}")
            if len(companies) > 10:
                print(f"      ... and {len(companies) - 10} more")
    print()

print("=" * 80)
print("KEY INSIGHTS")
print("=" * 80)
print()

print("🎯 HIGH-PRIORITY LIST (46 companies):")
print("   • All companies have vendor portal research completed")
print("   • 97.8% require SBLO contact (45 companies)")
print("   • 2.2% have full portals (1 company - KPMG)")
print("   • All have cleaned and verified SBLO contact info")
print("   • PDF-ready directory created")
print()

print("📚 FULL TIER 2 DIRECTORY (168 companies):")
print("   • Comprehensive list from multiple sources:")
print("     - DHS Prime Contractors")
print("     - DOT Subcontracting Directory")
print("     - DoD CSP Prime Directory")
print("   • Includes NAICS codes and contact quality ratings")
print("   • NOT all companies have portal research yet")
print()

print("💡 RECOMMENDATIONS:")
print("   1. HIGH-PRIORITY LIST is your go-to-market starting point")
print("   2. Use FULL DIRECTORY for additional pipeline opportunities")
print(f"   3. Consider portal research for {len(directory_only)} remaining companies")
print("   4. Prioritize companies with 'Email + Phone' contact quality")
print()

# Export unique companies to CSV for further research
if directory_only:
    with open('tier2-remaining-for-portal-research.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['company', 'sblo_name', 'email', 'phone', 'contact_quality', 'naics', 'source'])

        for company in sorted(directory_only):
            data = full_directory_data[company]
            writer.writerow([
                company.title(),
                data['sblo_name'],
                data['email'],
                data['phone'],
                data['contact_quality'],
                data['naics'],
                data['source']
            ])

    print(f"📄 EXPORTED: tier2-remaining-for-portal-research.csv")
    print(f"   Contains {len(directory_only)} companies ready for future portal research")
    print()

print("=" * 80)
