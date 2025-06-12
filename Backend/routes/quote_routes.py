from flask import Blueprint, request, jsonify, current_app
from utils.email import send_email

quote_bp = Blueprint('quote', __name__)

@quote_bp.route('/api/send-quote', methods=['POST'])
def send_quote():
    data = request.get_json()
    # Compose email content
    subject = 'New Free Quote Request'
    recipients = ['phelixmbani@gmail.com']
    template = None  # We'll use a simple string, not a template
    # Build message body
    body = f"""
    New Free Quote Request

    Name: {data.get('firstName', '')} {data.get('lastName', '')}
    Email: {data.get('email', '')}
    Phone: {data.get('phone', '')}
    Service Type: {data.get('serviceType', '')}
    Message: {data.get('message', '')}
    """
    try:
        from flask_mail import Message
        from extensions.extensions import mail
        msg = Message(subject=subject,
                      sender=current_app.config['MAIL_DEFAULT_SENDER'],
                      recipients=recipients,
                      body=body)
        mail.send(msg)
        return jsonify({'message': 'Quote sent successfully'}), 200
    except Exception as e:
        current_app.logger.error(f"Failed to send quote: {str(e)}")
        return jsonify({'error': 'Failed to send quote'}), 500
