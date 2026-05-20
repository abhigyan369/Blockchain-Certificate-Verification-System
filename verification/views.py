from django.shortcuts import render
from blockchain.services import (
    BlockchainError,
    blockchain_is_configured,
    get_certificate_record,
    verify_certificate_hash as verify_blockchain_hash,
)
from certificates.models import Certificate
from certificates.hash_utils import generate_data_hash, verify_data_hash
from .forms import PublicVerificationForm
from .pdf_utils import (
    PDFVerificationError,
    extract_certificate_id_from_pdf,
    uploaded_pdf_matches_certificate,
)


def build_verification_context(certificate, uploaded_pdf_text=None):
    recalculated_hash = generate_data_hash(certificate)
    local_hash_valid = verify_data_hash(certificate, certificate.certificate_hash)
    pdf_content_valid = None
    blockchain_valid = None
    blockchain_record = None
    blockchain_error = None
    verification_source = "Database hash"

    if uploaded_pdf_text is not None:
        pdf_content_valid = uploaded_pdf_matches_certificate(
            uploaded_pdf_text,
            certificate,
        )

    if blockchain_is_configured():
        try:
            blockchain_valid = verify_blockchain_hash(
                str(certificate.certificate_id),
                recalculated_hash,
            )
            blockchain_record = get_certificate_record(str(certificate.certificate_id))
            verification_source = "Blockchain"
        except BlockchainError as exc:
            blockchain_error = str(exc)
            verification_source = "Database hash fallback"

    is_valid = local_hash_valid
    if blockchain_valid is not None:
        is_valid = is_valid and blockchain_valid
    if pdf_content_valid is not None:
        is_valid = is_valid and pdf_content_valid

    return {
        "certificate": certificate,
        "is_valid": is_valid,
        "result_status": "Valid" if is_valid else "Tampered",
        "local_hash_valid": local_hash_valid,
        "pdf_content_valid": pdf_content_valid,
        "blockchain_configured": blockchain_is_configured(),
        "blockchain_valid": blockchain_valid,
        "blockchain_record": blockchain_record,
        "blockchain_error": blockchain_error,
        "recalculated_hash": recalculated_hash,
        "verification_source": verification_source,
        "status": "Found",
    }


def public_verification(request):
    form = PublicVerificationForm(request.POST or None, request.FILES or None)
    context = {"form": form}

    if request.method == "POST" and form.is_valid():
        certificate_id = form.cleaned_data.get("certificate_id")
        uploaded_pdf = form.cleaned_data.get("certificate_pdf")
        uploaded_pdf_text = None

        if uploaded_pdf:
            try:
                certificate_id, uploaded_pdf_text = extract_certificate_id_from_pdf(
                    uploaded_pdf
                )
            except PDFVerificationError as exc:
                form.add_error("certificate_pdf", str(exc))
                return render(request, "verification/verify_form.html", context)

        try:
            certificate = Certificate.objects.get(certificate_id=certificate_id)
        except Certificate.DoesNotExist:
            context.update(
                {
                    "status": "Not Found",
                    "result_status": "Not Found",
                    "submitted_certificate_id": certificate_id,
                }
            )
            return render(request, "verification/verify.html", context)

        context.update(build_verification_context(certificate, uploaded_pdf_text))
        return render(request, "verification/verify.html", context)

    return render(request, "verification/verify_form.html", context)


def verify_certificate(request, certificate_id):
    try:
        certificate = Certificate.objects.get(certificate_id=certificate_id)
        context = build_verification_context(certificate)
    except Certificate.DoesNotExist:
        context = {
            "status": "Not Found",
            "result_status": "Not Found",
            "submitted_certificate_id": certificate_id,
        }
        
    return render(request, 'verification/verify.html', context)
