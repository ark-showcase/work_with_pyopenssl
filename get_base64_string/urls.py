from django.urls import path

from .views import GetBase64String, ExtractText

urlpatterns = [
    path('', GetBase64String.as_view()),
    path('extract_text', ExtractText.as_view()),
]