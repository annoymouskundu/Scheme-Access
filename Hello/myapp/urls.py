from django.urls import path
from .views import upload_document, verify_aadhaar  # Import the views

urlpatterns = [
    path('', upload_document, name='upload_document'),  # Handle requests to '/upload/' for document upload
    path('verify-aadhaar/', verify_aadhaar, name='verify_aadhaar'),  # Endpoint for Aadhaar verification
]
