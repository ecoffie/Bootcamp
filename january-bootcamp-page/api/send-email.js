const nodemailer = require('nodemailer');

// CORS headers for browser requests
const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
};

module.exports = async function handler(req, res) {
    // Handle CORS preflight
    if (req.method === 'OPTIONS') {
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
        return res.status(200).end();
    }

    if (req.method !== 'POST') {
        return res.status(405).json({ error: 'Method not allowed' });
    }

    try {
        const { to_email, user_name, company_name, worksheet_content } = req.body;

        if (!to_email || !worksheet_content) {
            return res.status(400).json({ error: 'Missing required fields: to_email and worksheet_content' });
        }

        // Create transporter using Gmail SMTP
        const transporter = nodemailer.createTransport({
            host: 'smtp.gmail.com',
            port: 587,
            secure: false,
            auth: {
                user: process.env.SMTP_USER,
                pass: process.env.SMTP_PASSWORD,
            },
        });

        // Convert plain text content to HTML with proper formatting
        const formatContentToHtml = (content) => {
            // Escape HTML entities
            let html = content.replace(/</g, '&lt;').replace(/>/g, '&gt;');
            // Convert newlines to <br> tags
            html = html.replace(/\n/g, '<br>\n');
            return html;
        };

        // Email content
        const mailOptions = {
            from: `"GovCon Giants Bootcamp" <${process.env.SMTP_USER}>`,
            to: to_email,
            subject: `Your Execution Sheet - ${user_name || 'Attendee'} - January 2026 Bootcamp`,
            text: `Hi ${user_name || 'there'},

Here's your completed One-Page Execution Sheet from the January 2026 GovCon Bootcamp.

${worksheet_content}

---
GovCon Giants | shop.govcongiants.org`,
            html: `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, Helvetica, sans-serif; line-height: 1.6; color: #333333; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="max-width: 600px; width: 100%;">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #16a34a, #15803d); padding: 30px 20px; text-align: center; border-radius: 8px 8px 0 0;">
                            <h1 style="margin: 0; color: white; font-size: 28px; font-weight: bold;">
                                GovCon <span style="color: #bbf7d0;">Giants</span>
                            </h1>
                            <p style="margin: 10px 0 0 0; color: #bbf7d0; font-size: 16px;">January 2026 Bootcamp</p>
                        </td>
                    </tr>

                    <!-- Greeting -->
                    <tr>
                        <td style="background-color: #ffffff; padding: 30px 30px 20px 30px;">
                            <p style="margin: 0 0 15px 0; font-size: 18px;">
                                Hi <strong>${user_name || 'there'}</strong>${company_name ? ` from <strong>${company_name}</strong>` : ''},
                            </p>
                            <p style="margin: 0; color: #555555;">
                                Here's your completed <strong>One-Page Execution Sheet</strong> from the bootcamp. Keep this as your reference and accountability document!
                            </p>
                        </td>
                    </tr>

                    <!-- Worksheet Content -->
                    <tr>
                        <td style="background-color: #ffffff; padding: 0 30px 30px 30px;">
                            <div style="background-color: #f8fafc; border: 2px solid #e2e8f0; border-radius: 8px; padding: 25px; font-family: 'Courier New', Courier, monospace; font-size: 13px; line-height: 1.8; color: #334155;">
                                ${formatContentToHtml(worksheet_content)}
                            </div>
                        </td>
                    </tr>

                    <!-- Call to Action -->
                    <tr>
                        <td style="background-color: #ffffff; padding: 0 30px 30px 30px;">
                            <div style="background-color: #f0fdf4; border-left: 4px solid #22c55e; padding: 15px 20px; border-radius: 0 8px 8px 0;">
                                <p style="margin: 0; font-weight: bold; color: #166534;">
                                    Remember: One agency. One opportunity. One action. Repeat daily.
                                </p>
                            </div>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #1e293b; padding: 25px 30px; text-align: center; border-radius: 0 0 8px 8px;">
                            <p style="margin: 0 0 10px 0; color: #94a3b8; font-size: 14px;">
                                <a href="https://shop.govcongiants.org" style="color: #22c55e; text-decoration: none; font-weight: bold;">GovCon Giants</a> |
                                <a href="https://shop.govcongiants.org" style="color: #94a3b8; text-decoration: none;">shop.govcongiants.org</a>
                            </p>
                            <p style="margin: 0; color: #64748b; font-size: 12px;">
                                You received this email because you completed the Execution Sheet at the January 2026 Bootcamp.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
            `,
        };

        // Send email
        const info = await transporter.sendMail(mailOptions);
        console.log('Email sent:', info.messageId);

        res.setHeader('Access-Control-Allow-Origin', '*');
        return res.status(200).json({
            success: true,
            message: 'Email sent successfully',
            messageId: info.messageId
        });

    } catch (error) {
        console.error('Email error:', error);
        res.setHeader('Access-Control-Allow-Origin', '*');
        return res.status(500).json({
            error: 'Failed to send email',
            details: error.message
        });
    }
};
