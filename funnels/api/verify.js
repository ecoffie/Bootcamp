// Vercel Serverless Function - Lead Verification API
// Checks if an email exists in GoHighLevel CRM

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { email } = req.body;

    if (!email) {
      return res.status(400).json({ error: 'Email is required' });
    }

    const cleanEmail = email.toLowerCase().trim();
    const apiKey = process.env.GHL_API_KEY;
    const locationId = process.env.GHL_LOCATION_ID;

    if (!apiKey || !locationId) {
      console.log('GHL not configured');
      return res.status(500).json({ error: 'Verification service not configured' });
    }

    // Search for contact by email in GHL
    const searchUrl = `https://rest.gohighlevel.com/v1/contacts/lookup?email=${encodeURIComponent(cleanEmail)}`;

    const ghlResponse = await fetch(searchUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
    });

    if (!ghlResponse.ok) {
      const errorData = await ghlResponse.json();
      console.error('GHL lookup error:', errorData);

      // If 404, contact doesn't exist
      if (ghlResponse.status === 404) {
        return res.status(200).json({
          verified: false,
          message: 'Email not found'
        });
      }

      return res.status(500).json({ error: 'Verification failed' });
    }

    const ghlResult = await ghlResponse.json();

    // Check if contact exists
    if (ghlResult.contacts && ghlResult.contacts.length > 0) {
      const contact = ghlResult.contacts[0];
      return res.status(200).json({
        verified: true,
        firstName: contact.firstName || '',
        message: 'Email verified'
      });
    }

    return res.status(200).json({
      verified: false,
      message: 'Email not found'
    });

  } catch (error) {
    console.error('Verification error:', error);
    return res.status(500).json({
      error: 'Verification failed',
      message: error.message
    });
  }
}
