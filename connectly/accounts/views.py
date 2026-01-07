from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Profile
from posts.models import Post
from friends.utils import get_friendship_status
from friends.models import FriendRequest, Friend


# PROFILE VIEW
@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    is_owner = request.user == user
    friendship_status = None
    received_request = None

    friends = Friend.objects.filter(user=user)

    if not is_owner:
        friendship_status = get_friendship_status(request.user, user)

        if friendship_status == "request_received":
            received_request = FriendRequest.objects.filter(
                sender=user,
                receiver=request.user
            ).first()

    # POSTS + COMMENTS + REPLIES (CORRECT WAY)
    posts = (
        Post.objects
        .filter(user=user)
        .select_related("user")
        .prefetch_related(
            "likes",
            "comments__user",
            "comments__likes",
            "comments__replies__user",
            "comments__replies__likes",
        )
        .order_by("-created_at")
    )

    # PREPARE DATA FOR TEMPLATE
    for post in posts:
        post.liked = post.likes.filter(user=request.user).exists()

        # ROOT COMMENTS ONLY (no parent)
        post.root_comments = post.comments.filter(parent__isnull=True)

        for comment in post.comments.all():
            comment.liked = comment.likes.filter(user=request.user).exists()

            for reply in comment.replies.all():
                reply.liked = reply.likes.filter(user=request.user).exists()

    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "posts": posts,
            "is_owner": is_owner,
            "friendship_status": friendship_status,
            "received_request": received_request,
            "friends": friends,
            "friends_count": friends.count(),
            "is_profile_page": True,   # IMPORTANT for base.html
        }
    )

# EDIT PROFILE
@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        profile.bio = request.POST.get("bio")
        profile.work = request.POST.get("work")
        profile.education = request.POST.get("education")
        profile.location = request.POST.get("location")

        if "profile_pic" in request.FILES:
            profile.profile_pic = request.FILES["profile_pic"]

        if "cover_photo" in request.FILES:
            profile.cover_photo = request.FILES["cover_photo"]

        profile.save()
        return redirect("profile", username=request.user.username)

    return render(request, "account/edit_profile.html", {"profile": profile})
