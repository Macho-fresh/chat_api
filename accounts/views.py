from django.shortcuts import render
from .models import User
from .serializer import *
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import login, authenticate

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'User already exists'
            })
        User.objects.create_user(
            username = username,
            email = email,
            password = password
        )

        return Response({
            'message': 'User created successfully'
        })

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []      

    def post(self, request):
        serializer = LoginSerializer(data=request.data) 

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            ) 

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        if User.objects.filter(username=username).exists():
           user = authenticate(request, username=username, password=password)
        else:
            return Response({
                'error': 'user does not exist'
            })
        
        login(request, user)
        return Response({
            'message': f'welcome {user.username}'
        })