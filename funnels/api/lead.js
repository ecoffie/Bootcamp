// Vercel Serverless Function - Lead Capture API
// Captures leads from funnels, sends confirmation email, and sends to GoHighLevel
// Updated: Jan 22 2026 - Dark theme email design with resource lists

import nodemailer from 'nodemailer';

// Email templates for each funnel - Dark theme with green accents
const emailTemplates = {
  'january-bootcamp': {
    subject: 'Your Free January Bootcamp Resources',
    getHtml: (firstName) => `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: system-ui, -apple-system, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
    <!-- Header -->
    <div style="text-align: center; margin-bottom: 32px;">
      <span style="font-size: 24px; font-weight: bold; color: white;">GovCon</span>
      <span style="font-size: 24px; font-weight: bold; color: #22c55e;">Giants</span>
    </div>

    <!-- Main Content -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 32px; margin-bottom: 24px;">
      <h1 style="color: white; font-size: 24px; margin: 0 0 16px 0; text-align: center;">
        Hi ${firstName}, Your Resources Are Ready!
      </h1>

      <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0; text-align: center;">
        Click below to access your free January Bootcamp resources.
      </p>

      <!-- Resource List -->
      <div style="background-color: #0f172a; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">What you'll get:</p>
        <ul style="color: #22c55e; margin: 0; padding-left: 20px;">
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">January Agency Buyers List</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">January Hit List (34 NDAA-Based Contracts)</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">FY2026 NDAA Report</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Agency Pain Points Guide</span></li>
          <li style="margin-bottom: 0;"><span style="color: #e2e8f0;">And more!</span></li>
        </ul>
      </div>

      <!-- CTA Button -->
      <div style="text-align: center; margin-bottom: 24px;">
        <a href="https://guides.govcongiants.org/january-bootcamp/3-thank-you.html" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 16px 32px; border-radius: 8px; font-weight: bold; font-size: 16px;">
          Access Your Resources
        </a>
      </div>

      <!-- Event Reminder -->
      <div style="background-color: #0f172a; border-radius: 8px; padding: 16px; text-align: center; border: 1px solid #334155;">
        <p style="color: #22c55e; font-size: 12px; font-weight: 600; margin: 0 0 4px 0;">MARK YOUR CALENDAR</p>
        <p style="color: white; font-weight: bold; margin: 0;">January 31, 2026 • 9AM - 5PM ET</p>
      </div>
    </div>

    <!-- Need Help Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center;">
      <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">Need Help or Have Questions?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Our team is here to help you succeed in government contracting.</p>
      <div style="margin-bottom: 12px;">
        <span style="color: #22c55e; font-size: 14px;">Call or Text:</span>
        <a href="tel:7864770477" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">786-477-0477</a>
      </div>
      <div>
        <span style="color: #22c55e; font-size: 14px;">Email:</span>
        <a href="mailto:hello@govconedu.com" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">hello@govconedu.com</a>
      </div>
    </div>

    <!-- Ready to Get Started Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center; border: 1px solid #22c55e;">
      <p style="color: #22c55e; font-weight: 600; margin: 0 0 8px 0;">Ready to Get Started?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Join our programs and start winning federal contracts today.</p>
      <div style="margin-bottom: 12px;">
        <a href="https://federalhelpcenter.com/starter" style="display: inline-block; background-color: #3b82f6; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Starter - $27/mo</a>
      </div>
      <div>
        <a href="https://federalhelpcenter.com/pro" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Pro - $99/mo</a>
      </div>
    </div>

    <!-- Footer -->
    <div style="text-align: center; color: #64748b; font-size: 12px;">
      <p style="margin: 0 0 8px 0;">Didn't request this? You can safely ignore this email.</p>
      <p style="margin: 0;">© 2026 GovCon Giants. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
    `
  },

  'surge-bootcamp': {
    subject: 'Your Free Surge Bootcamp Resources',
    getHtml: (firstName) => `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: system-ui, -apple-system, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
    <!-- Header -->
    <div style="text-align: center; margin-bottom: 32px;">
      <span style="font-size: 24px; font-weight: bold; color: white;">GovCon</span>
      <span style="font-size: 24px; font-weight: bold; color: #22c55e;">Giants</span>
    </div>

    <!-- Main Content -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 32px; margin-bottom: 24px;">
      <h1 style="color: white; font-size: 24px; margin: 0 0 16px 0; text-align: center;">
        Hi ${firstName}, Your Resources Are Ready!
      </h1>

      <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0; text-align: center;">
        Click below to access your free Surge Bootcamp resources.
      </p>

      <!-- Resource List -->
      <div style="background-color: #0f172a; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">What you'll get:</p>
        <ul style="color: #22c55e; margin: 0; padding-left: 20px;">
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">2026 Action Plan Template</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Hit List (30+ Low-Competition Contracts)</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Hit List (Top 10 for Beginners)</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Spend Forecast + Buyers List</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Prime Contractor SBLO Directory</span></li>
          <li style="margin-bottom: 0;"><span style="color: #e2e8f0;">And more!</span></li>
        </ul>
      </div>

      <!-- CTA Button -->
      <div style="text-align: center; margin-bottom: 16px;">
        <a href="https://guides.govcongiants.org/surge-bootcamp/4-thank-you.html" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 16px 32px; border-radius: 8px; font-weight: bold; font-size: 16px;">
          Access Your Resources
        </a>
      </div>
    </div>

    <!-- Need Help Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center;">
      <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">Need Help or Have Questions?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Our team is here to help you succeed in government contracting.</p>
      <div style="margin-bottom: 12px;">
        <span style="color: #22c55e; font-size: 14px;">Call or Text:</span>
        <a href="tel:7864770477" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">786-477-0477</a>
      </div>
      <div>
        <span style="color: #22c55e; font-size: 14px;">Email:</span>
        <a href="mailto:hello@govconedu.com" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">hello@govconedu.com</a>
      </div>
    </div>

    <!-- Ready to Get Started Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center; border: 1px solid #22c55e;">
      <p style="color: #22c55e; font-weight: 600; margin: 0 0 8px 0;">Ready to Get Started?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Join our programs and start winning federal contracts today.</p>
      <div style="margin-bottom: 12px;">
        <a href="https://federalhelpcenter.com/starter" style="display: inline-block; background-color: #3b82f6; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Starter - $27/mo</a>
      </div>
      <div>
        <a href="https://federalhelpcenter.com/pro" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Pro - $99/mo</a>
      </div>
    </div>

    <!-- Footer -->
    <div style="text-align: center; color: #64748b; font-size: 12px;">
      <p style="margin: 0 0 8px 0;">Didn't request this? You can safely ignore this email.</p>
      <p style="margin: 0;">© 2026 GovCon Giants. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
    `
  },

  'opportunity-hunter': {
    subject: 'Your Opportunity Hunter Access Is Ready',
    getHtml: (firstName) => `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: system-ui, -apple-system, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
    <!-- Header -->
    <div style="text-align: center; margin-bottom: 32px;">
      <span style="font-size: 24px; font-weight: bold; color: white;">GovCon</span>
      <span style="font-size: 24px; font-weight: bold; color: #22c55e;">Giants</span>
    </div>

    <!-- Main Content -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 32px; margin-bottom: 24px;">
      <h1 style="color: white; font-size: 24px; margin: 0 0 16px 0; text-align: center;">
        Hi ${firstName}, Your Access Is Ready!
      </h1>

      <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0; text-align: center;">
        Click below to start using Opportunity Hunter and find federal agencies that buy what you sell.
      </p>

      <!-- Resource List -->
      <div style="background-color: #0f172a; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">What you'll get:</p>
        <ul style="color: #22c55e; margin: 0; padding-left: 20px;">
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Free Opportunity Hunter Tool Access</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">5 Searches Per Day</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Top 5 Agency Results</span></li>
          <li style="margin-bottom: 0;"><span style="color: #e2e8f0;">Quick Start Guide</span></li>
        </ul>
      </div>

      <!-- CTA Button -->
      <div style="text-align: center; margin-bottom: 16px;">
        <a href="https://guides.govcongiants.org/opportunity-hunter/3-thank-you.html" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 16px 32px; border-radius: 8px; font-weight: bold; font-size: 16px;">
          Launch Opportunity Hunter
        </a>
      </div>
    </div>

    <!-- Need Help Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center;">
      <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">Need Help or Have Questions?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Our team is here to help you succeed in government contracting.</p>
      <div style="margin-bottom: 12px;">
        <span style="color: #22c55e; font-size: 14px;">Call or Text:</span>
        <a href="tel:7864770477" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">786-477-0477</a>
      </div>
      <div>
        <span style="color: #22c55e; font-size: 14px;">Email:</span>
        <a href="mailto:hello@govconedu.com" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">hello@govconedu.com</a>
      </div>
    </div>

    <!-- Ready to Get Started Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center; border: 1px solid #22c55e;">
      <p style="color: #22c55e; font-weight: 600; margin: 0 0 8px 0;">Ready to Get Started?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Join our programs and start winning federal contracts today.</p>
      <div style="margin-bottom: 12px;">
        <a href="https://federalhelpcenter.com/starter" style="display: inline-block; background-color: #3b82f6; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Starter - $27/mo</a>
      </div>
      <div>
        <a href="https://federalhelpcenter.com/pro" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Pro - $99/mo</a>
      </div>
    </div>

    <!-- Footer -->
    <div style="text-align: center; color: #64748b; font-size: 12px;">
      <p style="margin: 0 0 8px 0;">Didn't request this? You can safely ignore this email.</p>
      <p style="margin: 0;">© 2026 GovCon Giants. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
    `
  },

  'free-resources': {
    subject: 'Your Free GovCon Resources',
    getHtml: (firstName) => `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: system-ui, -apple-system, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
    <!-- Header -->
    <div style="text-align: center; margin-bottom: 32px;">
      <span style="font-size: 24px; font-weight: bold; color: white;">GovCon</span>
      <span style="font-size: 24px; font-weight: bold; color: #22c55e;">Giants</span>
    </div>

    <!-- Main Content -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 32px; margin-bottom: 24px;">
      <h1 style="color: white; font-size: 24px; margin: 0 0 16px 0; text-align: center;">
        Hi ${firstName}, Your Resources Are Ready!
      </h1>

      <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0; text-align: center;">
        Click below to access your free GovCon resources.
      </p>

      <!-- Resource List -->
      <div style="background-color: #0f172a; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">What you'll get:</p>
        <ul style="color: #22c55e; margin: 0; padding-left: 20px;">
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">17+ Free Training Videos</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">SBLO Contact Directory</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Tribal Contractor List</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Agency Buyers Lists</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Hit Lists & Guides</span></li>
          <li style="margin-bottom: 0;"><span style="color: #e2e8f0;">And more!</span></li>
        </ul>
      </div>

      <!-- CTA Button -->
      <div style="text-align: center; margin-bottom: 16px;">
        <a href="https://guides.govcongiants.org/free-resources/resources.html" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 16px 32px; border-radius: 8px; font-weight: bold; font-size: 16px;">
          Access Your Resources
        </a>
      </div>
    </div>

    <!-- Need Help Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center;">
      <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">Need Help or Have Questions?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Our team is here to help you succeed in government contracting.</p>
      <div style="margin-bottom: 12px;">
        <span style="color: #22c55e; font-size: 14px;">Call or Text:</span>
        <a href="tel:7864770477" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">786-477-0477</a>
      </div>
      <div>
        <span style="color: #22c55e; font-size: 14px;">Email:</span>
        <a href="mailto:hello@govconedu.com" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">hello@govconedu.com</a>
      </div>
    </div>

    <!-- Ready to Get Started Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center; border: 1px solid #22c55e;">
      <p style="color: #22c55e; font-weight: 600; margin: 0 0 8px 0;">Ready to Get Started?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Join our programs and start winning federal contracts today.</p>
      <div style="margin-bottom: 12px;">
        <a href="https://federalhelpcenter.com/starter" style="display: inline-block; background-color: #3b82f6; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Starter - $27/mo</a>
      </div>
      <div>
        <a href="https://federalhelpcenter.com/pro" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Pro - $99/mo</a>
      </div>
    </div>

    <!-- Footer -->
    <div style="text-align: center; color: #64748b; font-size: 12px;">
      <p style="margin: 0 0 8px 0;">Didn't request this? You can safely ignore this email.</p>
      <p style="margin: 0;">© 2026 GovCon Giants. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
    `
  },

  'free-course': {
    subject: 'Your Free GovCon Course Access',
    getHtml: (firstName) => `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: system-ui, -apple-system, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
    <!-- Header -->
    <div style="text-align: center; margin-bottom: 32px;">
      <span style="font-size: 24px; font-weight: bold; color: white;">GovCon</span>
      <span style="font-size: 24px; font-weight: bold; color: #22c55e;">Giants</span>
    </div>

    <!-- Main Content -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 32px; margin-bottom: 24px;">
      <h1 style="color: white; font-size: 24px; margin: 0 0 16px 0; text-align: center;">
        Hi ${firstName}, Your Course Is Ready!
      </h1>

      <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0 0 24px 0; text-align: center;">
        Click below to start learning how to win federal contracts.
      </p>

      <!-- Resource List -->
      <div style="background-color: #0f172a; border-radius: 8px; padding: 20px; margin-bottom: 24px;">
        <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">What you'll learn:</p>
        <ul style="color: #22c55e; margin: 0; padding-left: 20px;">
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">GovCon Fundamentals</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">How to Get Registered</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Finding Contract Opportunities</span></li>
          <li style="margin-bottom: 8px;"><span style="color: #e2e8f0;">Writing Winning Proposals</span></li>
          <li style="margin-bottom: 0;"><span style="color: #e2e8f0;">And more!</span></li>
        </ul>
      </div>

      <!-- CTA Button -->
      <div style="text-align: center; margin-bottom: 16px;">
        <a href="https://guides.govcongiants.org/free-course/course.html" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 16px 32px; border-radius: 8px; font-weight: bold; font-size: 16px;">
          Start Your Course
        </a>
      </div>
    </div>

    <!-- Need Help Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center;">
      <p style="color: white; font-weight: 600; margin: 0 0 12px 0;">Need Help or Have Questions?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Our team is here to help you succeed in government contracting.</p>
      <div style="margin-bottom: 12px;">
        <span style="color: #22c55e; font-size: 14px;">Call or Text:</span>
        <a href="tel:7864770477" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">786-477-0477</a>
      </div>
      <div>
        <span style="color: #22c55e; font-size: 14px;">Email:</span>
        <a href="mailto:hello@govconedu.com" style="color: white; font-weight: bold; text-decoration: none; margin-left: 8px;">hello@govconedu.com</a>
      </div>
    </div>

    <!-- Ready to Get Started Section -->
    <div style="background-color: #1e293b; border-radius: 12px; padding: 24px; margin-bottom: 24px; text-align: center; border: 1px solid #22c55e;">
      <p style="color: #22c55e; font-weight: 600; margin: 0 0 8px 0;">Ready to Get Started?</p>
      <p style="color: #94a3b8; font-size: 14px; margin: 0 0 16px 0;">Join our programs and start winning federal contracts today.</p>
      <div style="margin-bottom: 12px;">
        <a href="https://federalhelpcenter.com/starter" style="display: inline-block; background-color: #3b82f6; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Starter - $27/mo</a>
      </div>
      <div>
        <a href="https://federalhelpcenter.com/pro" style="display: inline-block; background-color: #22c55e; color: white; text-decoration: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; font-size: 14px; margin: 4px;">Pro - $99/mo</a>
      </div>
    </div>

    <!-- Footer -->
    <div style="text-align: center; color: #64748b; font-size: 12px;">
      <p style="margin: 0 0 8px 0;">Didn't request this? You can safely ignore this email.</p>
      <p style="margin: 0;">© 2026 GovCon Giants. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
    `
  }
};

