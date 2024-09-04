from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm
from django.http import HttpResponseForbidden
from .models import CustomUser
from contacts.models import FriendshipRequest
from posts.models import Post
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome, {}!".format(user.username))
            return redirect('home')
        else:
            messages.error(request, "There was an error with your registration. Please check the form and try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "Welcome back, {}!".format(user.username))
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
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
    pending_requests = None

    if user == request.user:
        pending_requests = FriendshipRequest.objects.filter(to_user=request.user, accepted=False)
        if pending_requests.exists():
            messages.info(request, f"You have {pending_requests.count()} pending friend requests.")

    posts = Post.objects.filter(user=user)

    # Añadir un atributo 'user_has_liked' a cada post en la lista de posts
    for post in posts:
        post.user_has_liked = post.likes.filter(id=request.user.id).exists()

    context = {
        'user': user,
        'pending_requests': pending_requests,
        'posts': posts,
    }
    
    return render(request, 'users/profile.html', context)



@login_required
def edit_profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    if request.user != user:
        messages.error(request, "You are not allowed to edit this profile.")
        return HttpResponseForbidden("You are not allowed to edit this profile.")
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile', username=user.username)
        else:
            messages.error(request, "There was an error updating your profile. Please try again.")
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'users/edit_profile.html', {'form': form, 'user': user})

