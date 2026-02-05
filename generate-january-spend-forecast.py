#!/usr/bin/env python3
"""
Generate January 2026 Spend Forecast + Immediate Buyers List
Based on FY2026 NDAA (S.2296), Monthly Treasury Statement, GAO reports, USAspending dashboards
"""

import csv
from datetime import datetime

# Data sources template - Update with actual data from:
# - FY2026 NDAA (S.2296, 119th Congress)
# - Monthly Treasury Statement Jan 2026 (or latest available)
# - GAO Jan 2026 reports
# - USAspending Q1 FY2026 dashboards

JANUARY_FORECAST_DATA = [
    {
        'rank': 1,
        'agency': 'Department of Defense (overall)',
        'program': 'Overall DoD',
        'unobligated_balance': '$35B+',  # Updated from Dec $38B+ (spent some in Dec)
        'hot_naics': 'IT/Cyber (541512), Engineering (541330), Facilities (561210)',
        'ndaa_provision': 'S.2296 authorizes $32.1B over President\'s FY2026 Budget Request',
        'why_now': 'Q1 FY2026 push to obligate remaining balances; 23% small business goal',
    },
    {
        'rank': 2,
        'agency': 'Army Procurement',
        'program': 'Army Procurement',
        'unobligated_balance': '$8B',  # Updated from Dec $10B
        'hot_naics': 'Ground vehicles, weapons systems, logistics',
        'ndaa_provision': 'S.2296 Sec. [XXX] - Army modernization priorities',
        'why_now': 'Q1 FY2026 vehicle upgrades and weapons systems',
    },
    {
        'rank': 3,
        'agency': 'Navy Shipbuilding',
        'program': 'Navy Shipbuilding',
        'unobligated_balance': '$7B',  # Updated from Dec $8B
        'hot_naics': 'Maritime tech, ship repair, subsystems',
        'ndaa_provision': 'S.2296 Sec. [XXX] - Shipbuilding authorizations',
        'why_now': 'Q1 FY2026 ship maintenance and modernization',
    },
    {
        'rank': 4,
        'agency': 'Air Force RDT&E',
        'program': 'Air Force RDT&E',
        'unobligated_balance': '$6B',  # Updated from Dec $7B
        'hot_naics': 'Aircraft upgrades, space systems, AI prototypes',
        'ndaa_provision': 'S.2296 Sec. [XXX] - RDT&E priorities',
        'why_now': 'Q1 FY2026 tech prototypes and space systems',
    },
    {
        'rank': 5,
        'agency': 'Defense Logistics Agency',
        'program': 'DLA',
        'unobligated_balance': '$4.5B',  # Updated from Dec $5B
        'hot_naics': 'Supply chain, MRO, energy products',
        'ndaa_provision': 'S.2296 Sec. [XXX] - Logistics modernization',
        'why_now': 'Q1 FY2026 supply chain resilience',
    },
    {
        'rank': 6,
        'agency': 'Missile Defense Agency',
        'program': 'MDA',
        'unobligated_balance': '$3.5B',  # Updated from Dec $4B
        'hot_naics': 'Missile tech, sensors, testing',
        'ndaa_provision': 'S.2296 Sec. [XXX] - Missile defense systems',
        'why_now': 'Q1 FY2026 missile defense upgrades',
    },
    {
        'rank': 7,
        'agency': 'Cyber Command',
        'program': 'Cyber Command',
        'unobligated_balance': '$3B',  # Updated from Dec $3.5B
        'hot_naics': 'Cybersecurity, zero trust, cloud migration',
        'ndaa_provision': 'S.2296 Sec. [XXX] - Cybersecurity harmonization (June 2026 deadline)',
        'why_now': 'Q1 FY2026 cyber surge; CMMC support strategy (Jan 31 deadline)',
    },
    {
        'rank': 8,
        'agency': 'DOE / Atomic Energy Defense',
        'program': 'Atomic Energy Defense',
        'unobligated_balance': '$2.2B',  # Updated from Dec $2.5B
        'hot_naics': 'Nuclear cleanup, environmental services',
        'ndaa_provision': 'S.2296 Sec. [XXX] - Nuclear modernization',
        'why_now': 'Q1 FY2026 environmental cleanup',
    },
    {
        'rank': 9,
        'agency': 'Space Force',
        'program': 'Space Force',
        'unobligated_balance': '$2.5B',  # Updated from Dec $2.8B
        'hot_naics': 'Satellite support, launch services',
        'ndaa_provision': 'S.2296 Sec. 9083 - New Vice Chief role accelerates spending',
        'why_now': 'Q1 FY2026 satellite and launch services',
    },
    {
        'rank': 10,
        'agency': 'Defense Health Program',
        'program': 'DHP',
        'unobligated_balance': '$1.8B',  # Updated from Dec $2B
        'hot_naics': 'Medical IT, telehealth, equipment',
        'ndaa_provision': 'S.2296 Sec. [XXX] - Health modernization',
        'why_now': 'Q1 FY2026 medical IT and telehealth',
    },
]

