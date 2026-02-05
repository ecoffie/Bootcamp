#!/usr/bin/env python3
"""
Create enhanced PDF with NAICS codes and descriptions
"""

import csv
import html
import re

# Common NAICS code descriptions
NAICS_DESCRIPTIONS = {
    '236220': 'Commercial Building Construction',
    '237110': 'Water & Sewer Line Construction',
    '237120': 'Oil & Gas Pipeline Construction',
    '237310': 'Highway, Street, & Bridge Construction',
    '237990': 'Other Heavy Construction',
    '325412': 'Pharmaceutical Preparation Manufacturing',
    '325920': 'Explosives Manufacturing',
    '332322': 'Sheet Metal Work Manufacturing',
    '332410': 'Power Boiler & Heat Exchanger Manufacturing',
    '332510': 'Hardware Manufacturing',
    '332722': 'Bolt, Nut, Screw, Rivet Manufacturing',
    '332919': 'Other Metal Valve & Pipe Fitting',
    '332991': 'Ball & Roller Bearing Manufacturing',
    '332992': 'Small Arms Ammunition Manufacturing',
    '332993': 'Ammunition (except Small Arms) Manufacturing',
    '332994': 'Small Arms, Ordnance, & Accessories',
    '332999': 'All Other Miscellaneous Fabricated Metal',
    '333120': 'Construction Machinery Manufacturing',
    '333242': 'Semiconductor Machinery Manufacturing',
    '333310': 'Commercial & Service Industry Machinery',
    '333314': 'Optical Instrument & Lens Manufacturing',
    '333318': 'Other Commercial & Service Equipment',
    '333413': 'Industrial & Commercial Fan & Blower',
    '333415': 'Air-Conditioning & Warm Air Heating',
    '333611': 'Turbine & Turbine Generator Set Units',
    '333612': 'Speed Changer, Drive, & Gear Manufacturing',
    '333618': 'Other Engine Equipment Manufacturing',
    '333997': 'Scale & Balance Manufacturing',
    '333998': 'All Other Miscellaneous Machinery',
    '333999': 'All Other General Purpose Machinery',
    '334111': 'Electronic Computer Manufacturing',
    '334118': 'Computer Terminal & Other Equipment',
    '334210': 'Telephone Apparatus Manufacturing',
    '334220': 'Radio & TV Broadcasting Equipment',
    '334290': 'Other Communications Equipment',
    '334412': 'Bare Printed Circuit Board Manufacturing',
    '334418': 'Printed Circuit Assembly Manufacturing',
    '334419': 'Other Electronic Component Manufacturing',
    '334511': 'Search, Detection, Navigation Equipment',
    '334513': 'Industrial Process Variable Instruments',
    '334515': 'Electricity & Signal Testing Instruments',
    '334517': 'Irradiation Apparatus Manufacturing',
    '334519': 'Other Measuring & Controlling Devices',
    '334613': 'Blank Magnetic & Optical Media',
    '335312': 'Motor & Generator Manufacturing',
    '335910': 'Battery Manufacturing',
    '335999': 'All Other Electrical Equipment',
    '336120': 'Heavy Duty Truck Manufacturing',
    '336211': 'Motor Vehicle Body Manufacturing',
    '336212': 'Truck Trailer Manufacturing',
    '336214': 'Travel Trailer & Camper Manufacturing',
    '336310': 'Motor Vehicle Gasoline Engine Parts',
    '336320': 'Motor Vehicle Electrical Equipment',
    '336350': 'Motor Vehicle Transmission & Power Train',
    '336360': 'Motor Vehicle Seating & Interior Trim',
    '336390': 'Other Motor Vehicle Parts Manufacturing',
    '336411': 'Aircraft Manufacturing',
    '336412': 'Aircraft Engine & Engine Parts',
    '336413': 'Other Aircraft Parts & Equipment',
    '336414': 'Guided Missile & Space Vehicle',
    '336419': 'Other Guided Missile & Space Vehicle Parts',
    '336611': 'Ship Building & Repairing',
    '336992': 'Military Armored Vehicle & Tank Parts',
    '336999': 'All Other Transportation Equipment',
    '339112': 'Surgical & Medical Instrument Manufacturing',
    '423450': 'Medical Equipment & Supplies Wholesalers',
    '481212': 'Nonscheduled Chartered Freight Air',
    '488111': 'Air Traffic Control',
    '488190': 'Other Support Activities for Air Transportation',
    '488390': 'Other Support Activities for Water Transportation',
    '493110': 'General Warehousing & Storage',
    '511210': 'Software Publishers',
    '513210': 'Software Publishers (Alt)',
    '517110': 'Wired Telecommunications Carriers',
    '517112': 'Wireless Telecommunications (except Satellite)',
    '517410': 'Satellite Telecommunications',
    '517810': 'All Other Telecommunications',
    '517919': 'All Other Telecommunications',
    '518210': 'Data Processing, Hosting, & Related Services',
    '524114': 'Direct Health & Medical Insurance Carriers',
    '524292': 'Third Party Administration of Insurance',
    '541199': 'All Other Legal Services',
    '541211': 'Offices of Certified Public Accountants',
    '541219': 'Other Accounting Services',
    '541310': 'Architectural Services',
    '541330': 'Engineering Services',
    '541370': 'Surveying & Mapping Services',
    '541380': 'Testing Laboratories',
    '541511': 'Custom Computer Programming Services',
    '541512': 'Computer Systems Design Services',
    '541513': 'Computer Facilities Management Services',
    '541519': 'Other Computer Related Services',
    '541611': 'Administrative Management Consulting',
    '541612': 'Human Resources Consulting Services',
    '541613': 'Marketing Consulting Services',
    '541614': 'Process/Physical Distribution/Logistics',
    '541618': 'Other Management Consulting Services',
    '541620': 'Environmental Consulting Services',
    '541690': 'Other Scientific & Technical Consulting',
    '541710': 'Research & Development in Physical Sciences',
    '541712': 'Research & Development in Life Sciences',
    '541713': 'Research & Development in Nanotechnology',
    '541714': 'Research & Development in Biotechnology',
    '541715': 'Research & Development - Physical, Engineering, Life Sciences',
    '541720': 'Research & Development in Social Sciences',
    '541910': 'Marketing Research & Public Opinion Polling',
    '541990': 'All Other Professional, Scientific, Technical',
    '561210': 'Facilities Support Services',
    '561611': 'Investigation Services',
    '561612': 'Security Guards & Patrol Services',
    '561621': 'Security Systems Services',
    '561990': 'All Other Support Services',
    '562910': 'Remediation Services',
    '611430': 'Professional & Management Development Training',
    '611512': 'Flight Training',
    '611519': 'Other Technical & Trade Schools',
    '621111': 'Offices of Physicians',
    '621112': 'Offices of Physicians, Mental Health',
    '621498': 'All Other Outpatient Care Centers',
    '624230': 'Emergency & Other Relief Services',
    '811111': 'General Automotive Repair',
    '811210': 'Electronic & Precision Equipment Repair',
    '811219': 'Other Electronic & Precision Equipment',
    '811310': 'Commercial & Industrial Machinery Repair',
    '923120': 'Administration of Public Health Programs',
    '923130': 'Administration of Human Resource Programs',
}

