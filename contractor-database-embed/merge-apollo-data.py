#!/usr/bin/env python3
"""
Merge Apollo enriched data with existing contractor database
Updates data-extract.js for Vercel deployment
"""

import csv
import json
import sys
from datetime import datetime

print("=" * 70)
print("🔄 APOLLO DATA MERGE SCRIPT")
print("=" * 70)
print()

# Step 1: Read Apollo enriched data
print("📥 Step 1: Reading Apollo enriched CSV...")

try:
    apollo_file = input("Enter Apollo CSV filename (or press Enter for 'apollo-enriched.csv'): ").strip()
    if not apollo_file:
        apollo_file = 'apollo-enriched.csv'

    with open(apollo_file, 'r', encoding='utf-8') as f:
        apollo_data = list(csv.DictReader(f))

    print(f"✅ Loaded {len(apollo_data)} records from Apollo")
except FileNotFoundError:
    print(f"❌ Error: Could not find '{apollo_file}'")
    print("   Make sure you've downloaded the enriched CSV from Apollo")
    print("   and placed it in this folder")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error reading Apollo file: {e}")
    sys.exit(1)

print()

# Step 2: Read existing contractor data
print("📥 Step 2: Reading existing contractor database...")

try:
    with open('data-extract.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract JSON array
    start = content.find('const companies = [')
    end = content.rfind('];')

    if start == -1 or end == -1:
        raise ValueError("Could not find companies array in data-extract.js")

    json_str = content[start + 18:end + 1]  # Skip "const companies = "
    companies = json.loads(json_str)

    print(f"✅ Loaded {len(companies)} existing contractors")
except Exception as e:
    print(f"❌ Error reading existing data: {e}")
    sys.exit(1)

print()

# Step 3: Create lookup dictionary from Apollo data
print("🔍 Step 3: Creating Apollo lookup dictionary...")

apollo_lookup = {}
for row in apollo_data:
    # Try different possible column names from Apollo
    company_name = (
        row.get('Company Name') or
        row.get('Company') or
        row.get('Organization Name') or
        row.get('Account Name') or
        ''
    ).strip().upper()

    if company_name:
        apollo_lookup[company_name] = {
            'email': (row.get('Email') or row.get('Work Email') or '').strip(),
            'phone': (row.get('Phone') or row.get('Direct Phone') or row.get('Mobile Phone') or '').strip(),
            'name': (row.get('Full Name') or row.get('Name') or row.get('Contact Name') or '').strip(),
            'title': (row.get('Title') or row.get('Job Title') or '').strip(),
            'linkedin': (row.get('LinkedIn URL') or row.get('LinkedIn') or '').strip(),
        }

print(f"✅ Indexed {len(apollo_lookup)} Apollo companies")
print()

# Step 4: Merge data
print("🔄 Step 4: Merging Apollo data with existing database...")

updated_count = 0
email_added = 0
phone_added = 0
name_added = 0

for company in companies:
    company_name = company.get('company', '').strip().upper()

    if company_name in apollo_lookup:
        apollo_info = apollo_lookup[company_name]
        updated = False

        # Add email if missing
        if not company.get('email') and apollo_info['email']:
            company['email'] = apollo_info['email']
            company['has_email'] = True
            email_added += 1
            updated = True

        # Add phone if missing
        if not company.get('phone') and apollo_info['phone']:
            company['phone'] = apollo_info['phone']
            company['has_phone'] = True
            phone_added += 1
            updated = True

        # Add SBLO name if missing
        if not company.get('sblo_name') and apollo_info['name']:
            company['sblo_name'] = apollo_info['name']
            if apollo_info['title']:
                company['title'] = apollo_info['title']
            name_added += 1
            updated = True

        # Update has_contact flag
        if company.get('email') or company.get('phone') or company.get('sblo_name'):
            company['has_contact'] = True

        if updated:
            updated_count += 1

print(f"✅ Updated {updated_count} companies")
print(f"   📧 Added {email_added} emails")
print(f"   📞 Added {phone_added} phone numbers")
print(f"   👤 Added {name_added} contact names")
print()

# Step 5: Calculate new statistics
print("📊 Step 5: Calculating new statistics...")

total = len(companies)
with_email = sum(1 for c in companies if c.get('email'))
with_phone = sum(1 for c in companies if c.get('phone'))
with_contact = sum(1 for c in companies if c.get('has_contact'))

print(f"   Total contractors: {total:,}")
print(f"   With email: {with_email:,} ({(with_email/total)*100:.1f}%)")
print(f"   With phone: {with_phone:,} ({(with_phone/total)*100:.1f}%)")
print(f"   With any contact: {with_contact:,} ({(with_contact/total)*100:.1f}%)")
print()

# Step 6: Backup old file
print("💾 Step 6: Creating backup...")

backup_name = f"data-extract.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}.js"
try:
    with open('data-extract.js', 'r', encoding='utf-8') as f:
        backup_content = f.read()
    with open(backup_name, 'w', encoding='utf-8') as f:
        f.write(backup_content)
    print(f"✅ Backup saved as: {backup_name}")
except Exception as e:
    print(f"⚠️  Warning: Could not create backup: {e}")

print()

# Step 7: Write updated data
print("💾 Step 7: Writing updated data-extract.js...")

try:
    new_content = f"const companies = {json.dumps(companies, indent=2)};"

    with open('data-extract.js', 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✅ Successfully updated data-extract.js")
except Exception as e:
    print(f"❌ Error writing file: {e}")
    print(f"   Your original file is backed up as: {backup_name}")
    sys.exit(1)

print()

# Step 8: Show next steps
print("=" * 70)
print("✅ MERGE COMPLETE!")
print("=" * 70)
print()
print("📋 NEXT STEPS:")
print()
print("1. Verify the updated data:")
print("   - Open index.html in your browser")
print("   - Search for companies that previously had no contact info")
print("   - Verify they now show emails/phones")
print()
print("2. Deploy to Vercel:")
print("   cd /Users/ericcoffie/Bootcamp/contractor-database-embed")
print("   vercel --prod")
print()
print("3. Verify live site:")
print("   - Check your Vercel URL")
print("   - Test search functionality")
print("   - Verify contact info appears")
print()
print("4. Update Mighty Networks embed (if needed):")
print("   - Use latest Vercel URL")
print("   - Embed code should auto-update")
print()
print("=" * 70)
print()
print(f"💡 Backup saved: {backup_name}")
print("   (In case you need to revert)")
print()
print("🎉 Your database now has {:.1f}% contact coverage!".format((with_contact/total)*100))
print()
