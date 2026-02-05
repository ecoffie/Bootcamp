# Vendor Portal Research Guide

## Overview
This guide outlines the process for finding vendor registration/supplier portals for **393 companies** (225 Tier 1 + 168 Tier 2).

## Files Created
1. **priority-vendor-portal-searches.csv** - 29 major prime contractors (START HERE)
2. **tier1-vendor-portal-searches.csv** - All 225 Tier 1 companies
3. **tier2-vendor-portal-searches.csv** - All 168 Tier 2 companies

---

## Research Strategy

### Phase 1: Priority Companies (29 companies)
**Focus on major defense/IT primes first** - these have the most established portals:

Major Companies Include:
- Lockheed Martin
- Raytheon/RTX
- Boeing
- Northrop Grumman
- General Dynamics (GDIT)
- Booz Allen Hamilton
- Leidos
- SAIC
- BAE Systems
- L3Harris
- Accenture
- Deloitte
- KPMG
- IBM
- Amentum
- Jacobs Engineering
- AECOM
- Fluor
- Peraton
- CACI
- ManTech

### Phase 2: Remaining Tier 1 (196 companies)
Mid-size prime contractors with established vendor programs

### Phase 3: Tier 2 (168 companies)
Subcontractors - may not all have formal portals

---

## Common Vendor Portal URL Patterns

### Standard Locations:
```
https://supplier.company.com
https://suppliers.company.com
https://vendor.company.com
https://vendors.company.com
https://portal.company.com
https://sourcing.company.com
```

### Path-Based:
```
https://company.com/suppliers
https://company.com/vendors
https://company.com/small-business
https://company.com/smallbusiness
https://company.com/subcontractors
https://company.com/procurement
https://company.com/sourcing
https://company.com/supplier-diversity
https://company.com/supply-chain
```

### Federal-Specific:
```
https://companyfederal.com/suppliers
https://company.com/government/suppliers
https://company.com/federal/small-business
```

---

## Search Query Templates

### Primary Query:
```
"[Company Name]" supplier portal vendor registration
```

### Alternative Queries:
```
"[Company Name]" supplier registration
"[Company Name]" vendor portal
"[Company Name]" small business portal
"[Company Name]" subcontractor registration
"[Company Name]" become a supplier
site:[company.com] supplier registration
```

---

## What to Look For

### Positive Indicators:
- ✅ "Supplier Registration" page
- ✅ "Vendor Portal" link
- ✅ "Become a Supplier" section
- ✅ "Small Business Program" page with registration
- ✅ "Subcontractor Opportunities" with portal link
- ✅ Login page for supplier portal
- ✅ "Supplier Diversity" page with registration info

### Red Flags:
- ❌ Generic contact us page with no portal
- ❌ Recruiting/careers page (wrong type of portal)
- ❌ Customer support portal (not supplier)
- ❌ Press releases about suppliers (not a portal)

---

## Data to Capture

For each company, record:

1. **vendor_registration_url** - Direct link to registration/portal
2. **portal_type** - Type of portal found:
   - "Full Portal" - Complete online registration system
   - "Email Registration" - Email-based process
   - "Contact Form" - Web form to request info
   - "PDF Form" - Downloadable form
   - "None Found" - No public portal available
3. **notes** - Additional info:
   - Login requirements
   - Special certifications needed
   - Application process details
   - Alternative contact methods

---

## Automation Approach

### Option 1: Manual Research (Most Accurate)
- Search each company individually
- Verify portal is active
- Test registration process
- **Time: ~5-10 min per company = 33-66 hours total**

### Option 2: Automated Web Search (Faster)
- Use web search API
- Extract likely URLs
- Manual verification of results
- **Time: ~2-3 min per company = 13-20 hours total**

### Option 3: Hybrid (Recommended)
- Automate initial search
- Manual verification for high-priority
- Batch process low-priority
- **Time: ~3-4 min per company = 20-26 hours total**

---

## Progress Tracking

### Batch Processing Recommendation:
- **Batch 1:** 29 priority companies (2-3 hours)
- **Batch 2:** Next 50 Tier 1 companies (3-4 hours)
- **Batch 3:** Next 50 Tier 1 companies (3-4 hours)
- **Batch 4:** Remaining Tier 1 (96 companies, 5-6 hours)
- **Batch 5:** Top 50 Tier 2 companies (3-4 hours)
- **Batch 6:** Remaining Tier 2 (118 companies, 6-8 hours)

**Total estimated time: 22-32 hours**

---

## Known Vendor Portals (Examples)

### Major Defense Contractors:
- **Lockheed Martin:** https://www.lockheedmartin.com/en-us/suppliers.html
- **Raytheon/RTX:** https://www.rtx.com/suppliers
- **Boeing:** https://www.boeing.com/company/about-bca/california-suppliers
- **Northrop Grumman:** https://www.northropgrumman.com/suppliers/
- **General Dynamics:** https://www.gd.com/suppliers

### Major IT/Consulting:
- **Booz Allen Hamilton:** Small business team via email
- **Leidos:** https://www.leidos.com/partnerships
- **SAIC:** https://www.saic.com/small-business
- **Accenture Federal:** Contact SBLO team
- **Deloitte:** https://www2.deloitte.com/us/en/pages/operations/solutions/supplier-management.html

---

## Next Steps

1. ✅ **Start with priority list** (priority-vendor-portal-searches.csv)
2. **Use web search** to find portals
3. **Record findings** in spreadsheet
4. **Verify top portals** manually
5. **Merge results** back into main SBLO lists
6. **Create final deliverable** with vendor portal URLs added

---

## Tips for Success

1. **Check company website first** - Many have "Suppliers" link in footer
2. **Look for federal/government divisions** - Separate portals for gov't business
3. **Check Supplier Diversity pages** - Often have small business registration
4. **Search for "SBLO" contact** - Small Business Liaison Officer pages often link to portal
5. **Try variations** - Some use "partners", "alliance", "ecosystem" instead of "suppliers"
6. **Check recent** - Some portals have moved or been updated

---

*Created: December 2025*
*Companies to research: 393*
*Estimated completion: 20-32 hours*
