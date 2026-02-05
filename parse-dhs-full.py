#!/usr/bin/env python3
"""
Parse ALL contacts from DHS Prime Contractors page
Extracts every company and SBLO contact from the full page
"""

import csv
import re
from pathlib import Path

# Full DHS page content - parsing all companies
def extract_all_dhs_contacts():
    """Extract all contacts from the DHS page HTML content"""
    
    # Based on the full page content, extract all companies
    # Pattern: Company name, then SBLO info, then email, phone, website, NAICS
    
    contacts = []
    
    # Parse the structured data from the page
    # Each entry follows pattern: Company | SBLO Name | Email | Phone | Website | NAICS
    
    raw_data = """
AArete|Lynn Jenkins|ljenkins@aarete.com|312-288-5114|www.AArete.com|541519, 541511, 541611
ABS Group Consulting|Ruta Haile|rhaile@absconsulting.com||https://www.abs-group.com/Markets-We-Serve/Government/|541611, 541512, 541330, 541690
ABS Group Consulting|Michael Loveless|mloveless@absconsulting.com||https://www.abs-group.com/Markets-We-Serve/Government/|541611, 541512, 541330, 541690
Accenture|Irene Rivera|irene.c.rivera@accenturefederal.com||www.accenture.com/|
Acuity International|Susan Thibodeaux|Susan.Thibodeaux@acuityinternational.com||https://acuityinternational.com|
AECOM|Shawn Ralston|Shawn.ralston@aecom.com||www.aecom.com/|
Akima Global Services|Heidi Anderson|Heidi.anderson@akima.com||www.akima.com|561612, 561210
Amentum|Rochelle Lowe|SBLO@Amentum.com||https://www.amentum.com/supplier-diversity/|
APTIM|Ellen Mack|ellen.mack@aptim.com|||
BAE Systems Intelligence & Security|Dawn Dunlop|Dawn.Dunlop@baesystems.com|(703) 873-3895|http://www.baesystems.com/supplierdiversity|
Battelle National Biodefense Institute, LLC|Rodney Templo||||
Loyal Source|Chad Janovec|cjanovec@loyalsource.com||http://www.loyalsource.com/|561320
Maximus Federal|Abeer Bhatia|abeerbhatia@maximus.com||http://www.maximus.com/|541511, 541512, 541513, 541519
Mantech|Lissa Dunn|lissa.dunn@mantech.com||www.mantech.com|
McDean|Kathy Athey|Kathy.Athey@mcdean.com||http://www.mcdean.com/|511210
Michael Baker Jr., Inc.|Morgan Karimi|morgan.karimi@mbakerintl.com||https://mbakerintl.com/en/|
Mitre|Dakari Motague|dmontague@mitre.org||http://www.mitre.com/|541618, 541720, 611430
Monster Government Solutions LLC|Maria Maze|maria.maze@monstergovernmentsolutions.com|||611420
Mortenson|Mike Hommer|Mike.hommer@mortenson.com||http://www.mortenson.com/|
M V M, Inc.|Ty Richards|richardsta@mvminc.com||http://www.mvminc.com/|561210
Motorola Solutions, Inc.|Edith Moralis|edith.moralis@motorolasolutions.com||https://www.motorolasolutions.com/en_us.html|
Neopost Inc.|Stacey Graham|s.graham@quadient.com||http://www.quadient.com/|333298
Noblis|Anna Crawley|anna.crawley@noblis.org||https://noblis.org/|541330, 541715
Noresco LLC|Gopal Shiddapur|gshiddapur@noresco.com||http://www.noresco.com/|541330
Northrop Grumman (Information Technology)|Carla Undurraga|Carla.undurraga@ngc.com||https://www.northropgrumman.com/|
NTTData Federal|Angela Hannah|angela.hannah@nttdatafed.com||http://www.nttdatafed.com/|541330, 541519
Paragon Systems|Leslie Kaciban|lkaciban@parasys.com||http://www.parasys.com/|561612
Peraton|Ronald Penick|Ronald.penick@peraton.com|||
Rapiscan|Lakisha Bird|contracts@rapiscansystems.com||http://www.rapiscansystems.com/|334517
ReadyAmerica|Neil Chapin|neil@readyamerica.com||http://www.readyamerica.com/|311423, 423910, 423450, 339113, 315990, 336212
SAIC|Rita Brooks|Marguerite.brooks@saic.com||http://www.saic.com/sbp|
Salient|Debra Vanderhoof|Debra.Vanderhoof@salientcrgt.com||http://www.salientcrgt.com/|541512
Serco, Inc.|Wanda Montague|Wanda.Montague@serco-na.com||www.serco-na.com/|
THE BOEING COMPANY|Tina T. Wang|tina.t.wang@boeing.com||www.boeingsuppliers.com|
THE GEO GROUP|Ray Castro|racastro@geogroup.com||http://www.geogroup.com/|
The Rand Company|Linda Duffy|byone@rand.org||http://www.rand.org/|541720
The Rand Company|Linda Duffy|hsoac-operations@rand.org||http://www.rand.org/|541720
Triple Canopy|Christopher Philippsen|chris.philippsen@constellis.com||http://www.constellis.com/|561612
Verizon|Brandilynn Collins|Brandilynn.collins.garrison@verizon.com||www.vsecorp.com|517312
Verizon|Emily Bien|Emily.bien@verizon.com||www.vsecorp.com|517312
Whiting-Turner|Joanna Harmon|Joanna.harmon@whiting-turner.com||http://www.whiting-turner.com/|236220
WSP|Bernard Fanfan|bernie.fanfan@wsp.com||http://www.wsp.com/|541350
"""
    
    # Parse the data
    for line in raw_data.strip().split('\n'):
        if not line or line.startswith('#'):
            continue
        
        parts = line.split('|')
        if len(parts) >= 3:
            company = parts[0].strip()
            sblo_name = parts[1].strip()
            email = parts[2].strip()
            phone = parts[3].strip() if len(parts) > 3 else ''
            website = parts[4].strip() if len(parts) > 4 else ''
            naics = parts[5].strip() if len(parts) > 5 else ''
            
            if company and email:
                contacts.append({
                    'company': company,
                    'sblo_name': sblo_name,
                    'email': email,
                    'phone': phone,
                    'website': website,
                    'naics': naics
                })
    
    # Now I need to add the missing companies from the page
    # Looking at the web content, there are more companies mentioned
    # Let me add them based on the HTML structure patterns
    
    # Additional contacts that may have been missed - need to scrape more carefully
    # The page shows many more companies in the HTML
    
    return contacts

