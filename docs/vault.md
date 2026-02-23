# The Vault — Premium Document Library

**Live URL:** `guides.govcongiants.org`
**Project Path:** `/Users/ericcoffie/Projects/vault`
**Vercel Project:** `govcon-resources` (account: `evankoffdev-3209`)
**Framework:** Next.js 15 (App Router) + Tailwind CSS

## What It Is

A web app that hosts 125+ premium GovCon templates (proposals, contracts, bid forms, safety plans, etc.) behind a monthly password shared with paid members. Free visitors see all documents but with locked previews; after entering the password, everything unlocks.

## Architecture

- **Next.js Middleware** (`src/middleware.ts`) — intercepts requests to `/vault/premium/*` and checks for a valid `vault_access` cookie. Without it, direct PDF/DOCX links redirect to `/login`.
- **Cookie-based auth** — password validated against `VAULT_PASSWORD` env var; cookie includes SHA-256 hash of password+secret so it auto-expires when the password rotates.
- **Edge Runtime** — middleware uses Web Crypto API (`crypto.subtle`), not Node.js `crypto` (not available in Edge).
- **Build-time thumbnails** — `scripts/generate-thumbs.js` uses LibreOffice (headless) to convert Office docs to PDF, then pdf.js + Puppeteer to screenshot the first page of every document. Thumbnails stored in `public/vault/thumbs/`.
- **Client-side PDF fallback** — `PdfThumbnail.tsx` uses `pdfjs-dist` with IntersectionObserver to render PDF first pages if no pre-generated thumbnail exists.

## Key Files

| File | Purpose |
|------|---------|
| `src/app/layout.tsx` | Root layout (header, nav, AuthProvider, footer) |
| `src/app/page.tsx` | Homepage — all docs in category grid (uses DocumentThumbCard) |
| `src/app/category/[slug]/page.tsx` | Category view (uses DocumentList) |
| `src/app/search/page.tsx` | Search results |
| `src/app/login/page.tsx` | Password entry page |
| `src/app/api/validate/route.ts` | POST — validate password, set cookie |
| `src/app/api/check-session/route.ts` | GET — check auth status |
| `src/app/api/logout/route.ts` | POST — clear cookie |
| `src/middleware.ts` | Protects `/vault/premium/*` paths |
| `src/lib/auth-context.tsx` | React context: `hasPremiumAccess`, `refresh()`, `logout()` |
| `src/lib/types.ts` | `VaultDocument` interface (includes `tier`, `thumbnail` fields) |
| `src/components/DocumentThumbCard.tsx` | Grid card with thumbnail preview |
| `src/components/DocumentCard.tsx` | List-style card |
| `src/components/PdfThumbnail.tsx` | Client-side pdf.js thumbnail renderer |
| `src/components/HeaderAuthButton.tsx` | Unlock/Lock button in header |
| `src/components/HeaderSearch.tsx` | Search bar (Cmd+K shortcut) |
| `scripts/build-index.js` | Scans source folders -> `public/search-index.json` |
| `scripts/generate-thumbs.js` | Generates thumbnail JPEGs for all documents |

## Data Flow

1. **Source documents** live in `/Users/ericcoffie/Projects/Action Plan/The Vault ` (note trailing space)
2. `npm run build:index` scans that folder, copies files to `public/vault/premium/`, writes `public/search-index.json` with `tier: "premium"` on each document
3. `npm run build:thumbs` generates `public/vault/thumbs/*.jpg` for every document and adds `thumbnail` paths to the search index
4. `npm run build` (Next.js) builds the app
5. `npx vercel --prod` deploys to Vercel

## Environment Variables (Vercel)

| Variable | Purpose |
|----------|---------|
| `VAULT_PASSWORD` | Monthly password shared with paid members (current: `govcon-feb-2026`) |
| `VAULT_COOKIE_SECRET` | Random string for hashing cookies (set once) |

## Monthly Password Rotation

1. Vercel -> vault project -> Settings -> Environment Variables
2. Change `VAULT_PASSWORD` (use `printf`, NOT `echo`, to avoid trailing newline)
3. Redeploy or push a commit
4. Share new password in paid members group
5. Old sessions auto-expire (cookie hash includes password)

## Common Commands

```bash
# From /Users/ericcoffie/Projects/vault

# Rebuild search index (after adding/removing documents)
VAULT_PATH="/Users/ericcoffie/Projects/Action Plan/The Vault " npm run build:index

# Regenerate all document thumbnails (requires LibreOffice installed)
npm run build:thumbs

# Dev server
npm run dev

# Production build
npm run build

# Deploy to Vercel
npx vercel --prod --yes
```

## Dependencies

- **Runtime:** next, react, react-dom, lucide-react, pdfjs-dist
- **Dev:** puppeteer (thumbnail generation), tailwindcss, typescript
- **System:** LibreOffice (`/Applications/LibreOffice.app`) — required for Office doc -> PDF conversion during thumbnail generation

## Known Gotchas

- The Vault source folder has a **trailing space**: `"The Vault "` — must quote the path
- No "Free Resources" folder exists yet — all 125 documents are tagged `tier: "premium"`
- `useSearchParams()` requires `<Suspense>` boundary in Next.js App Router
- All React hooks must be called before early returns (React Error #310)
- Vercel env vars set via `echo` add trailing newlines — use `printf` instead
- Edge Runtime middleware cannot use Node.js `crypto` — use `crypto.subtle`
