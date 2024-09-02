from django.contrib import admin
from .models import FriendshipRequest

@admin.register(FriendshipRequest)
class FriendshipRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at', 'accepted')
    search_fields = ('from_user__username', 'to_user__username')
    list_filter = ('accepted', 'created_at')