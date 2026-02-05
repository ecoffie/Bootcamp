# 🌐 DNS Setup Instructions for database.govcongiants.org

## ✅ What's Already Done

- ✅ **Deployed to Vercel** - Your database is live!
- ✅ **Production URL**: https://federal-contractor-database-bymo4pxb4-eric-coffies-projects.vercel.app
- ✅ **Custom domain added**: database.govcongiants.org is registered in Vercel

## 🔧 What You Need to Do: Add DNS Record

Your domain `govcongiants.org` is currently using **GoDaddy nameservers**:
- ns17.domaincontrol.com
- ns18.domaincontrol.com

You need to add **ONE DNS record** to point the subdomain to Vercel.

---

## Option A: Add A Record (Recommended by Vercel)

### In GoDaddy DNS Settings:

1. **Login to GoDaddy**: https://sso.godaddy.com
2. Go to **My Products** → **Domains**
3. Click **DNS** next to `govcongiants.org`
4. Click **Add** → **A Record**

**Enter these details:**
```
Type: A
Name: database
Value: 76.76.21.21
TTL: 1 Hour (or 3600 seconds)
```

5. Click **Save**

---

## Option B: Add CNAME Record (Alternative)

If you prefer CNAME instead:

1. **Login to GoDaddy**: https://sso.godaddy.com
2. Go to **My Products** → **Domains**
3. Click **DNS** next to `govcongiants.org`
4. Click **Add** → **CNAME**

**Enter these details:**
```
Type: CNAME
Name: database
Value: cname.vercel-dns.com
TTL: 1 Hour
```

5. Click **Save**

---

## ⏰ Wait for DNS Propagation

- **Typical time**: 5-30 minutes
- **Maximum time**: Up to 24 hours
- **Check status**: https://dnschecker.org/#A/database.govcongiants.org

---

## ✅ Verify It's Working

### Once DNS propagates:

1. Visit: **https://database.govcongiants.org**
2. You should see your Federal Contractor Database
3. Test search functionality
4. Verify all links work

### Before DNS propagates:

Use the Vercel URL: https://federal-contractor-database-bymo4pxb4-eric-coffies-projects.vercel.app

---

## 🔍 Troubleshooting

### "DNS not updating"
- **Wait longer**: GoDaddy can take 30-60 minutes
- **Clear cache**: Try incognito mode in browser
- **Check spelling**: Ensure "database" subdomain is correct

### "SSL Certificate Error"
- Wait for DNS to fully propagate first
- Vercel automatically provisions SSL (takes ~5 minutes after DNS)
- Try https://database.govcongiants.org again after 10 minutes

### "Still showing Vercel 404"
- Verify the A record points to **76.76.21.21**
- Check: https://dnschecker.org/#A/database.govcongiants.org
- If still issues, check Vercel dashboard for domain status

---

## 📊 After Setup

### Share Your Database:

**Your URLs:**
- **Custom Domain**: https://database.govcongiants.org (after DNS)
- **Vercel URL**: https://federal-contractor-database-bymo4pxb4-eric-coffies-projects.vercel.app (works now)

### Email Template for GovCon Giants:

```
Subject: Federal Contractor Database Now Live at database.govcongiants.org

Hi [GovCon Giants Team],

Great news! I've deployed the federal contractor database as a subdomain
of govcongiants.org:

🔗 https://database.govcongiants.org

(Note: DNS is propagating, may take 30-60 minutes to be fully live)

Backup URL: https://federal-contractor-database-bymo4pxb4-eric-coffies-projects.vercel.app

Features:
✅ 2,768 federal contractors with $479.9B in contract data
✅ Real-time search and filtering
✅ Export to CSV
✅ Branded for GovCon Giants with links to your site
✅ Mobile responsive
✅ Lightning fast (hosted on Vercel edge network)

This complements your training by helping members identify WHO to
partner with, while your platform teaches them HOW to win contracts.

Let me know if you'd like any adjustments!

Best,
Eric Coffie
```

---

## 🎯 Quick Reference

| Item | Value |
|------|-------|
| **Production Site** | https://federal-contractor-database-bymo4pxb4-eric-coffies-projects.vercel.app |
| **Custom Domain** | https://database.govcongiants.org |
| **DNS Provider** | GoDaddy (ns17.domaincontrol.com) |
| **Required Record** | A record: database → 76.76.21.21 |
| **Or CNAME** | database → cname.vercel-dns.com |
| **Vercel Dashboard** | https://vercel.com/eric-coffies-projects/federal-contractor-database |

---

## 🚀 Done!

Once you add the DNS record in GoDaddy, you're all set! The site will be live at:

**https://database.govcongiants.org**

🎉 Congratulations on deploying your federal contractor database!
