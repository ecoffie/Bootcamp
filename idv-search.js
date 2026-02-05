/**
 * IDV Contract Search Module
 * GovCon Giants - USASpending.gov API Integration
 *
 * Usage:
 *   const idvSearch = require('./idv-search');
 *   const results = await idvSearch.searchIDVContracts({ naicsCode: '23', state: 'ME' });
 */

const https = require('https');

const API_URL = 'https://api.usaspending.gov/api/v2/search/spending_by_award/';

// IDV Award Type Codes
const IDV_CODES = ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"];
// Task Order Award Type Codes
const TASK_ORDER_CODES = ["A", "B", "C", "D"];

/**
 * Search for IDV contracts or task orders
 * @param {Object} options - Search options
 * @param {string} [options.naicsCode] - NAICS code (2, 4, or 6 digits)
 * @param {string} [options.agency] - Awarding agency name
 * @param {number} [options.minValue=0] - Minimum award value
 * @param {string} [options.dateFrom] - Start date (YYYY-MM-DD)
 * @param {string} [options.dateTo] - End date (YYYY-MM-DD)
 * @param {string} [options.state] - State code (e.g., 'ME', 'VA')
 * @param {string} [options.stateFilterType='recipient'] - 'recipient' for contractor HQ, 'pop' for place of performance
 * @param {number} [options.limit=50] - Results per page
 * @param {number} [options.page=1] - Page number
 * @returns {Promise<Object>} - Search results
 */
async function searchIDVContracts(options = {}) {
    const {
        naicsCode,
        agency,
        minValue = 0,
        dateFrom,
        dateTo,
        state,
        stateFilterType = 'recipient',
        limit = 50,
        page = 1
    } = options;

    // Determine if searching IDVs or task orders based on state filter type
    const isTaskOrderSearch = state && stateFilterType === 'pop';

    const requestBody = {
        filters: {
            award_type_codes: isTaskOrderSearch ? TASK_ORDER_CODES : IDV_CODES,
            award_amounts: [{
                lower_bound: minValue
            }]
        },
        fields: [
            "Award ID",
            "Recipient Name",
            "Recipient UEI",
            "Award Amount",
            "Total Outlays",
            "Description",
            "Start Date",
            "End Date",
            "Awarding Agency",
            "Awarding Sub Agency",
            "NAICS Code",
            "NAICS Description",
            "Contract Award Type",
            "Recipient State Code",
            "Place of Performance State Code",
            "generated_unique_award_id"
        ],
        page: page,
        limit: limit,
        sort: "Award Amount",
        order: "desc",
        subawards: false
    };

    // Add time period filter if dates provided
    if (dateFrom || dateTo) {
        const effectiveStartDate = dateFrom || '2000-01-01';
        const effectiveEndDate = dateTo || new Date().toISOString().split('T')[0];
        requestBody.filters.time_period = [{
            start_date: effectiveStartDate,
            end_date: effectiveEndDate
        }];
    }

    // Add NAICS filter if provided
    if (naicsCode) {
        let cleanNaics = naicsCode.replace(/0+$/, '') || naicsCode;
        if (cleanNaics.length === 1) cleanNaics = cleanNaics + '0';
        else if (cleanNaics.length === 3) cleanNaics = cleanNaics.substring(0, 2);
        else if (cleanNaics.length === 5) cleanNaics = cleanNaics + '0';
        requestBody.filters.naics_codes = { require: [cleanNaics] };
    }

    // Add agency filter if provided
    if (agency) {
        requestBody.filters.agencies = [{
            type: "awarding",
            tier: "toptier",
            name: agency
        }];
    }

    // Add state filter if provided
    if (state) {
        if (stateFilterType === 'pop') {
            requestBody.filters.place_of_performance_locations = [{
                country: "USA",
                state: state
            }];
        } else {
            requestBody.filters.recipient_locations = [{
                country: "USA",
                state: state
            }];
        }
    }

    // Make API request
    const response = await makeRequest(API_URL, requestBody);

    // Process results
    const contracts = (response.results || []).map(c => ({
        awardId: c['Award ID'],
        recipientName: c['Recipient Name'],
        recipientUei: c['Recipient UEI'],
        awardAmount: parseFloat(c['Award Amount']) || 0,
        description: c['Description'],
        startDate: c['Start Date'],
        endDate: c['End Date'],
        agency: c['Awarding Agency'],
        subAgency: c['Awarding Sub Agency'],
        naicsCode: c['NAICS Code'],
        naicsDescription: c['NAICS Description'],
        recipientState: c['Recipient State Code'],
        popState: c['Place of Performance State Code'],
        generatedId: c['generated_unique_award_id'],
        usaSpendingUrl: c['generated_unique_award_id']
            ? `https://www.usaspending.gov/award/${c['generated_unique_award_id']}`
            : `https://www.usaspending.gov/keyword_search/${encodeURIComponent(c['Award ID'])}`
    }));

    return {
        contracts,
        totalCount: contracts.length,
        page: page,
        hasNextPage: response.page_metadata?.hasNext || false,
        searchType: isTaskOrderSearch ? 'task_orders' : 'idv_contracts'
    };
}

/**
 * Search for IDV contracts by contractor state (headquarters location)
 */
async function searchByContractorState(state, options = {}) {
    return searchIDVContracts({
        ...options,
        state,
        stateFilterType: 'recipient'
    });
}

/**
 * Search for task orders by place of performance (work location)
 */
async function searchByWorkLocation(state, options = {}) {
    return searchIDVContracts({
        ...options,
        state,
        stateFilterType: 'pop'
    });
}

/**
 * Get list of available agencies
 */
function getAgencies() {
    return [
        "Department of Defense",
        "Department of Health and Human Services",
        "Department of Homeland Security",
        "Department of Veterans Affairs",
        "General Services Administration",
        "National Aeronautics and Space Administration",
        "Department of the Interior",
        "Department of Transportation",
        "Department of Energy",
        "Department of Justice",
        "Department of the Treasury",
        "Department of State"
    ];
}

/**
 * Get list of US state codes
 */
function getStateCodes() {
    return [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL",
        "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME",
        "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH",
        "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
        "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
    ];
}

// Helper function to make HTTPS POST request
function makeRequest(url, body) {
    return new Promise((resolve, reject) => {
        const urlObj = new URL(url);
        const postData = JSON.stringify(body);

        const options = {
            hostname: urlObj.hostname,
            port: 443,
            path: urlObj.pathname,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        };

        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(new Error(`Failed to parse response: ${e.message}`));
                }
            });
        });

        req.on('error', reject);
        req.write(postData);
        req.end();
    });
}

module.exports = {
    searchIDVContracts,
    searchByContractorState,
    searchByWorkLocation,
    getAgencies,
    getStateCodes
};
