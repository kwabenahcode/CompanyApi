# contact/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import threading
import logging

from .models import ContactInquiry
from .serializer import ContactSerializer
from .emails import EmailService

logger = logging.getLogger(__name__)

class ContactCreateView(generics.GenericAPIView):
    """
    Simple contact form API endpoint
    Returns success immediately, sends emails in background
    """
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
            
            # Prepare data for response
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
            
            # Send response immediately
            response = Response(response_data, status=status.HTTP_201_CREATED)
            
            # Prepare data for background email sending
            contact_data = {
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone or '',
                'message': contact.message,
                'created_at': contact.created_at,
            }
            
            # Send emails in background thread (won't block response)
            def send_emails_background():
                try:
                    # Send notification to company
                    EmailService.send_contact_notification(contact_data)
                    # Send auto-reply to client
                    EmailService.send_autoreply_to_client(contact_data)
                    logger.info(f"Emails sent for contact ID: {contact.id}")
                except Exception as e:
                    logger.error(f"Background email error: {e}")
                    # Continue even if emails fail
            
            # Start background thread
            email_thread = threading.Thread(target=send_emails_background)
            email_thread.daemon = True  # Thread won't block process exit
            email_thread.start()
            
            return response
            
        except Exception as e:
            logger.error(f"Contact form processing error: {e}")
            return Response(
                {
                    'success': False,
                    'message': 'An error occurred. Please try again.',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )