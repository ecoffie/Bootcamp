# 📥 Import Vercel Database to Mighty Networks

## 🎯 Goal: Import Your Contractor Database into Mighty Networks

You want to import your contractor database (currently on Vercel) into Mighty Networks as members, profiles, or directory entries.

**Current Database:**
- Location: Vercel deployment (`data-extract.js`)
- Records: ~3,502 contractors
- Data: Company names, SBLO contacts, emails, phones, NAICS codes, contract values, agencies

---

## 📋 Overview: Import Methods

Mighty Networks doesn't have a direct CSV bulk import feature for members, but there are several approaches:

### Option 1: Manual Member Invitation (For Small Lists)
- ✅ Best for: < 100 contractors
- ✅ Simple and straightforward
- ❌ Time-consuming for large lists

### Option 2: Zapier Integration (For Medium Lists)
- ✅ Best for: 100-1,000 contractors
- ✅ Automated workflow
- ✅ Can map custom fields
- ⚠️ Requires Zapier subscription

### Option 3: Mighty Networks API (For Large Lists)
- ✅ Best for: 1,000+ contractors
- ✅ Fully automated
- ✅ Direct integration
- ⚠️ Requires API access (may need Enterprise plan)
- ⚠️ Requires coding knowledge

### Option 4: Convert to Directory/Content Pages
- ✅ Best for: Reference database (not members)
- ✅ Import as posts/pages
- ✅ Searchable content
- ❌ Not actual member profiles

---

## 🚀 Method 1: Export Data from Vercel Database

First, let's extract your data from the Vercel database into a CSV format that Mighty Networks can use.

### Step 1: Create Export Script

Create a Python script to export your `data-extract.js` to CSV:

```python
# export-for-mighty-networks.py
import json
import csv
import re

# Read the data-extract.js file
with open('data-extract.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON array from the JavaScript file
# Look for: const companies = [...]
match = re.search(r'const companies = (\[.*?\]);', content, re.DOTALL)
if match:
    json_str = match.group(1)
    companies = json.loads(json_str)
else:
    print("❌ Could not extract companies array from data-extract.js")
    exit(1)

# Convert to CSV format suitable for Mighty Networks
output_file = 'contractors-for-mighty-networks.csv'

# Mighty Networks member import typically needs:
# - Email (required for invitations)
# - Name (display name)
# - Company (can be in profile fields)
# - Other custom fields

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
        'email',           # Required for member invitation
        'name',            # Display name (company name or SBLO name)
        'company',         # Company name
        'sblo_name',       # SBLO contact name
        'phone',           # Phone number
        'naics',           # NAICS codes
        'contract_count',  # Contract count
        'contract_value',  # Total contract value
        'agencies',        # Agencies worked with
        'has_subcontract_plan'  # Has subcontract plan
    ]
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    exported_count = 0
    
    for company in companies:
        # For Mighty Networks, we need at least an email or we can't invite
        # Option 1: Only export companies with emails
        if company.get('email') and company['email'].strip():
            writer.writerow({
                'email': company.get('email', '').strip(),
                'name': company.get('sblo_name', company.get('company', '')).strip(),
                'company': company.get('company', '').strip(),
                'sblo_name': company.get('sblo_name', '').strip(),
                'phone': company.get('phone', '').strip(),
                'naics': company.get('naics', '').strip(),
                'contract_count': company.get('contract_count', '').strip(),
                'contract_value': company.get('total_contract_value', '').strip(),
                'agencies': company.get('agencies', '').strip(),
                'has_subcontract_plan': company.get('has_subcontract_plan', '').strip()
            })
            exported_count += 1
        
        # Option 2: Export all companies (you'll need to add emails later)
        # Uncomment this section if you want to export all companies
        # writer.writerow({
        #     'email': company.get('email', '') or f"contact@{company.get('company', 'example').lower().replace(' ', '').replace('.', '').replace(',', '')}.com",
        #     'name': company.get('sblo_name', company.get('company', '')),
        #     'company': company.get('company', ''),
        #     'sblo_name': company.get('sblo_name', ''),
        #     'phone': company.get('phone', ''),
        #     'naics': company.get('naics', ''),
        #     'contract_count': company.get('contract_count', ''),
        #     'contract_value': company.get('total_contract_value', ''),
        #     'agencies': company.get('agencies', ''),
        #     'has_subcontract_plan': company.get('has_subcontract_plan', '')
        # })
    
    print(f"✅ Exported {exported_count} companies with emails to {output_file}")
    print(f"📊 Total companies in database: {len(companies)}")
    if exported_count < len(companies):
        print(f"⚠️  {len(companies) - exported_count} companies skipped (no email address)")
```

### Step 2: Run the Export Script

```bash
cd /Users/ericcoffie/Bootcamp/contractor-database-embed
python3 export-for-mighty-networks.py
```

