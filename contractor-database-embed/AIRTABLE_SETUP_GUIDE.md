# 🎯 Airtable Setup for Mighty Networks Embedding

## ✅ Solution: Use Airtable (Works with Mighty Networks!)

Airtable embeds are **officially supported** by Mighty Networks and will work perfectly for your contractor database.

---

## 📁 Your CSV File is Ready

**File:** `contractors-airtable.csv`
- **3,502 contractor records** (includes all data from GovConGiants)
- Cleaned and formatted for Airtable import
- Includes: Company, SBLO Name, Email, Phone, NAICS, Contract Value, Agencies, etc.

---

## 🚀 Step-by-Step Airtable Setup

### Step 1: Create Free Airtable Account
1. Go to **https://airtable.com/signup**
2. Sign up for a **free account** (no credit card needed)
3. Verify your email

### Step 2: Create a New Base
1. Click **"Create a base"** or **"Start from scratch"**
2. Name it: **"Federal Contractors Database"**
3. A blank base will be created

### Step 3: Import Your CSV
1. Click the **dropdown arrow** next to your table name (default: "Table 1")
2. Select **"Import data"** → **"CSV file"**
3. Click **"Choose CSV file"** and select `contractors-airtable.csv`
4. Click **"Import"**
5. Airtable will automatically:
   - Create columns for each field
   - Import all 3,502 contractors
   - Detect data types

### Step 4: Configure Table (Optional but Recommended)
1. **Rename table** to "Contractors"
2. **Set field types:**
   - `Contract Value` → Number (Currency)
   - `Email` → Email
   - `Phone` → Phone number
   - `NAICS Codes` → Long text
   - `Has Subcontract Plan` → Single select (Yes/No)
3. **Add filters** for better viewing:
   - Filter by "Has Email" = not empty
   - Filter by "Contract Value" > certain amount
4. **Create views:**
   - "All Contractors" (default)
   - "With Email Contact" (filtered)
   - "Mega Contracts ($1B+)" (filtered)
   - "By Agency" (grouped)

### Step 5: Get Embed Code
1. Click **"Share"** button (top right)
2. Toggle **"Turn on public access"** (allows embedding)
3. Click **"Create a shareable link"**
4. Click **"Embed this view"**
5. Copy the **iframe embed code**

It will look like:
```html
<iframe class="airtable-embed" src="https://airtable.com/embed/YOUR_SHARE_ID?backgroundColor=blue" frameborder="0" onmousewheel="" width="100%" height="533" style="background: transparent; border: 1px solid #ccc;"></iframe>
```

---

## 🎨 Customize Your Airtable View

### Add Search Functionality
Airtable's embed includes built-in:
- ✅ Search bar
- ✅ Sorting by any column
- ✅ Filtering options
- ✅ Grid/Gallery/Calendar views

### Styling Options
When getting embed code, you can choose:
- **Background color** (blue, cyan, green, yellow, orange, red, pink, purple, gray)
- **Height** (adjust in iframe code)
- **Which view to show** (if you create multiple views)

### Recommended View Settings
1. **Hide unnecessary fields** (like "Source", "Address" if empty)
2. **Reorder columns**: Company → Email → Phone → NAICS → Contract Value → Agencies
3. **Sort by**: Contract Value (descending) - shows biggest contractors first
4. **Enable**: "Allow viewers to copy data"

---

## 📋 Embed in Mighty Networks

### Step 1: Copy Airtable Embed Code
From Airtable: Share → Embed this view → Copy code

### Step 2: Add to Mighty Networks
1. Go to your Mighty Networks page
2. Click **"Edit"** or **"Add Content"**
3. Click **"Insert Embed"** or look for embed option
4. **Paste your Airtable iframe code**
5. **Adjust height** if needed (recommend 800px):
   ```html
   height="800"
   ```
6. **Save** and **Publish**

### Example Embed Code (Customize yours):
```html
<iframe
  class="airtable-embed"
  src="https://airtable.com/embed/YOUR_SHARE_ID?backgroundColor=blue"
  frameborder="0"
  width="100%"
  height="800"
  style="background: transparent; border: 1px solid #ccc;">
</iframe>
```