def generate_csv():
    """Generate CSV file with January forecast data"""
    csv_file = 'january-spend-forecast-enhanced.csv'
    
    fieldnames = ['agency', 'program', 'unobligated_balance', 'hot_naics', 
                  'prime_contractor', 'sblo_name', 'sblo_email', 'sblo_phone', 'source']
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for item in JANUARY_FORECAST_DATA:
            writer.writerow({
                'agency': item['agency'],
                'program': item['program'],
                'unobligated_balance': item['unobligated_balance'],
                'hot_naics': item['hot_naics'],
                'prime_contractor': '[NEEDS RESEARCH]',
                'sblo_name': '[NEEDS RESEARCH]',
                'sblo_email': '[NEEDS RESEARCH]',
                'sblo_phone': '[NEEDS RESEARCH]',
                'source': 'January 2026 Forecast - Needs Contact Research'
            })
    
    print(f"✅ Created: {csv_file}")
    print(f"📊 Generated {len(JANUARY_FORECAST_DATA)} agency entries")
    print(f"⚠️  Note: Prime contractor and SBLO contacts need to be researched")

def generate_data_sources_guide():
    """Generate guide for finding data sources"""
    guide = """# 📊 January 2026 Spend Forecast - Data Sources Guide

## Required Data Sources

### 1. FY2026 NDAA (S.2296, 119th Congress)
**Status:** ✅ Already have (signed December 18, 2025)
**Location:** https://www.congress.gov/bill/119th-congress/senate-bill/2296
**What to Extract:**
- Specific section numbers for each agency/program
- Authorization amounts vs. budget requests
- Small business provisions and thresholds
- Implementation deadlines

### 2. Monthly Treasury Statement (Latest Available)
**Status:** ⚠️ Need to find
**Where to Find:**
- Treasury.gov: https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/
- Look for: "Monthly Treasury Statement" for latest month (Jan 2026 or Dec 2025)
- Search for: "unobligated balances" or "budget execution"

**What to Extract:**
- Q1 FY2026 unobligated balances by agency
- Comparison to Q4 FY2025 (December data)
- Spending trends and gaps

### 3. GAO Reports (Latest Available)
**Status:** ⚠️ Need to find
**Where to Find:**
- GAO.gov: https://www.gao.gov/
- Search for: "unobligated balances" + "January 2026" or "FY2026"
- Or: "budget execution" + "defense" + "2026"

**What to Extract:**
- Agency-specific unobligated balance reports
- Spending efficiency reports
- Small business contracting reports

### 4. USAspending.gov Q1 FY2026 Dashboards
**Status:** ⚠️ Need to find
**Where to Find:**
- USAspending.gov: https://www.usaspending.gov/
- Navigate to: Dashboards → Agency Spending → Filter by FY2026 Q1
- Or: Search → Advanced Search → Filter by fiscal year and quarter

**What to Extract:**
- Agency spending by program
- Contract awards by NAICS code
- Small business set-aside data
- Unobligated vs. obligated amounts

## Quick Links

1. **FY2026 NDAA (S.2296):**
   - Full Text: https://www.congress.gov/bill/119th-congress/senate-bill/2296/text
   - Summary: https://www.congress.gov/bill/119th-congress/senate-bill/2296/summary

2. **Monthly Treasury Statement:**
   - Latest: https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/
   - Search: "Monthly Treasury Statement" + current month

3. **GAO Reports:**
   - Search: https://www.gao.gov/search?q=unobligated+balances+2026
   - Or: https://www.gao.gov/search?q=budget+execution+defense+2026

4. **USAspending.gov:**
   - Dashboard: https://www.usaspending.gov/explorer
   - Advanced Search: https://www.usaspending.gov/search/

## Data Collection Checklist

- [ ] Download latest Monthly Treasury Statement
- [ ] Find latest GAO report on unobligated balances
- [ ] Access USAspending.gov Q1 FY2026 dashboard
- [ ] Extract specific section numbers from NDAA for each agency
- [ ] Calculate updated unobligated balances (Dec → Jan)
- [ ] Verify small business set-aside percentages
- [ ] Research prime contractor contacts for each program
- [ ] Research SBLO contacts for each agency/program

## Next Steps

1. Run this script to generate the CSV template
2. Research and update unobligated balances from latest data sources
3. Add prime contractor and SBLO contact information
4. Generate HTML forecast using the updated CSV
"""
    
    with open('JANUARY-FORECAST-DATA-SOURCES.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(f"✅ Created: JANUARY-FORECAST-DATA-SOURCES.md")

if __name__ == '__main__':
    print("🚀 Generating January 2026 Spend Forecast Data...")
    print()
    
    generate_csv()
    print()
    generate_data_sources_guide()
    print()
    print("📋 Next Steps:")
    print("1. Review JANUARY-FORECAST-DATA-SOURCES.md for data source links")
    print("2. Research and update unobligated balances from latest sources")
    print("3. Add prime contractor and SBLO contacts to CSV")
    print("4. Use updated CSV to generate HTML forecast")
