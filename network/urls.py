from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.create_post, name="create_post"),
    path("post/<int:post_id>", views.edit_post, name="edit_post"),
    path("posts", views.view_posts, name="view_posts"),
    path("posts/<str:username>", views.view_filtered_posts, name="filter_posts"),
    path(
        "posts/<str:username>/following",
        views.view_followed_posts,
        name="followed_posts",
    ),
    path("profile/<str:username>", views.view_profile, name="view_profile"),
    path("like/<int:post_id>", views.toggle_like, name="toggle_like"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("followed", views.view_followed, name="view_followed"),
]
