# SBLO List Research Guide
## Step 2: Public Sources to Scale It (Free, 30 Min)

This guide lists free, public sources to populate your SBLO and Prime Contractor contact database.

---

## 1. SBA Prime Directory (300+ Primes)

**Source:** https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans

**Last Updated:** March 4, 2025

**Format:** Excel file

**Data Includes:**
- Prime Name
- Location
- PSC/NAICS codes
- Contract Numbers
- SBLO Contact (if listed; otherwise search prime's website)

**How to Use:**
1. Download the Excel file from the link above
2. Open in Excel/Google Sheets
3. Extract columns: Prime Name, Location, PSC/NAICS, Contract #, SBLO Contact
4. For missing SBLO contacts, visit the prime's website and search for "small business" or "supplier diversity"

---

## 2. DoD CSP Prime Directory (100+ DoD Primes)

**Source:** https://business.defense.gov/Portals/57/Documents/Dod%20CSP%20Prime%20Contractor%20Directory_May%202025.pdf

**Last Updated:** May 2025

**Format:** PDF/Excel

**Data Includes:**
- SBLO names
- Phone numbers
- Company information

**Example:**
- BAE Systems: Marianne Tenore, SBLO, 703-xxx-xxxx

**How to Use:**
1. Download the PDF/Excel from the link
2. Extract SBLO names and contact information
3. Cross-reference with company websites for email addresses
4. Update `sblo-list.html` and `sblo-list.csv` with prime contractor section

---

## 3. DHS Prime Contractors List (50+ Primes)

**Source:** https://www.dhs.gov/osdbu/prime-contractors

**Last Updated:** March 17, 2025

**Data Includes:**
- Prime contractor names
- SBLO email addresses (often directly listed)

**Example:**
- Accenture: smallbusiness@accenturefederal.com

**How to Use:**
1. Visit the DHS OSDBU page
2. Download or copy the prime contractors list
3. Extract company names and SBLO emails
4. Look for additional contact info (phone, address) on company websites

---

## 4. SUBNet (SBA Subcontracting Network)

**Source:** https://www.sba.gov/federal-contracting/contracting-guide/prime-subcontracting/subcontracting-opportunities

**Features:**
- Real-time subcontracting opportunity postings
- Filter by state/NAICS
- Primes are required to post opportunities here

**How to Use:**
1. Create a free account on SBA.gov
2. Navigate to SUBNet
3. Filter by:
   - Your state
   - Your NAICS codes
   - Contract type
4. Note the prime contractor contacts from postings
5. Add to your SBLO list

---

## 5. DOT Subcontracting Directory (FY2025)

**Source:** https://www.transportation.gov/osdbu/procurement-assistance/dot-subcontracting-directory

**Data Includes:**
- 100+ prime contractors
- SBLO names
- Phone numbers
- Company information

**How to Use:**
1. Download the directory
2. Extract SBLO contacts
3. Cross-reference for email addresses on company websites
4. Add to your database

---

## Additional Resources

### Agency Small Business Offices

**GSA Office of Small Business Utilization:**
- https://www.gsa.gov/about-us/organization/office-of-small-business-utilization-osbu
- Contact directory available

**NASA Office of Small Business Programs:**
- https://www.nasa.gov/offices/osbp/home/index.html
- Prime contractor list with SBLO contacts

**VA Office of Small & Disadvantaged Business Utilization:**
- https://www.va.gov/osdbu/
- Prime contractor directory

**HHS Office of Small and Disadvantaged Business Utilization:**
- https://www.hhs.gov/about/agencies/asfr/ogapa/osdbu/index.html
- Supplier directory

---

## Quick Research Workflow (30 Minutes)

1. **Download Resources (10 min):**
   - SBA Prime Directory Excel
   - DoD CSP Prime Directory PDF
   - DHS Prime Contractors List (copy from website)

2. **Extract Contacts (15 min):**
   - Open Excel files
   - Copy SBLO names, emails, phones
   - Note missing information

3. **Fill Gaps (5 min):**
   - Visit company websites for missing emails
   - Search "[Company Name] small business liaison"
   - Check LinkedIn for SBLO contacts

---

## Data Fields to Collect

For each prime contractor, collect:
- ✅ Company Name
- ✅ SBLO Name
- ✅ SBLO Title
- ✅ Email Address
- ✅ Phone Number
- ✅ Website
- ✅ NAICS Codes
- ✅ Location/Address
- ✅ Agency/Program Focus
- ✅ Notes (capabilities, set-asides, etc.)

---

## Import Template

Use the `sblo-list.csv` file structure:
- Column headers match the data fields above
- Can import into Excel, Google Sheets, or database
- Easy to merge with existing contacts

---

## Next Steps

1. Download all source files listed above
2. Extract contact information systematically
3. Update `sblo-list.csv` with new contacts
4. Verify emails by checking company websites
5. Export updated list to HTML for distribution

---

## Tips for Success

- **Verify contacts:** Don't rely solely on directory info—verify on company websites
- **Update regularly:** These directories update quarterly/semi-annually
- **Build relationships:** Once you have contacts, follow up with warm intro emails
- **Track responses:** Keep notes on who responds and when
- **Categorize:** Organize by agency, NAICS code, or opportunity type

---

## Automation Ideas

- **Web scraping:** Use tools like Python/BeautifulSoup to extract data from web pages
- **API integration:** Some agencies offer APIs for contractor data
- **CRM import:** Export CSV to Salesforce, HubSpot, or similar CRM systems
- **Email verification:** Use tools like Hunter.io or EmailHippo to verify email addresses




