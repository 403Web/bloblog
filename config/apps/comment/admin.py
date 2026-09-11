from django.contrib import admin
from .models import Comment, CommentLike


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    ordering = ('created_date',)
    readonly_fields = ('created_date', 'updated_date')
    list_display = ('user', 'id', 'post', 'created_date', 'updated_date')
    search_fields = ('id', 'content')


class CommentLikeAdmin(admin.ModelAdmin):
    model = CommentLike
    ordering = ('-created_date',)
    readonly_fields = ('created_date',)
    list_display = ('user', 'id', 'comment', 'created_date')
    search_fields = ('id',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(CommentLike, CommentLikeAdmin)
