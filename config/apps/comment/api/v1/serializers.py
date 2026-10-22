from rest_framework import serializers
from django.urls import reverse

from ...models import Comment, CommentLike


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'url',
            'user',
            'content',
            'likes',
            'created_date',
            'updated_date',
            'replies'
        ]
        read_only_fields = [
            'id',
            'url',
            'user',
            'likes',
            'created_date',
            'updated_date',
            'replies'
        ]

    def get_url(self, obj):
        request = self.context.get('request')

        relative = reverse(
            'comment_api_v1:comment-detail', kwargs={
                'post_pk': obj.post.pk,
                'comment_pk': obj.pk
            }
        )
        absolute = request.build_absolute_uri(relative) if request else None

        return {
            'absolute': absolute,
            'relative': relative
        }

    def get_likes(self, obj):
        request = self.context.get('request')

        likes_count = obj.likes.count()
        liked_by_user = (
            CommentLike.objects.filter(
                user=request.user.profile,
                comment=obj
            ).exists()
            if request.user.is_authenticated
            else None
        )

        return {
            'count': likes_count,
            'by_user': liked_by_user
        }

    def get_replies(self, obj):
        depth = int(self.context.get('request').query_params.get('depth', 2))

        if depth == 0:
            return CommentSerializer(
                obj.replies.all(),
                many=True,
                context=self.context
            ).data

        current_depth = self.context.get('current_depth', 0)
        if current_depth >= depth:
            request = self.context.get('request')

            relative = reverse(
                'comment_api_v1:comment_replies',
                kwargs={'post_pk': obj.post.pk, 'comment_pk': obj.pk}
            )
            absolute = request.build_absolute_uri(relative) if request else None

            return {
                'absolute': absolute,
                'relative': relative
            }

        return CommentSerializer(
            obj.replies.all(),
            many=True,
            context={
                **self.context,
                'current_depth': current_depth + 1
            }
        ).data

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs').get('comment_pk'):
            rep.pop('url', None)

        return rep


class ActionSerializer(serializers.Serializer):
    pass


class ReplyActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['content']
