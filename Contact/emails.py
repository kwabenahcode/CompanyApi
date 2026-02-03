# contact/emails.py - FIXED VERSION
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import uuid

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_contact_notification(contact_data):
        """Send notification to company"""
        try:
            context = {
                'name': contact_data.get('name', ''),
                'email': contact_data.get('email', ''),
                'phone': contact_data.get('phone', ''),
                'message': contact_data.get('message', ''),
                'created_at': contact_data.get('created_at', ''),
            }
            
            html_content = render_to_string('emails/contact_notification.html', context)
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject=f"📬 New Contact: {contact_data.get('name', 'Visitor')}",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Changed from EMAIL_HOST_USER
                to=[settings.COMPANY_EMAIL],
                reply_to=[contact_data.get('email', '')],
            )
            email.attach_alternative(html_content, "text/html")
            
            # ✅ CRITICAL FIX: Change to False to see errors
            email.send(fail_silently=False)  # Changed from True
            logger.info(f"✅ Notification email sent for {contact_data.get('email')}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Email notification failed: {str(e)}")
            # Don't swallow the exception - let it bubble up
            raise
    
    @staticmethod
    def send_autoreply_to_client(contact_data):
        """Send auto-reply to client"""
        try:
            reference_id = str(uuid.uuid4())[:8].upper()
            
            context = {
                'name': contact_data.get('name', ''),
                'email': contact_data.get('email', ''),
                'reference_id': reference_id,
                'created_at': contact_data.get('created_at', ''),
            }
            
            html_content = render_to_string('emails/contact_autoreply.html', context)
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject="✅ Message Received - OFORITECH SOLUTIONS",
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Changed from EMAIL_HOST_USER
                to=[contact_data.get('email', '')],
                reply_to=[settings.COMPANY_EMAIL],
            )
            email.attach_alternative(html_content, "text/html")
            
            # ✅ CRITICAL FIX: Change to False to see errors
            email.send(fail_silently=False)  # Changed from True
            logger.info(f"✅ Autoreply sent to {contact_data.get('email')}")
            return reference_id
            
        except Exception as e:
            logger.error(f"❌ Autoreply failed: {str(e)}")
            raise