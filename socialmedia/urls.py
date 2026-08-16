from django.contrib import admin
from django.urls import path
from social import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('create-post/', views.create_post, name='create_post'),

    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),

    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
]