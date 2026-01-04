from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_post, name="create_post"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),

    path("posts/<int:post_id>/like/", views.toggle_like, name="like_post"),

    # COMMENTS (AJAX)
    path("comment/add/<int:post_id>/", views.add_comment_ajax, name="add_comment_ajax"),
    path("comment/edit/<int:comment_id>/", views.edit_comment_ajax, name="edit_comment_ajax"),
    path("comment/delete/<int:comment_id>/", views.delete_comment_ajax, name="delete_comment_ajax"),
    path("comment-like/<int:comment_id>/", views.toggle_comment_like, name="comment_like"),
]