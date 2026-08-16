from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Post, Comment, Follow


def home(request):
    posts = Post.objects.all().order_by('-created_at')

    if request.user.is_authenticated:
        following_users = Follow.objects.filter(
            follower=request.user
        ).values_list('following', flat=True)

        posts = posts.filter(user__in=list(following_users) + [request.user.id])

    return render(request, 'home.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(user=user)

        messages.success(request, 'Account created successfully.')
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def create_post(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.POST.get('image')

        if content:
            Post.objects.create(
                user=request.user,
                content=content,
                image=image
            )

        return redirect('home')

    return render(request, 'create_post.html')


def like_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('home')


def add_comment(request, post_id):
    if not request.user.is_authenticated:
        return redirect('login')

    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')

        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

    return redirect('home')


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-created_at')

    followers_count = Follow.objects.filter(
        following=user
    ).count()

    following_count = Follow.objects.filter(
        follower=user
    ).count()

    is_following = False

    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

    return render(request, 'profile.html', {
        'profile_user': user,
        'posts': posts,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following
    })


def follow_user(request, username):
    if not request.user.is_authenticated:
        return redirect('login')

    user_to_follow = get_object_or_404(User, username=username)

    if request.user != user_to_follow:
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following=user_to_follow
        )

        if not created:
            follow.delete()

    return redirect('profile', username=username)