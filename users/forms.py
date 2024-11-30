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
        fields = (
            'username', 'first_name', 'last_name', 'phone', 'email', 
            'profile_picture', 'languages_to_learn', 'languages_to_teach', 
            'password1', 'password2', 'about'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if self.errors.get(field_name):
                field.widget.attrs['class'] += ' is-invalid'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone


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
        fields = [
            'first_name', 'last_name', 'phone', 'email', 
            'profile_picture', 'languages_to_learn', 
            'languages_to_teach', 'about'
        ]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if CustomUser.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone
