# 🚀 Quick Start: Generate January Hit Lists

## Step 1: Get CSV from SAM.gov

### Option A: Use the SAM.gov Fetcher Tool (Recommended)

1. **Open** `sam-gov-fetcher.html` in your browser
2. **Get API Key:**
   - Go to [SAM.gov](https://sam.gov) → Log in
   - Click your name → Account Details
   - Copy your Public API Key
3. **Fetch Opportunities:**
   - Paste API key in the tool
   - Set date range: **January 1-31, 2026** (or last 30 days)
   - Set filters (optional): Set-asides, NAICS, etc.
   - Click "Fetch Opportunities"
   - Wait for results (10-30 seconds)
4. **Export CSV:**
   - Click "Export to CSV" button
   - Save file (e.g., `ContractOpportunities-January-2026.csv`)

### Option B: If You Already Have a CSV

Make sure it has these columns:
- `Active/Inactive`
- `Title`
- `Set-Aside`
- `Current Response Date`
- `Award Amount`
- `NAICS Code`
- `Agency`
- `Notice ID`
- `Description`

---

## Step 2: Generate Hit Lists

Once you have the CSV file, run:

```bash
python3 create-bootcamp-files.py <path-to-csv> --month January --year 2026
```

**Example:**
```bash
# If CSV is in Downloads
python3 create-bootcamp-files.py ~/Downloads/ContractOpportunities-January-2026.csv --month January --year 2026

# If CSV is in Google Drive
python3 create-bootcamp-files.py "/Users/ericcoffie/Library/CloudStorage/GoogleDrive-evankoffdev@gmail.com/My Drive/Federal Help Center/Jan Event/ContractOpportunities.csv" --month January --year 2026
```

---

## Step 3: Verify Files Created

You should see 5 new files:
- ✅ `january-hit-list-beginner.html`
- ✅ `january-hit-list.html` (replaces existing template)
- ✅ `january-hit-list-general-contractors.html`
- ✅ `january-hit-list-real-opportunities.html`
- ✅ `january-hit-list-complete.html`

---

## Troubleshooting

**Error: "Could not read CSV file"**
- Check CSV path is correct
- Make sure CSV has the right columns (see Step 1, Option B)

**Error: "No opportunities found"**
- CSV might not have "Active/Inactive" column
- Check CSV format matches SAM.gov export format

**Need Help?**
- Check `HOW-TO-GET-CONTRACT-OPPORTUNITIES-CSV.md` for detailed instructions
