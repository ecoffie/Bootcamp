#!/usr/bin/env python3
"""
Regenerate the GOVCON-GIANTS-CONTRACTOR-DATABASE.html with vendor portal links.
This script reads the CSV data and generates an updated HTML file with clickable
supplier portal links.
"""

import csv
import json

def read_csv_data():
    """Read the contractor database CSV file."""
    companies = []
    with open('FEDERAL-CONTRACTOR-MASTER-DATABASE.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse contract value
            contract_value = row.get('total_contract_value', '0')
            try:
                contract_value_num = float(contract_value) if contract_value else 0
            except:
                contract_value_num = 0

            # Determine contact info flags
            email = row.get('email', '').strip()
            phone = row.get('phone', '').strip()
            has_email = bool(email and '@' in email)
            has_phone = bool(phone and len(phone) > 5)
            has_contact = has_email or has_phone

            company = {
                'company': row.get('company', ''),
                'sblo_name': row.get('sblo_name', ''),
                'title': row.get('title', ''),
                'email': email,
                'phone': phone,
                'address': row.get('address', ''),
                'naics': row.get('naics', ''),
                'source': row.get('source', ''),
                'contract_count': row.get('contract_count', ''),
                'total_contract_value': contract_value,
                'agencies': row.get('agencies', ''),
                'has_subcontract_plan': row.get('has_subcontract_plan', ''),
                'has_email': has_email,
                'has_phone': has_phone,
                'has_contact': has_contact,
                'contract_value_num': contract_value_num,
                # New vendor portal fields
                'vendor_registration_url': row.get('vendor_registration_url', '').strip(),
                'vendor_portal_type': row.get('vendor_portal_type', '').strip(),
                'vendor_portal_notes': row.get('vendor_portal_notes', '').strip()
            }
            companies.append(company)

    return companies

def generate_html(companies):
    """Generate the complete HTML file with vendor portal links."""

    # Sort by contract value descending
    companies.sort(key=lambda x: x['contract_value_num'], reverse=True)

    # Convert to JSON for embedding
    companies_json = json.dumps(companies, indent=2)

    # Count stats
    total_value = sum(c['contract_value_num'] for c in companies)
    portal_count = sum(1 for c in companies if c['vendor_registration_url'])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Federal Contractor Database | Free Tool for GovCon Giants Community</title>
    <meta name="description" content="Free searchable database of {len(companies):,} federal contractors with ${total_value/1e9:.1f}B in contract data. Perfect companion tool for GovCon Giants members.">
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

        .govcon-banner {{
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
            color: white;
            padding: 15px 30px;
            text-align: center;
            font-size: 14px;
            font-weight: 600;
            border-radius: 12px 12px 0 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .govcon-banner a {{
            color: white;
            text-decoration: underline;
            font-weight: 700;
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
            padding: 40px 30px 30px;
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
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            font-size: 15px;
            opacity: 0.85;
            font-style: italic;
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

        .info-bar {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 15px 30px;
            margin: 20px 30px;
            border-radius: 8px;
        }}

        .info-bar strong {{
            color: #92400e;
        }}

        .info-bar a {{
            color: #1e3a8a;
            font-weight: 600;
            text-decoration: none;
        }}

        .info-bar a:hover {{
            text-decoration: underline;
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
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
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
            font-size: 28px;
            font-weight: 800;
            background: linear-gradient(135deg, #1e3a8a, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stat-label {{
            font-size: 10px;
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

        .company-card.has-portal {{
            border-left: 4px solid #10b981;
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

        .badge-portal {{
            background: #d1fae5;
            color: #065f46;
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

        .portal-link {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, #059669 0%, #10b981 100%);
            color: white !important;
            padding: 10px 18px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            text-decoration: none !important;
            transition: all 0.3s;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
        }}

        .portal-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }}

        .portal-notes {{
            font-size: 12px;
            color: #64748b;
            margin-top: 8px;
            font-style: italic;
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

        .footer {{
            background: #f8fafc;
            padding: 30px;
            text-align: center;
            border-top: 2px solid #e2e8f0;
        }}

        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}

        .footer-link {{
            color: #1e3a8a;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
        }}

        .footer-link:hover {{
            color: #7c3aed;
            text-decoration: underline;
        }}

        .footer-note {{
            font-size: 13px;
            color: #64748b;
            margin-top: 15px;
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
    <div class="govcon-banner">
        Free Tool for <a href="https://govcongiants.org" target="_blank">GovCon Giants</a> Community Members | Find Your Perfect Prime Contractor Partner
    </div>

    <div class="header">
        <h1>Federal Contractor Database</h1>
        <p>Complete directory of {len(companies):,} prime contractors with contract data</p>
        <div class="subtitle">A complementary tool for GovCon Giants members to research and connect with prime contractors</div>
        <div class="value-badge">${total_value/1e9:.1f} Billion in Total Contracts | {portal_count} Supplier Portals</div>
    </div>

    <div class="info-bar">
        <strong>Pro Tip:</strong> Companies with a green left border have direct supplier portal links - click "Register as Supplier" to go straight to their vendor registration!
    </div>

    <div class="controls">
        <input type="text" id="searchBox" class="search-box" placeholder="Search by company, agency, NAICS code, or contact info...">

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
                <label>Supplier Portal</label>
                <select id="portalFilter">
                    <option value="all">All</option>
                    <option value="has_portal">Has Portal Link</option>
                    <option value="no_portal">No Portal Link</option>
                </select>
            </div>

            <div class="filter-group">
                <label>Subcontract Plan</label>
                <select id="subcontractFilter">
                    <option value="all">All</option>
                    <option value="yes">Has Plan (Required to Work w/ Small Business)</option>
                    <option value="no">No Plan</option>
                </select>
            </div>

            <div class="filter-group">
                <label>Contract Size</label>
                <select id="sizeFilter">
                    <option value="all">All Sizes</option>
                    <option value="mega">$10B+ (Mega Primes)</option>
                    <option value="large">$1B-$10B (Large Primes)</option>
                    <option value="medium">$100M-$1B (Mid-Tier)</option>
                    <option value="small">$10M-$100M (Small Primes)</option>
                    <option value="micro">Under $10M</option>
                </select>
            </div>

            <div class="filter-group">
                <label>Export</label>
                <button class="export-btn" onclick="exportResults()">Export CSV</button>
            </div>
        </div>
    </div>

    <div class="stats">
        <div class="stat">
            <div class="stat-number" id="totalCount">0</div>
            <div class="stat-label">Results</div>
        </div>
        <div class="stat">
            <div class="stat-number" id="portalCount">0</div>
            <div class="stat-label">With Portals</div>
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

    <div class="footer">
        <div class="footer-links">
            <a href="https://govcongiants.org" target="_blank" class="footer-link">GovCon Giants Home</a>
            <a href="https://govcongiants.org" target="_blank" class="footer-link">Training & Resources</a>
            <a href="https://govcongiants.org" target="_blank" class="footer-link">Join the Community</a>
        </div>
        <div class="footer-note">
            This is a free complementary tool for the GovCon Giants community.<br>
            For expert mentorship, training, and AI-powered opportunity matching, visit <a href="https://govcongiants.org" target="_blank" style="color: #1e3a8a; font-weight: 600;">GovConGiants.org</a>
        </div>
    </div>
</div>

<script>
const companies = {companies_json};

const naicsDescriptions = {{
    "541511": "Custom Computer Programming",
    "541512": "Computer Systems Design",
    "541519": "Other Computer Related Services",
    "541330": "Engineering Services",
    "541611": "Administrative Management Consulting",
    "541612": "Human Resources Consulting",
    "541613": "Marketing Consulting",
    "541614": "Process & Logistics Consulting",
    "541618": "Other Management Consulting",
    "541690": "Other Scientific & Technical Consulting",
    "541712": "R&D in Physical Sciences",
    "541713": "R&D in Nanotechnology",
    "541714": "R&D in Biotechnology",
    "541715": "R&D in Physical, Engineering & Life Sciences",
    "541990": "All Other Professional Services",
    "518210": "Data Processing & Hosting",
    "511210": "Software Publishers",
    "513210": "Telecommunications",
    "561210": "Facilities Support Services",
    "561611": "Investigation Services",
    "561612": "Security Guards",
    "561613": "Armored Car Services",
    "336411": "Aircraft Manufacturing",
    "336412": "Aircraft Engine Manufacturing",
    "336413": "Aerospace Parts Manufacturing",
    "336414": "Guided Missile Manufacturing",
    "336419": "Other Aerospace Parts",
    "336611": "Ship Building & Repairing",
    "332993": "Ammunition Manufacturing",
    "332994": "Small Arms Manufacturing",
    "334511": "Search & Navigation Equipment",
    "334220": "Radio & TV Broadcasting Equipment"
}};

let filteredCompanies = [...companies];

function formatCurrency(value) {{
    const num = parseFloat(value) || 0;
    if (num >= 1e9) return '$' + (num / 1e9).toFixed(1) + 'B';
    if (num >= 1e6) return '$' + (num / 1e6).toFixed(1) + 'M';
    if (num >= 1e3) return '$' + (num / 1e3).toFixed(0) + 'K';
    return '$' + num.toFixed(0);
}}

function filterCompanies() {{
    const search = document.getElementById('searchBox').value.toLowerCase();
    const contactFilter = document.getElementById('contactFilter').value;
    const portalFilter = document.getElementById('portalFilter').value;
    const subcontractFilter = document.getElementById('subcontractFilter').value;
    const sizeFilter = document.getElementById('sizeFilter').value;

    filteredCompanies = companies.filter(company => {{
        // Search filter
        if (search) {{
            const searchFields = [
                company.company, company.sblo_name, company.email,
                company.phone, company.naics, company.agencies,
                company.vendor_portal_notes
            ].join(' ').toLowerCase();
            if (!searchFields.includes(search)) return false;
        }}

        // Contact filter
        if (contactFilter === 'with_contact' && !company.has_contact) return false;
        if (contactFilter === 'email' && !company.has_email) return false;
        if (contactFilter === 'phone' && !company.has_phone) return false;
        if (contactFilter === 'both' && (!company.has_email || !company.has_phone)) return false;
        if (contactFilter === 'no_contact' && company.has_contact) return false;

        // Portal filter
        if (portalFilter === 'has_portal' && !company.vendor_registration_url) return false;
        if (portalFilter === 'no_portal' && company.vendor_registration_url) return false;

        // Subcontract filter
        if (subcontractFilter === 'yes' && company.has_subcontract_plan !== 'True') return false;
        if (subcontractFilter === 'no' && company.has_subcontract_plan === 'True') return false;

        // Size filter
        const value = company.contract_value_num;
        if (sizeFilter === 'mega' && value < 10e9) return false;
        if (sizeFilter === 'large' && (value < 1e9 || value >= 10e9)) return false;
        if (sizeFilter === 'medium' && (value < 100e6 || value >= 1e9)) return false;
        if (sizeFilter === 'small' && (value < 10e6 || value >= 100e6)) return false;
        if (sizeFilter === 'micro' && value >= 10e6) return false;

        return true;
    }});

    renderResults();
}}

function renderResults() {{
    const resultsDiv = document.getElementById('results');

    if (filteredCompanies.length === 0) {{
        resultsDiv.innerHTML = `
            <div class="no-results">
                <div class="no-results-icon">Search</div>
                <h2>No companies found</h2>
                <p>Try adjusting your search or filters</p>
            </div>
        `;
        updateStats(0, 0, 0, 0, 0, 0);
        return;
    }}

    const portalCount = filteredCompanies.filter(c => c.vendor_registration_url).length;
    const contactCount = filteredCompanies.filter(c => c.has_contact).length;
    const emailCount = filteredCompanies.filter(c => c.has_email).length;
    const phoneCount = filteredCompanies.filter(c => c.has_phone).length;
    const totalValue = filteredCompanies.reduce((sum, c) => sum + c.contract_value_num, 0);

    updateStats(filteredCompanies.length, portalCount, contactCount, emailCount, phoneCount, totalValue);

    resultsDiv.innerHTML = filteredCompanies.map(company => {{
        const badges = [];

        // Portal badge first (most important)
        if (company.vendor_registration_url) {{
            badges.push('<span class="badge badge-portal">Supplier Portal</span>');
        }}

        if (company.has_email && company.has_phone) {{
            badges.push('<span class="badge badge-both">Email + Phone</span>');
        }} else if (company.has_email) {{
            badges.push('<span class="badge badge-email">Email</span>');
        }} else if (company.has_phone) {{
            badges.push('<span class="badge badge-phone">Phone</span>');
        }}

        if (company.has_subcontract_plan === 'True') {{
            badges.push('<span class="badge badge-subcontract">Subcontract Plan</span>');
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

        // Portal link section
        let portalSection = '';
        if (company.vendor_registration_url) {{
            portalSection = `
                <div class="detail" style="grid-column: 1 / -1;">
                    <div class="detail-label">Supplier Registration Portal</div>
                    <div class="detail-value">
                        <a href="${{company.vendor_registration_url}}" target="_blank" rel="noopener noreferrer" class="portal-link">
                            Register as Supplier →
                        </a>
                        ${{company.vendor_portal_notes ? `<div class="portal-notes">${{company.vendor_portal_notes}}</div>` : ''}}
                    </div>
                </div>
            `;
        }}

        const hasPortalClass = company.vendor_registration_url ? 'has-portal' : '';

        return `
            <div class="company-card ${{hasPortalClass}}">
                <div class="company-header">
                    <div class="company-name">${{company.company}}</div>
                    ${{company.total_contract_value ? `<div class="contract-badge">${{formatCurrency(company.total_contract_value)}}</div>` : ''}}
                </div>
                <div class="company-meta">
                    ${{badges.join('')}}
                </div>
                <div class="company-details">
                    ${{portalSection}}
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

function updateStats(total, portal, contact, email, phone, value) {{
    document.getElementById('totalCount').textContent = total.toLocaleString();
    document.getElementById('portalCount').textContent = portal.toLocaleString();
    document.getElementById('contactCount').textContent = contact.toLocaleString();
    document.getElementById('emailCount').textContent = email.toLocaleString();
    document.getElementById('phoneCount').textContent = phone.toLocaleString();
    document.getElementById('valueCount').textContent = formatCurrency(value);
}}

function exportResults() {{
    const csvContent = [
        ['Company', 'SBLO Name', 'Title', 'Email', 'Phone', 'Address', 'NAICS', 'Source', 'Contracts', 'Contract Value', 'Agencies', 'Has Subcontract Plan', 'Vendor Portal URL', 'Portal Type', 'Portal Notes'],
        ...filteredCompanies.map(c => [
            c.company, c.sblo_name, c.title, c.email, c.phone, c.address,
            c.naics, c.source, c.contract_count, c.total_contract_value,
            c.agencies, c.has_subcontract_plan, c.vendor_registration_url,
            c.vendor_portal_type, c.vendor_portal_notes
        ])
    ].map(row => row.map(cell => `"${{cell || ''}}"`).join(',')).join('\\n');

    const blob = new Blob([csvContent], {{ type: 'text/csv' }});
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `federal-contractors-govcon-giants-${{new Date().toISOString().split('T')[0]}}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
}}

document.getElementById('searchBox').addEventListener('input', filterCompanies);
document.getElementById('contactFilter').addEventListener('change', filterCompanies);
document.getElementById('portalFilter').addEventListener('change', filterCompanies);
document.getElementById('subcontractFilter').addEventListener('change', filterCompanies);
document.getElementById('sizeFilter').addEventListener('change', filterCompanies);

filterCompanies();
</script>

</body>
</html>'''

    return html

def main():
    print("Reading contractor database...")
    companies = read_csv_data()
    print(f"Loaded {len(companies)} companies")

    portal_count = sum(1 for c in companies if c['vendor_registration_url'])
    print(f"Companies with portal links: {portal_count}")

    print("Generating HTML with portal links...")
    html = generate_html(companies)

    output_file = 'GOVCON-GIANTS-CONTRACTOR-DATABASE.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Successfully generated {output_file}")
    print(f"Total companies: {len(companies)}")
    print(f"Companies with portal links: {portal_count}")

if __name__ == '__main__':
    main()
