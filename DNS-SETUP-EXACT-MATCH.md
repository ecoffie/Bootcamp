# 🎯 DNS Setup - Match guides.govcongiants.org Configuration

## ✅ What I Found

Your existing subdomain **guides.govcongiants.org** is configured with:
```
Type: CNAME
Name: guides
Value: cname.vercel-dns.com
```

We need to configure **database.govcongiants.org** the **exact same way**.

---

## 🔧 Add DNS Record in GoDaddy (Exact Steps)

### Step 1: Login to GoDaddy

1. Go to: https://sso.godaddy.com
2. Login with your credentials

### Step 2: Access DNS Settings

1. Click **"My Products"** in the top menu
2. Find **govcongiants.org** in your domain list
3. Click the **"DNS"** button next to it
4. You'll see your current DNS records (including the one for "guides")

### Step 3: Add CNAME Record (Same as guides)

1. Scroll down to the DNS Records section
2. Click **"Add"** button
3. Select **"CNAME"** from the dropdown

**Enter these EXACT values (same as guides):**
```
Type: CNAME
Name: database
Value: cname.vercel-dns.com
TTL: 1 Hour
```

4. Click **"Save"** or **"Add Record"**

### Step 4: Verify You See Both Records

You should now see:
```
✅ guides.govcongiants.org → CNAME → cname.vercel-dns.com
✅ database.govcongiants.org → CNAME → cname.vercel-dns.com
```

---

## ⏰ Wait for DNS Propagation

- **Time**: 5-30 minutes (usually 10-15 minutes)
- **Check status**: https://dnschecker.org/#CNAME/database.govcongiants.org

---

## ✅ Test When Ready

### Test the CNAME Record:
```bash
dig database.govcongiants.org +short
```

**Expected output:**
```
cname.vercel-dns.com.
76.76.21.123
66.33.60.35
```

### Visit Your Site:
https://database.govcongiants.org

Should load your Federal Contractor Database!

---

## 🔍 Visual Guide

**In GoDaddy DNS Manager, you'll see something like:**

| Type  | Name     | Value                  | TTL    |
|-------|----------|------------------------|--------|
| CNAME | guides   | cname.vercel-dns.com   | 1 Hour |
| CNAME | database | cname.vercel-dns.com   | 1 Hour |

---

## 📊 Current Status

✅ **Vercel Project**: Deployed and live
✅ **Production URL**: https://federal-contractor-database-bymo4pxb4-eric-coffies-projects.vercel.app
✅ **Domain Added to Vercel**: database.govcongiants.org
✅ **Reference Config**: guides.govcongiants.org (working)
⏳ **Waiting For**: DNS CNAME record in GoDaddy

---

## 🆘 If You Need Help

If you can't access GoDaddy or need someone else to add the record, send them this:

**Message:**
```
Hi,

Can you please add this DNS record for database.govcongiants.org?

Type: CNAME
Name: database
Value: cname.vercel-dns.com
TTL: 1 Hour

This is the same configuration as guides.govcongiants.org

Thanks!
```

---

## 🎉 That's It!

Once you add the CNAME record in GoDaddy, your database will be live at:

**https://database.govcongiants.org**

It will match the exact same setup as guides.govcongiants.org! 🚀
