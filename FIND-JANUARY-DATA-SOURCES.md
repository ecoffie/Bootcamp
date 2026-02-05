# 🔍 Finding January 2026 Spend Forecast Data Sources

## Required Data Sources

### 1. ✅ FY2026 NDAA (S.2296, 119th Congress)
**Status:** Already have (signed December 18, 2025)
- **Location:** https://www.congress.gov/bill/119th-congress/senate-bill/2296
- **What We Have:** Full text and provisions
- **What We Need:** Specific section numbers for each agency/program

### 2. ⚠️ Monthly Treasury Statement (Latest)
**Where to Find:**
- **Primary Source:** https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/
- **Direct Link:** https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/mts-table-1-summary-of-receipts-outlays-and-the-deficit-surplus-of-the-u-s-government
- **Search Terms:** "Monthly Treasury Statement" + "January 2026" or latest month
- **What to Look For:** 
  - Table showing unobligated balances by agency
  - Q1 FY2026 budget execution data
  - Comparison to Q4 FY2025

**Quick Access:**
1. Go to https://fiscaldata.treasury.gov/
2. Click "Datasets" → "Monthly Treasury Statement"
3. Download latest CSV/Excel file
4. Look for "unobligated balances" column

### 3. ⚠️ GAO Reports (Latest)
**Where to Find:**
- **Primary Source:** https://www.gao.gov/
- **Search Links:**
  - https://www.gao.gov/search?q=unobligated+balances+2026
  - https://www.gao.gov/search?q=budget+execution+defense+2026
  - https://www.gao.gov/search?q=federal+spending+FY2026

**What to Look For:**
- Reports on unobligated balances
- Budget execution reports
- Defense spending reports
- Small business contracting reports

**Recent GAO Reports to Check:**
- GAO-26-XXX: Budget Execution Reports
- GAO-26-XXX: Defense Spending Efficiency
- GAO-26-XXX: Unobligated Balances Analysis

### 4. ⚠️ USAspending.gov Q1 FY2026 Dashboards
**Where to Find:**
- **Primary Source:** https://www.usaspending.gov/
- **Dashboard:** https://www.usaspending.gov/explorer
- **Advanced Search:** https://www.usaspending.gov/search/
- **Agency Profiles:** https://www.usaspending.gov/agency

**How to Use:**
1. Go to https://www.usaspending.gov/explorer
2. Filter by:
   - Fiscal Year: 2026
   - Quarter: Q1
   - Agency: Select specific agencies (DoD, Army, Navy, etc.)
3. View:
   - Spending by program
   - Contract awards
   - Unobligated vs. obligated amounts
   - Small business set-asides

**API Access:**
- USAspending.gov API: https://api.usaspending.gov/
- Documentation: https://api.usaspending.gov/docs/

## Step-by-Step Data Collection

### Step 1: Get Monthly Treasury Statement
```bash
# Visit Treasury.gov
https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/

# Download latest MTS file
# Look for unobligated balances table
# Extract Q1 FY2026 data
```

### Step 2: Find GAO Reports
```bash
# Search GAO website
https://www.gao.gov/search?q=unobligated+balances+2026

# Download relevant reports
# Extract agency-specific unobligated balance data
```

### Step 3: Access USAspending Dashboard
```bash
# Go to USAspending.gov
https://www.usaspending.gov/explorer

# Filter: FY2026, Q1
# Export data for each agency
# Compare obligated vs. unobligated amounts
```

### Step 4: Extract NDAA Section Numbers
```bash
# Review S.2296 full text
https://www.congress.gov/bill/119th-congress/senate-bill/2296/text

# Find sections for each agency/program
# Note authorization amounts
# Extract small business provisions
```

## Data Points to Extract

For each agency/program, collect:

1. **Unobligated Balance (Q1 FY2026)**
   - From: Monthly Treasury Statement or GAO reports
   - Compare to: December 2025 balance
   - Calculate: Change from Dec → Jan

2. **NDAA Authorization**
   - From: S.2296 full text
   - Extract: Specific section number
   - Note: Authorization amount vs. budget request

3. **Spending Trends**
   - From: USAspending.gov dashboard
   - Extract: Q1 FY2026 spending by program
   - Compare: Obligated vs. unobligated

4. **Small Business Set-Asides**
   - From: USAspending.gov or agency reports
   - Extract: Percentage of contracts set aside
   - Note: Specific set-aside types (8(a), SDVOSB, etc.)

5. **Prime Contractors**
   - From: USAspending.gov or SBA Prime Directory
   - Extract: Top contractors for each program
   - Research: SBLO contacts

## Quick Reference Links

| Source | URL | What to Get |
|--------|-----|-------------|
| NDAA S.2296 | https://www.congress.gov/bill/119th-congress/senate-bill/2296 | Section numbers, authorizations |
| Treasury MTS | https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/ | Unobligated balances |
| GAO Reports | https://www.gao.gov/search?q=unobligated+balances+2026 | Agency spending reports |
| USAspending | https://www.usaspending.gov/explorer | Q1 FY2026 spending data |

## Automation Options

### Option 1: Manual Collection
- Visit each website
- Download reports/data
- Extract relevant information
- Update CSV file

### Option 2: API Access (if available)
- USAspending.gov API: https://api.usaspending.gov/
- Treasury API: Check fiscaldata.treasury.gov for API access
- GAO: May require manual download

### Option 3: Web Scraping
- Use Python scripts to scrape data
- Parse HTML/CSV files
- Extract unobligated balances automatically

## Next Steps

1. ✅ Run `generate-january-spend-forecast.py` to create CSV template
2. ⚠️ Visit each data source and collect latest information
3. ⚠️ Update CSV with actual unobligated balances
4. ⚠️ Research prime contractor and SBLO contacts
5. ⚠️ Generate HTML forecast using updated data

## Notes

- **Data Availability:** Some data may not be available until mid-to-late January 2026
- **Estimates:** May need to use estimates based on December data and trends
- **Updates:** Re-run data collection monthly as new reports are published
- **Verification:** Cross-reference multiple sources for accuracy
