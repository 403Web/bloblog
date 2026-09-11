from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    ordering = ('created_date',)
    readonly_fields = ('created_date', 'updated_date')
    list_display = ('user', 'id', 'post', 'created_date', 'updated_date')
    search_fields = ('id', 'content')


admin.site.register(Comment, CommentAdmin)
