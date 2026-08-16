from django.contrib import admin
from .models import Profile, Post, Comment, Follow


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    list_filter = ('created_at',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')