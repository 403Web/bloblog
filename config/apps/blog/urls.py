from django.urls import path
from .views import PostRetrieveView


app_name = 'blog'


urlpatterns = [
    path('posts/<pk>/', PostRetrieveView.as_view(), name='post_detail')
]
