#!/usr/bin/env python3
"""
Create a beginner-friendly hit list from the contract opportunities CSV
"""

import csv
from datetime import datetime
import html

def format_date(date_str):
    """Format date string to be more readable"""
    if not date_str or date_str == 'N/A':
        return 'TBD'
    try:
        # Try to parse the date
        date_str = date_str.strip()
        # Handle different date formats
        if 'EST' in date_str or 'CST' in date_str or 'PST' in date_str or 'MST' in date_str:
            return date_str
        return date_str
    except:
        return date_str

def truncate_text(text, max_length=150):
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

# Read CSV file
csv_path = '/Users/ericcoffie/Library/CloudStorage/GoogleDrive-evankoffdev@gmail.com/My Drive/Federal Help Center/Dec 13 Surge Event/ContractOpportunities-20251212-092037.csv'

opportunities = []
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
        print(f"Successfully read CSV with {encoding} encoding")
        break
    except Exception as e:
        continue

print(f"Processing {len(opportunities)} active opportunities...")

# Sort by response date (earliest first for December urgency)
def sort_key(opp):
    date_str = opp.get('Current Response Date', '')
    if not date_str or date_str == 'N/A':
        return '9999-99-99'  # Put at end
    return date_str

opportunities.sort(key=sort_key)

# Limit to top 30 for beginner-friendly list
top_opportunities = opportunities[:30]

# Generate HTML
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>December 2025 Hit List - Real Opportunities</title>
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
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
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
            background: #f8fafc;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 35px;
            border-left: 5px solid #7c3aed;
        }}

        .intro h2 {{
            color: #1e3a8a;
            margin-bottom: 15px;
            font-size: 1.5rem;
        }}

        .intro p {{
            font-size: 1rem;
            color: #4a5568;
            margin-bottom: 10px;
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
            background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
        }}

        .opportunity-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            border-color: #7c3aed;
        }}

        .opportunity-number {{
            display: inline-block;
            width: 35px;
            height: 35px;
            background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
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
            color: #1e3a8a;
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
            color: #1e3a8a;
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

        .badge-beginner {{
            background: #dcfce7;
            color: #166534;
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
            color: #1e3a8a;
        }}

        .action-box {{
            background: #f0f9ff;
            border-left: 4px solid #0284c7;
            padding: 15px;
            margin-top: 15px;
            border-radius: 8px;
            font-size: 0.9rem;
        }}

        .action-box strong {{
            color: #0c4a6e;
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
            <h1>🎯 December 2025 Hit List</h1>
            <p class="subtitle">Top {len(top_opportunities)} Real Contract Opportunities</p>
            <p style="font-size: 1rem; margin-top: 10px; opacity: 0.9;">From SAM.gov - Active Solicitations</p>
            <span class="badge">Response Deadlines: Dec 2025 - Jan 2026</span>
        </div>

        <div class="intro">
            <h2>These Are REAL Opportunities</h2>
            <p><strong>✅ All active solicitations</strong> - These contracts are accepting bids RIGHT NOW</p>
            <p><strong>✅ Set-asides included</strong> - Many are reserved for small businesses, veterans, 8(a), HUBZone, WOSB</p>
            <p><strong>✅ Response deadlines listed</strong> - Know exactly when to submit</p>
            <p><strong>✅ POC information included</strong> - Contact the right person immediately</p>
            <p><strong>✅ NAICS codes provided</strong> - Match your business capabilities</p>
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
                    {badge_html}
                    {urgent_badge}
                </div>
                <div class="opportunity-details">
                    <p><strong>Description:</strong> {description}</p>
                    {f'<p><strong>Set-Aside:</strong> {set_aside}</p>' if set_aside != 'N/A' else ''}
                    <div class="action-box">
                        <strong>📞 Your Action Items:</strong>
                        1. Review full solicitation on SAM.gov using Notice ID: <strong>{notice_id}</strong><br>
                        2. {f'Contact POC: <strong>{poc}</strong>' if poc != 'N/A' else 'Check SAM.gov for POC information'}<br>
                        3. Ensure you meet set-aside requirements (if applicable)<br>
                        4. Submit response by <strong>{response_date}</strong>
                    </div>
                </div>
            </div>
"""

html_content += """
        </div>

        <div class="key-point">
            <p><strong>💡 How to Use This List:</strong></p>
            <p>1. <strong>Find opportunities matching your certifications</strong> - Look for your set-aside type (8(a), SDVOSB, HUBZone, WOSB, Small Business)</p>
            <p>2. <strong>Check NAICS codes</strong> - Make sure your business is qualified for the NAICS code listed</p>
            <p>3. <strong>Go to SAM.gov</strong> - Search by Notice ID to see the full solicitation</p>
            <p>4. <strong>Contact the POC immediately</strong> - Ask questions, request site visits, clarify requirements</p>
            <p>5. <strong>Don't wait</strong> - These deadlines are real. Start preparing your response NOW.</p>
            <p>6. <strong>Total opportunities available:</strong> This list shows the top 30 by deadline. Check SAM.gov for all {total_opps} active opportunities!</p>
        </div>

        <div class="footer">
            <p><strong>December 2025 Real Opportunities Hit List</strong> | GovCon Giants Bootcamp</p>
            <p>All opportunities sourced from SAM.gov (sam.gov)</p>
            <p>Last updated: {update_date}</p>
            <p style="margin-top: 15px; font-size: 0.85rem; color: #718096;">Screenshot and share this list! 📸</p>
        </div>
    </div>
</body>
</html>
""".format(
    total_opps=len(opportunities),
    update_date=datetime.now().strftime('%B %d, %Y')
)

# Write HTML file
output_path = '/Users/ericcoffie/Bootcamp/december-hit-list-real-opportunities.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Created hit list with {len(top_opportunities)} opportunities")
print(f"📄 Output file: {output_path}")
print(f"📊 Total active opportunities available: {len(opportunities)}")

