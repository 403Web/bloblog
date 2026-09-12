from django.contrib import admin

from .models import Post, PostLike, Category


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


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'id')
    search_fields = ('id', 'name')


admin.site.register(Post, PostAdmin)
admin.site.register(PostLike, PostLikeAdmin)
admin.site.register(Category, CategoryAdmin)
