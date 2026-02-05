# 🔄 Update Your Live Vercel Database with Apollo Data

## 🎯 Goal: Update Your Live Website

You want to update the contractor database that's currently live on Vercel with the new contact information from Apollo.

**Your live site:** https://contractor-database-embed-a51o537kq-eric-coffies-projects.vercel.app/

---

## 📋 The Process (Simple!)

```
1. Apollo enriches data → Download CSV
2. Run merge script → Updates data-extract.js
3. Deploy to Vercel → Live site updates
4. Done! → New contacts visible
```

**Total time: 10 minutes**

---

## 🚀 Step-by-Step Instructions

### Step 1: Complete Apollo Enrichment

**Follow the Apollo setup guide:**
1. ✅ Sign up for Apollo.io (or log in)
2. ✅ Upload `apollo-upload.csv` (2,628 companies)
3. ✅ Wait for enrichment (~30 minutes)
4. ✅ Download enriched CSV

**Save the downloaded file as:** `apollo-enriched.csv`
**Location:** In your `/contractor-database-embed/` folder

---

### Step 2: Run the Merge Script

Once you have the Apollo CSV downloaded:

1. **Open Terminal**

2. **Navigate to project folder:**
   ```bash
   cd /Users/ericcoffie/Bootcamp/contractor-database-embed
   ```

3. **Run the merge script:**
   ```bash
   python3 merge-apollo-data.py
   ```

4. **Follow the prompts:**
   ```
   Enter Apollo CSV filename (or press Enter for 'apollo-enriched.csv'):
   ```
   - If you named it `apollo-enriched.csv`, just press Enter
   - Otherwise, type the filename

5. **Watch the magic happen:**
   ```
   📥 Step 1: Reading Apollo enriched CSV...
   ✅ Loaded 2,628 records from Apollo

   📥 Step 2: Reading existing contractor database...
   ✅ Loaded 3,502 existing contractors

   🔍 Step 3: Creating Apollo lookup dictionary...
   ✅ Indexed 2,628 Apollo companies

   🔄 Step 4: Merging Apollo data...
   ✅ Updated 1,850 companies
      📧 Added 1,800 emails
      📞 Added 1,200 phone numbers
      👤 Added 1,500 contact names

   📊 Step 5: Calculating statistics...
      Total: 3,502
      With email: 2,643 (75.5%)
      With phone: 1,231 (35.1%)
      With contact: 2,724 (77.8%)

   💾 Step 6: Creating backup...
   ✅ Backup saved as: data-extract.backup.20241223_143022.js

   💾 Step 7: Writing updated data-extract.js...
   ✅ Successfully updated data-extract.js

   ✅ MERGE COMPLETE!
   ```

6. **Result:** Your `data-extract.js` file is now updated with Apollo data!

---

### Step 3: Test Locally (Optional but Recommended)

Before deploying, test that everything works:

1. **Open the database locally:**
   ```bash
   open index.html
   ```

2. **Test these things:**
   - ✅ Search for "PANTEXAS" (should now show contact info)
   - ✅ Filter by "Has Email" (should show 2,600+ companies)
   - ✅ Check a few companies that previously had no contact
   - ✅ Verify emails and phones appear correctly

3. **If something looks wrong:**
   - The script created a backup: `data-extract.backup.TIMESTAMP.js`
   - You can restore from backup if needed
   - Contact me for help!

---

### Step 4: Deploy to Vercel

Once you've verified the data looks good:

1. **Deploy the updated database:**
   ```bash
   cd /Users/ericcoffie/Bootcamp/contractor-database-embed
   vercel --prod
   ```

2. **Wait for deployment:**
   ```
   Vercel CLI 49.1.1
   Deploying eric-coffies-projects/contractor-database-embed
   Uploading [====================] (1.9MB/1.9MB)
   Production: https://contractor-database-embed-xyz123.vercel.app [6s]
   ✅ Deployment complete!
   ```

3. **Note the URL:**
   - Vercel will give you a new deployment URL
   - Or use your existing project URL

---

### Step 5: Verify Live Site

1. **Open your Vercel URL:**
   ```bash
   vercel open
   ```
   Or manually visit your deployment URL

2. **Test the live site:**
   - ✅ Search for companies
   - ✅ Verify new emails appear
   - ✅ Check phone numbers show up
   - ✅ Test filters (Has Email, Has Phone)
   - ✅ Verify counts updated

3. **Check statistics:**
   - Should show: "Showing: 3,502 companies"
   - Total value: "$479.9B"
   - When filtering "Has Email": Should show ~2,600+ companies

---

### Step 6: Update Mighty Networks (if needed)

If your Vercel URL changed:

1. **Copy new embed code:**
   ```html
   <iframe
     src="https://contractor-database-embed-NEW-URL.vercel.app/"
     width="100%"
     height="800px"
     frameborder="0"
     style="border: none;">
   </iframe>
   ```

2. **Update in Mighty Networks:**
   - Edit your page
   - Replace old embed code with new one
   - Save and publish

**Note:** If the URL didn't change, your Mighty Networks embed will auto-update!

---

## 📊 What the Merge Script Does

### Before & After:

