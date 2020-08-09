from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='feed'),
    path('post/', views.index), # redirect to the feed
    # path('post/<int:post_id>/', views.postApi), #TODO: show just the post identified. For now, redirect to Feed view
    path('post/<int:post_id>/a', views.post_api, name='post_api')
]
