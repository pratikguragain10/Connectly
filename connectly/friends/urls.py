from django.urls import path
from . import views

urlpatterns = [
    path("send/<int:user_id>/", views.send_request, name="send_request"),
    path("cancel/<int:user_id>/", views.cancel_request, name="cancel_request"),
    path("accept/<int:request_id>/", views.accept_request, name="accept_request"),
    path("reject/<int:request_id>/", views.reject_request, name="reject_request"),
    path("remove/<int:user_id>/", views.remove_friend, name="remove_friend"),
    path("search/", views.user_search, name="user_search"),
]
