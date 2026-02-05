# 📋 January 2026 Spend Forecast - Step-by-Step Checklist

## Overview
Create January 2026 Spend Forecast + Immediate Buyers List based on:
- FY2026 NDAA (S.2296, 119th Congress)
- Monthly Treasury Statement (latest available)
- GAO Reports (latest available)
- USAspending.gov Q1 FY2026 dashboards

---

## ✅ Step 1: Access FY2026 NDAA (S.2296)

**Status:** [ ] Not Started | [ ] In Progress | [x] Complete ✅

**Action Items:**
- [ ] Go to: https://www.congress.gov/bill/119th-congress/senate-bill/2296
- [ ] Download or bookmark the full text
- [ ] Find section numbers for each agency/program:
  - [ ] DoD Overall
  - [ ] Army Procurement
  - [ ] Navy Shipbuilding
  - [ ] Air Force RDT&E
  - [ ] Defense Logistics Agency
  - [ ] Missile Defense Agency
  - [ ] Cyber Command
  - [ ] DOE Atomic Energy Defense
  - [ ] Space Force
  - [ ] Defense Health Program
- [ ] Note authorization amounts vs. budget requests
- [ ] Extract small business provisions and thresholds

**Notes:**
- NDAA was signed December 18, 2025
- Full text available at Congress.gov
- Look for specific section numbers (e.g., Sec. 9083 for Space Force)

**Time Estimate:** 30-45 minutes

---

## ✅ Step 2: Get Monthly Treasury Statement Data

**Status:** [ ] Not Started | [x] In Progress | [ ] Complete

**Action Items:**
- [ ] Go to: https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/
- [ ] Find latest Monthly Treasury Statement (January 2026 or latest available)
- [ ] Download the data file (CSV or Excel)
- [ ] Locate unobligated balances table
- [ ] Extract Q1 FY2026 unobligated balances for each agency:
  - [ ] DoD Overall: $_____
  - [ ] Army: $_____
  - [ ] Navy: $_____
  - [ ] Air Force: $_____
  - [ ] DLA: $_____
  - [ ] MDA: $_____
  - [ ] Cyber Command: $_____
  - [ ] DOE: $_____
  - [ ] Space Force: $_____
  - [ ] Defense Health: $_____
- [ ] Compare to Q4 FY2025 (December) balances
- [ ] Calculate change from Dec → Jan

**Notes:**
- May need to search for "unobligated balances" in the document
- Data might be in table format or separate report
- If January data not available, use latest available month

**Time Estimate:** 20-30 minutes

---

## ✅ Step 3: Find GAO Reports on Unobligated Balances

**Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

**Action Items:**
- [ ] Go to: https://www.gao.gov/
- [ ] Search for: "unobligated balances 2026"
- [ ] Search for: "budget execution defense 2026"
- [ ] Search for: "federal spending FY2026"
- [ ] Review relevant reports:
  - [ ] Download report on unobligated balances
  - [ ] Download budget execution report
  - [ ] Download defense spending report (if available)
- [ ] Extract agency-specific unobligated balance data
- [ ] Note any trends or patterns mentioned
- [ ] Cross-reference with Treasury Statement data

**Notes:**
- GAO reports may be published monthly or quarterly
- Look for reports dated January 2026 or December 2025
- Reports may have different agency groupings than Treasury Statement

**Time Estimate:** 30-45 minutes

---

## ✅ Step 4: Access USAspending.gov Q1 FY2026 Dashboard

**Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

**Action Items:**
- [ ] Go to: https://www.usaspending.gov/explorer
- [ ] Set filters:
  - [ ] Fiscal Year: 2026
  - [ ] Quarter: Q1
  - [ ] Agency: Department of Defense
- [ ] View spending by program
- [ ] Export data for each major program:
  - [ ] DoD Overall
  - [ ] Army Procurement
  - [ ] Navy Shipbuilding
  - [ ] Air Force RDT&E
  - [ ] DLA
  - [ ] MDA
  - [ ] Cyber Command
  - [ ] DOE
  - [ ] Space Force
  - [ ] Defense Health
- [ ] Note obligated vs. unobligated amounts
- [ ] Extract small business set-aside percentages
- [ ] Note top NAICS codes for each program

**Alternative Method (API):**
- [ ] Go to: https://api.usaspending.gov/
- [ ] Review API documentation
- [ ] Use API to query Q1 FY2026 spending data
- [ ] Export data programmatically

**Notes:**
- Q1 FY2026 data may not be complete until mid-to-late January
- May need to use estimates based on trends
- Can compare to Q4 FY2025 for patterns

**Time Estimate:** 45-60 minutes

---

## ✅ Step 5: Update CSV with Actual Data

**Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

**Action Items:**
- [ ] Open: `january-spend-forecast-enhanced.csv`
- [ ] Update unobligated balances column with actual data from Steps 2-4:
  - [ ] Replace estimated values with actual Q1 FY2026 balances
  - [ ] Add notes if using estimates
