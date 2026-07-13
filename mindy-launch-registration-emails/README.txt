========================================================
MINDY LAUNCH — REGISTRATION PROMO EMAILS (GHL SEND GUIDE)
========================================================
Event: The Mindy Launch — Saturday, July 25, 2026, 10:00 AM ET (Free, Zoom)
Register link (used in all emails): https://govcongiants.com/mindy-launch
Goal: drive registrations for the live launch.

--------------------------------------------------------
THE 4 EMAILS — ORDER, TIMING & SUBJECT LINES
--------------------------------------------------------

EMAIL 1 — email-1-announcement.html
  Send:    Now / as soon as the list is ready
  Subject: The big contractors have armies. Now you have Mindy.
  Preview: Saturday July 25, 10AM ET — the full live launch of Mindy.

EMAIL 2 — email-2-hidden-market.html
  Send:    ~Wednesday, June 24
  Subject: You're seeing 28% of your market
  Preview: Drones hide 72% of their spend outside the obvious code.

EMAIL 3 — email-3-tomorrow.html
  Send:    Friday, June 26
  Subject: Tomorrow: you meet Mindy
  Preview: Last call to grab your free seat for the live launch.

EMAIL 4 — email-4-were-live.html
  Send:    Saturday, July 25 — early AM (a few hours before 10AM ET)
  Subject: We're live in a few hours — here's your link
  Preview: We go live today at 10AM ET. Register and your Zoom link lands instantly.

--------------------------------------------------------
HOW TO LOAD INTO GOHIGHLEVEL (IMPORTANT)
--------------------------------------------------------
1. In the GHL email builder, add a "Custom HTML" / "Code" element
   (NOT a normal text block — a text block will strip the layout).
2. Open the .html file in a text editor, copy ALL of it, paste into that element.
3. Set the Subject Line and Preview Text in GHL (see above) — these are
   NOT inside the HTML, they must be entered in GHL's send settings.

--------------------------------------------------------
MERGE FIELDS — MUST SWAP TO GHL SYNTAX
--------------------------------------------------------
The files use placeholder tokens. Find & replace before sending:

   {{FirstName}}          ->  {{contact.first_name}}
   {{UNSUBSCRIBE_LINK}}   ->  GHL unsubscribe link
                              (or remove the footer line if GHL auto-appends
                               an unsubscribe link in account settings)

--------------------------------------------------------
BEFORE YOU HIT SEND — QUICK CHECKLIST
--------------------------------------------------------
[ ] Subject line + preview text set in GHL
[ ] {{FirstName}} swapped to {{contact.first_name}}
[ ] Unsubscribe link working
[ ] Send a TEST to yourself; open on both Gmail AND Outlook
[ ] Click the purple button — confirm it goes to govcongiants.com/mindy-launch
[ ] Mobile preview looks right

Notes:
- Emails are 600px wide, table-based, tested for Gmail + Outlook.
- The CTA button uses VML so the gradient renders in Outlook desktop too.
- Header/footer gradients fall back to solid navy in Outlook (expected, looks fine).
