from django.db import models
from django.conf import settings

class Group(models.Model):
    group = models.CharField(max_length=150)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='creator')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')

class ChatUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    about_me = models.CharField(max_length=200)
    is_online = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_picture/')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)