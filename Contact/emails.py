# contact/emails.py - PROFESSIONAL VERSION
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    """Professional email service with fallback templates and error handling"""
    
    @staticmethod
    def send_contact_notification(contact_data):
        """Send notification to company about new contact"""
        try:
            # Prepare context with safe defaults
            context = {
                'name': contact_data.get('name', 'Guest'),
                'email': contact_data.get('email', 'No email provided'),
                'phone': contact_data.get('phone', 'Not provided'),
                'message': contact_data.get('message', 'No message content'),
                'created_at': contact_data.get('created_at', datetime.now()),
                'company_name': getattr(settings, 'COMPANY_NAME', 'Our Company'),
                'company_phone': getattr(settings, 'COMPANY_PHONE', ''),
                'company_website': getattr(settings, 'COMPANY_WEBSITE', '#'),
            }
            
            # Try to load HTML template, fallback to text
            try:
                html_content = render_to_string('emails/contact_notification.html', context)
            except:
                html_content = f"""
                <html><body>
                <h2>New Contact Form Submission</h2>
                <p><strong>Name:</strong> {context['name']}</p>
                <p><strong>Email:</strong> {context['email']}</p>
                <p><strong>Phone:</strong> {context['phone']}</p>
                <p><strong>Message:</strong></p>
                <p>{context['message']}</p>
                </body></html>
                """
            
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject=f"📬 New Contact: {context['name']}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.COMPANY_EMAIL],
                reply_to=[context['email']],
                headers={'X-Contact-ID': str(uuid.uuid4())},
            )
            email.attach_alternative(html_content, "text/html")
            
            email.send(fail_silently=False)
            logger.info(f"✅ Notification sent successfully to {settings.COMPANY_EMAIL}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Contact notification failed: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def send_autoreply_to_client(contact_data):
        """Send auto-reply to client with reference ID"""
        try:
            reference_id = str(uuid.uuid4())[:8].upper()
            
            context = {
                'name': contact_data.get('name', 'Valued Customer'),
                'email': contact_data.get('email', ''),
                'reference_id': reference_id,
                'created_at': contact_data.get('created_at', datetime.now()),
                'company_name': getattr(settings, 'COMPANY_NAME', 'OFORITECH SOLUTIONS'),
                'company_phone': getattr(settings, 'COMPANY_PHONE', ''),
                'company_website': getattr(settings, 'COMPANY_WEBSITE', 'https://oforitechsolutions.com'),
            }
            
            # Try to load HTML template, fallback to text
            try:
                html_content = render_to_string('emails/contact_autoreply.html', context)
            except:
                html_content = f"""
                <html><body>
                <h2>Thank You, {context['name']}!</h2>
                <p>We have received your message (Reference: {reference_id}) and will respond within 24 hours.</p>
                <p>Best regards,<br>{context['company_name']}</p>
                </body></html>
                """
            
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject=f"✅ Thank you for contacting {context['company_name']}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[context['email']],
                reply_to=[settings.COMPANY_EMAIL],
                headers={'X-Reference-ID': reference_id},
            )
            email.attach_alternative(html_content, "text/html")
            
            email.send(fail_silently=False)
            logger.info(f"✅ Auto-reply sent to {context['email']} (Ref: {reference_id})")
            return reference_id
            
        except Exception as e:
            logger.error(f"❌ Auto-reply failed for {contact_data.get('email', 'unknown')}: {str(e)}", exc_info=True)
            raise