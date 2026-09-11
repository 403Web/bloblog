from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    model = Post
    ordering = ('-created_date',)
    readonly_fields = ('created_date', 'updated_date')
    list_display = ('author', 'id', 'created_date', 'updated_date')
    search_fields = ('id', 'author', 'title', 'content')


admin.site.register(Post, PostAdmin)
