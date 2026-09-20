from django.urls import path

from .views import (
    RedirectToIndexView,
    PostListView,
    PostRetrieveView,
    PostCreateView
)


app_name = 'blog'


urlpatterns = [
    path('', RedirectToIndexView.as_view(), name='index'),
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', PostRetrieveView.as_view(), name='post_detail'),
    path('posts/create/', PostCreateView.as_view(), name='post_create')
]
