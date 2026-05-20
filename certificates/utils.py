import io
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
from reportlab.lib import colors

def generate_certificate_pdf(certificate):
    """
    Generates a PDF certificate dynamically and returns a ContentFile.
    """
    buffer = io.BytesIO()
    
    # Create the PDF object, using a landscape A4 page
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Background color and border
    p.setFillColor(colors.HexColor("#fdfdfd"))
    p.rect(0, 0, width, height, fill=True, stroke=False)
    
    p.setStrokeColor(colors.HexColor("#1b4b79"))
    p.setLineWidth(10)
    p.rect(0.5 * inch, 0.5 * inch, width - 1 * inch, height - 1 * inch)

    # Title
    p.setFillColor(colors.HexColor("#1b4b79"))
    p.setFont("Helvetica-Bold", 36)
    p.drawCentredString(width / 2.0, height - 2 * inch, "Certificate of Completion")
    
    # Subtitle
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2.0, height - 3 * inch, "This is to certify that")
    
    # Student Name
    p.setFont("Helvetica-Bold", 28)
    p.drawCentredString(width / 2.0, height - 4 * inch, certificate.student_name)
    
    # Course
    p.setFont("Helvetica", 18)
    p.drawCentredString(width / 2.0, height - 5 * inch, f"has successfully completed the course:")
    
    p.setFont("Helvetica-Bold", 22)
    p.drawCentredString(width / 2.0, height - 5.5 * inch, certificate.course_name)
    
    # Issue Date
    p.setFont("Helvetica", 14)
    p.drawCentredString(width / 2.0, height - 6.5 * inch, f"Issue Date: {certificate.issue_date.strftime('%B %d, %Y')}")
    
    # Certificate ID (bottom right)
    p.setFont("Helvetica", 10)
    p.drawRightString(width - 1 * inch, 0.8 * inch, f"Certificate ID: {certificate.certificate_id}")
    
    # Save the PDF
    p.showPage()
    p.save()
    
    # Get the value of the BytesIO buffer and return it as a ContentFile
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return ContentFile(pdf_bytes, name=f"{certificate.certificate_id}.pdf")