def get_naics_description(naics_code):
    """Get human-readable description for NAICS code"""
    code = naics_code.strip()
    return NAICS_DESCRIPTIONS.get(code, f'Industry Code {code}')

def format_naics_list(naics_string):
    """Format NAICS codes with descriptions"""
    if not naics_string or naics_string.strip() == '':
        return ''

    codes = [c.strip() for c in naics_string.split(',')]
    if len(codes) == 0:
        return ''

    # For multiple codes, show first 2 with descriptions
    if len(codes) > 2:
        formatted = []
        for code in codes[:2]:
            desc = get_naics_description(code)
            formatted.append(f'{code} - {desc}')
        formatted.append(f'+ {len(codes) - 2} more')
        return '<br>'.join(formatted)
    else:
        formatted = []
        for code in codes:
            desc = get_naics_description(code)
            formatted.append(f'{code} - {desc}')
        return '<br>'.join(formatted)

# Read contacts
csv_file = '/Users/ericcoffie/Bootcamp/FINAL-SBLO-CONTACT-LIST.csv'
contacts = []
with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    contacts = list(reader)

# Sort alphabetically
contacts.sort(key=lambda x: x['company'].upper())

# Generate table rows HTML
rows_html = []
for contact in contacts:
    quality = contact['contact_quality']
    if 'Both' in quality:
        badge_class = 'badge-both'
    elif 'Phone Only' in quality:
        badge_class = 'badge-phone'
    else:
        badge_class = 'badge-email'

    company = html.escape(contact['company'])
    sblo_name = html.escape(contact['sblo_name'])
    email = html.escape(contact['email'])
    phone = html.escape(contact['phone'])
    naics_formatted = format_naics_list(contact['naics'])

    row = f'''        <tr>
            <td class="company-name">{company}</td>
            <td>{sblo_name}</td>
            <td class="email">{email}</td>
            <td class="phone">{phone}</td>
            <td class="naics">{naics_formatted}</td>
            <td><span class="badge {badge_class}">{quality}</span></td>
        </tr>'''
    rows_html.append(row)

table_html = '\n'.join(rows_html)

