from rest_framework import serializers
from apps.accounts.models import Profile

from ...models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class PostSerializer(serializers.ModelSerializer):
    snippet = serializers.CharField(source='get_snippet', read_only=True)
    category = CategorySerializer()

    class Meta:
        model = Post
        fields = [
            'id',
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
            'author',
            'snippet',
            'created_date',
            'updated_date'
        ]
        write_only_fields = ['content']

    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(
            user=self.context.get('request').user
        )
        return super().create(validated_data)