- [ ] Update NDAA provision column:
  - [ ] Add specific section numbers from Step 1
  - [ ] Add authorization amounts
- [ ] Update "Why Now" column:
  - [ ] Add specific reasons based on latest data
  - [ ] Reference NDAA deadlines (e.g., CMMC support strategy Jan 31)
- [ ] Verify all 10 agencies have updated data
- [ ] Save the CSV file

**Notes:**
- Current CSV has estimated balances (adjusted from December)
- Replace estimates with actual data as available
- Keep estimates if actual data not yet published

**Time Estimate:** 20-30 minutes

---

## ✅ Step 6: Research Prime Contractor Contacts

**Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

**Action Items:**
- [ ] For each agency/program, identify top prime contractors:
  - [ ] Use USAspending.gov to find top contractors
  - [ ] Or use SBA Prime Directory: https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans
  - [ ] Or reuse December contacts (if still relevant)
- [ ] Research SBLO contacts for each prime:
  - [ ] Check prime contractor websites
  - [ ] Use December forecast contacts as starting point
  - [ ] Search for "small business" or "SBLO" contact pages
- [ ] Update CSV with:
  - [ ] Prime contractor names
  - [ ] SBLO names
  - [ ] SBLO emails
  - [ ] SBLO phone numbers
  - [ ] Source of contact information

**Notes:**
- Can reuse many contacts from `december-spend-forecast-enhanced.csv`
- Verify contacts are still current
- Some primes may have changed SBLOs

**Time Estimate:** 60-90 minutes

---

## ✅ Step 7: Generate HTML Spend Forecast

**Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

**Action Items:**
- [ ] Review `december-spend-forecast.html` as template
- [ ] Create `january-spend-forecast.html`:
  - [ ] Update title to "January 2026 Spend Forecast"
  - [ ] Update subtitle to reflect January timeframe
  - [ ] Update unobligated balance total (sum of all agencies)
  - [ ] Update agency table with Q1 FY2026 data
  - [ ] Update NDAA references to S.2296 section numbers
  - [ ] Update "Why Now" sections with January-specific reasons
  - [ ] Update data sources footer
  - [ ] Update contact email templates
- [ ] Verify all links work
- [ ] Check formatting and styling
- [ ] Test print/PDF export

**Notes:**
- Use December HTML as base template
- Update all month/year references
- Ensure data matches CSV file

**Time Estimate:** 60-90 minutes

---

## ✅ Step 8: Review and Verify

**Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

**Action Items:**
- [ ] Cross-check all data:
  - [ ] Unobligated balances match across sources
  - [ ] NDAA section numbers are correct
  - [ ] Contact information is current
  - [ ] Dates and timeframes are accurate
- [ ] Verify calculations:
  - [ ] Total unobligated balance sum
  - [ ] Percentage changes from December
  - [ ] Small business set-aside percentages
- [ ] Check for consistency:
  - [ ] Agency names match across all documents
  - [ ] NAICS codes are accurate
  - [ ] Program names are consistent
- [ ] Proofread HTML content
- [ ] Test all links and references

**Notes:**
- Have someone else review if possible
- Double-check against original sources
- Ensure all data is properly cited

**Time Estimate:** 30-45 minutes

---

## ✅ Step 9: Finalize and Save

**Status:** [ ] Not Started | [ ] In Progress | [ ] Complete

**Action Items:**
- [ ] Save final CSV: `january-spend-forecast-enhanced.csv`
- [ ] Save final HTML: `january-spend-forecast.html`
- [ ] Create backup copies
- [ ] Document any assumptions or estimates used
- [ ] Note data source dates in footer
- [ ] Update this checklist with completion dates

**Notes:**
- Keep December files for reference
- Document any data limitations
- Note when data sources were accessed

**Time Estimate:** 10-15 minutes

---

## 📊 Progress Tracking

**Overall Progress:** ___ / 9 steps complete

**Started:** _______________

**Completed:** _______________

**Total Time Spent:** ___ hours

---

## 📝 Notes Section

Use this space to track any issues, questions, or additional information:

- 

- 

- 

---

## 🔗 Quick Reference Links

- **NDAA S.2296:** https://www.congress.gov/bill/119th-congress/senate-bill/2296
- **Treasury MTS:** https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/
- **GAO Search:** https://www.gao.gov/search?q=unobligated+balances+2026
- **USAspending:** https://www.usaspending.gov/explorer
- **SBA Prime Directory:** https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans

---

## 💡 Tips

1. **Work incrementally:** Complete one step fully before moving to the next
2. **Save frequently:** Keep backups as you work
3. **Document sources:** Note where each piece of data came from
4. **Use estimates if needed:** If data isn't available, use reasonable estimates based on trends
5. **Reuse December data:** Many contacts and structures can be reused
6. **Ask for help:** If stuck on a step, note it and move on

---

**Ready to start? Begin with Step 1!** 🚀
