from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics, permissions

class UserProfile(generics.ListCreateAPIView):
    serializer_class = ChatUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = []
    queryset = ChatUser.objects.all()