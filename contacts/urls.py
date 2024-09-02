# contacts/urls.py
from django.urls import path
from .views import search_users, send_friend_request, accept_friend_request
from . import views

urlpatterns = [
    path('search/', search_users, name='search_users'),
    path('send_request/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('accept_request/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('contacts/', views.contacts_list, name='contacts_list'),
    path('reject_friend_request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
]
