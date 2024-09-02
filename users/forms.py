from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    languages_to_learn = forms.CharField(max_length=255, required=False)
    languages_to_teach = forms.CharField(max_length=255, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'profile_picture', 'languages_to_learn', 'languages_to_teach', 'password1', 'password2', 'about')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254, 
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username in ['admin', 'root']:
            raise ValidationError("Este nombre de usuario está reservado. Por favor, elige otro.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes añadir validaciones adicionales si es necesario
        return cleaned_data

class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    profile_picture = forms.ImageField(required=False)
    languages_to_learn = forms.CharField(max_length=255, required=False)
    languages_to_teach = forms.CharField(max_length=255, required=False)
    about = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone', 'email', 'profile_picture', 'languages_to_learn', 'languages_to_teach', 'about']