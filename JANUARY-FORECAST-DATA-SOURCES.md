# 📊 January 2026 Spend Forecast - Data Sources Guide

## Required Data Sources

### 1. FY2026 NDAA (S.2296, 119th Congress)
**Status:** ✅ Already have (signed December 18, 2025)
**Location:** https://www.congress.gov/bill/119th-congress/senate-bill/2296
**What to Extract:**
- Specific section numbers for each agency/program
- Authorization amounts vs. budget requests
- Small business provisions and thresholds
- Implementation deadlines

### 2. Monthly Treasury Statement (Latest Available)
**Status:** ⚠️ Need to find
**Where to Find:**
- Treasury.gov: https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/
- Look for: "Monthly Treasury Statement" for latest month (Jan 2026 or Dec 2025)
- Search for: "unobligated balances" or "budget execution"

**What to Extract:**
- Q1 FY2026 unobligated balances by agency
- Comparison to Q4 FY2025 (December data)
- Spending trends and gaps

### 3. GAO Reports (Latest Available)
**Status:** ⚠️ Need to find
**Where to Find:**
- GAO.gov: https://www.gao.gov/
- Search for: "unobligated balances" + "January 2026" or "FY2026"
- Or: "budget execution" + "defense" + "2026"

**What to Extract:**
- Agency-specific unobligated balance reports
- Spending efficiency reports
- Small business contracting reports

### 4. USAspending.gov Q1 FY2026 Dashboards
**Status:** ⚠️ Need to find
**Where to Find:**
- USAspending.gov: https://www.usaspending.gov/
- Navigate to: Dashboards → Agency Spending → Filter by FY2026 Q1
- Or: Search → Advanced Search → Filter by fiscal year and quarter

**What to Extract:**
- Agency spending by program
- Contract awards by NAICS code
- Small business set-aside data
- Unobligated vs. obligated amounts

## Quick Links

1. **FY2026 NDAA (S.2296):**
   - Full Text: https://www.congress.gov/bill/119th-congress/senate-bill/2296/text
   - Summary: https://www.congress.gov/bill/119th-congress/senate-bill/2296/summary

2. **Monthly Treasury Statement:**
   - Latest: https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/
   - Search: "Monthly Treasury Statement" + current month

3. **GAO Reports:**
   - Search: https://www.gao.gov/search?q=unobligated+balances+2026
   - Or: https://www.gao.gov/search?q=budget+execution+defense+2026

4. **USAspending.gov:**
   - Dashboard: https://www.usaspending.gov/explorer
   - Advanced Search: https://www.usaspending.gov/search/

## Data Collection Checklist

- [ ] Download latest Monthly Treasury Statement
- [ ] Find latest GAO report on unobligated balances
- [ ] Access USAspending.gov Q1 FY2026 dashboard
- [ ] Extract specific section numbers from NDAA for each agency
- [ ] Calculate updated unobligated balances (Dec → Jan)
- [ ] Verify small business set-aside percentages
- [ ] Research prime contractor contacts for each program
- [ ] Research SBLO contacts for each agency/program

## Next Steps

1. Run this script to generate the CSV template
2. Research and update unobligated balances from latest data sources
3. Add prime contractor and SBLO contact information
4. Generate HTML forecast using the updated CSV
