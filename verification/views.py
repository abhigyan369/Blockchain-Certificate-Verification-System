from django.shortcuts import render
from blockchain.services import (
    BlockchainError,
    blockchain_is_configured,
    get_certificate_record,
    verify_certificate_hash as verify_blockchain_hash,
)
from certificates.models import Certificate
from certificates.hash_utils import generate_data_hash, verify_data_hash

def verify_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(certificate_id=certificate_id)
        recalculated_hash = generate_data_hash(certificate)
        local_hash_valid = verify_data_hash(certificate, certificate.certificate_hash)
        blockchain_valid = None
        blockchain_record = None
        blockchain_error = None
        verification_source = 'Database hash'

        if blockchain_is_configured():
            try:
                blockchain_valid = verify_blockchain_hash(
                    str(certificate.certificate_id),
                    recalculated_hash,
                )
                blockchain_record = get_certificate_record(str(certificate.certificate_id))
                verification_source = 'Blockchain'
            except BlockchainError as exc:
                blockchain_error = str(exc)
                verification_source = 'Database hash fallback'
        
        context = {
            'certificate': certificate,
            'is_valid': (
                local_hash_valid
                if blockchain_valid is None
                else local_hash_valid and blockchain_valid
            ),
            'local_hash_valid': local_hash_valid,
            'blockchain_configured': blockchain_is_configured(),
            'blockchain_valid': blockchain_valid,
            'blockchain_record': blockchain_record,
            'blockchain_error': blockchain_error,
            'recalculated_hash': recalculated_hash,
            'verification_source': verification_source,
            'status': 'Found'
        }
    except Certificate.DoesNotExist:
        context = {
            'status': 'Not Found'
        }
        
    return render(request, 'verification/verify.html', context)
