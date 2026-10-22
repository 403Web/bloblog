from django.urls import path

from .views import (
    CommentCreateView,
    CommentEditView,
    CommentDeleteView,
    ReplyCreateView,
    CommentLikeView
)


app_name = 'comment'


urlpatterns = [
    path('<int:post_pk>/comment/create/', CommentCreateView.as_view(), name='comment_create'),
    path('<int:post_pk>/comment/<int:comment_pk>/edit/', CommentEditView.as_view(), name='comment_edit'),
    path('<int:post_pk>/comment/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('<int:post_pk>/comment/<int:parent_pk>/reply/create/', ReplyCreateView.as_view(), name='reply_create'),
    path('<int:post_pk>/comment/<int:comment_pk>/like/', CommentLikeView.as_view(), name='comment_like')
]
