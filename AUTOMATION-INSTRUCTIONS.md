# Automated SBLO List Compilation - Instructions

## 🚀 Two Ways to Compile Your SBLO List

### Option 1: Fully Automated (Limited)
Run the automated script that tries to download and scrape data:

```bash
python3 compile-sblo-list.py
```

**What it does:**
- ✅ Scrapes DHS prime contractors page (gets emails)
- ⚠️ Attempts to download DoD PDF (may fail due to access restrictions)
- ⚠️ SBA Excel requires manual download

**Result:** Gets ~3-10 contacts automatically

---

### Option 2: Semi-Automated (Recommended)
Download files manually, then process them automatically:

#### Step 1: Download Files Manually

1. **SBA Prime Directory** (300+ primes)
   - Go to: https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans
   - Click download button
   - Save as: `sba-prime-directory.xlsx` in `sblo-data-downloads/` folder

2. **DoD CSP Prime Directory** (100+ primes)
   - Go to: https://business.defense.gov/Portals/57/Documents/Dod%20CSP%20Prime%20Contractor%20Directory_May%202025.pdf
   - Right-click → Save As
   - Save as: `dod-csp-directory.pdf` in `sblo-data-downloads/` folder

3. **DOT Subcontracting Directory** (100+ primes)
   - Go to: https://www.transportation.gov/osdbu/procurement-assistance/dot-subcontracting-directory
   - Download Excel/PDF version
   - Save to `sblo-data-downloads/` folder

#### Step 2: Process Files Automatically

```bash
python3 process-manual-files.py
```

**What it does:**
- ✅ Parses all Excel files in `sblo-data-downloads/`
- ✅ Extracts company names, SBLO contacts, emails, phones
- ✅ Parses PDF files for contact information
- ✅ Removes duplicates
- ✅ Saves to `sblo-list-compiled.csv`

**Result:** Gets 100-500+ contacts from downloaded files

---

## 📋 What You'll Get

After running either script, you'll have:

1. **`sblo-list-compiled.csv`** - Raw extracted contacts
2. **Updated `sblo-list.csv`** - Merged with existing list
3. **Console output** - Shows what was found

---

## 🔧 Requirements

Install Python dependencies:

```bash
pip3 install pandas openpyxl PyPDF2 requests --user
```

---

## 📊 Expected Results

| Source | Expected Contacts | Format |
|--------|------------------|--------|
| SBA Prime Directory | 300+ | Excel |
| DoD CSP Directory | 100+ | PDF |
| DHS Web Scrape | 3-10 | Web |
| DOT Directory | 100+ | Excel/PDF |
| **Total** | **500+** | |

---

## ✅ Next Steps After Compilation

1. **Review** `sblo-list-compiled.csv`
2. **Clean up** any bad data or duplicates
3. **Verify emails** (some may need manual checking)
4. **Update** `sblo-list.html` with verified contacts
5. **Export** to PDF for distribution

---

## 🐛 Troubleshooting

**Problem:** Script says "No files found"
- **Solution:** Make sure files are in `sblo-data-downloads/` folder

**Problem:** Excel parsing fails
- **Solution:** Make sure file is .xlsx or .xls format (not CSV)

**Problem:** PDF parsing gets wrong data
- **Solution:** PDFs vary in format. May need manual review/editing

**Problem:** Missing dependencies
- **Solution:** Run `pip3 install pandas openpyxl PyPDF2 requests --user`

---

## 💡 Pro Tips

1. **Start with SBA directory** - It's the largest and most structured
2. **Verify emails** - Use tools like Hunter.io or EmailHippo
3. **Add notes** - Note which contacts responded or are most relevant
4. **Keep updated** - These directories update quarterly
5. **Export regularly** - Keep backups of your compiled list

---

## 📁 File Structure

```
Bootcamp/
├── compile-sblo-list.py          # Fully automated script
├── process-manual-files.py       # Process downloaded files
├── sblo-data-downloads/          # Put downloaded files here
│   ├── sba-prime-directory.xlsx
│   ├── dod-csp-directory.pdf
│   └── dot-directory.xlsx
├── sblo-list-compiled.csv        # Output: extracted contacts
├── sblo-list.csv                 # Main list (gets updated)
└── sblo-list.html                # Web version
```

---

**Ready to start?** Download the files and run `process-manual-files.py`!




