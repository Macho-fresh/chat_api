from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import User

class UserProfile(generics.ListCreateAPIView):
    serializer_class = ChatUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatUser.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateProfile(generics.GenericAPIView):
    serializer_class = ChatUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChatUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        chat_user = ChatUser.objects.get(user=request.user)
        chat_user.about_me = serializer.validated_data['about_me']
        chat_user.profile_picture = serializer.validated_data['profile_picture']
        chat_user.save()
 
        return Response({
    
            'message': 'profile updated successfully'
        })

class GroupCreateView(generics.ListCreateAPIView):
    serializer_class = Groupserializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Group.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class GroupView(generics.ListAPIView):
    serializer_class = Groupserializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Group.objects.all()        

class DeleteGroupMemberView(APIView):
    permission_classes = [permissions.IsAuthenticated]
   
    def get(self, request, id, user_id):
        group = Group.objects.get(id=id)

        if group.creator == request.user:

            group.members.remove(user_id)  
            group.save()  
            user = User.objects.get(id=user_id)
            return Response({
                "message": f'{user.username} has been removed from {group.group}'
            })
        return Response({
            'error': 'Only owners can remove users'
        })


class EditGroupView(generics.UpdateAPIView):
    serializer_class = EditGroupserializer  
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        return Group.objects.filter(creator=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user)
    
    def get(self, request, id):
        group = Group.objects.get(id=id, creator=request.user)
        serializer = Groupserializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        group.group = serializer.validated_data['group']
        group.save()
        
        return Response({
            'group': group.group
        })

class AddMemberView(APIView):
    def get(self, request, id, user_id):
        group = Group.objects.get(id=id)
        if group.creator == request.user:
            user = User.objects.get(id=user_id)
            group.members.add(user)
            group.save()
            return Response({
                 'message': f'{user.username} has been added to {group.group}'
             }, status=status.HTTP_202_ACCEPTED)
        return Response({
            'error': 'Only admins can add to group'
        })
    
class OnlineMembersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        users = ChatUser.objects.filter(is_online=True)
        serializer = OnlineUserSerializer(users, many=True)

        return Response({
            "online_users": serializer.data
        })