#!/usr/bin/env python3
"""
Update hit list HTML files for new month
Replaces month/year references in hit list files
"""

import os
import re
import sys
from datetime import datetime

def update_month_in_file(filepath, old_month, new_month, old_year=None, new_year=None):
    """Update month/year references in an HTML file"""
    
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return False
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update month references (case-insensitive)
        content = re.sub(
            rf'\b{old_month}\b',
            new_month,
            content,
            flags=re.IGNORECASE
        )
        
        # Update year references if provided
        if old_year and new_year:
            content = re.sub(
                rf'\b{old_year}\b',
                new_year,
                content
            )
        
        # Update in title tags
        content = re.sub(
            rf'<title>.*?{old_month}.*?</title>',
            lambda m: m.group(0).replace(old_month, new_month).replace(old_year or '', new_year or ''),
            content,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # Update in h1/h2 headers
        content = re.sub(
            rf'<h[12][^>]*>.*?{old_month}.*?</h[12]>',
            lambda m: m.group(0).replace(old_month, new_month).replace(old_year or '', new_year or ''),
            content,
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {filepath}")
            return True
        else:
            print(f"ℹ️  No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def rename_file(old_path, new_path):
    """Rename a file"""
    try:
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"✅ Renamed: {old_path} → {new_path}")
            return True
        else:
            print(f"⚠️  File not found: {old_path}")
            return False
    except Exception as e:
        print(f"❌ Error renaming {old_path}: {e}")
        return False

def main():
    """Main function to update hit lists for new month"""
    
    if len(sys.argv) < 3:
        print("Usage: python3 update-hit-lists-for-month.py <old_month> <new_month> [old_year] [new_year]")
        print("\nExample:")
        print("  python3 update-hit-lists-for-month.py December January 2025 2026")
        print("  python3 update-hit-lists-for-month.py December January")
        sys.exit(1)
    
    old_month = sys.argv[1]
    new_month = sys.argv[2]
    old_year = sys.argv[3] if len(sys.argv) > 3 else None
    new_year = sys.argv[4] if len(sys.argv) > 4 else None
    
    # If year not provided, try to infer from current date
    if not old_year or not new_year:
        current_year = datetime.now().year
        # Assume old month is previous month, new month is current
        old_year = str(current_year - 1) if old_month == "December" else str(current_year)
        new_year = str(current_year)
    
    print(f"🔄 Updating hit lists:")
    print(f"   From: {old_month} {old_year}")
    print(f"   To:   {new_month} {new_year}")
    print()
    
    # List of hit list files to update
    hit_list_files = [
        'december-hit-list-complete.html',
        'december-hit-list-beginner.html',
        'december-hit-list.html',
        'december-hit-list-general-contractors.html',
        'december-hit-list-real-opportunities.html',
    ]
    
    # List of spend forecast files
    spend_forecast_files = [
        'december-spend-forecast.html',
    ]
    
    updated_count = 0
    
    # Update hit list files
    print("📋 Updating hit list files...")
    for filename in hit_list_files:
        if os.path.exists(filename):
            # Update content
            if update_month_in_file(filename, old_month, new_month, old_year, new_year):
                updated_count += 1
            
            # Rename file
            new_filename = filename.replace(old_month.lower(), new_month.lower())
            rename_file(filename, new_filename)
        else:
            print(f"⚠️  File not found: {filename}")
    
    # Update spend forecast files
    print("\n📊 Updating spend forecast files...")
    for filename in spend_forecast_files:
        if os.path.exists(filename):
            # Update content
            if update_month_in_file(filename, old_month, new_month, old_year, new_year):
                updated_count += 1
            
            # Rename file
            new_filename = filename.replace(old_month.lower(), new_month.lower())
            rename_file(filename, new_filename)
        else:
            print(f"⚠️  File not found: {filename}")
    
    print(f"\n✅ Update complete!")
    print(f"   Updated {updated_count} files")
    print(f"\n📝 Next steps:")
    print(f"   1. Review updated files")
    print(f"   2. Generate new hit lists from fresh CSV data")
    print(f"   3. Update any hardcoded dates")
    print(f"   4. Test all links")

if __name__ == '__main__':
    main()
