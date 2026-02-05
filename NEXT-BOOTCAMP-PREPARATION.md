# 🚀 Next Bootcamp Preparation Checklist

## 📅 Pre-Bootcamp Timeline

**Recommended: Start 2-3 weeks before bootcamp date**

---

## ✅ Essential Materials to Update

### 1. Contract Opportunity Hit Lists ⭐ CRITICAL

**December Files (5 total):**
- `december-hit-list-complete.html` - Combined beginner + low competition
- `december-hit-list-beginner.html` - 10 beginner-friendly opportunities
- `december-hit-list.html` - 34 low competition opportunities
- `december-hit-list-general-contractors.html` - GC-specific opportunities
- `december-hit-list-real-opportunities.html` - Top 30 real opportunities

**January Files (currently 1 - needs to be recreated):**
- `january-hit-list.html` - ⚠️ Currently contains sample/template data (needs real data)
- ❌ Missing: `january-hit-list-beginner.html`
- ❌ Missing: `january-hit-list-complete.html`
- ❌ Missing: `january-hit-list-general-contractors.html`
- ❌ Missing: `january-hit-list-real-opportunities.html`

**Action Items:**
- [ ] **Get SAM.gov API Key** (free, from SAM.gov Account Details)
- [ ] **Use `sam-gov-fetcher.html`** to fetch fresh opportunities:
  - Open `sam-gov-fetcher.html` in browser
  - Enter your SAM.gov API key
  - Set filters (date range, set-asides, NAICS, etc.)
  - Click "Fetch Opportunities"
  - Click "Export to CSV" to download
- [ ] **Run `create-bootcamp-files.py`** to generate all hit lists:
  ```bash
  python3 create-bootcamp-files.py <path-to-csv> --month January --year 2026
  ```
  ⚠️ **Note:** This will overwrite the existing `january-hit-list.html` (which currently has sample data)
- [ ] Verify opportunity dates are current
- [ ] Check that all 5 hit list files were generated:
  - ✅ `january-hit-list-beginner.html`
  - ✅ `january-hit-list.html` (will replace existing template)
  - ✅ `january-hit-list-general-contractors.html`
  - ✅ `january-hit-list-real-opportunities.html`
  - ✅ `january-hit-list-complete.html`

**How December List Was Created:**
The December CSV (`ContractOpportunities-20251212-092037.csv`) was obtained using:
1. **Tool:** `sam-gov-fetcher.html` (SAM.gov API fetcher)
2. **Method:** SAM.gov Public API (requires free API key)
3. **Export:** Built-in CSV export button in the tool
4. **Location:** Saved to Google Drive folder "Dec 13 Surge Event"

**Scripts to Use:**
```bash
# NEW: Generate ALL hit lists at once (recommended)
python3 create-bootcamp-files.py <csv-path> --month January --year 2026

# OLD: Individual scripts (still work but slower)
python3 create-hit-list-from-csv.py  # Update CSV path first
python3 create-gc-hit-list.py        # Update CSV path first
python3 combine-hit-lists.py
```

---

### 2. Spend Forecast Reports ⭐ CRITICAL

**Current Files:**
- `december-spend-forecast.html`
- `december-spend-forecast-enhanced.csv`
- `january-spend-forecast.html` (if exists)

**Action Items:**
- [ ] Download latest spend forecast data
- [ ] Update month/year in filenames
- [ ] Update month/year in HTML content
- [ ] Verify data is current (not outdated)
- [ ] Check for new agencies or spending categories
- [ ] Update any expired forecasts

**Scripts to Use:**
```bash
# If you have an enhancement script
python3 enhance-december-forecast.py  # Update for new month
```

---

### 3. Expiring Contracts Forecast ⭐ IMPORTANT

**Current Files:**
- `expiring-contracts-viewer.html`
- `expiring-contracts.json`
- `Expiring Contracts 2025 - Expiring Contracts - December 2.csv`
- `Expiring_Contracts - 2026 - January February.csv`

**Action Items:**
- [ ] Download latest expiring contracts data
- [ ] Update for current/upcoming months
- [ ] Filter for relevant timeframes (next 3-6 months)
- [ ] Update HTML viewer with new data
- [ ] Verify contract end dates are accurate

---

### 4. Guides & Resources ⭐ UPDATE

