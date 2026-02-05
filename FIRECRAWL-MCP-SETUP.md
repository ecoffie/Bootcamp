# Firecrawl MCP Setup for DOT Directory Scraping

## Current Status
- ✅ Firecrawl SDK installed (`firecrawl-py`)
- ⚠️  API key not configured
- ⚠️  MCP server connection not established

## Option 1: Use Firecrawl MCP Server (Recommended)

If you have Firecrawl MCP server configured in Cursor:

1. **The MCP server should be accessible via Cursor's MCP integration**
2. **Run the script:** `python3 scrape-dot-with-firecrawl-mcp.py`
3. **The script will automatically use MCP if available**

## Option 2: Use Firecrawl API Key

1. **Get API key from:** https://firecrawl.dev
2. **Set environment variable:**
   ```bash
   export FIRECRAWL_API_KEY='your-api-key-here'
   ```
3. **Run the script:**
   ```bash
   python3 scrape-dot-with-firecrawl-mcp.py
   ```

## Option 3: Manual Download

If Firecrawl MCP is not available:

1. **Visit:** https://www.transportation.gov/osdbu/procurement-assistance/dot-subcontracting-directory
2. **Save the page** (right-click → Save As)
3. **Save as:** `dot-directory-manual.html` in the Bootcamp folder
4. **Run:** `python3 parse-dot-manual.py` (I can create this if needed)

## Scripts Created

- `scrape-dot-with-firecrawl-mcp.py` - Main scraper (uses Firecrawl MCP/SDK)
- `scrape-dot-directory.py` - Fallback scraper (regular HTTP)

## Next Steps

Once Firecrawl MCP is configured or API key is set:
1. Run: `python3 scrape-dot-with-firecrawl-mcp.py`
2. Script will extract SBLO contacts
3. Contacts will be added to `sblo-list-compiled.csv`




