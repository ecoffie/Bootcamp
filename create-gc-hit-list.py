#!/usr/bin/env python3
"""
Create a General Contractor-only hit list from the contract opportunities CSV
Filtering for construction-related NAICS codes
"""

import csv
from datetime import datetime
import html

def format_date(date_str):
    """Format date string to be more readable"""
    if not date_str or date_str == 'N/A':
        return 'TBD'
    return date_str.strip()

def truncate_text(text, max_length=200):
    """Truncate text to max_length and add ellipsis"""
    if not text:
        return ''
    text = text.strip()
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + '...'

def clean_html(text):
    """Clean HTML entities"""
    if not text:
        return ''
    return html.escape(text)

def get_set_aside_badge(set_aside):
    """Return appropriate badge class based on set-aside type"""
    if not set_aside or set_aside == 'N/A':
        return ''
    
    set_aside_lower = set_aside.lower()
    if 'veteran' in set_aside_lower or 'sdvosb' in set_aside_lower:
        return 'badge-set-aside badge-veteran'
    elif '8(a)' in set_aside_lower:
        return 'badge-set-aside badge-8a'
    elif 'hubzone' in set_aside_lower:
        return 'badge-set-aside badge-hubzone'
    elif 'wosb' in set_aside_lower or 'women' in set_aside_lower:
        return 'badge-set-aside badge-wosb'
    elif 'small business' in set_aside_lower:
        return 'badge-set-aside badge-sb'
    return 'badge-set-aside'

def is_construction_related(opp):
    """Check if opportunity is construction-related"""
    title = (opp.get('Title', '') or '').lower()
    description = (opp.get('Description', '') or '').lower()
    naics = (opp.get('NAICS', '') or '').lower()
    
    # Construction keywords
    construction_keywords = [
        'construction', 'building', 'renovation', 'renovate', 'repair', 'alteration',
        'electrical', 'plumbing', 'hvac', 'roof', 'roofing', 'sprinkler', 'fire alarm',
        'electrical', 'switchgear', 'transformer', 'facility', 'facilities',
        'infrastructure', 'upgrade', 'install', 'demolition', 'demolish',
        'paving', 'parking', 'asphalt', 'concrete', 'structural', 'foundation',
        'framing', 'drywall', 'flooring', 'painting', 'carpentry', 'masonry',
        'tile', 'ceiling', 'windows', 'doors', 'excavation', 'site work',
        'utilities', 'water', 'sewer', 'drainage', 'grading', 'landscaping'
    ]
    
    # Construction-related NAICS codes (partial matches for flexibility)
    construction_naics_patterns = [
        '236',  # Construction of buildings
        '237',  # Heavy and civil engineering construction
        '238',  # Specialty trade contractors
        '561210',  # Facilities support services
        'construction',
        'building',
        'contractor',
        'electrical',
        'plumbing',
        'hvac'
    ]
    
    # Check title and description for construction keywords
    text_to_check = f"{title} {description}"
    has_keyword = any(keyword in text_to_check for keyword in construction_keywords)
    
    # Check NAICS
    has_construction_naics = any(pattern in naics for pattern in construction_naics_patterns)
    
    return has_keyword or has_construction_naics

# Read CSV file
csv_path = '/Users/ericcoffie/Library/CloudStorage/GoogleDrive-evankoffdev@gmail.com/My Drive/Federal Help Center/Dec 13 Surge Event/ContractOpportunities-20251212-092037.csv'

opportunities = []
construction_opportunities = []

# Try different encodings
encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
for encoding in encodings:
    try:
        with open(csv_path, 'r', encoding=encoding, errors='replace') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Only include active opportunities
                if row.get('Active/Inactive', '').lower() == 'active':
                    opportunities.append(row)
                    # Filter for construction
                    if is_construction_related(row):
                        construction_opportunities.append(row)
        print(f"Successfully read CSV with {encoding} encoding")
        break
    except Exception as e:
        continue

print(f"Total active opportunities: {len(opportunities)}")
print(f"Construction-related opportunities: {len(construction_opportunities)}")

# Sort by response date (earliest first)
def sort_key(opp):
    date_str = opp.get('Current Response Date', '')
    if not date_str or date_str == 'N/A':
        return '9999-99-99'
    return date_str

construction_opportunities.sort(key=sort_key)

# Limit to top 25 for GC-focused list
top_opportunities = construction_opportunities[:25]

# Generate HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>December 2025 Hit List - General Contractors</title>
    <style>
        @page {{
            size: letter;
            margin: 0.5in;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #ffffff;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #dc2626 0%, #ea580c 100%);
            color: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 10px;
            font-weight: 800;
        }}

        .header .subtitle {{
            font-size: 1.2rem;
            opacity: 0.95;
            font-weight: 300;
            margin-bottom: 15px;
        }}

        .header .badge {{
            display: inline-block;
            margin-top: 10px;
            padding: 8px 20px;
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 600;
        }}

        .intro {{
            background: #fff7ed;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 35px;
            border-left: 5px solid #ea580c;
        }}

        .intro h2 {{
            color: #9a3412;
            margin-bottom: 15px;
            font-size: 1.5rem;
        }}

        .intro p {{
            font-size: 1rem;
            color: #7c2d12;
            margin-bottom: 10px;
        }}

        .naics-box {{
            background: #fef3c7;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }}

        .naics-box strong {{
            color: #92400e;
            display: block;
            margin-bottom: 10px;
        }}

        .naics-box ul {{
            margin-left: 20px;
            color: #78350f;
        }}

        .hit-list {{
            display: grid;
            gap: 20px;
            margin-bottom: 40px;
        }}

        .opportunity-card {{
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 25px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .opportunity-card::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 5px;
            background: linear-gradient(135deg, #dc2626 0%, #ea580c 100%);
        }}

        .opportunity-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border-color: #ea580c;
        }}

        .opportunity-number {{
            display: inline-block;
            width: 35px;
            height: 35px;
            background: linear-gradient(135deg, #dc2626 0%, #ea580c 100%);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 35px;
            font-weight: 800;
            font-size: 1rem;
            margin-bottom: 15px;
        }}

        .opportunity-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .opportunity-title {{
            font-size: 1.2rem;
            font-weight: 700;
            color: #9a3412;
            flex: 1;
            min-width: 250px;
        }}

        .opportunity-id {{
            font-size: 0.85rem;
            color: #64748b;
            font-family: monospace;
            margin-top: 5px;
        }}

        .opportunity-meta {{
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-bottom: 15px;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9rem;
            color: #4a5568;
        }}

        .meta-item strong {{
            color: #9a3412;
            font-weight: 600;
        }}

        .badge-tag {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 8px;
        }}

        .badge-gc {{
            background: #fee2e2;
            color: #991b1b;
        }}

        .badge-set-aside {{
            background: #fef3c7;
            color: #92400e;
        }}

        .badge-sb {{
            background: #dbeafe;
            color: #1e40af;
        }}

        .badge-8a {{
            background: #e9d5ff;
            color: #6b21a8;
        }}

        .badge-hubzone {{
            background: #fef3c7;
            color: #92400e;
        }}

        .badge-wosb {{
            background: #fce7f3;
            color: #9f1239;
        }}

        .badge-veteran {{
            background: #fed7aa;
            color: #9a3412;
        }}

        .badge-urgent {{
            background: #fee2e2;
            color: #991b1b;
        }}

        .opportunity-details {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
        }}

        .opportunity-details p {{
            margin-bottom: 10px;
            color: #4a5568;
            line-height: 1.7;
            font-size: 0.95rem;
        }}

        .opportunity-details strong {{
            color: #9a3412;
        }}

        .action-box {{
            background: #fff7ed;
            border-left: 4px solid #ea580c;
            padding: 15px;
            margin-top: 15px;
            border-radius: 8px;
            font-size: 0.9rem;
        }}

        .action-box strong {{
            color: #9a3412;
            display: block;
            margin-bottom: 8px;
        }}

        .key-point {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 20px;
            margin: 25px 0;
            border-radius: 8px;
        }}

        .key-point strong {{
            color: #92400e;
        }}

        .footer {{
            text-align: center;
            padding: 30px;
            background: #f8fafc;
            border-radius: 12px;
            margin-top: 40px;
        }}

        .footer p {{
            color: #4a5568;
            font-size: 0.95rem;
            margin-bottom: 8px;
        }}

        @media print {{
            .opportunity-card {{
                page-break-inside: avoid;
            }}
        }}

        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.8rem;
            }}

            .opportunity-header {{
                flex-direction: column;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏗️ December 2025 Hit List</h1>
            <p class="subtitle">Top {len(top_opportunities)} Construction Opportunities for General Contractors</p>
            <p style="font-size: 1rem; margin-top: 10px; opacity: 0.9;">Real Construction Contracts from SAM.gov</p>
            <span class="badge">Response Deadlines: Dec 2025 - Jan 2026</span>
        </div>

        <div class="intro">
            <h2>Perfect for General Contractors</h2>
            <p><strong>✅ Construction projects only</strong> - Building, renovation, electrical, plumbing, HVAC, and more</p>
            <p><strong>✅ Real opportunities</strong> - These are active solicitations accepting bids RIGHT NOW</p>
            <p><strong>✅ Set-asides included</strong> - Many reserved for SDVOSB, 8(a), HUBZone, WOSB, and Small Business</p>
            <p><strong>✅ Response deadlines listed</strong> - Know exactly when to submit your bid</p>
            <p><strong>✅ POC information included</strong> - Contact the right person immediately</p>
            
            <div class="naics-box">
                <strong>📋 Key NAICS Codes for General Contractors:</strong>
                <ul>
                    <li><strong>236220</strong> - Commercial and Institutional Building Construction</li>
                    <li><strong>238210</strong> - Electrical Contractors</li>
                    <li><strong>238220</strong> - Plumbing, Heating, and Air-Conditioning Contractors</li>
                    <li><strong>237110</strong> - Water and Sewer Line Construction</li>
                    <li><strong>561210</strong> - Facilities Support Services</li>
                </ul>
            </div>
        </div>

        <div class="hit-list">
"""

# Add each opportunity
for idx, opp in enumerate(top_opportunities, 1):
    notice_id = clean_html(opp.get('Notice ID', 'N/A'))
    title = clean_html(opp.get('Title', 'No Title'))
    description = truncate_text(clean_html(opp.get('Description', '')))
    response_date = format_date(opp.get('Current Response Date', 'N/A'))
    set_aside = clean_html(opp.get('Set Aside', 'N/A'))
    naics = clean_html(opp.get('NAICS', 'N/A'))
    poc = clean_html(opp.get('POC Information', 'N/A'))
    opp_type = clean_html(opp.get('Contract Opportunity Type', 'N/A'))
    
    # Determine badge class
    badge_class = get_set_aside_badge(set_aside) if set_aside != 'N/A' else ''
    badge_html = f'<span class="badge-tag {badge_class}">{set_aside[:40]}</span>' if set_aside != 'N/A' else ''
    
    # Check if deadline is urgent (within 2 weeks)
    urgent = False
    if response_date and 'Dec' in response_date and '2025' in response_date:
        urgent = True
    
    urgent_badge = '<span class="badge-tag badge-urgent">Urgent Deadline</span>' if urgent else ''
    gc_badge = '<span class="badge-tag badge-gc">GC Opportunity</span>'
    
    html_content += f"""
            <!-- Opportunity {idx} -->
            <div class="opportunity-card">
                <div class="opportunity-number">{idx}</div>
                <div class="opportunity-header">
                    <div>
                        <div class="opportunity-title">{title}</div>
                        <div class="opportunity-id">Notice ID: {notice_id}</div>
                    </div>
                </div>
                <div class="opportunity-meta">
                    <div class="meta-item"><strong>Response Deadline:</strong> {response_date}</div>
                    <div class="meta-item"><strong>Type:</strong> {opp_type}</div>
                    {f'<div class="meta-item"><strong>NAICS:</strong> {naics}</div>' if naics != 'N/A' else ''}
                </div>
                <div>
                    {gc_badge}
                    {badge_html}
                    {urgent_badge}
                </div>
                <div class="opportunity-details">
                    <p><strong>Project Description:</strong> {description}</p>
                    {f'<p><strong>Set-Aside:</strong> {set_aside}</p>' if set_aside != 'N/A' else ''}
                    <div class="action-box">
                        <strong>🏗️ Your Action Items:</strong>
                        1. Review full solicitation on SAM.gov using Notice ID: <strong>{notice_id}</strong><br>
                        2. {f'Contact POC: <strong>{poc}</strong>' if poc != 'N/A' else 'Check SAM.gov for POC information'}<br>
                        3. Check for site visit requirements (common in construction)<br>
                        4. Verify bonding requirements (often needed for construction contracts)<br>
                        5. Ensure you meet set-aside requirements (if applicable)<br>
                        6. Submit bid by <strong>{response_date}</strong>
                    </div>
                </div>
            </div>
"""

html_content += """
        </div>

        <div class="key-point">
            <p><strong>💡 Tips for General Contractors:</strong></p>
            <p>1. <strong>Site visits are critical</strong> - Most construction projects require mandatory site visits. Plan ahead!</p>
            <p>2. <strong>Bonding requirements</strong> - Many construction contracts require bid bonds, performance bonds, and payment bonds. Have your bonding capacity ready.</p>
            <p>3. <strong>Check NAICS codes</strong> - Make sure your business is registered with the correct NAICS codes in SAM.gov</p>
            <p>4. <strong>Licensing matters</strong> - Verify state/local licensing requirements for the project location</p>
            <p>5. <strong>Set-asides advantage</strong> - If you're SDVOSB, 8(a), HUBZone, or WOSB certified, these opportunities have less competition</p>
            <p>6. <strong>Read the full solicitation</strong> - Construction specs are detailed. Download all drawings, specs, and attachments from SAM.gov</p>
            <p>7. <strong>Ask questions early</strong> - Use the RFI (Request for Information) process. Submit questions well before the deadline</p>
            <p>8. <strong>Total opportunities available:</strong> This list shows the top 25 construction opportunities. Check SAM.gov for all {total_opps} construction-related opportunities!</p>
        </div>

        <div class="footer">
            <p><strong>December 2025 Construction Opportunities - General Contractors</strong> | GovCon Giants Bootcamp</p>
            <p>All opportunities sourced from SAM.gov (sam.gov)</p>
            <p>Filtered for construction-related projects only</p>
            <p>Last updated: {update_date}</p>
            <p style="margin-top: 15px; font-size: 0.85rem; color: #718096;">Screenshot and share this list! 📸</p>
        </div>
    </div>
</body>
</html>
""".format(
    total_opps=len(construction_opportunities),
    update_date=datetime.now().strftime('%B %d, %Y')
)

# Write HTML file
output_path = '/Users/ericcoffie/Bootcamp/december-hit-list-general-contractors.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Created GC-only hit list with {len(top_opportunities)} construction opportunities")
print(f"📄 Output file: {output_path}")
print(f"📊 Total construction opportunities found: {len(construction_opportunities)}")
















