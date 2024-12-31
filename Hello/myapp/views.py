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
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'  # Ensure this path is correct


def upload_document(request):
    extracted_text = ""
    if request.method == 'POST' and request.FILES.get('document'):
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = request.FILES['document']
            fs = FileSystemStorage()
            filename = fs.save(document.name, document)  # Save the uploaded document
            uploaded_file_url = fs.url(filename)

            try:
                # Process the uploaded image with OCR
                file_path = fs.path(filename)  # Get the saved file's path
                img = Image.open(file_path)  # Open the file from its saved path
                extracted_text = pytesseract.image_to_string(img)

                # Save the uploaded document and extracted text to the database
                UploadedDocument.objects.create(document=document, extracted_text=extracted_text)

                return render(request, 'myapp/upload.html', {  # Ensure the template path is correct
                    'uploaded_file_url': uploaded_file_url,
                    'extracted_text': extracted_text,
                })
            except Exception as e:
                logger.error(f"Error processing document with OCR: {e}")
                extracted_text = f"Error extracting text from document: {str(e)}"
        else:
            logger.warning("Form validation failed.")
    else:
        form = DocumentUploadForm()

    return render(request, 'myapp/upload.html', {'form': form, 'extracted_text': extracted_text})  # Ensure template path


def verify_aadhaar(request):
    if request.method == 'POST':
        aadhaar_number = request.POST.get('aadhaar_number')

        # Validate Aadhaar number format
        if not aadhaar_number or not aadhaar_number.isdigit() or len(aadhaar_number) != 12:
            return JsonResponse({'status': 'error', 'message': 'Invalid Aadhaar number format.'})

        try:
            # Query the User model for the provided Aadhaar number
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
