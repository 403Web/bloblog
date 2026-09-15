from rest_framework import serializers
from django.urls import reverse
from apps.accounts.models import Profile

from ...models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    snippet = serializers.CharField(source='get_snippet', read_only=True)
    category = CategorySerializer()

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
            'created_date',
            'updated_date'
        ]
        read_only_fields = [
            'id',
            'url',
            'author',
            'snippet',
            'created_date',
            'updated_date'
        ]
        write_only_fields = ['content']

    def get_url(self, obj):
        request = self.context.get('request')
        relative = reverse('blog_api_v1:post-detail', kwargs={'pk': obj.pk})
        absolute = request.build_absolute_uri(relative) if request else None
        return {
            'absolute': absolute,
            'relative': relative
        }

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)
        if request.parser_context.get('kwargs').get('pk'):
            rep.pop('url', None)
            rep.pop('snippet', None)
        else:
            rep.pop('content', None)
        return rep

    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(
            user=self.context.get('request').user
        )
        return super().create(validated_data)
