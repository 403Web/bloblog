from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from .paginations import PostPagination
from ...models import Post


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
    ordering_fields = ['created_date']
