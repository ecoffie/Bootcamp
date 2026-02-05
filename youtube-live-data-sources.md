# YouTube Live Series - Data Sources Reference

Use this document to cite sources in all presentations. Always verify data is current before publishing.

---

## Federal Spending Data

| Source | URL | Data Available |
|--------|-----|----------------|
| USASpending.gov | https://usaspending.gov | Obligations, outlays, unobligated balances by agency |
| USASpending API | https://api.usaspending.gov | Programmatic access to spending data |
| Treasury Fiscal Data | https://fiscaldata.treasury.gov | Monthly Treasury Statement, debt data |
| FPDS-NG | https://fpds.gov | Federal contract awards, modifications |

---

## Legislation & Budget

| Source | URL | Data Available |
|--------|-----|----------------|
| Congress.gov | https://congress.gov | Bill text, NDAA, appropriations |
| Congressional Budget Office | https://cbo.gov | Cost estimates, budget projections |
| OMB | https://whitehouse.gov/omb | Budget requests, agency justifications |
| GovInfo | https://govinfo.gov | Public laws, CFR, Federal Register |

---

## Small Business Programs

| Source | URL | Data Available |
|--------|-----|----------------|
| SBA.gov | https://sba.gov | Small business goals (23%), certifications |
| SAM.gov | https://sam.gov | Entity registration, opportunities, exclusions |
| DSBS | https://dsbs.sba.gov | Dynamic Small Business Search |
| Certify.SBA.gov | https://certify.sba.gov | 8(a), WOSB, HUBZone certifications |
| SBIR.gov | https://sbir.gov | Small Business Innovation Research |

---

## Agency-Specific Data

| Source | URL | Data Available |
|--------|-----|----------------|
| Agency Strategic Plans | [Agency].gov/strategic-plan | Priorities, goals, pain points |
| Budget Justification | [Agency].gov/budget | Detailed spending plans |
| Agency Forecast | SAM.gov or agency sites | Upcoming opportunities |
| OSDBU Offices | [Agency].gov/osdbu | Small business liaison contacts |

---

## Contract Intelligence

| Source | URL | Data Available |
|--------|-----|----------------|
| FPDS-NG | https://fpds.gov | Historical contract awards |
| GovWin (Deltek) | https://govwin.com | Market intelligence (paid) |
| Bloomberg Government | https://bgov.com | Contract analysis (paid) |
| Federal Procurement Data | https://sam.gov/reports | Award summaries |

---

## Audit & Oversight

| Source | URL | Data Available |
|--------|-----|----------------|
| GAO | https://gao.gov | Audits, unobligated funds reports |
| Agency IG Reports | [Agency].gov/oig | Internal audit findings |
| CIGIE | https://ignet.gov | Inspector General community |

---

## Key Data Points to Verify Before Each Presentation

### For $82B Unobligated Balances (YouTube Live #1):
1. Go to: api.usaspending.gov/api/v2/agency/
2. Pull "unobligated_balance" for each agency
3. Verify NDAA authorization amounts at congress.gov

### For Small Business Goals (YouTube Live #2):
1. Verify 23% goal at sba.gov/federal-contracting
2. Check agency-specific goals in SBA Scorecard
3. Pull subcontracting data from FPDS

### For Capability Statements (YouTube Live #3):
1. Reference SAM.gov registration requirements
2. NAICS codes from census.gov/naics
3. Verify CAGE requirements at cage.dla.mil

---

## How to Cite in Slides

**Option 1: Sources Slide (Recommended)**
Add a "Data Sources" slide near the end listing all sources used.

**Option 2: Inline Citations**
Add small text at bottom of data-heavy slides:
"Source: USASpending.gov, January 2026"

**Option 3: Description Box**
Include sources in YouTube video description.

---

## Template Sources Slide Code

```html
<!-- Data Sources Slide -->
<div class="slide slide-dark">
    <div class="content" style="text-align: left; padding: 60px 100px;">
        <h2 style="text-align: center; margin-bottom: 50px; font-size: 60px;">Data Sources</h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; font-size: 26px;">
            <div>
                <h3 style="color: #4ade80; font-size: 32px; margin-bottom: 20px;">[Category 1]</h3>
                <ul style="list-style: none; line-height: 2;">
                    <li>> [Source 1]</li>
                    <li>> [Source 2]</li>
                    <li>> [Source 3]</li>
                </ul>
            </div>
            <div>
                <h3 style="color: #4ade80; font-size: 32px; margin-bottom: 20px;">[Category 2]</h3>
                <ul style="list-style: none; line-height: 2;">
                    <li>> [Source 1]</li>
                    <li>> [Source 2]</li>
                    <li>> [Source 3]</li>
                </ul>
            </div>
            <!-- Add more categories as needed -->
        </div>
        <p style="text-align: center; margin-top: 40px; font-size: 24px; opacity: 0.7;">Data current as of [Month Year]</p>
    </div>
</div>
```

---

## Update Schedule

- Verify spending data monthly (especially Q4: July-September)
- Check NDAA data annually (December signing)
- Review SBA goals annually (October new fiscal year)
- Update agency strategic plans every 4 years or when new published

---

*Last Updated: January 2026*
