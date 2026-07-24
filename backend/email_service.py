"""
Email service for sending contact notifications via SMTP.
"""

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)

async def send_contact_email(
    name: str,
    email: str,
    message: str,
    ip_address: str
) -> bool:
    """
    Send contact form notification email to the portfolio owner.
    
    Args:
        name: Sender's name
        email: Sender's email
        message: Message content
        ip_address: Sender's IP address
    
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        logger.info(f"Sending contact email from {email}")
        
        # Create email content
        subject = f"New Contact Form Submission from {name}"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #333; border-bottom: 2px solid #3da9fc; padding-bottom: 10px;">New Contact Form Submission</h2>
                    
                    <div style="margin: 20px 0;">
                        <p><strong>From:</strong> {name}</p>
                        <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                        <p><strong>IP Address:</strong> {ip_address}</p>
                        <p><strong>Submission Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                    </div>
                    
                    <h3 style="color: #333; margin-top: 20px;">Message:</h3>
                    <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #3da9fc; border-radius: 4px;">
                        <p style="white-space: pre-wrap; word-wrap: break-word; color: #555;">{message}</p>
                    </div>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #999; font-size: 12px;">
                        <p>This is an automated notification from your portfolio contact form.</p>
                        <p>Please reply directly to {email} to respond to this message.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        text_body = f"""
New Contact Form Submission

From: {name}
Email: {email}
IP Address: {ip_address}

Message:
{message}

---
This is an automated notification from your portfolio contact form.
Please reply directly to {email} to respond to this message.
        """
        
        # Create MIME message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.SMTP_FROM_EMAIL
        msg['To'] = settings.OWNER_EMAIL
        msg['Reply-To'] = email
        
        # Attach text and HTML versions
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        if settings.SMTP_USE_TLS:
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT)
        
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Contact email sent successfully to {settings.OWNER_EMAIL}")
        return True
    
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"SMTP authentication failed: {e}")
        logger.error(f"Verify SMTP credentials in .env file")
        return False
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending email: {e}", exc_info=True)
        return False

async def send_autoresponder_email(
    recipient_email: str,
    recipient_name: str
) -> bool:
    """
    Send automated response email to the contact form submitter.
    
    Args:
        recipient_email: Email to send to
        recipient_name: Recipient's name
    
    Returns:
        True if email sent successfully, False otherwise
    """
    try:
        logger.info(f"Sending auto-response to {recipient_email}")
        
        subject = "Thank you for contacting me"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px;">
                    <h2 style="color: #3da9fc;">Thank you for reaching out, {recipient_name}!</h2>
                    
                    <p>I have received your message and appreciate you taking the time to contact me.</p>
                    
                    <p>I typically respond to messages within 24-48 hours. I'll review your message and get back to you as soon as possible.</p>
                    
                    <p>Best regards,<br>Aravind Adityaa</p>
                    
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #999; font-size: 12px;">
                        <p>This is an automated response. Please do not reply to this email.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        text_body = f"""
Thank you for reaching out, {recipient_name}!

I have received your message and appreciate you taking the time to contact me.

I typically respond to messages within 24-48 hours. I'll review your message and get back to you as soon as possible.

Best regards,
Aravind Adityaa

---
This is an automated response. Please do not reply to this email.
        """
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = settings.SMTP_FROM_EMAIL
        msg['To'] = recipient_email
        
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        if settings.SMTP_USE_TLS:
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(settings.SMTP_SERVER, settings.SMTP_PORT)
        
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Auto-response sent to {recipient_email}")
        return True
    
    except Exception as e:
        logger.error(f"Error sending auto-response: {e}", exc_info=True)
        return False
