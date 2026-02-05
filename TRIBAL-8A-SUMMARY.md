# Tribal 8(a) Companies - Summary

## ✅ Setup Complete

I've created a complete toolkit to help you find and compile Tribal 8(a) companies for your prime list.

---

## 📁 Files Created

### Guides & Documentation
1. **TRIBAL-8A-RESEARCH-GUIDE.md** - Complete research guide with all sources and strategies
2. **TRIBAL-8A-QUICK-START.md** - Quick start guide (15-minute workflow)

### Tools & Scripts
3. **find-tribal-8a-companies.py** - Searches your SBA directory for potential tribal companies by name patterns
4. **search-sba-dsbs-tribal-8a.py** - Processes SBA DSBS exports and cross-references with your prime list

### Data Files
5. **tribal-8a-research-template.csv** - 42 potential tribal companies found in your SBA directory

---

## 🔍 Initial Findings

### Potential Tribal Companies Found (42 total)
- **CHEROKEE NATION** - $51.2M ✅ (Verified tribal)
- **PPD DEVELOPMENT LP** - $497.8M (needs verification)
- **CACI ENTERPRISE SOLUTIONS** - $137.2M (needs verification)
- Plus 39 more companies with tribal name patterns

**Note:** These were found by name patterns and need verification through SBA DSBS.

---

## 🎯 Quick Start (15 minutes)

### Step 1: Search SBA DSBS (10 min)
1. Go to: https://web.sba.gov/pro-net/search/dsp_dsbs.cfm
2. Check: ☑ Native American (in Ownership section)
3. Check: ☑ 8(a) Certified (in Certifications section)
4. Click "Search Using These Criteria"
5. Export results to CSV
6. Save as: `sba-dsbs-tribal-8a-export.csv`

### Step 2: Process Export (2 min)
```bash
python3 search-sba-dsbs-tribal-8a.py process sba-dsbs-tribal-8a-export.csv
```

### Step 3: Review Results
- Script creates: `sba-dsbs-tribal-8a-processed.csv`
- Cross-references with your prime list
- Creates: `tribal-8a-in-prime-list.csv` (companies already in your list)

### Step 4: Research SBLO Contacts
- Use same process as other primes
- Add to your SBLO compiled list
- Tag as "Tribal 8(a)" in source column

---

## 📊 Primary Sources

### 1. SBA Dynamic Small Business Search (DSBS) ⭐ PRIMARY
- **URL:** https://web.sba.gov/pro-net/search/dsp_dsbs.cfm
- **Best for:** Verified 8(a) status, contact information
- **Search:** Native American + 8(a) Certified

### 2. USET Tribal Enterprise Directory
- **URL:** https://www.usetinc.org/departments/economic-development/tribal-enterprise-directory/
- **Best for:** Tribal enterprise contacts

### 3. NCAIED
- **URL:** http://www.ncaied.org/
- **Best for:** Networking and business directories

### 4. Alaska Native Corporations (ANCs)
- Search DSBS for: Alaska Native Corporation + 8(a) Certified
- Major ANCs: ASRC, Bristol Bay, Calista, Chugach, Doyon, NANA, Sealaska, etc.

---

## 💡 Why Target Tribal 8(a) Companies?

### Benefits:
- **Sole-source eligibility** up to $4M (services) or $6.5M (manufacturing)
- **No limit** on contract value for tribal/ANC-owned 8(a) companies
- **Set-aside opportunities** in federal contracting
- **Strong relationships** with federal agencies
- **Subcontracting opportunities** for small businesses

### Strategic Value:
- Many tribal 8(a) companies are established primes
- They actively seek small business partners
- Often have dedicated SBLO programs
- High contract values = more subcontracting opportunities

---

## 🔧 Integration with Your Prime List

### Process:
1. Find Tribal 8(a) companies via SBA DSBS
2. Cross-reference with your SBA prime directory
3. Research SBLO contacts (same process as other primes)
4. Add to `sblo-list-compiled.csv`
5. Tag as "Tribal 8(a)" in source column
6. Include tribal affiliation information

### Priority Companies:
- Companies with existing prime contracts
- Companies in your target NAICS codes
- Companies with active SBLO programs
- Companies seeking small business partners

---

## 📋 Next Steps

1. ✅ **Today:** Export from SBA DSBS (Native American + 8(a))
2. ✅ **Today:** Export from SBA DSBS (Alaska Native + 8(a))
3. ✅ **This Week:** Process exports and cross-reference
4. ✅ **This Week:** Research SBLO contacts for top 20 companies
5. ✅ **Ongoing:** Add verified companies to prime list

---

## 📚 Additional Resources

- **SBA 8(a) Program:** https://www.sba.gov/federal-contracting/contracting-assistance-programs/8a-business-development-program
- **Tribal 8(a) Benefits:** https://www.sba.gov/federal-contracting/contracting-assistance-programs/8a-business-development-program/tribal-8a-program
- **SAM.gov:** Search for "Native American" or "Tribal" set-asides
- **FPDS.gov:** Search contracts awarded to tribal 8(a) companies

---

**Status:** ✅ Research toolkit ready  
**Last Updated:** December 2025




