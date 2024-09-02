from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from django.http import HttpResponseForbidden
from .models import CustomUser
from contacts.models import FriendshipRequest
from posts.models import Post


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            print(f"User {user.username} registered successfully.")
            login(request, user)  # Auto-login the user after registration
            return redirect('home')
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user) 
            return redirect('home')  # Asegúrate de que 'home' es el nombre de la vista correcta
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required
def home(request):
    user = request.user
    user_posts = Post.objects.filter(user=user)
    friends = user.friends.all()
    friend_posts = Post.objects.filter(user__in=friends)
    posts = user_posts | friend_posts
    posts = posts.order_by('-created_at')
    return render(request, 'users/home.html', {'posts': posts})


@login_required
def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    
    # Solo mostrar las solicitudes de amistad si el usuario está viendo su propio perfil
    pending_requests = None
    if user == request.user:
        pending_requests = FriendshipRequest.objects.filter(to_user=request.user, accepted=False)
    
    posts = Post.objects.filter(user=user)  # Ejemplo de obtención de publicaciones
    
    context = {
        'user': user,
        'pending_requests': pending_requests,
        'posts': posts,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    # Verifica si el usuario actual es el propietario del perfil
    if request.user != user:
        return HttpResponseForbidden("You are not allowed to edit this profile.")
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'users/edit_profile.html', {'form': form, 'user': user})






