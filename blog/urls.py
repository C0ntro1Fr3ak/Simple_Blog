import profile

from django.urls import path, include
from blog.views import HomeView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, create_post, \
    likes_or_not, ProfileView, create_profile, load_user_from_file, register_user

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post_detail/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('post_delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('post_create_2/', create_post, name='post_create_function'),
    path('likes_or_not/', likes_or_not, name='likes_or_not'),
    path('user_profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('create_profile', create_profile, name='create_profile'),
    path('register/', register_user, name='register'),
    path('load_user_from_file/', load_user_from_file, name='load_user_from_file'),
]
