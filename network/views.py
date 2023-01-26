import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Post, User


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)  # type: ignore
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def index(request):
    """Display new post form if logged in and all posts

    Args:
        request (HttpRequest): Django request object

    Returns:
        HttpResponse: Rendered template output
    """

    return render(request, "network/index.html")


def view_profile(request, username):
    """Display user profile

    Includes:
        Number of followers
        Number of people followed
        All posts created by the user (reverse chronological)
        Follow / Unfollow button
            - Only when signed and and not self

    Args:
        request (HttpRequest): Django request object
        username (str): Username of active user
    """
    # Retrieve existing user to ensure it's valid
    user = User.objects.filter(username=username).first()

    if not user:
        messages.error(
            request,
            "<strong>Error:</strong>  The provided username does not exist or is no longer active!",
        )
        return HttpResponseRedirect(reverse("index"))

    return render(
        request,
        "network/profile.html",
        {
            "profile": user,
        },
    )


@login_required
def view_followed(request):
    """Display user's followed psots

    Args:
        request (HttpRequest): Django request object
    """
    return render(request, "network/following.html")


def view_posts(request):
    """View all posts

    Args:
        request (HttpRequest): Django request object
    """
    # Don't allow POST method as this is a data retrieval view
    if request.method == "POST":
        return JsonResponse({"error": "POST request not supported."}, status=400)

    page_number = int(request.GET.get("page_number", 1))

    posts = Post.objects.all().order_by("-created_at")

    paged_posts = Paginator(posts, 10)
    current_page = paged_posts.get_page(page_number)

    timezone = request.COOKIES.get("time_zone", None)

    return JsonResponse(
        {
            "posts": [post.serialize(request.user, timezone) for post in current_page],
            "page_current": page_number,
            "page_max": paged_posts.num_pages,
        }
        # safe=False,
    )


def view_filtered_posts(request, username):
    """View filtered posts

    Args:
        request (HttpRequest): Django request object
        username (str): Username of posts to return
    """
    # Don't allow POST method as this is a data retrieval view
    if request.method == "POST":
        return JsonResponse({"error": "POST request not supported."}, status=400)

    page_number = int(request.GET.get("page_number", 1))

    posts = Post.objects.filter(user__username=username).order_by("-created_at")

    paged_posts = Paginator(posts, 10)
    current_page = paged_posts.get_page(page_number)

    timezone = request.COOKIES.get("time_zone", None)

    return JsonResponse(
        {
            "posts": [post.serialize(request.user, timezone) for post in current_page],
            "page_current": page_number,
            "page_max": paged_posts.num_pages,
        }
        # safe=False,
    )


@login_required
def view_followed_posts(request, username):
    """Lists all the posts from users the current user follows

    Args:
        request (HttpRequest): Django request object
        username (str): Username of follower of posts to return (Not strictly necessary here)
    """
    # Don't allow POST method as this is a data retrieval view
    if request.method == "POST":
        return JsonResponse({"error": "POST request not supported."}, status=400)

    if not username == request.user.username:
        return JsonResponse(
            {"error": "Follower posts can only be displayed for original user."},
            status=400,
        )

    page_number = int(request.GET.get("page_number", 1))

    posts = Post.objects.filter(user__in=request.user.following.all()).order_by(
        "-created_at"
    )

    paged_posts = Paginator(posts, 10)
    current_page = paged_posts.get_page(page_number)

    timezone = request.COOKIES.get("time_zone", None)

    return JsonResponse(
        {
            "posts": [post.serialize(request.user, timezone) for post in current_page],
            "page_current": page_number,
            "page_max": paged_posts.num_pages,
        }
        # safe=False,
    )


@login_required
def create_post(request):
    """Create a new post by the current user

    Args:
        request (HttpRequest): Django request object
    """
    # Creating a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    text = data.get("post_content", "")

    if not text:
        return JsonResponse({"error": "Post content required."}, status=400)

    try:
        new_post = Post(text=text, user=request.user)
        new_post.save()
    except:
        return JsonResponse(
            {"error": "Post content experienced an error during save."}, status=400
        )

    return JsonResponse({"message": "Post created successfully."}, status=201)


@login_required
def edit_post(request, post_id):
    """Edit a post created by the post owner

    Args:
        request (HttpRequest): Django request object
        post_id (int): Primary key of the post to update
    """
    # Updating a post must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    post = Post.objects.filter(pk=post_id).first()

    if not post:
        return JsonResponse({"error": "Request post does not exist."}, status=400)

    if not post.user == request.user:
        return JsonResponse(
            {"error": "Post can only be updated by original user."}, status=400
        )

    data = json.loads(request.body)
    text = data.get("post_content", None)

    try:
        post.text = text
        post.save()
    except:
        return JsonResponse(
            {"error": "Post content experienced an error during save."}, status=400
        )

    return JsonResponse({"message": "Post updated successfully."}, status=201)


@login_required
def toggle_like(request, post_id):
    """Add or remove a like on an given post

    Args:
        request (HttpRequest): Django request object
        post_id (int): Primary key of the post to like
    """
    # Updating a posts like status must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    post = Post.objects.filter(pk=post_id).first()

    if not post:
        return JsonResponse({"error": "Unknown post."}, status=400)

    if not post.likes.filter(id=request.user.id).exists():
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)

    return JsonResponse({"message": "Like status updated successfully."}, status=201)


# @login_required - Can't use here due to supporting GET for non-authenticated users
def follow(request, username):
    """Provide follower information and toggle follower status

    Args:
        request (HttpRequest): Django request object
        username (str): Username of user to follow
    """
    user = User.objects.filter(username=username).first()

    if not user:
        return JsonResponse({"error": "Unknown user."}, status=400)

    # Updating follow status must be via POST
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User is not authenticated."}, status=401)

        if not user.followers.filter(username=request.user.username).exists():
            user.followers.add(request.user)
        else:
            user.followers.remove(request.user)

        return JsonResponse(
            {"message": "Follow status updated successfully."}, status=201
        )

    return JsonResponse(
        {
            "following": user.followers.filter(username=request.user.username).exists(),
            "countFollowers": user.followers.count(),
            "countFollowing": user.following.count(),
        }
    )
