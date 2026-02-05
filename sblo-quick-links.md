# SBLO & Prime Contractor Data Sources - Quick Links

## 🎯 Download These Files (30 Minutes)

### 1. SBA Prime Directory (300+ Primes)
**URL:** https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans  
**Format:** Excel  
**Last Updated:** March 4, 2025  
**Columns:** Prime Name, Location, PSC/NAICS, Contract #, SBLO Contact

---

### 2. DoD CSP Prime Directory (100+ DoD Primes)
**URL:** https://business.defense.gov/Portals/57/Documents/Dod%20CSP%20Prime%20Contractor%20Directory_May%202025.pdf  
**Format:** PDF/Excel  
**Last Updated:** May 2025  
**Includes:** SBLO names, phone numbers  
**Example:** BAE Systems: Marianne Tenore, SBLO, 703-xxx-xxxx

---

### 3. DHS Prime Contractors List (50+ Primes)
**URL:** https://www.dhs.gov/osdbu/prime-contractors  
**Format:** Web page  
**Last Updated:** March 17, 2025  
**Includes:** SBLO emails (often direct)  
**Example:** Accenture: smallbusiness@accenturefederal.com

---

### 4. SUBNet (SBA Subcontracting Network)
**URL:** https://www.sba.gov/federal-contracting/contracting-guide/prime-subcontracting/subcontracting-opportunities  
**Format:** Online database  
**Features:** Real-time postings, filter by state/NAICS  
**Requires:** Free SBA account

---

### 5. DOT Subcontracting Directory (100+ Primes)
**URL:** https://www.transportation.gov/osdbu/procurement-assistance/dot-subcontracting-directory  
**Format:** Directory  
**Includes:** SBLO names, phone numbers  
**FY:** 2025

---

## 📋 Quick Workflow

1. **Download** all 5 sources above (15 min)
2. **Extract** SBLO names, emails, phones (10 min)
3. **Fill gaps** by visiting company websites (5 min)
4. **Update** `sblo-list.csv` with new contacts
5. **Export** updated HTML list for distribution

---

## 📁 Files in This Project

- **sblo-list.html** - Interactive web version with search
- **sblo-list.csv** - Spreadsheet for easy editing
- **sblo-research-guide.md** - Detailed instructions
- **download-sblo-data.sh** - Automated download script (optional)

---

## 🔧 Using the Download Script

```bash
./download-sblo-data.sh
```

This will attempt to download available files to `sblo-data-downloads/` folder.

---

## 📝 Data Fields to Collect

For each contact, collect:
- Company/Agency Name
- SBLO Name
- Title
- Email
- Phone
- Website
- NAICS Codes
- Location
- Notes

---

## ✅ Checklist

- [ ] Download SBA Prime Directory Excel
- [ ] Download DoD CSP Prime Directory PDF
- [ ] Visit DHS Prime Contractors page
- [ ] Sign up for SUBNet (if needed)
- [ ] Download DOT Subcontracting Directory
- [ ] Extract contacts to CSV
- [ ] Verify emails on company websites
- [ ] Update sblo-list.csv
- [ ] Export to HTML for distribution

---

**Last Updated:** December 2025




