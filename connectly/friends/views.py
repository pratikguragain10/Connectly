from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from .models import FriendRequest, Friend


# ================= SEND FRIEND REQUEST =================
@login_required
@require_POST
def send_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    if receiver != request.user:
        FriendRequest.objects.get_or_create(
            sender=request.user,
            receiver=receiver
        )

    return JsonResponse({"status": "request_sent"})


# ================= CANCEL FRIEND REQUEST =================
@login_required
@require_POST
def cancel_request(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    FriendRequest.objects.filter(
        sender=request.user,
        receiver=receiver
    ).delete()

    return JsonResponse({"status": "cancelled"})


# ================= ACCEPT FRIEND REQUEST =================
@login_required
@require_POST
def accept_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id)

    # Create friendship both ways
    Friend.objects.get_or_create(user=fr.sender, friend=fr.receiver)
    Friend.objects.get_or_create(user=fr.receiver, friend=fr.sender)

    fr.delete()

    return JsonResponse({"status": "friends"})


# ================= REJECT FRIEND REQUEST =================
@login_required
@require_POST
def reject_request(request, request_id):
    FriendRequest.objects.filter(id=request_id).delete()
    return JsonResponse({"status": "rejected"})


# ================= REMOVE FRIEND =================
@login_required
@require_POST
def remove_friend(request, user_id):
    friend = get_object_or_404(User, id=user_id)

    Friend.objects.filter(user=request.user, friend=friend).delete()
    Friend.objects.filter(user=friend, friend=request.user).delete()

    return JsonResponse({"status": "removed"})


# ================= SEARCH USERS =================
@login_required
def user_search(request):
    query = request.GET.get("q", "")
    users = []

    if query:
        users = User.objects.filter(
            username__icontains=query
        ).exclude(id=request.user.id)

    return render(request, "friends/search.html", {
        "users": users,
        "query": query
    })
