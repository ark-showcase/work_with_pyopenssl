from django.urls import path

from .views import GetBase64String, ExtractText, Read_from_b64

urlpatterns = [
    path('', GetBase64String.as_view()),
    path('extract_text', ExtractText.as_view()),
    path('get_text_from_b64/', Read_from_b64.as_view(), name='get_text_from_b64'),
]