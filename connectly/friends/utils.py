from .models import FriendRequest, Friend

def get_friendship_status(user1, user2):
    if Friend.objects.filter(user=user1, friend=user2).exists():
        return "friends"

    if FriendRequest.objects.filter(sender=user1, receiver=user2).exists():
        return "request_sent"

    if FriendRequest.objects.filter(sender=user2, receiver=user1).exists():
        return "request_received"

    return "none"

