from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('', RedirectView.as_view(url='/upload/', permanent=False)),  # Redirect root URL to /upload/
    path('upload/', include('myapp.urls')),  # Include your app's URLs for upload
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
