import os
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread
from extensions.extensions import mail

def send_async_email(app, msg):
    """Helper function to send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f"Error sending email: {str(e)}")

def send_email(subject, recipients, template, **kwargs):
    """
    Send an email using a template.
    
    Args:
        subject (str): Email subject
        recipients (list): List of recipient email addresses
        template (str): Template name without extension (looks in templates/email/)
        **kwargs: Variables to pass to the template
    """
    try:
        # Ensure we have a list of recipients
        if isinstance(recipients, str):
            recipients = [recipients]
            
        # Skip sending email if in test mode and not explicitly allowed
        if current_app.config.get('TESTING') and not kwargs.get('force_send', False):
            current_app.logger.info(f"Email not sent in test mode: {subject} to {recipients}")
            return True
            
        # Render email templates
        html_body = render_template(f'email/{template}.html', **kwargs)
        text_body = render_template(f'email/{template}.txt', **kwargs)
        
        # Create message
        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=recipients,
            html=html_body,
            body=text_body
        )
        
        # Send email asynchronously in production, synchronously in development
        if current_app.config.get('MAIL_USE_ASYNC', True) and not current_app.config.get('TESTING'):
            # Create a new thread to send the email asynchronously
            Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        else:
            mail.send(msg)
            
        current_app.logger.info(f"Email sent: {subject} to {recipients}")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Failed to send email to {recipients}: {str(e)}")
        if current_app.config.get('DEBUG'):
            raise
        return False

def send_welcome_email(user):
    """Send welcome email to new user"""
    login_url = f"{current_app.config.get('FRONTEND_URL', '')}/login"
    return send_email(
        subject="Welcome to Laundry & Services Platform",
        recipients=[user.email],
        template='welcome',
        user=user,
        login_url=login_url
    )

def send_password_reset_email(user, token):
    """Send password reset email"""
    reset_url = f"{current_app.config.get('FRONTEND_URL', '')}/reset-password?token={token}"
    return send_email(
        subject="Password Reset Request",
        recipients=[user.email],
        template='reset_password',
        user=user,
        reset_url=reset_url
    )

def send_password_changed_email(user):
    """Send confirmation email when password is changed"""
    return send_email(
        subject="Your Password Has Been Changed",
        recipients=[user.email],
        template='password_changed',
        user=user
    )

def send_service_assignment_email(service, provider):
    """Send email to service provider when assigned to a service"""
    service_url = f"{current_app.config.get('FRONTEND_URL', '')}/services/{service.id}"
    return send_email(
        subject=f"New Service Assignment: {service.title}",
        recipients=[provider.email],
        template='service_assignment',
        service=service,
        provider=provider,
        service_url=service_url
    )

def send_service_status_update(service, user, status):
    """Send email when service status is updated"""
    service_url = f"{current_app.config.get('FRONTEND_URL', '')}/services/{service.id}"
    return send_email(
        subject=f"Service Update: {service.title} is now {status}",
        recipients=[user.email],
        template='service_status_update',
        service=service,
        user=user,
        status=status,
        service_url=service_url
    )

def send_new_message_notification(recipient, sender, message, service):
    """Send notification about new message"""
    message_url = f"{current_app.config.get('FRONTEND_URL', '')}/messages/{service.id}"
    return send_email(
        subject=f"New message about your service: {service.title}",
        recipients=[recipient.email],
        template='new_message',
        recipient=recipient,
        sender=sender,
        message=message,
        service=service,
        message_url=message_url
    )
