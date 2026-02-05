# 🚀 Airtable Quick Setup - 10 Minutes to Live Database

## ✅ What You're Building

A beautiful, searchable database of 3,502 federal contractors embedded in Mighty Networks.

**Built-in features (automatic):**
- 🔍 Search bar
- 🎛️ Filter options
- 📊 Sortable columns
- 📱 Mobile responsive
- ✨ Professional design

---

## 📋 Step-by-Step Setup

### Step 1: Create Airtable Account (2 minutes)

**Airtable signup is now open in your browser!**

1. **Enter your email**
2. **Create password**
3. **Click "Sign up"**
4. **Verify email** (check your inbox)

**Choose plan:**
- ✅ **Free plan** is perfect for this!
- Supports up to 1,200 records per base
- **Note:** You have 3,502 records - see options below

---

### ⚠️ Important: Record Limit

**Free plan limit:** 1,200 records
**Your data:** 3,502 records

**Options:**

#### Option A: Show Top 1,200 Contractors (FREE)
- Filter by highest contract value
- Show the most important companies
- **Best for:** Getting started quickly

#### Option B: Upgrade to Plus ($10/month)
- 5,000 records per base
- Fits all your contractors
- **Best for:** Complete database

#### Option C: Split into Multiple Bases (FREE)
- Base 1: Top 1,200 contractors
- Base 2: Next 1,200 contractors
- Base 3: Remaining contractors
- **Best for:** Free but want everything

**Recommendation:** Start with Option A (top 1,200), see if that meets your needs!

---

### Step 2: Create Your First Base (1 minute)

After signing up:

1. Click **"Create a base"** or **"Start from scratch"**
2. **Name it:** "Federal Contractors Database"
3. Click **"Create"**

You'll see a blank spreadsheet-like interface.

---

### Step 3: Import Your CSV (3 minutes)

#### Option A: Import Top 1,200 Only (Free Plan)

Let me create a filtered CSV for you with just the top contractors:

**I'll create this file for you - give me a moment...**

#### Option B: Import All 3,502 (If You Upgraded)

1. **Click on table name** (default: "Table 1")
2. **Select:** "Import data" → "CSV file"
3. **Choose file:** `contractors-airtable.csv`
4. **Click "Import"**
5. Wait ~30 seconds for import

---

### Step 4: Rename and Organize (2 minutes)

1. **Rename table:**
   - Click "Table 1" → Rename to "Contractors"

2. **Airtable automatically created columns from your CSV:**
   - ✅ Company
   - ✅ SBLO Name
   - ✅ Email
   - ✅ Phone
   - ✅ NAICS Codes
   - ✅ Contract Count
   - ✅ Contract Value
   - ✅ Agencies
   - ✅ Has Subcontract Plan

3. **That's it!** The data is imported and ready.

---

### Step 5: Make It Look Professional (Optional - 5 minutes)

#### Quick Formatting:

**Set Contract Value as Currency:**
1. Click "Contract Value" column header
2. Click "Customize field type"
3. Select "Currency"
4. Choose "US Dollar ($)"
5. Precision: 0 decimals (for cleaner look)
6. Click "Save"

**Set Email as Email Type:**
1. Click "Email" column header
2. "Customize field type"
3. Select "Email"
4. Emails become clickable!

**Set Phone as Phone Type:**
1. Click "Phone" column header
2. "Customize field type"
3. Select "Phone number"
4. Phones become clickable on mobile!

**Result:** Professional formatting with clickable contacts!

---

### Step 6: Create Views (Optional but Recommended)

Views let users see data in different ways:

#### Create "With Contact Info" View:

1. Click **"Grid view"** dropdown (next to table name)
2. Select **"Create new view"**
3. Choose **"Grid"**
4. Name it: **"With Contact Info"**
5. Click **"Create view"**
6. Click **"Filter"** button
7. Add filter: **"Email" → "is not empty"**
8. Result: Shows only 874 companies with contact info!

#### Create "Top 100" View:

1. Create new view: "Top 100"
2. Click **"Sort"** button
3. Sort by: **"Contract Value"** → **Descending (Z→A)**
4. This shows biggest contractors first!

---

### Step 7: Share & Get Embed Code (2 minutes)

**This is the most important step!**

1. **Click "Share" button** (top right corner)

2. **Turn on public sharing:**
   - Toggle switch: **"Turn on public access"**
   - Or click: **"Create a shareable link"**

3. **Click "Create a shareable link"**
   - You'll see a public URL like: `https://airtable.com/shrXXXXXXXXXX`

4. **Get embed code:**
   - Click **"Embed this view"**
   - You'll see embed code like:
   ```html
   <iframe class="airtable-embed"
     src="https://airtable.com/embed/shrXXXXXXXXXX?backgroundColor=blue"
     frameborder="0" width="100%" height="533">
   </iframe>
   ```

