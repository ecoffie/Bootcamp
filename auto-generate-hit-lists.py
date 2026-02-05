#!/usr/bin/env python3
"""
Automatically fetch contract opportunities from SAM.gov API
and generate all hit list files for a given month
"""

import csv
import sys
import os
import json
from datetime import datetime, timedelta
import html
import argparse
import requests
from urllib.parse import urlencode

def format_date(date_str):
    """Format date string to be more readable"""
    if not date_str or date_str == 'N/A':
        return 'TBD'
    return date_str.strip()

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
    return html.escape(str(text))

def get_set_aside_badge(set_aside):
    """Return appropriate badge class based on set-aside type"""
    if not set_aside or set_aside == 'N/A':
        return ''
    
    set_aside_lower = str(set_aside).lower()
    if 'veteran' in set_aside_lower or 'sdvosb' in set_aside_lower:
        return 'badge-set-aside badge-veteran'
    elif '8(a)' in set_aside_lower or '8a' in set_aside_lower:
        return 'badge-set-aside badge-8a'
    elif 'hubzone' in set_aside_lower:
        return 'badge-set-aside badge-hubzone'
    elif 'wosb' in set_aside_lower or 'women' in set_aside_lower:
        return 'badge-set-aside badge-wosb'
    elif 'small business' in set_aside_lower:
        return 'badge-set-aside badge-sb'
    return 'badge-set-aside'

def filter_by_ndaa_criteria(opportunities):
    """Filter opportunities based on FY2026 NDAA and $138B+ unobligated balances"""
    
    # Agencies with large unobligated balances (from December spend forecast)
    target_agencies = [
        'defense', 'dod', 'department of defense', 'army', 'navy', 'air force',
        'missile defense', 'space force', 'dla', 'defense logistics',
        'cyber', 'cybersecurity', 'command', 'veterans affairs', 'va',
        'homeland security', 'dhs', 'energy', 'doe', 'gsa', 'general services'
    ]
    
    # NAICS codes from NDAA/unobligated balance programs
    target_naics = [
        '541512',  # IT/Cyber
        '541330',  # Engineering
        '561210',  # Facilities
        '541511',  # IT Services
        '541519',  # Other IT
        '541690',  # Other Scientific/Technical Consulting
        '541611',  # Management Consulting
        '541330',  # Engineering Services
        '236220',  # Commercial/Institutional Building Construction
        '237110',  # Water/Sewer Line Construction
        '237130',  # Power/Communication Line Construction
        '238220',  # Plumbing/HVAC
        '336411',  # Aircraft Manufacturing
        '336414',  # Guided Missile/Space Vehicle Manufacturing
        '541715',  # Research/Development in Physical/Engineering Sciences
    ]
    
    # Keywords from NDAA provisions
    ndaa_keywords = [
        'cybersecurity', 'cmmc', 'innovation', 'nontraditional', 'small business',
        'set-aside', 'sole source', 'subcontract', 'supply chain', 'defense',
        'ship', 'aircraft', 'missile', 'space', 'logistics', 'facilities',
        'maintenance', 'repair', 'upgrade', 'modernization'
    ]
    
    filtered = []
    
    for opp in opportunities:
        title = str(opp.get('Title', '')).lower()
        description = str(opp.get('Description', '')).lower()
        agency = str(opp.get('Agency', '')).lower()
        naics = str(opp.get('NAICS Code', ''))
        set_aside = str(opp.get('Set-Aside', '')).lower()
        
        # Must have small business set-aside
        has_set_aside = any(keyword in set_aside for keyword in ['small business', '8(a)', '8a', 'wosb', 'sdvosb', 'hubzone', 'veteran'])
        
        # Check agency match
        agency_match = any(target in agency for target in target_agencies)
        
        # Check NAICS match
        naics_match = any(naics.startswith(code) for code in target_naics)
        
        # Check keyword match in title/description
        text = f"{title} {description}"
        keyword_match = any(keyword in text for keyword in ndaa_keywords)
        
        # Include if matches criteria
        if has_set_aside and (agency_match or naics_match or keyword_match):
            filtered.append(opp)
    
    return filtered

