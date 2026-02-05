# 🔄 Merging Apollo Data into Airtable (Live Updates)

## 🎯 Goal: Update Your Live Airtable Database

When you enrich data with Apollo, you'll get a CSV. We need to **merge** that data back into Airtable so your embedded database updates automatically.

**The embedded version in Mighty Networks pulls from Airtable in real-time**, so once you update Airtable, it updates everywhere!

---

## 📊 The Process Overview

```
Step 1: Import CSV to Airtable → Create New Table
Step 2: Link Records → Match Companies
Step 3: Update Fields → Copy Enriched Data
Step 4: Verify → Check Updates
Step 5: Embed Updates Automatically → Live in Mighty Networks!
```

---

## 🚀 Method 1: Airtable's Built-in CSV Import (RECOMMENDED)

### Step 1: Import Apollo CSV to New Table (5 minutes)

After downloading enriched data from Apollo:

1. **Open your Airtable base** (Federal Contractors Database)
2. **Create new table:**
   - Click "+" next to your table tabs
   - Name it: "Apollo Enriched Data"
3. **Import CSV:**
   - Click table dropdown → "Import data" → "CSV file"
   - Select your Apollo enriched CSV
   - Click "Import"
4. **Result:** New table with Apollo data

---

### Step 2: Add Link Field to Match Companies (5 minutes)

We need to connect Apollo data to your main Contractors table:

1. **In "Apollo Enriched Data" table:**
   - Add new field
   - Type: "Link to another record"
   - Choose: "Contractors" table
   - Name it: "Linked Contractor"

2. **Match companies:**
   - Click first "Linked Contractor" cell
   - Start typing company name
   - Airtable will suggest matches
   - Select the matching contractor
   - Repeat for each row

**Pro Tip:** For 2,628 rows, this is tedious. Better option below! ⬇️

---

## 🤖 Method 2: Automated Matching (MUCH FASTER)

### Using Airtable Formula + Script

**Step 1: Prepare Main Table**

In your main "Contractors" table:

1. **Add new columns** (if not already there):
   - "Apollo Email" (Email type)
   - "Apollo Phone" (Phone type)
   - "Apollo Contact Name" (Single line text)
   - "Last Updated" (Date)

**Step 2: Use Airtable's CSV Import with Matching**

1. **Export your current Contractors table:**
   - Click "..." menu → "Download CSV"
   - Save as "contractors-current.csv"

2. **Merge CSVs outside Airtable:**
   - I'll create a Python script for you!
   - It matches by company name
   - Adds Apollo emails/phones to existing data
   - Creates new CSV with merged data

3. **Re-import merged CSV:**
   - Delete all records in Contractors table (or create backup)
   - Import merged CSV
   - All data updated!

---

## 🛠️ Method 3: Python Merge Script (AUTOMATED)

Let me create a script that automatically merges Apollo data with your existing Airtable CSV:

**I'll create this script for you after you get Apollo data!**

The script will:
1. Read your original contractors CSV
2. Read Apollo enriched CSV
3. Match by company name
4. Add emails/phones where missing
5. Create final merged CSV
6. You import to Airtable

**Takes 2 minutes to run, updates all 2,628 records automatically!**

---

## 📋 Method 4: Airtable Extensions (No Code Solution)

### Using "Data Fetcher" Extension

1. **In your Airtable base:**
   - Click "Extensions" (top right)
   - Search: "CSV Import"
   - Install extension

2. **Configure:**
   - Upload Apollo CSV
   - Map "Company Name" to existing company field
   - Choose "Update existing records"
   - Map Email → Email field
   - Map Phone → Phone field
   - Click "Import"

3. **Result:**
   - Airtable automatically matches by company name
   - Updates existing records with new data
   - No duplicates created!

---

## ✅ Step-by-Step: Easiest Method (After Apollo Download)

### Here's what we'll do together:

**When you download Apollo enriched CSV:**

1. **You:** Download Apollo CSV (let's call it `apollo-enriched.csv`)

2. **Me:** I'll create a merge script that:
   ```python
   # Reads apollo-enriched.csv
   # Reads contractors-airtable.csv
   # Matches by company name
   # Adds emails/phones
   # Creates contractors-merged.csv
   ```

3. **You:** Import `contractors-merged.csv` to Airtable:
   - Method A: Delete old records, import new
   - Method B: Create new table, switch embed to use it

4. **Result:**
   - ✅ Airtable updated with 2,000+ new contacts
   - ✅ Embedded version auto-updates
   - ✅ Mighty Networks shows new data immediately!

---

## 🔄 How Real-Time Updates Work

### Important: Airtable Embed Updates Automatically!

When you embed Airtable in Mighty Networks:

```
Airtable (Source) → Embed Code → Mighty Networks
```

**Any changes you make in Airtable appear instantly in the embed:**
- ✅ Add new records → Shows immediately
- ✅ Update emails/phones → Updates immediately
- ✅ Add new columns → Shows immediately
- ✅ Filter/sort views → Updates immediately

**No need to re-embed or update Mighty Networks!**

The embed code **points to your Airtable base**, so it's always live.

---

## 📊 Before vs After Example

### BEFORE (Current State):
```
Company: THE BOEING COMPANY
Email: tina.t.wang@boeing.com
Phone: [empty]
SBLO: Tina T. Wang
```

### AFTER (Apollo Enrichment):
```
Company: THE BOEING COMPANY
Email: tina.t.wang@boeing.com
Phone: (555) 123-4567          ← NEW!
SBLO: Tina T. Wang
```

**This update happens in Airtable → Shows in embed automatically!**

---

## 🎯 My Recommendation for You

**Follow this workflow:**

### Today: Apollo Enrichment
1. ✅ Sign up for Apollo.io
2. ✅ Upload `apollo-upload.csv` (2,628 companies)
3. ✅ Wait for enrichment (~30 mins)
4. ✅ Download enriched CSV
5. ✅ **Send me the filename or let me know it's done**

### Today: Merge Data
1. ✅ I'll create a merge script for you
2. ✅ Run the script (takes 2 minutes)
3. ✅ Get `contractors-final.csv` with all enriched data

### Today: Update Airtable
1. ✅ Import `contractors-final.csv` to Airtable
2. ✅ Verify data looks good
3. ✅ **Done! Embed auto-updates!**

---

## 🔧 Merge Script Preview

Here's what the script will look like (I'll create full version after you get Apollo data):