5. **Copy the entire iframe code**

---

### Step 8: Customize Embed (Optional)

Before copying, you can customize:

**Background Color:**
- Choose: blue, cyan, green, yellow, orange, red, pink, purple, gray
- **Recommended:** `blue` (professional) or `purple` (modern)

**Height:**
- Change `height="533"` to `height="800"` for more visible rows

**View Controls:**
- Add to URL: `&viewControls=on`
- Allows users to switch between your different views

**Final embed code example:**
```html
<iframe class="airtable-embed"
  src="https://airtable.com/embed/shrXXXXXXXXXX?backgroundColor=blue&viewControls=on"
  frameborder="0"
  onmousewheel=""
  width="100%"
  height="800"
  style="background: transparent; border: 1px solid #ccc;">
</iframe>
```

---

### Step 9: Test Embed in Mighty Networks (5 minutes)

1. **Go to your Mighty Networks page**
2. **Edit the page** where you want the database
3. **Look for embed option:**
   - "Insert Embed"
   - "Add Content" → "Embed"
   - "Custom Code"
   - Or HTML block

4. **Paste your Airtable iframe code**

5. **Save and preview**

6. **Test:**
   - ✅ Search works
   - ✅ Can sort by clicking columns
   - ✅ Can filter (if viewControls=on)
   - ✅ Emails are clickable
   - ✅ Mobile responsive

---

## 🎨 What Users Will See

```
┌─────────────────────────────────────────────────────────────┐
│  Federal Contractors Database           🔍 Search     ⚙️   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Company          Email              Contract Value  Plan   │
│  ─────────────────────────────────────────────────────────  │
│  PANTEXAS         [empty]            $30.1B          Yes    │
│  THE BOEING       tina@boeing.com    $20.5B          Yes    │
│  TRIWEST          [empty]            $17.8B          Yes    │
│  ...                                                         │
│                                                             │
│  Showing X records                                          │
└─────────────────────────────────────────────────────────────┘
```

**Features automatically included:**
- 🔍 Search bar (top right)
- 📊 Sort (click any column header)
- 🎛️ Filter (filter button)
- 📱 Works on mobile
- ✉️ Clickable emails
- 📞 Clickable phones (on mobile)

---

## 🆘 Troubleshooting

### "Can't import - too many records"
**Solution:**
- Use the filtered CSV with top 1,200 contractors
- Or upgrade to Plus plan ($10/mo)

### "Share button is grayed out"
**Solution:**
- Make sure you've verified your email
- Try refreshing the page

### "Embed not showing in Mighty Networks"
**Solution:**
- Make sure you used "Insert Embed" option
- Try the link/button approach instead
- Contact Mighty Networks support about iframe embeds

### "Search isn't working"
**Solution:**
- Search bar is automatic - click magnifying glass icon
- It appears in top right of Airtable interface
- In the embed, users can search by typing in the search box

---

## 💡 Pro Tips

### 1. Start Simple
- Import data → Share → Embed
- Add fancy formatting later

### 2. Test Views
- Create different views for different purposes
- Each view gets its own embed code
- Switch between them to see what works best

### 3. Update Anytime
- Edit data in Airtable
- Changes appear in embed immediately
- No need to re-embed!

### 4. Mobile First
- Test on your phone
- Make sure it's readable
- Adjust column widths if needed

---

## ✅ Quick Checklist

- [ ] Sign up for Airtable
- [ ] Create new base
- [ ] Import contractors CSV
- [ ] Format key columns (Currency, Email, Phone)
- [ ] Turn on public sharing
- [ ] Get embed code
- [ ] Customize height & colors
- [ ] Paste in Mighty Networks
- [ ] Test functionality
- [ ] Done! 🎉

---

## 📊 What You'll Have

**After setup:**
- ✅ Professional contractor database
- ✅ Embedded in Mighty Networks
- ✅ Searchable by company, NAICS, agency
- ✅ Sortable by any column
- ✅ Filterable by criteria
- ✅ Updates in real-time when you edit
- ✅ Mobile responsive
- ✅ Built-in search bar (automatic!)

**Time to set up:** 10-15 minutes
**Maintenance:** Just edit in Airtable when needed
**Cost:** Free (for top 1,200) or $10/mo (for all 3,502)

---

## 🎯 Next Steps

1. **Right now:** Sign up on Airtable (page is open)
2. **After signup:** Come back and I'll help with the import
3. **Need top 1,200 CSV?** Let me know and I'll create it
4. **Questions?** Ask me at any step!

---

**Ready? Go sign up on Airtable and let me know when you're at the import step!** 🚀