# Create enhanced HTML
html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prime Contractor SBLO Contact Directory with NAICS</title>
    <style>
        @page {{
            size: letter landscape;
            margin: 0.4in;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 8pt;
            line-height: 1.2;
            color: #333;
            background: white;
        }}

        .header {{
            text-align: center;
            padding: 15px 0;
            border-bottom: 3px solid #2c5282;
            margin-bottom: 15px;
            page-break-after: avoid;
        }}

        .header h1 {{
            font-size: 20pt;
            color: #2c5282;
            margin-bottom: 5px;
        }}

        .header .subtitle {{
            font-size: 10pt;
            color: #666;
        }}

        .stats {{
            background: #f7fafc;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 15px;
            border: 1px solid #e2e8f0;
            page-break-inside: avoid;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }}

        .stat-box {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 18pt;
            font-weight: bold;
            color: #2c5282;
        }}

        .stat-label {{
            font-size: 7pt;
            color: #666;
        }}

        .contact-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }}

        .contact-table thead {{
            background: #2c5282;
            color: white;
        }}

        .contact-table th {{
            padding: 8px 6px;
            text-align: left;
            font-size: 8pt;
            font-weight: 600;
            border-right: 1px solid white;
        }}

        .contact-table th:last-child {{
            border-right: none;
        }}

        .contact-table tbody tr {{
            border-bottom: 1px solid #e2e8f0;
            page-break-inside: avoid;
        }}

        .contact-table tbody tr:nth-child(even) {{
            background: #f7fafc;
        }}

        .contact-table td {{
            padding: 6px 4px;
            font-size: 7pt;
            vertical-align: top;
        }}

        .company-name {{
            font-weight: 600;
            color: #2c5282;
        }}

        .email {{
            color: #2b6cb0;
            word-break: break-all;
        }}

        .phone {{
            color: #2d3748;
            white-space: nowrap;
        }}

        .naics {{
            font-size: 6.5pt;
            color: #4a5568;
            line-height: 1.3;
        }}

        .badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 10px;
            font-size: 6pt;
            font-weight: 600;
            text-transform: uppercase;
            white-space: nowrap;
        }}

        .badge-both {{
            background: #c6f6d5;
            color: #22543d;
        }}

        .badge-email {{
            background: #bee3f8;
            color: #2c5282;
        }}

        .badge-phone {{
            background: #feebc8;
            color: #7c2d12;
        }}

        .footer {{
            margin-top: 20px;
            padding-top: 10px;
            border-top: 2px solid #e2e8f0;
            text-align: center;
            font-size: 7pt;
            color: #666;
            page-break-inside: avoid;
        }}

        @media print {{
            body {{
                background: white;
            }}
            .contact-table thead {{
                display: table-header-group;
            }}
            .contact-table tbody tr {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>

<div class="header">
    <h1>Prime Contractor SBLO Contact Directory</h1>
    <div class="subtitle">Small Business Liaison Officer Contacts with Industry Focus (NAICS)</div>
    <div style="font-size: 8pt; color: #718096; margin-top: 8px;">
        December 2025 | Federal Government Prime Contractors
    </div>
</div>

<div class="stats">
    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-number">225</div>
            <div class="stat-label">Total Companies</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">93</div>
            <div class="stat-label">With Email</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">161</div>
            <div class="stat-label">With Phone</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">29</div>
            <div class="stat-label">Both Contacts</div>
        </div>
    </div>
</div>

<table class="contact-table">
    <thead>
        <tr>
            <th style="width: 18%">Company</th>
            <th style="width: 12%">SBLO Name</th>
            <th style="width: 22%">Email</th>
            <th style="width: 12%">Phone</th>
            <th style="width: 26%">Industry Focus (NAICS)</th>
            <th style="width: 10%">Contact</th>
        </tr>
    </thead>
    <tbody>
{table_html}
    </tbody>
</table>

<div class="footer">
    <p><strong>Prime Contractor SBLO Directory with Industry Focus</strong> | December 2025</p>
    <p style="margin-top: 5px;">
        Sources: DHS Prime Contractors, SBA Prime Directory FY24, DoD CSP Directory, DOT Subcontracting Directory
    </p>
    <p style="margin-top: 8px; font-style: italic;">
        🤖 Generated with <a href="https://claude.com/claude-code" style="color: #2c5282; text-decoration: none;">Claude Code</a>
    </p>
</div>

</body>
</html>'''

# Write output
output_file = '/Users/ericcoffie/Bootcamp/SBLO-DIRECTORY-WITH-NAICS-PDF-READY.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("=" * 80)
print("ENHANCED PDF WITH NAICS CREATED")
print("=" * 80)
print(f"\n✅ Created directory with NAICS industry codes")
print(f"📄 File: {output_file}")
print(f"\n📊 Features:")
print(f"   • 225 companies with contacts")
print(f"   • NAICS codes with descriptions")
print(f"   • Landscape layout for better readability")
print(f"   • Color-coded contact types")
print(f"\n📝 TO CREATE PDF:")
print(f"   1. Opening file in browser...")
print(f"   2. Press Cmd+P")
print(f"   3. Save as PDF")
print(f"   4. Enable 'Print backgrounds'")
print("\n" + "=" * 80)
