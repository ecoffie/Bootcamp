# 🔍 Database Connection Status

## Current Status

### ✅ What's Working:
- **guides.govcongiants.org** → ✅ Live and working (points to Vercel)
- **Database code** → ✅ Ready in `/federal-contractor-database/` folder
- **Vercel config** → ✅ `vercel.json` file exists

### ❌ What's NOT Connected:
- **database.govcongiants.org** → ❌ DNS record NOT added yet
- **Vercel deployment** → ❓ Need to verify if deployed

---

## 🎯 To Connect Database to guides.govcongiants.org (or database.govcongiants.org)

### Option 1: Use guides.govcongiants.org (Same Domain)
If you want the database at `guides.govcongiants.org`:

1. **Deploy database to Vercel** (if not already done)
2. **In Vercel Dashboard:**
   - Go to your project
   - Settings → Domains
   - Add domain: `guides.govcongiants.org`
   - Vercel will verify it matches existing DNS

### Option 2: Use database.govcongiants.org (Separate Subdomain) ⭐ RECOMMENDED
Keep guides and database as separate subdomains:

1. **Deploy database to Vercel** (if not already done)
2. **Add DNS record in GoDaddy:**
   ```
   Type: CNAME
   Name: database
   Value: cname.vercel-dns.com
   TTL: 1 Hour
   ```
3. **In Vercel Dashboard:**
   - Settings → Domains
   - Add domain: `database.govcongiants.org`
   - Wait for DNS verification (5-60 minutes)

---

## 📋 Step-by-Step: Connect Database Now

### Step 1: Check if Database is Deployed on Vercel

**Check Vercel Dashboard:**
1. Go to https://vercel.com/dashboard
2. Look for project: `federal-contractor-database`
3. If it exists → Skip to Step 2
4. If it doesn't exist → Deploy first (see Step 1B)

**Step 1B: Deploy to Vercel (if needed)**

```bash
cd /Users/ericcoffie/Bootcamp/federal-contractor-database

# Option A: Via Vercel Dashboard (Easiest)
# 1. Go to vercel.com
# 2. Import GitHub repo OR drag & drop the folder
# 3. Click Deploy

# Option B: Via CLI
npm install -g vercel
vercel login
vercel --prod
```

### Step 2: Add Custom Domain in Vercel

1. **In Vercel Dashboard:**
   - Open your `federal-contractor-database` project
   - Go to **Settings** → **Domains**
   - Click **Add Domain**
   - Type: `database.govcongiants.org`
   - Click **Add**

2. **Vercel will show you DNS instructions:**
   - It will say: "Add CNAME record: database → cname.vercel-dns.com"

### Step 3: Add DNS Record in GoDaddy

**Exact Steps:**

1. **Login to GoDaddy:** https://sso.godaddy.com
2. **Go to:** My Products → Domains
3. **Click:** DNS button next to `govcongiants.org`
4. **Click:** Add → CNAME
5. **Enter:**
   ```
   Type: CNAME
   Name: database
   Value: cname.vercel-dns.com
   TTL: 1 Hour
   ```
6. **Click:** Save

**You should now see TWO CNAME records:**
```
✅ guides   → cname.vercel-dns.com
✅ database → cname.vercel-dns.com
```

### Step 4: Wait for DNS Propagation

- **Time:** 5-60 minutes (usually 10-15 minutes)
- **Check status:** https://dnschecker.org/#CNAME/database.govcongiants.org
- **Vercel Dashboard:** Will show green checkmark when ready

### Step 5: Verify It Works

```bash
# Test DNS resolution
dig database.govcongiants.org +short
# Should show: cname.vercel-dns.com

# Visit in browser
open https://database.govcongiants.org
```

---

## 🔗 Your URLs After Setup

- **Database:** https://database.govcongiants.org
- **Guides:** https://guides.govcongiants.org (already working)
- **Main Site:** https://govcongiants.org

---

## ❓ Quick Check: Is Database Already Deployed?

Run this command to check:

```bash
# Check if Vercel project exists
curl -sI https://federal-contractor-database-bymo4pxb4-eric-coffies-projects.vercel.app | head -1
```

**If you get HTTP 200 or 301:** Database is deployed ✅  
**If you get HTTP 404 or error:** Need to deploy first ❌

---

## 🆘 Need Help?

**If DNS isn't working:**
- Wait longer (can take up to 24 hours)
- Clear browser cache
- Try incognito mode
- Check: https://dnschecker.org/#CNAME/database.govcongiants.org

**If Vercel deployment fails:**
- Check Vercel dashboard for error logs
- Verify `index.html` exists in the folder
- Check `vercel.json` configuration

**If you want to use guides.govcongiants.org instead:**
- The database would REPLACE the guides site
- Not recommended unless you want to merge them

---

## ✅ Next Steps

1. ✅ Check Vercel deployment status
2. ✅ Add DNS record in GoDaddy
3. ✅ Wait for DNS propagation
4. ✅ Test database at database.govcongiants.org
5. ✅ Share with GovCon Giants team

---

**Last Updated:** $(date)  
**Status:** Database code ready, DNS configuration pending


