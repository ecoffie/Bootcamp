#!/usr/bin/env python3
"""
Update the top 20 SBA companies research list with findings from web research
"""

import csv

# Research findings for top 20 companies
research_findings = {
    "TRIWEST HEALTHCARE ALLIANCE CORP.": {
        "email": "VendorRegistration@TriWest.com",
        "status": "FOUND",
        "notes": "Vendor registration email for small business program"
    },
    "CACI  INC. - FEDERAL": {
        "sblo_name": "Wayne Pizer",
        "email": "smallbusiness@caci.com",
        "status": "FOUND",
        "notes": "Small Business Advocacy Office contact"
    },
    "GENERAL DYNAMICS CORPORATION": {
        "email": "smallbusiness@gd-ms.com; sb@gdls.com",
        "status": "FOUND",
        "notes": "Multiple GD divisions - Mission Systems and Land Systems contacts"
    },
    "MCKESSON CORPORATION": {
        "email": "FederalPrograms@McKesson.com",
        "status": "FOUND",
        "notes": "Federal programs contact for GSA/VA inquiries"
    },
    "NORTHROP GRUMMAN SYSTEMS CORPORATION": {
        "email": "[SEE SBLO LIST PDF]",
        "status": "PARTIAL",
        "notes": "Has SBLO list on website - multiple business units"
    },
    "DELOITTE CONSULTING LLP": {
        "sblo_name": "Tracey Thompson",
        "email": "trthompson@deloitte.com",
        "status": "FOUND",
        "notes": "Small Business Liaison Officer for federal govt subcontracting"
    },
    "GENERAL ATOMIC TECHNOLOGIES CORPORATION": {
        "sblo_name": "Zachary Baur (GA) / Tony Vigo (GA-ASI)",
        "email": "GA-ASI-Small-Business@ga-asi.com",
        "status": "FOUND",
        "notes": "GA-ASI contact; GA corporate SBLO is Zachary Baur"
    },
    "GENERAL DYNAMICS INFORMATION TECHNOLOGY  INC.": {
        "sblo_name": "Ludmilla Parnell",
        "email": "smallbusiness@gdit.com",
        "status": "FOUND",
        "notes": "GDIT Small Business contact"
    },
    "TRIAD NATIONAL SECURITY  LLC": {
        "email": "business@lanl.gov",
        "status": "FOUND",
        "notes": "LANL Small Business Program Office"
    },
    "SCIENCE APPLICATIONS INTERNATIONAL CORPORATION": {
        "sblo_name": "Rita Brooks",
        "email": "margauerite.brooks@saic.com",
        "phone": "(571) 203-6832",
        "status": "FOUND",
        "notes": "Director of Small Business Outreach & Utilization"
    },
    "LEIDOS  INC.": {
        "sblo_name": "Charmaine Edwards",
        "email": "Charmaine.edwards@leidos.com; shaun.k.smith@leidos.com",
        "phone": "(703) 664-4270",
        "status": "FOUND",
        "notes": "Multiple SBLO contacts available"
    },
    "LOCKHEED MARTIN CORPORATION": {
        "email": "supplier.communications@lmco.com",
        "status": "FOUND",
        "notes": "Supplier communications email - SBLOs available by business unit"
    },
    "VERTEX AEROSPACE LLC": {
        "email": "info@vertexaerospace.com",
        "status": "PARTIAL",
        "notes": "General contact - request SBLO contact"
    },
    "HUNTINGTON INGALLS INC": {
        "email": "info@hii-co.com",
        "status": "PARTIAL",
        "notes": "General contact - Ingalls has Small Business Office (SEBP)"
    },
    "INTUITIVE MACHINES  LLC": {
        "email": "[NEEDS RESEARCH]",
        "status": "PENDING",
        "notes": "New NASA contractor - contact through website or SAM.gov"
    }
}

# Read the existing research file
input_file = '/Users/ericcoffie/Bootcamp/sba-top-100-research-list.csv'
output_file = '/Users/ericcoffie/Bootcamp/sba-top-20-updated-research.csv'

with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Update the first 20 rows with research findings
updated_count = 0
for i, row in enumerate(rows[:20]):
    company = row['company']

    if company in research_findings:
        findings = research_findings[company]

        # Update fields with findings
        if 'sblo_name' in findings:
            row['sblo_name'] = findings['sblo_name']
        if 'email' in findings:
            row['email'] = findings['email']
        if 'phone' in findings:
            row['phone'] = findings['phone']
        if 'status' in findings:
            row['research_status'] = findings['status']
        if 'notes' in findings:
            row['research_notes'] = findings['notes']

        updated_count += 1
        print(f"✅ Updated: {company}")
    else:
        print(f"⏭️  Skipped: {company} (no new data)")

# Write updated data
with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    if rows:
        fieldnames = rows[0].keys()
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows[:20])  # Only write top 20

print(f"\n✅ Updated {updated_count} companies out of 20")
print(f"📄 Output file: {output_file}")
