from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count
from apps.blog.models import Post

from .models import Newsletter
from .forms import NewsletterForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        posts = {
            'latest': Post.objects.all().order_by('-created_date')[:9],
            'popular': Post.objects.annotate(
                likes_count=Count('likes')
            ).order_by('-likes_count').first()
        }
        return render(request, 'index.html', {'posts': posts})


class NewsletterView(View):

    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # TODO: complete method's functionality (success pop up and failure)
