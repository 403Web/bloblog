from rest_framework import serializers
from django.urls import reverse

from ...models import Post, PostView, PostLike, Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    snippet = serializers.CharField(source='get_snippet', read_only=True)
    category = CategorySerializer(read_only=True)
    category_pk = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True
    )
    likes = serializers.SerializerMethodField()
    views = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'url',
            'author',
            'image',
            'title',
            'content',
            'snippet',
            'category',
            'category_pk',
            'likes',
            'views',
            'comments',
            'created_date',
            'updated_date'
        ]
        read_only_fields = [
            'id',
            'url',
            'author',
            'snippet',
            'category',
            'likes',
            'views',
            'comments',
            'created_date',
            'updated_date'
        ]
        write_only_fields = ['content', 'category_pk']

    def get_url(self, obj):
        request = self.context.get('request')

        relative = reverse('blog_api_v1:post-detail', kwargs={'pk': obj.pk})
        absolute = request.build_absolute_uri(relative) if request else None

        return {
            'absolute': absolute,
            'relative': relative
        }

    def get_likes(self, obj):
        request = self.context.get('request')

        liked_by_user = (
            PostLike.objects.filter(
                user=request.user.profile,
                post=obj
            ).exists()
            if request.user.is_authenticated
            else None
        )
        likes_count = obj.likes.count()

        return {
            'count': likes_count,
            'by_user': liked_by_user
        }

    def get_views(self, obj):
        request = self.context.get('request')

        viewed_by_user = (
            PostView.objects.filter(
                user=request.user.profile,
                post=obj
            ).exists()
            if request.user.is_authenticated
            else None
        )
        views_count = obj.views.count()

        return {
            'count': views_count,
            'by_user': viewed_by_user
        }

    def get_comments(self, obj):
        request = self.context.get('request')

        relative = reverse('comment_api_v1:comment-list', kwargs={'post_pk': obj.pk})
        absolute = request.build_absolute_uri(relative) if request else None

        return {
            'count': obj.comments.count(),
            'url': {
                'absolute': absolute,
                'relative': relative
            }
        }

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('url', None)
            rep.pop('snippet', None)
        else:
            rep.pop('content', None)
            rep['comments'] = rep.get('comments').get('count')

        return rep

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user.profile
        return super().create(validated_data)


class ActionSerializer(serializers.Serializer):
    pass
