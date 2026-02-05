# How to Export to PDF

## For the December Spend Forecast PDF

1. **Open `december-spend-forecast.html`** in your browser
2. **Press `Cmd+P` (Mac) or `Ctrl+P` (Windows)**
3. **Select "Save as PDF"**
4. **Important Settings:**
   - Enable **"Background graphics"** to preserve colors
   - Set margins to **Default** or **Minimum**
   - Make sure "More settings" shows "Background graphics" is checked
5. **Click "Save"** and name it "December-2025-Spend-Forecast.pdf"

The document is already formatted for 8 pages with proper page breaks!

---

## For the Bootcamp Presentation Slides

## Method 1: Browser Print to PDF (Easiest)

1. **Open the presentation** in your browser (`index.html`)

2. **Print the page:**
   - **Chrome/Edge**: Press `Cmd+P` (Mac) or `Ctrl+P` (Windows/Linux)
   - **Firefox**: Press `Cmd+P` (Mac) or `Ctrl+P` (Windows/Linux)
   - **Safari**: Press `Cmd+P` (Mac)

3. **Select "Save as PDF"** as the destination:
   - In Chrome/Edge: Choose "Save as PDF" from the destination dropdown
   - In Safari: Click "PDF" button, then "Save as PDF"
   - In Firefox: Choose "Print to File" or "Save to PDF"

4. **Configure print settings:**
   - **Layout**: Portrait (recommended)
   - **Margins**: Default or None
   - **Background graphics**: Enable this to keep colors and gradients
   - **Scale**: 100% (default)

5. **Click "Save"** and choose where to save your PDF

### Tips for Better PDF Output:
- ✅ Enable "Background graphics" in print settings to keep colors
- ✅ Use Chrome or Safari for best results
- ✅ Each slide will automatically print on a separate page
- ✅ The print.css file ensures proper formatting

## Method 2: Using Browser DevTools (Advanced)

If you want more control:

1. Open the presentation in Chrome/Edge
2. Press `F12` to open DevTools
3. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
4. Type "print" and select "Show Rendering"
5. Set the emulation to "Screen" or "Print"
6. Then use Print to PDF as described above

## Method 3: Command Line (For Developers)

If you have Node.js installed, you can use tools like:
- **Puppeteer**: Convert HTML to PDF programmatically
- **wkhtmltopdf**: Command-line tool for HTML to PDF conversion

## Method 4: Online HTML to PDF Converters

Upload your `index.html` to services like:
- HTML2PDF.com
- WeasyPrint (if you use Python)
- Prince XML (paid, professional)

**Note**: These may not preserve all styling perfectly, so browser print-to-PDF is usually best.

## Troubleshooting

**Problem**: Slides are overlapping or not on separate pages
- **Solution**: Make sure `print.css` is linked in the HTML (it should be)

**Problem**: Colors/gradients are missing
- **Solution**: Enable "Background graphics" in print settings

**Problem**: Navigation buttons appear in PDF
- **Solution**: The print.css automatically hides them, but if they appear, check that print.css is linked correctly

## After Exporting

Your PDF will have:
- ✅ Each slide on a separate page
- ✅ Professional formatting
- ✅ All text and content preserved
- ✅ Print-friendly layout

