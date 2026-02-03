# contact/views.py - MODIFIED VERSION
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import logging
from django.conf import settings  # Add this

from .models import ContactInquiry
from .serializer import ContactSerializer
from .emails import EmailService

logger = logging.getLogger(__name__)

class ContactCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContactSerializer
    
    def post(self, request, *args, **kwargs):
        # Validate the incoming data
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
        
        try:
            # Save to database
            contact = serializer.save()
            logger.info(f"Contact saved: {contact.name} - {contact.email}")
            
            # --- REMOVE THREADING, SEND EMAILS DIRECTLY ---
            try:
                contact_data = {
                    'name': contact.name,
                    'email': contact.email,
                    'phone': contact.phone or '',
                    'message': contact.message,
                    'created_at': contact.created_at,
                }
                
                # DEBUG: Print email settings
                logger.info(f"EMAIL_HOST_USER configured: {bool(settings.EMAIL_HOST_USER)}")
                logger.info(f"EMAIL_HOST_PASSWORD configured: {bool(settings.EMAIL_HOST_PASSWORD)}")
                
                # Send notification to company
                EmailService.send_contact_notification(contact_data)
                logger.info("Company notification email sent")
                
                # Send auto-reply to client
                EmailService.send_autoreply_to_client(contact_data)
                logger.info("Client auto-reply email sent")
                
            except Exception as email_error:
                # Log the actual SMTP error
                logger.error(f"EMAIL FAILED: {str(email_error)}")
                # Don't fail the request, just log it
                pass
            
            # Prepare success response
            response_data = {
                'success': True,
                'message': 'Thank you for your message! We\'ll contact you within 24 hours.',
                'data': {
                    'id': contact.id,
                    'name': contact.name,
                    'email': contact.email,
                    'submitted_at': contact.created_at.strftime('%B %d, %Y at %I:%M %p'),
                }
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Contact form processing error: {e}")
            return Response(
                {
                    'success': False,
                    'message': 'An error occurred. Please try again.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )