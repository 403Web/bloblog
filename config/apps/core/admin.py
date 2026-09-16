from django.contrib import admin
from .models import Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    ordering = ('-created_date',)
    readonly_fields = ('created_date',)
    list_display = ('email', 'id', 'created_date')
    search_fields = ('id', 'email')


admin.site.register(Newsletter, NewsletterAdmin)
