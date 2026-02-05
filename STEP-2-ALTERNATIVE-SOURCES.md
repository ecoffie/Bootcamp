# Step 2 Alternative: Finding Unobligated Balances

## Current File
- **File:** `january/MonthlyReceiptsOutlaysDeficitSurplus.xls`
- **Content:** Summary receipts/outlays by month (not agency-level)
- **Status:** ✅ Downloaded but doesn't have unobligated balances by agency

## What We Need
Agency-level unobligated balances showing:
- Department of Defense: $XXB
- Army: $XXB
- Navy: $XXB
- Air Force: $XXB
- etc.

## Alternative Data Sources

### Option 1: USAspending.gov (Recommended) ⭐
**Why:** Most detailed, agency-level, shows obligated vs unobligated

**How to Access:**
1. Go to: https://www.usaspending.gov/explorer
2. Filter by:
   - Fiscal Year: 2026
   - Quarter: Q1 (or latest available)
   - Agency: Select specific agencies
3. Export data showing:
   - Budget Authority
   - Obligations
   - Unobligated Balance (calculated: Budget Authority - Obligations)

**Direct Links:**
- Dashboard: https://www.usaspending.gov/explorer
- Agency Profiles: https://www.usaspending.gov/agency
- API: https://api.usaspending.gov/

### Option 2: GAO Reports
**Why:** Often have unobligated balance analysis

**How to Access:**
1. Go to: https://www.gao.gov/
2. Search for: "unobligated balances 2026" or "budget execution defense"
3. Look for reports with agency-level breakdowns

**Search Links:**
- https://www.gao.gov/search?q=unobligated+balances+2026
- https://www.gao.gov/search?q=budget+execution+defense+2026

### Option 3: Treasury Budget Execution Reports
**Why:** Official budget execution data

**How to Access:**
1. Go to: https://fiscaldata.treasury.gov/
2. Look for "Budget Execution" or "Agency Budget" datasets
3. Not the Monthly Treasury Statement (that's summary data)

### Option 4: Use Estimates Based on December Data
**Why:** If actual data not available yet

**How:**
- Use December 2025 unobligated balances from previous forecast
- Adjust based on spending trends
- Note in forecast that estimates are used

## Recommended Approach

**Best:** Use USAspending.gov Q1 FY2026 data
- Most detailed
- Agency-level breakdowns
- Shows obligated vs unobligated
- Can export as CSV/Excel

**Steps:**
1. Go to USAspending.gov explorer
2. Filter for FY2026 Q1
3. Select each agency (DoD, Army, Navy, etc.)
4. Export data showing Budget Authority and Obligations
5. Calculate: Unobligated = Budget Authority - Obligations
6. Save to CSV file

## Quick Calculation Method

If you have Budget Authority and Obligations:
```
Unobligated Balance = Budget Authority - Obligations
```

Example:
- Budget Authority: $100B
- Obligations: $65B
- Unobligated Balance: $35B

## Next Steps

1. **Try USAspending.gov first** (most reliable)
2. If not available, check GAO reports
3. If still not available, use estimates from December data
4. Document data source and date in forecast
