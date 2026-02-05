#!/usr/bin/env python3
"""
Embed contact data directly into HTML for easy PDF export
"""

import csv
import html

csv_file = '/Users/ericcoffie/Bootcamp/FINAL-SBLO-CONTACT-LIST.csv'
html_template_file = '/Users/ericcoffie/Bootcamp/FINAL-SBLO-CONTACT-LIST.html'
output_html = '/Users/ericcoffie/Bootcamp/SBLO-CONTACT-DIRECTORY-PDF-READY.html'

# Read contacts
contacts = []
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    contacts = list(reader)

# Sort alphabetically
contacts.sort(key=lambda x: x['company'].upper())

# Generate table rows HTML
rows_html = []
for contact in contacts:
    # Determine badge class
    quality = contact['contact_quality']
    if 'Both' in quality:
        badge_class = 'badge-both'
    elif 'Phone Only' in quality:
        badge_class = 'badge-phone'
    else:
        badge_class = 'badge-email'

    # Escape HTML
    company = html.escape(contact['company'])
    sblo_name = html.escape(contact['sblo_name'])
    email = html.escape(contact['email'])
    phone = html.escape(contact['phone'])

    row = f'''        <tr>
            <td class="company-name">{company}</td>
            <td>{sblo_name}</td>
            <td class="email">{email}</td>
            <td class="phone">{phone}</td>
            <td><span class="badge {badge_class}">{quality}</span></td>
        </tr>'''

    rows_html.append(row)

# Read HTML template
with open(html_template_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace placeholder and script section
table_html = '\n'.join(rows_html)

# Remove the script section and placeholder comment
import re
html_content = re.sub(
    r'<tbody>.*?</tbody>',
    f'<tbody>\n{table_html}\n    </tbody>',
    html_content,
    flags=re.DOTALL
)

# Remove the script tag
html_content = re.sub(
    r'<script>.*?</script>',
    '',
    html_content,
    flags=re.DOTALL
)

# Write output
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("=" * 80)
print("PDF-READY HTML CREATED")
print("=" * 80)
print(f"\n✅ Embedded {len(contacts)} contacts into HTML")
print(f"📄 File: {output_html}")
print("\n📝 TO CREATE PDF:")
print("   1. Open the file in Chrome or Safari")
print("   2. Press Cmd+P (Mac) or Ctrl+P (Windows)")
print("   3. Select 'Save as PDF'")
print("   4. Enable 'Background graphics' in print settings")
print("   5. Click 'Save'")
print("\n" + "=" * 80)
