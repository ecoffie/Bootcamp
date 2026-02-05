#!/usr/bin/env python3
"""
Parse DHS Prime Contractors page and extract all SBLO contacts
Based on content from: https://www.dhs.gov/osdbu/prime-contractors
"""

import csv
import re
from pathlib import Path

# DHS Prime Contractors data extracted from the page
DHS_DATA = """
AArete | Small Business Liaison: Lynn Jenkins | ljenkins@aarete.com, 312-288-5114 | www.AArete.com | 541519, 541511, 541611
ABS Group Consulting | Small Business Liaison: Ruta Haile | rhaile@absconsulting.com | Small Business Liaison: Michael Loveless | mloveless@absconsulting.com | https://www.abs-group.com/Markets-We-Serve/Government/ | 541611, 541512, 541330, 541690
Accenture | Small Business Liaison: Irene Rivera | irene.c.rivera@accenturefederal.com | www.accenture.com/
Acuity International | Small Business Liaison: Susan Thibodeaux | Susan.Thibodeaux@acuityinternational.com | https://acuityinternational.com
AECOM | Small Business Liaison: Shawn Ralston | Shawn.ralston@aecom.com | www.aecom.com/ | Contracts: HSFEHQ12D0882, HSFE6015D0003, 70FB8018D00000012, 70Z05018DAECOMT06, HSCG5014DPSL008
Akima Global Services | Small Business Liaison: Heidi Anderson | Heidi.anderson@akima.com | www.akima.com | 561612, 561210
Amentum | Small Business Liaison Officer: Rochelle Lowe | SBLO@Amentum.com | https://www.amentum.com/supplier-diversity/
APTIM | Small Business Liaison: Ellen Mack | ellen.mack@aptim.com
BAE Systems Intelligence & Security | Dawn Dunlop | (703) 873-3895 | Dawn.Dunlop@baesystems.com | http://www.baesystems.com/supplierdiversity
Battelle National Biodefense Institute, LLC | Small Business Liaison: Rodney Templo
Loyal Source | Small Business Liaison: Chad Janovec | cjanovec@loyalsource.com | http://www.loyalsource.com/ | 561320
Maximus Federal | Small Business Liaison: Abeer Bhatia | abeerbhatia@maximus.com | http://www.maximus.com/ | 541511, 541512, 541513, 541519
Mantech | Small Business Liaison: Lissa Dunn | lissa.dunn@mantech.com | www.mantech.com | Contracts: EAGLE II FCI, TABBS
McDean | Small Business Liaison: Kathy Athey | Kathy.Athey@mcdean.com | http://www.mcdean.com/ | 511210
Michael Baker Jr., Inc. | Small Business Liaison: Morgan Karimi | morgan.karimi@mbakerintl.com | https://mbakerintl.com/en/ | Contract: FEMA HSFEHQ-04-D0025, Multi Hazard Flood Map Modernization
Mitre | Small Business Liaison: Dakari Motague | dmontague@mitre.org | http://www.mitre.com/ | 541618, 541720, 611430
Monster Government Solutions LLC | Small Business Liaison: Maria Maze | maria.maze@monstergovernmentsolutions.com | 611420
Mortenson | Small Business Liaison: Mike Hommer | Mike.hommer@mortenson.com | http://www.mortenson.com/
M V M, Inc. | Small Business Liaison: Ty Richards | richardsta@mvminc.com | http://www.mvminc.com/ | 561210
Motorola Solutions, Inc. | Supplier Diversity Manager: Edith Moralis | edith.moralis@motorolasolutions.com | https://www.motorolasolutions.com/en_us.html
Neopost Inc. | Small Business Liaison: Stacey Graham | s.graham@quadient.com | http://www.quadient.com/ | 333298
Noblis | Small Business Liaison: Anna Crawley | anna.crawley@noblis.org | https://noblis.org/ | 541330, 541715
Noresco LLC | Small Business Liaison: Gopal Shiddapur | gshiddapur@noresco.com | http://www.noresco.com/ | 541330
Northrop Grumman (Information Technology) | Small Business Liaison: Carla Undurraga | Carla.undurraga@ngc.com | https://www.northropgrumman.com/ | Contract: HSHQDC06D00022
NTTData Federal | Small Business Liaison: Angela Hannah | angela.hannah@nttdatafed.com | http://www.nttdatafed.com/ | 541330, 541519
Paragon Systems | Small Business Liaison: Leslie Kaciban | lkaciban@parasys.com | http://www.parasys.com/ | 561612
Peraton | Small Business Liaison: Ronald Penick | Ronald.penick@peraton.com
Rapiscan | Small Business Liaison: Lakisha Bird | contracts@rapiscansystems.com | http://www.rapiscansystems.com/ | 334517
ReadyAmerica | Small Business Liaison: Neil Chapin | neil@readyamerica.com | http://www.readyamerica.com/ | 311423, 423910, 423450, 339113, 315990, 336212
SAIC | Small Business Liaison: Rita Brooks | Marguerite.brooks@saic.com | http://www.saic.com/sbp
Salient | Small Business Liaison: Debra Vanderhoof | Debra.Vanderhoof@salientcrgt.com | http://www.salientcrgt.com/ | 541512
Serco, Inc. | Deputy Small Business Liaison: Wanda Montague | Wanda.Montague@serco-na.com | www.serco-na.com/ | Contracts: http://www.serco-na.com/contracts
THE BOEING COMPANY | Small Business Liaison: Tina T. Wang | tina.t.wang@boeing.com | www.boeingsuppliers.com
THE GEO GROUP | Small Business Liaison: Ray Castro | racastro@geogroup.com | http://www.geogroup.com/ | Contract No: HSCEMEM-10-D-00001
The Rand Company | Small Business Liaison: Linda Duffy | byone@rand.org, hsoac-operations@rand.org | http://www.rand.org/ | 541720
Triple Canopy | Small Business Liaison: Christopher Philippsen | chris.philippsen@constellis.com | http://www.constellis.com/ | 561612
Verizon | Small Business Liaison: Brandilynn Collins | Brandilynn.collins.garrison@verizon.com | Small Business Liaison: Emily Bien | Emily.bien@verizon.com | www.vsecorp.com | 517312
Whiting-Turner | Small Business Liaison: Joanna Harmon | Joanna.harmon@whiting-turner.com | http://www.whiting-turner.com/ | 236220
WSP | Small Business Liaison: Bernard Fanfan | bernie.fanfan@wsp.com | http://www.wsp.com/ | 541350, All 541 Series
"""

