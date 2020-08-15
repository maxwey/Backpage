from django.urls import path

from . import views

app_name = 'feed'
urlpatterns = [
    # HTML visible pages
    path('', views.feed, name='feed'),  # main view (feed)
    path('login', views.login, name='login'),  # the login page
    path('user/<int:user_id>/', views.user_profile, name='user_profile'),  # the user profile page

    # APIs endpoints
    path('post/<int:post_id>/a', views.post_api, name='post_api'),  # api endpoint for interacting with posts
    path('auth', views.auth, name='auth'),  # auth endpoint
]
