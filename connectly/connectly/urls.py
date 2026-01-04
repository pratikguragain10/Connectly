from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("accounts/", include("allauth.urls")),

    # Profile pages
    path("profile/", include("accounts.urls")),

    # Home feed + posts
    path("", include("posts.urls")),

    # Friend system
    path("friends/", include("friends.urls")),
    
]
