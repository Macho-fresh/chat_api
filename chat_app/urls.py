from django.urls import path
from .views import *

urlpatterns=[
    path('profile/', UserProfile.as_view())
]