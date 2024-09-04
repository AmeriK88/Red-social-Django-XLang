from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FriendshipRequest
from .forms import UserSearchForm
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages


@login_required
def search_users(request):
    form = UserSearchForm(request.GET or None)
    users = form.search() if form.is_valid() else []
    return render(request, 'contacts/search.html', {'form': form, 'users': users})

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(get_user_model(), id=user_id)
    
    if to_user == request.user:
        messages.error(request, "You cannot send a friend request to yourself.")
        return redirect('search_users')
    
    # Verificar si ya son amigos
    if request.user.friends.filter(id=to_user.id).exists():
        messages.warning(request, "You are already friends with this user.")
        return redirect('search_users')
    
    # Verificar si ya existe una solicitud de amistad en cualquier dirección
    if FriendshipRequest.objects.filter(
        Q(from_user=request.user, to_user=to_user) | 
        Q(from_user=to_user, to_user=request.user)
    ).exists():
        messages.warning(request, "A friend request already exists between you and this user.")
    else:
        FriendshipRequest.objects.create(from_user=request.user, to_user=to_user)
        messages.success(request, f"Friend request sent to {to_user.username}!")
    
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
    user_contacts = request.user.friends.all()
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
    
    # Asegurar que la persona que se envió solicitud pueda rechazarla
    if friend_request.to_user == request.user:
        friend_request.delete()
    
    return redirect('profile', username=request.user.username)

@login_required
def remove_contact(request, contact_id):
    return redirect('confirm_remove_contact', contact_id=contact_id)


@login_required
def confirm_remove_contact(request, contact_id):
    contact = get_object_or_404(get_user_model(), id=contact_id)
    
    # Verifica si el contacto es realmente un amigo
    if contact not in request.user.friends.all():
        messages.error(request, f"{contact.username} is not in your contacts.")
        return redirect('contacts_list')
    
    if request.method == 'POST':
        # Elimina el contacto y las solicitudes de amistad
        request.user.friends.remove(contact)
        contact.friends.remove(request.user)
        
        FriendshipRequest.objects.filter(
            (Q(from_user=request.user, to_user=contact) | Q(from_user=contact, to_user=request.user))
        ).delete()
        
        messages.success(request, f"{contact.username} has been removed from your contacts.")
        return redirect('contacts_list')
    
    return render(request, 'contacts/confirm_remove_contact.html', {'contact': contact})
