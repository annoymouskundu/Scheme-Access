from django.shortcuts import render
from django.http import JsonResponse  # Import JsonResponse for the API response
import pytesseract
from .forms import DocumentUploadForm
from .models import UploadedDocument, User  # Import the new model for user details
from django.core.files.storage import FileSystemStorage
from PIL import Image
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Set the tesseract_cmd to the path where Tesseract is installed
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'  # Ensure this path is correct

def upload_document(request):
    extracted_text = ""
    if request.method == 'POST' and request.FILES.get('document'):
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = request.FILES['document']
            fs = FileSystemStorage()
            filename = fs.save(document.name, document)
            uploaded_file_url = fs.url(filename)

            try:
                # Process the uploaded image with OCR
                img = Image.open(document)
                extracted_text = pytesseract.image_to_string(img)

                # Save the uploaded document and extracted text to the database
                UploadedDocument.objects.create(document=document, extracted_text=extracted_text)

                return render(request, 'myapp/upload.html', {  # Updated path here
                    'uploaded_file_url': uploaded_file_url,
                    'extracted_text': extracted_text,
                })
            except Exception as e:
                logger.error(f"Error processing document with OCR: {e}")
                extracted_text = "Error extracting text from document."
        else:
            logger.warning("Form validation failed.")
    else:
        form = DocumentUploadForm()

    return render(request, 'myapp/upload.html', {'form': form, 'extracted_text': extracted_text})  # Updated path here


def verify_aadhaar(request):
    if request.method == 'POST':
        aadhaar_number = request.POST.get('aadhaar_number')
        try:
            user = User.objects.get(aadhaar_number=aadhaar_number)
            response_data = {
                'status': 'success',
                'message': 'Aadhaar verified successfully.',
                'user_details': {
                    'name': user.name,
                    'aadhaar_number': user.aadhaar_number,
                    'demographic_details': user.demographic_details,
                }
            }
        except User.DoesNotExist:
            response_data = {
                'status': 'error',
                'message': 'Aadhaar number not found.'
            }
        return JsonResponse(response_data)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
