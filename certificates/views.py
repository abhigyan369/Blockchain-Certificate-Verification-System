from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Certificate
from .forms import CertificateForm
from .utils import generate_certificate_pdf
from .hash_utils import generate_data_hash

@user_passes_test(lambda u: u.is_staff, login_url='login')
def certificate_list(request):
    certificates = Certificate.objects.all().order_by('-created_at')
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def certificate_create(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save()
            
            # Generate Hash
            certificate.certificate_hash = generate_data_hash(certificate)
            certificate.save(update_fields=['certificate_hash'])
            
            # Generate and save PDF
            base_url = request.build_absolute_uri('/')[:-1]
            pdf_file = generate_certificate_pdf(certificate, base_url)
            certificate.pdf_file.save(f"{certificate.certificate_id}.pdf", pdf_file, save=True)
            
            messages.success(request, 'Certificate issued successfully.')
            return redirect('certificate_list')
    else:
        form = CertificateForm()
    return render(request, 'certificates/certificate_form.html', {'form': form, 'action': 'Issue'})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def certificate_update(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id)
    if request.method == 'POST':
        form = CertificateForm(request.POST, instance=certificate)
        if form.is_valid():
            certificate = form.save()
            
            # Regenerate Hash
            certificate.certificate_hash = generate_data_hash(certificate)
            certificate.save(update_fields=['certificate_hash'])
            
            # Regenerate PDF
            base_url = request.build_absolute_uri('/')[:-1]
            pdf_file = generate_certificate_pdf(certificate, base_url)
            certificate.pdf_file.save(f"{certificate.certificate_id}.pdf", pdf_file, save=True)
            
            messages.success(request, 'Certificate updated successfully.')
            return redirect('certificate_list')
    else:
        form = CertificateForm(instance=certificate)
    return render(request, 'certificates/certificate_form.html', {'form': form, 'action': 'Update'})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def certificate_delete(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id)
    if request.method == 'POST':
        certificate.delete()
        messages.success(request, 'Certificate deleted successfully.')
        return redirect('certificate_list')
    return render(request, 'certificates/certificate_confirm_delete.html', {'certificate': certificate})

def certificate_download(request, certificate_id):
    certificate = get_object_or_404(Certificate, certificate_id=certificate_id)
    if certificate.pdf_file:
        return FileResponse(certificate.pdf_file.open('rb'), as_attachment=True, filename=f"Certificate_{certificate.student_name}.pdf")
    else:
        raise Http404("Certificate PDF not found.")
