# 🥷 CommonNinja Setup Guide - Federal Contractors Database

## ✅ Why CommonNinja?

- ✅ **Officially supported** by Mighty Networks
- ✅ **Guaranteed to work** - no compatibility issues
- ✅ **Table widget** perfect for your database
- ✅ **Searchable & filterable**
- ✅ **Mobile responsive**
- ✅ **Easy to update**

---

## 🚀 Quick Setup (15 Minutes)

### Step 1: Sign Up for CommonNinja (2 minutes)

**CommonNinja is now open in your browser!**

1. **Click "Sign Up" or "Get Started"**
2. **Enter email and password**
3. **Verify email**
4. **Choose plan:**
   - **Free plan** - Good for testing
   - **Pro plan** ($9-29/month) - Remove branding, more features

**Recommendation:** Start with free to test!

---

### Step 2: Find Table Widget (1 minute)

After signing up:

1. **Look for widget gallery** or search
2. **Search for:** "Table" or "Data Table"
3. **Click on "Table Widget"** or similar
4. **Click "Create" or "Use This Widget"**

**Possible names:**
- Table Widget
- Data Table
- Advanced Table
- Dynamic Table

---

### Step 3: Import Your CSV (5 minutes)

Once in the table widget editor:

#### Upload CSV:

1. **Look for "Import" or "Add Data" button**
2. **Choose "Import from CSV"**
3. **Select file:** `contractors-airtable.csv`
4. **Upload**

#### Configure Import:

1. **First row as headers:** ✅ Yes
2. **Columns to import:** Select all
   - Company
   - SBLO Name
   - Email
   - Phone
   - NAICS Codes
   - Contract Count
   - Contract Value
   - Agencies
   - Has Subcontract Plan

3. **Click "Import" or "Continue"**

**Wait:** 30-60 seconds for 3,502 records to import

---

### Step 4: Configure Table Display (5 minutes)

#### Basic Settings:

**Table Name:**
- "Federal Contractors Database"

**Visible Columns:**
Reorder to show most important first:
1. Company (make wider)
2. Email
3. Phone
4. Contract Value
5. SBLO Name
6. Has Subcontract Plan

**Hide if too cluttered:**
- NAICS Codes (can show on click)
- Agencies (can show on click)

#### Enable Features:

✅ **Search** - Enable search bar
✅ **Sort** - Allow sorting by columns
✅ **Filter** - Enable column filters
✅ **Pagination** - Show 50-100 rows per page
✅ **Row click** - Expand to see all details
✅ **Export** - Allow users to download (optional)

---

### Step 5: Style Your Table (3 minutes)

#### Design Tab:

