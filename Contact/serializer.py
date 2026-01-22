from rest_framework import serializers
from .models import ContactInquiry

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = ['id', 'name', 'email', 'phone', 'message']
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'message': {'required': True, 'allow_blank': False},
        }
    
    def validate_email(self, value):
        """Ensure email is valid"""
        value = value.strip().lower()
        if not value:
            raise serializers.ValidationError("Email is required")
        return value
    
    def validate_message(self, value):
        """Ensure message has reasonable length"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Please provide more details in your message")
        if len(value) > 2000:
            raise serializers.ValidationError("Message is too long (max 2000 characters)")
        return value.strip()