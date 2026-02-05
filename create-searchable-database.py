#!/usr/bin/env python3
"""
Create searchable web database from all 897 companies
"""

import csv
import json
import html

# NAICS code descriptions
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

# Read all companies
csv_file = '/Users/ericcoffie/Bootcamp/sblo-list-compiled.csv'
companies = []

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company_name = row.get('company', '').strip()

        # Skip invalid entries
        if not company_name or company_name in ['In Search Of:', 'Contract', 'https://']:
            continue

        email = row.get('email', '').strip()
        phone = row.get('phone', '').strip()

        # Determine contact quality
        has_email = bool(email)
        has_phone = bool(phone)

        companies.append({
            'company': company_name,
            'sblo_name': row.get('sblo_name', '').strip(),
            'title': row.get('title', '').strip(),
            'email': email,
            'phone': phone,
            'address': row.get('address', '').strip(),
            'naics': row.get('naics', '').strip(),
            'source': row.get('source', '').strip(),
            'has_email': has_email,
            'has_phone': has_phone
        })

# Sort alphabetically
companies.sort(key=lambda x: x['company'].upper())

print(f"Loaded {len(companies)} companies")

# Convert to JSON for embedding in HTML
companies_json = json.dumps(companies, indent=2)
naics_json = json.dumps(NAICS_DESCRIPTIONS, indent=2)

