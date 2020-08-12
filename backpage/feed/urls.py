from django.urls import path

from . import views

app_name = 'feed'
urlpatterns = [
    path('', views.feed, name='feed'),
    path('post/', views.feed),  # redirect to the feed
    path('post/<int:post_id>/a', views.post_api, name='post_api'),
    path('user/<int:user_id>/', views.user_profile, name='user_profile')
]
