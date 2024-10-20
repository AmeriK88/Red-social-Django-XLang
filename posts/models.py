from django.db import models
from django.conf import settings

# Modelo para representar un post en la plataforma
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    title = models.CharField(max_length=100)  
    content = models.TextField() 
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  
    link = models.URLField(max_length=200, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)  

    def __str__(self):
        return self.title

    # Devuelve el total de likes que tiene el post
    def total_likes(self):
        return self.likes.count()

# Modelo para representar los comentarios de un post
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

# Modelo para representar solicitudes de amistad entre usuarios
class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendship_requests_sent', on_delete=models.CASCADE)  
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friendship_requests_received', on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True) 
    accepted = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.from_user} to {self.to_user}"
