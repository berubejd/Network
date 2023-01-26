from django.contrib.auth.models import AbstractUser
from django.db import models
from network.templatetags import berube_tags
from pytz import timezone


class User(AbstractUser):
    # Existing fields: "id", "username", "first_name", "last_name", "email",

    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following"
    )
    photo_url = models.URLField(blank=True, help_text="A URL for the user's photo")


class Post(models.Model):
    text = models.TextField(
        help_text="Post content",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        help_text="Related user",
    )
    likes = models.ManyToManyField(
        User,
        related_name="likes",
        help_text="Users who liked this post",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Post creation timestamp",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Post last update timestamp",
    )

    def __str__(self):
        return f"{self.user} ({self.created_at}): {self.text}"

    def serialize(self, user, tz=None):
        format = "%b %e, %Y @ %-I:%M %P"

        if tz:
            timestamp = self.created_at.astimezone(timezone(tz))
        else:
            timestamp = self.created_at

        return {
            "id": self.id,  # type: ignore
            "text": self.text,
            "user": self.user.username,
            "userphoto": self.user.photo_url,
            "likes": self.likes.filter(id=user.id).exists(),
            "likecount": self.likes.count(),
            "timestamp": berube_tags.nt_plus(timestamp, format),
            "edited": self.created_at.isoformat(" ", "seconds")
            != self.updated_at.isoformat(" ", "seconds"),
            "editable": self.user == user,
        }
