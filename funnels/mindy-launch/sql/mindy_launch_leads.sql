-- Backup store for Mindy Launch (and other funnel) signups.
-- Idempotent: safe to re-run. Run in the Mindy/Market Assassin Supabase SQL editor.

create table if not exists public.funnel_leads (
  id          uuid primary key default gen_random_uuid(),
  name        text,
  email       text not null,
  phone       text,
  source      text,                         -- e.g. 'mindy-launch'
  tags        text[] default '{}',
  raw         jsonb,                         -- full payload for safety
  created_at  timestamptz not null default now()
);

-- Fast lookups by source (e.g. all mindy-launch signups) and recency
create index if not exists funnel_leads_source_idx     on public.funnel_leads (source);
create index if not exists funnel_leads_created_at_idx  on public.funnel_leads (created_at desc);
create index if not exists funnel_leads_email_idx       on public.funnel_leads (email);

-- Service-role writes only (the API uses the service-role key); no public access.
alter table public.funnel_leads enable row level security;
