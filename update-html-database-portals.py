#!/usr/bin/env python3
"""
Update the HTML database file to include vendor portal information in company details.
This script adds vendor portal display to the HTML template.
"""

import re
import os

def update_html_database():
    """Add vendor portal display to the HTML database."""
    html_file = 'federal-contractor-database/index.html'
    
    if not os.path.exists(html_file):
        print(f"❌ Error: {html_file} not found")
        return
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the section where company details are displayed (after NAICS codes)
    # Look for the pattern where NAICS codes are displayed, then add vendor portal info after
    naics_pattern = r'(?P<naics_section>                    \$\{naicsCodes \? `\s*<div class="detail">\s*<div class="detail-label">NAICS Codes</div>\s*<div class="detail-value">\s*\$\{naicsCodes\}\s*\$\{moreNaics > 0 \? `<span class="naics-code">\+\$\{moreNaics\}</span>` : ''\}\s*</div>\s*</div>\s*` : ''\})'
    
    vendor_portal_section = '''                    ${company.vendor_registration_url && company.vendor_registration_url !== 'Contact SBLO directly' ? `
                        <div class="detail">
                            <div class="detail-label">Vendor Portal</div>
                            <div class="detail-value">
                                <a href="${company.vendor_registration_url}" target="_blank" rel="noopener noreferrer" style="color: #7c3aed; font-weight: 600; text-decoration: none;">
                                    ${company.vendor_registration_url}
                                </a>
                                ${company.vendor_portal_type ? `<span class="badge" style="margin-left: 8px; background: #dcfce7; color: #166534;">${company.vendor_portal_type}</span>` : ''}
                                ${company.vendor_portal_notes ? `<div style="margin-top: 6px; font-size: 12px; color: #64748b;">${company.vendor_portal_notes.substring(0, 100)}${company.vendor_portal_notes.length > 100 ? '...' : ''}</div>` : ''}
                            </div>
                        </div>
                    ` : ''}
                    ${company.vendor_registration_url === 'Contact SBLO directly' ? `
                        <div class="detail">
                            <div class="detail-label">Vendor Registration</div>
                            <div class="detail-value">
                                <span class="badge" style="background: #fef3c7; color: #92400e;">Contact SBLO</span>
                                <span style="margin-left: 8px; font-size: 12px; color: #64748b;">Direct contact required for vendor registration</span>
                            </div>
                        </div>
                    ` : ''}'''
    
    # Check if vendor portal section already exists
    if 'vendor_registration_url' in content and 'Vendor Portal' in content:
        print("✅ HTML database already has vendor portal information")
        return
    
    # Find the NAICS section and add vendor portal info after it
    match = re.search(naics_pattern, content, re.DOTALL)
    
    if match:
        # Insert vendor portal section after NAICS
        new_content = content[:match.end()] + '\n' + vendor_portal_section + '\n' + content[match.end():]
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Updated HTML database with vendor portal display")
        print(f"   File: {html_file}")
        print("   Added vendor portal information to company detail cards")
    else:
        # Try alternative pattern - look for closing divs after details
        alt_pattern = r'(\s+</div>\s+</div>\s+`;\s*\n\s*}).join\(.*?\);'
        
        # If that doesn't work, find the detail section more generally
        detail_closing = r'                    \$\{naicsCodes \? `.*?</div>\s*</div>\s*` : ''\}\s*</div>'
        
        match = re.search(detail_closing, content, re.DOTALL)
        if match:
            # Insert before the closing </div> of company-details
            insert_pos = content.rfind('</div>', 0, match.end())
            if insert_pos > 0:
                new_content = content[:insert_pos] + '\n' + vendor_portal_section + '\n                    ' + content[insert_pos:]
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print("✅ Updated HTML database with vendor portal display")
            else:
                print("⚠️  Could not find insertion point. Manual update may be required.")
        else:
            print("⚠️  Could not find NAICS section. The HTML structure may be different.")
            print("   Vendor portal data is in CSV, but HTML display needs manual update.")

def main():
    """Main function."""
    print("Updating HTML database with vendor portal information...")
    print("=" * 60)
    update_html_database()
    print("=" * 60)

if __name__ == '__main__':
    main()