// Default template for unknown sources
const defaultTemplate = {
  subject: 'Welcome to GovCon Giants!',
  getHtml: (firstName) => `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background-color: #0f172a; font-family: system-ui, -apple-system, sans-serif;">
  <div style="max-width: 600px; margin: 0 auto; padding: 40px 20px;">
    <div style="text-align: center; margin-bottom: 32px;">
      <span style="font-size: 24px; font-weight: bold; color: white;">GovCon</span>
      <span style="font-size: 24px; font-weight: bold; color: #22c55e;">Giants</span>
    </div>
    <div style="background-color: #1e293b; border-radius: 12px; padding: 32px;">
      <h1 style="color: white; font-size: 24px; margin: 0 0 16px 0; text-align: center;">Welcome, ${firstName}!</h1>
      <p style="color: #94a3b8; font-size: 16px; line-height: 1.6; margin: 0; text-align: center;">
        Thank you for joining GovCon Giants. We'll be in touch with resources to help you win federal contracts.
      </p>
    </div>
    <div style="text-align: center; color: #64748b; font-size: 12px; margin-top: 24px;">
      <p style="margin: 0;">© 2026 GovCon Giants. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
  `
};

// Send confirmation email
async function sendConfirmationEmail(to, firstName, source) {
  const gmailUser = process.env.GMAIL_USER;
  const gmailAppPassword = process.env.GMAIL_APP_PASSWORD;

  if (!gmailUser || !gmailAppPassword) {
    console.log('Gmail not configured, skipping email');
    return { success: false, reason: 'Gmail not configured' };
  }

  // Create transporter
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
      user: gmailUser,
      pass: gmailAppPassword
    }
  });

  // Get template based on source
  const template = emailTemplates[source] || defaultTemplate;

  try {
    const result = await transporter.sendMail({
      from: `"GovCon Giants" <${gmailUser}>`,
      to: to,
      subject: template.subject,
      html: template.getHtml(firstName)
    });

    console.log('Email sent:', result.messageId);
    return { success: true, messageId: result.messageId };
  } catch (error) {
    console.error('Email error:', error.message);
    return { success: false, reason: error.message };
  }
}

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
    const { name, email, phone, source, tags } = req.body;

    // Validate required fields
    if (!name || !email) {
      return res.status(400).json({ error: 'Name and email are required' });
    }

    // Parse first and last name
    const nameParts = name.trim().split(' ');
    const firstName = nameParts[0] || '';
    const lastName = nameParts.slice(1).join(' ') || '';
    const cleanEmail = email.toLowerCase().trim();

    // 1. Send confirmation email FIRST (so user gets it immediately)
    const emailResult = await sendConfirmationEmail(cleanEmail, firstName, source);

    // 2. Send to GHL
    const apiKey = process.env.GHL_API_KEY;
    const locationId = process.env.GHL_LOCATION_ID;

    let ghlSuccess = false;
    let ghlError = null;

    if (apiKey && locationId) {
      const ghlPayload = {
        firstName,
        lastName,
        email: cleanEmail,
        phone: phone || '',
        source: source || 'funnel',
        tags: tags || [],
        locationId: locationId,
      };

      try {
        const ghlResponse = await fetch('https://rest.gohighlevel.com/v1/contacts/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(ghlPayload),
        });

        const ghlResult = await ghlResponse.json();

        if (!ghlResponse.ok) {
          console.error('GHL API error:', ghlResult);
          ghlError = ghlResult;
        } else {
          console.log('Contact created/updated in GHL:', ghlResult.contact?.id);
          ghlSuccess = true;
        }
      } catch (ghlErr) {
        console.error('GHL fetch error:', ghlErr.message);
        ghlError = ghlErr.message;
      }
    } else {
      console.log('GHL API not configured. Lead data:', { firstName, lastName, email: cleanEmail, phone, source, tags });
    }

    // Return success
    return res.status(200).json({
      success: true,
      message: 'Lead captured successfully',
      emailSent: emailResult.success,
      ghlSuccess: ghlSuccess,
      ghlError: ghlError,
      data: {
        firstName,
        lastName,
        email: cleanEmail,
        source,
      }
    });

  } catch (error) {
    console.error('Lead capture error:', error);
    return res.status(500).json({
      error: 'Failed to capture lead',
      message: error.message
    });
  }
}
