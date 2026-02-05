#!/usr/bin/env python3
"""
Regenerate the embedded JavaScript companies array in the HTML database file
from the updated CSV file, including vendor portal information.
"""

import csv
import json
import re
import os

def convert_value(value):
    """Convert CSV value to appropriate JavaScript type."""
    if not value or value.strip() == '':
        return None
    
    value = value.strip()
    
    # Try to convert to number
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        pass
    
    # Boolean strings
    if value.upper() == 'TRUE':
        return True
    if value.upper() == 'FALSE':
        return False
    
    # Return as string
    return value

def csv_to_js_array(csv_file):
    """Convert CSV file to JavaScript array format."""
    companies = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            company = {}
            
            # Process each field
            for key, value in row.items():
                # Skip empty vendor portal fields for cleaner output
                if key.startswith('vendor_') and (not value or value.strip() == ''):
                    continue
                
                converted_value = convert_value(value)
                if converted_value is not None and converted_value != '':
                    company[key] = converted_value
            
            # Add computed fields that might be used by the HTML
            company['has_email'] = bool(company.get('email', ''))
            company['has_phone'] = bool(company.get('phone', ''))
            company['has_contact'] = bool(company.get('sblo_name', '') or company.get('email', ''))
            
            # Convert contract_value to number
            if 'total_contract_value' in company:
                try:
                    company['contract_value_num'] = float(company['total_contract_value'])
                except (ValueError, TypeError):
                    company['contract_value_num'] = 0.0
            
            companies.append(company)
    
    return companies

def generate_js_array(companies):
    """Generate JavaScript array string from companies list."""
    # Use json.dumps with proper formatting for JavaScript
    js_array = 'const companies = [\n'
    
    for i, company in enumerate(companies):
        # Convert to JSON with 2-space indent
        company_json = json.dumps(company, indent=2, ensure_ascii=False)
        # Add extra indent (2 more spaces) for array elements
        indented_json = '\n'.join('  ' + line if line else line for line in company_json.split('\n'))
        
        js_array += indented_json
        
        if i < len(companies) - 1:
            js_array += ','
        js_array += '\n'
    
    js_array += '];\n'
    
    return js_array

def update_html_file(html_file, csv_file):
    """Update HTML file with regenerated companies array from CSV."""
    print(f"Reading CSV file: {csv_file}")
    companies = csv_to_js_array(csv_file)
    print(f"Loaded {len(companies)} companies from CSV")
    
    # Count companies with vendor portals
    with_portals = sum(1 for c in companies if c.get('vendor_registration_url', '').strip())
    print(f"  - {with_portals} companies have vendor portal information")
    
    print(f"\nReading HTML file: {html_file}")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the companies array in the HTML
    # Pattern: const companies = [ ... ];
    pattern = r'(const companies = \[)(.*?)(\];)'
    
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("❌ Error: Could not find 'const companies = [...]' in HTML file")
        return False
    
    # Generate new JavaScript array
    print("Generating JavaScript array...")
    new_js_array = generate_js_array(companies)
    
    # Replace the array content (keep const companies = [ and ];)
    new_content = content[:match.start()] + new_js_array + content[match.end():]
    
    # Write updated HTML
    print(f"Writing updated HTML file...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Successfully updated {html_file}")
    return True

def main():
    """Main function."""
    csv_file = 'FEDERAL-CONTRACTOR-MASTER-DATABASE.csv'
    html_file = 'federal-contractor-database/index.html'
    
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found")
        return
    
    if not os.path.exists(html_file):
        print(f"❌ Error: {html_file} not found")
        return
    
    print("=" * 60)
    print("Regenerating HTML Database from CSV")
    print("=" * 60)
    print()
    
    success = update_html_file(html_file, csv_file)
    
    print()
    print("=" * 60)
    if success:
        print("✅ HTML database regenerated successfully!")
        print(f"   Open {html_file} in a browser to see vendor portal information")
    else:
        print("❌ Failed to regenerate HTML database")
    print("=" * 60)

if __name__ == '__main__':
    main()