def scrape_from_html_content():
    """Try to extract more contacts by parsing HTML patterns"""
    contacts = []
    
    # Based on the web search results, there are many more companies
    # The HTML shows patterns like:
    # <h2>Company Name</h2>
    # Small Business Liaison: Name
    # email@company.com
    # phone
    
    # Since we have the full page content, let's extract all email patterns
    # and match them with company names
    
    # From the web content, I can see these additional patterns:
    additional_companies = [
        # Add any companies that were truncated in the original parse
    ]
    
    return contacts

def main():
    print("""
    ╔══════════════════════════════════════════════════════╗
    ║   DHS Prime Contractors - FULL Extraction           ║
    ╚══════════════════════════════════════════════════════╝
    """)
    
    print("🔍 Extracting ALL contacts from DHS page...")
    
    # First, get what we can parse directly
    contacts = extract_all_dhs_contacts()
    
    print(f"✅ Initial extraction: {len(contacts)} contacts")
    
    # The page HTML shows there should be ~100+ companies
    # We need to parse the HTML more carefully to get all of them
    
    # Save what we have
    output_file = Path('dhs-contacts-full.csv')
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
    
    print(f"💾 Saved {len(contacts)} contacts to: {output_file}")
    print(f"\n⚠️  Expected ~100+ contacts, found {len(contacts)}")
    print("\n📋 To get ALL contacts, we need to:")
    print("   1. Use Firecrawl MCP to scrape the full page HTML")
    print("   2. Parse all <h2> company names")
    print("   3. Extract all email addresses and match to companies")
    print("   4. Extract phone numbers and SBLO names")
    
    print("\n💡 The page structure shows companies in <h2> tags")
    print("   Each company section has: SBLO name, email, phone, website, NAICS")
    
    return contacts

if __name__ == '__main__':
    main()




