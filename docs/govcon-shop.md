# GovCon Shop — E-commerce & Product Emails

**Project Path:** `/Users/ericcoffie/govcon-shop`
**Framework:** Next.js 16 (App Router) + Tailwind CSS
**Live URL:** `shop.govcongiants.org`

## Free Resources Email Flow

1. User submits email at `/free-resources` or `/all-free-resources`
2. `POST /api/request-verification` -> creates lead in Supabase, sends verification email
3. User clicks verification link -> `POST /api/verify-email-token`
4. After verification: welcome email sent, lead synced to GHL + Slack

## CRM Integration

**File:** `src/lib/crm.ts`

| Function | Purpose |
|----------|---------|
| `sendToGoHighLevel()` | Create/update contact in GHL v2 API |
| `sendToSlack()` | Send lead notification to Slack webhook |
| `sendLeadToCrm()` | Calls both GHL + Slack in parallel |

## Stripe Webhook (`/api/stripe-webhook`)

Handles `checkout.session.completed` events and sends product-specific confirmation emails.

**Product IDs & Emails:**

| Product | Stripe Product ID | Email Function |
|---------|-------------------|----------------|
| Ultimate Giant Bundle | `prod_RqZdWzZyPM3jlQ` | `sendUltimateBundleEmail()` |
| Opportunity Hunter Pro | `prod_RqZSrMmcvPwzSN` | `sendOpportunityHunterProEmail()` |
| Federal Contractor Database | `prod_RpMU88VU0DlnGa` | `sendDatabaseAccessEmail()` |
| Market Assassin Legacy | `prod_RpMQJlzqKcfaFL` | `sendAccessCodeEmail()` |
| Market Assassin Standard | `prod_SB3FnPexrDxCVJ`, `prod_SBPN0rBnAPXWPf` | `sendMarketAssassinEmail('standard')` |
| Market Assassin Premium | `prod_SB3GvDp5VHuIXi`, `prod_SBPN6bqlFGZjsH` | `sendMarketAssassinEmail('premium')` |
| Recompete Tracker | `prod_TmMbpcfofGpDZd` | `sendRecompeteTrackerEmail()` |
| Content Reaper | `prod_TqrkVq4DfRrrPY` | `sendContentReaperEmail()` |

## Email Functions (`src/lib/send-email.ts`)

| Function | Purpose | Logo |
|----------|---------|------|
| `sendFreeResourceVerificationEmail()` | Verification link for free resources | -- |
| `sendFreeResourcesWelcomeEmail()` | Welcome after email verification | -- |
| `sendDatabaseAccessEmail()` | Federal Contractor Database access | -- |
| `sendOpportunityHunterProEmail()` | Opportunity Hunter Pro access | -- |
| `sendUltimateBundleEmail()` | Ultimate Giant Bundle welcome | -- |
| `sendAccessCodeEmail()` | Market Assassin Legacy (one-time code) | -- |
| `sendMarketAssassinEmail()` | Market Assassin Standard/Premium | market-assassin-logo.png |
| `sendRecompeteTrackerEmail()` | Recompete Tracker access | -- |
| `sendContentReaperEmail()` | Content Reaper access | content-reaper-logo.png |

## Product Logo Images

| File | URL |
|------|-----|
| `public/images/market-assassin-logo.png` | `https://shop.govcongiants.org/images/market-assassin-logo.png` |
| `public/images/content-reaper-logo.png` | `https://shop.govcongiants.org/images/content-reaper-logo.png` |

## Environment Variables (Vercel Production)

| Variable | Purpose |
|----------|---------|
| `GHL_API_KEY` | GoHighLevel API key (PIT token) |
| `GHL_LOCATION_ID` | GHL location/sub-account ID |
| `SLACK_LEAD_WEBHOOK_URL` | Slack incoming webhook for lead notifications |
| `SMTP_USER` | Gmail address for sending emails |
| `SMTP_PASSWORD` | Gmail app password |
| `STRIPE_SECRET_KEY` | Stripe API secret key |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key |

## Key Files

| File | Purpose |
|------|---------|
| `src/app/api/request-verification/route.ts` | Free resource email verification request |
| `src/app/api/verify-email-token/route.ts` | Verify email token, send welcome email |
| `src/app/api/stripe-webhook/route.ts` | Handle Stripe checkout completions |
| `src/lib/send-email.ts` | All email templates (nodemailer) |
| `src/lib/crm.ts` | GHL + Slack integrations |
| `src/lib/rate-limit.ts` | Rate limiting for verification requests |

## Deploy

```bash
cd /Users/ericcoffie/govcon-shop
npx vercel --prod --yes
```
