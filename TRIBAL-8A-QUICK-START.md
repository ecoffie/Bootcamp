# Tribal 8(a) Companies - Quick Start Guide

## 🎯 Goal
Find and compile a list of Tribal 8(a) companies to add to your prime contractor list.

---

## ⚡ Quick Steps (15 minutes)

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

### Step 3: Cross-Reference (automatic)
The script will automatically:
- ✅ Process the export
- ✅ Cross-reference with your prime list
- ✅ Create `tribal-8a-in-prime-list.csv` with matches

### Step 4: Research SBLO Contacts (ongoing)
- Use same process as other primes
- Add to your SBLO compiled list
- Tag as "Tribal 8(a)" in source column

---

## 📊 What You'll Get

### Files Created:
- `sba-dsbs-tribal-8a-processed.csv` - All tribal 8(a) companies from DSBS
- `tribal-8a-in-prime-list.csv` - Companies already in your prime list
- `tribal-8a-research-template.csv` - Potential tribal companies (by name patterns)

### Current Status:
- ✅ Found 42 potential tribal companies by name patterns
- ⏳ Need SBA DSBS export for verified list
- ⏳ Need SBLO contact research

---

## 🔍 Additional Searches

### Alaska Native Corporations (ANCs)
1. Same SBA DSBS search
2. Check: ☑ Alaska Native Corporation
3. Check: ☑ 8(a) Certified
4. Export and process

### By NAICS Code
Add NAICS filter to narrow by industry:
- 541330 (Engineering Services)
- 541511 (Custom Computer Programming)
- 541512 (Computer Systems Design)
- 541519 (Other Computer Related Services)
- 541611 (Administrative Management)
- 541690 (Other Consulting Services)

---

## 📋 Known Tribal Companies Found

From your SBA directory (need verification):
1. **CHEROKEE NATION** - $51.2M ✅ Verified tribal
2. PPD DEVELOPMENT LP - $497.8M (needs verification)
3. CACI ENTERPRISE SOLUTIONS - $137.2M (needs verification)
4. Plus 39 more potential matches

---

## 🎯 Priority Actions

1. **Today:** Export from SBA DSBS (Native American + 8(a))
2. **Today:** Export from SBA DSBS (Alaska Native + 8(a))
3. **This Week:** Process exports and cross-reference
4. **This Week:** Research SBLO contacts for top 20 companies
5. **Ongoing:** Add verified companies to prime list

---

## 📚 Full Guide

See `TRIBAL-8A-RESEARCH-GUIDE.md` for complete details.

---

**Last Updated:** December 2025




