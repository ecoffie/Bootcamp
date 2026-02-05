# 📥 How to Get Contract Opportunities CSV for Bootcamp

## Overview

The December bootcamp CSV was obtained using the **SAM.gov API** via the `sam-gov-fetcher.html` tool. This is NOT a direct download from SAM.gov's website - it uses their API.

---

## Step-by-Step Process

### 1. Get Your Free SAM.gov API Key

1. Go to [SAM.gov](https://sam.gov) and **log in** (or create a free account)
2. Click your **name** in the top right corner
3. Select **Account Details**
4. Enter your password to reveal your **Public API Key**
5. **Copy** the API key (you'll need it in the next step)

### 2. Use the SAM.gov Fetcher Tool

1. **Open** `sam-gov-fetcher.html` in your web browser
2. **Paste** your SAM.gov API key into the input field
3. **Set your filters:**
   - **Date Range:** Select "Posted From" and "Posted To" dates
     - For bootcamp: Usually last 30-60 days
     - Example: December 1 - December 31 for December bootcamp
   - **Set-Aside Type:** (Optional) Filter for Small Business, 8(a), etc.
   - **NAICS Code:** (Optional) Filter by specific industry codes
   - **Opportunity Type:** (Optional) Filter by Presolicitation, Solicitation, etc.
   - **Number of Results:** Select 100, 250, 500, or 1000 (max)
4. **Click** "Fetch Opportunities"
5. **Wait** for results to load (may take 10-30 seconds)
6. **Review** the opportunities displayed
7. **Click** "Export to CSV" button
8. **Save** the CSV file to your desired location

### 3. Generate Bootcamp Hit Lists

Once you have the CSV file:

```bash
python3 create-bootcamp-files.py <path-to-csv> --month January --year 2026
```

This will generate all 5 hit list files:
- `january-hit-list-beginner.html`
- `january-hit-list.html`
- `january-hit-list-general-contractors.html`
- `january-hit-list-real-opportunities.html`
- `january-hit-list-complete.html`

---

## December Bootcamp Example

**File Used:** `ContractOpportunities-20251212-092037.csv`

**Location:** 
```
/Users/ericcoffie/Library/CloudStorage/GoogleDrive-evankoffdev@gmail.com/My Drive/Federal Help Center/Dec 13 Surge Event/
```

**How It Was Created:**
1. Used `sam-gov-fetcher.html` tool
2. Fetched opportunities from SAM.gov API
3. Exported to CSV using the built-in export button
4. Saved to Google Drive folder

---

## Alternative Methods (Not Used for December)

### Method 1: Manual SAM.gov Search
- Go to [SAM.gov/opportunities](https://sam.gov/opportunities)
- Use advanced search filters
- Export results manually
- ⚠️ **Limitation:** Manual export may have fewer fields than API

### Method 2: SAM.gov Bulk Download
- SAM.gov offers bulk data downloads
- ⚠️ **Limitation:** May not have real-time data or all fields

### Method 3: Third-Party Tools
- Various tools scrape or access SAM.gov data
- ⚠️ **Limitation:** May violate terms of service or have data quality issues

---

## Recommended Approach

**✅ Use `sam-gov-fetcher.html`** because:
- ✅ Uses official SAM.gov API (compliant)
- ✅ Free API key (no cost)
- ✅ Real-time data
- ✅ All opportunity fields included
- ✅ Built-in CSV export
- ✅ Easy to filter by date, set-aside, NAICS, etc.
- ✅ Already tested and working (used for December bootcamp)

---

## Troubleshooting

### "API returned status 401"
- **Problem:** Invalid API key
- **Solution:** Double-check your API key from SAM.gov Account Details

### "CORS restrictions"
- **Problem:** Browser blocking API request
- **Solution:** The tool uses a CORS proxy - should work automatically

### "No opportunities found"
- **Problem:** Filters too restrictive or date range has no opportunities
- **Solution:** 
  - Expand date range (try last 60 days)
  - Remove optional filters
  - Check SAM.gov directly to verify opportunities exist

### CSV Export Not Working
- **Problem:** Export button not appearing or not downloading
- **Solution:**
  - Make sure opportunities were fetched successfully
  - Check browser console for errors
  - Try a different browser (Chrome recommended)

---

## Tips for Bootcamp Preparation

1. **Fetch Early:** Get CSV 1-2 weeks before bootcamp to allow time for processing
2. **Wide Date Range:** Use 30-60 day range to ensure enough opportunities
3. **Filter Later:** Don't over-filter in the tool - filter in Python scripts instead
4. **Save Multiple Versions:** Keep raw CSV and processed versions
5. **Verify Active:** Make sure to filter for "Active" opportunities only in scripts

---

## File Structure

```
Bootcamp/
├── sam-gov-fetcher.html          # Tool to fetch opportunities
├── create-bootcamp-files.py       # Generate all hit lists
├── create-hit-list-from-csv.py   # Generate individual lists
└── ContractOpportunities-*.csv   # Downloaded CSV files
```

---

## Next Steps

After getting your CSV:
1. Run `create-bootcamp-files.py` to generate hit lists
2. Review the generated HTML files
3. Update any month/year references
4. Test the files in a browser
5. Share with bootcamp participants
