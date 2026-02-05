# Quick Deployment Guide - Get Your Database Live in 5 Minutes

## 🚀 Fastest Method: Netlify Drop (Recommended)

### Step 1: Deploy to Netlify
1. Go to https://app.netlify.com/drop
2. Drag the entire `contractor-database-embed` folder onto the page
3. Wait 30 seconds for deployment
4. Copy your URL (will look like: `https://amazing-name-123456.netlify.app`)

### Step 2: Embed in Mighty Networks
1. Log into Mighty Networks
2. Go to your page/post editor
3. Look for "Embed" or "Add Content" button
4. Try these options:
   - **If you see "Website" or "iframe"**: Use the iframe code below
   - **If you see specific providers**: Try "Other" or "Custom"

**Iframe Code:**
```html
<iframe src="YOUR_NETLIFY_URL_HERE" width="100%" height="800px" frameborder="0" style="border: none;"></iframe>
```

### Step 3: If Embedding Doesn't Work
Create a button/link instead:
- Add a text block in Mighty Networks
- Add this text: **[🔍 Search Federal Contractors →](YOUR_NETLIFY_URL)**
- Links the button to your Netlify URL

---

## 🎨 Alternative: CodePen (If You Want to Customize)

### Step 1: Create CodePen
1. Go to https://codepen.io/pen/
2. In the **HTML** section:
   - Paste everything from `index.html` EXCEPT the `<script src="data-extract.js"></script>` line
3. In the **JS** section:
   - Paste contents of `data-extract.js`
   - Then paste the `<script>` section from `index.html` (starting from line ~287)
4. Click **Save** (you may need to create a free account)
5. Get your CodePen URL

### Step 2: Embed in Mighty Networks
1. In Mighty Networks editor, look for "CodePen" in the embed options
2. If available, paste your CodePen URL
3. If not available, use the iframe method above

---

## 💻 Professional Method: GitHub Pages

### Step 1: Create GitHub Repository
```bash
cd /Users/ericcoffie/Bootcamp/contractor-database-embed

# Initialize git
git init
git add .
git commit -m "Federal contractor database"

# Create repo at github.com (name it: contractor-database)
# Then run:
git remote add origin https://github.com/YOUR_USERNAME/contractor-database.git
git branch -M main
git push -u origin main
```

### Step 2: Enable GitHub Pages
1. Go to your repo on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select "main" branch
4. Click **Save**
5. Wait 2-3 minutes
6. Your URL will be: `https://YOUR_USERNAME.github.io/contractor-database/`

### Step 3: Embed in Mighty Networks
Use the iframe code with your GitHub Pages URL.

---

## 🎯 Which Method Should You Choose?

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Netlify Drop** | Quick & easy | Fastest, no signup needed | Random URL name |
| **CodePen** | Easy customization | Can edit live | May show CodePen branding |
| **GitHub Pages** | Professional | Custom domain support, version control | Requires GitHub account |
| **Vercel** | Developers | Fast, free SSL, custom domains | Requires signup |

---

## 🔧 Troubleshooting

### "This provider is not supported" Error
This means Mighty Networks doesn't support iframe embeds on your plan. Solutions:
1. **Use a link/button instead** (always works)
2. **Upgrade Mighty Networks plan** (if available)
3. **Check for "Custom Code" or "HTML" blocks** in your editor

### Database Loads Slowly
The database contains 2,768 contractors. This is normal on first load. The data is cached after the first load.

### Search Not Working
Make sure both `index.html` and `data-extract.js` are uploaded/deployed together.

### Styling Looks Broken
If hosting on CodePen, make sure all CSS is in the CSS section, not split across HTML and CSS sections.

---

## 📱 Mobile Optimization

The database is fully responsive and works on mobile devices. Test your embed on mobile before sharing widely.

---

## 🎨 Custom Branding (Optional)

To match your Mighty Networks branding, edit `index.html`:

**Change primary color** (currently purple):
Find all instances of `#7c3aed` and replace with your brand color.

**Change header** (line 49-59):
```css
.header {
    background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
}
```

**Add your logo** (after line 56):
```html
<img src="your-logo-url.png" alt="Logo" style="height: 40px; margin-bottom: 10px;">
```

---

## 📊 Analytics (Optional)

To track usage, add Google Analytics:

1. Get your GA4 tracking code
2. Add before `</head>` in `index.html`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

---

## ✅ Next Steps

1. Choose your deployment method above
2. Deploy the database
3. Test the URL in your browser
4. Try embedding in Mighty Networks
5. If embedding doesn't work, use a link/button
6. Share with your community!

---

## 🆘 Need Help?

Common Mighty Networks embed providers (check your platform):
- YouTube
- Vimeo
- SoundCloud
- Spotify
- Twitter/X
- Instagram
- Google Drive
- CodePen
- Custom iFrame (varies by plan)

If none work, a prominent link/button is often the best solution!
