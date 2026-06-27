from rest_framework import serializers
from .models import *

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['about_me', 'profile_picture', 'group']
        read_only_fields = ['group']

class UpdateUserSerializer(serializers.Serializer):
    about_me = serializers.CharField()
    profile_picture = serializers.ImageField()

class Groupserializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__' 
        read_only_fields = ['creator']  

class EditGroupserializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__' 
        read_only_fields = ['creator', 'members']    

class OnlineUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['user', 'is_online']
