from django.shortcuts import render
from django.views import View
from django.db.models import Count
from apps.blog.models import Post


class IndexView(View):

    def get(self, request, *args, **kwargs):
        posts = {
            'latest': Post.objects.all().order_by('-created_date')[:9],
            'popular': Post.objects.annotate(
                likes_count=Count('likes')
            ).order_by('-likes_count').first()
        }
        return render(request, 'index.html', {'posts': posts})
