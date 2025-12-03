from flask import Flask, request, jsonify, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

app = Flask(__name__)

# Mailtrap Configuration (Use environment variables in production)
MAILTRAP_HOST = os.getenv('MAILTRAP_HOST', 'sandbox.smtp.mailtrap.io')
MAILTRAP_PORT = int(os.getenv('MAILTRAP_PORT', 2525))
MAILTRAP_USER = os.getenv('MAILTRAP_USER', 'YOUR_MAILTRAP_USERNAME')
MAILTRAP_PASSWORD = os.getenv('MAILTRAP_PASSWORD', 'YOUR_MAILTRAP_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'info@wanderwell.com')


def send_lead_email(lead_data):
    """
    Send lead notification via Mailtrap SMTP

    Args:
        lead_data (dict): Lead information containing name, phone, travelers, source, etc.

    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🎯 New Lead from Wanderwell Landing Page - {lead_data.get('source', 'Unknown')}"
        msg['From'] = f"Wanderwell Travels <noreply@wanderwell.com>"
        msg['To'] = RECIPIENT_EMAIL

        # Format timestamp
        timestamp = lead_data.get('timestamp', datetime.now().isoformat())
        formatted_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00')).strftime('%B %d, %Y at %I:%M %p')

        # Create HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #3b82f6, #2563eb);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 24px;
                }}
                .content {{
                    background: #f9fafb;
                    padding: 30px;
                    border-left: 5px solid #ef4444;
                }}
                .lead-info {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .info-row {{
                    display: flex;
                    padding: 12px 0;
                    border-bottom: 1px solid #e5e7eb;
                }}
                .info-row:last-child {{
                    border-bottom: none;
                }}
                .info-label {{
                    font-weight: 600;
                    color: #1f2937;
                    width: 140px;
                    flex-shrink: 0;
                }}
                .info-value {{
                    color: #6b7280;
                    flex: 1;
                }}
                .cta-button {{
                    display: inline-block;
                    background: #ef4444;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 6px;
                    font-weight: 600;
                    margin-top: 20px;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #6b7280;
                    font-size: 14px;
                }}
                .badge {{
                    display: inline-block;
                    background: #10b981;
                    color: white;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                    margin-left: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎯 New Lead Received!</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">Someone is interested in your Kashmir tour packages</p>
            </div>

            <div class="content">
                <p style="font-size: 16px; margin-bottom: 20px;">
                    Great news! You have a new lead from your landing page. 
                    <span class="badge">{lead_data.get('source', 'Unknown').replace('_', ' ').upper()}</span>
                </p>

                <div class="lead-info">
                    <h2 style="margin-top: 0; color: #1f2937; font-size: 20px;">Lead Details</h2>

                    <div class="info-row">
                        <div class="info-label">👤 Name:</div>
                        <div class="info-value">{lead_data.get('name', 'Not provided')}</div>
                    </div>

                    <div class="info-row">
                        <div class="info-label">📱 Phone:</div>
                        <div class="info-value">
                            <strong style="color: #ef4444; font-size: 18px;">
                                {lead_data.get('phone', 'Not provided')}
                            </strong>
                        </div>
                    </div>

                    <div class="info-row">
                        <div class="info-label">👥 Travelers:</div>
                        <div class="info-value">{lead_data.get('travelers', 'Not specified')}</div>
                    </div>

                    <div class="info-row">
                        <div class="info-label">📍 Source:</div>
                        <div class="info-value">{lead_data.get('source', 'Unknown').replace('_', ' ').title()}</div>
                    </div>

                    <div class="info-row">
                        <div class="info-label">🌐 Page URL:</div>
                        <div class="info-value">
                            <a href="{lead_data.get('page_url', '#')}" style="color: #3b82f6;">
                                {lead_data.get('page_url', 'Not available')}
                            </a>
                        </div>
                    </div>

                    <div class="info-row">
                        <div class="info-label">🕐 Timestamp:</div>
                        <div class="info-value">{formatted_time}</div>
                    </div>
                </div>

                <div style="text-align: center;">
                    <a href="tel:{lead_data.get('phone', '')}" class="cta-button">
                        📞 Call {lead_data.get('name', 'Customer')} Now
                    </a>
                </div>

                <p style="margin-top: 20px; padding: 15px; background: #fef3c7; border-left: 4px solid #fbbf24; border-radius: 4px;">
                    <strong>⚡ Quick Tip:</strong> Respond within 5 minutes for best conversion rates! 
                    Customers are most engaged immediately after filling the form.
                </p>
            </div>

            <div class="footer">
                <p>This is an automated notification from your Wanderwell Travels landing page.</p>
                <p style="margin: 5px 0;">© 2024 Wanderwell Travels. All rights reserved.</p>
            </div>
        </body>
        </html>
        """

        # Create plain text version (fallback)
        text_body = f"""
        NEW LEAD RECEIVED - Wanderwell Travels
        ========================================

        Name: {lead_data.get('name', 'Not provided')}
        Phone: {lead_data.get('phone', 'Not provided')}
        Travelers: {lead_data.get('travelers', 'Not specified')}
        Source: {lead_data.get('source', 'Unknown')}
        Page URL: {lead_data.get('page_url', 'Not available')}
        Timestamp: {formatted_time}

        ========================================
        Call the customer now: {lead_data.get('phone', '')}
        """

        # Attach both versions
        part1 = MIMEText(text_body, 'plain')
        part2 = MIMEText(html_body, 'html')
        msg.attach(part1)
        msg.attach(part2)

        # Send email via Mailtrap SMTP
        with smtplib.SMTP(MAILTRAP_HOST, MAILTRAP_PORT) as server:
            server.starttls()
            server.login(MAILTRAP_USER, MAILTRAP_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent successfully to {RECIPIENT_EMAIL}")
        return True

    except Exception as e:
        print(f"❌ Email sending failed: {str(e)}")
        return False


@app.route('/')
def index():
    """Serve the landing page"""
    # Read the HTML file
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return render_template_string(html_content)
    except FileNotFoundError:
        return """
        <h1>Error: index.html not found</h1>
        <p>Please ensure index.html is in the same directory as app.py</p>
        """, 404


@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    """
    Handle lead submission from the landing page
    - Validates phone number (required field)
    - Sends email notification via Mailtrap
    - Returns JSON response
    """
    try:
        # Get JSON data from request
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No data received'
            }), 400

        # Validate required field (phone)
        phone = data.get('phone', '').strip()
        if not phone:
            return jsonify({
                'success': False,
                'message': 'Phone number is required'
            }), 400

        # Extract lead information
        lead_data = {
            'name': data.get('name', 'Not provided').strip() or 'Not provided',
            'phone': phone,
            'travelers': data.get('travelers', 'Not specified').strip() or 'Not specified',
            'source': data.get('source', 'unknown'),
            'timestamp': data.get('timestamp', datetime.now().isoformat()),
            'page_url': data.get('page_url', 'Not available')
        }

        # Log lead to console
        print("\n" + "=" * 60)
        print("📝 NEW LEAD RECEIVED")
        print("=" * 60)
        print(f"Name: {lead_data['name']}")
        print(f"Phone: {lead_data['phone']}")
        print(f"Travelers: {lead_data['travelers']}")
        print(f"Source: {lead_data['source']}")
        print(f"Page URL: {lead_data['page_url']}")
        print(f"Timestamp: {lead_data['timestamp']}")
        print("=" * 60 + "\n")

        # Send email notification
        email_sent = send_lead_email(lead_data)

        if email_sent:
            return jsonify({
                'success': True,
                'message': 'Thank you for your interest! Our team will contact you within 24 hours.',
                'leadId': datetime.now().strftime('%Y%m%d%H%M%S')
            }), 200
        else:
            # Email failed but we still received the lead (logged to console)
            return jsonify({
                'success': False,
                'message': 'We received your request but there was an issue with notifications. Please call us directly at +91 98765 43210.',
                'leadId': datetime.now().strftime('%Y%m%d%H%M%S')
            }), 200

    except Exception as e:
        print(f"❌ Error processing lead: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'An error occurred. Please try again or call us directly.'
        }), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'Wanderwell Travels Landing Page'
    }), 200


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Development server
    print("\n" + "=" * 60)
    print("🚀 Starting Wanderwell Travels Landing Page Server")
    print("=" * 60)
    print(f"Server: Flask Development Server")
    print(f"URL: http://localhost:5000")
    print(f"Mailtrap Host: {MAILTRAP_HOST}")
    print(f"Mailtrap Port: {MAILTRAP_PORT}")
    print(f"Recipient Email: {RECIPIENT_EMAIL}")
    print("=" * 60 + "\n")
    print("⚠️  IMPORTANT: Update Mailtrap credentials in environment variables:")
    print("   export MAILTRAP_USER='your_mailtrap_username'")
    print("   export MAILTRAP_PASSWORD='your_mailtrap_password'")
    print("   export RECIPIENT_EMAIL='your_email@example.com'")
    print("\n" + "=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