def fetch_sam_gov_opportunities(api_key, month, year, limit=500, filter_ndaa=True):
    """Fetch opportunities from SAM.gov API"""
    print(f"🔍 Fetching opportunities from SAM.gov API...")
    
    # Calculate date range for the month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    
    posted_from = start_date.strftime('%m/%d/%Y')
    posted_to = end_date.strftime('%m/%d/%Y')
    
    print(f"📅 Date range: {posted_from} to {posted_to}")
    
    if filter_ndaa:
        print(f"🎯 Filtering by FY2026 NDAA provisions and $138B+ unobligated balances")
    
    # Build API URL
    base_url = "https://api.sam.gov/opportunities/v2/search"
    params = {
        'api_key': api_key,
        'postedFrom': posted_from,
        'postedTo': posted_to,
        'limit': limit,
        'ptype': 'o,k',  # Solicitation and Combined Synopsis/Solicitation
        'typeOfSetAside': 'SBA',  # Small Business set-asides
    }
    
    url = f"{base_url}?{urlencode(params)}"
    
    try:
        print(f"🌐 Making API request...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'error' in data:
            raise Exception(f"SAM.gov API Error: {data['error'].get('message', 'Unknown error')}")
        
        opportunities = data.get('opportunitiesData', [])
        total_records = data.get('totalRecords', 0)
        
        print(f"✅ Found {total_records} total opportunities")
        print(f"📊 Retrieved {len(opportunities)} opportunities")
        
        # Convert API format to CSV-like format
        csv_opportunities = []
        for opp in opportunities:
            csv_opp = {
                'Active/Inactive': 'Active',  # All fetched are active
                'Title': opp.get('title', 'N/A'),
                'Description': opp.get('description', 'N/A'),
                'Set-Aside': opp.get('typeOfSetAsideDescription', 'N/A'),
                'Current Response Date': opp.get('responseDeadLine', 'N/A'),
                'Award Amount': str(opp.get('award', {}).get('amount', 'N/A')) if opp.get('award') else 'N/A',
                'NAICS Code': opp.get('naicsCode', 'N/A'),
                'Agency': opp.get('organizationType', 'N/A'),
                'Opportunity ID': opp.get('noticeId', 'N/A'),
                'Notice ID': opp.get('noticeId', 'N/A'),
            }
            csv_opportunities.append(csv_opp)
        
        # Filter by NDAA criteria if requested
        if filter_ndaa:
            print(f"🔍 Filtering by FY2026 NDAA and unobligated balance criteria...")
            csv_opportunities = filter_by_ndaa_criteria(csv_opportunities)
            print(f"✅ Filtered to {len(csv_opportunities)} NDAA-aligned opportunities")
        
        return csv_opportunities
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch from SAM.gov API: {str(e)}")
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON response from SAM.gov API: {str(e)}")

def filter_beginner_friendly(opportunities):
    """Filter for beginner-friendly opportunities"""
    beginner_criteria = []
    
    for opp in opportunities:
        score = 0
        set_aside = str(opp.get('Set-Aside', '')).lower()
        
        # Prefer set-asides (less competition)
        if 'small business' in set_aside or '8(a)' in set_aside or '8a' in set_aside or 'wosb' in set_aside or 'sdvosb' in set_aside or 'hubzone' in set_aside:
            score += 3
        
        # Prefer smaller contracts (easier to win)
        contract_value = opp.get('Award Amount', '')
        if contract_value and contract_value != 'N/A':
            try:
                value = float(str(contract_value).replace('$', '').replace(',', ''))
                if value < 1000000:  # Under $1M
                    score += 2
            except:
                pass
        
        # Prefer opportunities with clear requirements
        description = opp.get('Description', '')
        if description and len(str(description)) > 100:
            score += 1
        
        if score >= 3:
            beginner_criteria.append(opp)
    
    return beginner_criteria[:10]  # Top 10

def filter_low_competition(opportunities):
    """Filter for low competition opportunities"""
    low_comp = []
    
    for opp in opportunities:
        set_aside = str(opp.get('Set-Aside', '')).lower()
        
        # Must have set-aside
        if 'small business' in set_aside or '8(a)' in set_aside or '8a' in set_aside or 'wosb' in set_aside or 'sdvosb' in set_aside or 'hubzone' in set_aside:
            low_comp.append(opp)
    
    # Sort by response date (earliest first)
    low_comp.sort(key=lambda x: x.get('Current Response Date', '9999-99-99'))
    
    return low_comp[:34]  # Top 34

def filter_general_contractors(opportunities):
    """Filter for construction/GC opportunities"""
    gc_keywords = ['construction', 'build', 'renovation', 'facility', 'infrastructure', 
                   'maintenance', 'repair', 'construction services', 'general contractor',
                   'architect', 'engineering', 'design-build']
    
    gc_opportunities = []
    
    for opp in opportunities:
        description = str(opp.get('Description', '')).lower()
        title = str(opp.get('Title', '')).lower()
        naics = str(opp.get('NAICS Code', '')).lower()
        
        # Check if construction-related
        is_gc = False
        for keyword in gc_keywords:
            if keyword in description or keyword in title:
                is_gc = True
                break
        
        # Check NAICS codes (construction-related)
        construction_naics = ['236', '237', '238', '5413']  # Construction NAICS prefixes
        if any(naics.startswith(code) for code in construction_naics):
            is_gc = True
        
        if is_gc:
            gc_opportunities.append(opp)
    
    # Sort by response date
    gc_opportunities.sort(key=lambda x: x.get('Current Response Date', '9999-99-99'))
    
    return gc_opportunities[:25]  # Top 25

def generate_html_hit_list(opportunities, title, subtitle, output_file, month, year):
    """Generate HTML hit list file"""
    
    month_name = datetime(year, month, 1).strftime('%B')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{month_name} {year} Hit List - {title}</title>
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
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 50px;
            padding: 30px;
            background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
            color: white;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .header h1 {{
            font-size: 3rem;
            margin-bottom: 10px;
            font-weight: 800;
        }}

        .header .subtitle {{
            font-size: 1.3rem;
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

        .opportunity-card {{
            background: #ffffff;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        .opportunity-card:hover {{
            border-color: #7c3aed;
            box-shadow: 0 8px 20px rgba(124, 58, 237, 0.2);
            transform: translateY(-2px);
        }}

        .opportunity-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .opportunity-number {{
            font-size: 1.5rem;
            font-weight: 800;
            color: #7c3aed;
            min-width: 50px;
        }}

        .opportunity-title {{
            flex: 1;
            font-size: 1.4rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 10px;
        }}

        .badges {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }}

        .badge-set-aside {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .badge-veteran {{
            background: #fef3c7;
            color: #92400e;
        }}

        .badge-8a {{
            background: #dbeafe;
            color: #1e40af;
        }}

        .badge-hubzone {{
            background: #d1fae5;
            color: #065f46;
        }}

        .badge-wosb {{
            background: #fce7f3;
            color: #9f1239;
        }}

        .badge-sb {{
            background: #e0e7ff;
            color: #3730a3;
        }}

        .opportunity-details {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .detail-item {{
            display: flex;
            flex-direction: column;
        }}

        .detail-label {{
            font-size: 0.85rem;
            font-weight: 600;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}

        .detail-value {{
            font-size: 1rem;
            color: #1a1a1a;
            font-weight: 500;
        }}

        .description {{
            margin-top: 20px;
            padding: 15px;
            background: #f9fafb;
            border-radius: 8px;
            border-left: 4px solid #7c3aed;
        }}

        .description-text {{
            color: #4b5563;
            line-height: 1.7;
        }}

        .link-button {{
            display: inline-block;
            margin-top: 15px;
            padding: 12px 24px;
            background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .link-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
        }}

        .footer {{
            text-align: center;
            margin-top: 50px;
            padding: 30px;
            background: #f9fafb;
            border-radius: 12px;
            color: #6b7280;
        }}

        @media print {{
            .opportunity-card {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{month_name} {year} Hit List</h1>
            <div class="subtitle">{subtitle}</div>
            <div class="badge">{len(opportunities)} Opportunities</div>
        </div>
"""

    for idx, opp in enumerate(opportunities, 1):
        title_text = clean_html(opp.get('Title', 'N/A'))
        description = clean_html(truncate_text(opp.get('Description', ''), 300))
        set_aside = opp.get('Set-Aside', 'N/A')
        response_date = format_date(opp.get('Current Response Date', 'N/A'))
        award_amount = opp.get('Award Amount', 'N/A')
        naics = opp.get('NAICS Code', 'N/A')
        agency = opp.get('Agency', 'N/A')
        notice_id = opp.get('Notice ID', 'N/A')
        
        # Build SAM.gov link
        sam_link = f"https://sam.gov/opp/{notice_id}" if notice_id != 'N/A' else "#"
        
        badge_html = ''
        if set_aside != 'N/A':
            badge_class = get_set_aside_badge(set_aside)
            if badge_class:
                badge_html = f'<span class="{badge_class}">{clean_html(set_aside)}</span>'
        
        html_content += f"""
        <div class="opportunity-card">
            <div class="opportunity-header">
                <div class="opportunity-number">#{idx}</div>
                <div style="flex: 1;">
                    <div class="opportunity-title">{title_text}</div>
                    <div class="badges">
                        {badge_html}
                    </div>
                </div>
            </div>
            
            <div class="opportunity-details">
                <div class="detail-item">
                    <div class="detail-label">Response Date</div>
                    <div class="detail-value">{response_date}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Award Amount</div>
                    <div class="detail-value">{clean_html(award_amount)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">NAICS Code</div>
                    <div class="detail-value">{clean_html(naics)}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Agency</div>
                    <div class="detail-value">{clean_html(agency)}</div>
                </div>
            </div>
            
            {f'<div class="description"><div class="description-text">{description}</div></div>' if description and description != 'N/A' else ''}
            
            <a href="{sam_link}" target="_blank" class="link-button">View on SAM.gov →</a>
        </div>
"""
    
    html_content += f"""
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%B %d, %Y')}</p>
            <p>Total Opportunities: {len(opportunities)}</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Created: {output_file} ({len(opportunities)} opportunities)")

def main():
    parser = argparse.ArgumentParser(description='Automatically fetch and generate bootcamp hit lists')
    parser.add_argument('--api-key', help='SAM.gov API key (or set SAM_GOV_API_KEY env var)')
    parser.add_argument('--month', type=int, default=None, help='Month number (1-12)')
    parser.add_argument('--year', type=int, default=None, help='Year (e.g., 2026)')
    parser.add_argument('--limit', type=int, default=500, help='Max opportunities to fetch (default: 500)')
    parser.add_argument('--no-ndaa-filter', action='store_true', help='Disable NDAA/unobligated balance filtering')
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv('SAM_GOV_API_KEY')
    if not api_key:
        print("❌ Error: SAM.gov API key required!")
        print("   Get it from: https://sam.gov → Account Details → Public API Key")
        print("   Then run: export SAM_GOV_API_KEY='your-key-here'")
        print("   Or pass: --api-key 'your-key-here'")
        sys.exit(1)
    
    # Determine month/year
    if not args.month or not args.year:
        now = datetime.now()
        month = args.month or now.month
        year = args.year or now.year
    else:
        month = args.month
        year = args.year
    
    month_name = datetime(year, month, 1).strftime('%B').lower()
    
    print(f"🚀 Auto-generating hit lists for {datetime(year, month, 1).strftime('%B %Y')}")
    print()
    
    # Fetch opportunities from SAM.gov
    try:
        opportunities = fetch_sam_gov_opportunities(api_key, month, year, args.limit, filter_ndaa=not args.no_ndaa_filter)
    except Exception as e:
        print(f"❌ Error fetching opportunities: {e}")
        sys.exit(1)
    
    if not opportunities:
        print("⚠️  No opportunities found. Try adjusting date range or filters.")
        sys.exit(1)
    
    # Generate different hit lists
    print("\n📋 Generating hit lists...")
    
    # 1. Beginner-friendly (top 10)
    beginner = filter_beginner_friendly(opportunities)
    generate_html_hit_list(
        beginner,
        "Beginner-Friendly Opportunities",
        "Perfect for first-time contractors",
        f"{month_name}-hit-list-beginner.html",
        month, year
    )
    
    # 2. Low competition (top 34)
    low_comp = filter_low_competition(opportunities)
    generate_html_hit_list(
        low_comp,
        "Low Competition Opportunities",
        "Set-aside contracts with less competition",
        f"{month_name}-hit-list.html",
        month, year
    )
    
    # 3. General Contractors (top 25)
    gc_opps = filter_general_contractors(opportunities)
    generate_html_hit_list(
        gc_opps,
        "General Contractor Opportunities",
        "Construction and facilities management contracts",
        f"{month_name}-hit-list-general-contractors.html",
        month, year
    )
    
    # 4. Real opportunities (top 30, sorted by response date)
    real_opps = sorted(opportunities, key=lambda x: x.get('Current Response Date', '9999-99-99'))[:30]
    generate_html_hit_list(
        real_opps,
        "Real Opportunities",
        "Top active opportunities sorted by response date",
        f"{month_name}-hit-list-real-opportunities.html",
        month, year
    )
    
    # 5. Combined list (beginner + low competition)
    combined = beginner + low_comp
    # Remove duplicates based on Notice ID
    seen = set()
    unique_combined = []
    for opp in combined:
        notice_id = opp.get('Notice ID', '')
        if notice_id not in seen:
            seen.add(notice_id)
            unique_combined.append(opp)
    
    generate_html_hit_list(
        unique_combined,
        "Complete Hit List",
        "Combined beginner-friendly and low competition opportunities",
        f"{month_name}-hit-list-complete.html",
        month, year
    )
    
    print(f"\n✅ All files created successfully!")
    print(f"\n📄 Generated Files:")
    print(f"   - {month_name}-hit-list-beginner.html")
    print(f"   - {month_name}-hit-list.html")
    print(f"   - {month_name}-hit-list-general-contractors.html")
    print(f"   - {month_name}-hit-list-real-opportunities.html")
    print(f"   - {month_name}-hit-list-complete.html")

if __name__ == '__main__':
    main()
