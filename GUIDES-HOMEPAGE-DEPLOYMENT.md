# GovCon Giants Guides Homepage - Deployment Instructions

**Created:** December 11, 2025
**Purpose:** Deploy the guides homepage with database link at guides.govcongiants.org

---

## What Was Created

**File:** `guides-homepage-with-database-link.html`

### Features:
1. **Tabbed Navigation** - 5 main sections
2. **Finding Prime Contractors Tab (DEFAULT)** - Features the database prominently
3. **Featured Database Tool** - Highlighted with stats and direct link
4. **Responsive Design** - Mobile-friendly layout
5. **Professional Styling** - Matches GovCon Giants branding

### Database Link Location:
- **Tab:** "Finding Prime Contractors" (first tab, active by default)
- **Section:** Featured tool at top with green gradient background
- **Link:** https://guides.govcongiants.org/database
- **Stats Displayed:**
  - 2,768 Prime Contractors
  - $479.9B Contract Value
  - 625 SBLO Contacts

---

## Deployment Options

Since everything is routed in Vercel, you have two options:

### Option 1: Create New Vercel Project for Guides Homepage

**Step 1:** Create a new directory for the guides site
```bash
mkdir ~/govcon-giants-guides
cd ~/govcon-giants-guides

# Copy the homepage
cp /Users/ericcoffie/Bootcamp/guides-homepage-with-database-link.html ./index.html

# Initialize git
git init
git add .
git commit -m "Initial commit: GovCon Giants Guides Homepage"
```

**Step 2:** Push to GitHub
```bash
# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR-USERNAME/govcon-giants-guides.git
git branch -M main
git push -u origin main
```

**Step 3:** Deploy to Vercel
1. Go to https://vercel.com/dashboard
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Deploy

**Step 4:** Configure Custom Domain
1. In Vercel project settings → Domains
2. Add domain: `guides.govcongiants.org`
3. Vercel will provide DNS instructions
4. Add CNAME record in your DNS:
   - Name: `guides`
   - Value: `cname.vercel-dns.com`

---

### Option 2: Use Vercel Rewrites (Simpler - Recommended)

If you already have a Vercel project handling `govcongiants.org`, you can use rewrites to route `guides.govcongiants.org` to the homepage.

**Step 1:** Add the homepage to your existing project

If you have a main govcongiants.org project, add this file to it:
```bash
# In your main govcongiants.org project directory:
mkdir guides
cp /Users/ericcoffie/Bootcamp/guides-homepage-with-database-link.html ./guides/index.html
```

**Step 2:** Update `vercel.json` with rewrites
```json
{
  "version": 2,
  "cleanUrls": true,
  "trailingSlash": false,
  "rewrites": [
    {
      "source": "/",
      "destination": "/guides/index.html",
      "has": [
        {
          "type": "host",
          "value": "guides.govcongiants.org"
        }
      ]
    },
    {
      "source": "/database",
      "destination": "/federal-contractor-database/index.html",
      "has": [
        {
          "type": "host",
          "value": "guides.govcongiants.org"
        }
      ]
    }
  ]
}
```

This configuration:
- Routes `guides.govcongiants.org/` to the homepage
- Routes `guides.govcongiants.org/database` to the database tool
- Keeps them in the same Vercel project

**Step 3:** Commit and deploy
```bash
git add .
git commit -m "Add guides homepage with database link"
git push
```

Vercel will auto-deploy.

**Step 4:** Configure DNS (if not already done)
Add CNAME record:
- Name: `guides`
- Value: `cname.vercel-dns.com`

---

## Quick Preview

Before deploying, you can preview the homepage:

```bash
# Open in browser
open /Users/ericcoffie/Bootcamp/guides-homepage-with-database-link.html
```

Or use Python's simple HTTP server:
```bash
cd /Users/ericcoffie/Bootcamp
python3 -m http.server 8080
# Then visit: http://localhost:8080/guides-homepage-with-database-link.html
```

---

## Homepage Structure

### 5 Tabs:

1. **Finding Prime Contractors** (Default Active)
   - Featured: Federal Contractor Database tool
   - How to Use the Database guide
   - Identifying Target Primes guide
   - Contacting SBLOs guide
   - Understanding Subcontract Plans guide

2. **Getting Started**
   - SAM.gov registration
   - NAICS codes
   - Certifications
   - Capability statements

3. **Marketing & Outreach**
   - Capability statements
   - Email templates
   - LinkedIn strategies
   - Industry days

4. **Compliance**
   - FAR basics
   - Set-asides
   - Certifications (WOSB, 8(a), HUBZone)

5. **Resources**
   - SAM.gov link
   - SBA.gov link
   - FPDS link
   - GovCon Giants community link

---

## Database Link Details

### Where It Appears:

**Primary Location (Most Prominent):**
- Tab: "Finding Prime Contractors"
- Section: Featured tool with green gradient background
- Link text: "Access Database →"
- URL: `https://guides.govcongiants.org/database`

**Features:**
- Eye-catching green gradient box
- Stats displayed prominently
- Clear call-to-action button
- Positioned at the top of the first tab (highest visibility)

---

## Customization

### To Update Database Link:
Find this line in the HTML (around line 265):
```html
<a href="https://guides.govcongiants.org/database" class="btn">Access Database →</a>
```

### To Update Stats:
Find the stats section (around lines 246-260) and update the numbers.

### To Add More Guides:
Add to the `<ul class="guide-list">` sections in each tab.

### To Change Default Tab:
Move the `active` class to a different tab in both:
- The tab button: `<div class="tab active" onclick="openTab(event, 'finding-primes')">`
- The tab content: `<div id="finding-primes" class="tab-content active">`

---

## Testing Checklist

After deployment, verify:

- [ ] `https://guides.govcongiants.org` loads the homepage
- [ ] "Finding Prime Contractors" tab is active by default
- [ ] Database tool is featured at the top
- [ ] "Access Database →" button links to `https://guides.govcongiants.org/database`
- [ ] All 5 tabs switch correctly
- [ ] Page is mobile-responsive
- [ ] All external links work (govcongiants.org, sam.gov, etc.)
- [ ] Footer displays correctly

---

## Current Status

✅ **Homepage created** with database link prominently featured
✅ **Database tool highlighted** in "Finding Prime Contractors" tab
✅ **Responsive design** ready for all devices
⏭️ **Deployment needed** - Choose Option 1 or 2 above

---

## Files Created

1. `guides-homepage-with-database-link.html` - The homepage HTML
2. `GUIDES-HOMEPAGE-DEPLOYMENT.md` - This deployment guide

---

## Support

If you encounter issues:
1. Check Vercel deployment logs
2. Verify DNS propagation (can take 5-60 minutes)
3. Clear browser cache if changes don't appear
4. Test in incognito/private mode

---

## Next Steps

1. **Choose deployment option** (Option 1 or 2)
2. **Deploy to Vercel**
3. **Configure DNS** (if needed)
4. **Test the live site**
5. **Add real guide content** (currently placeholder links)

---

*Homepage created with database link - December 11, 2025*
