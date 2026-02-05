#!/usr/bin/env python3
"""
Enhance December Spend Forecast with SBLO Contacts
Integrates compiled SBLO list with December forecast opportunities
"""

import csv
from pathlib import Path
import re

def load_sblo_contacts():
    """Load SBLO contacts from compiled list"""
    sblo_file = Path('sblo-list-compiled.csv')
    
    if not sblo_file.exists():
        print(f"❌ SBLO list not found: {sblo_file}")
        return {}
    
    contacts = {}
    with open(sblo_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            company = row.get('company', '').strip()
            if company:
                # Normalize company name
                company_key = company.lower()
                company_key = re.sub(r'\s+(inc|llc|corp|corporation|lp|incorporated)$', '', company_key)
                
                if company_key not in contacts:
                    contacts[company_key] = []
                
                contacts[company_key].append({
                    'company': company,
                    'sblo_name': row.get('sblo_name', ''),
                    'email': row.get('email', ''),
                    'phone': row.get('phone', ''),
                    'naics': row.get('naics', ''),
                    'source': row.get('source', '')
                })
    
    return contacts

def match_companies_to_agencies():
    """Match prime contractors to December forecast agencies"""
    
    # Agency to company mappings based on typical DoD contracts
    agency_mappings = {
        'Army': ['BAE Systems', 'General Dynamics', 'Lockheed Martin', 'Raytheon', 'Northrop Grumman'],
        'Navy': ['Huntington Ingalls', 'Lockheed Martin', 'General Dynamics', 'BAE Systems', 'Raytheon'],
        'Air Force': ['Lockheed Martin', 'Boeing', 'Northrop Grumman', 'Raytheon', 'General Electric', 'Honeywell'],
        'DLA': ['Multiple', 'Various'],
        'MDA': ['Raytheon', 'Lockheed Martin', 'Northrop Grumman', 'Boeing'],
        'Cyber Command': ['Booz Allen Hamilton', 'Leidos', 'CACI', 'SAIC', 'General Dynamics IT'],
        'Space Force': ['Lockheed Martin', 'Boeing', 'Northrop Grumman', 'SpaceX'],
        'DOE': ['Battelle', 'Amentum', 'Fluor', 'Jacobs'],
        'DHP': ['Leidos', 'Cerner', 'General Dynamics IT', 'Booz Allen Hamilton']
    }
    
    return agency_mappings

def create_enhanced_forecast():
    """Create enhanced forecast with SBLO contacts"""
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   Enhancing December Spend Forecast                  ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    # Load SBLO contacts
    print("📊 Loading SBLO contacts...")
    sblo_contacts = load_sblo_contacts()
    print(f"   Loaded {len(sblo_contacts)} companies")
    
    # Agency mappings
    agency_mappings = match_companies_to_agencies()
    
    # December forecast data
    forecast_data = [
        {
            'agency': 'Department of Defense',
            'program': 'Overall DoD',
            'balance': '$38B+',
            'naics': 'IT/Cyber (541512), Engineering (541330), Facilities (561210)',
            'key_primes': ['Booz Allen Hamilton', 'General Dynamics IT', 'Leidos', 'CACI', 'SAIC']
        },
        {
            'agency': 'Army',
            'program': 'Army Procurement',
            'balance': '$10B',
            'naics': 'Ground vehicles, weapons systems, logistics',
            'key_primes': ['BAE Systems', 'General Dynamics', 'Lockheed Martin']
        },
        {
            'agency': 'Navy',
            'program': 'Navy Shipbuilding',
            'balance': '$8B',
            'naics': 'Maritime tech, ship repair, subsystems',
            'key_primes': ['Huntington Ingalls', 'Lockheed Martin', 'General Dynamics']
        },
        {
            'agency': 'Air Force',
            'program': 'Air Force RDT&E',
            'balance': '$7B',
            'naics': 'Aircraft upgrades, space systems, AI prototypes',
            'key_primes': ['Lockheed Martin', 'Boeing', 'Northrop Grumman', 'General Electric', 'Honeywell']
        },
        {
            'agency': 'Defense Logistics Agency',
            'program': 'DLA',
            'balance': '$5B',
            'naics': 'Supply chain, MRO, energy products',
            'key_primes': ['Multiple']
        },
        {
            'agency': 'Missile Defense Agency',
            'program': 'MDA',
            'balance': '$4B',
            'naics': 'Missile tech, sensors, testing',
            'key_primes': ['Raytheon', 'Lockheed Martin', 'Northrop Grumman']
        },
        {
            'agency': 'Cyber Command',
            'program': 'Cyber Command',
            'balance': '$3.5B',
            'naics': 'Cybersecurity, zero trust, cloud migration',
            'key_primes': ['Booz Allen Hamilton', 'Leidos', 'CACI', 'SAIC']
        },
        {
            'agency': 'DOE',
            'program': 'Atomic Energy Defense',
            'balance': '$2.5B',
            'naics': 'Nuclear cleanup, environmental services',
            'key_primes': ['Battelle', 'Amentum', 'Fluor', 'Jacobs']
        },
        {
            'agency': 'Space Force',
            'program': 'Space Force',
            'balance': '$2.8B',
            'naics': 'Satellite support, launch services',
            'key_primes': ['Lockheed Martin', 'Boeing', 'Northrop Grumman']
        },
        {
            'agency': 'Defense Health Program',
            'program': 'DHP',
            'balance': '$2B',
            'naics': 'Medical IT, telehealth, equipment',
            'key_primes': ['Leidos', 'General Dynamics IT', 'Booz Allen Hamilton']
        }
    ]
    
    # Create enhanced list
    enhanced_forecast = []
    
    for forecast in forecast_data:
        agency = forecast['agency']
        primes = forecast['key_primes']
        
        for prime in primes:
            # Find matching SBLO contacts
            prime_key = prime.lower()
            prime_key = re.sub(r'\s+(inc|llc|corp|corporation|lp|incorporated)$', '', prime_key)
            
            contacts_found = []
            if prime_key in sblo_contacts:
                contacts_found = sblo_contacts[prime_key]
            else:
                # Try partial match
                for key, contacts in sblo_contacts.items():
                    if prime_key in key or key in prime_key:
                        contacts_found.extend(contacts)
                        break
            
            if contacts_found:
                for contact in contacts_found[:2]:  # Limit to top 2 contacts per company
                    enhanced_forecast.append({
                        'agency': agency,
                        'program': forecast['program'],
                        'unobligated_balance': forecast['balance'],
                        'hot_naics': forecast['naics'],
                        'prime_contractor': contact['company'],
                        'sblo_name': contact['sblo_name'],
                        'sblo_email': contact['email'],
                        'sblo_phone': contact['phone'],
                        'source': contact['source']
                    })
            else:
                # Add entry without contact (needs research)
                enhanced_forecast.append({
                    'agency': agency,
                    'program': forecast['program'],
                    'unobligated_balance': forecast['balance'],
                    'hot_naics': forecast['naics'],
                    'prime_contractor': prime,
                    'sblo_name': '[NEEDS RESEARCH]',
                    'sblo_email': '[NEEDS RESEARCH]',
                    'sblo_phone': '[NEEDS RESEARCH]',
                    'source': 'December Forecast - Needs Contact Research'
                })
    
    # Save enhanced forecast
    output_file = Path('december-spend-forecast-enhanced.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['agency', 'program', 'unobligated_balance', 'hot_naics', 'prime_contractor',
                     'sblo_name', 'sblo_email', 'sblo_phone', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enhanced_forecast)
    
    print(f"\n💾 Saved enhanced forecast: {output_file}")
    print(f"📊 Total entries: {len(enhanced_forecast)}")
    
    # Statistics
    with_contacts = sum(1 for e in enhanced_forecast if e['sblo_email'] != '[NEEDS RESEARCH]')
    print(f"✅ Entries with SBLO contacts: {with_contacts}")
    print(f"⏳ Entries needing research: {len(enhanced_forecast) - with_contacts}")
    
    # Show sample
    print("\n📋 Sample Enhanced Entries:")
    for entry in enhanced_forecast[:5]:
        if entry['sblo_email'] != '[NEEDS RESEARCH]':
            print(f"   {entry['agency']} - {entry['prime_contractor']}: {entry['sblo_email']}")
    
    return enhanced_forecast

if __name__ == '__main__':
    create_enhanced_forecast()




