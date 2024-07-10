from django.urls import path
from .views import get_numbers

urlpatterns = [
    path('numbers/<str:qualified_id>/', get_numbers, name='get_numbers'),
]   