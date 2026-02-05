# 🚀 Apollo.io Setup - Step-by-Step Instructions

## ✅ Preparation Complete!

I've created **apollo-upload.csv** with **2,628 companies** that need contact enrichment.

This file contains ONLY companies missing email/phone (no point paying to enrich companies you already have!)

---

## 📋 Step-by-Step Setup

### Step 1: Create Apollo Account (5 minutes)

**Apollo.io signup page is now open in your browser!**

1. **Enter your email** (use your business email if possible)
2. **Create a password**
3. **Click "Sign Up"**
4. **Verify your email** (check inbox)
5. **Choose plan:**
   - Click "Start Free Trial" (14 days free!)
   - OR go straight to Basic ($49/mo) or Professional ($99/mo)

**Recommended:** Start with free trial, upgrade only if needed!

---

### Step 2: Skip the Onboarding (2 minutes)

After signup, Apollo will try to onboard you:

1. Click "Skip" or "Skip tour" on any onboarding popups
2. Or quickly fill out:
   - Company name: (your company)
   - Role: Business Development / Sales
   - Team size: 1-10
   - Click "Next" → "Skip" rest

**Goal:** Get to the main dashboard as fast as possible

---

### Step 3: Navigate to Data Enrichment (1 minute)

Once you're in Apollo:

1. Look for navigation menu (left side or top)
2. Find one of these options:
   - **"Enrich"** (direct option)
   - OR **"Data"** → **"Enrichment"**
   - OR **"Tools"** → **"Bulk Enrichment"**

**Note:** The exact menu location may vary based on Apollo version

---

### Step 4: Upload Your CSV (5 minutes)

On the Enrichment page:

1. **Click "Upload CSV"** or "New Enrichment" button
2. **Select file:** Choose `apollo-upload.csv`
3. **Map columns:**
   - Apollo will ask: "Which column has company names?"
   - Select: **"Company Name"** column
4. **Settings (if shown):**
   - ✅ Enable "Find emails"
   - ✅ Enable "Find phone numbers"
   - ✅ Enable "Find contact names"
   - Leave other options as default
5. **Click "Start Enrichment"** or "Upload"

---

### Step 5: Wait for Results (10-30 minutes)

Apollo will process your 2,628 companies:

**What's happening:**
- Apollo searches its database of 275M+ contacts
- Matches your company names
- Finds associated emails, phones, and contact names
- Verifies data accuracy

**Timeline:**
- Small batches (100 companies): ~5-10 minutes
- Your file (2,628 companies): ~15-30 minutes

**You can:**
- ✅ Close the window (it processes in background)
- ✅ Check status by refreshing the page
- ✅ You'll get an email when it's done

---

### Step 6: Review Results (5 minutes)

Once enrichment is complete:

1. **Go back to Enrichment page**
2. **Find your completed enrichment**
3. **Click to view results**

**You'll see:**
- Total companies processed: 2,628
- **Emails found:** ~1,800-2,100 (70-80% match rate)
- **Phone numbers found:** ~1,200-1,600 (45-60% match rate)
- **Contact names found:** ~1,500-1,900 (60-70% match rate)

**Match rates vary because:**
- Some companies are private (less public data)
- Some use unlisted numbers
- Some have outdated records

---

### Step 7: Download Enriched Data (2 minutes)

1. **Click "Export"** or "Download" button
2. **Select format:** CSV
3. **Choose columns to include:**
   - ✅ Company Name
   - ✅ Email (Work Email)
   - ✅ Phone (Direct Phone)
   - ✅ Contact Name (Full Name)
   - ✅ Title/Job Title
   - ✅ LinkedIn URL (optional)
   - ✅ Company Website (optional)
4. **Click "Download"**

**File will download as:** `apollo_enriched_[date].csv`

---

### Step 8: Review Downloaded Data (5 minutes)

Open the downloaded CSV to verify:

**What you should see:**

```csv
Company Name,Email,Phone,Contact Name,Title,LinkedIn
THE BOEING COMPANY,john.doe@boeing.com,(555) 123-4567,John Doe,Small Business Liaison Officer,linkedin.com/in/johndoe
LOCKHEED MARTIN,jane.smith@lmco.com,(555) 234-5678,Jane Smith,Business Development Manager,linkedin.com/in/janesmith
...
```

**Quality check:**
- ✅ Emails should end with company domain
- ✅ Phone numbers in US format
- ✅ Names should be real people (not "Admin" or "Info")
- ✅ Titles relevant (SBLO, Business Dev, Program Manager, etc.)

---

### Step 9: Import to Airtable (10 minutes)

Now we need to merge Apollo data with your existing Airtable:

**Option A: Manual Import (Easier)**

1. Open your Airtable base
2. Create new table: "Apollo Enriched Data"
3. Import the Apollo CSV
4. Manually copy/paste emails and phones to main table
   - Match by company name
   - Update Email column
   - Update Phone column
   - Update SBLO Name column