This creates: `contractors-for-mighty-networks.csv`

---

## 🔧 Method 2: Manual Member Invitation (Small Lists)

If you have fewer than 100 contractors with email addresses:

### Step 1: Prepare Your CSV

Your CSV should have at minimum:
- `email` (required)
- `name` (display name)

### Step 2: Use Mighty Networks Bulk Invite

1. **Log into Mighty Networks Admin Panel**
2. **Navigate to:** Members → Invite Members
3. **Click:** "Bulk Invite" or "Invite Multiple Members"
4. **Upload CSV:** Select your `contractors-for-mighty-networks.csv`
5. **Map Fields:**
   - Email → Email Address
   - Name → Display Name
6. **Send Invitations:** Members will receive email invitations

### Step 3: Custom Profile Fields (After Import)

After members accept invitations, you can add custom profile fields:
1. **Settings → Member Profiles → Custom Fields**
2. Add fields:
   - Company Name
   - Phone Number
   - NAICS Codes
   - Contract Value
   - Agencies
   - Has Subcontract Plan

**Note:** Members will need to manually fill these fields unless you use the API (see Method 4).

---

## ⚙️ Method 3: Zapier Integration (Medium Lists)

Zapier can automate member invitations from CSV or Google Sheets.

### Step 1: Upload CSV to Google Sheets

1. Create a new Google Sheet
2. Import `contractors-for-mighty-networks.csv`
3. Share sheet (make it accessible if needed)

### Step 2: Set Up Zapier Zap

**Trigger:** Google Sheets → New Spreadsheet Row
**Action:** Mighty Networks → Invite Member

1. **Connect Accounts:**
   - Connect Google Sheets
   - Connect Mighty Networks (requires API access)

2. **Configure Trigger:**
   - Select your Google Sheet
   - Select the worksheet
   - Choose "New Spreadsheet Row"

3. **Configure Action:**
   - Select "Invite Member"
   - Map fields:
     - Email → `email` column
     - Name → `name` column
     - Custom fields (if supported)

4. **Test & Activate**

### Step 3: Run the Zap

- Zapier will automatically invite members when new rows are added
- For existing data, you may need to trigger it manually or add a helper column

**Limitations:**
- Zapier free plan: 5 Zaps, 100 tasks/month
- Paid plans needed for larger imports
- Mighty Networks API access required

---

## 💻 Method 4: Mighty Networks API (Large Lists)

For full automation and control, use the Mighty Networks API.

### Prerequisites

1. **API Access:** Contact Mighty Networks support for API credentials
   - May require Enterprise plan
   - Request API documentation

2. **API Endpoints Needed:**
   - `POST /members` - Create/invite members
   - `PATCH /members/{id}` - Update member profiles
   - `POST /members/{id}/profile_fields` - Add custom fields

### Step 1: Create API Import Script

```python
# import-to-mighty-networks-api.py
import csv
import requests
import json
import time

# Mighty Networks API Configuration
API_BASE_URL = "https://api.mightynetworks.com/api/v1"
API_KEY = "YOUR_API_KEY_HERE"  # Get from Mighty Networks support

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def invite_member(email, name, company_data):
    """Invite a member to Mighty Networks"""
    
    # Endpoint to invite/create member
    url = f"{API_BASE_URL}/members"
    
    payload = {
        "email": email,
        "name": name,
        # Add custom profile fields if supported
        "profile_fields": {
            "company": company_data.get('company', ''),
            "phone": company_data.get('phone', ''),
            "naics": company_data.get('naics', ''),
            "contract_count": company_data.get('contract_count', ''),
            "contract_value": company_data.get('contract_value', ''),
            "agencies": company_data.get('agencies', ''),
            "has_subcontract_plan": company_data.get('has_subcontract_plan', '')
        }
    }
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Error inviting {email}: {e}")
        return None

# Read CSV
csv_file = 'contractors-for-mighty-networks.csv'

invited_count = 0
error_count = 0

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        email = row.get('email', '').strip()
        name = row.get('name', '').strip()
        
        if not email:
            print(f"⚠️  Skipping row - no email: {row.get('company', 'Unknown')}")
            continue
        
        print(f"📧 Inviting {email} ({name})...")
        
        result = invite_member(email, name, row)
        
        if result:
            invited_count += 1
            print(f"✅ Successfully invited {email}")
        else:
            error_count += 1
            print(f"❌ Failed to invite {email}")
        
        # Rate limiting - be respectful of API limits
        time.sleep(0.5)  # 2 requests per second

print(f"\n📊 Summary:")
print(f"✅ Successfully invited: {invited_count}")
print(f"❌ Errors: {error_count}")
```

### Step 2: Get API Credentials

