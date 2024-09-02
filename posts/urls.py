from django.urls import path
from . import views

urlpatterns = [
    path('post/create/', views.create_post, name='create_post'),
    path('post/edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('post/delete/<int:pk>/', views.delete_post, name='delete_post'),
]
