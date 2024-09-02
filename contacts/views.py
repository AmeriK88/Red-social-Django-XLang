from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import FriendshipRequest
from .forms import UserSearchForm
from django.contrib.auth import get_user_model
from django.db.models import Q

@login_required
def search_users(request):
    form = UserSearchForm(request.GET or None)
    users = form.search() if form.is_valid() else []
    return render(request, 'contacts/search.html', {'form': form, 'users': users})

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(get_user_model(), id=user_id)
    if to_user == request.user:
        return HttpResponseForbidden("You cannot send a friend request to yourself.")
    if not FriendshipRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        FriendshipRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('search_users')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendshipRequest, id=request_id, to_user=request.user)
    
    # Marcar la solicitud como aceptada
    friend_request.accepted = True
    friend_request.save()

    # Añadir a ambos usuarios como amigos
    request.user.friends.add(friend_request.from_user)
    friend_request.from_user.friends.add(request.user)
    
    # Redirigir al perfil del usuario que aceptó la solicitud
    return redirect('profile', username=request.user.username)

@login_required
def contacts_list(request):
    # Obtener los contactos aceptados del usuario
    contacts = FriendshipRequest.objects.filter(
        (Q(from_user=request.user) | Q(to_user=request.user)),
        accepted=True
    ).select_related('from_user', 'to_user')
    
    # Filtrar los contactos para excluir al usuario actual y organizar la lista
    user_contacts = []
    for contact in contacts:
        if contact.from_user != request.user:
            user_contacts.append(contact.from_user)
        else:
            user_contacts.append(contact.to_user)
    
    return render(request, 'contacts/contacts_list.html', {'contacts': user_contacts})

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendshipRequest, id=request_id)
    
    # Asegúrate de que solo la persona a la que se le envió la solicitud pueda rechazarla
    if friend_request.to_user == request.user:
        friend_request.delete()
    
    return redirect('profile', username=request.user.username)