# Create searchable HTML
html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Federal Contractor Database - Searchable Directory</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 32px;
            margin-bottom: 10px;
        }}

        .header p {{
            font-size: 16px;
            opacity: 0.9;
        }}

        .controls {{
            padding: 30px;
            background: #f7fafc;
            border-bottom: 2px solid #e2e8f0;
        }}

        .search-box {{
            width: 100%;
            padding: 15px 20px;
            font-size: 16px;
            border: 2px solid #cbd5e0;
            border-radius: 8px;
            margin-bottom: 20px;
            transition: all 0.3s;
        }}

        .search-box:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}

        .filters {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .filter-group {{
            display: flex;
            flex-direction: column;
        }}

        .filter-group label {{
            font-size: 12px;
            font-weight: 600;
            color: #4a5568;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .filter-group select {{
            padding: 10px;
            border: 2px solid #cbd5e0;
            border-radius: 6px;
            font-size: 14px;
            background: white;
            cursor: pointer;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            padding: 20px 30px;
            background: white;
            border-bottom: 1px solid #e2e8f0;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-number {{
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
        }}

        .stat-label {{
            font-size: 12px;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 5px;
        }}

        .results {{
            padding: 30px;
            max-height: 600px;
            overflow-y: auto;
        }}

        .company-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }}

        .company-card:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}

        .company-name {{
            font-size: 20px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
        }}

        .company-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .detail {{
            display: flex;
            flex-direction: column;
        }}

        .detail-label {{
            font-size: 11px;
            font-weight: 600;
            color: #718096;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}

        .detail-value {{
            font-size: 14px;
            color: #2d3748;
            word-break: break-word;
        }}

        .detail-value a {{
            color: #667eea;
            text-decoration: none;
        }}

        .detail-value a:hover {{
            text-decoration: underline;
        }}

        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            margin-right: 5px;
            margin-top: 5px;
        }}

        .badge-email {{
            background: #bee3f8;
            color: #2c5282;
        }}

        .badge-phone {{
            background: #c6f6d5;
            color: #22543d;
        }}

        .badge-both {{
            background: #fbb6ce;
            color: #702459;
        }}

        .naics-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            margin-top: 5px;
        }}

        .naics-code {{
            background: #edf2f7;
            color: #4a5568;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-family: monospace;
        }}

        .no-results {{
            text-align: center;
            padding: 60px 20px;
            color: #718096;
        }}

        .no-results-icon {{
            font-size: 64px;
            margin-bottom: 20px;
        }}

        .export-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}

        .export-btn:hover {{
            background: #5568d3;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}

        ::-webkit-scrollbar {{
            width: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: #f1f1f1;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #888;
            border-radius: 5px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #555;
        }}
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>Federal Contractor Database</h1>
        <p>Searchable directory of {len(companies)} federal contractors and their SBLO contacts</p>
    </div>

    <div class="controls">
        <input type="text" id="searchBox" class="search-box" placeholder="Search by company name, SBLO name, email, or NAICS code...">

        <div class="filters">
            <div class="filter-group">
                <label>Contact Type</label>
                <select id="contactFilter">
                    <option value="all">All Companies</option>
                    <option value="email">Has Email</option>
                    <option value="phone">Has Phone</option>
                    <option value="both">Has Both</option>
                    <option value="none">No Contact Info</option>
                </select>
            </div>

            <div class="filter-group">
                <label>Source</label>
                <select id="sourceFilter">
                    <option value="all">All Sources</option>
                </select>
            </div>

            <div class="filter-group">
                <label>Actions</label>
                <button class="export-btn" onclick="exportResults()">Export Results (CSV)</button>
            </div>
        </div>
    </div>

    <div class="stats">
        <div class="stat">
            <div class="stat-number" id="totalCount">0</div>
            <div class="stat-label">Total Results</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="emailCount">0</div>
            <div class="stat-label">With Email</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="phoneCount">0</div>
            <div class="stat-label">With Phone</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="bothCount">0</div>
            <div class="stat-label">Both Contacts</div>
        </div>
    </div>

    <div class="results" id="results"></div>
</div>

<script>
// Data
const companies = {companies_json};
const naicsDescriptions = {naics_json};

let filteredCompanies = [...companies];

// Populate source filter
const sourceFilter = document.getElementById('sourceFilter');
const sources = [...new Set(companies.map(c => c.source).filter(s => s))];
sources.forEach(source => {{
    const option = document.createElement('option');
    option.value = source;
    option.textContent = source;
    sourceFilter.appendChild(option);
}});

// Search and filter
function filterCompanies() {{
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();
    const contactFilter = document.getElementById('contactFilter').value;
    const sourceFilter = document.getElementById('sourceFilter').value;

    filteredCompanies = companies.filter(company => {{
        // Search filter
        const matchesSearch =
            company.company.toLowerCase().includes(searchTerm) ||
            company.sblo_name.toLowerCase().includes(searchTerm) ||
            company.email.toLowerCase().includes(searchTerm) ||
            company.naics.toLowerCase().includes(searchTerm) ||
            company.source.toLowerCase().includes(searchTerm);

        // Contact filter
        let matchesContact = true;
        if (contactFilter === 'email') matchesContact = company.has_email;
        else if (contactFilter === 'phone') matchesContact = company.has_phone;
        else if (contactFilter === 'both') matchesContact = company.has_email && company.has_phone;
        else if (contactFilter === 'none') matchesContact = !company.has_email && !company.has_phone;

        // Source filter
        const matchesSource = sourceFilter === 'all' || company.source === sourceFilter;

        return matchesSearch && matchesContact && matchesSource;
    }});

    renderResults();
}}

// Render results
function renderResults() {{
    const resultsDiv = document.getElementById('results');

    if (filteredCompanies.length === 0) {{
        resultsDiv.innerHTML = `
            <div class="no-results">
                <div class="no-results-icon">🔍</div>
                <h2>No companies found</h2>
                <p>Try adjusting your search or filters</p>
            </div>
        `;
        updateStats(0, 0, 0, 0);
        return;
    }}

    const emailCount = filteredCompanies.filter(c => c.has_email).length;
    const phoneCount = filteredCompanies.filter(c => c.has_phone).length;
    const bothCount = filteredCompanies.filter(c => c.has_email && c.has_phone).length;
    updateStats(filteredCompanies.length, emailCount, phoneCount, bothCount);

    resultsDiv.innerHTML = filteredCompanies.map(company => {{
        const badges = [];
        if (company.has_email && company.has_phone) {{
            badges.push('<span class="badge badge-both">Email + Phone</span>');
        }} else if (company.has_email) {{
            badges.push('<span class="badge badge-email">Email</span>');
        }} else if (company.has_phone) {{
            badges.push('<span class="badge badge-phone">Phone</span>');
        }}

        const naicsCodes = company.naics ? company.naics.split(',').map(code => {{
            const trimmedCode = code.trim();
            const description = naicsDescriptions[trimmedCode] || trimmedCode;
            return `<span class="naics-code" title="${{description}}">${{trimmedCode}}</span>`;
        }}).join('') : '';

        return `
            <div class="company-card">
                <div class="company-name">
                    ${{company.company}}
                    ${{badges.join('')}}
                </div>
                <div class="company-details">
                    ${{company.sblo_name ? `
                        <div class="detail">
                            <div class="detail-label">SBLO Contact</div>
                            <div class="detail-value">${{company.sblo_name}}</div>
                        </div>
                    ` : ''}}
                    ${{company.email ? `
                        <div class="detail">
                            <div class="detail-label">Email</div>
                            <div class="detail-value"><a href="mailto:${{company.email}}">${{company.email}}</a></div>
                        </div>
                    ` : ''}}
                    ${{company.phone ? `
                        <div class="detail">
                            <div class="detail-label">Phone</div>
                            <div class="detail-value"><a href="tel:${{company.phone}}">${{company.phone}}</a></div>
                        </div>
                    ` : ''}}
                    ${{company.address ? `
                        <div class="detail">
                            <div class="detail-label">Address</div>
                            <div class="detail-value">${{company.address}}</div>
                        </div>
                    ` : ''}}
                    ${{company.source ? `
                        <div class="detail">
                            <div class="detail-label">Source</div>
                            <div class="detail-value">${{company.source}}</div>
                        </div>
                    ` : ''}}
                    ${{naicsCodes ? `
                        <div class="detail">
                            <div class="detail-label">NAICS Codes</div>
                            <div class="naics-list">${{naicsCodes}}</div>
                        </div>
                    ` : ''}}
                </div>
            </div>
        `;
    }}).join('');
}}

// Update stats
function updateStats(total, email, phone, both) {{
    document.getElementById('totalCount').textContent = total;
    document.getElementById('emailCount').textContent = email;
    document.getElementById('phoneCount').textContent = phone;
    document.getElementById('bothCount').textContent = both;
}}

// Export to CSV
function exportResults() {{
    const csvContent = [
        ['Company', 'SBLO Name', 'Title', 'Email', 'Phone', 'Address', 'NAICS', 'Source'],
        ...filteredCompanies.map(c => [
            c.company,
            c.sblo_name,
            c.title,
            c.email,
            c.phone,
            c.address,
            c.naics,
            c.source
        ])
    ].map(row => row.map(cell => `"${{cell}}"`).join(',')).join('\\n');

    const blob = new Blob([csvContent], {{ type: 'text/csv' }});
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `federal-contractors-${{new Date().toISOString().split('T')[0]}}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}}

// Event listeners
document.getElementById('searchBox').addEventListener('input', filterCompanies);
document.getElementById('contactFilter').addEventListener('change', filterCompanies);
document.getElementById('sourceFilter').addEventListener('change', filterCompanies);

// Initial render
filterCompanies();
</script>

</body>
</html>'''

# Write output
output_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-DATABASE-SEARCHABLE.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("=" * 80)
print("SEARCHABLE DATABASE CREATED")
print("=" * 80)
print(f"\n✅ Created searchable web database")
print(f"📊 Total companies: {len(companies)}")
print(f"📄 File: {output_file}")
print(f"\n🎯 FEATURES:")
print(f"   • Real-time search (company, SBLO, email, NAICS)")
print(f"   • Filter by contact type (email/phone/both/none)")
print(f"   • Filter by source")
print(f"   • Export filtered results to CSV")
print(f"   • Interactive cards with hover effects")
print(f"   • NAICS code tooltips")
print(f"   • Click-to-call phone numbers")
print(f"   • Click-to-email addresses")
print(f"\n📝 TO USE:")
print(f"   • Open in any web browser")
print(f"   • Works 100% offline (no server needed)")
print(f"   • Can be hosted on any web server")
print("\n" + "=" * 80)
