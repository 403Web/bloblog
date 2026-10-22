from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from apps.blog.models import Post
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework import status

from ...models import Comment, CommentLike
from .serializers import CommentSerializer, ActionSerializer, ReplyActionSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import CommentPaginator


class CommentViewSet(ModelViewSet):
    lookup_url_kwarg = 'comment_pk'
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    pagination_class = CommentPaginator
    ordering_fields = ['created_date', 'likes']

    def get_queryset(self):
        return Comment.objects.filter(
            post__pk=self.kwargs.get('post_pk'), parent=None
        )

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))

        serializer.save(user=self.request.user.profile, post=post)

    @action(
        methods=['POST'],
        detail=True,
        serializer_class=ActionSerializer,
        permission_classes=[IsAuthenticated]
    )
    def like(self, request, post_pk=None, comment_pk=None):
        comment = self.get_object()
        
        if CommentLike.objects.filter(
            user=request.user.profile, comment=comment
        ).exists():
            return Response(
                {'detail': 'You have already liked this comment.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        CommentLike.objects.create(
            user=request.user.profile,
            comment=comment
        )
        return Response(
            {'detail': 'You liked this comment successfully.'},
            status=status.HTTP_201_CREATED
        )

    @action(methods=['DELETE'], detail=True, permission_classes=[IsAuthenticated])
    def unlike(self, request, post_pk=None, comment_pk=None):
        comment = self.get_object()
        
        if not CommentLike.objects.filter(
            user=request.user.profile, comment=comment
        ).exists():
            return Response(
                {'detail': 'You have not liked this comment.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        CommentLike.objects.get(
            user=request.user.profile, comment=comment
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST'],
        detail=True,
        serializer_class=ReplyActionSerializer,
        permission_classes=[IsAuthenticated]
    )
    def reply(self, request, post_pk=None, comment_pk=None):
        comment = get_object_or_404(Comment, pk=comment_pk)

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            user=request.user.profile,
            post=comment.post,
            parent=comment
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReplyListAPIView(ListAPIView):
    lookup_url_kwarg = 'comment_pk'
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    pagination_class = CommentPaginator
    ordering_fields = ['created_date', 'likes']

    def get_queryset(self):
        return Comment.objects.filter(parent__pk=self.kwargs.get('comment_pk'))
