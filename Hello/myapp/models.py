from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    aadhaar_number = models.CharField(max_length=12, unique=True)
    demographic_details = models.TextField()

class GovernmentScheme(models.Model):
    name = models.CharField(max_length=200)
    eligibility_criteria = models.TextField()
    benefits = models.TextField()

class UploadedDocument(models.Model):  # New model for uploaded documents
    document = models.FileField(upload_to='documents/')
    extracted_text = models.TextField(blank=True)  # Field to store extracted text
