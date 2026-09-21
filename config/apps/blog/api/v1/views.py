from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework import status

from .serializers import PostSerializer, CategorySerializer, ActionSerializer
from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from .paginations import PostPagination
from ...models import Post, PostLike, Category


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
    ]
    pagination_class = PostPagination
    filterset_fields = ['category', 'category__name']
    search_fields = ['title', 'content']
    ordering_fields = ['created_date', 'likes']

    @action(
        methods=['POST'],
        detail=True,
        serializer_class=ActionSerializer,
        permission_classes=[IsAuthenticated]
    )
    def like(self, request, pk=None):
        post = self.get_object()

        if PostLike.objects.filter(
            user=request.user.profile, post=post
        ).exists():
            return Response(
                {'detail': 'You have already liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        PostLike.objects.create(
            user=request.user.profile,
            post=post
        )
        return Response(
            {'detail': 'You liked this post successfully.'},
            status=status.HTTP_201_CREATED
        )

    @action(methods=['DELETE'], detail=True, permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()

        if not PostLike.objects.filter(
            user=request.user.profile, post=post
        ).exists():
            return Response(
                {'detail': 'You have not liked this post.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        PostLike.objects.get(
            user=request.user.profile, post=post
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
