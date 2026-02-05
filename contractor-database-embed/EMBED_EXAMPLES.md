# Embed Code Examples for Mighty Networks

## 📋 Basic iframe Embed

```html
<iframe
  src="YOUR_DEPLOYED_URL_HERE"
  width="100%"
  height="800px"
  frameborder="0"
  style="border: none; border-radius: 8px;">
</iframe>
```

**Replace `YOUR_DEPLOYED_URL_HERE` with:**
- Netlify: `https://your-site-name.netlify.app`
- GitHub Pages: `https://username.github.io/contractor-database`
- Vercel: `https://contractor-database.vercel.app`

---

## 🎨 Styled iframe Embed (Recommended)

```html
<div style="width: 100%; max-width: 1600px; margin: 0 auto;">
  <iframe
    src="YOUR_DEPLOYED_URL_HERE"
    width="100%"
    height="900px"
    frameborder="0"
    style="
      border: none;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    ">
  </iframe>
</div>
```

---

## 📱 Responsive iframe Embed

```html
<div style="position: relative; width: 100%; padding-bottom: 75%; overflow: hidden;">
  <iframe
    src="YOUR_DEPLOYED_URL_HERE"
    style="
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      border: none;
      border-radius: 8px;
    "
    frameborder="0">
  </iframe>
</div>
```

---

## 🔗 Link/Button Examples (If Embedding Doesn't Work)

### Example 1: Simple Link
```markdown
[🔍 Search Federal Contractors Database →](YOUR_DEPLOYED_URL_HERE)
```

### Example 2: Call-to-Action Button
```html
<a href="YOUR_DEPLOYED_URL_HERE" target="_blank" style="
  display: inline-block;
  padding: 15px 30px;
  background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transition: transform 0.2s;
">
  🔍 Search 2,768 Federal Contractors
</a>
```

### Example 3: Info Card with Link
```html
<div style="
  background: linear-gradient(135deg, #1e3a8a 0%, #7c3aed 100%);
  color: white;
  padding: 30px;
  border-radius: 12px;
  text-align: center;
  margin: 20px 0;
">
  <h3 style="margin: 0 0 10px 0; font-size: 24px;">🇺🇸 Federal Contractor Database</h3>
  <p style="margin: 0 0 20px 0; opacity: 0.9;">Search 2,768 prime contractors • $479.9B in contracts</p>
  <a href="YOUR_DEPLOYED_URL_HERE" target="_blank" style="
    display: inline-block;
    padding: 12px 24px;
    background: white;
    color: #1e3a8a;
    text-decoration: none;
    border-radius: 6px;
    font-weight: 700;
  ">
    Open Database →
  </a>
</div>
```

---

## 🎯 Mighty Networks Specific Tips

### If You Have "Custom Code" Block:
1. Add a "Custom Code" or "HTML" block to your page
2. Paste any of the iframe examples above
3. Save and publish

### If You Have "Embed" Option:
1. Look for supported providers (YouTube, Vimeo, etc.)
2. Check if "Other" or "Custom URL" is available
3. Try pasting your deployed URL
4. If it works, great! If not, use a link/button

### If Neither Works:
Use the link/button examples above. They work on ALL Mighty Networks plans and often provide a better user experience since the database opens in a new tab with full screen space.

---

## 📊 Advanced: Embedding with Parameters

You can pre-filter the database using URL parameters (future enhancement):

```html
<!-- Example: Show only companies with email -->
<iframe src="YOUR_URL?filter=has_email" ...></iframe>

<!-- Example: Search for specific NAICS -->
<iframe src="YOUR_URL?search=541330" ...></iframe>
```

*(Note: This requires custom JavaScript implementation)*

---

## 🔒 Privacy & Security Notes

- All data is public government contractor information
- No personal data collection
- No cookies or tracking (unless you add analytics)
- Safe to embed in any environment
- HTTPS enabled (on Netlify/GitHub Pages/Vercel)

---

## ✅ Testing Your Embed

Before adding to Mighty Networks:

1. **Test the URL** in your browser
2. **Test on mobile** (use browser dev tools or your phone)
3. **Check load time** (should be < 3 seconds)
4. **Try all filters** to ensure functionality
5. **Test search** with company names, NAICS codes, agencies

---

## 🎨 Customization Ideas

### Add Your Branding
Edit `index.html` to change:
- Colors (search for `#7c3aed` and `#1e3a8a`)
- Header text (line 56)
- Footer links (add after line 286)

### Add Analytics
Insert Google Analytics code before `</head>` in `index.html`

### Change Results Limit
Edit line 244 in `index.html`: change `slice(0, 100)` to your preferred number

### Add Welcome Message
Add after line 100 in `index.html`:
```html
<div class="welcome-banner">
  <h2>Welcome to Our Contractor Database</h2>
  <p>Your custom message here...</p>
</div>
```

---

## 📞 Common Mighty Networks Questions

**Q: Can I embed this without a paid plan?**
A: Depends on your plan. Try the iframe first. If it doesn't work, use a link/button.

**Q: Will it work on mobile?**
A: Yes! The database is fully responsive.

**Q: Can members search the database?**
A: Yes! All search and filter features work in the embed.

**Q: Will it slow down my page?**
A: No. The iframe loads independently and won't affect your page speed.

**Q: Can I customize the look?**
A: Yes! Edit the HTML/CSS files before deploying.

---

## 🚀 Ready to Embed?

1. ✅ Deploy your database (see DEPLOYMENT_GUIDE.md)
2. ✅ Copy one of the embed codes above
3. ✅ Replace `YOUR_DEPLOYED_URL_HERE` with your actual URL
4. ✅ Paste into Mighty Networks
5. ✅ Test and publish!

**Need help?** Check DEPLOYMENT_GUIDE.md for step-by-step instructions.
