from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .models import Certificate
from .forms import CertificateForm

@user_passes_test(lambda u: u.is_staff, login_url='login')
def certificate_list(request):
    certificates = Certificate.objects.all().order_by('-created_at')
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})

@user_passes_test(lambda u: u.is_staff, login_url='login')
def certificate_create(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            form.save()
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
            form.save()
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
