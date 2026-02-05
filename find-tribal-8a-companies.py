#!/usr/bin/env python3
"""
Find Tribal 8(a) Companies for Prime List
Searches SBA DSBS and compiles list of tribal-owned 8(a) companies
"""

import csv
import requests
from pathlib import Path
import time
import re

def search_sba_dsbs_tribal_8a():
    """
    Search SBA Dynamic Small Business Search for Tribal 8(a) companies
    Note: This requires web scraping or API access to SBA DSBS
    """
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Finding Tribal 8(a) Companies                     ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    print("📋 Public Sources for Tribal 8(a) Companies:")
    print("=" * 60)
    print("""
    1. SBA Dynamic Small Business Search (DSBS)
       URL: https://web.sba.gov/pro-net/search/dsp_dsbs.cfm
       Search Criteria:
       - Ownership: Native American
       - Certification: 8(a) Certified
       
    2. USET Tribal Enterprise Directory
       URL: https://www.usetinc.org/departments/economic-development/tribal-enterprise-directory/
       
    3. NCAIED (National Center for American Indian Enterprise Development)
       URL: http://www.ncaied.org/
       
    4. BIA Tribal Leaders Directory
       URL: https://www.bia.gov/service/tribal-leaders-directory
    """)
    
    return []

def check_sba_directory_for_tribal():
    """Check if SBA directory has tribal/8(a) indicators"""
    sba_file = Path('sba-prime-directory-companies.csv')
    
    if not sba_file.exists():
        print("❌ SBA directory file not found")
        return []
    
    print("\n🔍 Checking SBA Prime Directory for tribal/8(a) indicators...")
    
    # Read first few rows to check columns
    with open(sba_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        first_row = next(reader, None)
        
        if first_row:
            print(f"\n📊 Available columns: {', '.join(first_row.keys())}")
            
            # Look for tribal/8a indicators
            tribal_keywords = ['tribal', 'native', '8a', '8(a)', 'indian', 'alaska native']
            found_columns = []
            
            for col in first_row.keys():
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in tribal_keywords):
                    found_columns.append(col)
            
            if found_columns:
                print(f"✅ Found potential columns: {', '.join(found_columns)}")
            else:
                print("⚠️  No obvious tribal/8(a) columns found")
                print("   Will need to search by company name patterns")
    
    return []

