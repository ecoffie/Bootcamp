# Domains & Deployments

## Vercel Team: `eric-coffies-projects`

| Domain | Vercel Project | Purpose |
|--------|----------------|---------|
| `govcongiants.org` | govcon-funnels | Main homepage (was Framer, now Vercel) |
| `www.govcongiants.org` | govcon-funnels | Main homepage (www redirect) |
| `funnels.govcongiants.org` | govcon-funnels | Funnels subdomain |
| `freegovconcourse.com` | govcon-funnels | Free course landing |
| `tools.govcongiants.org` | market-assassin | Market Assassin tool |
| `shop.govcongiants.org` | govcon-shop | E-commerce/products |
| `guides.govcongiants.org` | govcon-resources | The Vault (premium docs) |
| `vault.govcongiants.org` | vault | Vault alternate URL |
| `database.govcongiants.org` | federal-contractor-database | Contractor database |
| `bootcamp.govcongiants.org` | january-bootcamp-page | Bootcamp landing page |

## DNS Configuration

**Registrar:** GoDaddy
**Nameservers:** `ns1.vercel-dns.com`, `ns2.vercel-dns.com`

All DNS is managed through Vercel after nameserver delegation (February 2026).

## Framer Project (Legacy Homepage)

**Project:** GCG
**URL:** `https://framer.com/projects/GCG--v9UQvXswg7VBTLQFdr1X-8i9uz`
**Status:** Deprecated (domain moved to Vercel February 2026)

### Framer API Automation

| File | Purpose |
|------|---------|
| `/Users/ericcoffie/govcon-funnels/update-framer.mjs` | Framer API automation script |
| `/Users/ericcoffie/govcon-funnels/update-framer.js` | Framer connection test script |

**Node IDs:**
- Page: `Xe878dnHC` (path: `/page`)
- Desktop: `MlCI5JDag`
- Embed: `qe2Z5r3kb`

**API Key:** `3a7ef1ce-8e56-440d-b05f-016e295357b0`

```bash
# Test Framer connection
node /Users/ericcoffie/govcon-funnels/update-framer.js

# Update Framer embed with HTML
node /Users/ericcoffie/govcon-funnels/update-framer.mjs [html-path] [--dry-run] [--publish]
```
