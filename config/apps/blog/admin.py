from django.contrib import admin

from .models import Post, PostLike


class PostAdmin(admin.ModelAdmin):
    model = Post
    ordering = ('-created_date',)
    readonly_fields = ('created_date', 'updated_date')
    list_display = ('author', 'id', 'created_date', 'updated_date')
    search_fields = ('id', 'author', 'title', 'content')


class PostLikeAdmin(admin.ModelAdmin):
    model = PostLike
    ordering = ('-created_date',)
    readonly_fields = ('created_date',)
    list_display = ('user', 'id', 'post', 'created_date')
    search_fields = ('id',)


admin.site.register(Post, PostAdmin)
admin.site.register(PostLike, PostLikeAdmin)