def parse_dhs_data():
    """Parse the DHS data and extract structured contacts"""
    contacts = []
    
    # Parse structured data from the web content
    entries = [
        {"company": "AArete", "sblo_name": "Lynn Jenkins", "email": "ljenkins@aarete.com", "phone": "312-288-5114", "website": "www.AArete.com", "naics": "541519, 541511, 541611"},
        {"company": "ABS Group Consulting", "sblo_name": "Ruta Haile", "email": "rhaile@absconsulting.com", "phone": "", "website": "https://www.abs-group.com/Markets-We-Serve/Government/", "naics": "541611, 541512, 541330, 541690"},
        {"company": "ABS Group Consulting", "sblo_name": "Michael Loveless", "email": "mloveless@absconsulting.com", "phone": "", "website": "https://www.abs-group.com/Markets-We-Serve/Government/", "naics": "541611, 541512, 541330, 541690"},
        {"company": "Accenture", "sblo_name": "Irene Rivera", "email": "irene.c.rivera@accenturefederal.com", "phone": "", "website": "www.accenture.com/", "naics": ""},
        {"company": "Acuity International", "sblo_name": "Susan Thibodeaux", "email": "Susan.Thibodeaux@acuityinternational.com", "phone": "", "website": "https://acuityinternational.com", "naics": ""},
        {"company": "AECOM", "sblo_name": "Shawn Ralston", "email": "Shawn.ralston@aecom.com", "phone": "", "website": "www.aecom.com/", "naics": ""},
        {"company": "Akima Global Services", "sblo_name": "Heidi Anderson", "email": "Heidi.anderson@akima.com", "phone": "", "website": "www.akima.com", "naics": "561612, 561210"},
        {"company": "Amentum", "sblo_name": "Rochelle Lowe", "email": "SBLO@Amentum.com", "phone": "", "website": "https://www.amentum.com/supplier-diversity/", "naics": ""},
        {"company": "APTIM", "sblo_name": "Ellen Mack", "email": "ellen.mack@aptim.com", "phone": "", "website": "", "naics": ""},
        {"company": "BAE Systems Intelligence & Security", "sblo_name": "Dawn Dunlop", "email": "Dawn.Dunlop@baesystems.com", "phone": "(703) 873-3895", "website": "http://www.baesystems.com/supplierdiversity", "naics": ""},
        {"company": "Loyal Source", "sblo_name": "Chad Janovec", "email": "cjanovec@loyalsource.com", "phone": "", "website": "http://www.loyalsource.com/", "naics": "561320"},
        {"company": "Maximus Federal", "sblo_name": "Abeer Bhatia", "email": "abeerbhatia@maximus.com", "phone": "", "website": "http://www.maximus.com/", "naics": "541511, 541512, 541513, 541519"},
        {"company": "Mantech", "sblo_name": "Lissa Dunn", "email": "lissa.dunn@mantech.com", "phone": "", "website": "www.mantech.com", "naics": ""},
        {"company": "McDean", "sblo_name": "Kathy Athey", "email": "Kathy.Athey@mcdean.com", "phone": "", "website": "http://www.mcdean.com/", "naics": "511210"},
        {"company": "Michael Baker Jr., Inc.", "sblo_name": "Morgan Karimi", "email": "morgan.karimi@mbakerintl.com", "phone": "", "website": "https://mbakerintl.com/en/", "naics": ""},
        {"company": "Mitre", "sblo_name": "Dakari Motague", "email": "dmontague@mitre.org", "phone": "", "website": "http://www.mitre.com/", "naics": "541618, 541720, 611430"},
        {"company": "Monster Government Solutions LLC", "sblo_name": "Maria Maze", "email": "maria.maze@monstergovernmentsolutions.com", "phone": "", "website": "", "naics": "611420"},
        {"company": "Mortenson", "sblo_name": "Mike Hommer", "email": "Mike.hommer@mortenson.com", "phone": "", "website": "http://www.mortenson.com/", "naics": ""},
        {"company": "M V M, Inc.", "sblo_name": "Ty Richards", "email": "richardsta@mvminc.com", "phone": "", "website": "http://www.mvminc.com/", "naics": "561210"},
        {"company": "Motorola Solutions, Inc.", "sblo_name": "Edith Moralis", "email": "edith.moralis@motorolasolutions.com", "phone": "", "website": "https://www.motorolasolutions.com/en_us.html", "naics": ""},
        {"company": "Neopost Inc.", "sblo_name": "Stacey Graham", "email": "s.graham@quadient.com", "phone": "", "website": "http://www.quadient.com/", "naics": "333298"},
        {"company": "Noblis", "sblo_name": "Anna Crawley", "email": "anna.crawley@noblis.org", "phone": "", "website": "https://noblis.org/", "naics": "541330, 541715"},
        {"company": "Noresco LLC", "sblo_name": "Gopal Shiddapur", "email": "gshiddapur@noresco.com", "phone": "", "website": "http://www.noresco.com/", "naics": "541330"},
        {"company": "Northrop Grumman (Information Technology)", "sblo_name": "Carla Undurraga", "email": "Carla.undurraga@ngc.com", "phone": "", "website": "https://www.northropgrumman.com/", "naics": ""},
        {"company": "NTTData Federal", "sblo_name": "Angela Hannah", "email": "angela.hannah@nttdatafed.com", "phone": "", "website": "http://www.nttdatafed.com/", "naics": "541330, 541519"},
        {"company": "Paragon Systems", "sblo_name": "Leslie Kaciban", "email": "lkaciban@parasys.com", "phone": "", "website": "http://www.parasys.com/", "naics": "561612"},
        {"company": "Peraton", "sblo_name": "Ronald Penick", "email": "Ronald.penick@peraton.com", "phone": "", "website": "", "naics": ""},
        {"company": "Rapiscan", "sblo_name": "Lakisha Bird", "email": "contracts@rapiscansystems.com", "phone": "", "website": "http://www.rapiscansystems.com/", "naics": "334517"},
        {"company": "ReadyAmerica", "sblo_name": "Neil Chapin", "email": "neil@readyamerica.com", "phone": "", "website": "http://www.readyamerica.com/", "naics": "311423, 423910, 423450, 339113, 315990, 336212"},
        {"company": "SAIC", "sblo_name": "Rita Brooks", "email": "Marguerite.brooks@saic.com", "phone": "", "website": "http://www.saic.com/sbp", "naics": ""},
        {"company": "Salient", "sblo_name": "Debra Vanderhoof", "email": "Debra.Vanderhoof@salientcrgt.com", "phone": "", "website": "http://www.salientcrgt.com/", "naics": "541512"},
        {"company": "Serco, Inc.", "sblo_name": "Wanda Montague", "email": "Wanda.Montague@serco-na.com", "phone": "", "website": "www.serco-na.com/", "naics": ""},
        {"company": "THE BOEING COMPANY", "sblo_name": "Tina T. Wang", "email": "tina.t.wang@boeing.com", "phone": "", "website": "www.boeingsuppliers.com", "naics": ""},
        {"company": "THE GEO GROUP", "sblo_name": "Ray Castro", "email": "racastro@geogroup.com", "phone": "", "website": "http://www.geogroup.com/", "naics": ""},
        {"company": "The Rand Company", "sblo_name": "Linda Duffy", "email": "byone@rand.org", "phone": "", "website": "http://www.rand.org/", "naics": "541720"},
        {"company": "The Rand Company", "sblo_name": "Linda Duffy", "email": "hsoac-operations@rand.org", "phone": "", "website": "http://www.rand.org/", "naics": "541720"},
        {"company": "Triple Canopy", "sblo_name": "Christopher Philippsen", "email": "chris.philippsen@constellis.com", "phone": "", "website": "http://www.constellis.com/", "naics": "561612"},
        {"company": "Verizon", "sblo_name": "Brandilynn Collins", "email": "Brandilynn.collins.garrison@verizon.com", "phone": "", "website": "www.vsecorp.com", "naics": "517312"},
        {"company": "Verizon", "sblo_name": "Emily Bien", "email": "Emily.bien@verizon.com", "phone": "", "website": "www.vsecorp.com", "naics": "517312"},
        {"company": "Whiting-Turner", "sblo_name": "Joanna Harmon", "email": "Joanna.harmon@whiting-turner.com", "phone": "", "website": "http://www.whiting-turner.com/", "naics": "236220"},
        {"company": "WSP", "sblo_name": "Bernard Fanfan", "email": "bernie.fanfan@wsp.com", "phone": "", "website": "http://www.wsp.com/", "naics": "541350"},
    ]
    
    return entries

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   DHS Prime Contractors - Contact Extractor         ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    contacts = parse_dhs_data()
    
    print(f"✅ Extracted {len(contacts)} contacts from DHS page")
    
    # Save to CSV
    output_file = Path('dhs-contacts-extracted.csv')
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['company', 'sblo_name', 'title', 'email', 'phone', 'website', 'naics', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for contact in contacts:
            writer.writerow({
                'company': contact['company'],
                'sblo_name': contact['sblo_name'],
                'title': 'SBLO',
                'email': contact['email'],
                'phone': contact['phone'],
                'website': contact['website'],
                'naics': contact['naics'],
                'source': 'DHS Prime Contractors Page'
            })
    
    print(f"💾 Saved to: {output_file}")
    
    # Update main compiled list
    compiled_file = Path('sblo-list-compiled.csv')
    if compiled_file.exists():
        with open(compiled_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing = list(reader)
        
        # Add new contacts
        existing_emails = {row.get('email', '').lower() for row in existing}
        
        # Read existing fieldnames
        with open(compiled_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_fieldnames = reader.fieldnames
        
        with open(compiled_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=existing_fieldnames)
            for contact in contacts:
                if contact['email'].lower() not in existing_emails:
                    row = {field: '' for field in existing_fieldnames}
                    row['company'] = contact['company']
                    row['sblo_name'] = contact['sblo_name']
                    row['title'] = 'SBLO'
                    row['email'] = contact['email']
                    row['phone'] = contact['phone']
                    row['naics'] = contact['naics']
                    row['source'] = 'DHS Prime Contractors Page'
                    writer.writerow(row)
                    existing_emails.add(contact['email'].lower())
        
        print(f"✅ Updated {compiled_file}")
    
    # Update main SBLO list CSV
    main_csv = Path('sblo-list.csv')
    if main_csv.exists():
        with open(main_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing = list(reader)
        
        existing_companies = {row.get('Agency', '') + row.get('Company Name', '') + row.get('Email', '') for row in existing}
        
        with open(main_csv, 'a', newline='', encoding='utf-8') as f:
            fieldnames_main = ['Agency', 'Office/Program', 'Contact Name', 'Title', 'Email', 'Phone', 'Website', 'Address', 'City', 'State', 'Notes', 'Unobligated Balance (Dec 2025)', 'Key NAICS']
            writer = csv.DictWriter(f, fieldnames=fieldnames_main)
            
            for contact in contacts:
                key = 'Prime Contractor' + contact['company'] + contact['email']
                if key not in existing_companies:
                    writer.writerow({
                        'Agency': 'Prime Contractor',
                        'Office/Program': 'Small Business',
                        'Contact Name': contact['sblo_name'],
                        'Title': 'SBLO',
                        'Email': contact['email'],
                        'Phone': contact['phone'],
                        'Website': contact['website'],
                        'Address': '',
                        'City': '',
                        'State': '',
                        'Notes': f"DHS Prime Contractor - {contact['naics']}",
                        'Unobligated Balance (Dec 2025)': '',
                        'Key NAICS': contact['naics']
                    })
                    existing_companies.add(key)
        
        print(f"✅ Updated {main_csv}")
    
    print("\n" + "="*60)
    print("✨ Extraction Complete!")
    print("="*60)
    print(f"\n📊 Total DHS contacts: {len(contacts)}")
    print("\n📋 Sample contacts:")
    for i, contact in enumerate(contacts[:10]):
        print(f"   {i+1:2d}. {contact['company'][:35]:35s} - {contact['email']}")

if __name__ == '__main__':
    main()

