from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    work = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)

    profile_pic = CloudinaryField(
        'image',
        blank=True,
        null=True,
        default='https://res.cloudinary.com/demo/image/upload/v1690000000/default-avatar.png'
    )
    cover_photo = CloudinaryField(
        'image',
        blank=True,
        null=True,
        default='https://res.cloudinary.com/demo/image/upload/v1690000000/default-cover.jpg'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username