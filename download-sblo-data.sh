#!/bin/bash

# SBLO Data Download Script
# Downloads public prime contractor directories for SBLO list building

echo "SBLO Data Download Script"
echo "========================="
echo ""

# Create downloads directory
mkdir -p sblo-data-downloads
cd sblo-data-downloads

echo "Downloading SBA Prime Directory..."
# Note: Update this URL if it changes
curl -L -o "sba-prime-directory.xlsx" "https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans" 2>/dev/null || echo "⚠️  Manual download required: https://www.sba.gov/document/support-directory-federal-government-prime-contractors-subcontracting-plans"

echo "Downloading DoD CSP Prime Directory..."
curl -L -o "dod-csp-prime-directory.pdf" "https://business.defense.gov/Portals/57/Documents/Dod%20CSP%20Prime%20Contractor%20Directory_May%202025.pdf" 2>/dev/null || echo "⚠️  Manual download required: https://business.defense.gov/Portals/57/Documents/Dod%20CSP%20Prime%20Contractor%20Directory_May%202025.pdf"

echo ""
echo "✅ Downloads complete!"
echo ""
echo "Manual downloads needed:"
echo "  1. DHS Prime Contractors: https://www.dhs.gov/osdbu/prime-contractors"
echo "  2. DOT Subcontracting Directory: https://www.transportation.gov/osdbu/procurement-assistance/dot-subcontracting-directory"
echo "  3. SUBNet: https://www.sba.gov/federal-contracting/contracting-guide/prime-subcontracting/subcontracting-opportunities"
echo ""
echo "Files saved to: sblo-data-downloads/"




