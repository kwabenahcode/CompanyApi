# contact/resend_backend.py - PROFESSIONAL VERSION
import resend
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ResendBackend(BaseEmailBackend):
    """Professional Resend.com email backend with comprehensive error handling"""
    
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        
        # Initialize Resend with API key
        api_key = getattr(settings, 'RESEND_API_KEY', '')
        if not api_key:
            raise ValueError("RESEND_API_KEY is not configured in settings")
        
        resend.api_key = api_key
        
        # Set default configuration
        self.default_from = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
    
    def send_messages(self, email_messages):
        """Send multiple email messages via Resend"""
        if not email_messages:
            return 0
        
        num_sent = 0
        
        for email in email_messages:
            try:
                # Validate required fields
                if not email.to:
                    logger.warning("Email skipped: No recipients specified")
                    continue
                
                if not email.subject:
                    logger.warning("Email skipped: No subject specified")
                    continue
                
                # Prepare Resend parameters
                params = {
                    "from": email.from_email or self.default_from,
                    "to": email.to,
                    "subject": email.subject,
                    "text": email.body or "No text content",
                }
                
                # Add HTML content if available
                if email.alternatives:
                    html_content = None
                    for content, mimetype in email.alternatives:
                        if mimetype == "text/html":
                            html_content = content
                            break
                    
                    if html_content:
                        params["html"] = html_content
                
                # Add reply-to if specified
                if hasattr(email, 'reply_to') and email.reply_to:
                    params["reply_to"] = email.reply_to[0] if isinstance(email.reply_to, list) else email.reply_to
                
                # Send via Resend
                response = resend.Emails.send(params)
                
                if response and 'id' in response:
                    logger.debug(f"✅ Resend email sent: {params['to']} (ID: {response['id']})")
                    num_sent += 1
                else:
                    logger.warning(f"⚠️ Resend response missing ID: {response}")
                    if not self.fail_silently:
                        raise ValueError(f"Invalid response from Resend: {response}")
                
            except resend.ResendError as e:
                logger.error(f"❌ Resend API error: {str(e)}")
                if not self.fail_silently:
                    raise
            except Exception as e:
                logger.error(f"❌ Unexpected error sending email: {str(e)}")
                if not self.fail_silently:
                    raise
        
        return num_sent
    
    def open(self):
        """Required by BaseEmailBackend - no-op for Resend"""
        return True
    
    def close(self):
        """Required by BaseEmailBackend - no-op for Resend"""
        pass