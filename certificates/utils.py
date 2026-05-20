import io
import qrcode
from PIL import Image
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

def generate_certificate_pdf(certificate, base_url):
    """
    Generates a PDF certificate dynamically and returns a ContentFile.
    """
    buffer = io.BytesIO()
    
    # Create the PDF object, using a landscape A4 page
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Clean paper background with layered border.
    p.setFillColor(colors.HexColor("#ffffff"))
    p.rect(0, 0, width, height, fill=True, stroke=False)
    
    p.setStrokeColor(colors.HexColor("#173b67"))
    p.setLineWidth(7)
    p.rect(0.45 * inch, 0.45 * inch, width - 0.9 * inch, height - 0.9 * inch)

    p.setStrokeColor(colors.HexColor("#0f766e"))
    p.setLineWidth(1.5)
    p.rect(0.72 * inch, 0.72 * inch, width - 1.44 * inch, height - 1.44 * inch)

    # Header
    p.setFillColor(colors.HexColor("#173b67"))
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width / 2.0, height - 1.15 * inch, "CERTIVERIFY")

    p.setStrokeColor(colors.HexColor("#0f766e"))
    p.line(width / 2.0 - 1.4 * inch, height - 1.32 * inch, width / 2.0 + 1.4 * inch, height - 1.32 * inch)

    # Title
    p.setFillColor(colors.HexColor("#173b67"))
    p.setFont("Helvetica-Bold", 34)
    p.drawCentredString(width / 2.0, height - 1.9 * inch, "Certificate of Completion")
    
    # Subtitle
    p.setFillColor(colors.HexColor("#344054"))
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2.0, height - 2.9 * inch, "This is to certify that")
    
    # Student Name
    p.setFillColor(colors.HexColor("#101828"))
    p.setFont("Helvetica-Bold", 28)
    p.drawCentredString(width / 2.0, height - 3.75 * inch, certificate.student_name)

    p.setStrokeColor(colors.HexColor("#d0d5dd"))
    p.setLineWidth(1)
    p.line(width / 2.0 - 2.3 * inch, height - 3.95 * inch, width / 2.0 + 2.3 * inch, height - 3.95 * inch)
    
    # Course
    p.setFillColor(colors.HexColor("#344054"))
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2.0, height - 4.75 * inch, "has successfully completed the course")
    
    p.setFillColor(colors.HexColor("#173b67"))
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width / 2.0, height - 5.28 * inch, certificate.course_name)
    
    # Issue Date
    p.setFillColor(colors.HexColor("#344054"))
    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2.0, height - 6.2 * inch, f"Issue Date: {certificate.issue_date.strftime('%B %d, %Y')}")

    # Seal
    seal_x = width - 2.0 * inch
    seal_y = 1.75 * inch
    p.setStrokeColor(colors.HexColor("#0f766e"))
    p.setFillColor(colors.HexColor("#eef9f6"))
    p.circle(seal_x, seal_y, 0.55 * inch, stroke=True, fill=True)
    p.setFillColor(colors.HexColor("#0f766e"))
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(seal_x, seal_y + 0.08 * inch, "VERIFIED")
    p.setFont("Helvetica", 8)
    p.drawCentredString(seal_x, seal_y - 0.12 * inch, "DIGITAL RECORD")
    
    # Certificate ID
    p.setFillColor(colors.HexColor("#475467"))
    p.setFont("Helvetica", 10)
    p.drawRightString(width - 1 * inch, 0.95 * inch, f"Certificate ID: {certificate.certificate_id}")
    
    # QR Code (bottom left)
    qr_url = f"{base_url}/verify/{certificate.certificate_id}/"
    qr = qrcode.make(qr_url)
    qr_io = io.BytesIO()
    qr.save(qr_io, format='PNG')
    qr_io.seek(0)
    
    qr_image = ImageReader(qr_io)
    p.drawImage(qr_image, 1 * inch, 0.95 * inch, width=1.25 * inch, height=1.25 * inch)
    p.setFillColor(colors.HexColor("#475467"))
    p.setFont("Helvetica", 8)
    p.drawString(1 * inch, 0.75 * inch, "Scan to verify")
    
    # Save the PDF
    p.showPage()
    p.save()
    
    # Get the value of the BytesIO buffer and return it as a ContentFile
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return ContentFile(pdf_bytes, name=f"{certificate.certificate_id}.pdf")