---

## ✅ Why Airtable Works Better

| Feature | Airtable | Vercel/Custom HTML |
|---------|----------|-------------------|
| Mighty Networks Support | ✅ Official | ❌ Blocked |
| Built-in Search | ✅ Yes | Manual coding |
| Sorting | ✅ Click any column | Manual coding |
| Filtering | ✅ Built-in | Manual coding |
| Mobile Responsive | ✅ Perfect | Varies |
| Updates | ✅ Edit anytime | Redeploy needed |
| Free | ✅ Yes (5 bases) | ✅ Yes |

---

## 🎯 Features Your Users Will Have

When embedded in Mighty Networks, users can:
- ✅ **Search** for any company, NAICS, or agency
- ✅ **Sort** by any column (click column header)
- ✅ **Filter** using Airtable's filter bar
- ✅ **View details** - click any row to expand
- ✅ **Copy data** - if you enable it
- ✅ **View on mobile** - fully responsive
- ✅ **Export** - if you enable it

---

## 🔄 Updating Your Database

Need to add/update contractors?
1. Log into Airtable
2. Edit directly in the table
3. Changes appear **instantly** in your Mighty Networks embed
4. No redeployment needed!

---

## 📊 Advanced: Multiple Views

Create different views for different purposes:

**View 1: "All Contractors"** (default)
- Shows everything
- Sorted by contract value

**View 2: "With Email Contact"**
- Filter: Email is not empty
- Perfect for outreach

**View 3: "By Agency"**
- Grouped by Agencies field
- Easy to find contractors by agency

**View 4: "Top 100"**
- Filter: Show only top 100 by contract value
- Faster loading

Each view gets its own embed code!

---

## 🆓 Airtable Free Plan Limits

- ✅ **1,200 records per base** (you have 3,502 - see note below)
- ✅ **Unlimited bases**
- ✅ **2GB attachments**
- ✅ **Public sharing/embedding**

**Note:** You have 3,502 contractors, which exceeds the free limit. Options:
1. **Split into multiple bases** (Top 1000, Others)
2. **Upgrade to Plus** ($10/user/month, 5,000 records)
3. **Filter to most relevant** contractors (e.g., only those with email)

For now, import all - Airtable will let you know if you hit limits.

---

## 🎉 Quick Start Checklist

- [ ] Sign up for Airtable (https://airtable.com/signup)
- [ ] Create new base
- [ ] Import `contractors-airtable.csv`
- [ ] Configure fields (optional)
- [ ] Turn on public access
- [ ] Get embed code
- [ ] Paste into Mighty Networks
- [ ] Test and publish!

**Estimated time: 10-15 minutes** ⏱️

---

## 🆘 Troubleshooting

**"Import failed"**
→ Make sure CSV file is not open in Excel/Numbers

**"Can't turn on public access"**
→ Check your Airtable account is verified

**"Embed not showing in Mighty Networks"**
→ Make sure you used "Insert Embed" option, not just paste

**"Table is too wide"**
→ Hide unnecessary columns in Airtable view settings

**"Want to add more data"**
→ Just add rows in Airtable - updates live instantly!

---

## 📞 Support

- **Airtable Help:** https://support.airtable.com
- **Mighty Networks Embeds:** Check the guide in your admin panel
- **Your CSV File:** `contractors-airtable.csv` (ready to import!)

---

## 🎊 Ready to Go!

Your CSV file `contractors-airtable.csv` is ready with **3,502 federal contractors**.

**Next step:** Go to https://airtable.com/signup and follow Step 1 above!

**Sources:**
- [Airtable embedding in Mighty Networks](https://community.mightynetworks.com/posts/65450029)
- [Mighty Networks Embeds Guide](https://faq.mightynetworks.com/en/articles/9718687-can-i-use-external-embeds)
- [Mighty Networks Integrations List](https://supplygem.com/mighty-networks-integrations/)
