from django.urls import path
from .views import get_response

urlpatterns = [
    path('chat/', get_response, name='chatbot'),
]
