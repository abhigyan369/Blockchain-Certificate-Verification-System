import io
from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from reportlab.pdfgen import canvas

from certificates.hash_utils import generate_data_hash
from certificates.models import Certificate


class PublicVerificationTests(TestCase):
    def setUp(self):
        self.certificate = Certificate.objects.create(
            student_name="Asha Rao",
            course_name="Blockchain Basics",
            issue_date=date(2026, 5, 20),
        )
        self.certificate.certificate_hash = generate_data_hash(self.certificate)
        self.certificate.save(update_fields=["certificate_hash"])

    def test_public_verification_page_loads(self):
        response = self.client.get(reverse("public_verification"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Verify Certificate")

    def test_certificate_id_verification_returns_valid_result(self):
        response = self.client.post(
            reverse("public_verification"),
            {"certificate_id": str(self.certificate.certificate_id)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Valid Certificate")
        self.assertContains(response, "Database hash")

    def test_unknown_certificate_id_returns_not_found(self):
        response = self.client.post(
            reverse("public_verification"),
            {"certificate_id": "missing-certificate"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Certificate Not Found")
        self.assertContains(response, "missing-certificate")

    def test_uploaded_pdf_verification_returns_valid_result(self):
        uploaded_pdf = SimpleUploadedFile(
            "certificate.pdf",
            self._build_certificate_pdf(),
            content_type="application/pdf",
        )

        response = self.client.post(
            reverse("public_verification"),
            {"certificate_pdf": uploaded_pdf},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Valid Certificate")
        self.assertContains(response, "Uploaded PDF Match")

    def _build_certificate_pdf(self):
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.drawString(72, 760, "Certificate of Completion")
        pdf.drawString(72, 730, self.certificate.student_name)
        pdf.drawString(72, 700, self.certificate.course_name)
        pdf.drawString(72, 670, "Issue Date: May 20, 2026")
        pdf.drawString(72, 640, f"Certificate ID: {self.certificate.certificate_id}")
        pdf.save()

        return buffer.getvalue()
