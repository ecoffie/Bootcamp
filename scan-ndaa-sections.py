#!/usr/bin/env python3
"""
Automatically scan FY2026 NDAA (S.2296) to extract section numbers and provisions
"""

import requests
import re
from bs4 import BeautifulSoup
import json
import os

# Try to import PDF libraries
try:
    import PyPDF2
    PDF_LIB = 'PyPDF2'
except ImportError:
    try:
        import pypdf
        PDF_LIB = 'pypdf'
    except ImportError:
        PDF_LIB = None

# Agencies/programs to search for
AGENCIES_TO_FIND = [
    'Department of Defense',
    'DoD',
    'Army',
    'Navy',
    'Air Force',
    'Defense Logistics Agency',
    'DLA',
    'Missile Defense Agency',
    'MDA',
    'Cyber Command',
    'DOE',
    'Department of Energy',
    'Atomic Energy',
    'Space Force',
    'Defense Health',
]

# Keywords to search for
KEYWORDS = [
    'procurement',
    'shipbuilding',
    'RDT&E',
    'research and development',
    'logistics',
    'missile defense',
    'cybersecurity',
    'cyber',
    'nuclear',
    'space',
    'health',
]

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    if not PDF_LIB:
        print("❌ No PDF library available. Install with: pip3 install PyPDF2")
        return None
    
    print(f"📄 Extracting text from PDF: {pdf_path}")
    
    try:
        text_content = ""
        with open(pdf_path, 'rb') as f:
            if PDF_LIB == 'PyPDF2':
                pdf_reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(pdf_reader.pages):
                    text_content += page.extract_text()
                    if page_num % 50 == 0:
                        print(f"  Processed {page_num} pages...")
            elif PDF_LIB == 'pypdf':
                pdf_reader = pypdf.PdfReader(f)
                for page_num, page in enumerate(pdf_reader.pages):
                    text_content += page.extract_text()
                    if page_num % 50 == 0:
                        print(f"  Processed {page_num} pages...")
        
        print(f"✅ Extracted text from PDF ({len(text_content)} characters)")
        return text_content
        
    except Exception as e:
        print(f"❌ Error extracting PDF text: {e}")
        return None

def fetch_ndaa_text(file_path=None):
    """Fetch the NDAA text from Congress.gov or read from file"""
    
    # If file path provided, read from file
    if file_path:
        print(f"📄 Reading NDAA from file: {file_path}")
        
        # Check if it's a PDF
        if file_path.lower().endswith('.pdf'):
            return extract_text_from_pdf(file_path)
        
        # Otherwise read as text file
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text_content = f.read()
            print(f"✅ Read NDAA text ({len(text_content)} characters)")
            return text_content
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return None
    
    # Try to fetch from Congress.gov (may be blocked)
    print("🔍 Attempting to fetch NDAA text from Congress.gov...")
    print("⚠️  Note: Congress.gov may block automated access")
    
    url = "https://www.congress.gov/bill/119th-congress/senate-bill/2296/text"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the text content
        text_content = soup.get_text()
        
        print(f"✅ Fetched NDAA text ({len(text_content)} characters)")
        return text_content
        
    except Exception as e:
        print(f"❌ Error fetching NDAA text: {e}")
        print("\n💡 Alternative methods:")
        print("1. Download the PDF/text from: https://www.congress.gov/bill/119th-congress/senate-bill/2296/text")
        print("2. Copy/paste the text into a file")
        print("3. Run: python3 scan-ndaa-sections.py --file path/to/ndaa-text.txt")
        return None

def extract_sections(text):
    """Extract section numbers from NDAA text"""
    print("\n🔍 Scanning for section numbers...")
    
    # Pattern to match section numbers (e.g., "Sec. 9083", "Section 9083", "SEC. 9083")
    section_pattern = r'(?:Sec\.|Section|SEC\.)\s*(\d{1,5})'
    
    sections = {}
    matches = re.finditer(section_pattern, text, re.IGNORECASE)
    
    for match in matches:
        section_num = match.group(1)
        # Get context around the section (100 chars before and after)
        start = max(0, match.start() - 100)
        end = min(len(text), match.end() + 200)
        context = text[start:end]
        
        sections[section_num] = {
            'number': section_num,
            'context': context.strip()
        }
    
    print(f"✅ Found {len(sections)} section numbers")
    return sections

def find_agency_sections(text, sections):
    """Find sections related to specific agencies"""
    print("\n🔍 Finding agency-related sections...")
    
    agency_sections = {}
    
    for agency in AGENCIES_TO_FIND:
        agency_sections[agency] = []
        
        # Search for agency name near section numbers
        for section_num, section_data in sections.items():
            context_lower = section_data['context'].lower()
            agency_lower = agency.lower()
            
            # Check if agency name appears near this section
            if agency_lower in context_lower:
                # Also check for keywords
                has_keyword = any(keyword.lower() in context_lower for keyword in KEYWORDS)
                
                agency_sections[agency].append({
                    'section': section_num,
                    'context': section_data['context'],
                    'has_keyword': has_keyword
                })
    
    return agency_sections

