import uuid
from django.db import models

class Certificate(models.Model):
    certificate_id = models.CharField(max_length=64, unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    student_name = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    issue_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='certificates/generated/', null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} - {self.course_name} ({self.certificate_id})"