def create_tribal_8a_research_template():
    """Create research template for finding tribal 8(a) companies"""
    print("\n" + "=" * 60)
    print("📝 Creating Tribal 8(a) Research Template")
    print("=" * 60)
    
    # Common tribal company name patterns
    tribal_patterns = [
        r'\btribal\b',
        r'\bnative\b',
        r'\bindian\b',
        r'\balaska native\b',
        r'\bcherokee\b',
        r'\bnavajo\b',
        r'\bsioux\b',
        r'\bchoctaw\b',
        r'\bcreek\b',
        r'\bchickasaw\b',
        r'\bseminole\b',
        r'\benterprises?\b',
        r'\bdevelopment\b',
    ]
    
    # Check SBA directory for matches
    sba_file = Path('sba-prime-directory-companies.csv')
    tribal_companies = []
    
    if sba_file.exists():
        print("🔍 Searching SBA directory for tribal company name patterns...")
        
        with open(sba_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company = row.get('company', '') or row.get('Prime Name', '') or ''
                company_lower = company.lower()
                
                # Check for tribal patterns
                if any(re.search(pattern, company_lower) for pattern in tribal_patterns):
                    tribal_companies.append({
                        'company': company,
                        'contract_count': row.get('contract_count', ''),
                        'total_contract_value': row.get('total_contract_value', ''),
                        'agencies': row.get('agencies', ''),
                        'naics': row.get('naics', ''),
                        'match_reason': 'Name pattern match',
                        '8a_status': '[NEEDS VERIFICATION]',
                        'tribal_affiliation': '[NEEDS RESEARCH]',
                        'sblo_contact': '[NEEDS RESEARCH]'
                    })
        
        print(f"✅ Found {len(tribal_companies)} potential tribal companies")
    
    # Create research template
    template_file = Path('tribal-8a-research-template.csv')
    with open(template_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'contract_count', 'total_contract_value', 'agencies', 'naics',
                     'match_reason', '8a_status', 'tribal_affiliation', 'sblo_contact', 'email', 'phone', 'website', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tribal_companies)
    
    print(f"💾 Saved research template: {template_file}")
    
    if tribal_companies:
        print("\n📋 Top Potential Tribal Companies Found:")
        for i, company in enumerate(tribal_companies[:10], 1):
            value = company.get('total_contract_value', '')
            if value:
                try:
                    value_str = f"${float(value):,.0f}"
                except:
                    value_str = value
            else:
                value_str = 'N/A'
            print(f"   {i:2d}. {company['company'][:50]:50s} - {value_str}")
    
    return tribal_companies

def create_tribal_8a_guide():
    """Create comprehensive guide for finding tribal 8(a) companies"""
    guide_file = Path('TRIBAL-8A-RESEARCH-GUIDE.md')
    
    guide_content = """# Tribal 8(a) Companies Research Guide

## Overview
This guide helps you find and compile a list of Tribal 8(a) companies to target as part of your prime contractor list.

## What are Tribal 8(a) Companies?
- Companies owned by Native American tribes or Alaska Native Corporations (ANCs)
- Certified in the SBA 8(a) Business Development Program
- Eligible for sole-source contracts up to $4M (services) or $6.5M (manufacturing)
- No limit on contract value for tribal/ANC-owned 8(a) companies

---

## 🔍 Primary Sources

### 1. SBA Dynamic Small Business Search (DSBS)
**URL:** https://web.sba.gov/pro-net/search/dsp_dsbs.cfm

**How to Search:**
1. Go to the DSBS search page
2. In "Ownership and Self-Certifications" section:
   - Select "Native American" or "Alaska Native Corporation"
3. In "Government Certifications" section:
   - Select "8(a) Certified"
4. Click "Search Using These Criteria"
5. Export results to CSV/Excel

**Advantages:**
- Official SBA database
- Can filter by location, NAICS codes
- Includes contact information
- Updated regularly

**Limitations:**
- Requires manual search/export
- May need multiple searches for different regions

---

### 2. USET Tribal Enterprise Directory
**URL:** https://www.usetinc.org/departments/economic-development/tribal-enterprise-directory/

**What it contains:**
- Directory of tribal enterprises
- Some 8(a) certified companies
- Contact information for tribal businesses

**How to use:**
- Browse by tribe or enterprise type
- Contact tribal economic development offices
- Request lists of 8(a) certified companies

---

### 3. National Center for American Indian Enterprise Development (NCAIED)
**URL:** http://www.ncaied.org/

**Resources:**
- Business directories
- Networking events
- Certification assistance
- Contact information for tribal businesses

---

### 4. Bureau of Indian Affairs (BIA) Tribal Leaders Directory
**URL:** https://www.bia.gov/service/tribal-leaders-directory

**Use for:**
- Finding tribal leadership contacts
- Contacting tribes directly for business enterprise lists
- Understanding tribal structure

---

### 5. Alaska Native Corporations (ANCs)
**Key ANCs with 8(a) companies:**
- Arctic Slope Regional Corporation (ASRC)
- Bristol Bay Native Corporation
- Calista Corporation
- Chugach Alaska Corporation
- Doyon, Limited
- Koniag, Inc.
- NANA Regional Corporation
- Sealaska Corporation
- The Aleut Corporation
- And many more...

**ANC Directory:** Search for "Alaska Native Corporation directory"

---

## 📋 Research Strategy

### Step 1: Search SBA DSBS
1. Search for "Native American" + "8(a) Certified"
2. Search for "Alaska Native Corporation" + "8(a) Certified"
3. Export results to CSV
4. Filter by your target NAICS codes

### Step 2: Cross-Reference with Your Prime List
1. Check your existing SBA prime directory
2. Look for companies with tribal names/patterns
3. Verify 8(a) status in DSBS
4. Add to tribal 8(a) target list

### Step 3: Contact Tribal Economic Development Offices
1. Use BIA directory to find tribes
2. Contact economic development departments
3. Request lists of 8(a) certified tribal enterprises
4. Ask for SBLO contacts

### Step 4: Attend Networking Events
- NCAIED conferences
- Tribal business summits
- Government contracting events
- Small business conferences

---

## 🎯 Target Companies

### High-Value Tribal 8(a) Companies
Look for companies that:
- Have existing prime contracts
- Work in your target NAICS codes
- Have SBLO contacts listed
- Are actively seeking subcontractors

### Company Name Patterns
Common patterns to look for:
- "[Tribe Name] Enterprises"
- "[Tribe Name] Development Corporation"
- "[Tribe Name] Industries"
- "[Tribe Name] Holdings"
- "ANC" in company name (Alaska Native Corporation)

---

## 📊 Integration with Prime List

### Adding to Your SBLO List
1. Find tribal 8(a) companies
2. Research SBLO contacts (same process as other primes)
3. Add to `sblo-list-compiled.csv`
4. Tag as "Tribal 8(a)" in source column
5. Include tribal affiliation

### Priority Companies
Focus on:
- Companies with existing prime contracts
- Companies in your target industries
- Companies with active SBLO programs
- Companies seeking small business partners

---

## 🔧 Tools & Scripts

### Research Template
- `tribal-8a-research-template.csv` - Template for tracking research

### Name Pattern Search
Run `find-tribal-8a-companies.py` to search your SBA directory for potential tribal companies by name patterns.

---

## 📝 Next Steps

1. ✅ Search SBA DSBS for Native American + 8(a) companies
2. ✅ Search SBA DSBS for Alaska Native Corporation + 8(a) companies
3. ✅ Cross-reference with your SBA prime directory
4. ✅ Contact top tribal economic development offices
5. ✅ Research SBLO contacts for identified companies
6. ✅ Add verified companies to your prime list

---

## 📚 Additional Resources

- **SBA 8(a) Program:** https://www.sba.gov/federal-contracting/contracting-assistance-programs/8a-business-development-program
- **Tribal 8(a) Benefits:** https://www.sba.gov/federal-contracting/contracting-assistance-programs/8a-business-development-program/tribal-8a-program
- **SAM.gov:** Search for companies with "Native American" or "Tribal" set-asides
- **FPDS.gov:** Search contracts awarded to tribal 8(a) companies

---

**Last Updated:** December 2025
**Status:** Research Guide Ready
"""
    
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"💾 Created research guide: {guide_file}")
    return guide_file

def main():
    print("Starting Tribal 8(a) Company Research...\n")
    
    # Create research guide
    create_tribal_8a_guide()
    
    # Check SBA directory
    check_sba_directory_for_tribal()
    
    # Create research template
    tribal_companies = create_tribal_8a_research_template()
    
    print("\n" + "=" * 60)
    print("✨ Research Setup Complete!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   - Research guide created: TRIBAL-8A-RESEARCH-GUIDE.md")
    print(f"   - Potential tribal companies found: {len(tribal_companies)}")
    print(f"   - Research template created: tribal-8a-research-template.csv")
    
    print("\n🎯 Next Steps:")
    print("   1. Review TRIBAL-8A-RESEARCH-GUIDE.md")
    print("   2. Search SBA DSBS for Native American + 8(a) companies")
    print("   3. Search SBA DSBS for Alaska Native Corporation + 8(a) companies")
    print("   4. Verify companies in tribal-8a-research-template.csv")
    print("   5. Research SBLO contacts for identified companies")
    print("   6. Add to your prime list")

if __name__ == '__main__':
    main()