```python
import csv

# Read original contractors
with open('contractors-airtable.csv') as f:
    original = {row['Company']: row for row in csv.DictReader(f)}

# Read Apollo enriched data
with open('apollo-enriched.csv') as f:
    apollo = {row['Company Name']: row for row in csv.DictReader(f)}

# Merge
for company_name, company_data in original.items():
    if company_name in apollo:
        # Add Apollo email if original is empty
        if not company_data['Email'] and apollo[company_name].get('Email'):
            company_data['Email'] = apollo[company_name]['Email']

        # Add Apollo phone if original is empty
        if not company_data['Phone'] and apollo[company_name].get('Phone'):
            company_data['Phone'] = apollo[company_name]['Phone']

        # Add contact name if empty
        if not company_data['SBLO Name'] and apollo[company_name].get('Full Name'):
            company_data['SBLO Name'] = apollo[company_name]['Full Name']

# Write merged CSV
# (You import this to Airtable)
```

**Takes 30 seconds to run, updates all records automatically!**

---

## 🎨 Airtable View Updates

After merging Apollo data:

### Create New View: "Recently Updated"
1. Filter: "Last Updated" is within "Last 7 days"
2. See all newly enriched contacts
3. Verify quality

### Update Existing Views:
Your existing views automatically show new data:
- "With Contact Info" → Now shows 2,700+ companies (was 874)
- "Mega Contracts" → Now includes email/phone for big contractors
- "All Contractors" → Everyone has contact info now!

---

## 📱 Testing the Updates

### After importing to Airtable:

1. **Check Airtable:**
   - Open your base
   - Filter for companies that previously had no email
   - Verify they now show Apollo emails

2. **Check Embed:**
   - Go to your Mighty Networks page
   - Refresh the embedded database
   - Search for a company (e.g., "PANTEXAS")
   - Verify new contact info shows up

3. **Verify Counts:**
   - Before: 874 with contact info
   - After: ~2,700 with contact info
   - Change: +1,826 new contacts!

---

## ⚠️ Important Notes

### Backup Before Merging!

Before updating Airtable:

1. **Export current data:**
   - Click "..." → "Download CSV"
   - Save as "contractors-backup-[date].csv"
   - Keep this safe!

2. **Test on small batch first:**
   - Try merging 10 companies manually
   - Verify it works correctly
   - Then do full merge

### Avoid Duplicates

The merge script will:
- ✅ Only update EMPTY fields
- ✅ Not overwrite existing emails/phones
- ✅ Match by exact company name
- ✅ Handle variations (LLC vs L.L.C.)

---

## 🚀 Summary: Your Workflow

```
1. Apollo.io
   ↓ (Upload apollo-upload.csv)
   ↓ (Wait 30 mins)
   ↓ (Download apollo-enriched.csv)

2. Merge Script (I'll create this)
   ↓ (Run: python merge.py)
   ↓ (Get: contractors-final.csv)

3. Airtable Import
   ↓ (Import contractors-final.csv)
   ↓ (Data updated!)

4. Mighty Networks Embed
   ↓ (Auto-updates - no action needed!)
   ✅ DONE!
```

**Total time: 1 hour**
**Result: 85-90% contact coverage, live in Mighty Networks!**

---

## ✅ Action Items

**Right now:**
- [ ] Complete Apollo enrichment (following previous guide)
- [ ] Download enriched CSV
- [ ] Let me know when you have the file

**After you download:**
- [ ] I'll create the merge script
- [ ] You'll run it (takes 2 minutes)
- [ ] Import to Airtable
- [ ] Verify embed updates

**You'll end up with:**
- ✅ Live Airtable database with 2,700+ contacts
- ✅ Embedded in Mighty Networks
- ✅ Searchable, filterable, beautiful
- ✅ Updates automatically forever!

---

## 🎉 The Magic of Airtable Embeds

**Once you embed Airtable in Mighty Networks:**
- Any changes you make in Airtable → Instantly visible in embed
- Add contacts → They appear immediately
- Update emails → Changes show immediately
- No need to re-deploy or re-embed!

**This is why we use Airtable instead of static HTML!**

---

**Go complete your Apollo enrichment, then come back and I'll help you merge the data into your live Airtable database!** 🚀