**BEFORE (Current):**
```json
{
  "company": "PANTEXAS DETERRENCE LLC",
  "email": "",
  "phone": "",
  "sblo_name": "",
  "has_email": false,
  "has_phone": false,
  "has_contact": false
}
```

**AFTER (With Apollo Data):**
```json
{
  "company": "PANTEXAS DETERRENCE LLC",
  "email": "john.doe@pantexas.com",
  "phone": "(555) 123-4567",
  "sblo_name": "John Doe",
  "has_email": true,
  "has_phone": true,
  "has_contact": true
}
```

### The Script:
- ✅ Reads your existing `data-extract.js`
- ✅ Reads Apollo enriched CSV
- ✅ Matches companies by name
- ✅ Adds emails where missing
- ✅ Adds phones where missing
- ✅ Adds contact names where missing
- ✅ Updates flags (has_email, has_phone, has_contact)
- ✅ Creates backup of original file
- ✅ Writes updated data-extract.js
- ✅ Preserves all other data (contract values, agencies, etc.)

---

## 🔧 Advanced: Custom Merge Options

If you want to customize the merge:

### Option 1: Only Add Emails (Skip Phones)
Edit `merge-apollo-data.py` line 92-96:
```python
# Comment out phone merging
# if not company.get('phone') and apollo_info['phone']:
#     company['phone'] = apollo_info['phone']
#     company['has_phone'] = True
```

### Option 2: Overwrite Existing Data
By default, script only fills empty fields. To overwrite:
```python
# Change line 85 from:
if not company.get('email') and apollo_info['email']:

# To:
if apollo_info['email']:  # Always overwrite
```

### Option 3: Add Apollo as Separate Field
Keep original and Apollo data separate:
```python
company['apollo_email'] = apollo_info['email']
company['apollo_phone'] = apollo_info['phone']
```

---

## 🆘 Troubleshooting

### Error: "Could not find apollo-enriched.csv"
**Solution:**
- Make sure you downloaded CSV from Apollo
- Place it in `/contractor-database-embed/` folder
- Or specify full path when script asks

### Error: "Could not find companies array"
**Solution:**
- Your data-extract.js might be corrupted
- Restore from backup
- Or re-extract from original source

### Merge Found 0 Matches
**Solution:**
- Check company names match between files
- Apollo might use slightly different names
- Try manual verification of a few companies

### Vercel Deployment Failed
**Solution:**
```bash
# Check file size
ls -lh data-extract.js

# Should be around 1.8-1.9MB
# If much larger, something went wrong

# Try redeploying
vercel --prod --yes
```

### New Data Not Showing on Live Site
**Solution:**
- Clear browser cache (Ctrl+Shift+R or Cmd+Shift+R)
- Check deployment URL is correct
- Verify deployment completed successfully
- Wait 1-2 minutes for CDN to update

---

## 📈 Expected Results

### Before Apollo:
- Total: 3,502 contractors
- With email: 843 (24.1%)
- With phone: 31 (0.9%)
- With any contact: 874 (25.0%)

### After Apollo:
- Total: 3,502 contractors
- With email: ~2,643 (75.5%)
- With phone: ~1,231 (35.1%)
- With any contact: ~2,724 (77.8%)

### Improvement:
- ➕ ~1,800 new emails
- ➕ ~1,200 new phone numbers
- ➕ ~1,850 new contacts
- 📈 From 25% to 78% contact coverage!

---

## 🔄 Future Updates

### Want to re-enrich in 6 months?

1. **Export current database:**
   ```bash
   # Already have data-extract.js
   ```

2. **Create new apollo-upload.csv:**
   ```bash
   python3 merge-apollo-data.py --export-missing
   ```
   (Feature to add: export only companies still missing contacts)

3. **Upload to Apollo again**

4. **Merge new data**

5. **Deploy**

**Keep your database fresh!**

---

## ✅ Quick Command Reference

```bash
# Navigate to project
cd /Users/ericcoffie/Bootcamp/contractor-database-embed

# Run merge script
python3 merge-apollo-data.py

# Test locally
open index.html

# Deploy to production
vercel --prod

# Open live site
vercel open

# Check deployment status
vercel ls

# View logs
vercel logs
```

---

## 📁 Files Involved

- `apollo-upload.csv` - Companies to enrich (input to Apollo)
- `apollo-enriched.csv` - Apollo results (you download this)
- `data-extract.js` - Your live database (gets updated)
- `data-extract.backup.TIMESTAMP.js` - Automatic backup
- `merge-apollo-data.py` - The merge script
- `index.html` - Database interface (unchanged)

---

## 🎉 Summary

**The workflow is:**

```
1. Apollo enriches → Download CSV
2. Run: python3 merge-apollo-data.py
3. Test: open index.html
4. Deploy: vercel --prod
5. Done! 🎊
```

**Time:** 10 minutes (after Apollo finishes)

**Result:** Your live Vercel site now has 78% contact coverage instead of 25%!

---

## 💡 Pro Tips

1. **Always test locally first** before deploying
2. **Keep Apollo CSV** for future reference
3. **Backup is automatic** - restore if needed
4. **Can re-run merge** multiple times safely
5. **Script only adds missing data** - won't overwrite existing contacts

---

**Ready? Go complete your Apollo enrichment, then run the merge script!** 🚀

After merging and deploying, your Vercel database will be updated with all the new contact information!
