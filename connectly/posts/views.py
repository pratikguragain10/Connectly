from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.db.models import Q
from .models import Post, Like, Comment, CommentLike
from friends.models import Friend

@login_required
def home(request):
    friends = Friend.objects.filter(
        user=request.user
    ).values_list("friend", flat=True)

    posts = (
        Post.objects
        .filter(Q(user=request.user) | Q(user__in=friends))
        .select_related("user")
        .prefetch_related(
            "comments__user",
            "comments__likes",
            "comments__replies__user",
            "comments__replies__likes",
        )
        .order_by("-created_at")
    )

    for post in posts:
        post.liked = post.likes.filter(user=request.user).exists()
        post.root_comments = post.comments.filter(parent__isnull=True)

        for comment in post.comments.all():
            comment.liked = comment.likes.filter(user=request.user).exists()
            for reply in comment.replies.all():
                reply.liked = reply.likes.filter(user=request.user).exists()

    return render(request, "home.html", {"posts": posts})

@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get("content", "").strip()
        image = request.FILES.get("image")
        video = request.FILES.get("video")

        if content or image or video:
            Post.objects.create(
                user=request.user,
                content=content,
                image=image,
                video=video,
            )
    return redirect("home")


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return HttpResponseForbidden("You cannot edit this post")

    if request.method == "POST":
        post.content = request.POST.get("content", "").strip()

        # OPTIONAL replace media
        if request.FILES.get("image"):
            post.image = request.FILES.get("image")

        if request.FILES.get("video"):
            post.video = request.FILES.get("video")

        post.save()
        return redirect("home")

    return render(request, "edit_post.html", {"post": post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        return HttpResponseForbidden("You cannot delete this post")

    post.delete()
    return redirect("home")


@login_required
def toggle_like(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if created:
        liked = True
    else:
        like.delete()
        liked = False

    return JsonResponse({
        "liked": liked,
        "likes_count": post.likes.count()
    })

@login_required
def add_comment_ajax(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid"}, status=400)

    post = get_object_or_404(Post, id=post_id)
    content = request.POST.get("content", "").strip()
    parent_id = request.POST.get("parent")

    if not content:
        return JsonResponse({"error": "Empty"}, status=400)

    parent = None
    if parent_id:
        parent = get_object_or_404(Comment, id=parent_id)

    comment = Comment.objects.create(
        user=request.user,
        post=post,
        content=content,
        parent=parent
    )

    return render(
        request,
        "partials/comment.html",
        {"comment": comment, "post": post, "level": 0},
    )
    
@login_required
def edit_comment_ajax(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({"error": "Forbidden"}, status=403)

    content = request.POST.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "Empty"}, status=400)

    comment.content = content
    comment.save()

    return JsonResponse({"content": comment.content})

@login_required
def delete_comment_ajax(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return JsonResponse({"error": "Forbidden"}, status=403)

    comment.delete()
    return JsonResponse({"deleted": True})


@login_required
def toggle_comment_like(request, comment_id):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": comment.likes.count()
    })