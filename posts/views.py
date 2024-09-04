from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib import messages

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an error creating your post. Please try again.")
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was an error updating your post. Please try again.")
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})


@login_required
def delete_post(request, pk):
    return redirect('confirm_delete_post', pk=pk)


@login_required
def confirm_delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Verifica si el usuario tiene permiso para eliminar la publicación
    if post.user != request.user:
        messages.error(request, "You do not have permission to delete this post.")
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('home')
    
    return render(request, 'posts/confirm_delete_post.html', {'post': post})

