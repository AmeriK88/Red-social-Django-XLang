# contacts/forms.py
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSearchForm(forms.Form):
    username = forms.CharField(max_length=150, required=False, label='Search by username')
    
    def search(self):
        query = self.cleaned_data.get('username')
        if query:
            return User.objects.filter(username__icontains=query)
        return User.objects.none()
