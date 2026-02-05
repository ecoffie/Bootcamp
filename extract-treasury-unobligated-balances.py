#!/usr/bin/env python3
"""
Extract unobligated balances from Monthly Treasury Statement data
Supports CSV and Excel files from Treasury.gov
"""

import csv
import sys
import os
import re
from datetime import datetime

# Agency name mappings (Treasury may use different names)
AGENCY_MAPPINGS = {
    'department of defense': 'DoD',
    'dod': 'DoD',
    'defense': 'DoD',
    'army': 'Army',
    'navy': 'Navy',
    'air force': 'Air Force',
    'defense logistics agency': 'DLA',
    'dla': 'DLA',
    'missile defense agency': 'MDA',
    'mda': 'MDA',
    'cyber command': 'Cyber Command',
    'cyber': 'Cyber Command',
    'department of energy': 'DOE',
    'doe': 'DOE',
    'atomic energy': 'DOE',
    'space force': 'Space Force',
    'defense health': 'Defense Health Program',
    'defense health program': 'Defense Health Program',
}

def read_csv_file(file_path):
    """Read CSV file and extract unobligated balances"""
    print(f"📄 Reading CSV file: {file_path}")
    
    balances = {}
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                    # Try to detect delimiter
                    sample = f.read(1024)
                    f.seek(0)
                    
                    sniffer = csv.Sniffer()
                    delimiter = sniffer.sniff(sample).delimiter
                    
                    reader = csv.DictReader(f, delimiter=delimiter)
                    
                    # Look for unobligated balance columns
                    headers = reader.fieldnames
                    print(f"✅ Found columns: {', '.join(headers[:10])}...")
                    
                    # Find relevant columns
                    agency_col = None
                    balance_col = None
                    
                    for col in headers:
                        col_lower = col.lower()
                        if 'agency' in col_lower or 'department' in col_lower or 'organization' in col_lower:
                            agency_col = col
                        if 'unobligated' in col_lower or 'balance' in col_lower or 'unexpended' in col_lower:
                            balance_col = col
                    
                    if not agency_col:
                        print("⚠️  Could not find agency column. Using first column.")
                        agency_col = headers[0] if headers else None
                    
                    if not balance_col:
                        print("⚠️  Could not find unobligated balance column.")
                        print("   Looking for columns with: unobligated, balance, unexpended")
                        # Show columns that might contain balances
                        for col in headers:
                            if any(keyword in col.lower() for keyword in ['balance', 'amount', 'fund', 'obligat', 'unexpend']):
                                print(f"   Possible: {col}")
                    
                    # Extract data
                    for row in reader:
                        if agency_col and row.get(agency_col):
                            agency_name = str(row[agency_col]).strip()
                            
                            # Check if it's one of our target agencies
                            agency_lower = agency_name.lower()
                            matched_agency = None
                            
                            for key, value in AGENCY_MAPPINGS.items():
                                if key in agency_lower:
                                    matched_agency = value
                                    break
                            
                            if matched_agency:
                                balance_value = None
                                if balance_col and row.get(balance_col):
                                    balance_str = str(row[balance_col]).replace('$', '').replace(',', '').strip()
                                    try:
                                        balance_value = float(balance_str)
                                    except:
                                        balance_value = balance_str
                                
                                if matched_agency not in balances:
                                    balances[matched_agency] = []
                                
                                balances[matched_agency].append({
                                    'agency_name': agency_name,
                                    'balance': balance_value,
                                    'raw_row': row
                                })
                
                print(f"✅ Successfully read CSV with {encoding} encoding")
                break
                
            except Exception as e:
                if encoding == encodings[-1]:
                    raise e
                continue
        
        return balances
        
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return None

