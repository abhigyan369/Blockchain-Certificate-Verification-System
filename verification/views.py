from django.shortcuts import render
from certificates.models import Certificate
from certificates.hash_utils import verify_data_hash

def verify_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(certificate_id=certificate_id)
        # Verify the hash matches what is in the database
        is_valid = verify_data_hash(certificate, certificate.certificate_hash)
        
        context = {
            'certificate': certificate,
            'is_valid': is_valid,
            'status': 'Found'
        }
    except Certificate.DoesNotExist:
        context = {
            'status': 'Not Found'
        }
        
    return render(request, 'verification/verify.html', context)
