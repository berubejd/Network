from django.contrib import admin
from network.models import User, Post


# Register your models here.

# class FollowersInline(admin.StackedInline):
#     model = User.followers.through
#     fk_name = "from_user"


class LikesInline(admin.StackedInline):
    model = Post.likes.through


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
    )
    # inlines = [
    #     FollowersInline,
    #     LikesInline,
    # ]
    inlines = [
        LikesInline,
    ]
    exclude = ("followers", "following")


admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "text",
        "user",
        "created_at",
        "updated_at",
    )
    inlines = [
        LikesInline,
    ]
    readonly_fields = ("created_at", "updated_at")
    exclude = ("likes",)


admin.site.register(Post, PostAdmin)
