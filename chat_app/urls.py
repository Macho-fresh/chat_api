from django.urls import path
from .views import *

urlpatterns=[
    path('profile/', UserProfile.as_view()),
    path('update-profile/', UpdateProfile.as_view()),
    path('view-group/', GroupView.as_view()),

    path('create-group/', GroupCreateView.as_view()),
    path('delete-group-member/<int:id>/<int:user_id>', DeleteGroupMemberView.as_view()),
    path('edit-group-name/<int:id>/', EditGroupView.as_view()),
    path('add-to-group/<int:id>/<int:user_id>', AddMemberView.as_view()),
    path('online/', OnlineMembersView.as_view()),

]