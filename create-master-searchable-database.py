#!/usr/bin/env python3
"""
Create comprehensive searchable database from master database
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
    '335931': 'Current-Carrying Wiring Device Manufacturing',
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

# Read master database
csv_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
companies = []

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        company_name = row.get('company', '').strip()
        if not company_name:
            continue

        email = row.get('email', '').strip()
        phone = row.get('phone', '').strip()
        contract_value = row.get('total_contract_value', '').strip()

        companies.append({
            'company': company_name,
            'sblo_name': row.get('sblo_name', '').strip(),
            'title': row.get('title', '').strip(),
            'email': email,
            'phone': phone,
            'address': row.get('address', '').strip(),
            'naics': row.get('naics', '').strip(),
            'source': row.get('source', '').strip(),
            'contract_count': row.get('contract_count', '').strip(),
            'total_contract_value': contract_value,
            'agencies': row.get('agencies', '').strip(),
            'has_subcontract_plan': row.get('has_subcontract_plan', '').strip(),
            'has_email': bool(email),
            'has_phone': bool(phone),
            'has_contact': bool(email or phone),
            'contract_value_num': float(contract_value) if contract_value else 0
        })

print(f"Loaded {len(companies)} companies")

# Convert to JSON
companies_json = json.dumps(companies, indent=2)
naics_json = json.dumps(NAICS_DESCRIPTIONS, indent=2)

# Format large numbers
def format_currency(value):
    if not value:
        return ''
    try:
        num = float(value)
        if num >= 1_000_000_000:
            return f'${num/1_000_000_000:.1f}B'
        elif num >= 1_000_000:
            return f'${num/1_000_000:.1f}M'
        elif num >= 1_000:
            return f'${num/1_000:.1f}K'
        else:
            return f'${num:.0f}'
    except:
        return value

# Create HTML
html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Federal Contractor Master Database - 2,768 Companies</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.4);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 38px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .header p {{
            font-size: 18px;
            opacity: 0.95;
        }}

        .header .value-badge {{
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 20px;
            margin-top: 15px;
            font-size: 16px;
            font-weight: 600;
        }}

        .controls {{
            padding: 30px;
            background: #f8fafc;
            border-bottom: 3px solid #e2e8f0;
        }}

        .search-box {{
            width: 100%;
            padding: 18px 24px;
            font-size: 17px;
            border: 3px solid #cbd5e0;
            border-radius: 12px;
            margin-bottom: 20px;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}

        .search-box:focus {{
            outline: none;
            border-color: #7c3aed;
            box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.1);
        }}

        .filters {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}

        .filter-group {{
            display: flex;
            flex-direction: column;
        }}

        .filter-group label {{
            font-size: 11px;
            font-weight: 700;
            color: #475569;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }}

        .filter-group select {{
            padding: 12px;
            border: 2px solid #cbd5e0;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            cursor: pointer;
            transition: all 0.2s;
        }}

        .filter-group select:hover {{
            border-color: #7c3aed;
        }}

        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 15px;
            padding: 25px 30px;
            background: linear-gradient(to bottom, white, #f8fafc);
            border-bottom: 2px solid #e2e8f0;
        }}

        .stat {{
            text-align: center;
            padding: 10px;
        }}

        .stat-number {{
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, #1e3a8a, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stat-label {{
            font-size: 11px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 6px;
            font-weight: 600;
        }}

        .results {{
            padding: 30px;
            max-height: 700px;
            overflow-y: auto;
            background: #fafbfc;
        }}

        .company-card {{
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 18px;
            transition: all 0.3s;
            position: relative;
        }}

        .company-card:hover {{
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            transform: translateY(-3px);
            border-color: #7c3aed;
        }}

        .company-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }}

        .company-name {{
            font-size: 22px;
            font-weight: 800;
            color: #1e293b;
            flex: 1;
        }}

        .contract-badge {{
            background: linear-gradient(135deg, #1e3a8a, #7c3aed);
            color: white;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            white-space: nowrap;
            margin-left: 15px;
        }}

        .company-meta {{
            display: flex;
            gap: 10px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }}

        .company-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 18px;
            margin-top: 18px;
            padding-top: 18px;
            border-top: 1px solid #e2e8f0;
        }}

        .detail {{
            display: flex;
            flex-direction: column;
        }}

        .detail-label {{
            font-size: 10px;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
        }}

        .detail-value {{
            font-size: 14px;
            color: #1e293b;
            word-break: break-word;
            line-height: 1.5;
        }}

        .detail-value a {{
            color: #7c3aed;
            text-decoration: none;
            font-weight: 600;
        }}

        .detail-value a:hover {{
            text-decoration: underline;
        }}

        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}

        .badge-email {{
            background: #dbeafe;
            color: #1e40af;
        }}

        .badge-phone {{
            background: #d1fae5;
            color: #065f46;
        }}

        .badge-both {{
            background: #fce7f3;
            color: #9f1239;
        }}

        .badge-subcontract {{
            background: #fef3c7;
            color: #92400e;
        }}

        .agency-tag {{
            display: inline-block;
            background: #f1f5f9;
            color: #475569;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            margin: 3px 3px 0 0;
        }}

        .naics-code {{
            background: #ede9fe;
            color: #5b21b6;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-family: 'Courier New', monospace;
            display: inline-block;
            margin: 3px 3px 0 0;
            font-weight: 600;
        }}

        .no-results {{
            text-align: center;
            padding: 80px 20px;
            color: #64748b;
        }}

        .no-results-icon {{
            font-size: 72px;
            margin-bottom: 24px;
        }}

        .export-btn {{
            background: linear-gradient(135deg, #1e3a8a, #7c3aed);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .export-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(124, 58, 237, 0.4);
        }}

        ::-webkit-scrollbar {{
            width: 12px;
        }}

        ::-webkit-scrollbar-track {{
            background: #f1f5f9;
        }}

        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(135deg, #1e3a8a, #7c3aed);
            border-radius: 6px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(135deg, #1e40af, #6d28d9);
        }}
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>🇺🇸 Federal Contractor Master Database</h1>
        <p>Complete directory of 2,768 prime contractors with contract data</p>
        <div class="value-badge">$479.9 Billion in Total Contracts</div>
    </div>

    <div class="controls">
        <input type="text" id="searchBox" class="search-box" placeholder="🔍 Search by company, agency, NAICS code, or contact info...">

        <div class="filters">
            <div class="filter-group">
                <label>Contact Info</label>
                <select id="contactFilter">
                    <option value="all">All Companies</option>
                    <option value="with_contact">Has Contact Info</option>
                    <option value="email">Has Email</option>
                    <option value="phone">Has Phone</option>
                    <option value="both">Has Both</option>
                    <option value="no_contact">No Contact Info</option>
                </select>
            </div>

            <div class="filter-group">
                <label>Subcontract Plan</label>
                <select id="subcontractFilter">
                    <option value="all">All</option>
                    <option value="yes">Has Plan</option>
                    <option value="no">No Plan</option>
                </select>
            </div>

            <div class="filter-group">
                <label>Contract Size</label>
                <select id="sizeFilter">
                    <option value="all">All Sizes</option>
                    <option value="mega">$10B+ (Mega)</option>
                    <option value="large">$1B-$10B</option>
                    <option value="medium">$100M-$1B</option>
                    <option value="small">$10M-$100M</option>
                    <option value="micro">Under $10M</option>
                </select>
            </div>

            <div class="filter-group">
                <label>Export</label>
                <button class="export-btn" onclick="exportResults()">📥 Export CSV</button>
            </div>
        </div>
    </div>

    <div class="stats">
        <div class="stat">
            <div class="stat-number" id="totalCount">0</div>
            <div class="stat-label">Results</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="contactCount">0</div>
            <div class="stat-label">With Contacts</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="emailCount">0</div>
            <div class="stat-label">Emails</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="phoneCount">0</div>
            <div class="stat-label">Phones</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="valueCount">$0</div>
            <div class="stat-label">Total Value</div>
        </div>
    </div>

    <div class="results" id="results"></div>
</div>

<script>
const companies = {companies_json};
const naicsDescriptions = {naics_json};

let filteredCompanies = [...companies];

function formatCurrency(value) {{
    if (!value) return '';
    const num = parseFloat(value);
    if (num >= 1e9) return `$` + (num/1e9).toFixed(1) + 'B';
    if (num >= 1e6) return `$` + (num/1e6).toFixed(1) + 'M';
    if (num >= 1e3) return `$` + (num/1e3).toFixed(1) + 'K';
    return `$` + num.toFixed(0);
}}

function filterCompanies() {{
    const searchTerm = document.getElementById('searchBox').value.toLowerCase();
    const contactFilter = document.getElementById('contactFilter').value;
    const subcontractFilter = document.getElementById('subcontractFilter').value;
    const sizeFilter = document.getElementById('sizeFilter').value;

    filteredCompanies = companies.filter(company => {{
        const matchesSearch =
            company.company.toLowerCase().includes(searchTerm) ||
            company.sblo_name.toLowerCase().includes(searchTerm) ||
            company.email.toLowerCase().includes(searchTerm) ||
            company.naics.toLowerCase().includes(searchTerm) ||
            company.agencies.toLowerCase().includes(searchTerm);

        let matchesContact = true;
        if (contactFilter === 'with_contact') matchesContact = company.has_contact;
        else if (contactFilter === 'email') matchesContact = company.has_email;
        else if (contactFilter === 'phone') matchesContact = company.has_phone;
        else if (contactFilter === 'both') matchesContact = company.has_email && company.has_phone;
        else if (contactFilter === 'no_contact') matchesContact = !company.has_contact;

        let matchesSubcontract = true;
        if (subcontractFilter === 'yes') matchesSubcontract = company.has_subcontract_plan === 'True';
        else if (subcontractFilter === 'no') matchesSubcontract = company.has_subcontract_plan !== 'True';

        let matchesSize = true;
        const value = company.contract_value_num;
        if (sizeFilter === 'mega') matchesSize = value >= 10e9;
        else if (sizeFilter === 'large') matchesSize = value >= 1e9 && value < 10e9;
        else if (sizeFilter === 'medium') matchesSize = value >= 100e6 && value < 1e9;
        else if (sizeFilter === 'small') matchesSize = value >= 10e6 && value < 100e6;
        else if (sizeFilter === 'micro') matchesSize = value < 10e6;

        return matchesSearch && matchesContact && matchesSubcontract && matchesSize;
    }});

    renderResults();
}}

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
        updateStats(0, 0, 0, 0, 0);
        return;
    }}

    const contactCount = filteredCompanies.filter(c => c.has_contact).length;
    const emailCount = filteredCompanies.filter(c => c.has_email).length;
    const phoneCount = filteredCompanies.filter(c => c.has_phone).length;
    const totalValue = filteredCompanies.reduce((sum, c) => sum + c.contract_value_num, 0);

    updateStats(filteredCompanies.length, contactCount, emailCount, phoneCount, totalValue);

    resultsDiv.innerHTML = filteredCompanies.map(company => {{
        const badges = [];
        if (company.has_email && company.has_phone) {{
            badges.push('<span class="badge badge-both">✉️ + 📱</span>');
        }} else if (company.has_email) {{
            badges.push('<span class="badge badge-email">✉️ Email</span>');
        }} else if (company.has_phone) {{
            badges.push('<span class="badge badge-phone">📱 Phone</span>');
        }}

        if (company.has_subcontract_plan === 'True') {{
            badges.push('<span class="badge badge-subcontract">📋 Subcontract Plan</span>');
        }}

        const agencies = company.agencies ? company.agencies.split(',').slice(0, 3).map(a =>
            `<span class="agency-tag">${{a.trim()}}</span>`
        ).join('') : '';

        const moreAgencies = company.agencies ? company.agencies.split(',').length - 3 : 0;

        const naicsCodes = company.naics ? company.naics.split(',').slice(0, 5).map(code => {{
            const trimmedCode = code.trim();
            const description = naicsDescriptions[trimmedCode] || trimmedCode;
            return `<span class="naics-code" title="${{description}}">${{trimmedCode}}</span>`;
        }}).join('') : '';

        const moreNaics = company.naics ? Math.max(0, company.naics.split(',').length - 5) : 0;

        return `
            <div class="company-card">
                <div class="company-header">
                    <div class="company-name">${{company.company}}</div>
                    ${{company.total_contract_value ? `<div class="contract-badge">${{formatCurrency(company.total_contract_value)}}</div>` : ''}}
                </div>
                <div class="company-meta">
                    ${{badges.join('')}}
                </div>
                <div class="company-details">
                    ${{company.contract_count ? `
                        <div class="detail">
                            <div class="detail-label">Contracts</div>
                            <div class="detail-value">${{company.contract_count}} contracts</div>
                        </div>
                    ` : ''}}
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
                    ${{agencies ? `
                        <div class="detail">
                            <div class="detail-label">Primary Agencies</div>
                            <div class="detail-value">
                                ${{agencies}}
                                ${{moreAgencies > 0 ? `<span class="agency-tag">+${{moreAgencies}} more</span>` : ''}}
                            </div>
                        </div>
                    ` : ''}}
                    ${{naicsCodes ? `
                        <div class="detail">
                            <div class="detail-label">NAICS Codes</div>
                            <div class="detail-value">
                                ${{naicsCodes}}
                                ${{moreNaics > 0 ? `<span class="naics-code">+${{moreNaics}}</span>` : ''}}
                            </div>
                        </div>
                    ` : ''}}
                </div>
            </div>
        `;
    }}).join('');
}}

function updateStats(total, contact, email, phone, value) {{
    document.getElementById('totalCount').textContent = total.toLocaleString();
    document.getElementById('contactCount').textContent = contact.toLocaleString();
    document.getElementById('emailCount').textContent = email.toLocaleString();
    document.getElementById('phoneCount').textContent = phone.toLocaleString();
    document.getElementById('valueCount').textContent = formatCurrency(value);
}}

function exportResults() {{
    const csvContent = [
        ['Company', 'SBLO Name', 'Title', 'Email', 'Phone', 'Address', 'NAICS', 'Source', 'Contracts', 'Contract Value', 'Agencies', 'Has Subcontract Plan'],
        ...filteredCompanies.map(c => [
            c.company, c.sblo_name, c.title, c.email, c.phone, c.address,
            c.naics, c.source, c.contract_count, c.total_contract_value,
            c.agencies, c.has_subcontract_plan
        ])
    ].map(row => row.map(cell => `"${{cell}}"`).join(',')).join('\\n');

    const blob = new Blob([csvContent], {{ type: 'text/csv' }});
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `federal-contractors-master-${{new Date().toISOString().split('T')[0]}}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}}

document.getElementById('searchBox').addEventListener('input', filterCompanies);
document.getElementById('contactFilter').addEventListener('change', filterCompanies);
document.getElementById('subcontractFilter').addEventListener('change', filterCompanies);
document.getElementById('sizeFilter').addEventListener('change', filterCompanies);

filterCompanies();
</script>

</body>
</html>'''

# Write output
output_file = '/Users/ericcoffie/Bootcamp/FEDERAL-CONTRACTOR-MASTER-DATABASE-SEARCHABLE.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("=" * 80)
print("MASTER SEARCHABLE DATABASE CREATED")
print("=" * 80)
print(f"\n✅ Created comprehensive searchable database")
print(f"📊 Total companies: {len(companies):,}")
print(f"📄 File: {output_file}")
print(f"\n🎯 PREMIUM FEATURES:")
print(f"   • 2,768 federal contractors")
print(f"   • $479.9B in contract data")
print(f"   • Search by company, agency, NAICS, contact")
print(f"   • Filter by contact availability")
print(f"   • Filter by subcontract plan")
print(f"   • Filter by contract size ($10M-$10B+)")
print(f"   • Beautiful card UI with gradients")
print(f"   • Real-time statistics")
print(f"   • Export to CSV")
print(f"   • Works 100% offline")
print("\n" + "=" * 80)
