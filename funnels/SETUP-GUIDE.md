# GovCon Giants Funnels - Setup Guide

## Overview
This folder contains marketing funnels that capture leads and send them to GoHighLevel CRM.

## Funnels Included
| Funnel | Source Tag | Description |
|--------|------------|-------------|
| January Bootcamp | `january-bootcamp` | Monthly bootcamp registration |
| Surge Bootcamp | `surge-bootcamp` | Q4 spending surge resources |
| Free Course | `free-course` | GovCon fundamentals course |
| Opportunity Hunter | `opportunity-hunter` | Contract search tool |
| Free Resources | `free-resources` | Resource library access |

## Lead Data Captured
- **Name** (split into firstName/lastName)
- **Email**
- **Phone**
- **Source** (which funnel)
- **Tags** (for segmentation)

---

## Deployment Steps

### 1. Deploy to Vercel

```bash
cd /Users/ericcoffie/Bootcamp/funnels
vercel
```

Follow the prompts to deploy.

### 2. Set Up GoHighLevel Webhook

1. Log into GoHighLevel
2. Go to **Settings > Integrations > Webhooks**
3. Create a new **Inbound Webhook**
4. Copy the webhook URL (looks like: `https://services.leadconnectorhq.com/hooks/...`)

### 3. Add Webhook URL to Vercel

```bash
vercel env add GHL_WEBHOOK_URL
```

Paste your GoHighLevel webhook URL when prompted.

Or add it in the Vercel dashboard:
- Go to your project > Settings > Environment Variables
- Add: `GHL_WEBHOOK_URL` = `<your-webhook-url>`

### 4. Redeploy

```bash
vercel --prod
```

---

## GoHighLevel Webhook Setup

### Recommended GHL Workflow

When a lead hits the webhook, set up a workflow in GHL:

1. **Trigger:** Inbound Webhook
2. **Actions:**
   - Create/Update Contact
   - Add tags based on `tags` field
   - Add to pipeline (e.g., "Free Lead")
   - Start email sequence based on source:
     - `january-bootcamp` → January Bootcamp Sequence
     - `free-resources` → Free Resources Nurture
     - `free-course` → Course Onboarding
     - etc.

### Email Sequences by Funnel

| Funnel | Recommended Sequence |
|--------|---------------------|
| january-bootcamp | `/email-sequence-bootcamp-january-2026.md` |
| surge-bootcamp | `/email-sequence-for-surge-downloads/` |
| free-resources | `/december-downloads-sequence/` |
| free-course | Course onboarding sequence |
| opportunity-hunter | Tool follow-up sequence |

---

## Webhook Payload Format

The API sends this JSON to GoHighLevel:

```json
{
  "firstName": "John",
  "lastName": "Smith",
  "email": "john@example.com",
  "phone": "555-123-4567",
  "source": "january-bootcamp",
  "tags": ["january-bootcamp", "bootcamp-registrant", "january-2026"],
  "customFields": {
    "lead_source": "january-bootcamp",
    "signup_date": "2026-01-21T12:00:00.000Z"
  }
}
```

---

## Testing

### Test the API locally:

```bash
curl -X POST http://localhost:3000/api/lead \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"555-0000","source":"test"}'
```

### Test on production:

```bash
curl -X POST https://your-vercel-url.vercel.app/api/lead \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"555-0000","source":"test"}'
```

---

## File Structure

```
funnels/
├── api/
│   └── lead.js          # Serverless API endpoint
├── january-bootcamp/
│   ├── 1-landing.html
│   ├── 2-upsell.html
│   └── 3-thank-you.html
├── surge-bootcamp/
│   ├── 1-landing.html
│   ├── 2-upsell.html
│   ├── 3-downsell.html
│   └── 4-thank-you.html
├── free-course/
│   ├── 1-landing.html
│   └── 2-thank-you.html
├── opportunity-hunter/
│   ├── 1-landing.html
│   ├── 2-upsell.html
│   └── 3-thank-you.html
├── free-resources/
│   ├── 1-landing.html
│   ├── 2-upsell.html
│   ├── 3-downsell.html
│   ├── 4-thank-you.html
│   └── resources.html
├── package.json
├── vercel.json
└── SETUP-GUIDE.md
```

---

## Troubleshooting

### Leads not appearing in GHL
1. Check Vercel logs: `vercel logs`
2. Verify `GHL_WEBHOOK_URL` is set correctly
3. Test webhook URL directly in GHL

### Form not submitting
1. Check browser console for errors
2. Verify API endpoint is accessible
3. Check CORS settings in `api/lead.js`

### Wrong tags/source
Each landing page has hardcoded source and tags. Edit the `<script>` section at the bottom of each `1-landing.html` file.