**Current Files:**
- `GENERAL-CONTRACTOR-GUIDE.md`
- `AGENCY-PAIN-POINTS-DECISION-FRAMEWORK.md`
- `AGENCY-SELECTION-REPORT.md`
- `TIER-2-VS-TIER-1-BENEFITS.md`
- `SMALL-BUSINESS-INDUSTRIAL-BASE-PAIN-POINTS.md`
- `AGENCY-PAIN-POINTS-FINDING-SMALL-BUSINESSES.md`

**Action Items:**
- [x] ✅ **DONE:** Updated with 2026 NDAA provisions (December 18, 2025)
- [ ] Review all guides for accuracy
- [ ] Update any outdated statistics or data
- [ ] Add new insights or learnings from December bootcamp
- [ ] Check links are still working
- [ ] Update examples with current opportunities

**New Files Created:**
- `2026-NDAA-SMALL-BUSINESS-PROVISIONS.md` ✅ (Already created)

---

### 5. Presentation Materials ⭐ IMPORTANT

**Current Files:**
- `index.html` - Bootcamp presentation slides
- `styles.css` - Presentation styling
- `script.js` - Presentation navigation

**Action Items:**
- [ ] Update date in title slide
- [ ] Update any month-specific content
- [ ] Add new slides if needed (2026 NDAA updates?)
- [ ] Update resource links
- [ ] Review and update learning objectives
- [ ] Add testimonials or success stories from December bootcamp

---

### 6. Email Templates & Sequences ⭐ OPTIONAL

**Current Files:**
- `EMAIL-SEQUENCE-10-DAY-NURTURE.md`
- `email-templates/` directory

**Action Items:**
- [ ] Review email templates for relevance
- [ ] Update month-specific references
- [ ] Add new templates if needed
- [ ] Update links to new hit lists/forecasts

---

## 📊 Data Sources to Refresh

### Contract Opportunities
- **Source:** SAM.gov
- **URL:** https://sam.gov/content/opportunities
- **What to Download:** Active contract opportunities CSV
- **Filters:** 
  - Active opportunities only
  - Set-asides (8(a), WOSB, SDVOSB, HUBZone)
  - Small business set-asides
- **Frequency:** Weekly or bi-weekly before bootcamp

### Spend Forecasts
- **Source:** SAM.gov, agency forecast databases
- **What to Download:** Agency spending forecasts
- **Focus:** Upcoming fiscal year quarters
- **Frequency:** Monthly

### Expiring Contracts
- **Source:** SAM.gov, agency databases
- **What to Download:** Contracts expiring in next 3-6 months
- **Focus:** Recompete opportunities
- **Frequency:** Monthly

---

## 🎯 Bootcamp-Specific Updates

### Month-Specific Content

**For January Bootcamp:**
- Update all "December" references to "January"
- Focus on Q1 FY2026 opportunities
- Highlight 2026 NDAA provisions (new!)
- Update fiscal year references

**For February Bootcamp:**
- Update all "December" references to "February"
- Focus on Q1/Q2 FY2026 opportunities
- Include January success stories
- Update with latest agency forecasts

**For March Bootcamp:**
- Update all "December" references to "March"
- Focus on Q2 FY2026 opportunities
- Mid-fiscal year insights
- Update with latest trends

---

## 🔄 Automation Scripts to Run

### Pre-Bootcamp Script Execution Order

```bash
# 1. Generate new hit lists from fresh CSV
python3 create-hit-list-from-csv.py

# 2. Generate GC-specific list
python3 create-gc-hit-list.py

# 3. Combine lists if needed
python3 combine-hit-lists.py

# 4. Enhance spend forecast (if script exists)
python3 enhance-december-forecast.py  # Update filename for new month

# 5. Generate any PDFs needed
python3 create-tier2-pdf-final.py  # If using Tier 2 materials
```

---

## 📋 Quality Checklist

Before bootcamp, verify:

### Hit Lists
- [ ] All opportunities are active (not expired)
- [ ] Dates are current
- [ ] Links work (SAM.gov opportunity links)
- [ ] No duplicate opportunities
- [ ] Proper categorization (beginner, GC, etc.)
- [ ] Month/year updated in titles

### Spend Forecasts
- [ ] Data is current (within last 30 days)
- [ ] Month/year updated
- [ ] Agency names are correct
- [ ] Dollar amounts are formatted correctly
- [ ] Links work