def read_excel_file(file_path):
    """Read Excel file and extract unobligated balances"""
    print(f"📄 Reading Excel file: {file_path}")
    
    try:
        import pandas as pd
    except ImportError:
        print("❌ pandas not installed. Install with: pip3 install pandas openpyxl")
        return None
    
    balances = {}
    
    try:
        # Read Excel file
        df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets
        
        print(f"✅ Found {len(df)} sheet(s)")
        
        # Process each sheet
        for sheet_name, sheet_df in df.items():
            print(f"  Processing sheet: {sheet_name}")
            
            # Find relevant columns
            headers = [str(col).lower() for col in sheet_df.columns]
            
            agency_col = None
            balance_col = None
            
            for i, col in enumerate(headers):
                if 'agency' in col or 'department' in col or 'organization' in col:
                    agency_col = sheet_df.columns[i]
                if 'unobligated' in col or ('balance' in col and 'unobligated' not in col) or 'unexpended' in col:
                    balance_col = sheet_df.columns[i]
            
            if agency_col:
                for _, row in sheet_df.iterrows():
                    agency_name = str(row[agency_col]).strip() if pd.notna(row[agency_col]) else ''
                    
                    if agency_name:
                        agency_lower = agency_name.lower()
                        matched_agency = None
                        
                        for key, value in AGENCY_MAPPINGS.items():
                            if key in agency_lower:
                                matched_agency = value
                                break
                        
                        if matched_agency:
                            balance_value = None
                            if balance_col and pd.notna(row.get(balance_col)):
                                balance_str = str(row[balance_col]).replace('$', '').replace(',', '').strip()
                                try:
                                    balance_value = float(balance_str)
                                except:
                                    balance_value = balance_str
                            
                            if matched_agency not in balances:
                                balances[matched_agency] = []
                            
                            balances[matched_agency].append({
                                'agency_name': agency_name,
                                'balance': balance_value,
                                'sheet': sheet_name
                            })
        
        return balances
        
    except Exception as e:
        print(f"❌ Error reading Excel: {e}")
        return None

def format_balance(balance):
    """Format balance as currency string"""
    if balance is None:
        return 'N/A'
    
    if isinstance(balance, str):
        return balance
    
    if balance >= 1_000_000_000:
        return f"${balance/1_000_000_000:.1f}B"
    elif balance >= 1_000_000:
        return f"${balance/1_000_000:.1f}M"
    elif balance >= 1_000:
        return f"${balance/1_000:.1f}K"
    else:
        return f"${balance:,.0f}"

def save_results(balances, output_file='treasury-unobligated-balances.csv'):
    """Save extracted balances to CSV"""
    print(f"\n💾 Saving results to: {output_file}")
    
    fieldnames = ['Agency', 'Program', 'Unobligated_Balance', 'Source_Agency_Name', 'Notes']
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for agency, entries in balances.items():
            for entry in entries:
                writer.writerow({
                    'Agency': agency,
                    'Program': entry.get('agency_name', ''),
                    'Unobligated_Balance': format_balance(entry.get('balance')),
                    'Source_Agency_Name': entry.get('agency_name', ''),
                    'Notes': f"From sheet: {entry.get('sheet', 'N/A')}" if 'sheet' in entry else ''
                })
    
    print(f"✅ Saved {len(balances)} agencies to {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract unobligated balances from Treasury Statement')
    parser.add_argument('file', help='Path to Treasury Statement CSV or Excel file')
    parser.add_argument('--output', default='treasury-unobligated-balances.csv', help='Output CSV file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"❌ File not found: {args.file}")
        return
    
    print("🚀 Extracting unobligated balances from Treasury Statement...\n")
    
    # Determine file type and read
    if args.file.lower().endswith('.csv'):
        balances = read_csv_file(args.file)
    elif args.file.lower().endswith(('.xlsx', '.xls')):
        balances = read_excel_file(args.file)
    else:
        print("❌ Unsupported file type. Please provide CSV or Excel file.")
        return
    
    if not balances:
        print("\n⚠️  No balances found. The file may use different column names.")
        print("💡 Tip: Check the file manually and note the column names for 'agency' and 'unobligated balance'")
        return
    
    # Display results
    print("\n📊 Extracted Unobligated Balances:\n")
    for agency, entries in sorted(balances.items()):
        print(f"{agency}:")
        for entry in entries[:3]:  # Show first 3 entries
            balance_str = format_balance(entry.get('balance'))
            print(f"  - {entry.get('agency_name', 'N/A')}: {balance_str}")
        if len(entries) > 3:
            print(f"  ... and {len(entries) - 3} more entries")
        print()
    
    # Save results
    save_results(balances, args.output)
    
    print("\n✅ Extraction complete!")
    print(f"\n📋 Next steps:")
    print(f"1. Review {args.output}")
    print(f"2. Compare balances to December 2025 data")
    print(f"3. Update january-spend-forecast-enhanced.csv with actual balances")

if __name__ == '__main__':
    main()