1. **Contact Mighty Networks Support:**
   - Email: support@mightynetworks.com
   - Request: API access and documentation
   - Specify: You want to bulk import members

2. **API Documentation:**
   - Request API endpoints documentation
   - Get authentication method
   - Understand rate limits

### Step 3: Run the Import

```bash
# Update API_KEY in the script first!
python3 import-to-mighty-networks-api.py
```

---

## 📄 Method 5: Convert to Directory/Content (Reference Database)

If you want the database as searchable content rather than member profiles:

### Option A: Import as Posts/Pages

1. **Convert CSV to individual posts:**
   - Each contractor = one post/page
   - Include all information in post content
   - Use tags/categories for filtering (NAICS, agencies, etc.)

2. **Use Zapier:**
   - Trigger: Google Sheets row
   - Action: Mighty Networks → Create Post

### Option B: Embed Your Vercel Database

You're already doing this! Your Vercel database can be embedded in Mighty Networks:

1. **In Mighty Networks:**
   - Create a new page
   - Add HTML block
   - Paste your embed code from `YOUR_EMBED_CODE.md`

2. **Keep it on Vercel:**
   - Database stays on Vercel
   - Embedded in Mighty Networks page
   - No import needed!

---

## 🎯 Recommended Approach Based on Your Needs

### Scenario 1: Want Members to Have Profiles
**Use:** Method 4 (API) if you have API access, or Method 3 (Zapier) for automation

### Scenario 2: Want Searchable Directory
**Use:** Method 5 (Keep on Vercel + Embed) - You're already doing this!

### Scenario 3: Want Both
**Use:** 
- Keep Vercel database embedded (reference/search)
- Import key contacts as members (for networking)

---

## 📊 Data Preparation Checklist

Before importing, ensure your CSV has:

- [ ] Email addresses (required for member invitations)
- [ ] Names (display names)
- [ ] Company names
- [ ] Phone numbers (optional, can add later)
- [ ] Other custom fields mapped

**For companies without emails:**
- Option 1: Skip them (reference database only)
- Option 2: Enrich with Apollo first (see `APOLLO_SETUP_INSTRUCTIONS.md`)
- Option 3: Use company domain emails (e.g., contact@company.com)

---

## 🔍 Finding Mighty Networks Import Options

### Check Your Admin Panel

1. **Log into Mighty Networks**
2. **Navigate to:** Settings → Members → Invite Members
3. **Look for:**
   - "Bulk Invite" button
   - "Import CSV" option
   - "Invite Multiple" link

### Contact Support

If you don't see bulk import options:
1. **Email:** support@mightynetworks.com
2. **Ask:**
   - "Do you have CSV bulk member import?"
   - "What's the best way to import 3,500+ members?"
   - "Do you have API access for member imports?"
   - "Can I use Zapier to import members from CSV?"

---

## 🚨 Important Notes

### Rate Limits
- Mighty Networks may have rate limits on invitations
- Don't send thousands of invites at once
- Space out invitations (use delays in scripts)

### Email Deliverability
- Ensure emails are valid (verify before importing)
- Use double opt-in if possible
- Follow email marketing best practices

### Member Experience
- Send welcome message explaining why they're invited
- Set expectations (directory, networking, etc.)
- Provide value proposition

### Privacy & Compliance
- Ensure you have permission to contact these emails
- Follow GDPR/CCPA if applicable
- Include unsubscribe options

---

## 📝 Next Steps

1. **Decide on import method** based on your needs
2. **Export data** using the export script (if needed)
3. **Test with small sample** (10-20 records) first
4. **Scale up** once confirmed working
5. **Monitor results** and adjust as needed

---

## 🆘 Need Help?

**Common Issues:**

1. **"No bulk import option"**
   - Contact Mighty Networks support
   - Consider Zapier integration
   - Use API if available

2. **"API not available"**
   - Request API access from support
   - May require Enterprise plan
   - Alternative: Use Zapier

3. **"Too many members to invite"**
   - Use API with rate limiting
   - Space out invitations over days/weeks
   - Contact support for bulk import assistance

4. **"Companies don't have emails"**
   - Use Apollo enrichment (see `APOLLO_SETUP_INSTRUCTIONS.md`)
   - Skip companies without emails (reference only)
   - Use domain-based emails as placeholder

---

## ✅ Quick Start (Recommended)

**For your 3,500+ contractor database:**

1. **Keep Vercel database embedded** (you're already doing this - great!)
2. **Export companies WITH emails** using export script
3. **Contact Mighty Networks support** about bulk import options
4. **Use Zapier** if API not available (for companies with emails)
5. **Import key contacts** as members (SBLOs, decision-makers)

**Result:** 
- Searchable database embedded (all 3,500 contractors)
- Key contacts as members (networking/engagement)
- Best of both worlds!

---

**Ready to export your data? Run the export script and let's get started!** 🚀










