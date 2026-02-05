# Federal Contractor Database - Custom Embed for Mighty Networks

This is a custom embeddable version of the GovConGiants Federal Contractor Database (2,768 contractors with $479.9B in contract data).

## What's Included

- `index.html` - Main database interface with search and filtering
- `data-extract.js` - Complete contractor data (auto-extracted from original database)

## Features

✅ **Search** - Search by company name, NAICS code, or agency
✅ **Filters** - Filter by contact availability, subcontract plans, and contract size
✅ **Clean Design** - Optimized for embedding in Mighty Networks
✅ **Responsive** - Works on desktop and mobile
✅ **Fast** - No external dependencies

## How to Embed in Mighty Networks

Mighty Networks has restrictions on embedding custom HTML directly. Here are your options:

### Option 1: Host on Supported Platform (RECOMMENDED)

1. **Upload to a hosting service** that Mighty Networks supports:
   - **CodePen** (free, easiest)
   - **GitHub Pages** (free)
   - **Netlify** (free)
   - **Vercel** (free)

2. **Steps for CodePen** (Fastest):
   - Go to https://codepen.io/pen/
   - Copy contents of `index.html` into the HTML section
   - Copy contents of `data-extract.js` into the JS section
   - Click "Save" and get your CodePen URL
   - In Mighty Networks, use the CodePen embed option with your URL

3. **Steps for GitHub Pages** (Most Professional):
   ```bash
   # Initialize git repository
   cd contractor-database-embed
   git init
   git add .
   git commit -m "Initial contractor database"

   # Create GitHub repo and push
   # (Create repo at github.com first)
   git remote add origin YOUR_GITHUB_REPO_URL
   git branch -M main
   git push -u origin main

   # Enable GitHub Pages in repo settings
   # Your site will be at: https://USERNAME.github.io/REPO-NAME/
   ```

4. **Steps for Netlify/Vercel**:
   - Drag and drop this entire folder to Netlify or Vercel
   - Get your deployment URL
   - Use that URL in Mighty Networks

### Option 2: Link Instead of Embed

If embedding doesn't work, create a prominent button/link in Mighty Networks that opens the database in a new tab.

### Option 3: Custom HTML Block (if available)

If your Mighty Networks plan supports custom HTML blocks:

1. Go to your Mighty Networks page editor
2. Add a "Custom Code" or "HTML" block
3. Paste this iframe code:

```html
<iframe src="YOUR_HOSTED_URL_HERE" width="100%" height="800px" frameborder="0" style="border: none; border-radius: 8px;"></iframe>
```

## Testing Locally

Open `index.html` in your web browser to test the database locally before hosting.

## Customization

### Change Colors

Edit the CSS in `index.html`:
- Line 53-56: Header gradient colors
- Line 65-67: Search input focus color
- Line 144-146: Company card hover color

### Adjust Results Limit

Change line 244 in `index.html`:
```javascript
resultsDiv.innerHTML = companiesToShow.slice(0, 100) // Change 100 to your desired limit
```

## Database Statistics

- **Total Contractors:** 2,768
- **Total Contract Value:** $479.9B
- **Data Sources:** SBA Prime Directory FY24, DHS Prime Contractors Page
- **Last Updated:** 2024

## Support

For issues with:
- **The database itself:** Contact GovCon Giants
- **Embedding in Mighty Networks:** Check [Mighty Networks embed documentation](https://faq.mightynetworks.com/en/articles/9718687-can-i-use-external-embeds)
- **Technical issues with this code:** Contact the developer who created this for you

## License

Data sourced from GovCon Giants (https://guides.govcongiants.org). Please respect their terms of use.
