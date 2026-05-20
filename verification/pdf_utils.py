import re

from pypdf import PdfReader


CERTIFICATE_ID_PATTERN = re.compile(
    r"Certificate\s+ID:\s*([0-9a-fA-F-]{32,64})"
)
UUID_PATTERN = re.compile(
    r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"
)


class PDFVerificationError(Exception):
    """Raised when certificate details cannot be read from an uploaded PDF."""


def extract_text_from_pdf(uploaded_pdf):
    try:
        reader = PdfReader(uploaded_pdf)
    except Exception as exc:
        raise PDFVerificationError("The uploaded file could not be read as a PDF.") from exc

    page_text = []
    for page in reader.pages:
        page_text.append(page.extract_text() or "")

    text = "\n".join(page_text).strip()
    if not text:
        raise PDFVerificationError("No readable text was found in the PDF.")

    return text


def extract_certificate_id_from_pdf(uploaded_pdf):
    text = extract_text_from_pdf(uploaded_pdf)

    label_match = CERTIFICATE_ID_PATTERN.search(text)
    if label_match:
        return label_match.group(1), text

    uuid_match = UUID_PATTERN.search(text)
    if uuid_match:
        return uuid_match.group(0), text

    raise PDFVerificationError("No certificate ID was found in the uploaded PDF.")


def uploaded_pdf_matches_certificate(uploaded_pdf_text, certificate):
    issue_date = certificate.issue_date.strftime("%B %d, %Y")
    expected_values = [
        str(certificate.certificate_id),
        certificate.student_name,
        certificate.course_name,
        issue_date,
    ]

    return all(value in uploaded_pdf_text for value in expected_values)
