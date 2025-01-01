from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    demographic_details = models.TextField()  # You may want to structure this further

    def __str__(self):
        return self.name

class GovernmentScheme(models.Model):
    name = models.CharField(max_length=200)
    eligibility_criteria = models.JSONField()  # Changed to JSONField for structured data
    benefits = models.TextField()

    def __str__(self):
        return self.name

class UploadedDocument(models.Model):  # New model for uploaded documents
    document = models.FileField(upload_to='documents/')
    extracted_text = models.TextField(blank=True)  # Field to store extracted text

    def __str__(self):
        return self.document.name
