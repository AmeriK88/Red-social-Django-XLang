from django.urls import path
from . import views
from .views import like_post, add_comment

urlpatterns = [
    path('post/create/', views.create_post, name='create_post'),
    path('post/edit/<int:pk>/', views.edit_post, name='edit_post'),
    path('post/delete/<int:pk>/', views.delete_post, name='delete_post'),
    path('posts/delete/<int:pk>/confirm/', views.confirm_delete_post, name='confirm_delete_post'),
    path('<int:pk>/like/', like_post, name='like_post'),
    path('<int:pk>/comment/', add_comment, name='add_comment'),
]
