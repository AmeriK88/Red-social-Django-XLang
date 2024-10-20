from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True)
    about = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    languages_to_learn = models.CharField(max_length=255, blank=True)
    languages_to_teach = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True, null=True)
    friends = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_to')
    
    # related_name evita los conflictos con modelos existentes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )
    
    def __str__(self):
        return self.username