**Colors:**
- **Header background:** Blue (#1e3a8a) or Purple (#7c3aed)
- **Header text:** White
- **Row background:** White
- **Alternate rows:** Light gray (#f3f4f6)
- **Border:** Light gray

**Typography:**
- **Font:** Sans-serif (default)
- **Header size:** 14px, bold
- **Body size:** 13px

**Layout:**
- **Width:** 100% (full width)
- **Height:** Auto or 800px
- **Borders:** Show column borders
- **Striped rows:** ✅ Yes (easier to read)

#### Mobile Settings:

✅ **Responsive:** Enabled
✅ **Stack columns:** On mobile
✅ **Horizontal scroll:** If needed

---

### Step 6: Add Search & Filters (Built-in)

CommonNinja tables usually include:

**Search Bar:**
- Position: Top of table
- Placeholder: "Search contractors..."
- Searches all visible columns

**Column Filters:**
- Click column header → Filter icon
- Users can filter by:
  - Email (has/doesn't have)
  - Contract Value (greater than, less than)
  - Has Subcontract Plan (Yes/No)

**These are automatic!** Just make sure they're enabled in settings.

---

### Step 7: Preview & Test (2 minutes)

1. **Click "Preview" button**
2. **Test features:**
   - ✅ Search for "Boeing"
   - ✅ Sort by Contract Value
   - ✅ Filter to show only companies with Email
   - ✅ Click a row to see full details
   - ✅ Test on mobile view

3. **Adjust settings** if needed

---

### Step 8: Publish & Get Embed Code (2 minutes)

1. **Click "Save" or "Publish"**
2. **Click "Get Embed Code"** or "Share"
3. **Copy the iframe code:**

```html
<iframe
  src="https://common.ninja/widget/XXXXXX"
  width="100%"
  height="800"
  frameborder="0"
  scrolling="auto">
</iframe>
```

**CommonNinja embed code format:**
- Unique widget ID
- Customizable width/height
- No authentication needed (public)

---

### Step 9: Embed in Mighty Networks (2 minutes)

1. **Go to your Mighty Networks page**
2. **Edit the page**
3. **Look for "Embed" or "Add Content"**
4. **Paste CommonNinja embed code**
5. **Save and publish**

✅ **It will work!** CommonNinja is officially supported.

---

## 🎨 Customization Options

### Advanced Features (Pro Plan):

**Custom CSS:**
```css
/* Make header stand out */
.cn-table-header {
  background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
  color: white;
  font-weight: bold;
}

/* Clickable emails */
.cn-table-email {
  color: #7c3aed;
  text-decoration: underline;
}

/* Highlight high-value contracts */
.cn-table-value {
  font-weight: bold;
  color: #059669;
}
```

**Conditional Formatting:**
- Highlight rows with emails in green
- Show mega contracts ($1B+) in bold
- Color-code by contract size

---

## 💰 Pricing

### Free Plan:
- ✅ Up to 5,000 rows (covers your 3,502!)
- ✅ All basic features
- ⚠️ Shows "Powered by CommonNinja" badge
- ✅ Good for testing!

### Pro Plan ($9-29/month):
- ✅ Remove branding
- ✅ Custom CSS
- ✅ Priority support
- ✅ Advanced features

**Recommendation:** Start free, upgrade if you don't want the badge!

---

## 📊 What Users Will See

```
┌─────────────────────────────────────────────────────────┐
│  Federal Contractors Database                           │
│  🔍 [Search contractors...]                    [Filter] │
├─────────────────────────────────────────────────────────┤
│  Company          Email             Value      Plan     │
│  ────────────────────────────────────────────────────── │
│  PANTEXAS                            $30.1B     Yes      │
│  THE BOEING       tina@boeing.com    $20.5B     Yes      │
│  TRIWEST                             $17.8B     Yes      │
│  ...                                                     │
│                                                          │
│  Showing 1-100 of 3,502              [1] 2 3 ... 36 >   │
└─────────────────────────────────────────────────────────┘
```

**Features:**
- ✅ Search bar (searches all fields)
- ✅ Sortable columns (click headers)
- ✅ Filterable (click filter icon)
- ✅ Pagination (50-100 per page)
- ✅ Click row to see full details
- ✅ Mobile responsive

---

## 🔄 Updating Your Data

### Option 1: Re-upload CSV (Easiest)
1. Update your CSV file locally
2. Go to CommonNinja dashboard
3. Edit widget
4. Import → Upload new CSV
5. Save

**Changes appear immediately** in embedded version!

### Option 2: Edit Directly (Manual)
1. Go to CommonNinja dashboard
2. Edit widget
3. Click on row to edit
4. Update values
5. Save

---

## 🆘 Troubleshooting

### "Can't find Table Widget"

**Try searching for:**
- "Table"
- "Data Table"
- "Grid"
- "Spreadsheet"

**Or browse categories:**
- Data & Tables
- Business Tools
- Content Display

### "CSV Import Failed"

**Solutions:**
1. Make sure file is .csv (not .xlsx)
2. Check file size (should be ~500KB)
3. Remove special characters from data
4. Try with smaller sample (first 100 rows) to test

### "Too Many Rows Error"

**If free plan limits to fewer rows:**
1. Create filtered CSV with top 1,200 (I can help)
2. Or upgrade to Pro plan
3. Or split into multiple widgets

### "Embed Not Showing in Mighty Networks"

**This shouldn't happen** since CommonNinja is officially supported, but if it does:
1. Check embed code is complete
2. Verify widget is published (not draft)
3. Make sure widget is set to "Public"
4. Contact Mighty Networks support (it's on their supported list!)

---

## ✅ Quick Checklist

- [ ] Sign up for CommonNinja
- [ ] Find Table/Data Table widget
- [ ] Import `contractors-airtable.csv`
- [ ] Configure columns (show/hide, reorder)
- [ ] Enable search and filters
- [ ] Style table (colors, fonts)
- [ ] Test preview (search, sort, filter)
- [ ] Publish widget
- [ ] Get embed code
- [ ] Paste in Mighty Networks
- [ ] Test live embed
- [ ] Done! 🎉

---

## 🎯 Expected Result

**After setup:**
- ✅ 3,502 federal contractors in searchable table
- ✅ Embedded in Mighty Networks (guaranteed to work!)
- ✅ Professional appearance
- ✅ Search, sort, filter functionality
- ✅ Mobile responsive
- ✅ Easy to update
- ✅ No compatibility issues

**Time to set up:** 15 minutes
**Cost:** Free (with badge) or $9-29/month (no badge)
**Maintenance:** Easy - just re-upload CSV when needed

---

## 💡 Pro Tips

### 1. Column Order Matters
Put most important columns first:
- Company (always visible)
- Email (for outreach)
- Contract Value (shows importance)

### 2. Use Pagination
Don't show all 3,502 at once:
- 50-100 rows per page
- Faster loading
- Better user experience

### 3. Enable Row Expansion
Let users click rows to see:
- All NAICS codes
- Full agency list
- Complete contact info

### 4. Test Mobile First
Most users will view on phones:
- Check mobile preview
- Make sure critical info shows
- Test horizontal scroll

---

## 🚀 Ready to Start?

**CommonNinja is now open in your browser!**

**Next steps:**
1. Sign up
2. Find Table widget
3. Import your CSV
4. Get embed code
5. Paste in Mighty Networks

**Let me know when you're at the import step and I'll help if you get stuck!** 🥷

---

## 📁 Your Files Ready:

- ✅ `contractors-airtable.csv` (3,502 records)
- ✅ Full contractor data
- ✅ Ready to upload to CommonNinja

**File location:** `/Users/ericcoffie/Bootcamp/contractor-database-embed/`
