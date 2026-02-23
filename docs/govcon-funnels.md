# GovCon Funnels — Lead Capture & Email System

**Project Path:** `/Users/ericcoffie/govcon-funnels`
**Framework:** Next.js 16 (App Router) + Tailwind CSS
**Live URL:** `funnels.govcongiants.org`

## Lead API (`/api/lead`)

All funnel forms POST to `/api/lead` which:
1. Creates/updates contact in GoHighLevel (GHL) with custom tags
2. Sends Slack notification to `#leads` channel
3. Sends confirmation email based on funnel source

## Key Files

| File | Purpose |
|------|---------|
| `src/app/page.tsx` | Main homepage (hero, resources, urgency, videos, premium, CTA) |
| `src/components/SiteNav.tsx` | Navigation bar — hides "Back to Home" on `/`, shows on all other pages (uses `usePathname()`) |
| `src/app/api/lead/route.ts` | Lead capture API endpoint |
| `src/lib/crm.ts` | GHL + Slack + webhook integrations |
| `src/lib/email.ts` | Email templates for all funnels |

## Funnel Sources & Email Templates

| Source | Funnel | Email Template |
|--------|--------|----------------|
| `opp` | Opportunity Hunter | Opportunity Hunter access email (with logo) |
| `surge` | 10 Free Resources | 10 resources download email |
| `free-course` | Free 12-Day Course | Course welcome email |
| `bootcamp` | General bootcamp | Bootcamp registration email |
| `feb28-bootcamp` | Feb 28 bootcamp | Bootcamp registration email |
| `proposal-bootcamp` | Proposal templates | 5 download links email |
| *(other)* | Any unknown source | Generic welcome email |

## Funnel Logo Images

| File | URL |
|------|-----|
| `public/images/opportunity-hunter-logo.png` | `https://funnels.govcongiants.org/images/opportunity-hunter-logo.png` |

## Environment Variables (Vercel Production)

| Variable | Purpose |
|----------|---------|
| `GHL_API_KEY` | GoHighLevel API key (PIT token) |
| `GHL_LOCATION_ID` | GHL location/sub-account ID |
| `SLACK_LEAD_WEBHOOK_URL` | Slack incoming webhook for lead notifications |
| `SMTP_USER` | Gmail address for sending emails |
| `SMTP_PASSWORD` | Gmail app password |
| `CRM_WEBHOOK_URL` | Optional: Zapier/Make webhook |

## Testing Lead Capture

```bash
curl -X POST https://funnels.govcongiants.org/api/lead \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","source":"opp","tags":["test"]}'
```

## Active Funnels

| Path | Pages | Description |
|------|-------|-------------|
| `/opp` | landing, upsell, downsell, thank-you | Opportunity Hunter tool |
| `/surge` | landing, upsell, downsell, thank-you | 10 free resources |
| `/free-course` | landing, upsell, downsell, thank-you, course | 12-day email course |
| `/bootcamp` | landing, upsell, downsell, thank-you | General bootcamp registration |
| `/feb-28-bootcamp` | landing, upsell, downsell, thank-you | February bootcamp |
| `/proposal-bootcamp` | (in `/Bootcamp/funnels/`) | Proposal writing templates |
