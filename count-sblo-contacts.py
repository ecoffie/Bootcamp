#!/usr/bin/env python3
"""
Count unique companies with SBLO contacts in compiled list
"""

import csv

compiled_file = '/Users/ericcoffie/Bootcamp/sblo-list-compiled.csv'

total_rows = 0
rows_with_email = 0
rows_with_phone = 0
rows_with_both = 0
unique_companies = set()
unique_companies_with_email = set()

with open(compiled_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        total_rows += 1
        company = row.get('company', '').strip()
        email = row.get('email', '').strip()
        phone = row.get('phone', '').strip()

        if company:
            unique_companies.add(company.upper())

        if email:
            rows_with_email += 1
            if company:
                unique_companies_with_email.add(company.upper())

        if phone:
            rows_with_phone += 1

        if email and phone:
            rows_with_both += 1

print("=" * 80)
print("SBLO COMPILED LIST STATISTICS")
print("=" * 80)
print(f"\n📊 TOTAL ENTRIES:")
print(f"   • Total rows in file: {total_rows}")
print(f"   • Unique companies: {len(unique_companies)}")

print(f"\n📧 EMAIL CONTACTS:")
print(f"   • Rows with email: {rows_with_email}")
print(f"   • Unique companies with email: {len(unique_companies_with_email)}")
print(f"   • Percentage with email: {(len(unique_companies_with_email) / len(unique_companies) * 100):.1f}%")

print(f"\n📞 PHONE CONTACTS:")
print(f"   • Rows with phone: {rows_with_phone}")
print(f"   • Rows with both email & phone: {rows_with_both}")

print(f"\n✅ COMPLETE CONTACTS:")
print(f"   • Companies ready for outreach: {len(unique_companies_with_email)}")

print("\n" + "=" * 80)
