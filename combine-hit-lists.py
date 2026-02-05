#!/usr/bin/env python3
"""
Combine the beginner-friendly list (10 opportunities) with the full low-competition list (34 opportunities)
into one unified document
"""

import re

# Read both files
with open('december-hit-list-beginner.html', 'r', encoding='utf-8') as f:
    beginner_html = f.read()

with open('december-hit-list.html', 'r', encoding='utf-8') as f:
    full_html = f.read()

# Extract CSS from full list (more complete styling)
css_match = re.search(r'(<style>.*?</style>)', full_html, re.DOTALL)
css = css_match.group(1) if css_match else ""

# Extract beginner opportunities section (keep as-is, numbered 1-10)
beginner_start = beginner_html.find('<div class="hit-list">')
beginner_end = beginner_html.find('</div>\n        </div>\n\n        <div class="key-point">')
if beginner_end == -1:
    beginner_end = beginner_html.find('</div>\n        </div>', beginner_start + 100)
beginner_opps = beginner_html[beginner_start:beginner_end] if beginner_start > 0 and beginner_end > 0 else ""

# Extract full list opportunities section
full_start = full_html.find('<div class="hit-list">')
full_end = full_html.find('</div>\n        </div>\n\n        <div class="key-point">')
if full_end == -1:
    full_end = full_html.find('</div>\n        </div>', full_start + 100)
full_opps_html = full_html[full_start:full_end] if full_start > 0 and full_end > 0 else ""

# Extract individual opportunity cards from full list
full_opp_cards = re.findall(r'(<!-- Opportunity \d+ -->.*?</div>\s*</div>\s*)', full_opps_html, re.DOTALL)

# Renumber full list opportunities to start at 11
renumbered_full_opps = []
for i, card in enumerate(full_opp_cards, start=11):
    # Replace opportunity number in comment
    card = re.sub(r'<!-- Opportunity \d+ -->', f'<!-- Opportunity {i} -->', card, count=1)
    # Replace opportunity number in div (if it exists) - but full list doesn't have opportunity-number divs
    # Just update the comment
    renumbered_full_opps.append(card)

# Combine the opportunities - append full list to beginner list
# Remove the closing tags from beginner_opps and add full list before closing
beginner_opps_clean = beginner_opps.rstrip()
if beginner_opps_clean.endswith('</div>'):
    beginner_opps_clean = beginner_opps_clean[:-6].rstrip()
if beginner_opps_clean.endswith('</div>'):
    beginner_opps_clean = beginner_opps_clean[:-6].rstrip()

combined_opps = beginner_opps_clean + '\n' + '\n'.join(renumbered_full_opps) + '\n        </div>\n        </div>'

# Extract intro sections
beginner_intro_match = re.search(r'(<div class="intro">.*?</div>)', beginner_html, re.DOTALL)
beginner_intro = beginner_intro_match.group(1) if beginner_intro_match else ""

full_intro_match = re.search(r'(<div class="intro">.*?</div>)', full_html, re.DOTALL)
full_intro = full_intro_match.group(1) if full_intro_match else ""

# Extract key points
beginner_key_match = re.search(r'(<div class="key-point">.*?</div>)', beginner_html, re.DOTALL)
beginner_key = beginner_key_match.group(1) if beginner_key_match else ""

full_key_match = re.search(r'(<div class="key-point">.*?</div>)', full_html, re.DOTALL)
full_key = full_key_match.group(1) if full_key_match else ""

# Create combined HTML
combined_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>December 2025 Hit List - Complete Edition</title>
    {css}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 December 2025 Hit List</h1>
            <p class="subtitle">44 Low-Competition Contracts: 10 Beginner-Friendly + 34 Full List</p>
            <p style="font-size: 1rem; margin-top: 10px; opacity: 0.9;">Perfect for All Experience Levels</p>
            <span class="badge">$138B+ in Unobligated Funds | Use It or Lose It</span>
        </div>

        <div class="intro">
            <h2>Two Lists in One Document</h2>
            <p><strong>📚 Part 1: Top 10 Beginner-Friendly Opportunities</strong> - Perfect for first-time government contractors. Easy to understand, clear action steps, and active primes seeking partners.</p>
            <p><strong>🚀 Part 2: Full 34 Low-Competition Opportunities</strong> - Complete list of December opportunities with detailed information, SBLO contacts, and strategic insights.</p>
            <p><strong>December is "use it or lose it" month.</strong> Agencies have $138B+ in unobligated balances that MUST be spent before FY2025 closes.</p>
            <p><strong>Low competition = Higher win rates.</strong> These opportunities are specifically selected for small businesses with set-asides and limited competition.</p>
        </div>

        <div style="background: #fef3c7; padding: 20px; border-radius: 12px; margin-bottom: 30px; border-left: 5px solid #f59e0b;">
            <h2 style="color: #92400e; margin-bottom: 15px; font-size: 1.5rem;">📚 Part 1: Top 10 Beginner-Friendly Opportunities</h2>
            <p style="color: #78350f; margin-bottom: 10px;"><strong>Start here if you're new to government contracting!</strong></p>
            <p style="color: #78350f;">These 10 opportunities are specifically selected for beginners - easy requirements, clear scopes, and multiple ways to win (direct contracts + subcontracting).</p>
        </div>

        {combined_opps}

        <div class="key-point">
            <p><strong>💡 Beginner Success Tips (Part 1):</strong></p>
            <p>1. <strong>Start with subcontracting</strong> - Work with primes first to learn the system</p>
            <p>2. <strong>Focus on your certifications</strong> - 8(a), SDVOSB, HUBZone, WOSB open doors</p>
            <p>3. <strong>Contact SBLOs directly</strong> - They want to help beginners get started</p>
            <p>4. <strong>Don't wait for perfect</strong> - Apply even if you're 80% qualified</p>
            <p>5. <strong>December is your friend</strong> - Agencies move faster when they need to spend money</p>
        </div>

        <div class="key-point" style="margin-top: 30px;">
            <p><strong>💡 Pro Tips for All Opportunities (Part 2):</strong></p>
            <p>These opportunities are specifically selected for low competition. Focus on the ones matching your NAICS codes and certifications (8(a), SDVOSB, HUBZone, WOSB). Contact the SBLOs listed immediately - December moves FAST.</p>
        </div>

        <div class="footer">
            <p><strong>December 2025 Hit List - Complete Edition</strong> | GovCon Giants Bootcamp</p>
            <p>Based on FY2026 NDAA (S.2296) and $138B+ in unobligated balances</p>
            <p>Total: 44 Low-Competition Opportunities (10 Beginner-Friendly + 34 Full List)</p>
            <p>For database: <a href="https://guides.govcongiants.org/database">guides.govcongiants.org/database</a></p>
            <p style="margin-top: 15px; font-size: 0.85rem; color: #718096;">Screenshot and share this list! 📸</p>
        </div>
    </div>
</body>
</html>
"""

# Write combined file
output_path = 'december-hit-list-complete.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(combined_html)

print(f"✅ Combined hit list created!")
print(f"📄 Output file: {output_path}")
print(f"📊 Total opportunities: 44 (10 beginner + 34 full list)")

