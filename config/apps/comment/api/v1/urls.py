from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from apps.blog.api.v1.views import PostViewSet

from .views import CommentViewSet, ReplyListAPIView


app_name = 'comment_api_v1'


router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')

nested_router = NestedDefaultRouter(router, 'posts', lookup='post')
nested_router.register('comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(nested_router.urls)),
    path(
        'posts/<int:post_pk>/comments/<int:comment_pk>/replies/',
        ReplyListAPIView.as_view(),
        name='comment_replies'
    )
]
