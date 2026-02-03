# contact/views.py - PROFESSIONAL VERSION
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import logging
from django.conf import settings

from .models import ContactInquiry
from .serializer import ContactSerializer
from .emails import EmailService

logger = logging.getLogger(__name__)

class ContactCreateView(generics.GenericAPIView):
    """Professional contact form API with comprehensive error handling"""
    permission_classes = [AllowAny]
    serializer_class = ContactSerializer
    
    def post(self, request, *args, **kwargs):
        # Step 1: Validate incoming data
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'success': False,
                    'message': 'Please check your form inputs',
                    'errors': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Step 2: Save contact to database
        try:
            contact = serializer.save()
            logger.info(f"Contact saved successfully: {contact.name} - {contact.email}")
            
            # Prepare contact data for emails
            contact_data = {
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone or 'Not provided',
                'message': contact.message,
                'created_at': contact.created_at,
            }
            
            # Step 3: Send emails synchronously (better error tracking)
            email_success = self._send_emails(contact_data, contact.id)
            
            # Step 4: Prepare success response
            response_data = {
                'success': True,
                'message': 'Thank you for your message! We\'ll contact you within 24 hours.',
                'data': {
                    'id': contact.id,
                    'name': contact.name,
                    'email': contact.email,
                    'submitted_at': contact.created_at.strftime('%B %d, %Y at %I:%M %p'),
                    'emails_sent': email_success,
                }
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Contact form processing error: {str(e)}", exc_info=True)
            return Response(
                {
                    'success': False,
                    'message': 'An error occurred while processing your request.',
                    'error': str(e) if settings.DEBUG else None,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def _send_emails(self, contact_data, contact_id):
        """Handle email sending with proper error tracking"""
        email_results = {
            'notification': False,
            'autoreply': False
        }
        
        try:
            # Debug: Log email configuration
            self._log_email_config()
            
            # Send notification to company
            try:
                EmailService.send_contact_notification(contact_data)
                email_results['notification'] = True
                logger.info(f"✅ Notification email sent for contact ID: {contact_id}")
            except Exception as e:
                logger.error(f"❌ Notification email failed for contact {contact_id}: {str(e)}")
                if settings.DEBUG:
                    raise  # Re-raise in development to see errors
            
            # Send auto-reply to client
            try:
                reference_id = EmailService.send_autoreply_to_client(contact_data)
                email_results['autoreply'] = True
                logger.info(f"✅ Auto-reply sent to {contact_data['email']} (Ref: {reference_id})")
            except Exception as e:
                logger.error(f"❌ Auto-reply failed for {contact_data['email']}: {str(e)}")
                if settings.DEBUG:
                    raise
            
            return email_results
            
        except Exception as e:
            logger.error(f"❌ Email sending process failed: {str(e)}", exc_info=True)
            return email_results
    
    def _log_email_config(self):
        """Log email configuration for debugging"""
        if settings.DEBUG:
            logger.debug(f"Email Backend: {settings.EMAIL_BACKEND}")
            logger.debug(f"Resend API Key Set: {bool(settings.RESEND_API_KEY)}")
            logger.debug(f"Default From: {settings.DEFAULT_FROM_EMAIL}")
            logger.debug(f"Company Email: {settings.COMPANY_EMAIL}")