# Backend/context_processors.py
from django.conf import settings

def company_info(request):
    """Make company information available in all templates"""
    return {
        'company_name': getattr(settings, 'COMPANY_NAME', 'OFORITECH SOLUTIONS'),
        'company_phone': getattr(settings, 'COMPANY_PHONE', ''),
        'company_email': getattr(settings, 'COMPANY_EMAIL', ''),
        'company_website': getattr(settings, 'COMPANY_WEBSITE', ''),
        'company_address': getattr(settings, 'COMPANY_ADDRESS', ''),
    }