**Option B: Advanced (Using Airtable's Link Records)**

1. Import Apollo CSV to new table
2. Create "Linked Record" field linking to main Contractors table
3. Use Lookup fields to pull in enriched data
4. This keeps enrichment separate but linked

**I'll help you with the merge after you download the Apollo data!**

---

## 💰 Pricing Options

### Free Trial (14 days)
- ✅ **Perfect for one-time enrichment**
- ✅ Unlimited enrichment during trial
- ✅ Export your data
- ✅ Cancel anytime
- **Cost: $0**

**Strategy:** Use the trial, enrich all 2,628 companies, export, cancel!

---

### Basic Plan ($49/month)
- Unlimited email enrichment
- Limited phone numbers
- Good if you mainly need emails

---

### Professional Plan ($99/month)
- **RECOMMENDED if paying**
- Unlimited emails
- Unlimited phone numbers
- Direct dial numbers
- Mobile numbers
- Export capabilities

**Best for:** Full enrichment with phones + emails

---

### After Enrichment

**If using free trial:**
1. Download your enriched CSV
2. Import to Airtable
3. **Cancel subscription** (Settings → Billing → Cancel)
4. Keep your enriched data!

**If you paid:**
- Keep for ongoing enrichment
- Or cancel after first month
- Re-subscribe later if needed

---

## 🎯 Expected Results

Based on Apollo's typical match rates for B2B companies:

**From your 2,628 companies missing contacts:**

| Data Type | Match Rate | Expected Count |
|-----------|------------|----------------|
| **Emails** | 70-80% | ~1,800-2,100 |
| **Phone Numbers** | 45-60% | ~1,200-1,600 |
| **Contact Names** | 60-70% | ~1,500-1,900 |
| **Job Titles** | 60-70% | ~1,500-1,900 |

**Your Final Database:**
- Current contacts: 874
- New from Apollo: ~1,800-2,100
- **Total: 2,700-3,000 contacts (85-90% coverage)**

---

## ⚠️ Important Tips

### 1. Verify Company Names
Apollo matches by company name, so:
- Check for typos in your CSV
- Ensure names are complete (not abbreviated)
- Examples:
  - ✅ "Booz Allen Hamilton Inc"
  - ❌ "BAH" or "Booz Allen"

### 2. Download During Trial
If using free trial:
- ✅ Download enriched data BEFORE trial ends
- ✅ Export to CSV (you keep the file forever)
- ✅ Cancel before day 14 to avoid charges

### 3. Contact Quality
Apollo provides:
- **Work emails** (not personal Gmail/Yahoo)
- **Direct dials** (not main switchboard)
- **Current contacts** (not outdated info)

### 4. Privacy & Compliance
- ✅ Use for B2B outreach only
- ✅ Follow CAN-SPAM Act
- ✅ Provide opt-out options
- ✅ Don't scrape or resell data

---

## 🆘 Troubleshooting

### "Upload Failed"
- **Solution:** Make sure CSV is not open in Excel
- Save and close the file, try again

### "Low Match Rate"
- **Common for:** Very small companies, new companies
- **Solution:** Try manual research for high-priority ones

### "Can't Find Enrichment Page"
- **Solution:** Look for:
  - "Enrich" in top menu
  - "Data" → "Enrichment"
  - Or search "enrich" in Apollo search bar

### "Download Not Working"
- **Solution:** Try different browser
- Or contact Apollo support (very responsive!)

### "Need Help Importing to Airtable"
- Let me know after you download Apollo data
- I'll create a merge script or guide you through it

---

## 📧 Apollo Support

If you get stuck:
- **Help Center:** https://help.apollo.io
- **Live Chat:** Available in app (bottom right)
- **Email:** support@apollo.io
- **Response Time:** Usually within 1 hour

---

## ✅ Checklist

Follow these steps in order:

- [ ] Sign up for Apollo.io (free trial)
- [ ] Verify email
- [ ] Skip onboarding tour
- [ ] Navigate to Enrichment section
- [ ] Upload `apollo-upload.csv`
- [ ] Map "Company Name" column
- [ ] Start enrichment
- [ ] Wait 15-30 minutes
- [ ] Review results
- [ ] Download enriched CSV
- [ ] Import to Airtable (I'll help with this!)
- [ ] Celebrate 🎉 (85-90% contact coverage!)

---

## 🚀 You're Ready!

**Apollo.io signup page is open in your browser!**

**Your upload file is ready:** `apollo-upload.csv` (2,628 companies)

**Follow the steps above** and let me know when you:
1. Complete the enrichment
2. Download the results
3. Are ready to import to Airtable

I'll help you merge the Apollo data with your existing Airtable database! 🎯

---

## 📁 Files You Have

1. ✅ **apollo-upload.csv** - Ready to upload to Apollo (2,628 companies)
2. ✅ **contractors-airtable.csv** - Original full database (3,502 companies)
3. ✅ **APOLLO_SETUP_INSTRUCTIONS.md** - This guide

**Next step:** Sign up on Apollo.io and follow steps above!
