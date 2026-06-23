from rest_framework import serializers
from .models import *

class ChatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ['about_me', 'profile_picture', 'group']
        read_only_fields = ['group']