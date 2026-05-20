from django import forms


class PublicVerificationForm(forms.Form):
    certificate_id = forms.CharField(
        label="Certificate ID",
        required=False,
        max_length=64,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter certificate ID",
            }
        ),
    )
    certificate_pdf = forms.FileField(
        label="Certificate PDF",
        required=False,
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control",
                "accept": "application/pdf",
            }
        ),
    )

    def clean_certificate_pdf(self):
        certificate_pdf = self.cleaned_data.get("certificate_pdf")

        if not certificate_pdf:
            return certificate_pdf

        if certificate_pdf.content_type != "application/pdf":
            raise forms.ValidationError("Upload a PDF certificate file.")

        return certificate_pdf

    def clean(self):
        cleaned_data = super().clean()
        certificate_id = cleaned_data.get("certificate_id")
        certificate_pdf = cleaned_data.get("certificate_pdf")

        if not certificate_id and not certificate_pdf:
            raise forms.ValidationError(
                "Enter a certificate ID or upload a certificate PDF."
            )

        return cleaned_data