def find_small_business_provisions(text):
    """Find small business-related provisions"""
    print("\n🔍 Finding small business provisions...")
    
    sb_keywords = [
        'small business',
        'set-aside',
        'set aside',
        'sole source',
        '8\\(a\\)',
        '8a',
        'SDVOSB',
        'HUBZone',
        'WOSB',
        'subcontract',
        'unified application',
        'CMMC',
        'cybersecurity harmonization',
    ]
    
    provisions = []
    
    # Find sections with small business keywords
    section_pattern = r'(?:Sec\.|Section|SEC\.)\s*(\d{1,5})'
    sections = re.finditer(section_pattern, text, re.IGNORECASE)
    
    for section_match in sections:
        section_num = section_match.group(1)
        # Get context around section
        start = max(0, section_match.start() - 50)
        end = min(len(text), section_match.end() + 500)
        context = text[start:end].lower()
        
        # Check for small business keywords
        for keyword in sb_keywords:
            if re.search(keyword, context, re.IGNORECASE):
                provisions.append({
                    'section': section_num,
                    'keyword': keyword,
                    'context': text[start:end].strip()[:300]  # First 300 chars
                })
                break
    
    print(f"✅ Found {len(provisions)} small business provisions")
    return provisions

def save_results(sections, agency_sections, sb_provisions):
    """Save results to JSON and markdown files"""
    
    # Save JSON
    results = {
        'all_sections': sections,
        'agency_sections': agency_sections,
        'small_business_provisions': sb_provisions
    }
    
    with open('ndaa-sections-extracted.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("✅ Saved: ndaa-sections-extracted.json")
    
    # Save markdown report
    md_content = "# FY2026 NDAA (S.2296) - Extracted Sections\n\n"
    md_content += "**Automatically extracted from Congress.gov**\n\n"
    md_content += f"**Total sections found:** {len(sections)}\n\n"
    
    md_content += "## Agency-Related Sections\n\n"
    for agency, sections_list in agency_sections.items():
        if sections_list:
            md_content += f"### {agency}\n\n"
            for item in sections_list[:5]:  # Top 5 matches
                md_content += f"**Section {item['section']}**\n"
                md_content += f"```\n{item['context'][:200]}...\n```\n\n"
    
    md_content += "## Small Business Provisions\n\n"
    for prov in sb_provisions[:20]:  # Top 20
        md_content += f"**Section {prov['section']}** - Keyword: {prov['keyword']}\n"
        md_content += f"```\n{prov['context'][:200]}...\n```\n\n"
    
    with open('ndaa-sections-extracted.md', 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print("✅ Saved: ndaa-sections-extracted.md")
    
    # Update the tracking file
    update_tracking_file(agency_sections, sb_provisions)

def update_tracking_file(agency_sections, sb_provisions):
    """Update NDAA-SECTION-NUMBERS.md with found sections"""
    try:
        with open('NDAA-SECTION-NUMBERS.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Map agencies to tracking file sections
        agency_map = {
            'Department of Defense': 'DoD Overall',
            'DoD': 'DoD Overall',
            'Army': 'Army Procurement',
            'Navy': 'Navy Shipbuilding',
            'Air Force': 'Air Force RDT&E',
            'Defense Logistics Agency': 'Defense Logistics Agency (DLA)',
            'DLA': 'Defense Logistics Agency (DLA)',
            'Missile Defense Agency': 'Missile Defense Agency (MDA)',
            'MDA': 'Missile Defense Agency (MDA)',
            'Cyber Command': 'Cyber Command',
            'DOE': 'DOE / Atomic Energy Defense',
            'Department of Energy': 'DOE / Atomic Energy Defense',
            'Atomic Energy': 'DOE / Atomic Energy Defense',
            'Space Force': 'Space Force',
            'Defense Health': 'Defense Health Program',
        }
        
        # Update section numbers
        for agency_key, tracking_name in agency_map.items():
            if agency_key in agency_sections and agency_sections[agency_key]:
                sections_found = [item['section'] for item in agency_sections[agency_key][:3]]
                section_str = ', '.join(sections_found)
                
                # Replace [TO FIND] with found sections
                pattern = f"### \\d+\\. {re.escape(tracking_name)}.*?\\*\\*Section Number:\\*\\* \\[TO FIND\\]"
                replacement = f"### \\d+\\. {tracking_name}.*?\\*\\*Section Number:\\*\\* {section_str}"
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open('NDAA-SECTION-NUMBERS.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Updated: NDAA-SECTION-NUMBERS.md")
        
    except Exception as e:
        print(f"⚠️  Could not update tracking file: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Scan NDAA document for section numbers')
    parser.add_argument('--file', help='Path to downloaded NDAA text file')
    args = parser.parse_args()
    
    print("🚀 Scanning FY2026 NDAA (S.2296) for section numbers...\n")
    
    # Fetch text
    text = fetch_ndaa_text(file_path=args.file)
    
    if not text:
        print("\n❌ Could not fetch NDAA text automatically.")
        print("\n📋 To use this script:")
        print("1. Go to: https://www.congress.gov/bill/119th-congress/senate-bill/2296/text")
        print("2. Copy the text or download as PDF/text")
        print("3. Save to a file (e.g., ndaa-text.txt)")
        print("4. Run: python3 scan-ndaa-sections.py --file ndaa-text.txt")
        return
    
    # Extract sections
    sections = extract_sections(text)
    
    # Find agency-related sections
    agency_sections = find_agency_sections(text, sections)
    
    # Find small business provisions
    sb_provisions = find_small_business_provisions(text)
    
    # Save results
    save_results(sections, agency_sections, sb_provisions)
    
    print("\n✅ Scan complete!")
    print("\n📋 Next steps:")
    print("1. Review ndaa-sections-extracted.md")
    print("2. Review ndaa-sections-extracted.json for detailed data")
    print("3. Update NDAA-SECTION-NUMBERS.md with verified sections")
    print("4. Move to Step 2: Get Monthly Treasury Statement Data")

if __name__ == '__main__':
    main()