### Guides
- [ ] 2026 NDAA updates included ✅
- [ ] Statistics are current
- [ ] Examples are relevant
- [ ] Links work
- [ ] No broken references

### Presentation
- [ ] Date updated
- [ ] All slides display correctly
- [ ] Navigation works
- [ ] Links to materials work
- [ ] Print version works (if needed)

---

## 🆕 New Content to Consider

### Based on December Bootcamp Learnings

1. **2026 NDAA Updates** ✅
   - Already created: `2026-NDAA-SMALL-BUSINESS-PROVISIONS.md`
   - Include in presentation?
   - Add to guides?

2. **Success Stories**
   - Any wins from December bootcamp attendees?
   - Testimonials to add?
   - Case studies?

3. **New Tools/Resources**
   - Any new tools discovered?
   - Updated vendor portals?
   - New agency programs?

4. **Updated Pain Points**
   - New agency challenges?
   - Updated statistics?
   - New opportunities?

---

## 📁 File Organization

### Recommended Structure

```
Bootcamp/
├── [MONTH]-hit-list-complete.html
├── [MONTH]-hit-list-beginner.html
├── [MONTH]-hit-list.html
├── [MONTH]-hit-list-general-contractors.html
├── [MONTH]-spend-forecast.html
├── [MONTH]-spend-forecast-enhanced.csv
├── expiring-contracts-[MONTH].html
├── expiring-contracts-[MONTH].json
└── guides/ (or keep in root)
    ├── GENERAL-CONTRACTOR-GUIDE.md
    ├── AGENCY-PAIN-POINTS-DECISION-FRAMEWORK.md
    └── ...
```

---

## 🚨 Critical Path (Week Before Bootcamp)

### Day -7 (1 Week Before)
- [ ] Download fresh contract opportunities CSV
- [ ] Generate new hit lists
- [ ] Review and update guides

### Day -5 (5 Days Before)
- [ ] Download spend forecast data
- [ ] Generate spend forecast reports
- [ ] Update presentation materials

### Day -3 (3 Days Before)
- [ ] Final review of all materials
- [ ] Test all links
- [ ] Verify data accuracy
- [ ] Print materials if needed

### Day -1 (Day Before)
- [ ] Final quality check
- [ ] Backup all files
- [ ] Prepare delivery method (email, Mighty Networks, etc.)

---

## 💡 Pro Tips

1. **Automate What You Can**
   - Use scripts to generate hit lists automatically
   - Set up reminders to download fresh data
   - Create templates for month-specific updates

2. **Version Control**
   - Keep December materials archived
   - Don't overwrite old files
   - Use version numbers or dates in filenames

3. **Test Everything**
   - Open all HTML files in browser
   - Click all links
   - Verify data accuracy
   - Test on mobile devices

4. **Get Feedback**
   - Share materials with team before bootcamp
   - Get feedback from December attendees
   - Update based on learnings

5. **Stay Current**
   - Monitor SAM.gov for new opportunities
   - Check agency websites for updates
   - Follow government contracting news
   - Update with latest NDAA provisions

---

## 📞 Quick Reference

### Key Scripts
- `create-hit-list-from-csv.py` - Generate hit lists
- `create-gc-hit-list.py` - Generate GC-specific list
- `combine-hit-lists.py` - Combine multiple lists
- `enhance-december-forecast.py` - Enhance spend forecasts

### Key Data Sources
- SAM.gov - Contract opportunities
- Agency forecast databases - Spend forecasts
- SAM.gov - Expiring contracts

### Key Files to Update
- All `december-hit-list-*.html` files
- `december-spend-forecast.html`
- `expiring-contracts-viewer.html`
- `index.html` (presentation)

---

## ✅ Final Checklist (Day Before Bootcamp)

- [ ] All hit lists generated and reviewed
- [ ] Spend forecasts updated
- [ ] Expiring contracts updated
- [ ] Guides reviewed (2026 NDAA included ✅)
- [ ] Presentation updated
- [ ] All links tested
- [ ] Materials delivered to attendees
- [ ] Backup created
- [ ] Ready to present!

---

**Last Updated:** December 2025  
**Next Review:** Before each bootcamp

**Need help?** Review the scripts and guides in this directory, or ask for assistance with specific updates!
